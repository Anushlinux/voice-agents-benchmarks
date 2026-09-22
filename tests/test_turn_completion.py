"""Regressions for interrupted input and preparing an already accepted offer."""

import asyncio
import base64
from contextlib import nullcontext
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
from uuid import uuid4

import pytest
from test_caller import Session, Socket, caller
from test_natural_restaurant import catalog as catalog
from test_natural_restaurant import context, query
from test_reservations import observations

from voice_bench.business.environment import WORKFLOWS, BusinessService
from voice_bench.business.natural_restaurant import NaturalRestaurantWorkflowV5
from voice_bench.caller.responses import ResponseCoordinator
from voice_bench.evaluation.natural_restaurant import consent_boundary, natural_metrics
from voice_bench.evaluation.scoring import load_bundle
from voice_bench.evidence.local import LocalEvidence
from voice_bench.models import CounterpartBrief
from voice_bench.restaurant_natural import convert_catalog
from voice_bench.runtime import validate_live
from voice_bench.settings import load_config


@pytest.mark.asyncio
async def test_worker_and_grader_accept_heard_terms_before_internal_offer(catalog, tmp_path):
    case = convert_catalog(catalog)[0]
    # Execute and grade with the case's own workflow; version 6 inherits this rule from 5.
    workflow = WORKFLOWS[(case.workflow, case.workflow_version)]
    sink = LocalEvidence(tmp_path, uuid4(), uuid4())
    run = {
        "workflow": case.workflow,
        "workflow_version": case.workflow_version,
        "state": workflow.initialize(case.initial_state),
        "user_task_served": True,
        "accept_tools": True,
        "operations": {},
        "audit": [],
        "tool_access": {"counterpart": list(workflow.tools)},
    }
    service = BusinessService(SimpleNamespace(locked_run=lambda _: nullcontext(run)))
    await sink.emit("controller", "connected")
    lookup = service.execute(
        sink.run_id,
        "check_availability",
        query(),
        "lookup",
        actor="counterpart",
        observations=await sink.event_snapshot(),
    )
    await sink.emit(
        "business",
        "business_tool_result",
        {
            "actor": "counterpart",
            "operation_id": "lookup",
            "tool": "check_availability",
            "result": lookup,
        },
    )
    # The employee speaks the quote completely, then the caller requests a booking.
    for event in observations(sink.run_id):
        await sink.emit(event["source"], event["kind"], event["payload"])
    offer = service.execute(
        sink.run_id,
        "offer_reservation",
        {"option_id": "evening"},
        "offer",
        actor="counterpart",
        observations=await sink.event_snapshot(),
    )
    await sink.emit(
        "business",
        "business_tool_result",
        {
            "actor": "counterpart",
            "operation_id": "offer",
            "tool": "offer_reservation",
            "result": offer,
        },
    )
    result = service.execute(
        sink.run_id,
        "record_reservation",
        {"offer_id": offer["offer"]["offer_id"], "booking_name": "Asha Rao"},
        "book",
        actor="counterpart",
        observations=await sink.event_snapshot(),
    )
    assert result["ok"], "Internal offer preparation must not require repeating heard terms"
    await sink.emit("business", "reservation_action", {"operation_id": "book", "result": result})
    value = case.model_dump(mode="json")
    for name, content in {
        "config/case.json": value,
        "business/final.json": run["state"],
        "business/audit.json": run["audit"],
    }.items():
        await sink.json(name, content)
    await sink.finalize(sink.run_id)
    _, refs = load_bundle(sink.directory)
    metric = next(
        m
        for m in natural_metrics(sink.directory, value, refs, run["state"], run["audit"])
        if m.name == "reservation_history"
    )
    assert metric.status == "met"


@pytest.mark.asyncio
@pytest.mark.parametrize("pause_at", ["factory", "evidence"])
async def test_new_input_while_preparing_response_defers_until_committed(pause_at):
    entered, release = asyncio.Event(), asyncio.Event()
    sent = asyncio.Queue()
    blocked = False

    async def pause(stage):
        if stage == pause_at and not release.is_set():
            entered.set()
            await release.wait()

    class Evidence:
        async def emit(self, *args):
            await pause("evidence")

    async def factory():
        await pause("factory")
        return {"type": "response.create"}

    coordinator = ResponseCoordinator(sent.put, Evidence(), factory, lambda: blocked)
    task = asyncio.create_task(coordinator.run())
    try:
        coordinator.request("tool_results")
        await asyncio.wait_for(entered.wait(), 1)
        blocked = True
        release.set()
        await asyncio.sleep(0.03)
        assert sent.empty(), "Preparing a reply must not reserve the right to interrupt"
        assert coordinator.idle.is_set()
        blocked = False
        coordinator.request("committed_input")
        assert await asyncio.wait_for(sent.get(), 1) == {"type": "response.create"}
        assert sent.empty()
    finally:
        coordinator.close()
        await task


@pytest.mark.asyncio
async def test_cancel_before_created_discards_late_audio_and_completed_tools(tmp_path):
    evidence = LocalEvidence(tmp_path, uuid4(), uuid4())
    session, socket = Session(evidence, 24000), Socket()
    simulator = caller(socket)
    task = asyncio.create_task(
        simulator.converse(
            None,
            CounterpartBrief(role="Employee", goal="Listen", known_facts={}),
            session,
            evidence,
        )
    )
    try:
        async with asyncio.timeout(3):
            await socket.sent.get()
            await socket.incoming.put({"type": "session.updated", "session": {}})
            await socket.incoming.put({"type": "input_audio_buffer.committed", "item_id": "first"})
            assert (await socket.sent.get())["type"] == "response.create"
            # Caller interrupts before the response-created acknowledgement arrives.
            await socket.incoming.put(
                {"type": "input_audio_buffer.speech_started", "item_id": "second"}
            )
            await socket.incoming.put({"type": "response.created", "response": {"id": "old"}})
            assert await socket.sent.get() == {"type": "response.cancel", "response_id": "old"}
            await socket.incoming.put(
                {
                    "type": "response.output_audio.delta",
                    "response_id": "old",
                    "item_id": "late",
                    "delta": base64.b64encode(b"\x02\x00" * 2400).decode(),
                }
            )
            assert (await socket.sent.get())["audio_end_ms"] == 0
            await socket.incoming.put(
                {
                    "type": "response.function_call_arguments.done",
                    "response_id": "old",
                    "name": "finish_counterpart",
                    "call_id": "stale-finish",
                }
            )
            # Cancellation can race with a completed acknowledgement. Intent still matters.
            await socket.incoming.put(
                {"type": "response.done", "response": {"id": "old", "status": "completed"}}
            )
            await socket.incoming.put(
                {"type": "input_audio_buffer.speech_stopped", "item_id": "second"}
            )
            await asyncio.sleep(0.05)
            assert not task.done(), "An interrupted finish tool must not close the call"
            assert socket.sent.empty(), "Speech stop alone is not a committed caller turn"
            events = await evidence.event_snapshot()
            assert any(e["kind"] == "cancelled_tools_discarded" for e in events)
            assert any(e["kind"] == "audio_discarded_after_interruption" for e in events)
            assert not any(e["kind"] == "sent_block" for e in events)
            await socket.incoming.put({"type": "input_audio_buffer.committed", "item_id": "second"})
            assert (await socket.sent.get())["type"] == "response.create"
    finally:
        task.cancel()
        await asyncio.gather(task, return_exceptions=True)
        await session.close("test")


@pytest.mark.asyncio
async def test_interruption_during_closing_playback_reopens_conversation(tmp_path):
    evidence = LocalEvidence(tmp_path, uuid4(), uuid4())
    entered, release = asyncio.Event(), asyncio.Event()

    class ClosingSession(Session):
        async def drain(self):
            entered.set()
            await release.wait()

    session, socket = ClosingSession(evidence, 24000), Socket()
    task = asyncio.create_task(
        caller(socket).converse(
            None,
            CounterpartBrief(role="Employee", goal="Listen", known_facts={}),
            session,
            evidence,
        )
    )
    try:
        async with asyncio.timeout(3):
            await socket.sent.get()
            await socket.incoming.put({"type": "session.updated", "session": {}})
            await socket.incoming.put(
                {
                    "type": "response.function_call_arguments.done",
                    "response_id": "closing",
                    "name": "finish_counterpart",
                    "call_id": "finish",
                }
            )
            await socket.incoming.put(
                {"type": "response.done", "response": {"id": "closing", "status": "completed"}}
            )
            await entered.wait()
            await socket.incoming.put(
                {"type": "input_audio_buffer.speech_started", "item_id": "correction"}
            )
            # Ensure the input event has been handled before closing audio drains.
            while not any(
                e["kind"] == "target_speech_detected" for e in await evidence.event_snapshot()
            ):
                await asyncio.sleep(0.005)
            release.set()
            rejected_finish = await socket.sent.get()
            assert rejected_finish["item"]["call_id"] == "finish"
            assert "new_input_received" in rejected_finish["item"]["output"]
            await socket.incoming.put(
                {"type": "input_audio_buffer.speech_stopped", "item_id": "correction"}
            )
            await asyncio.sleep(0.03)
            assert socket.sent.empty() and not task.done()
            await socket.incoming.put(
                {"type": "input_audio_buffer.committed", "item_id": "correction"}
            )
            assert (await socket.sent.get())["type"] == "response.create"
            assert not task.done()
    finally:
        task.cancel()
        await asyncio.gather(task, return_exceptions=True)
        await session.close("test")


@pytest.mark.parametrize("change", ["none", "price", "dietary", "missing_result", "stale_speech"])
def test_existing_agreement_survives_late_offer_preparation_only_for_unchanged_terms(
    catalog, change
):
    workflow = NaturalRestaurantWorkflowV5()
    state = workflow.initialize(convert_catalog(catalog)[0].initial_state)
    lookup = workflow.execute(state, "check_availability", query(), context=context(1, "lookup"))
    if change == "price":
        option = next(o for o in state["options"] if o["option_id"] == "evening")
        option["total_inr"] += 100
        option["remaining_due_inr"] += 100
    offer = workflow.execute(
        state,
        "offer_reservation",
        {"option_id": "evening", "without_onion_garlic_guests": 2 if change == "dietary" else 0},
        context={
            **context(20),
            "tool_result_sequences": {} if change == "missing_result" else {"lookup": 2},
        },
    )["offer"]
    result = workflow.execute(
        state,
        "record_reservation",
        {"offer_id": offer["offer_id"], "booking_name": "Asha Rao"},
        context={
            **context(21, "book"),
            "consent_anchors": {
                "event_sequences": [0, 1] if change == "stale_speech" else [3, 4, 5, 6]
            },
        },
    )
    assert result["ok"] is (change == "none")
    events = [
        {
            "kind": "business_tool_result",
            "sequence": 2,
            "payload": {
                "actor": "counterpart",
                "tool": "check_availability",
                "operation_id": "lookup",
                "result": lookup,
            },
        }
    ]
    assert consent_boundary({"workflow_version": "5"}, offer, events) == workflow.consent_cutoff(
        offer
    )
    assert consent_boundary({"workflow_version": "4"}, offer, events) == 20
    tampered = deepcopy(events)
    tampered[0]["payload"]["operation_id"] = "another-lookup"
    assert consent_boundary({"workflow_version": "5"}, offer, tampered) == 20
    assert consent_boundary({"workflow_version": "5"}, offer, []) == 20


@pytest.mark.parametrize("channel", ["browser", "phone"])
def test_new_cases_reject_the_old_pause_based_turn_configuration(catalog, channel):
    config = load_config(Path("configs/restaurant-natural.example.toml"))
    config = config.model_copy(update={"channels": (channel,)})
    case = convert_catalog(catalog)[0]
    for turn in (
        {"type": "server_vad", "silence_duration_ms": 500},
        {"type": "semantic_vad", "eagerness": "high"},
    ):
        old = config.model_copy(
            update={"counterpart": config.counterpart.model_copy(update={"turn_detection": turn})}
        )
        with pytest.raises(ValueError, match="requires semantic_vad"):
            validate_live(old, [case])
    # The current example clears turn validation and stops at the ordinary funding check.
    with pytest.raises(ValueError, match="funded limits"):
        validate_live(config, [case])
