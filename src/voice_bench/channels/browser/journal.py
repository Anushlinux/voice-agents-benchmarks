"""Bounded persistence queue: disk latency must not become conversational latency."""

import asyncio
import time
from datetime import UTC, datetime

from voice_bench.errors import HarnessFailure


class BrowserJournal:
    def __init__(self, evidence, failed, capacity=4096):
        self.evidence, self.failed = evidence, failed
        self.queue = asyncio.Queue(capacity)
        self.worker = None
        self.error = None
        self.closed = False

    def submit(self, *, write=None, observations=()):
        if self.error or self.closed:
            raise HarnessFailure("Browser evidence writer is unavailable")
        observations = [
            dict(
                item,
                observed_ns=item.get("observed_ns") or time.monotonic_ns(),
                observed_at=item.get("observed_at") or datetime.now(UTC),
            )
            for item in observations
        ]
        try:
            self.queue.put_nowait((write, observations))
        except asyncio.QueueFull:
            self.error = "evidence_queue_overflow"
            self.failed(self.error)
            raise HarnessFailure("Browser evidence queue overflow") from None
        if self.worker is None or self.worker.done():
            self.worker = asyncio.create_task(self._persist())

    async def _persist(self):
        try:
            while not self.queue.empty():
                jobs = [self.queue.get_nowait() for _ in range(min(64, self.queue.qsize()))]
                try:
                    writes = [write for write, _ in jobs if write is not None]
                    if writes:
                        await asyncio.to_thread(self._write, writes)
                    observations = [item for _, items in jobs for item in items]
                    for start in range(0, len(observations), 100):
                        await self.evidence.emit_many(observations[start : start + 100])
                finally:
                    for _ in jobs:
                        self.queue.task_done()
        except Exception:
            self.error = "evidence_write_failed"
            self.failed(self.error)
            while not self.queue.empty():
                self.queue.get_nowait()
                self.queue.task_done()

    @staticmethod
    def _write(writes):
        for write in writes:
            write()

    async def flush(self):
        await self.queue.join()
        if self.error:
            raise HarnessFailure("Browser evidence could not be persisted")

    async def close(self):
        self.closed = True
        await self.flush()


class BufferedEvidence:
    def __init__(self, journal):
        self.journal = journal

    def __getattr__(self, name):
        return getattr(self.journal.evidence, name)

    async def emit_many(self, observations):
        self.journal.submit(observations=observations)

    async def emit(self, source, kind, payload=None, *, clock_id=None, observed_ns=None):
        await self.emit_many(
            [
                dict(
                    source=source,
                    kind=kind,
                    payload=payload or {},
                    clock_id=clock_id,
                    observed_ns=observed_ns,
                )
            ]
        )


class BufferedRecorder:
    def __init__(self, recorder, journal):
        self.recorder, self.journal = recorder, journal

    @property
    def closed(self):
        return self.recorder.closed

    async def write(self, name, frame):
        self.journal.submit(write=lambda: self.recorder._write(name, frame))

    async def close(self):
        try:
            await self.journal.close()
        finally:
            await self.recorder.close()
