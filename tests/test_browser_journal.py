import asyncio
import json
import threading
import wave
from uuid import uuid4

import pytest

from voice_bench.channels.browser.adapter import BrowserSession
from voice_bench.channels.browser.journal import BrowserJournal
from voice_bench.errors import HarnessFailure
from voice_bench.evidence.local import LocalEvidence, verify_bundle


@pytest.mark.asyncio
async def test_disk_pause_does_not_hold_up_hearing_and_flush_preserves_every_sample(tmp_path):
    evidence = LocalEvidence(tmp_path, uuid4(), uuid4())
    session = BrowserSession(evidence)
    blocked, release = threading.Event(), threading.Event()

    def stall_disk():
        blocked.set()
        assert release.wait(5)

    session.journal.submit(write=stall_disk)
    await asyncio.to_thread(blocked.wait, 1)
    stream = session.received_audio()
    try:
        for index in range(100):
            await session._event(
                dict(type="received", samples=[0.1] * 960, sample=index * 960, rate=48000)
            )
            # The disk is still blocked, but each live frame is immediately available.
            frame = await asyncio.wait_for(anext(stream), 0.1)
            assert frame.sample_offset == index * 960
        flush = asyncio.create_task(session.flush_evidence())
        await asyncio.sleep(0.02)
        assert not flush.done()
        release.set()
        await asyncio.wait_for(flush, 3)
    finally:
        release.set()
        await stream.aclose()
        await session.close("test")
    with wave.open(str(evidence.directory / "audio/received.wav")) as audio:
        assert audio.getnframes() == 96000
    events = [json.loads(s) for s in (evidence.directory / "events.jsonl").read_text().splitlines()]
    blocks = [e for e in events if e["kind"] == "received_block"]
    assert [e["payload"]["recording_offset"] for e in blocks] == list(range(0, 96000, 960))
    await evidence.finalize(evidence.run_id)
    verify_bundle(evidence.directory)


@pytest.mark.asyncio
async def test_persistence_failure_and_overflow_are_harness_failures(tmp_path):
    evidence = LocalEvidence(tmp_path, uuid4(), uuid4())
    failures = []
    journal = BrowserJournal(evidence, failures.append, capacity=2)

    def broken():
        raise OSError("Synthetic write failure")

    journal.submit(write=broken)
    with pytest.raises(HarnessFailure, match="persisted"):
        await journal.flush()
    assert failures == ["evidence_write_failed"]
    journal = BrowserJournal(evidence, failures.append, capacity=2)
    journal.submit()
    journal.submit()
    with pytest.raises(HarnessFailure, match="overflow"):
        journal.submit()
    with pytest.raises(HarnessFailure):
        await journal.close()
    assert failures[-1] == "evidence_queue_overflow"
    session = BrowserSession(evidence)
    session.fail("event_queue_overflow")
    with pytest.raises(HarnessFailure):
        await session.send_audio(None)
    await session.close("test")
