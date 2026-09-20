"""Plivo telephone transport with authenticated, one-attempt media sessions."""

import asyncio
import audioop
import base64
import secrets
import time
from uuid import uuid4
from xml.etree.ElementTree import Element, SubElement, tostring

import httpx

from voice_bench.channels.media import MediaSession


class PlivoClient:
    def __init__(self, account, token, transport=None):
        self.account, self.token = account, token
        self.client = httpx.AsyncClient(
            base_url=f"https://api.plivo.com/v1/Account/{account}/",
            auth=(account, token),
            timeout=20,
            transport=transport,
        )

    async def dial(self, source, target, base, run_id, maximum):
        response = await self.client.post(
            "Call/",
            json={
                "from": source,
                "to": target,
                "answer_url": f"{base}/callbacks/plivo/answer/{run_id}",
                "answer_method": "POST",
                "hangup_url": f"{base}/callbacks/plivo/status/{run_id}",
                "hangup_method": "POST",
                "time_limit": maximum,
            },
        )
        response.raise_for_status()
        return response.json()

    async def hangup(self, call_id):
        response = await self.client.delete(f"Call/{call_id}/")
        if response.status_code != 404:
            response.raise_for_status()

    async def call(self, call_id):
        response = await self.client.get(f"Call/{call_id}/")
        response.raise_for_status()
        return response.json()

    async def close(self):
        await self.client.aclose()


class PhoneSession(MediaSession):
    def __init__(self, evidence, store, run_id, account, media_timeout):
        super().__init__(evidence, 8000)
        self.store, self.run_id, self.account = store, run_id, account
        self.token = secrets.token_urlsafe(32)
        self.socket = None
        self.stream_id = None
        self.connected = asyncio.Event()
        self.clear_confirmed = asyncio.Event()
        self.pending = {}
        self.played_samples = {}
        self.sequence = 0
        self.media_timeout = media_timeout
        self.sender = None
        self.send_lock = asyncio.Lock()

    async def attach(self, socket):
        if self.socket is not None:
            raise ValueError("An attempt cannot reconnect its media stream")
        self.socket = socket
        try:
            while not self.closed.is_set():
                event = await asyncio.wait_for(socket.receive_json(), self.media_timeout)
                await self.handle(event)
        except Exception as exc:
            self.fail(type(exc).__name__)
        finally:
            self.closed.set()

    async def handle(self, event):
        sequence = int(event["sequenceNumber"])
        if sequence != self.sequence + 1:
            raise ValueError("Carrier stream sequence gap")
        self.sequence = sequence
        kind = event["event"]
        if kind == "start":
            start = event["start"]
            if self.stream_id or start["accountId"] != self.account:
                raise ValueError("Unexpected carrier session")
            if await asyncio.to_thread(self.store.resolve, "plivo", start["callId"]) != self.run_id:
                raise ValueError("Carrier call belongs to another attempt")
            if start["mediaFormat"] != {"encoding": "audio/x-mulaw", "sampleRate": 8000}:
                raise ValueError("Unexpected carrier codec")
            self.stream_id = start["streamId"]
            await self.evidence.emit(
                "channel",
                "codec_conversion",
                {
                    "wire": "audio/x-mulaw;rate=8000",
                    "internal": "pcm_s16le;rate=8000",
                    "method": "audioop.ulaw2lin/lin2ulaw",
                },
            )
            self.connected.set()
            self.sender = self.background(self._sender())
            self.background(self._watch_media())
        elif not self.stream_id or event.get("streamId") != self.stream_id:
            raise ValueError("Wrong stream ID")
        elif kind == "media":
            if event["media"]["track"] != "inbound":
                raise ValueError("Unexpected media track")
            pcm = audioop.ulaw2lin(base64.b64decode(event["media"]["payload"], validate=True), 2)
            await self.receive(pcm, "plivo-media")
            await self.evidence.emit(
                "channel",
                "carrier_media",
                {
                    "timestamp": event["media"]["timestamp"],
                    "chunk": event["media"]["chunk"],
                    "samples": len(pcm) // 2,
                },
                clock_id="plivo-media",
            )
        elif kind == "playedStream":
            checkpoint = self.pending.pop(event["name"], None)
            if checkpoint:
                item, samples, _ = checkpoint
                previous_ms = self.played_samples.get(item, 0) * 1000 // 8000
                self.played_samples[item] = self.played_samples.get(item, 0) + samples
                await self.acknowledged(
                    item,
                    self.played_samples[item] * 1000 // 8000 - previous_ms,
                    "carrier_checkpoint",
                    self.evidence.clock_id,
                )
        elif kind == "clearedAudio":
            self.pending.clear()
            self.clear_confirmed.set()
        elif kind == "dtmf":
            await self.evidence.emit("channel", "dtmf", event["dtmf"])

    async def _watch_media(self):
        while True:
            await asyncio.sleep(1)
            if time.monotonic() - self.last_received > self.media_timeout:
                raise RuntimeError("Carrier receive stream stalled")
            if (
                self.pending
                and time.monotonic() - min(p[2] for p in self.pending.values()) > self.media_timeout
            ):
                raise RuntimeError("Carrier playback unacknowledged")

    async def _sender(self):
        while True:
            frame = await self.outgoing.get()
            try:
                async with self.send_lock:
                    name = str(uuid4())
                    self.pending[name] = (
                        frame.item_id,
                        len(frame.pcm_s16le) // 2,
                        time.monotonic(),
                    )
                    await self.socket.send_json(
                        {
                            "event": "playAudio",
                            "media": {
                                "contentType": "audio/x-mulaw",
                                "sampleRate": 8000,
                                "payload": base64.b64encode(
                                    audioop.lin2ulaw(frame.pcm_s16le, 2)
                                ).decode(),
                            },
                        }
                    )
                    await self.socket.send_json(
                        {"event": "checkpoint", "streamId": self.stream_id, "name": name}
                    )
                    await self.record_sent(frame)
                await asyncio.sleep(len(frame.pcm_s16le) / 2 / 8000)
            finally:
                self.outgoing.task_done()

    async def cancel_playback(self):
        if self.sender:
            self.sender.cancel()
            await asyncio.gather(self.sender, return_exceptions=True)
        await super().cancel_playback()
        self.clear_confirmed.clear()
        async with self.send_lock:
            await self.socket.send_json({"event": "clearAudio", "streamId": self.stream_id})
        await asyncio.wait_for(self.clear_confirmed.wait(), 5)
        self.sender = self.background(self._sender())
        return dict(self.played)

    async def drain(self):
        await self.outgoing.join()
        while self.pending:
            if self.closed.is_set():
                raise RuntimeError("Playback completion is unconfirmed")
            await asyncio.sleep(0.02)

    async def close(self, reason):
        await super().close(reason)
        if self.socket:
            try:
                await self.socket.close()
            except RuntimeError:
                pass


class PhoneHub:
    def __init__(self, store, config, client, agent_id=None):
        self.store, self.config, self.client = store, config, client
        self.sessions = {}
        self.agent_id = agent_id or config.target.agent_ref

    def correlate(self, run_id, params):
        runtime = self.config.runtime
        try:
            bound = self.store.resolve("plivo", params["CallUUID"])
            if bound != run_id:
                raise ValueError("Carrier call belongs to another attempt")
        except KeyError:
            run = self.store.run(run_id)
            if (
                run_id not in self.sessions
                or not run.get("dispatch_intent")
                or run["phase"] not in {"connecting", "in_conversation", "finalizing"}
                or params.get("From") != runtime.caller_number
                or params.get("To") != runtime.target_number
            ):
                raise ValueError("Unexpected or stale phone route") from None
            self.store.bind("plivo", params["CallUUID"], run_id)

    def answer(self, run_id, params):
        session = self.sessions[run_id]
        self.correlate(run_id, params)
        runtime = self.config.runtime
        base = runtime.public_base_url.rstrip("/")
        ws = base.replace("https://", "wss://", 1)
        root = Element("Response")
        stream = SubElement(
            root,
            "Stream",
            {
                "bidirectional": "true",
                "keepCallAlive": "true",
                "audioTrack": "inbound",
                "contentType": "audio/x-mulaw;rate=8000",
                "statusCallbackUrl": f"{base}/callbacks/plivo/status/{run_id}",
            },
        )
        stream.text = f"{ws}/callbacks/plivo/media/{run_id}/{session.token}"
        return tostring(root, encoding="unicode")


class PhoneAdapter:
    def __init__(self, target, hub):
        self.target, self.hub, self.store = target, hub, hub.store

    async def connect(self, request, evidence):
        config = self.hub.config
        run_id = request.run.run_id
        await asyncio.to_thread(
            self.store.reserve_route, config.runtime.caller_number, self.hub.agent_id, run_id
        )
        session = PhoneSession(
            evidence,
            self.store,
            run_id,
            self.hub.client.account,
            config.runtime.media_timeout_seconds,
        )
        self.hub.sessions[run_id] = session
        reply = await self.hub.client.dial(
            config.runtime.caller_number,
            config.runtime.target_number,
            config.runtime.public_base_url.rstrip("/"),
            run_id,
            request.max_duration_seconds,
        )
        await asyncio.to_thread(self.store.bind, "plivo_request", reply["request_uuid"], run_id)
        ready = asyncio.create_task(session.connected.wait())
        stopped = asyncio.create_task(session.closed.wait())
        try:
            await asyncio.wait({ready, stopped}, return_when=asyncio.FIRST_COMPLETED)
            if not session.connected.is_set():
                raise RuntimeError("Telephone media did not connect")
        finally:
            ready.cancel()
            stopped.cancel()
            await asyncio.gather(ready, stopped, return_exceptions=True)
        return session

    async def reconcile(self, run_id, evidence):
        session = self.hub.sessions.pop(run_id, None)
        if session:
            await session.close("reconcile")
        bindings = await asyncio.to_thread(self.store.bindings, run_id)
        ids = {b["provider"]: b["call_id"] for b in bindings}
        if "plivo" not in ids:
            return False
        await self.hub.client.hangup(ids["plivo"])
        while True:
            record = await self.hub.client.call(ids["plivo"])
            if record.get("call_status") in {"completed", "busy", "failed", "no-answer", "cancel"}:
                break
            await asyncio.sleep(0.5)
        await evidence.json("provider/plivo-call.json", record)
        if "rumik" in ids:
            while True:
                record = await self.target.call(ids["rumik"])
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
            return record.get("status") in {"completed", "failed", "expired"}
        return True
