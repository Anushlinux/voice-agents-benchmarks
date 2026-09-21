import asyncio
from decimal import Decimal
from pathlib import Path

import pytest

from voice_bench.batches import make_plan
from voice_bench.controller.runner import Controller
from voice_bench.fixture import fixture_case
from voice_bench.settings import load_config


def configured(tmp_path):
    config = load_config(Path("configs/local.toml"))
    return config.model_copy(
        update={
            "artifact_root": tmp_path,
            "target": config.target.model_copy(update={"agent_ref": "test"}),
            "limits": config.limits.model_copy(
                update={
                    "max_call_seconds": 1,
                    "max_total_call_minutes": 10,
                    "max_spend_inr": Decimal(10),
                }
            ),
            "runtime": config.runtime.model_copy(
                update={
                    "cost_ceiling_inr_per_attempt": Decimal(1),
                    "rate_card_version": "test-only",
                    "setup_timeout_seconds": 1,
                    "finalize_timeout_seconds": 1,
                }
            ),
        }
    )


class Session:
    def __init__(self):
        self.closed = False

    async def close(self, reason):
        self.closed = True

    def check_health(self):
        pass


class Channel:
    def __init__(self, mode="ok", store=None):
        self.store = store
        self.mode, self.calls = mode, 0
        self.session = Session()

    async def connect(self, request, evidence):
        self.calls += 1
        if self.mode == "setup_error":
            raise RuntimeError("connection failed")
        if self.store and self.mode != "missing_task":
            from voice_bench.business.environment import BusinessService

            call_id = str(request.run.run_id)
            self.store.bind("rumik", call_id, request.run.run_id)
            BusinessService(self.store).serve_user_task(call_id, "test")
        return self.session

    async def reconcile(self, run_id, evidence):
        return self.mode != "setup_error"


class Caller:
    def __init__(self, mode="ok"):
        self.mode = mode

    async def converse(self, run, brief, session, evidence):
        if self.mode == "error":
            raise RuntimeError("simulator failed")
        if self.mode == "timeout":
            await asyncio.sleep(20)


def batch(store, config):
    case = fixture_case()
    plan = make_plan([case], ["browser"])[0]
    store.create_batch(
        plan.batch_id,
        {"plans": [plan.model_dump(mode="json")], "limits": config.limits.model_dump(mode="json")},
    )
    return plan, case


@pytest.mark.asyncio
@pytest.mark.parametrize("mode", ["ok", "error", "timeout"])
async def test_controller_always_closes_seals_and_releases(store, tmp_path, mode):
    config = configured(tmp_path)
    plan, case = batch(store, config)
    channel = Channel(store=store)
    result = await Controller(store, config, channel, Caller(mode)).execute(plan, case, "digest")
    assert channel.session.closed
    run = store.run(result.run_id)
    assert run["evidence_sealed"] and not run["accept_tools"]
    assert not run["reservation"]["active"]
    assert result.termination_confirmed
    assert result.failure_stage == (None if mode == "ok" else "conversation")
    assert (tmp_path / str(plan.batch_id) / str(result.run_id) / "manifest.json").exists()
    assert (
        tmp_path / str(plan.batch_id) / str(result.run_id) / "target/report-requests.json"
    ).read_text() == "[]"


@pytest.mark.asyncio
async def test_unknown_start_retains_capacity_and_evidence(store, tmp_path):
    config = configured(tmp_path)
    plan, case = batch(store, config)
    result = await Controller(store, config, Channel("setup_error", store=store), Caller()).execute(
        plan, case, "x"
    )
    assert not result.termination_confirmed
    assert result.failure_stage == "connection"
    assert store.run(result.run_id)["reservation"]["active"]


@pytest.mark.asyncio
async def test_zero_budget_never_dispatches(store, tmp_path):
    config = configured(tmp_path)
    config = config.model_copy(
        update={"limits": config.limits.model_copy(update={"max_spend_inr": Decimal(0)})}
    )
    plan, case = batch(store, config)
    channel = Channel(store=store)
    result = await Controller(store, config, channel, Caller()).execute(plan, case, "x")
    assert channel.calls == 0
    assert result.termination_confirmed
    assert not store.run(result.run_id).get("dispatch_intent")


@pytest.mark.asyncio
async def test_cancellation_finalizes_attempt(store, tmp_path):
    config = configured(tmp_path)
    plan, case = batch(store, config)
    channel = Channel(store=store)
    task = asyncio.create_task(
        Controller(store, config, channel, Caller("timeout")).execute(plan, case, "x")
    )
    for _ in range(100):
        await asyncio.sleep(0.02)
        rows = store.runs(plan.batch_id)
        if rows and rows[0]["phase"] == "in_conversation":
            break
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    assert channel.session.closed
    assert store.runs(plan.batch_id)[0]["evidence_sealed"]


@pytest.mark.asyncio
async def test_controller_delivers_task_and_passes_only_counterpart_brief(store, tmp_path):
    import json

    config = configured(tmp_path)
    plan, case = batch(store, config)

    class InspectCounterpart:
        async def converse(self, run, brief, session, evidence):
            assert brief == case.counterpart
            assert not hasattr(brief, "user_task") and not hasattr(brief, "criteria")
            assert store.run(run.run_id)["user_task_served"]

    result = await Controller(store, config, Channel(store=store), InspectCounterpart()).execute(
        plan, case, "digest"
    )
    assert result.error is None
    path = tmp_path / str(plan.batch_id) / str(result.run_id) / "target/task-delivery.json"
    assert json.loads(path.read_text())["call_id"] == str(result.run_id)


@pytest.mark.asyncio
async def test_missing_user_task_stops_before_counterpart_conversation(store, tmp_path):
    config = configured(tmp_path)
    plan, case = batch(store, config)
    called = []

    class Counterpart:
        async def converse(self, *args):
            called.append(True)

    channel = Channel("missing_task", store=store)
    result = await Controller(store, config, channel, Counterpart()).execute(plan, case, "digest")
    assert result.error and not called
    assert result.connected and result.validity == "invalid"
    assert result.attribution == "harness"
    assert channel.session.closed and result.termination_confirmed


@pytest.mark.asyncio
async def test_cleanup_failure_does_not_skip_provider_reconciliation(store, tmp_path):
    config = configured(tmp_path)
    plan, case = batch(store, config)
    channel = Channel(store=store)

    async def broken_close(reason):
        raise RuntimeError("browser event delivery failed")

    channel.session.close = broken_close
    result = await Controller(store, config, channel, Caller()).execute(plan, case, "digest")
    assert result.termination_confirmed
    assert not store.run(result.run_id)["reservation"]["active"]


@pytest.mark.asyncio
async def test_transport_failure_during_task_wait_is_reported_immediately(store, tmp_path):
    from voice_bench.errors import HarnessFailure

    config = configured(tmp_path)
    plan, case = batch(store, config)
    channel = Channel("missing_task", store=store)

    def broken_health():
        raise HarnessFailure("receive_queue_overflow")

    channel.session.check_health = broken_health
    result = await Controller(store, config, channel, Caller()).execute(plan, case, "digest")
    assert result.error == "HarnessFailure"
    assert result.termination_confirmed


@pytest.mark.asyncio
@pytest.mark.parametrize("native_hangup", [True, False])
async def test_report_does_not_cut_off_live_audio_and_requires_hangup(
    store, tmp_path, native_hangup
):
    import json
    from uuid import uuid4

    from voice_bench.business.environment import BusinessService
    from voice_bench.channels.media import MediaSession
    from voice_bench.evidence.local import LocalEvidence

    config = configured(tmp_path)
    config = config.model_copy(
        update={"runtime": config.runtime.model_copy(update={"post_report_hangup_seconds": 0.3})}
    )
    plan, case = batch(store, config)
    case = case.model_copy(
        update={"completion": "target_report_then_hangup", "target_tools": ("submit_user_report",)}
    )
    channel = Channel(store=store)
    channel.session = MediaSession(LocalEvidence(tmp_path / "media", uuid4(), uuid4()), 24000)
    producer_stopped = asyncio.Event()
    tail_completed = asyncio.Event()

    class StillSpeaking:
        async def converse(self, *args):
            try:
                await asyncio.sleep(30)
            finally:
                producer_stopped.set()

    async def report_then_finish_turn():
        while not store.runs(plan.batch_id) or not store.runs(plan.batch_id)[0].get(
            "user_task_served"
        ):
            await asyncio.sleep(0.01)
        run = store.runs(plan.batch_id)[0]
        receipt = BusinessService(store).submit_user_report(
            str(run["run_id"]), "test", "Accurate failure report."
        )
        assert receipt["ok"]
        await asyncio.sleep(0.15)
        assert not producer_stopped.is_set(), "A report must not cancel live speech"
        assert not channel.session.closed.is_set()
        tail_completed.set()
        if native_hangup:
            channel.session.closed.set()

    pending = asyncio.create_task(report_then_finish_turn())
    try:
        result = await Controller(store, config, channel, StillSpeaking()).execute(
            plan, case, "digest"
        )
        await pending
        assert tail_completed.is_set() and producer_stopped.is_set()
        assert result.error == (None if native_hangup else "ConversationTimeout")
        assert result.termination_confirmed
        path = tmp_path / str(plan.batch_id) / str(result.run_id) / "events.jsonl"
        events = [json.loads(line) for line in path.read_text().splitlines()]
        assert not any(e["kind"] == "end_call_requested" for e in events)
        assert any(e["kind"] == "target_hangup_after_report" for e in events) == native_hangup
        assert (
            any(e["kind"] == "target_hangup_missing_after_report" for e in events) != native_hangup
        )
    finally:
        pending.cancel()
        await asyncio.gather(pending, return_exceptions=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("target_speaks", [False, True])
async def test_silence_deadline_remains_active_after_employee_finishes(
    store, tmp_path, target_speaks
):
    import json
    import struct
    from uuid import uuid4

    from voice_bench.business.environment import BusinessService
    from voice_bench.channels.media import MediaSession
    from voice_bench.evidence.local import LocalEvidence

    config = configured(tmp_path)
    config = config.model_copy(
        update={
            "limits": config.limits.model_copy(update={"max_call_seconds": 2}),
            "counterpart": config.counterpart.model_copy(
                update={"conversation_idle_seconds": 0.15}
            ),
        }
    )
    plan, case = batch(store, config)
    case = case.model_copy(
        update={"completion": "target_report_then_hangup", "target_tools": ("submit_user_report",)}
    )
    channel = Channel(store=store)
    channel.session = MediaSession(LocalEvidence(tmp_path / "media", uuid4(), uuid4()), 24000)

    async def reply():
        while not store.runs(plan.batch_id) or not store.runs(plan.batch_id)[0].get(
            "user_task_served"
        ):
            await asyncio.sleep(0.01)
        # Incoming silent frames must not keep a dead conversation alive. Actual
        # received speech may continue beyond the response-start deadline.
        for _ in range(12):
            if channel.session.closed.is_set():
                return
            await channel.session.receive(struct.pack("<h", 2000 if target_speaks else 0) * 720)
            await asyncio.sleep(0.03)
        if target_speaks:
            run = store.runs(plan.batch_id)[0]
            BusinessService(store).submit_user_report(
                str(run["run_id"]), "test", "The requested task was not completed."
            )
            channel.session.closed.set()

    pending = asyncio.create_task(reply())
    try:
        result = await Controller(store, config, channel, Caller()).execute(plan, case, "test")
        events = [
            json.loads(line)
            for line in (tmp_path / str(plan.batch_id) / str(result.run_id) / "events.jsonl")
            .read_text()
            .splitlines()
        ]
        assert result.error == (None if target_speaks else "ConversationTimeout")
        assert result.termination_confirmed
        assert any(e["kind"] == "target_report_idle_timeout" for e in events) != target_speaks
    finally:
        pending.cancel()
        await asyncio.gather(pending, return_exceptions=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("speaker", ["target", "employee", "silent_frames"])
async def test_post_report_deadline_measures_silence_not_time_since_receipt(
    store, tmp_path, speaker
):
    import struct
    from uuid import uuid4

    from voice_bench.business.environment import BusinessService
    from voice_bench.channels.media import MediaSession
    from voice_bench.evidence.local import LocalEvidence

    config = configured(tmp_path)
    config = config.model_copy(
        update={
            "limits": config.limits.model_copy(update={"max_call_seconds": 2}),
            "runtime": config.runtime.model_copy(update={"post_report_hangup_seconds": 0.15}),
        }
    )
    plan, case = batch(store, config)
    case = case.model_copy(
        update={"completion": "target_report_then_hangup", "target_tools": ("submit_user_report",)}
    )
    channel = Channel(store=store)
    channel.session = MediaSession(LocalEvidence(tmp_path / "media", uuid4(), uuid4()), 24000)

    async def finish_exchange():
        while not store.runs(plan.batch_id) or not store.runs(plan.batch_id)[0].get(
            "user_task_served"
        ):
            await asyncio.sleep(0.01)
        run = store.runs(plan.batch_id)[0]
        BusinessService(store).submit_user_report(
            str(run["run_id"]), "test", "No booking was made."
        )
        for i in range(10):
            if speaker == "silent_frames" and channel.session.closed.is_set():
                return
            assert not channel.session.closed.is_set(), "Report receipt must not cut off speech"
            if speaker == "target":
                await channel.session.receive(struct.pack("<h", 2000) * 960)
            elif speaker == "silent_frames":
                await channel.session.receive(b"\x00\x00" * 960)
            else:
                channel.session.played["closing"] = (i + 1) * 40
            await asyncio.sleep(0.04)
        channel.session.closed.set()

    pending = asyncio.create_task(finish_exchange())
    try:
        result = await Controller(store, config, channel, Caller("timeout")).execute(
            plan, case, "test"
        )
        await pending
        assert result.error == ("ConversationTimeout" if speaker == "silent_frames" else None)
        assert result.termination_confirmed
    finally:
        pending.cancel()
        await asyncio.gather(pending, return_exceptions=True)
