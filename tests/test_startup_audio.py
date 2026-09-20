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
