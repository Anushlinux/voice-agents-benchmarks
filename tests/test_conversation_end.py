"""Conversation ending requires explicit intent, drained speech and a saved report."""

import asyncio
import json
import struct
from uuid import uuid4

import pytest
from test_controller import Channel, batch, configured

from voice_bench.business.environment import BusinessService
from voice_bench.channels.media import MediaSession
from voice_bench.contracts import CounterpartFinished, ExecutionCase
from voice_bench.controller.runner import Controller
from voice_bench.evidence.local import LocalEvidence


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "order,mode,expected",
    [
        ("report_first", "explicit", None),
        ("finish_first", "explicit", None),
        ("report_first", "native", None),
        ("report_first", "implicit_return", "ConversationTimeout"),
        ("missing_report", "explicit", "ConversationTimeout"),
        ("report_first", "strict_target_hangup", "ConversationTimeout"),
        ("report_first", "failed", "RuntimeError"),
        ("report_first", "unconfirmed", "TerminationUnconfirmed"),
    ],
)
async def test_end_requires_both_signals_and_preserves_failures(
    store, tmp_path, order, mode, expected
):
    config = configured(tmp_path)
    config = config.model_copy(
        update={
            "limits": config.limits.model_copy(update={"max_call_seconds": 3}),
            "runtime": config.runtime.model_copy(
                update={"post_report_hangup_seconds": 0.35, "conversation_end_quiet_seconds": 0.1}
            ),
            "counterpart": config.counterpart.model_copy(
                update={"conversation_idle_seconds": 0.35}
            ),
        }
    )
    plan, original = batch(store, config)
    case = original.model_copy(
        update={
            "completion": "target_report_then_hangup"
            if mode == "strict_target_hangup"
            else "target_report_then_conversation_end",
            "target_tools": ("submit_user_report",),
        }
    )
    # The new policy still requires authenticated reporting authority.
    with pytest.raises(ValueError, match="reporting tool"):
        ExecutionCase.model_validate({**case.model_dump(), "target_tools": []})
    channel = Channel(store=store)
    channel.session = MediaSession(LocalEvidence(tmp_path / "media", uuid4(), uuid4()), 24000)
    if mode == "unconfirmed":

        async def not_confirmed(*args):
            return False

        channel.reconcile = not_confirmed
    finish = asyncio.Event()
    report = asyncio.Event()

    class Employee:
        async def converse(self, *args):
            await finish.wait()
            if mode == "failed":
                raise RuntimeError("Synthetic employee failure")
            if mode == "implicit_return":
                return None
            return CounterpartFinished(tool_call_id="saved-priya-finish-order")

    async def exchange():
        while not store.runs(plan.batch_id) or not store.runs(plan.batch_id)[0].get(
            "user_task_served"
        ):
            await asyncio.sleep(0.01)
        run = store.runs(plan.batch_id)[0]
        if order in {"finish_first", "missing_report"}:
            finish.set()
            await asyncio.sleep(0.15)
            assert not channel.session.closed.is_set(), "Employee finish cannot replace a report"
        if order != "missing_report":
            BusinessService(store).submit_user_report(run["run_id"], "test", "Synthetic outcome")
            report.set()
        if order == "report_first":
            await asyncio.sleep(0.15)
            assert not channel.session.closed.is_set(), "Report alone cannot hang up"
            finish.set()
        if mode == "native":
            channel.session.closed.set()

    pending = asyncio.create_task(exchange())
    try:
        result = await Controller(store, config, channel, Employee()).execute(plan, case, "unit")
        await pending
        assert result.error == expected
        assert result.termination_confirmed == (mode != "unconfirmed")
        events = [
            json.loads(s)
            for s in (tmp_path / str(plan.batch_id) / str(result.run_id) / "events.jsonl")
            .read_text()
            .splitlines()
        ]
        requested = [e for e in events if e["kind"] == "counterpart_hangup_requested"]
        should_end = mode in {"explicit", "unconfirmed"} and order != "missing_report"
        assert bool(requested) == should_end
        if should_end:
            assert result.conversation_end == "counterpart_finish"
            assert requested[0]["payload"]["tool_call_id"] == "saved-priya-finish-order"
            assert not any(e["kind"] == "target_hangup_missing_after_report" for e in events)
        assert not store.run(result.run_id)["reservation"]["active"] or mode == "unconfirmed"
    finally:
        pending.cancel()
        await asyncio.gather(pending, return_exceptions=True)


@pytest.mark.asyncio
async def test_received_speech_after_finish_defers_close_but_silent_frames_do_not(store, tmp_path):
    config = configured(tmp_path)
    config = config.model_copy(
        update={
            "limits": config.limits.model_copy(update={"max_call_seconds": 3}),
            "runtime": config.runtime.model_copy(update={"conversation_end_quiet_seconds": 0.12}),
        }
    )
    plan, original = batch(store, config)
    case = original.model_copy(
        update={
            "completion": "target_report_then_conversation_end",
            "target_tools": ("submit_user_report",),
        }
    )
    channel = Channel(store=store)
    channel.session = MediaSession(LocalEvidence(tmp_path / "media", uuid4(), uuid4()), 24000)
    finish = asyncio.Event()

    class Employee:
        async def converse(self, run, *args):
            BusinessService(store).submit_user_report(str(run.run_id), "test", "Synthetic outcome")
            finish.set()
            return CounterpartFinished(tool_call_id="finish")

    async def trailing_speech():
        await finish.wait()
        for _ in range(12):
            assert not channel.session.closed.is_set(), "Trailing speech must be captured"
            await channel.session.receive(struct.pack("<h", 2000) * 960)
            await asyncio.sleep(0.04)
        # Silent audio keeps arriving, as it did during the recorded 15-second wait.
        for _ in range(12):
            if channel.session.closed.is_set():
                return
            await channel.session.receive(b"\x00\x00" * 960)
            await asyncio.sleep(0.04)
        pytest.fail("Continuous silent frames kept the ended conversation open")

    pending = asyncio.create_task(trailing_speech())
    try:
        result = await Controller(store, config, channel, Employee()).execute(plan, case, "unit")
        await pending
        assert result.error is None and result.conversation_end == "counterpart_finish"
        assert result.termination_confirmed
    finally:
        pending.cancel()
        await asyncio.gather(pending, return_exceptions=True)
