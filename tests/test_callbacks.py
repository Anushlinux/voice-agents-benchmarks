from pathlib import Path
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient
from plivo.utils.signature_v3 import construct_get_url, construct_post_url, get_signature_v3
from starlette.websockets import WebSocketDisconnect

from voice_bench.api.app import create_app
from voice_bench.channels.phone.adapter import PhoneHub
from voice_bench.settings import load_config


def signed(path, params=None, websocket=False):
    uri = ("wss" if websocket else "https") + "://benchmark.example" + path
    base = construct_get_url(uri, {}) if websocket else construct_post_url(uri, params or {})
    value = get_signature_v3(b"test-token", base.decode(), b"test-nonce").decode()
    return {"x-plivo-signature-v3": value, "x-plivo-signature-v3-nonce": "test-nonce"}


def hub_for(store, run_id):
    config = load_config(Path("configs/local.toml"))
    config = config.model_copy(
        update={
            "runtime": config.runtime.model_copy(
                update={
                    "public_base_url": "https://benchmark.example",
                    "caller_number": "+10000000001",
                    "target_number": "+10000000002",
                }
            )
        }
    )
    hub = PhoneHub(store, config, SimpleNamespace(token="test-token"))
    hub.sessions[run_id] = SimpleNamespace(
        token="session-token", socket=None, closed=SimpleNamespace(set=lambda: None)
    )
    store.update_run(run_id, dispatch_intent=True, phase="connecting")
    return hub


def test_carrier_authentication_and_duplicate_early_failure(store, prepared):
    _, (run_id, _) = prepared
    hub = hub_for(store, run_id)
    path = f"/callbacks/plivo/status/{run_id}"
    params = {
        "CallUUID": "early-failure",
        "From": "+10000000001",
        "To": "+10000000002",
        "CallStatus": "completed",
        "Event": "failed",
    }
    with TestClient(create_app(store, "tools-secret", hub)) as client:
        assert client.post(path, data=params).status_code == 401
        headers = signed(path, params)
        assert client.post(path, data=params, headers=headers).status_code == 200
        assert client.post(path, data=params, headers=headers).status_code == 200
        tampered = {**params, "CallUUID": "different-call"}
        assert client.post(path, data=tampered, headers=headers).status_code == 401
        assert client.post(path, data=tampered, headers=signed(path, tampered)).status_code == 409
    assert len(store.run(run_id)["carrier_callbacks"]) == 1
    assert store.resolve("plivo", "early-failure") == run_id


def test_media_rejects_bad_signature_and_wrong_session_token(store, prepared):
    _, (run_id, _) = prepared
    hub = hub_for(store, run_id)
    with TestClient(create_app(store, "tools-secret", hub)) as client:
        for token in ("session-token", "wrong-token"):
            path = f"/callbacks/plivo/media/{run_id}/{token}"
            headers = {} if token == "session-token" else signed(path, websocket=True)
            with pytest.raises(WebSocketDisconnect):
                with client.websocket_connect(path, headers=headers):
                    pass


def test_signed_answer_returns_narrow_stream_and_binds_call(store, prepared):
    _, (run_id, _) = prepared
    hub = hub_for(store, run_id)
    params = {"CallUUID": "answered", "From": "+10000000001", "To": "+10000000002"}
    path = f"/callbacks/plivo/answer/{run_id}"
    with TestClient(create_app(store, "tools-secret", hub)) as client:
        response = client.post(path, data=params, headers=signed(path, params))
        assert response.status_code == 200
        assert 'bidirectional="true"' in response.text
        assert "audio/x-mulaw;rate=8000" in response.text
        assert "test-token" not in response.text
    assert store.resolve("plivo", "answered") == run_id


def test_answer_accepts_carrier_number_formats_and_sip_destination(store, prepared):
    _, (run_id, _) = prepared
    hub = hub_for(store, run_id)
    hub.config = hub.config.model_copy(
        update={
            "runtime": hub.config.runtime.model_copy(
                update={"target_sip_uri": "sip:+10000000002@sip.example"}
            )
        }
    )
    hub.agent_aliases = {"ua_handle"}
    assert hub.canonical_agent("ua_handle") == hub.agent_id
    assert hub.canonical_agent("someone-else") == "someone-else"
    path = f"/callbacks/plivo/answer/{run_id}"
    with TestClient(create_app(store, "tools-secret", hub)) as client:
        params = {
            "CallUUID": "sip-leg",
            "From": "10000000001",
            "To": "sip:+10000000002@sip.example",
        }
        assert client.post(path, data=params, headers=signed(path, params)).status_code == 200
        wrong = {"CallUUID": "other-leg", "From": "10000000009", "To": "+10000000002"}
        assert client.post(path, data=wrong, headers=signed(path, wrong)).status_code == 409
    assert store.resolve("plivo", "sip-leg") == run_id


@pytest.mark.parametrize("status", ["no-answer", "failed", "busy", "cancel", "timeout"])
def test_early_hangup_wakes_waiting_phone_session(store, prepared, status):
    from threading import Event

    _, (run_id, _) = prepared
    hub = hub_for(store, run_id)
    hub.sessions[run_id].closed = Event()
    path = f"/callbacks/plivo/status/{run_id}"
    params = {
        "CallUUID": "rejected-call",
        "From": "+10000000001",
        "To": "+10000000002",
        "CallStatus": status,
        "Event": "Hangup",
        "HangupCause": "CALL_REJECTED",
    }
    with TestClient(create_app(store, "tools-secret", hub)) as client:
        assert client.post(path, data=params, headers=signed(path, params)).status_code == 200
    assert hub.sessions[run_id].closed.is_set()
    assert store.resolve("plivo", "rejected-call") == run_id


@pytest.mark.parametrize("scheme", ["wss", "https", "http"])
def test_media_accepts_signed_public_upgrade_url(store, prepared, scheme):
    _, (run_id, _) = prepared
    hub = hub_for(store, run_id)

    async def attach(socket):
        await socket.send_json({"attached": True})
        await socket.close()

    hub.sessions[run_id].attach = attach
    path = f"/callbacks/plivo/media/{run_id}/session-token"
    uri = scheme + "://benchmark.example" + path
    value = get_signature_v3(b"test-token", uri, b"test-nonce").decode()
    headers = {"x-plivo-signature-v3": value, "x-plivo-signature-v3-nonce": "test-nonce"}
    with TestClient(create_app(store, "tools-secret", hub)) as client:
        with client.websocket_connect(path, headers=headers) as socket:
            assert socket.receive_json() == {"attached": True}
