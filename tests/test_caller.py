import asyncio
import base64
import json
from uuid import uuid4

import pytest

from voice_bench.caller.openai_realtime import OpenAICounterpart
from voice_bench.channels.media import MediaSession
from voice_bench.contracts import CounterpartConfig, CounterpartFinished
from voice_bench.errors import CallerFailure, TransportFailure
from voice_bench.evidence.local import LocalEvidence
from voice_bench.models import CounterpartBrief


class Socket:
    def __init__(self):
        self.incoming = asyncio.Queue()
        self.sent = asyncio.Queue()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass

    def __aiter__(self):
        return self

    async def __anext__(self):
        return json.dumps(await self.incoming.get())

    async def send(self, value):
        await self.sent.put(json.loads(value))


class Session(MediaSession):
    async def send_audio(self, frame):
        await self.record_sent(frame)

    async def cancel_playback(self):
        return {"speech": 20}

    async def drain(self):
        pass


def caller(socket):
    return OpenAICounterpart(
        CounterpartConfig(
            model="test-model",
            voice="test-voice",
            instructions="Assigned behavior.",
            turn_detection={"type": "server_vad"},
        ),
        "test-key",
        lambda *a, **kw: socket,
    )


@pytest.mark.asyncio
async def test_realtime_counterpart_receives_audio_and_truncates_unplayed_speech(tmp_path):
    evidence = LocalEvidence(tmp_path, uuid4(), uuid4())
    session, socket = Session(evidence, 24000), Socket()
    brief = CounterpartBrief(
        role="Record custodian",
        goal="Handle permitted note changes",
        known_facts={"name": "Synthetic Custodian"},
    )
    task = asyncio.create_task(caller(socket).converse(None, brief, session, evidence))
    try:
        async with asyncio.timeout(5):
            update = await socket.sent.get()
            assert update["session"]["audio"]["output"]["voice"] == "test-voice"
            instructions = update["session"]["instructions"]
            assert "Synthetic Custodian" in instructions
            assert "initial_state" not in instructions and "criteria" not in instructions
            await socket.incoming.put({"type": "session.updated", "session": {"id": "fake"}})
            await session.receive(b"\x01\x00" * 480)
            audio = await socket.sent.get()
            assert audio["type"] == "input_audio_buffer.append"
            assert base64.b64decode(audio["audio"]) == b"\x01\x00" * 480
            await socket.incoming.put({"type": "response.created"})
            await socket.incoming.put(
                {
                    "type": "response.output_audio.delta",
                    "item_id": "speech",
                    "delta": base64.b64encode(b"\x02\x00" * 2400).decode(),
                }
            )
            await socket.incoming.put({"type": "input_audio_buffer.speech_started"})
            truncate = await socket.sent.get()
            assert truncate == {
                "type": "conversation.item.truncate",
                "item_id": "speech",
                "content_index": 0,
                "audio_end_ms": 20,
            }
            # Incoming audio continues after cancellation of caller playback.
            await session.receive(b"\x03\x00" * 480)
            assert (await socket.sent.get())["type"] == "input_audio_buffer.append"
            await socket.incoming.put({"type": "input_audio_buffer.speech_stopped"})
            await socket.incoming.put({"type": "input_audio_buffer.committed"})
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
            assert await task == CounterpartFinished(tool_call_id="finish")
    finally:
        task.cancel()
        await asyncio.gather(task, return_exceptions=True)
        await session.close("test")


@pytest.mark.asyncio
@pytest.mark.parametrize("mode,exception", [("error", CallerFailure), ("drop", TransportFailure)])
async def test_realtime_failures_do_not_become_success(tmp_path, mode, exception):
    evidence = LocalEvidence(tmp_path, uuid4(), uuid4())
    session, socket = Session(evidence, 24000), Socket()
    task = asyncio.create_task(
        caller(socket).converse(
            None,
            CounterpartBrief(role="Record custodian", goal="Test", known_facts={}),
            session,
            evidence,
        )
    )
    await socket.sent.get()
    if mode == "error":
        await socket.incoming.put({"type": "error", "error": {"code": "test_error"}})
    else:
        session.closed.set()
    with pytest.raises(exception):
        await asyncio.wait_for(task, 2)
    await session.close("test")


@pytest.mark.asyncio
@pytest.mark.parametrize("status", ["completed", "cancelled", "incomplete"])
async def test_counterpart_tools_require_completed_response_and_do_not_block_audio(
    tmp_path, status
):
    import threading
    from types import SimpleNamespace

    from voice_bench.business.environment import FixtureWorkflow
    from voice_bench.fixture import fixture_case

    entered, release = threading.Event(), threading.Event()

    class Business:
        def __init__(self):
            self.actions = []
            self.requests = []

        def counterpart_tools(self, run_id):
            assert run_id == "worker-bound-run"
            return [
                {
                    "type": "function",
                    "name": "business_set_note",
                    **FixtureWorkflow.tool_definitions["set_note"],
                }
            ]

        def record_counterpart_request(self, *args):
            self.requests.append(args)

        def execute(self, run_id, tool, arguments, operation_id, *, actor):
            entered.set()
            if not release.wait(3):
                raise RuntimeError("Test did not release the tool")
            self.actions.append((run_id, tool, arguments, operation_id, actor))
            return {"ok": True, "record": {"note": "updated"}}

    evidence = LocalEvidence(tmp_path, uuid4(), uuid4())
    session, socket, business = Session(evidence, 24000), Socket(), Business()
    simulator = caller(socket)
    simulator.business = business
    task = asyncio.create_task(
        simulator.converse(
            SimpleNamespace(run_id="worker-bound-run"),
            fixture_case().counterpart,
            session,
            evidence,
        )
    )
    try:
        async with asyncio.timeout(6):
            update = await socket.sent.get()
            assert [t["name"] for t in update["session"]["tools"]] == [
                "business_set_note",
                "finish_counterpart",
            ]
            assert "user_task" not in update["session"]["instructions"]
            assert fixture_case().user_task.request not in update["session"]["instructions"]
            await socket.incoming.put({"type": "session.updated", "session": {"id": "fake"}})
            await socket.incoming.put({"type": "response.created"})
            await socket.incoming.put(
                {
                    "type": "response.function_call_arguments.done",
                    "name": "business_set_note",
                    "arguments": json.dumps({"record_id": "owned", "note": "updated"}),
                    "response_id": "business-response",
                    "call_id": "tool-call",
                }
            )
            # A tool proposal alone must not mutate anything.
            await session.receive(b"\x01\x00" * 480)
            assert (await socket.sent.get())["type"] == "input_audio_buffer.append"
            assert not entered.is_set() and business.actions == []
            await socket.incoming.put(
                {"type": "response.done", "response": {"id": "business-response", "status": status}}
            )
            if status == "incomplete":
                with pytest.raises(CallerFailure, match="incomplete"):
                    await task
                assert not business.actions and not business.requests
                events = [
                    json.loads(line)
                    for line in (evidence.directory / "events.jsonl").read_text().splitlines()
                ]
                assert any(e["kind"] == "counterpart_incomplete" for e in events)
                return
            if status == "completed":
                assert await asyncio.to_thread(entered.wait, 2)
                # Real reception continues while the business transaction is waiting.
                await session.receive(b"\x02\x00" * 480)
                assert (await socket.sent.get())["type"] == "input_audio_buffer.append"
                release.set()
                output = await socket.sent.get()
                assert output["item"]["type"] == "function_call_output"
                assert json.loads(output["item"]["output"])["ok"]
                assert (await socket.sent.get())["type"] == "response.create"
                assert business.actions == [
                    (
                        "worker-bound-run",
                        "set_note",
                        {"record_id": "owned", "note": "updated"},
                        "tool-call",
                        "counterpart",
                    )
                ]
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
            if status != "completed":
                assert not business.actions and not business.requests
    finally:
        release.set()
        task.cancel()
        await asyncio.gather(task, return_exceptions=True)
        await session.close("test")


@pytest.mark.asyncio
async def test_idle_after_completed_playback_is_unattributed_not_a_target_failure(tmp_path):
    evidence = LocalEvidence(tmp_path, uuid4(), uuid4())
    session, socket = Session(evidence, 24000), Socket()
    simulator = caller(socket)
    simulator.config = simulator.config.model_copy(update={"conversation_idle_seconds": 0.1})
    task = asyncio.create_task(
        simulator.converse(
            None, CounterpartBrief(role="Employee", goal="Test", known_facts={}), session, evidence
        )
    )
    try:
        await socket.sent.get()
        await socket.incoming.put({"type": "session.updated", "session": {"id": "fake"}})
        await socket.incoming.put({"type": "response.created"})
        await socket.incoming.put(
            {
                "type": "response.output_audio.delta",
                "item_id": "speech",
                "delta": base64.b64encode(b"\x01\x00" * 2400).decode(),
            }
        )
        await socket.incoming.put(
            {"type": "response.done", "response": {"id": "one", "status": "completed"}}
        )
        await asyncio.sleep(0.2)
        assert not task.done(), "Queued speech must finish playing before idle timeout"
        session.played["speech"] = 100
        with pytest.raises(TransportFailure, match="cause not established"):
            await asyncio.wait_for(task, 1)
        events = [
            json.loads(line)
            for line in (evidence.directory / "events.jsonl").read_text().splitlines()
        ]
        timeout = next(e for e in events if e["kind"] == "conversation_idle_timeout")
        assert timeout["payload"]["attribution"] == "unknown"
    finally:
        task.cancel()
        await asyncio.gather(task, return_exceptions=True)
        await session.close("test")


@pytest.mark.asyncio
async def test_silence_recovery_waits_for_playback_and_is_bounded(tmp_path):
    evidence = LocalEvidence(tmp_path, uuid4(), uuid4())
    session, socket = Session(evidence, 24000), Socket()
    simulator = caller(socket)
    simulator.config = simulator.config.model_copy(
        update={
            "conversation_idle_seconds": 0.2,
            "silence_recovery_seconds": 0.05,
            "max_silence_recovery_prompts": 1,
        }
    )
    task = asyncio.create_task(
        simulator.converse(
            None, CounterpartBrief(role="Employee", goal="Test", known_facts={}), session, evidence
        )
    )
    try:
        await socket.sent.get()
        await socket.incoming.put({"type": "session.updated", "session": {"id": "fake"}})
        await socket.incoming.put({"type": "response.created"})
        await socket.incoming.put(
            {
                "type": "response.output_audio.delta",
                "item_id": "speech",
                "delta": base64.b64encode(b"\x01\x00" * 2400).decode(),
            }
        )
        await socket.incoming.put(
            {"type": "response.done", "response": {"id": "one", "status": "completed"}}
        )
        await asyncio.sleep(0.15)
        assert socket.sent.empty(), "Never nudge over speech still queued for playback"
        session.played["speech"] = 100
        request = await asyncio.wait_for(socket.sent.get(), 1)
        assert request["type"] == "response.create"
        assert request["response"]["tool_choice"] == "none"
        assert "Employee" in request["response"]["instructions"]
        assert "Do not invent" in request["response"]["instructions"]
        await asyncio.sleep(0.15)
        assert socket.sent.empty(), "Do not request a second response while one is pending"
        await socket.incoming.put(
            {"type": "response.done", "response": {"id": "recovery", "status": "completed"}}
        )
        with pytest.raises(TransportFailure):
            await asyncio.wait_for(task, 1)
        assert socket.sent.empty(), "Exhausted recovery must not produce an endless prompt loop"
        events = [
            json.loads(line)
            for line in (evidence.directory / "events.jsonl").read_text().splitlines()
        ]
        assert sum(e["kind"] == "silence_recovery_requested" for e in events) == 1
    finally:
        task.cancel()
        await asyncio.gather(task, return_exceptions=True)
        await session.close("test")
