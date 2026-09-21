"""Real Chromium/LiveKit adapter; the local page holds only ephemeral room access."""

import asyncio
import base64
import os
import struct
import time
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from voice_bench.channels.browser.journal import BrowserJournal, BufferedEvidence, BufferedRecorder
from voice_bench.channels.media import MediaSession
from voice_bench.errors import HarnessFailure
from voice_bench.models import AudioFrame

STATIC = Path(__file__).parent / "static"


class BrowserSession(MediaSession):
    def __init__(self, evidence, *, startup_seconds=0):
        super().__init__(evidence, 48000, startup_seconds=startup_seconds)
        self.journal = BrowserJournal(evidence, self.fail)
        self.evidence = BufferedEvidence(self.journal)
        self.recorder = BufferedRecorder(self.recorder, self.journal)
        self.browser = self.playwright = self.page = None
        self.rendered = {}
        self.rendered_samples = 0
        self.http_server = self.http_thread = None
        self.playback_generation = 0
        self.native_sequences = {}

    def _append_native(self, capture_id, data):
        self.evidence._open()
        path = self.evidence.directory / "audio" / f"received-native-{capture_id}.webm"
        path.parent.mkdir(exist_ok=True)
        with path.open("ab") as output:
            output.write(data)
            output.flush()

    async def event(self, source, event):
        if event["type"] != "batch":
            return await self._event(event)
        observations = []
        for item in event["events"]:
            if item["type"] not in {"received", "rendered_audio"}:
                # Keep disconnect and cancellation boundaries after preceding audio.
                if observations:
                    await self.evidence.emit_many(observations)
                    observations.clear()
                await self._event(item)
            else:
                await self._event(item, observations)
        if observations:
            await self.evidence.emit_many(observations)

    async def _event(self, event, batch=None):
        kind = event["type"]
        if kind in {"received", "rendered_audio"}:
            pcm = struct.pack(
                "<" + "h" * len(event["samples"]),
                *[max(-32768, min(32767, round(x * 32768))) for x in event["samples"]],
            )
            offset = self.received_samples if kind == "received" else self.rendered_samples
            if kind == "received":
                await self.receive(pcm, "chromium-audio-context")
            else:
                await self.recorder.write(
                    "played",
                    AudioFrame(
                        pcm_s16le=pcm,
                        sample_rate_hz=self.rate,
                        sample_offset=offset,
                        clock_id="chromium-audio-context",
                        observed_monotonic_ns=time.monotonic_ns(),
                    ),
                )
                self.rendered_samples += len(pcm) // 2
            event_kind = "received_block" if kind == "received" else "rendered_block"
            observations = [
                {
                    "source": "channel",
                    "kind": event_kind,
                    "payload": {
                        "sample": event["sample"],
                        "samples": len(event["samples"]),
                        "rate": event["rate"],
                        "recording_offset": offset,
                        "bridge_delay_ms": event.get("bridge_delay_ms"),
                    },
                    "clock_id": "chromium-audio-context",
                }
            ]
            for progress in event.get("progress", []):
                item = progress["item"]
                self.rendered[item] = self.rendered.get(item, 0) + progress["samples"]
                self.played[item] = self.rendered[item] * 1000 // progress["rate"]
                observations.append(
                    {
                        "source": "channel",
                        "kind": "playback_progress",
                        "clock_id": "chromium-audio-context",
                        "payload": {
                            "item_id": item,
                            "played_ms": self.played[item],
                            "sample": progress["sample"],
                            "samples": progress["samples"],
                            "rate": progress["rate"],
                            "boundary": "browser_render",
                        },
                    }
                )
            if batch is None:
                await self.evidence.emit_many(observations)
            else:
                batch.extend(observations)
        elif kind == "native_audio":
            capture_id = event["capture_id"]
            if not isinstance(capture_id, int) or not 0 <= capture_id < 16:
                raise ValueError("Invalid native capture identity")
            expected = self.native_sequences.get(capture_id, 0)
            if event["sequence"] != expected:
                raise ValueError("Native audio chunks are out of sequence")
            data = base64.b64decode(event["data"], validate=True)
            if len(data) != event["bytes"] or len(data) > 2 * 1024 * 1024:
                raise ValueError("Invalid native audio chunk")
            self.journal.submit(write=lambda: self._append_native(capture_id, data))
            self.native_sequences[capture_id] = expected + 1
            await self.evidence.emit(
                "channel",
                "native_capture_chunk",
                {
                    "capture_id": capture_id,
                    "chunk_sequence": expected,
                    "bytes": len(data),
                    "boundary": "received_media_stream_before_web_audio",
                },
            )
        elif kind == "played":
            item = event["item"]
            self.rendered[item] = self.rendered.get(item, 0) + event["samples"]
            self.played[item] = self.rendered[item] * 1000 // event["rate"]
            await self.evidence.emit(
                "channel",
                "playback_progress",
                {
                    "item_id": item,
                    "played_ms": self.played[item],
                    "sample": event["sample"],
                    "samples": event["samples"],
                    "rate": event["rate"],
                    "boundary": "browser_render",
                },
                clock_id="chromium-audio-context",
            )
        elif kind == "target_left":
            await self.evidence.emit("channel", "remote_audio_participant_left")
            self.closed.set()
        elif kind == "disconnected":
            await self.evidence.emit("channel", "room_disconnected")
            self.closed.set()
        elif kind == "bridge_error":
            self.fail(event["reason"])
            await self.evidence.emit("channel", "bridge_error", {"reason": event["reason"]})
        elif kind == "target_text_observation":
            await self.evidence.emit(
                "channel", "target_text_observation", event, clock_id="chromium-audio-context"
            )
        elif kind == "transport_observation":
            # Browser timestamps remain payload observations, not worker timestamps.
            await self.evidence.emit(
                "channel",
                "transport_observation",
                event
                | {
                    "performance_clock": "browser-performance",
                    "audio_clock": "chromium-audio-context",
                },
            )

    async def prepare(self, *, test=False):
        """Validate local audio before registering or starting a hosted call."""
        from playwright.async_api import async_playwright

        if not (STATIC / "bridge.js").is_file():
            raise RuntimeError("Build the browser bridge with npm ci and npm run build in browser/")

        class Handler(SimpleHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_GET(self):
                if self.path == "/":
                    body = b'<script type="module" src="/bridge.js"></script>'
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html")
                    self.send_header("Content-Length", str(len(body)))
                    self.end_headers()
                    self.wfile.write(body)
                elif self.path in {"/bridge.js", "/audio-worklet.js"}:
                    super().do_GET()
                else:
                    self.send_error(404)

        self.http_server = ThreadingHTTPServer(
            ("127.0.0.1", 0), partial(Handler, directory=str(STATIC))
        )
        self.http_thread = Thread(target=self.http_server.serve_forever, daemon=True)
        self.http_thread.start()
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=True,
            args=[
                "--autoplay-policy=no-user-gesture-required",
                "--disable-background-timer-throttling",
            ]
            + (["--allow-loopback-in-peer-connection"] if test else []),
        )
        self.page = await self.browser.new_page()
        await self.page.expose_binding("benchEvent", self.event)

        await self.page.goto(f"http://127.0.0.1:{self.http_server.server_port}/")
        await self.page.wait_for_function("!!window.bridge")
        await self.page.evaluate("bridge.prepare()")

    async def join(self, call):
        await self.page.evaluate("call => bridge.join(call)", call)
        self.background(self._sender())

    async def start(self, call, *, test=False):
        await self.prepare(test=test)
        if test:
            self.background(self._sender())
        else:
            await self.join(call)

    async def _sender(self):
        generation = self.playback_generation
        while True:
            frame = await self.outgoing.get()
            try:
                encoded = base64.b64encode(frame.pcm_s16le).decode()
                while True:
                    status = await self.page.evaluate(
                        "([pcm,item,generation]) => bridge.push(pcm,item,generation)",
                        [encoded, frame.item_id, generation],
                    )
                    if status == "cancelled":
                        return
                    if status == "queued":
                        await self.record_sent(frame)
                        break
                    if status != "full":
                        raise RuntimeError("Unexpected browser playback acknowledgement")
                    await asyncio.sleep(0.02)
            finally:
                self.outgoing.task_done()

    async def cancel_playback(self):
        # Stop a sender that may already hold a frame before clearing the remote queue.
        for task in self.tasks:
            task.cancel()
        await asyncio.gather(*self.tasks, return_exceptions=True)
        self.tasks.clear()
        await super().cancel_playback()
        self.playback_generation += 1
        self.played = await self.page.evaluate("bridge.clear()")
        if not self.closed.is_set():
            self.background(self._sender())
        return dict(self.played)

    async def drain(self):
        await self.outgoing.join()
        await self.page.evaluate("bridge.drain()")
        await self.flush_evidence()

    async def flush_evidence(self):
        await self.journal.flush()

    async def close(self, reason):
        self.closed.set()
        for task in self.tasks:
            task.cancel()
        await asyncio.gather(*self.tasks, return_exceptions=True)
        try:
            if self.page and not self.page.is_closed():
                await self.page.evaluate("window.bridge?.close()")
        finally:
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
            self.browser = self.playwright = self.page = None
            if self.http_server:
                await asyncio.to_thread(self.http_server.shutdown)
                self.http_server.server_close()
                await asyncio.to_thread(self.http_thread.join)
                self.http_server = self.http_thread = None
            try:
                await super().close(reason)
            finally:
                for capture_id in self.native_sequences:
                    path = self.evidence.directory / "audio" / f"received-native-{capture_id}.webm"
                    if path.exists():
                        with path.open("rb") as audio:
                            await asyncio.to_thread(os.fsync, audio.fileno())


class BrowserAdapter:
    def __init__(self, target, store):
        self.target, self.store = target, store
        self.session = None
        self.registration_requested = False
        self.preflight_started = False

    async def connect(self, request, evidence):
        self.registration_requested = False
        self.preflight_started = True
        self.session = BrowserSession(evidence, startup_seconds=request.setup_timeout_seconds)
        try:
            await self.session.prepare()
        except Exception as exc:
            # This boundary is entirely local and precedes all provider actions.
            # Do not expose arbitrary browser errors or misattribute them to Rumik.
            raise HarnessFailure("Local browser audio preparation failed") from exc
        await evidence.emit("target", "registration_requested")
        self.registration_requested = True
        registration = await self.target.register(request.agent_ref)
        call_id = registration["call_id"]
        await evidence.emit("target", "registered", {"call_id": call_id})
        await asyncio.to_thread(self.store.bind, "rumik", call_id, request.run.run_id)
        await evidence.emit("target", "browser_start_requested", {"call_id": call_id})
        call = await self.target.start_browser(registration["access_token"])
        if call["callId"] != call_id:
            raise ValueError("Rumik returned a different call ID")
        await self.session.join(call)
        return self.session

    async def reconcile(self, run_id, evidence):
        if self.session:
            try:
                async with asyncio.timeout(5):
                    await self.session.close("reconcile")
            except Exception as exc:
                await evidence.emit("channel", "cleanup_failed", {"type": type(exc).__name__})
            finally:
                self.session = None
        bindings = await asyncio.to_thread(self.store.bindings, run_id)
        calls = [b["call_id"] for b in bindings if b["provider"] == "rumik"]
        if not calls:
            # This live instance can prove preparation failed before any request.
            # A timed-out registration is still uncertain and must not be cleared.
            return self.preflight_started and not self.registration_requested
        while True:
            record = await self.target.call(calls[0])
            if record.get("status") in {"completed", "failed", "expired"}:
                break
            await asyncio.sleep(0.5)
        url = record.pop("recordingUrl", None)
        await evidence.json("provider/rumik-call.json", record)
        if url:
            try:
                await evidence.store_artifact(
                    run_id, "provider/recording", await self.target.recording(url)
                )
            except Exception:
                await evidence.emit("target", "recording_unavailable")
        return True
