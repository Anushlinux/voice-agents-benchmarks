import base64
import json
from uuid import uuid4

import httpx
import pytest

from voice_bench.channels.phone.adapter import PhoneSession
from voice_bench.evidence.local import LocalEvidence
from voice_bench.target.rumik.client import RumikClient


@pytest.mark.asyncio
async def test_registered_browser_redemption_has_no_account_key():
    requests = []

    def handler(request):
        requests.append(request)
        if request.url.path.endswith("register-call"):
            return httpx.Response(201, json={"call_id": "call", "access_token": "single-use"})
        return httpx.Response(200, json={"callId": "call"})

    client = RumikClient("unit-test-key", transport=httpx.MockTransport(handler))
    registration = await client.register("agent")
    await client.start_browser(registration["access_token"])
    await client.close()
    assert requests[0].headers["Authorization"] == "Bearer unit-test-key"
    assert "Authorization" not in requests[1].headers
    assert json.loads(requests[1].content) == {"accessToken": "single-use"}


@pytest.mark.asyncio
@pytest.mark.parametrize("status", [401, 402, 409, 429, 500])
async def test_call_start_is_never_retried_automatically(status):
    requests = []

    def handler(request):
        requests.append(request)
        return httpx.Response(status, json={"code": "failed"})

    client = RumikClient("test", transport=httpx.MockTransport(handler))
    with pytest.raises(httpx.HTTPStatusError):
        await client.start_browser("token")
    assert len(requests) == 1
    await client.close()


class Socket:
    def __init__(self):
        self.sent = []

    async def send_json(self, message):
        self.sent.append(message)

    async def close(self):
        pass


@pytest.mark.asyncio
async def test_phone_correlation_codec_checkpoints_and_sequence(store, prepared, tmp_path):
    _, (run_id, _) = prepared
    store.bind("plivo", "call", run_id)
    session = PhoneSession(LocalEvidence(tmp_path, uuid4(), run_id), store, run_id, "account", 10)
    session.socket = Socket()
    await session.handle(
        {
            "event": "start",
            "sequenceNumber": 1,
            "start": {
                "callId": "call",
                "streamId": "stream",
                "accountId": "account",
                "mediaFormat": {"encoding": "audio/x-mulaw", "sampleRate": 8000},
            },
        }
    )
    await session.handle(
        {
            "event": "media",
            "sequenceNumber": 2,
            "streamId": "stream",
            "media": {
                "track": "inbound",
                "timestamp": "1000",
                "chunk": 1,
                "payload": base64.b64encode(b"\xff" * 160).decode(),
            },
        }
    )
    frame = await session.incoming.get()
    assert frame.pcm_s16le == b"\0" * 320
    session.pending["checkpoint"] = ("item", 800, 0)
    await session.handle(
        {"event": "playedStream", "sequenceNumber": 3, "streamId": "stream", "name": "checkpoint"}
    )
    assert session.played["item"] == 100
    with pytest.raises(ValueError, match="sequence"):
        await session.handle({"event": "media", "sequenceNumber": 5})
    await session.close("test")


@pytest.mark.asyncio
async def test_phone_rejects_cross_run_stream(store, prepared, tmp_path):
    _, (first, second) = prepared
    store.bind("plivo", "other-call", second)
    session = PhoneSession(LocalEvidence(tmp_path, uuid4(), first), store, first, "account", 10)
    with pytest.raises(ValueError, match="another"):
        await session.handle(
            {
                "event": "start",
                "sequenceNumber": 1,
                "start": {
                    "callId": "other-call",
                    "streamId": "stream",
                    "accountId": "account",
                    "mediaFormat": {"encoding": "audio/x-mulaw", "sampleRate": 8000},
                },
            }
        )
    await session.close("test")
