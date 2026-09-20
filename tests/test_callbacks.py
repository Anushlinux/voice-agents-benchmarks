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
