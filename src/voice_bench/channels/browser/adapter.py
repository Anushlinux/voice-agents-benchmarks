"""Real Chromium/LiveKit adapter; the local page holds only ephemeral room access."""

import asyncio
import base64
import struct
import time
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from voice_bench.channels.media import MediaSession
from voice_bench.models import AudioFrame

STATIC = Path(__file__).parent / "static"


class BrowserSession(MediaSession):
    def __init__(self, evidence, *, startup_seconds=0):
        super().__init__(evidence, 48000, startup_seconds=startup_seconds)
        self.browser = self.playwright = self.page = None
        self.rendered = {}
        self.rendered_samples = 0
        self.http_server = self.http_thread = None

    async def event(self, source, event):
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
            await self.evidence.emit(
                "channel",
                event_kind,
                {
                    "sample": event["sample"],
                    "samples": len(event["samples"]),
                    "rate": event["rate"],
                    "recording_offset": offset,
                    "bridge_delay_ms": event.get("bridge_delay_ms"),
                },
                clock_id="chromium-audio-context",
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
        elif kind == "disconnected":
            self.closed.set()
        elif kind == "bridge_error":
            self.fail(event["reason"])
            await self.evidence.emit("channel", "bridge_error", {"reason": event["reason"]})

    async def start(self, call, *, test=False):
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
            ],
        )
        self.page = await self.browser.new_page()
        await self.page.expose_binding("benchEvent", self.event)

        await self.page.goto(f"http://127.0.0.1:{self.http_server.server_port}/")
        await self.page.wait_for_function("!!window.bridge")
        if test:
            await self.page.evaluate("bridge.testStart()")
        else:
            await self.page.evaluate("call => bridge.join(call)", call)
        self.background(self._sender())

    async def _sender(self):
        next_time = time.monotonic()
        while True:
            frame = await self.outgoing.get()
            try:
                await asyncio.sleep(max(0, next_time - time.monotonic()))
                await self.page.evaluate(
                    "([pcm,item]) => bridge.push(pcm,item)",
                    [base64.b64encode(frame.pcm_s16le).decode(), frame.item_id],
                )
                next_time = max(next_time, time.monotonic()) + len(frame.pcm_s16le) / 2 / self.rate
                await self.record_sent(frame)
            finally:
                self.outgoing.task_done()

    async def cancel_playback(self):
        # Stop a sender that may already hold a frame before clearing the remote queue.
        for task in self.tasks:
            task.cancel()
        await asyncio.gather(*self.tasks, return_exceptions=True)
        self.tasks.clear()
        await super().cancel_playback()
        self.played = await self.page.evaluate("bridge.clear()")
        if not self.closed.is_set():
            self.background(self._sender())
        return dict(self.played)

    async def drain(self):
        await self.outgoing.join()
        await self.page.evaluate("bridge.drain()")

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
            await super().close(reason)


class BrowserAdapter:
    def __init__(self, target, store):
        self.target, self.store = target, store
        self.session = None

    async def connect(self, request, evidence):
        await evidence.emit("target", "registration_requested")
        registration = await self.target.register(request.agent_ref)
        call_id = registration["call_id"]
        await evidence.emit("target", "registered", {"call_id": call_id})
        await asyncio.to_thread(self.store.bind, "rumik", call_id, request.run.run_id)
        await evidence.emit("target", "browser_start_requested", {"call_id": call_id})
        call = await self.target.start_browser(registration["access_token"])
        if call["callId"] != call_id:
            raise ValueError("Rumik returned a different call ID")
        self.session = BrowserSession(evidence, startup_seconds=request.setup_timeout_seconds)
        await self.session.start(call)
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
            return False
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
