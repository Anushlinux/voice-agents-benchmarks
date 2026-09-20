import asyncio
import base64
import json
from uuid import uuid4

import pytest

from voice_bench.caller.openai_realtime import OpenAICaller
from voice_bench.channels.media import MediaSession
from voice_bench.contracts import CallerConfig
from voice_bench.errors import CallerFailure, TransportFailure
from voice_bench.evidence.local import LocalEvidence
from voice_bench.models import CallerBrief


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
    return OpenAICaller(
        CallerConfig(
            model="test-model",
            voice="test-voice",
            instructions="Assigned behavior.",
            turn_detection={"type": "server_vad"},
        ),
        "test-key",
        lambda *a, **kw: socket,
    )


@pytest.mark.asyncio
async def test_realtime_customer_receives_audio_and_truncates_unplayed_speech(tmp_path):
    evidence = LocalEvidence(tmp_path, uuid4(), uuid4())
    session, socket = Session(evidence, 24000), Socket()
    brief = CallerBrief(goal="Change my note", known_facts={"name": "Synthetic Customer"})
    task = asyncio.create_task(caller(socket).converse(None, brief, session, evidence))
    try:
        async with asyncio.timeout(5):
            update = await socket.sent.get()
            assert update["session"]["audio"]["output"]["voice"] == "test-voice"
            instructions = update["session"]["instructions"]
            assert "Synthetic Customer" in instructions
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
            await socket.incoming.put(
                {"type": "response.function_call_arguments.done", "name": "finish_customer"}
            )
            await task
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
        caller(socket).converse(None, CallerBrief(goal="Test", known_facts={}), session, evidence)
    )
    await socket.sent.get()
    if mode == "error":
        await socket.incoming.put({"type": "error", "error": {"code": "test_error"}})
    else:
        session.closed.set()
    with pytest.raises(exception):
        await asyncio.wait_for(task, 2)
    await session.close("test")
