import asyncio
import os
import struct
import wave
from uuid import uuid4

import pytest

from voice_bench.channels.browser.adapter import BrowserSession
from voice_bench.evidence.local import LocalEvidence
from voice_bench.models import AudioFrame


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get("RUN_BROWSER_TESTS") != "1", reason="Opt-in local Chromium test")
@pytest.mark.parametrize("startup", range(5))
async def test_synthetic_microphone_publishes_mono(tmp_path, startup):
    evidence = LocalEvidence(tmp_path, uuid4(), uuid4())
    session = BrowserSession(evidence)
    try:
        await session.start({}, test=True)
        settings = await session.page.evaluate("bridge.microphoneSettings()")
        # The worklet has one output, but MediaStreamDestination independently
        # defaults to stereo. LiveKit infers its publication mode from this track.
        assert settings["channelCount"] == 1
        assert settings["sampleRate"] == session.rate
        # A running AudioContext can still have a dormant graph. Require actual
        # rendered frames, as publication depends on the graph having processed.
        async with asyncio.timeout(2):
            while not any(e["kind"] == "rendered_block" for e in await evidence.event_snapshot()):
                await session.flush_evidence()
                await asyncio.sleep(0.02)
        ready = [
            e
            for e in await evidence.event_snapshot()
            if e["kind"] == "transport_observation"
            and e["payload"].get("name") == "microphone_ready"
        ]
        assert ready and ready[-1]["payload"]["silent_sink"] is True
        assert ready[-1]["payload"]["audio_context_seconds"] > 0
    finally:
        await session.close("microphone format check")


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get("RUN_BROWSER_TESTS") != "1", reason="Opt-in local Chromium test")
async def test_streamed_playback_has_no_worker_inserted_gaps(tmp_path, monkeypatch):
    """Sample delivery alone is insufficient: storage must not pace the microphone."""
    import json

    evidence = LocalEvidence(tmp_path, uuid4(), uuid4())
    session = BrowserSession(evidence)
    try:
        await session.start({}, test=True)
        evaluate = session.page.evaluate

        async def delayed_bridge(expression, *args):
            if "bridge.push(" in expression:
                # A busy bridge adds round-trip latency, independent of audio time.
                await asyncio.sleep(0.035)
            return await evaluate(expression, *args)

        monkeypatch.setattr(session.page, "evaluate", delayed_bridge)
        # All input is already available. Each chunk is shorter than an utterance;
        # the browser's audio clock must play the chunks without worker pacing gaps.
        for index in range(20):
            await session.send_audio(
                AudioFrame(
                    pcm_s16le=struct.pack("<h", 2000) * 6000,
                    sample_rate_hz=24000,
                    sample_offset=index * 6000,
                    clock_id="synthetic",
                    observed_monotonic_ns=0,
                    item_id="continuous-speech",
                )
            )
        await asyncio.wait_for(session.drain(), 10)
    finally:
        await session.close("continuity regression")
    events = [
        json.loads(line) for line in (evidence.directory / "events.jsonl").read_text().splitlines()
    ]
    progress = [e["payload"] for e in events if e["kind"] == "playback_progress"]
    delivered = sum(p["samples"] for p in progress)
    elapsed = progress[-1]["sample"] + progress[-1]["samples"] - progress[0]["sample"]
    assert delivered >= 239999
    # Allow one audio quantum, not cumulative HTTP/storage/scheduler overhead.
    assert elapsed - delivered <= 128
    await evidence.finalize(evidence.run_id)


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get("RUN_BROWSER_TESTS") != "1", reason="Opt-in local Chromium test")
@pytest.mark.parametrize("end_actor", ["target", "counterpart"])
async def test_final_report_preserves_browser_audio_until_hangup(store, tmp_path, end_actor):
    from test_controller import batch, configured

    from voice_bench.business.environment import BusinessService
    from voice_bench.contracts import CounterpartFinished
    from voice_bench.controller.runner import Controller

    config = configured(tmp_path)
    config = config.model_copy(
        update={
            # Leave room for cold Chromium audio startup while still requiring all
            # three seconds of speech after report receipt. The old two-second
            # shutdown path still fails the exact playback assertion below.
            "limits": config.limits.model_copy(update={"max_call_seconds": 10}),
            "runtime": config.runtime.model_copy(
                update={"setup_timeout_seconds": 10, "finalize_timeout_seconds": 5}
            ),
        }
    )
    plan, case = batch(store, config)
    case = case.model_copy(
        update={
            "completion": "target_report_then_hangup"
            if end_actor == "target"
            else "target_report_then_conversation_end",
            "target_tools": ("submit_user_report",),
        }
    )
    started = asyncio.Event()

    class LocalChannel:
        session = None

        async def connect(self, request, evidence):
            call_id = str(request.run.run_id)
            store.bind("rumik", call_id, request.run.run_id)
            BusinessService(store).serve_user_task(call_id, "test")
            self.session = BrowserSession(evidence)
            await self.session.start({}, test=True)
            return self.session

        async def reconcile(self, run_id, evidence):
            # Local transport proof only: no provider is contacted by this test.
            return self.session.browser is None and self.session.recorder.closed

    class Counterpart:
        async def converse(self, run, brief, session, evidence):
            await session.send_audio(
                AudioFrame(
                    pcm_s16le=struct.pack("<h", 2000) * 72000,
                    sample_rate_hz=24000,
                    sample_offset=0,
                    clock_id="test",
                    observed_monotonic_ns=0,
                    item_id="closing",
                )
            )
            started.set()
            if end_actor == "counterpart":
                await session.drain()
                return CounterpartFinished(tool_call_id="finish-after-real-playback")
            await asyncio.sleep(30)

    async def submit_report():
        await started.wait()
        run = store.runs(plan.batch_id)[0]
        receipt = BusinessService(store).submit_user_report(
            str(run["run_id"]), "test", "The task could not be completed."
        )
        await channel.session.drain()
        assert channel.session.played["closing"] >= 2999
        if end_actor == "target":
            await channel.session.event(None, {"type": "target_left"})
        return receipt

    channel = LocalChannel()
    pending = asyncio.create_task(submit_report())
    try:
        result = await Controller(store, config, channel, Counterpart()).execute(plan, case, "x")
        assert result.error is None and result.termination_confirmed
        assert result.conversation_end == (
            "target_hangup" if end_actor == "target" else "counterpart_finish"
        )
        assert (await pending)["ok"]
        assert channel.session.browser is None and channel.session.page is None
        saved = store.run(result.run_id)
        assert saved["evidence_sealed"] and not saved["reservation"]["active"]
    finally:
        pending.cancel()
        await asyncio.gather(pending, return_exceptions=True)
        if channel.session:
            await channel.session.close("test cleanup")


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get("RUN_BROWSER_TESTS") != "1", reason="Opt-in local Chromium test")
async def test_browser_full_duplex_playback_cancel_and_cleanup(tmp_path):
    evidence = LocalEvidence(tmp_path, uuid4(), uuid4())
    session = BrowserSession(evidence)
    try:
        await session.start({}, test=True)
        await session.page.evaluate("bridge.testInput()")
        frame = AudioFrame(
            pcm_s16le=struct.pack("<h", 2000) * 24000,
            sample_rate_hz=24000,
            sample_offset=0,
            clock_id="test",
            observed_monotonic_ns=0,
            item_id="first",
        )
        await session.send_audio(frame)
        async with asyncio.timeout(5):
            while True:
                received = await session.incoming.get()
                if any(received.pcm_s16le):
                    break
        async with asyncio.timeout(5):
            while session.played.get("first", 0) < 100:
                await asyncio.sleep(0.02)
        played = await session.cancel_playback()
        assert 0 < played["first"] < 1000
        assert await session.page.evaluate("bridge.push('AAAAAA==', 'stale', 0)") == "cancelled"
        await session.send_audio(frame.model_copy(update={"item_id": "after-cancel"}))
        await asyncio.wait_for(session.drain(), 3)
        assert session.played["after-cancel"] >= 999
        before = session.received_samples
        await asyncio.sleep(0.1)
        assert session.received_samples > before
    finally:
        await session.close("test")
        await session.close("idempotent cleanup")
    for name in ("received", "played", "sent"):
        with wave.open(str(evidence.directory / f"audio/{name}.wav"), "rb") as handle:
            assert handle.getnframes() > 0
    await evidence.finalize(evidence.run_id)


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get("RUN_BROWSER_TESTS") != "1", reason="Opt-in local Chromium test")
async def test_browser_startup_keeps_audio_past_former_five_second_limit(tmp_path):
    evidence = LocalEvidence(tmp_path, uuid4(), uuid4())
    session = BrowserSession(evidence, startup_seconds=10)
    try:
        await session.start({}, test=True)
        await session.page.evaluate("bridge.testInput()")
        async with asyncio.timeout(9):
            while session.received_samples < 48000 * 6:
                session.check_health()
                await asyncio.sleep(0.05)
        session.check_health()
        stream = session.received_audio()
        first = await anext(stream)
        assert first.sample_offset == 0
        assert session.received_samples > 48000 * 5
        await stream.aclose()
    finally:
        await session.close("startup regression")
    assert session.browser is None and session.recorder.closed
    await evidence.finalize(evidence.run_id)


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get("RUN_BROWSER_TESTS") != "1", reason="Opt-in local Chromium test")
async def test_remote_webrtc_audio_contains_real_pcm(tmp_path):
    evidence = LocalEvidence(tmp_path, uuid4(), uuid4())
    session = BrowserSession(evidence)
    try:
        await session.start({}, test=True)
        await session.page.evaluate(r"""async () => {
    const audio = new AudioContext({sampleRate:48000}); await audio.resume();
    const source = audio.createOscillator(); const dest = audio.createMediaStreamDestination();
    source.connect(dest); source.start();
    const a = new RTCPeerConnection(); const b = new RTCPeerConnection();
    window.localPeers = [a,b];
    // Both endpoints are local. Avoid relying on VPN/LAN/mDNS reachability.
    const loopback = c => ({...c.toJSON(), candidate:
      c.candidate.replace(/(candidate:\S+ \d+ udp \d+ )\S+/i, '$1127.0.0.1')});
    a.onicecandidate=e=>{if(e.candidate)b.addIceCandidate(loopback(e.candidate))};
    b.onicecandidate=e=>{if(e.candidate)a.addIceCandidate(loopback(e.candidate))};
    b.ontrack=e=>{
      window.remoteStream=e.streams[0]; bridge.testCaptureStream(e.streams[0]);
      bridge.testObserveTrack('loopback-in', {
        getRTCStatsReport: () => e.receiver.getStats(), mediaStreamTrack: e.track,
      }, 'incoming');
    };
    a.addTrack(dest.stream.getAudioTracks()[0],dest.stream);
    await a.setLocalDescription(await a.createOffer());
    await b.setRemoteDescription(a.localDescription);
    await b.setLocalDescription(await b.createAnswer());
    await a.setRemoteDescription(b.localDescription);
  }""")
        async with asyncio.timeout(5):
            while True:
                frame = await session.incoming.get()
                if any(frame.pcm_s16le):
                    break
        assert frame.sample_rate_hz == 48000
        assert await session.page.evaluate(
            "localPeers.every(p => p.connectionState === 'connected')"
        )
        async with asyncio.timeout(4):
            while True:
                observed = await evidence.event_snapshot()
                stats = [
                    e["payload"]
                    for e in observed
                    if e["kind"] == "transport_observation"
                    and e["payload"].get("name") == "audio_transport_stats"
                ]
                if any(r.get("packetsReceived", 0) > 0 for s in stats for r in s.get("rows", [])):
                    break
                await asyncio.sleep(0.05)
    finally:
        await session.close("webrtc regression")
    native = evidence.directory / "audio/received-native-0.webm"
    assert native.stat().st_size > 100
    import shutil
    import subprocess

    if shutil.which("ffmpeg"):
        decoded = subprocess.run(
            ["ffmpeg", "-v", "error", "-i", str(native), "-f", "s16le", "-ac", "1", "-"],
            capture_output=True,
            check=True,
            timeout=10,
        ).stdout
        assert len(decoded) > 16000 and any(decoded)
    await evidence.finalize(evidence.run_id)


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get("RUN_BROWSER_TESTS") != "1", reason="Opt-in local Chromium test")
async def test_full_duplex_under_slow_evidence_sink_preserves_playback(tmp_path, monkeypatch):
    import json

    evidence = LocalEvidence(tmp_path, uuid4(), uuid4())
    original = evidence.emit_many

    async def slower(observations):
        # Six milliseconds per binding would overload the former ~475 events/sec stream.
        await asyncio.sleep(0.006)
        return await original(observations)

    monkeypatch.setattr(evidence, "emit_many", slower)
    session = BrowserSession(evidence)
    consumer = None
    captured = []

    async def receive():
        async for frame in session.received_audio():
            captured.append(frame.sample_offset)

    try:
        await session.start({}, test=True)
        await session.page.evaluate("bridge.testInput()")
        consumer = asyncio.create_task(receive())
        # Pace each second of speech; the bounded audio queue remains meaningful.
        for second in range(10):
            await session.send_audio(
                AudioFrame(
                    pcm_s16le=struct.pack("<h", 2000) * 24000,
                    sample_rate_hz=24000,
                    sample_offset=second * 24000,
                    clock_id="synthetic",
                    observed_monotonic_ns=0,
                    item_id="long-readback",
                )
            )
            await asyncio.sleep(1)
            session.check_health()
        await asyncio.wait_for(session.drain(), 5)
        assert session.played["long-readback"] >= 9999
        assert len(captured) >= 400 and captured == sorted(set(captured))
    finally:
        if consumer:
            consumer.cancel()
            await asyncio.gather(consumer, return_exceptions=True)
        await session.close("slow sink regression")
    events = [
        json.loads(line) for line in (evidence.directory / "events.jsonl").read_text().splitlines()
    ]
    assert not any(e["kind"] == "bridge_error" for e in events)
    progress = [e for e in events if e["kind"] == "playback_progress"]
    assert 400 < len(progress) < 600
    assert sum(e["payload"]["samples"] for e in progress) >= 479950
    await evidence.finalize(evidence.run_id)
