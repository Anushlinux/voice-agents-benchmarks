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
