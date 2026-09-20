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
async def test_final_report_closes_real_browser_without_native_hangup(store, tmp_path):
    from test_controller import batch, configured

    from voice_bench.business.environment import BusinessService
    from voice_bench.controller.runner import Controller

    config = configured(tmp_path)
    config = config.model_copy(
        update={
            "limits": config.limits.model_copy(update={"max_call_seconds": 5}),
            "runtime": config.runtime.model_copy(
                update={"setup_timeout_seconds": 10, "finalize_timeout_seconds": 5}
            ),
        }
    )
    plan, case = batch(store, config)
    case = case.model_copy(
        update={"completion": "target_report_then_hangup", "target_tools": ("submit_user_report",)}
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
                    pcm_s16le=struct.pack("<h", 2000) * 2400,
                    sample_rate_hz=24000,
                    sample_offset=0,
                    clock_id="test",
                    observed_monotonic_ns=0,
                    item_id="closing",
                )
            )
            started.set()
            await asyncio.sleep(30)

    async def submit_report():
        await started.wait()
        run = store.runs(plan.batch_id)[0]
        return BusinessService(store).submit_user_report(
            str(run["run_id"]), "test", "The task could not be completed."
        )

    channel = LocalChannel()
    pending = asyncio.create_task(submit_report())
    try:
        result = await Controller(store, config, channel, Counterpart()).execute(plan, case, "x")
        assert result.error is None and result.termination_confirmed
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
        await session.page.evaluate("""async () => {
    const audio = new AudioContext({sampleRate:48000}); await audio.resume();
    const source = audio.createOscillator(); const dest = audio.createMediaStreamDestination();
    source.connect(dest); source.start();
    const a = new RTCPeerConnection(); const b = new RTCPeerConnection();
    window.localPeers = [a,b];
    a.onicecandidate=e=>{if(e.candidate)b.addIceCandidate(e.candidate)};
    b.onicecandidate=e=>{if(e.candidate)a.addIceCandidate(e.candidate)};
    b.ontrack=e=>{ window.remoteStream=e.streams[0]; bridge.testCaptureStream(e.streams[0]); };
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
    finally:
        await session.close("webrtc regression")
    await evidence.finalize(evidence.run_id)
