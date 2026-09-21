import wave
from uuid import uuid4

import pytest

from voice_bench.channels.media import MediaSession
from voice_bench.errors import HarnessFailure
from voice_bench.evidence.local import LocalEvidence


@pytest.mark.asyncio
async def test_startup_audio_survives_task_wait_and_replays_in_order(tmp_path):
    evidence = LocalEvidence(tmp_path, uuid4(), uuid4())
    session = MediaSession(evidence, 48000, startup_seconds=30)
    pcm = b"\x01\x00" * 960
    # Seven seconds exceeds the former five-second buffer.
    for _ in range(350):
        await session.receive(pcm)
    assert not session.closed.is_set()
    stream = session.received_audio()
    first = await anext(stream)
    await session.receive(pcm)  # Live arrivals continue while the backlog is replayed.
    frames = [first] + [await anext(stream) for _ in range(350)]
    assert [frame.sample_offset for frame in frames] == list(range(0, 351 * 960, 960))
    assert not session.startup_pending and not session.startup_frames
    await stream.aclose()
    await session.close("test")
    with wave.open(str(evidence.directory / "audio/received.wav")) as audio:
        assert audio.getnframes() == 351 * 960


@pytest.mark.asyncio
async def test_startup_buffer_still_has_a_hard_limit(tmp_path):
    session = MediaSession(LocalEvidence(tmp_path, uuid4(), uuid4()), 48000, startup_seconds=1)
    try:
        await session.receive(b"\0\0" * 48000)
        with pytest.raises(HarnessFailure):
            await session.receive(b"\0\0")
        with pytest.raises(HarnessFailure):
            session.check_health()
    finally:
        await session.close("test")


@pytest.mark.asyncio
@pytest.mark.parametrize("mode", ["local_error", "ready", "registration_error"])
async def test_browser_checks_local_audio_before_any_provider_dispatch(tmp_path, monkeypatch, mode):
    from types import SimpleNamespace

    from voice_bench.channels.browser import adapter as browser

    calls = []

    class Session:
        def __init__(self, evidence, **kwargs):
            pass

        async def prepare(self):
            calls.append("prepare")
            if mode == "local_error":
                raise HarnessFailure("local audio unavailable")

        async def join(self, call):
            calls.append("join")

        async def close(self, reason):
            calls.append("close")

    class Target:
        async def register(self, agent):
            calls.append("register")
            if mode == "registration_error":
                raise TimeoutError("Unknown registration result")
            return {"call_id": "call", "access_token": "test"}

        async def start_browser(self, token):
            calls.append("start_browser")
            return {"callId": "call"}

    monkeypatch.setattr(browser, "BrowserSession", Session)
    store = SimpleNamespace(bind=lambda *args: calls.append("bind"), bindings=lambda _: [])
    channel = browser.BrowserAdapter(Target(), store)
    sink = LocalEvidence(tmp_path, uuid4(), uuid4())
    request = SimpleNamespace(
        agent_ref="test", run=SimpleNamespace(run_id=sink.run_id), setup_timeout_seconds=10
    )
    assert not await channel.reconcile(sink.run_id, sink), "A fresh adapter proves nothing"
    if mode == "ready":
        await channel.connect(request, sink)
        assert calls == ["prepare", "register", "bind", "start_browser", "join"]
    elif mode == "local_error":
        with pytest.raises(HarnessFailure, match="Local browser audio preparation"):
            await channel.connect(request, sink)
        assert calls == ["prepare"]
        assert not any(e["source"] == "target" for e in await sink.event_snapshot())
        assert await channel.reconcile(sink.run_id, sink), "No provider request needs termination"
    else:
        with pytest.raises(TimeoutError):
            await channel.connect(request, sink)
        assert calls == ["prepare", "register"]
        assert not await channel.reconcile(sink.run_id, sink), "Unknown writes remain unresolved"
