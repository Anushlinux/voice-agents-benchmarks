"""Synthetic harness tests, not additional dataset points or live conversations."""

import hashlib
import json
from contextlib import contextmanager
from copy import deepcopy
from pathlib import Path
from uuid import uuid4

import pytest

from voice_bench.business.environment import BusinessService
from voice_bench.business.reservations import ReservationWorkflow, consent_anchors
from voice_bench.evaluation.reservations import display_verdict
from voice_bench.evaluation.scoring import (
    deterministic,
    import_review,
    review_template,
    save_evaluation,
)
from voice_bench.evidence.local import LocalEvidence
from voice_bench.restaurant_case import HUMAN_CHECKS, RULE_CHECKS, import_case, pilot_blockers
from voice_bench.settings import load_config


@pytest.fixture
def inventory():
    base = {
        "branch": "Fallback",
        "date": "2026-09-25",
        "time": "19:00",
        "timezone": "Asia/Kolkata",
        "party_size": 8,
        "seating": "regular_table",
        "table_sizes": [8],
        "reservation_charge_inr": 0,
    }
    return [
        {**base, "option_id": str(i), **changes}
        for i, changes in enumerate(
            [
                {"branch": "Preferred", "time": "17:00"},
                {"branch": "Preferred", "time": "20:00"},
                {"seating": "bar", "table_sizes": [1] * 8},
                {"table_sizes": [4, 4]},
                {},
            ]
        )
    ]


class MemoryStore:
    def __init__(self, inventory):
        self.id = uuid4()
        self.runs = {
            self.id: {
                "workflow": ReservationWorkflow.name,
                "workflow_version": "1",
                "state": ReservationWorkflow().initialize({"inventory": inventory, "bookings": []}),
                "user_task_served": True,
                "accept_tools": True,
                "operations": {},
                "audit": [],
                "tool_access": {
                    "counterpart": ["check_availability", "record_reservation"],
                    "target": [],
                },
            }
        }

    @contextmanager
    def locked_run(self, run_id):
        yield self.runs[run_id]

    def run(self, run_id):
        return deepcopy(self.runs[run_id])


def observations(run_id):
    specs = [
        ("caller", "counterpart_audio_done", {"item_id": "desk-readback", "samples": 24000}),
        (
            "channel",
            "playback_progress",
            {"item_id": "desk-readback", "played_ms": 1000, "boundary": "browser_render"},
        ),
        ("caller", "target_speech_detected", {"provider_item_id": "target-acceptance"}),
        ("caller", "target_speech_stopped", {"provider_item_id": "target-acceptance"}),
    ]
    return [
        {"run_id": str(run_id), "source": source, "kind": kind, "sequence": i, "payload": payload}
        for i, (source, kind, payload) in enumerate(specs)
    ]


def book(store, option="4", operation="book", events=None, **kwargs):
    return BusinessService(store).execute(
        store.id,
        "record_reservation",
        {"option_id": option, "booking_name": "Test User"},
        operation,
        actor="counterpart",
        observations=observations(store.id) if events is None else events,
        **kwargs,
    )


@pytest.mark.parametrize("option", ["0", "1", "2", "3", "4"])
def test_every_physical_option_can_be_booked_without_autocorrection(inventory, option):
    store = MemoryStore(inventory)
    result = book(store, option)
    assert result["ok"]
    booking = result["reservation"]
    assert all(booking[k] == v for k, v in inventory[int(option)].items())
    assert booking["consent_evidence"]["semantic_confirmation"] == "requires_human_review"


def test_available_matching_options_are_not_withheld(inventory):
    store = MemoryStore(inventory)
    result = BusinessService(store).execute(
        store.id, "check_availability", {"branch": "Fallback"}, "read", actor="counterpart"
    )
    assert {o["option_id"] for o in result["options"]} == {"2", "3", "4"}
    assert not store.run(store.id)["state"]["bookings"]


@pytest.mark.parametrize("played_ms,accepted", [(999, True), (500, False)])
def test_phone_booking_requires_complete_carrier_playback_then_response(
    inventory, played_ms, accepted
):
    store = MemoryStore(inventory)
    events = observations(store.id)
    for event in events:
        event["sequence"] += 1
    events[1]["payload"].update(boundary="carrier_checkpoint", played_ms=played_ms)
    events.insert(
        0,
        {
            "run_id": str(store.id),
            "source": "channel",
            "kind": "carrier_stream_start",
            "sequence": 0,
            "payload": {"callId": "call", "streamId": "stream"},
        },
    )
    result = book(store, events=events)
    assert result["ok"] is accepted
    if accepted:
        anchors = result["reservation"]["consent_evidence"]
        assert anchors["observation_boundary"] == "carrier_checkpoint_and_received_audio"
        assert anchors["audio_artifacts"] == ["audio/sent.wav", "audio/received.wav"]
        assert anchors["semantic_confirmation"] == "requires_human_review"
    else:
        assert not store.run(store.id)["state"]["bookings"]


def test_idempotency_attempt_isolation_and_rejected_requests(inventory):
    store, other = MemoryStore(inventory), MemoryStore(inventory)
    first = book(store)
    assert book(store, events=[]) == first
    assert store.run(store.id)["audit"][-1]["replay"]
    assert book(store, "0")["error"] == "operation_conflict"
    assert book(store, "0", "different")["error"] == "consent_already_used"
    assert book(store, "4", "again")["error"] == "unavailable_option"
    assert len(store.run(store.id)["state"]["bookings"]) == 1
    assert other.run(other.id)["state"]["bookings"] == []
    assert book(other)["reservation"]["reference"] != first["reservation"]["reference"]
    service = BusinessService(store)
    assert (
        service.execute(store.id, "record_reservation", {}, "bad", actor="target")["error"]
        == "forbidden_tool"
    )
    assert len(store.run(store.id)["audit"]) == 6


@pytest.mark.parametrize(
    "damage",
    [
        "absent",
        "partial_playback",
        "wrong_item",
        "wrong_run",
        "incomplete_response",
        "model_flag",
        "carrier",
    ],
)
def test_missing_or_fabricated_consent_cannot_write(inventory, damage):
    store = MemoryStore(inventory)
    events = observations(store.id)
    if damage == "absent":
        events = []
    if damage == "partial_playback":
        events[1]["payload"]["played_ms"] = 100
    if damage == "wrong_item":
        events[3]["payload"]["provider_item_id"] = "different"
    if damage == "wrong_run":
        events[1]["run_id"] = str(uuid4())
    if damage == "incomplete_response":
        events.pop()
    if damage == "carrier":
        events[1]["payload"]["boundary"] = "carrier_checkpoint"
    if damage == "model_flag":
        result = BusinessService(store).execute(
            store.id,
            "record_reservation",
            {"option_id": "4", "booking_name": "Test User", "confirmed": True},
            "book",
            actor="counterpart",
        )
    else:
        result = book(store, events=events)
    assert not result["ok"]
    assert store.run(store.id)["state"]["bookings"] == []
    assert len(store.run(store.id)["audit"]) == 1


@pytest.fixture
def custom_case(tmp_path, inventory, monkeypatch):
    import voice_bench.restaurant_case as module

    source = {
        "conversation_id": module.CONVERSATION_ID,
        "instruction_id": "restaurant-table-2",
        "utterances": [{"text": "Synthetic source validation input"}] * 20,
    }
    raw = json.dumps(source).encode()
    monkeypatch.setattr(
        module,
        "SOURCE_BLOB",
        hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest(),
    )
    source_path = tmp_path / "source.json"
    source_path.write_bytes(raw)
    expected = {k: v for k, v in inventory[-1].items() if k != "option_id"}
    expected["booking_name"] = "Test User"
    data = {
        "case_id": module.CASE_ID,
        "reconstructed_from_handoff": True,
        "agent_brief": {
            "request": "User-only instruction",
            "known_facts": {},
            "constraints": [],
            "permissions": [],
        },
        "simulator_brief": {
            "role": "Desk employee",
            "goal": "Desk-only instruction",
            "known_facts": {},
            "behavior_rules": [],
        },
        "inventory": inventory,
        "expected_outcome": expected,
        "rubrics": {"private": "Evaluator-only instruction"},
    }
    case_path = tmp_path / "case.json"
    case_path.write_text(json.dumps(data))
    return case_path, source_path


def test_import_preserves_roles_and_rejects_changed_source(custom_case):
    case_path, source_path = custom_case
    case = import_case(case_path, source_path)
    assert case.target_tools == () and not case.harness_fixture
    assert case.task_scope == "single_call" and case.call_initiation == "harness_connected"
    assert len(case.initial_state["inventory"]) == 5
    assert "inventory" not in case.user_task.model_dump_json()
    assert "Evaluator-only" not in case.counterpart.model_dump_json()
    assert "User-only" not in case.counterpart.model_dump_json()
    assert "Desk-only" not in case.user_task.model_dump_json()
    source_path.write_bytes(source_path.read_bytes() + b" ")
    with pytest.raises(ValueError, match="differs"):
        import_case(case_path, source_path)


def test_preflight_is_unfunded_and_provider_free(custom_case):
    case = import_case(*custom_case)
    config = load_config(Path("configs/live.example.toml"))
    result = pilot_blockers(config, [case])
    assert result["provider_calls"] == 0
    assert result["counts"]["attempted"] == 0 and result["counts"]["planned"] == 1
    assert "No funded spend/minute limits" in result["blockers"]


async def bundle(tmp_path, case, inventory, option="4", damage=None, telephone=False):
    from voice_bench.channels.media import AudioRecorder
    from voice_bench.models import AudioFrame

    store = MemoryStore(inventory)
    evidence = LocalEvidence(tmp_path / "artifacts", uuid4(), store.id)
    events = observations(store.id)
    if telephone:
        for event in events:
            event["sequence"] += 1
        events[1]["payload"]["boundary"] = "carrier_checkpoint"
        events.insert(
            0,
            {
                "run_id": str(store.id),
                "source": "channel",
                "kind": "carrier_stream_start",
                "sequence": 0,
                "payload": {"callId": "call", "streamId": "stream"},
            },
        )
    result = book(store, option, events=events)
    for event in events:
        await evidence.emit(event["source"], event["kind"], event["payload"])
    await evidence.emit(
        "business",
        "reservation_action",
        {
            "operation_id": "book",
            "result": result,
        },
    )
    final = deepcopy(store.run(store.id)["state"])
    if damage == "reference":
        final["bookings"][0]["reference"] = "made-up"
    if damage == "anchors":
        final["bookings"][0]["consent_evidence"]["event_sequences"] = [999]
    if damage == "duplicate":
        final["bookings"].append(deepcopy(final["bookings"][0]))
    if damage == "silent_repair":
        final["bookings"][0].update(inventory[-1])
    await evidence.json("config/case.json", case.model_dump(mode="json"))
    await evidence.json("business/final.json", final)
    await evidence.json("business/audit.json", store.run(store.id)["audit"])
    await evidence.json(
        "target/task-delivery.json", {"served": True, "call_id": "fixture-call", "sha256": "task"}
    )
    if case.criteria.get("user_report_source") == "target_callback":
        await evidence.json(
            "target/user-report.json",
            {
                "source": "authenticated_rumik_tool",
                "run_id": str(evidence.run_id),
                "call_id": "wrong-call" if damage == "report_binding" else "fixture-call",
                "task_sha256": "task",
                "text": "Synthetic target-authored report.",
            },
        )
        await evidence.json("target/report-requests.json", [{"result": {"ok": True}}])
    await evidence.json("result.json", {"termination_confirmed": True})
    await evidence.json(
        "provider/rumik-call.json",
        {
            "test_native_report": "Synthetic test-only report with "
            + result["reservation"]["reference"]
        },
    )
    recorder = AudioRecorder(evidence)
    for name in ("sent" if telephone else "played", "received"):
        if damage == "missing_audio" and name == "played":
            continue
        await recorder.write(
            name,
            AudioFrame(
                pcm_s16le=b"\x00\x10" * 24000,
                sample_rate_hz=24000,
                sample_offset=0,
                observed_monotonic_ns=0,
                clock_id="synthetic-test",
            ),
        )
    await recorder.close()
    await evidence.finalize(evidence.run_id)
    path = save_evaluation(evidence.directory, "rules-v1", deterministic(evidence.directory))
    evidence.close_writer()
    return evidence.directory, json.loads(path.read_text())


@pytest.mark.asyncio
@pytest.mark.parametrize("option", ["0", "1", "2", "3", "4"])
async def test_correct_and_incorrect_booking_grades(tmp_path, custom_case, inventory, option):
    case = import_case(*custom_case)
    directory, result = await bundle(tmp_path, case, inventory, option)
    metrics = {m["name"]: m for m in result["metrics"]}
    expected = "met" if option == "4" else "not_met"
    assert metrics["task_state"]["status"] == expected
    assert metrics["reservation_history"]["status"] == expected
    assert metrics["reservation_references"]["status"] == "met"
    assert metrics["reservation_evidence"]["status"] == "met"
    assert result["verdict"] == "inconclusive"  # no human review yet
    template = review_template(directory, "rules-v1")
    assert {m["name"] for m in template["checks"]} == set(HUMAN_CHECKS)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "damage,metric",
    [
        ("reference", "reservation_references"),
        ("anchors", "reservation_evidence"),
        ("duplicate", "reservation_count"),
    ],
)
async def test_bad_state_or_proof_is_detected(tmp_path, custom_case, inventory, damage, metric):
    _, result = await bundle(tmp_path, import_case(*custom_case), inventory, damage=damage)
    assert next(m for m in result["metrics"] if m["name"] == metric)["status"] == "not_met"


@pytest.mark.asyncio
async def test_silent_repair_does_not_hide_an_earlier_bad_booking(tmp_path, custom_case, inventory):
    directory, result = await bundle(
        tmp_path, import_case(*custom_case), inventory, "0", damage="silent_repair"
    )
    metrics = {m["name"]: m["status"] for m in result["metrics"]}
    assert metrics["task_state"] == "met"
    assert metrics["reservation_history"] == "not_met"
    with pytest.raises(ValueError, match="deterministic"):
        import_review(directory, "false-pass", human_review(directory))


@pytest.mark.asyncio
async def test_missing_audio_remains_inconclusive(tmp_path, custom_case, inventory):
    directory, result = await bundle(
        tmp_path, import_case(*custom_case), inventory, damage="missing_audio"
    )
    assert (
        next(m for m in result["metrics"] if m["name"] == "reservation_evidence")["status"]
        == "uncertain"
    )
    assert result["verdict"] == "inconclusive"
    with pytest.raises(ValueError, match="required captured evidence"):
        import_review(directory, "false-pass", human_review(directory))


@pytest.mark.asyncio
async def test_phone_evidence_uses_sent_audio_and_carrier_acknowledgments(
    tmp_path, custom_case, inventory
):
    directory, result = await bundle(tmp_path, import_case(*custom_case), inventory, telephone=True)
    metric = next(m for m in result["metrics"] if m["name"] == "reservation_evidence")
    assert metric["status"] == "met"
    assert not (directory / "audio/played.wav").exists()
    review = human_review(directory)
    imported = json.loads(import_review(directory, "phone-human-v1", review).read_text())
    assert imported["verdict"] == "pass"


def human_review(directory, *, outcome="passed", invalid=False):
    review = review_template(directory, "rules-v1")
    review.update(
        reviewer="synthetic-test-reviewer",
        validity="invalid" if invalid else "valid",
        outcome="unresolved" if invalid else outcome,
        explanation="Synthetic unit test",
        report_pointer=["test_native_report"],
    )
    for metric in review["checks"]:
        metric.update(
            status="not_met" if invalid and metric["name"] == "counterpart_validity" else "met",
            explanation="Synthetic unit test",
            evidence=review["evidence"],
        )
    return review


@pytest.mark.asyncio
async def test_human_pass_requires_report_and_all_checks(tmp_path, custom_case, inventory):
    directory, _ = await bundle(tmp_path, import_case(*custom_case), inventory)
    review = human_review(directory)
    missing = deepcopy(review)
    missing["report_pointer"] = []
    with pytest.raises(ValueError, match="post-call report"):
        import_review(directory, "missing-report", missing)
    bad = deepcopy(review)
    bad["checks"][1]["status"] = "uncertain"
    with pytest.raises(ValueError, match="every human check"):
        import_review(directory, "uncertain-consent", bad)
    bad = deepcopy(review)
    bad["checks"][-1]["status"] = "not_met"
    with pytest.raises(ValueError, match="every human check"):
        import_review(directory, "wrong-report", bad)
    result = json.loads(import_review(directory, "human-v1", review).read_text())
    assert result["verdict"] == "pass" and result["user_report"].startswith("Synthetic")


@pytest.mark.asyncio
@pytest.mark.parametrize("field", ["summary", "transcript"])
async def test_dashboard_text_is_not_native_user_report(tmp_path, custom_case, inventory, field):
    directory, _ = await bundle(tmp_path, import_case(*custom_case), inventory)
    review = human_review(directory)
    review["report_pointer"] = [field]
    with pytest.raises(ValueError, match="not user-facing report delivery"):
        import_review(directory, "not-a-report", review)


@pytest.mark.asyncio
async def test_missing_report_cannot_be_scored_as_target_failure(tmp_path, custom_case, inventory):
    directory, _ = await bundle(tmp_path, import_case(*custom_case), inventory)
    review = human_review(directory, outcome="failed")
    review["report_pointer"] = []
    review["checks"][-1]["status"] = "not_met"
    with pytest.raises(ValueError, match="missing report proof"):
        import_review(directory, "false-failure", review)


@pytest.mark.asyncio
async def test_simulator_errors_invalidate_and_wrong_commitments_fail(
    tmp_path, custom_case, inventory
):
    directory, _ = await bundle(tmp_path, import_case(*custom_case), inventory, "0")
    review = human_review(directory, invalid=True)
    assert (
        json.loads(import_review(directory, "invalid", review).read_text())["verdict"] == "invalid"
    )
    review = human_review(directory, outcome="failed")
    assert json.loads(import_review(directory, "failed", review).read_text())["verdict"] == "fail"
    with pytest.raises(ValueError, match="deterministic"):
        import_review(directory, "false-pass", human_review(directory))


def test_unresolved_is_never_a_pass_or_target_failure():
    assert display_verdict("unresolved", "failed") == "inconclusive"
    assert display_verdict("invalid", "failed") == "invalid"
    assert "reservation_count" in RULE_CHECKS
    assert consent_anchors([]) is None


def test_reservations_persist_and_replay_in_postgres(store, inventory):
    batch_id, run_id = uuid4(), uuid4()
    data = MemoryStore(inventory)
    run = data.run(data.id)
    run.update(plan_id=str(uuid4()), context={"case_id": "synthetic-test", "channel": "browser"})
    store.create_batch(
        batch_id, {"limits": {"max_attempts_per_case": 1}, "plans": [{"plan_id": run["plan_id"]}]}
    )
    store.create_run(batch_id, run_id, run)
    # create_run initializes the task delivery gate; use the same authenticated-serving state.
    with store.locked_run(run_id) as current:
        current["user_task_served"] = True
    service = BusinessService(store)
    args = {"option_id": "4", "booking_name": "Test User"}
    first = service.execute(
        run_id,
        "record_reservation",
        args,
        "write",
        actor="counterpart",
        observations=observations(run_id),
    )
    assert first["ok"]
    assert (
        service.execute(run_id, "record_reservation", args, "write", actor="counterpart") == first
    )
    assert len(store.run(run_id)["state"]["bookings"]) == 1
    assert store.run(run_id)["audit"][-1]["replay"]


@pytest.mark.asyncio
async def test_pilot_cannot_expand_into_repetitions_or_phone(custom_case):
    from voice_bench.runtime import execute_batch

    case = import_case(*custom_case)
    config = load_config(Path("configs/live.example.toml"))
    with pytest.raises(ValueError, match="one browser attempt"):
        await execute_batch(config, [case], repetitions=2)


@pytest.mark.asyncio
async def test_realtime_worker_supplies_observed_anchors_to_booking(tmp_path, inventory):
    import asyncio
    import base64
    from types import SimpleNamespace

    from test_caller import Session, Socket, caller

    class RenderedSession(Session):
        async def cancel_playback(self):
            return {"desk-readback": 1000}

    store = MemoryStore(inventory)
    evidence = LocalEvidence(tmp_path, uuid4(), store.id)
    socket, session = Socket(), RenderedSession(evidence, 24000)
    simulator = caller(socket)
    simulator.business = BusinessService(store)
    from voice_bench.models import CounterpartBrief

    task = asyncio.create_task(
        simulator.converse(
            SimpleNamespace(run_id=store.id),
            CounterpartBrief(role="Desk", goal="Synthetic test", known_facts={}),
            session,
            evidence,
        )
    )
    try:
        async with asyncio.timeout(5):
            await socket.sent.get()
            await socket.incoming.put({"type": "session.updated", "session": {}})
            await socket.incoming.put({"type": "response.created"})
            await socket.incoming.put(
                {
                    "type": "response.output_audio.delta",
                    "item_id": "desk-readback",
                    "delta": base64.b64encode(b"\x00\x10" * 24000).decode(),
                }
            )
            await evidence.emit(
                "channel",
                "playback_progress",
                {"item_id": "desk-readback", "played_ms": 1000, "boundary": "browser_render"},
            )
            await socket.incoming.put(
                {"type": "response.output_audio.done", "item_id": "desk-readback"}
            )
            await socket.incoming.put(
                {"type": "response.done", "response": {"id": "readback", "status": "completed"}}
            )
            for phase in ("started", "stopped"):
                await socket.incoming.put(
                    {"type": "input_audio_buffer.speech_" + phase, "item_id": "acceptance"}
                )
            await socket.incoming.put(
                {"type": "input_audio_buffer.committed", "item_id": "acceptance"}
            )
            assert (await socket.sent.get())["type"] == "response.create"
            await socket.incoming.put({"type": "response.created"})
            await socket.incoming.put(
                {
                    "type": "response.function_call_arguments.done",
                    "name": "business_record_reservation",
                    "call_id": "book",
                    "response_id": "write",
                    "arguments": json.dumps({"option_id": "4", "booking_name": "Test User"}),
                }
            )
            await socket.incoming.put(
                {"type": "response.done", "response": {"id": "write", "status": "completed"}}
            )
            output = await socket.sent.get()
            booking_result = json.loads(output["item"]["output"])
            assert booking_result["ok"]
            assert (
                booking_result["reference_delivery"]["reference"]
                == booking_result["reservation"]["reference"]
            )
            assert "readback" in booking_result["reference_delivery"]["instruction"]
            assert (await socket.sent.get())["type"] == "response.create"
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
            action = next(e for e in events if e["kind"] == "reservation_action")
            assert action["payload"]["result"]["reservation"]["consent_evidence"]
            delivery = next(e for e in events if e["kind"] == "reference_delivery_requested")
            assert delivery["payload"]["reference"] == booking_result["reservation"]["reference"]
            assert len(store.run(store.id)["state"]["bookings"]) == 1
    finally:
        task.cancel()
        await asyncio.gather(task, return_exceptions=True)
        await session.close("test")
        evidence.close_writer()


@pytest.mark.asyncio
@pytest.mark.parametrize("seconds", [90, 300, 301])
async def test_pilot_duration_is_an_upper_bound(custom_case, monkeypatch, seconds):
    from voice_bench import runtime

    case = import_case(*custom_case)
    config = load_config(Path("configs/live.example.toml"))
    config = config.model_copy(
        update={
            "channels": ("browser",),
            "limits": config.limits.model_copy(
                update={
                    "max_call_seconds": seconds,
                    "max_attempts_per_case": 1,
                    "max_concurrent_calls": 1,
                }
            ),
        }
    )
    cap_blocker = "Pilot requires one attempt, concurrency one and at most 300 seconds"
    assert (cap_blocker in pilot_blockers(config, [case])["blockers"]) == (seconds > 300)

    def stop_before_provider_setup(config, cases):
        raise RuntimeError("duration accepted; stop before live setup")

    monkeypatch.setattr(runtime, "validate_live", stop_before_provider_setup)
    if seconds > 300:
        with pytest.raises(ValueError, match="at most 300 seconds"):
            await runtime.execute_batch(config, [case])
    else:
        with pytest.raises(RuntimeError, match="duration accepted"):
            await runtime.execute_batch(config, [case])


@pytest.mark.asyncio
@pytest.mark.parametrize("wrong_binding", [False, True])
async def test_private_target_report_receipt_is_bound_to_the_attempt(
    tmp_path, custom_case, inventory, wrong_binding
):
    case = import_case(*custom_case)
    case = case.model_copy(
        update={"criteria": {**case.criteria, "user_report_source": "target_callback"}}
    )
    directory, result = await bundle(
        tmp_path, case, inventory, damage="report_binding" if wrong_binding else None
    )
    metric = next(m for m in result["metrics"] if m["name"] == "user_report_presence")
    assert metric["status"] == ("not_met" if wrong_binding else "met")
    review = human_review(directory)
    review["report_pointer"] = ["text"]
    if wrong_binding:
        with pytest.raises(ValueError, match="deterministic"):
            import_review(directory, "private-report-review", review)
    else:
        saved = json.loads(import_review(directory, "private-report-review", review).read_text())
        assert saved["user_report"] == "Synthetic target-authored report."


def test_reference_delivery_preserves_one_identifier_and_spells_every_character():
    from voice_bench.business.reservations import reference_delivery

    delivery = reference_delivery("SIM-3453F8061B")
    assert delivery["reference"] == "SIM-3453F8061B"
    assert delivery["spoken_characters"] == [
        "S for Sierra",
        "I for India",
        "M for Mike",
        "hyphen",
        "three",
        "four",
        "five",
        "three",
        "F for Foxtrot",
        "eight",
        "zero",
        "six",
        "one",
        "B for Bravo",
    ]
    assert "ONE booking reference" in delivery["instruction"]
    assert "readback" in delivery["instruction"]
    assert reference_delivery("SIM-0AEF901BCD")["reference"] == "SIM-0AEF901BCD"
