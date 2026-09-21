"""Bounded independent audio paths and streaming PCM conversion."""

import asyncio
import audioop
import os
import time
import wave
from collections import deque

from voice_bench.errors import HarnessFailure, TransportFailure
from voice_bench.evidence.local import safe_path
from voice_bench.models import AudioFrame


class Resampler:
    def __init__(self, source_rate, target_rate):
        self.source_rate, self.target_rate = source_rate, target_rate
        self.state = None

    def convert(self, pcm):
        if self.source_rate == self.target_rate:
            return pcm
        output, self.state = audioop.ratecv(
            pcm, 2, 1, self.source_rate, self.target_rate, self.state
        )
        return output


class AudioRecorder:
    def __init__(self, evidence):
        self.evidence = evidence
        self.handles = {}
        self.lock = asyncio.Lock()
        self.closed = False

    def _write(self, name, frame):
        self.evidence._open()
        if self.closed:
            raise ValueError("Audio recorder is closed")
        if name not in self.handles:
            path = safe_path(self.evidence.directory, f"audio/{name}.wav")
            path.parent.mkdir(exist_ok=True)
            raw = path.open("xb")
            handle = wave.open(raw, "wb")
            handle.setparams((1, 2, frame.sample_rate_hz, 0, "NONE", "not compressed"))
            self.handles[name] = (handle, raw, frame.sample_rate_hz)
        handle, _, rate = self.handles[name]
        if frame.sample_rate_hz != rate:
            raise ValueError("Audio sample rate changed mid-stream")
        handle.writeframes(frame.pcm_s16le)

    async def write(self, name, frame):
        async with self.lock:
            await asyncio.to_thread(self._write, name, frame)

    async def close(self):
        async with self.lock:
            for handle, raw, _ in self.handles.values():
                await asyncio.to_thread(handle.close)
                raw.flush()
                await asyncio.to_thread(os.fsync, raw.fileno())
                raw.close()
            self.handles.clear()
            self.closed = True


class MediaSession:
    def __init__(self, evidence, rate, queue_size=250, *, startup_seconds=0):
        self.evidence, self.rate = evidence, rate
        self.incoming = asyncio.Queue(queue_size)
        self.outgoing = asyncio.Queue(queue_size)
        self.recorder = AudioRecorder(evidence)
        self.played = {}
        self.received_samples = 0
        self.closed = asyncio.Event()
        self.last_received = time.monotonic()
        self.last_received_speech_at = None
        self.error = None
        self.tasks = []
        self.converters = {}
        self.submitted_samples = 0
        # Task delivery may precede the counterpart's receive loop. Keep that
        # audio separately, bounded by the configured setup deadline.
        self.startup_frames = deque()
        self.startup_limit = rate * startup_seconds
        self.startup_pending = startup_seconds > 0

    async def receive(self, pcm, clock="channel"):
        frame = AudioFrame(
            pcm_s16le=pcm,
            sample_rate_hz=self.rate,
            sample_offset=self.received_samples,
            clock_id=clock,
            observed_monotonic_ns=time.monotonic_ns(),
        )
        self.received_samples += len(pcm) // 2
        self.last_received = time.monotonic()
        if audioop.rms(pcm, 2) >= 500:
            self.last_received_speech_at = self.last_received
        await self.recorder.write("received", frame)
        if self.startup_pending:
            if self.received_samples > self.startup_limit or len(self.startup_frames) >= 10000:
                self.fail("startup_queue_overflow")
                raise HarnessFailure("Startup audio buffer exceeded its limit")
            self.startup_frames.append(frame)
            return
        try:
            self.incoming.put_nowait(frame)
        except asyncio.QueueFull:
            self.fail("receive_queue_overflow")
            raise HarnessFailure("Receive queue overflow") from None

    def fail(self, reason):
        self.error = reason
        self.closed.set()

    async def received_audio(self):
        self.startup_pending = False
        while self.startup_frames:
            yield self.startup_frames.popleft()
        while not self.closed.is_set() or not self.incoming.empty():
            try:
                frame = await asyncio.wait_for(self.incoming.get(), 0.2)
            except TimeoutError:
                continue
            yield frame
        if self.error:
            if self.harness_error:
                raise HarnessFailure(self.error)
            raise TransportFailure(self.error)

    @property
    def harness_error(self):
        return bool(self.error) and (
            "queue_overflow" in self.error
            or self.error
            in {"evidence_write_failed", "event_delivery_failed", "capture_playback_failed"}
        )

    def check_health(self):
        if self.error:
            if self.harness_error:
                raise HarnessFailure(self.error)
            raise TransportFailure(self.error)
        if self.closed.is_set():
            raise TransportFailure("Transport closed during setup")

    async def send_audio(self, frame):
        if self.closed.is_set():
            self.check_health()
            raise TransportFailure("Transport is closed")
        if frame.sample_rate_hz not in self.converters:
            self.converters[frame.sample_rate_hz] = Resampler(frame.sample_rate_hz, self.rate)
            await self.evidence.emit(
                "channel",
                "sample_rate_conversion",
                {
                    "source_rate": frame.sample_rate_hz,
                    "target_rate": self.rate,
                    "method": "audioop.ratecv streaming linear interpolation",
                },
            )
        converter = self.converters[frame.sample_rate_hz]
        pcm = converter.convert(frame.pcm_s16le)
        if not pcm:
            return
        converted = frame.model_copy(
            update={
                "pcm_s16le": pcm,
                "sample_rate_hz": self.rate,
                "sample_offset": self.submitted_samples,
            }
        )
        self.submitted_samples += len(pcm) // 2
        try:
            self.outgoing.put_nowait(converted)
        except asyncio.QueueFull:
            self.fail("send_queue_overflow")
            raise HarnessFailure("Send queue overflow") from None

    async def record_sent(self, frame):
        await self.recorder.write("sent", frame)
        await self.evidence.emit(
            "channel",
            "audio_submitted",
            {
                "item_id": frame.item_id,
                "samples": len(frame.pcm_s16le) // 2,
                "rate": frame.sample_rate_hz,
                "boundary": "submission",
            },
        )

    async def acknowledged(self, item_id, milliseconds, boundary, clock_id):
        self.played[item_id] = self.played.get(item_id, 0) + milliseconds
        await self.evidence.emit(
            "channel",
            "playback_progress",
            {"item_id": item_id, "played_ms": self.played[item_id], "boundary": boundary},
            clock_id=clock_id,
        )

    async def flush_evidence(self):
        """Non-browser channels persist observations before returning."""

    async def cancel_playback(self):
        while not self.outgoing.empty():
            self.outgoing.get_nowait()
            self.outgoing.task_done()
        await self.evidence.emit("channel", "caller_playback_cancelled", {"played_ms": self.played})
        return dict(self.played)

    async def close(self, reason):
        self.closed.set()
        for task in self.tasks:
            task.cancel()
        await asyncio.gather(*self.tasks, return_exceptions=True)
        await self.recorder.close()

    async def events(self):
        # Concrete sessions write events directly to the shared evidence sequencer.
        if False:
            yield

    def background(self, coroutine):
        task = asyncio.create_task(coroutine)
        self.tasks.append(task)

        def finished(t):
            if not t.cancelled() and t.exception():
                self.fail(self.error or type(t.exception()).__name__)

        task.add_done_callback(finished)
        return task
