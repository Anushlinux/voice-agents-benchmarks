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
@pytest.mark.parametrize("first_sequence", [0, 1])
async def test_phone_correlation_codec_checkpoints_and_sequence(
    store, prepared, tmp_path, first_sequence
):
    _, (run_id, _) = prepared
    store.bind("plivo", "call", run_id)
    session = PhoneSession(LocalEvidence(tmp_path, uuid4(), run_id), store, run_id, "account", 10)
    session.socket = Socket()
    await session.handle(
        {
            "event": "start",
            "sequenceNumber": first_sequence,
            "start": {
                "callId": "call",
                "streamId": "stream",
                "accountId": "10229869",
                "mediaFormat": {"encoding": "audio/x-mulaw", "sampleRate": 8000},
            },
        }
    )
    await session.handle(
        {
            "event": "media",
            "sequenceNumber": first_sequence + 1,
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
        {
            "event": "playedStream",
            "sequenceNumber": first_sequence + 1,
            "streamId": "stream",
            "name": "checkpoint",
        }
    )
    assert session.played["item"] == 100
    media = {
        "event": "media",
        "sequenceNumber": first_sequence + 3,
        "streamId": "stream",
        "media": {
            "track": "inbound",
            "timestamp": "1020",
            "chunk": 2,
            "payload": base64.b64encode(b"\xff" * 160).decode(),
        },
    }
    await session.handle(media)
    assert (await session.incoming.get()).pcm_s16le == b"\0" * 320
    # Duplicate audio must still fail even when carrier event numbers advance.
    with pytest.raises(ValueError, match="sequence"):
        await session.handle({**media, "sequenceNumber": first_sequence + 4})
    with pytest.raises(ValueError, match="sequence"):
        await session.handle({**media, "media": {**media["media"], "chunk": 4}})
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


@pytest.mark.parametrize(
    ("record", "ended"),
    [
        ({"call_status": "record_pending"}, False),
        ({"call_state": "ANSWER"}, False),
        ({"call_status": "timeout"}, True),
        ({"end_time": "2026-09-22 06:55:12+00:00", "hangup_cause_code": 3020}, True),
        ({"hangup_cause_name": "Unknown", "hangup_cause_code": 0}, True),
    ],
)
def test_carrier_terminal_records(record, ended):
    from voice_bench.channels.phone.adapter import carrier_leg_ended

    assert carrier_leg_ended(record) is ended


@pytest.mark.asyncio
async def test_plivo_sip_auth_stays_in_dial_request():
    import json

    import httpx

    from voice_bench.channels.phone.adapter import PlivoClient

    requests = []

    def respond(request):
        requests.append(json.loads(request.content))
        return httpx.Response(201, json={"request_uuid": "test-call"})

    client = PlivoClient(
        "account",
        "token",
        transport=httpx.MockTransport(respond),
        sip_username="test-user",
        sip_password="OnlySynthetic123",
    )
    try:
        await client.dial(
            "+10000000001",
            "sip:+10000000002@sip.example;transport=tcp",
            "https://benchmark.example",
            uuid4(),
            180,
        )
        assert requests[0]["sip_auth_username"] == "test-user"
        assert requests[0]["sip_auth_password"] == "OnlySynthetic123"
        assert requests[0]["to"].endswith(";transport=tcp")
        assert requests[0]["time_limit"] == 180
        with pytest.raises(ValueError, match="SIP destination"):
            await client.dial(
                "+10000000001", "+10000000002", "https://benchmark.example", uuid4(), 180
            )
        assert len(requests) == 1
    finally:
        await client.close()


@pytest.mark.asyncio
async def test_phone_close_tolerates_carrier_disconnect(tmp_path):
    from starlette.websockets import WebSocketDisconnect

    class DisconnectedSocket:
        async def close(self):
            raise WebSocketDisconnect(1006)

    run_id = uuid4()
    session = PhoneSession(LocalEvidence(tmp_path, uuid4(), run_id), None, run_id, "account", 10)
    session.socket = DisconnectedSocket()
    await session.close("reconcile")
    assert session.closed.is_set()
