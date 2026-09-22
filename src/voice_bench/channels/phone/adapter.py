"""Plivo telephone transport with authenticated, one-attempt media sessions."""

import asyncio
import audioop
import base64
import secrets
import time
from uuid import uuid4
from xml.etree.ElementTree import Element, SubElement, tostring

import httpx
from starlette.websockets import WebSocketDisconnect

from voice_bench.channels.media import MediaSession
from voice_bench.numbers import same_endpoint


class PlivoClient:
    def __init__(self, account, token, transport=None, *, sip_username=None, sip_password=None):
        if bool(sip_username) != bool(sip_password):
            raise ValueError("SIP username and password must be supplied together")
        self.account, self.token = account, token
        self.sip_username, self.sip_password = sip_username, sip_password
        self.client = httpx.AsyncClient(
            base_url=f"https://api.plivo.com/v1/Account/{account}/",
            auth=(account, token),
            timeout=20,
            transport=transport,
        )

    async def dial(self, source, target, base, run_id, maximum):
        credentials = {}
        if self.sip_username:
            if not target.startswith(("sip:", "sips:")):
                raise ValueError("SIP credentials require an explicit SIP destination")
            credentials = {
                "sip_auth_username": self.sip_username,
                "sip_auth_password": self.sip_password,
            }
        response = await self.client.post(
            "Call/",
            json={
                # Plivo documents E.164 caller IDs without the plus sign.
                "from": source.lstrip("+"),
                "to": target,
                "answer_url": f"{base}/callbacks/plivo/answer/{run_id}",
                "answer_method": "POST",
                "hangup_url": f"{base}/callbacks/plivo/status/{run_id}",
                "hangup_method": "POST",
                "time_limit": maximum,
                **credentials,
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
        if response.status_code == 404:
            # The call record is published after the leg ends; keep polling until then.
            return {"call_status": "record_pending"}
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
        self.media_chunk = None
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
            reason = type(exc).__name__
            self.fail(reason)
            try:
                await self.evidence.emit(
                    "channel",
                    "carrier_stream_failed",
                    {"reason": reason, "detail": str(exc)[:200], "events_seen": self.sequence},
                )
            except Exception:
                pass
        finally:
            self.closed.set()

    async def handle(self, event):
        sequence = int(event["sequenceNumber"])
        kind = event["event"]
        if sequence < 0:
            raise ValueError("Invalid carrier event sequence")
        if self.stream_id is None:
            await self.evidence.emit(
                "channel",
                "carrier_initial_event",
                {"event": kind, "sequence": sequence, "keys": sorted(event)},
            )
        zero_start = kind == "start" and self.stream_id is None and sequence == self.sequence == 0
        if sequence != self.sequence + 1 and not zero_start:
            await self.evidence.emit(
                "channel",
                "carrier_sequence_anomaly",
                {
                    "event": kind,
                    "received": sequence,
                    "previous": self.sequence,
                    "chunk": event.get("media", {}).get("chunk"),
                },
            )
        # Playback acknowledgments can reuse the preceding event number on
        # live Plivo streams. Audio continuity is checked by media.chunk below;
        # the shared event counter is diagnostic, not proof of lost audio.
        self.sequence = max(self.sequence, sequence)
        if kind in {"playedStream", "clearedAudio"}:
            await self.evidence.emit(
                "channel", "carrier_control", {"event": kind, "sequence": sequence}
            )
        if kind == "start":
            start = event["start"]
            # Retain the carrier's own description of the stream before any check can fail.
            await self.evidence.emit(
                "channel",
                "carrier_stream_start",
                {
                    key: start.get(key)
                    for key in ("callId", "streamId", "accountId", "tracks", "mediaFormat")
                },
            )
            # accountId is Plivo's numeric internal ID on live streams, not the
            # REST auth ID. The upgrade is authenticated with this account's
            # token; the persisted call binding below establishes run ownership.
            if self.stream_id or not start.get("accountId"):
                raise ValueError("Unexpected carrier session")
            if await asyncio.to_thread(self.store.resolve, "plivo", start["callId"]) != self.run_id:
                raise ValueError("Carrier call belongs to another attempt")
            media_format = start["mediaFormat"]
            if (
                media_format.get("encoding") != "audio/x-mulaw"
                or int(media_format.get("sampleRate") or 0) != 8000
            ):
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
            chunk = int(event["media"]["chunk"])
            if chunk < 0 or (self.media_chunk is not None and chunk != self.media_chunk + 1):
                raise ValueError("Carrier audio chunk sequence gap")
            self.media_chunk = chunk
            pcm = audioop.ulaw2lin(base64.b64decode(event["media"]["payload"], validate=True), 2)
            await self.receive(pcm, "plivo-media")
            await self.evidence.emit(
                "channel",
                "carrier_media",
                {
                    "timestamp": event["media"]["timestamp"],
                    "sequence": sequence,
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
            except (RuntimeError, WebSocketDisconnect):
                pass


def carrier_leg_ended(record):
    """A Plivo call detail record exists only after the leg ends; live legs report no end."""
    if record.get("call_status") in {
        "completed",
        "busy",
        "failed",
        "no-answer",
        "cancel",
        "timeout",
    }:
        return True
    return bool(record.get("end_time") or record.get("hangup_cause_name"))


class PhoneHub:
    def __init__(self, store, config, client, agent_id=None):
        self.store, self.config, self.client = store, config, client
        self.sessions = {}
        self.agent_id = agent_id or config.target.agent_ref
        self.agent_aliases = set()

    def canonical_agent(self, value):
        """Map the target's handle to its canonical ID; unknown values stay unchanged."""
        return self.agent_id if value in self.agent_aliases else value

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
                or not same_endpoint(params.get("From"), runtime.caller_number)
                or not (
                    same_endpoint(params.get("To"), runtime.target_number)
                    or same_endpoint(params.get("To"), runtime.target_sip_uri)
                )
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
        try:
            reply = await self.hub.client.dial(
                config.runtime.caller_number,
                config.runtime.target_sip_uri or config.runtime.target_number,
                config.runtime.public_base_url.rstrip("/"),
                run_id,
                request.max_duration_seconds,
            )
        except httpx.HTTPStatusError as exc:
            # Carrier rejection bodies explain the refusal and contain no credentials.
            await evidence.emit(
                "channel",
                "carrier_dial_rejected",
                {"status": exc.response.status_code, "detail": exc.response.text[:300]},
            )
            raise
        await evidence.emit(
            "channel", "carrier_dial_accepted", {"request_uuid": reply.get("request_uuid")}
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
            if carrier_leg_ended(record):
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
