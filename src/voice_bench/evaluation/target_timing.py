"""Time to first token for each hosted Rumik generation, from the packets Rumik publishes.

Rumik's pipeline broadcasts `rtvi-ai` lifecycle packets into the call room. The browser
records each one with its own receipt clock (`performance_ms`) and audio clock
(`audio_context_seconds`). Both ends of every interval below come from the same browser
clock, so the subtraction is valid; the values include network transit and are therefore
upper bounds on the hosted model's own latency. Provider-reported LLM first-byte times
from `metrics` packets are retained separately as Rumik's own measurement.
"""

import json
import math
from collections import Counter

from voice_bench.evaluation.cohort_metrics import distribution

VERSION = "target-timing-v1"


def _packets(events):
    for event in events:
        if event.get("kind") != "target_text_observation":
            continue
        payload = event.get("payload", {})
        if payload.get("kind") != "data_packet" or not payload.get("remote_audio_participant"):
            continue
        try:
            packet = json.loads(payload.get("text", ""))
        except (ValueError, TypeError):
            continue
        if not isinstance(packet, dict) or packet.get("label") != "rtvi-ai":
            continue
        yield event, payload, packet


def _stamp(event, payload):
    return {
        "sequence": event.get("sequence"),
        "performance_ms": payload.get("performance_ms"),
        "audio_context_seconds": payload.get("audio_context_seconds"),
    }


def _delta_ms(later, earlier):
    if later is None or earlier is None:
        return None
    if later["performance_ms"] is None or earlier["performance_ms"] is None:
        return None
    value = later["performance_ms"] - earlier["performance_ms"]
    return value if value >= 0 else None


def generation_windows(events):
    """One row per `bot-llm-started` … `bot-llm-stopped`/`bot-interrupted` window."""
    rows = []
    current = None
    last_user_stopped = None
    for event, payload, packet in _packets(events):
        kind = packet.get("type")
        stamp = _stamp(event, payload)
        if kind == "user-stopped-speaking":
            last_user_stopped = stamp
        elif kind == "bot-llm-started":
            if current is not None:
                current["ended"] = current.get("ended") or "superseded"
                rows.append(current)
            current = {
                "trigger_user_stopped": last_user_stopped,
                "started": stamp,
                "first_text": None,
                "first_tts_started": None,
                "first_bot_speaking": None,
                "function_call": False,
                "ended": None,
                "ended_at": None,
                "usage": None,
                "provider_llm_ttfb_ms": None,
                "provider_tts_ttfb_ms": None,
                "provider_tts_ttfa_ms": None,
            }
        elif current is None:
            continue
        elif kind == "bot-llm-text":
            text = (packet.get("data") or {}).get("text", "")
            if isinstance(text, str) and text.strip() and current["first_text"] is None:
                current["first_text"] = stamp
        elif kind == "llm-function-call-started":
            current["function_call"] = True
        elif kind == "bot-tts-started" and current["first_tts_started"] is None:
            current["first_tts_started"] = stamp
        elif kind == "bot-started-speaking" and current["first_bot_speaking"] is None:
            current["first_bot_speaking"] = stamp
        elif kind == "bot-interrupted":
            if current["ended"] is None:
                current["ended"], current["ended_at"] = "interrupted", stamp
        elif kind == "bot-llm-stopped":
            if current["ended"] is None:
                current["ended"], current["ended_at"] = "stopped", stamp
        elif kind == "metrics" and isinstance(packet.get("data"), dict):
            data = packet["data"]
            for usage in data.get("tokens") or []:
                if isinstance(usage, dict) and current["usage"] is None:
                    current["usage"] = {
                        k: usage.get(k)
                        for k in ("completion_tokens", "reasoning_tokens", "prompt_tokens")
                    }
            for metric in ("ttfb", "ttfa"):
                for entry in data.get(metric) or []:
                    if not isinstance(entry, dict):
                        continue
                    value = entry.get("value" if metric == "ttfb" else metric)
                    if isinstance(value, bool) or not isinstance(value, int | float):
                        continue
                    if not math.isfinite(value) or value < 0:
                        continue
                    processor = str(entry.get("processor", ""))
                    if "LLMService" in processor and metric == "ttfb":
                        current["provider_llm_ttfb_ms"] = value * 1000
                    elif "TTSService" in processor:
                        current[f"provider_tts_{metric}_ms"] = value * 1000
    if current is not None:
        current["ended"] = current.get("ended") or "unterminated"
        rows.append(current)
    previous = None
    for row in rows:
        trigger, started, first = row["trigger_user_stopped"], row["started"], row["first_text"]
        # A generation that follows a tool call without new caller speech is chained: its
        # first token is measured from the same caller pause, so tool time is included.
        row["chained_after_tool_call"] = bool(
            previous
            and previous.get("function_call")
            and previous.get("trigger_user_stopped") == trigger
        )
        previous = row
        row["ttft_ms"] = _delta_ms(first, trigger)
        row["llm_started_to_first_text_ms"] = _delta_ms(first, started)
        row["user_stopped_to_llm_started_ms"] = _delta_ms(started, trigger)
        row["user_stopped_to_bot_speaking_ms"] = _delta_ms(row["first_bot_speaking"], trigger)
        row["first_text_to_bot_speaking_ms"] = _delta_ms(row["first_bot_speaking"], first)
        row["produced_text"] = first is not None
        row["classification"] = (
            "interrupted_before_text"
            if row["ended"] == "interrupted" and first is None
            else "completed_without_text"
            if row["ended"] == "stopped" and first is None and not row["function_call"]
            else "tool_call_without_text"
            if first is None and row["function_call"]
            else "text_then_interrupted"
            if row["ended"] == "interrupted"
            else "text"
        )
    return rows


def measure(events):
    rows = generation_windows(events)
    with_text = [r for r in rows if r["produced_text"]]
    ttft = [r["ttft_ms"] for r in with_text if r["ttft_ms"] is not None]
    return {
        "version": VERSION,
        "status": "measured" if rows else "unavailable",
        "clock": "browser-performance (packet receipt); audio_context_seconds retained",
        "definitions": {
            "ttft_ms": "Rumik's own end-of-caller-speech packet (user-stopped-speaking) to the "
            "first non-empty bot-llm-text packet, both as received by the browser. This is "
            "the caller-perceived time to first token, an upper bound on hosted LLM latency "
            "because it includes Rumik's endpoint decision, network transit and observer "
            "scheduling. Only generations that produced text are counted; interrupted and "
            "silent generations are retained separately.",
            "llm_started_to_first_text_ms": "bot-llm-started to first bot-llm-text on the same "
            "clock; excludes endpointing, includes transit.",
            "provider_llm_ttfb_ms": "Rumik's own reported LLM time to first byte for that "
            "generation, when a metrics packet followed it.",
            "user_stopped_to_bot_speaking_ms": "Rumik's end-of-speech decision to its own "
            "bot-started-speaking packet; comparable to but distinct from audio-clock TTFS.",
        },
        "counts": dict(Counter(r["classification"] for r in rows)),
        "generations": len(rows),
        "ttft_ms": distribution(ttft),
        "llm_started_to_first_text_ms": distribution(
            [
                r["llm_started_to_first_text_ms"]
                for r in with_text
                if r["llm_started_to_first_text_ms"] is not None
            ]
        ),
        "provider_llm_ttfb_ms": distribution(
            [r["provider_llm_ttfb_ms"] for r in rows if r["provider_llm_ttfb_ms"] is not None]
        ),
        "provider_tts_ttfb_ms": distribution(
            [r["provider_tts_ttfb_ms"] for r in rows if r["provider_tts_ttfb_ms"] is not None]
        ),
        "user_stopped_to_bot_speaking_ms": distribution(
            [
                r["user_stopped_to_bot_speaking_ms"]
                for r in rows
                if r["user_stopped_to_bot_speaking_ms"] is not None
            ]
        ),
        "completion_tokens": [r["usage"]["completion_tokens"] for r in rows if r["usage"]],
        "rows": rows,
        "limitations": "Packets are observed at the browser, not inside Rumik; a capped capture "
        "omits later generations. Fragmented caller speech yields many short windows that "
        "are interrupted before text and are not first-token latencies.",
    }


def measure_directory(directory):
    events = [json.loads(line) for line in (directory / "events.jsonl").open()]
    return measure(events)
