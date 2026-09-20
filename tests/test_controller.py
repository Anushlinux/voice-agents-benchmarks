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
    assert (tmp_path / str(plan.batch_id) / str(result.run_id) / "manifest.json").exists()


@pytest.mark.asyncio
async def test_unknown_start_retains_capacity_and_evidence(store, tmp_path):
    config = configured(tmp_path)
    plan, case = batch(store, config)
    result = await Controller(store, config, Channel("setup_error", store=store), Caller()).execute(
        plan, case, "x"
    )
    assert not result.termination_confirmed
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
