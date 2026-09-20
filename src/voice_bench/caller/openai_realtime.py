"""Audio-only customer perception. Provider clients are created only during converse."""

import asyncio
import base64
import json
import time

from voice_bench.channels.media import AudioRecorder, Resampler
from voice_bench.errors import CallerFailure, HarnessFailure, TransportFailure
from voice_bench.models import AudioFrame


class OpenAICaller:
    def __init__(self, config, key=None, connector=None):
        self.config, self.key, self.connector = config, key, connector

    async def converse(self, run, brief, session, evidence):
        try:
            return await self._converse(run, brief, session, evidence)
        except (HarnessFailure, TransportFailure):
            raise
        except Exception as exc:
            raise CallerFailure(type(exc).__name__) from exc

    async def _converse(self, run, brief, session, evidence):
        import websockets

        config = self.config
        connector = self.connector or websockets.connect
        url = f"wss://api.openai.com/v1/realtime?model={config.model}"
        instructions = (
            config.instructions + "\nYou are the CUSTOMER, not the business agent. "
            "Keep your assigned facts fixed. You can hear only the received audio. "
            "Use finish_customer only after your closing speech has finished.\n"
            + json.dumps(brief.model_dump(), ensure_ascii=False)
        )
        recorder = AudioRecorder(evidence)
        async with connector(
            url,
            additional_headers={"Authorization": f"Bearer {self.key}"},
            max_size=4 * 1024 * 1024,
        ) as socket:

            async def send(value):
                await socket.send(json.dumps(value))

            turn = dict(config.turn_detection)
            turn["create_response"] = config.interrupt_after_ms is None
            turn["interrupt_response"] = config.interrupt_after_ms is None
            await send(
                {
                    "type": "session.update",
                    "session": {
                        "type": "realtime",
                        "instructions": instructions,
                        "output_modalities": ["audio"],
                        "max_output_tokens": config.max_output_tokens,
                        "audio": {
                            "input": {
                                "format": {"type": "audio/pcm", "rate": 24000},
                                "turn_detection": turn,
                            },
                            "output": {
                                "format": {"type": "audio/pcm", "rate": 24000},
                                "voice": config.voice,
                            },
                        },
                        "tools": [
                            {
                                "type": "function",
                                "name": "finish_customer",
                                "description": "End the conversation after saying goodbye.",
                                "parameters": {
                                    "type": "object",
                                    "properties": {},
                                    "additionalProperties": False,
                                },
                            }
                        ],
                    },
                }
            )
            ready = asyncio.Event()
            converter = Resampler(session.rate, 24000)
            last_item = None
            generated_items = {}
            interrupted = set()
            response_idle = asyncio.Event()
            response_idle.set()
            generated_samples = 0
            interruption = None
            finished = asyncio.Event()

            async def audio_input():
                await asyncio.wait_for(ready.wait(), 15)
                await evidence.emit(
                    "caller",
                    "sample_rate_conversion",
                    {
                        "source_rate": session.rate,
                        "target_rate": 24000,
                        "method": "audioop.ratecv streaming linear interpolation",
                    },
                )
                async for frame in session.received_audio():
                    pcm = converter.convert(frame.pcm_s16le)
                    await send(
                        {
                            "type": "input_audio_buffer.append",
                            "audio": base64.b64encode(pcm).decode(),
                        }
                    )

            async def trigger_interruption():
                await asyncio.sleep(config.interrupt_after_ms / 1000)
                if not response_idle.is_set():
                    await send({"type": "response.cancel"})
                    await asyncio.wait_for(response_idle.wait(), 5)
                await evidence.emit("caller", "controlled_interruption")
                await send(
                    {
                        "type": "response.create",
                        "response": {
                            "instructions": "Interrupt now. Keep the assigned customer facts."
                        },
                    }
                )

            async def model_events():
                nonlocal last_item, generated_samples, interruption
                async for raw in socket:
                    event = json.loads(raw)
                    kind = event["type"]
                    if kind == "error":
                        await evidence.emit(
                            "caller", "provider_error", {"code": event.get("error", {}).get("code")}
                        )
                        raise RuntimeError("OpenAI Realtime error")
                    if kind == "session.updated":
                        await evidence.json("config/caller-effective.json", event["session"])
                        ready.set()
                    elif kind == "response.output_audio.delta":
                        last_item = event["item_id"]
                        pcm = base64.b64decode(event["delta"], validate=True)
                        frame = AudioFrame(
                            pcm_s16le=pcm,
                            sample_rate_hz=24000,
                            sample_offset=generated_samples,
                            item_id=last_item,
                            clock_id="openai-output-observed",
                            observed_monotonic_ns=time.monotonic_ns(),
                        )
                        generated_samples += len(pcm) // 2
                        if last_item not in generated_items:
                            await evidence.emit(
                                "caller", "first_audio_generated", {"item_id": last_item}
                            )
                        generated_items[last_item] = (
                            generated_items.get(last_item, 0) + len(pcm) // 2
                        )
                        await recorder.write("generated", frame)
                        if last_item not in interrupted:
                            await session.send_audio(frame)
                        else:
                            await evidence.emit(
                                "caller",
                                "audio_discarded_after_interruption",
                                {"item_id": last_item, "samples": len(pcm) // 2},
                            )
                    elif kind == "input_audio_buffer.speech_started":
                        await evidence.emit(
                            "caller",
                            "target_speech_detected",
                            {"audio_start_ms": event.get("audio_start_ms")},
                        )
                        if config.interrupt_after_ms is not None:
                            if interruption is None or interruption.done():
                                interruption = asyncio.create_task(trigger_interruption())
                        elif generated_items:
                            # Server VAD already cancels generation when interrupt_response=true.
                            played = await session.cancel_playback()
                            for item, samples in generated_items.items():
                                if (
                                    item not in interrupted
                                    and played.get(item, 0) < samples * 1000 // 24000
                                ):
                                    await send(
                                        {
                                            "type": "conversation.item.truncate",
                                            "item_id": item,
                                            "content_index": 0,
                                            "audio_end_ms": played.get(item, 0),
                                        }
                                    )
                                    interrupted.add(item)
                            if last_item and not response_idle.is_set():
                                interrupted.add(last_item)
                    elif kind == "input_audio_buffer.speech_stopped":
                        if interruption and not interruption.done():
                            interruption.cancel()
                            await asyncio.gather(interruption, return_exceptions=True)
                            if response_idle.is_set():
                                await send({"type": "response.create"})
                        await evidence.emit("caller", "target_speech_stopped")
                    elif kind == "response.function_call_arguments.done":
                        if event.get("name") == "finish_customer":
                            # Wait for the audio path to drain, bounded by the controller timeout.
                            await session.drain()
                            finished.set()
                            return
                    elif kind == "response.done":
                        response_idle.set()
                        await evidence.emit(
                            "caller",
                            "response_done",
                            {
                                "status": event["response"].get("status"),
                                "usage": event["response"].get("usage"),
                            },
                        )
                        if event["response"].get("status") == "failed":
                            raise CallerFailure("Realtime response failed")
                    elif kind == "response.created":
                        response_idle.clear()
                    elif kind.endswith("transcript.done"):
                        await evidence.emit(
                            "caller",
                            "transcript_observation",
                            {"text": event.get("transcript"), "source": kind},
                        )
                if not finished.is_set() and not session.closed.is_set():
                    raise RuntimeError("OpenAI stream ended before conversation completion")

            tasks = [
                asyncio.create_task(audio_input()),
                asyncio.create_task(model_events()),
                asyncio.create_task(session.closed.wait()),
                asyncio.create_task(finished.wait()),
            ]
            try:
                done, _ = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                for task in done:
                    task.result()
                if session.error:
                    raise TransportFailure(session.error)
                if not finished.is_set():
                    raise TransportFailure("Audio disconnected before customer completion")
            finally:
                if interruption:
                    interruption.cancel()
                    await asyncio.gather(interruption, return_exceptions=True)
                for task in tasks:
                    task.cancel()
                await asyncio.gather(*tasks, return_exceptions=True)
                await recorder.close()
