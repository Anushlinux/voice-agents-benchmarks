"""Synthetic state/audio checks. None are additional benchmark datapoints."""

from copy import deepcopy
from pathlib import Path
from uuid import uuid4

import pytest
from test_reservations import MemoryStore, observations
from test_reservations import custom_case as custom_case
from test_reservations import inventory as inventory

from voice_bench.business.dining import DiningWorkflow
from voice_bench.business.environment import BusinessService
from voice_bench.caller.conversation_events import ConversationEventDriver
from voice_bench.contracts import ConversationEvent, ExecutionCase
from voice_bench.evaluation.conversation_events import (
    ConversationEventReview,
    observe_events,
    review_events,
)
from voice_bench.evaluation.scoring import deterministic, load_bundle
from voice_bench.evidence.local import LocalEvidence
from voice_bench.restaurant_case import import_case
from voice_bench.restaurant_hard_cases import HARD_IDS, convert_variants


@pytest.fixture
def dining_store(inventory):
    store = MemoryStore(inventory)
    run = store.runs[store.id]
    run["workflow_version"] = "2"
    run["state"] = DiningWorkflow().initialize(
        {
            "inventory": inventory,
            "bookings": [],
            "dining_policy": {
                "opening_total_inr": 13200,
                "minimum_total_inr": 12000,
                "max_without_onion_garlic_guests": 8,
            },
        }
    )
    run["tool_access"]["counterpart"] = list(DiningWorkflow.tools)
    return store


def invoke(store, tool, args, operation=None, offset=0):
    events = observations(store.id)
    for event in events:
        event["sequence"] += offset
    return BusinessService(store).execute(
        store.id, tool, args, operation or str(uuid4()), actor="counterpart", observations=events
    )


def quote(store):
    return invoke(store, "quote_reservation", {"option_id": "4"})["quote"]


def prepare(store, q, offset=0):
    return invoke(
        store,
        "prepare_confirmation",
        {"quote_id": q["quote_id"], "booking_name": "Test User"},
        offset=offset,
    )["confirmation"]


def test_opening_quote_negotiation_and_scope(dining_store):
    store = dining_store
    opening = quote(store)
    assert opening["dining_total_inr"] == 13200
    assert "minimum_total_inr" not in opening
    assert (
        invoke(store, "counteroffer", {"quote_id": opening["quote_id"], "total_inr": 11999})[
            "error"
        ]
        == "offer_outside_policy"
    )
    lower = invoke(store, "counteroffer", {"quote_id": opening["quote_id"], "total_inr": 12000})[
        "quote"
    ]
    assert lower["quote_id"] != opening["quote_id"]
    assert lower["dining_total_inr"] == 12000
    assert lower["reservation_charge_inr"] == 0 and lower["payment_status"] == "not_requested"
    service = BusinessService(store)
    assert (
        service.execute(store.id, "counteroffer", {}, "target", actor="target")["error"]
        == "forbidden_tool"
    )


def test_available_but_over_budget_offer_is_not_silently_fixed(dining_store):
    opening = quote(dining_store)
    confirmation = prepare(dining_store, opening)
    result = invoke(
        dining_store,
        "record_reservation",
        {"confirmation_id": confirmation["confirmation_id"]},
        offset=10,
    )
    assert result["ok"] and result["reservation"]["dining_total_inr"] == 13200


@pytest.mark.parametrize("change", ["price", "diet", "option", "new_confirmation"])
def test_revisions_invalidate_previous_confirmation(dining_store, change):
    store = dining_store
    q = quote(store)
    previous = prepare(store, q)
    if change == "price":
        invoke(store, "counteroffer", {"quote_id": q["quote_id"], "total_inr": 12000})
    elif change == "diet":
        invoke(
            store,
            "set_dietary_requirements",
            {"quote_id": q["quote_id"], "without_onion_garlic_guests": 2},
        )
    elif change == "option":
        invoke(store, "quote_reservation", {"option_id": "3"})
    else:
        prepare(store, q, offset=5)
    result = invoke(
        store, "record_reservation", {"confirmation_id": previous["confirmation_id"]}, offset=20
    )
    assert result["error"] == "stale_confirmation"
    assert not store.run(store.id)["state"]["bookings"]


def test_fresh_readback_required_and_duplicate_write_replays(dining_store):
    store = dining_store
    confirmation = prepare(store, quote(store), offset=10)
    args = {"confirmation_id": confirmation["confirmation_id"]}
    assert invoke(store, "record_reservation", args, offset=0)["error"] == "fresh_consent_required"
    first = invoke(store, "record_reservation", args, operation="book", offset=20)
    assert first["ok"]
    assert invoke(store, "record_reservation", args, operation="book", offset=30) == first
    assert len(store.run(store.id)["state"]["bookings"]) == 1


def test_dietary_semantics_are_explicit_and_physical_limits_apply(dining_store):
    store = dining_store
    q = quote(store)
    assert q["without_onion_garlic_guests"] == 0
    assert (
        invoke(
            store,
            "set_dietary_requirements",
            {"quote_id": q["quote_id"], "without_onion_garlic_guests": 9},
        )["error"]
        == "dietary_capacity_unavailable"
    )
    revised = invoke(
        store,
        "set_dietary_requirements",
        {"quote_id": q["quote_id"], "without_onion_garlic_guests": 2},
    )["quote"]
    assert revised["without_onion_garlic_guests"] == 2
    assert revised["dining_total_inr"] == q["dining_total_inr"]


def challenge(event_id="time", occurrence=1, kind="misread"):
    return ConversationEvent(
        event_id=event_id,
        trigger_tool="prepare_confirmation",
        occurrence=occurrence,
        after_tools=("check_availability",),
        kind=kind,
        field="time",
        spoken_value="20:00",
        instruction="Misread the time once; yield to correction and restore accurate terms.",
    )


@pytest.mark.asyncio
async def test_event_triggers_require_success_prerequisites_and_unique_operations(tmp_path):
    evidence = LocalEvidence(tmp_path, uuid4(), uuid4())
    driver = ConversationEventDriver([challenge(), challenge("seating", 2)])
    driver.after_tool("prepare_confirmation", {"ok": False}, "failed")
    assert not driver.pending
    driver.after_tool("check_availability", {"ok": True}, "availability")
    driver.after_tool("prepare_confirmation", {"ok": True}, "first")
    driver.after_tool("prepare_confirmation", {"ok": True}, "first")
    request = await driver.response_request(evidence, "Private desk instructions only")
    assert request["response"]["metadata"] == {"conversation_event_id": "time"}
    assert "hypothetical Rumik response" in request["response"]["instructions"]
    assert not driver.pending
    driver.after_tool("prepare_confirmation", {"ok": True}, "second")
    second = await driver.response_request(evidence, "Desk")
    assert second["response"]["metadata"]["conversation_event_id"] == "seating"
    await driver.observe({"type": "response.created", "response": {"id": "unrelated"}}, evidence)
    assert not driver.responses
    await driver.observe(
        {
            "type": "response.created",
            "response": {"id": "linked", "metadata": {"conversation_event_id": "time"}},
        },
        evidence,
    )
    await driver.observe(
        {"type": "response.output_audio.delta", "response_id": "linked", "item_id": "audio"},
        evidence,
    )
    assert (
        len([e for e in await evidence.event_snapshot() if e["kind"] == "conversation_event_audio"])
        == 1
    )
    await driver.finish(evidence)
    evidence.close_writer()


@pytest.fixture
def variant_specs(custom_case):
    baseline = import_case(*custom_case).model_dump(mode="json")
    specs = []
    for n, case_id in enumerate(HARD_IDS, 1):
        expected = {
            **baseline["criteria"]["reservation_expected"],
            "dining_total_inr": 0 if n == 1 else 12000,
            "without_onion_garlic_guests": 2 if n == 3 else 0,
            "all_inclusive": True,
            "deposit_inr": 0,
            "cancellation_fee_inr": 0,
            "payment_status": "not_requested",
        }
        user = deepcopy(baseline["user_task"])
        user["known_facts"]["dining_budget_inr"] = expected["dining_total_inr"]
        specs.append(
            {
                "case_id": case_id,
                "parent_case_id": baseline["case_id"],
                "authored_extensions": ["Synthetic test fixture"],
                "agent_brief": user,
                "simulator_brief": baseline["counterpart"],
                "expected_outcome": expected,
                "rubrics": {},
                "dining_policy": {
                    "opening_total_inr": 0 if n == 1 else 13200,
                    "minimum_total_inr": 0 if n == 1 else 12000,
                    "max_without_onion_garlic_guests": 8,
                },
                "conversation_events": [challenge().model_dump(mode="json")],
            }
        )
    return baseline, specs


def test_exactly_three_variants_role_separation_and_baseline_preservation(variant_specs):
    baseline, specs = variant_specs
    before = deepcopy(baseline)
    cases = convert_variants(baseline, specs)
    assert len(cases) == 3 and baseline == before
    assert ExecutionCase.model_validate(baseline).conversation_events == ()
    for case in cases:
        assert not case.target_tools
        assert "dining_policy" not in case.user_task.model_dump_json()
        assert "conversation_events" not in case.user_task.model_dump_json()
        assert "dining_budget_inr" not in case.counterpart.model_dump_json()
        assert case.criteria["provenance"]["authored_variant"]
        assert "consent_alignment" in case.criteria["required_metrics"]
    assert "negotiation_behavior" in cases[1].criteria["required_metrics"]
    assert "dietary_understanding" in cases[2].criteria["required_metrics"]
    with pytest.raises(ValueError, match="exactly"):
        convert_variants(baseline, specs[:2])


@pytest.mark.parametrize("damage", ["price", "diet", "payment", "physical", "budget"])
def test_impossible_variants_are_rejected(variant_specs, damage):
    baseline, specs = variant_specs
    expected = specs[2]["expected_outcome"]
    if damage == "price":
        expected["dining_total_inr"] = 11999
    if damage == "diet":
        expected["without_onion_garlic_guests"] = 9
    if damage == "payment":
        expected["deposit_inr"] = 100
    if damage == "physical":
        expected["time"] = "22:00"
    if damage == "budget":
        specs[2]["agent_brief"]["known_facts"]["dining_budget_inr"] = 1000
    with pytest.raises(ValueError):
        convert_variants(baseline, specs)


async def audio_bundle(tmp_path, *, overlap=True, linked=True, played=True, mapped=True):
    from voice_bench.channels.media import AudioRecorder
    from voice_bench.models import AudioFrame

    evidence = LocalEvidence(tmp_path, uuid4(), uuid4())
    await evidence.emit("caller", "conversation_event_requested", challenge().model_dump())
    if linked:
        await evidence.emit(
            "caller", "conversation_event_audio", {"event_id": "time", "item_id": "desk"}
        )
    if played:
        await evidence.emit(
            "channel",
            "playback_progress",
            {
                "item_id": "desk",
                "played_ms": 1000,
                "sample": 0,
                "samples": 8000,
                "rate": 8000,
                "boundary": "browser_render",
            },
            clock_id="chromium-audio-context",
        )
    recorder = AudioRecorder(evidence)
    for name, kind in (("played", "rendered_block"), ("received", "received_block")):
        samples = bytearray(16000 * 2)
        start, end = (
            (0, 8000) if name == "played" else ((4000, 12000) if overlap else (8800, 14400))
        )
        samples[start * 2 : end * 2] = b"\x00\x10" * (end - start)
        await recorder.write(
            name,
            AudioFrame(
                pcm_s16le=bytes(samples),
                sample_rate_hz=8000,
                sample_offset=0,
                observed_monotonic_ns=0,
                clock_id="synthetic",
            ),
        )
        if mapped:
            await evidence.emit(
                "channel",
                kind,
                {"sample": 0, "samples": 16000, "recording_offset": 0, "rate": 8000},
                clock_id="chromium-audio-context",
            )
    await recorder.close()
    await evidence.finalize(evidence.run_id)
    evidence.close_writer()
    return evidence.directory, {"conversation_events": [challenge().model_dump()]}


@pytest.mark.asyncio
@pytest.mark.parametrize("mode", ["overlap", "waited", "unlinked", "unplayed", "unmapped"])
async def test_audio_proves_overlap_but_not_semantic_correction(tmp_path, mode):
    directory, case = await audio_bundle(
        tmp_path,
        overlap=mode != "waited",
        linked=mode != "unlinked",
        played=mode != "unplayed",
        mapped=mode != "unmapped",
    )
    _, refs = load_bundle(directory)
    result = observe_events(directory, case, refs)[0]
    assert result["challenge_result"] == "untested"
    if mode == "overlap":
        assert result["overlap_ms"] == 500
        assert result["audio_overlap_status"] == "overlap_observed"
    elif mode == "unmapped":
        assert result["audio_overlap_status"] == "uncertain"
    else:
        assert result["audio_overlap_status"] == "interruption_not_observed"
    review = ConversationEventReview(
        event_id="time",
        delivered="met",
        correction="met",
        resumption="met",
        explanation="Synthetic listening test",
        evidence=tuple(refs.values()),
    )
    if mode in {"unlinked", "unplayed"}:
        with pytest.raises(ValueError, match="unplayed"):
            review_events(directory, case, refs, [review])
    else:
        resolved = review_events(directory, case, refs, [review])[0]
        assert (resolved["challenge_result"] == "interruption_demonstrated") == (mode == "overlap")


@pytest.mark.asyncio
async def test_declared_but_unspoken_content_stays_untested(tmp_path):
    directory, case = await audio_bundle(tmp_path)
    _, refs = load_bundle(directory)
    review = ConversationEventReview(
        event_id="time",
        delivered="not_met",
        correction="uncertain",
        resumption="uncertain",
        explanation="Wrong field was never actually spoken",
        evidence=tuple(refs.values()),
    )
    result = review_events(directory, case, refs, [review])[0]
    assert result["audio_overlap_status"] == "overlap_observed"
    assert result["challenge_result"] == "untested"


@pytest.mark.asyncio
@pytest.mark.parametrize("damage", [None, "over_budget", "vegetarian_only", "tampered_quote"])
async def test_valid_dining_terms_and_prior_quotes_are_auditable(
    tmp_path, dining_store, variant_specs, damage
):
    store = dining_store
    q = quote(store)
    if damage != "over_budget":
        q = invoke(store, "counteroffer", {"quote_id": q["quote_id"], "total_inr": 12000})["quote"]
    q = invoke(
        store,
        "set_dietary_requirements",
        {
            "quote_id": q["quote_id"],
            "without_onion_garlic_guests": 0 if damage == "vegetarian_only" else 2,
        },
    )["quote"]
    confirmation = prepare(store, q)
    result = invoke(
        store, "record_reservation", {"confirmation_id": confirmation["confirmation_id"]}, offset=10
    )
    assert result["ok"]
    if damage == "tampered_quote":
        store.runs[store.id]["state"]["quotes"][-1]["dining_total_inr"] = 1
    case = convert_variants(*variant_specs)[2]
    evidence = LocalEvidence(tmp_path, uuid4(), store.id)
    for name, value in (
        ("config/case.json", case.model_dump(mode="json")),
        ("business/final.json", store.run(store.id)["state"]),
        ("business/audit.json", store.run(store.id)["audit"]),
    ):
        await evidence.json(name, value)
    await evidence.finalize(store.id)
    metrics = {m.name: m.status for m in deterministic(evidence.directory)}
    assert metrics["task_state"] == (
        "not_met" if damage in {"over_budget", "vegetarian_only"} else "met"
    )
    assert metrics["reservation_history"] == metrics["task_state"]
    assert metrics["dining_terms_history"] == ("not_met" if damage == "tampered_quote" else "met")
    assert metrics["reservation_evidence"] == "uncertain"  # no captured audio in this state test
    evidence.close_writer()


@pytest.mark.asyncio
async def test_hard_execution_rejects_opposite_interruption_and_repeats(variant_specs):
    from voice_bench.runtime import execute_batch
    from voice_bench.settings import load_config

    cases = convert_variants(*variant_specs)
    config = load_config(Path("configs/live.example.toml"))
    with pytest.raises(ValueError, match="Hard restaurant"):
        await execute_batch(config, cases, repetitions=2)


def test_postgres_dining_revisions_replay_and_attempt_isolation(store, dining_store):
    batch_id = uuid4()
    plan_ids = [uuid4(), uuid4()]
    store.create_batch(
        batch_id,
        {
            "limits": {"max_attempts_per_case": 1},
            "plans": [{"plan_id": str(p)} for p in plan_ids],
        },
    )
    runs = [uuid4(), uuid4()]
    for run_id, plan_id in zip(runs, plan_ids, strict=True):
        run = deepcopy(dining_store.run(dining_store.id))
        run.update(plan_id=str(plan_id), context={"case_id": "synthetic", "channel": "browser"})
        store.create_run(batch_id, run_id, run)
        with store.locked_run(run_id) as current:
            current["user_task_served"] = True
    service = BusinessService(store)

    def call(run_id, tool, args, operation, offset=0):
        events = observations(run_id)
        for e in events:
            e["sequence"] += offset
        return service.execute(
            run_id, tool, args, operation, actor="counterpart", observations=events
        )

    q = call(runs[0], "quote_reservation", {"option_id": "4"}, "quote")["quote"]
    q = call(runs[0], "counteroffer", {"quote_id": q["quote_id"], "total_inr": 12000}, "offer")[
        "quote"
    ]
    c = call(
        runs[0],
        "prepare_confirmation",
        {"quote_id": q["quote_id"], "booking_name": "Test User"},
        "confirm",
    )["confirmation"]
    args = {"confirmation_id": c["confirmation_id"]}
    assert call(runs[1], "record_reservation", args, "book", 10)["error"] == "stale_confirmation"
    saved = call(runs[0], "record_reservation", args, "book", 10)
    assert saved["ok"]
    assert call(runs[0], "record_reservation", args, "book", 20) == saved
    assert (
        call(runs[0], "record_reservation", args, "another", 20)["error"]
        == "reservation_already_recorded"
    )
    assert len(store.run(runs[0])["state"]["bookings"]) == 1
    assert store.run(runs[1])["state"]["quotes"] == []


@pytest.mark.asyncio
async def test_worker_triggers_event_with_real_workflow_and_keeps_receiving_audio(
    tmp_path, dining_store
):
    import asyncio
    import base64
    import json
    from types import SimpleNamespace

    from test_caller import Session, Socket, caller

    from voice_bench.models import CounterpartBrief

    evidence = LocalEvidence(tmp_path, uuid4(), dining_store.id)
    socket, session = Socket(), Session(evidence, 24000)
    simulator = caller(socket)
    simulator.business = BusinessService(dining_store)
    task = asyncio.create_task(
        simulator.converse(
            SimpleNamespace(run_id=dining_store.id),
            CounterpartBrief(role="Desk", goal="Synthetic event test", known_facts={}),
            session,
            evidence,
            conversation_events=(challenge(),),
        )
    )
    try:
        async with asyncio.timeout(5):
            await socket.sent.get()
            await socket.incoming.put({"type": "session.updated", "session": {}})

            async def tool(name, args):
                await socket.incoming.put(
                    {
                        "type": "response.function_call_arguments.done",
                        "name": "business_" + name,
                        "arguments": json.dumps(args),
                        "response_id": name,
                        "call_id": name,
                    }
                )
                await socket.incoming.put(
                    {"type": "response.done", "response": {"id": name, "status": "completed"}}
                )
                output = await socket.sent.get()
                return json.loads(output["item"]["output"]), await socket.sent.get()

            await tool("check_availability", {"branch": "Khar"})
            q, _ = await tool("quote_reservation", {"option_id": "4"})
            confirmation, request = await tool(
                "prepare_confirmation",
                {"quote_id": q["quote"]["quote_id"], "booking_name": "Test User"},
            )
            assert confirmation["ok"]
            assert request["response"]["metadata"] == {"conversation_event_id": "time"}
            await socket.incoming.put(
                {
                    "type": "response.created",
                    "response": {
                        "id": "challenge-audio",
                        "metadata": request["response"]["metadata"],
                    },
                }
            )
            await socket.incoming.put(
                {
                    "type": "response.output_audio.delta",
                    "response_id": "challenge-audio",
                    "item_id": "speech",
                    "delta": base64.b64encode(b"\x00\x10" * 2400).decode(),
                }
            )
            await socket.incoming.put(
                {"type": "input_audio_buffer.speech_started", "item_id": "target"}
            )
            assert await socket.sent.get() == {
                "type": "response.cancel",
                "response_id": "challenge-audio",
            }
            assert (await socket.sent.get())["type"] == "conversation.item.truncate"
            await session.receive(b"\x00\x10" * 480)
            assert (await socket.sent.get())["type"] == "input_audio_buffer.append"
            await socket.incoming.put(
                {
                    "type": "response.done",
                    "response": {"id": "challenge-audio", "status": "cancelled"},
                }
            )
            await socket.incoming.put(
                {"type": "input_audio_buffer.speech_stopped", "item_id": "target"}
            )
            await socket.incoming.put({"type": "input_audio_buffer.committed", "item_id": "target"})
            assert (await socket.sent.get())["type"] == "response.create"
            await socket.incoming.put({"type": "response.created", "response": {"id": "closing"}})
            await socket.incoming.put(
                {
                    "type": "response.function_call_arguments.done",
                    "name": "finish_counterpart",
                    "call_id": "finish",
                    "response_id": "closing",
                }
            )
            await socket.incoming.put(
                {"type": "response.done", "response": {"id": "closing", "status": "completed"}}
            )
            await task
            events = await evidence.event_snapshot()
            assert any(e["kind"] == "conversation_event_audio" for e in events)
            assert any(e["kind"] == "counterpart_playback_interrupted" for e in events)
            assert not dining_store.run(dining_store.id)["state"]["bookings"]
    finally:
        task.cancel()
        await asyncio.gather(task, return_exceptions=True)
        await session.close("test")
        evidence.close_writer()


def test_dimension_summary_keeps_missing_report_and_voice_proof_explicit(variant_specs):
    from voice_bench.evaluation.reservations import dimension_summary

    case = convert_variants(*variant_specs)[2].model_dump(mode="json")
    metrics = [{"name": name, "status": "met"} for name in case["criteria"]["required_metrics"]]
    metrics = [m for m in metrics if m["name"] != "user_report_accuracy"]
    result = dimension_summary(
        case, metrics, [{"event_id": "time", "kind": "misread", "challenge_result": "untested"}]
    )
    assert result["task_completion"] == "uncertain"
    assert result["negotiation"] == "met"
    assert result["hinglish_quality"] == "requires_listening_review"
    assert result["interruption_behavior"][0]["result"] == "untested"
