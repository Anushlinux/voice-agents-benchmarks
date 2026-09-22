"""Telephone observations; never relabel carrier acknowledgments as remote playout."""

import json
import wave
from bisect import bisect_right
from collections import Counter

from voice_bench.evaluation.cohort_metrics import distribution, word_errors
from voice_bench.evaluation.conversation_timing import merge
from voice_bench.evaluation.timing import speech_segments


def measure(directory):
    events = [json.loads(line) for line in (directory / "events.jsonl").read_text().splitlines()]
    media = [e for e in events if e["kind"] == "carrier_media"]
    summaries = [e["payload"] for e in events if e["kind"] == "counterpart_playback_summary"]
    unavailable = {"status": "unavailable", "n": 0, "p50": None, "p90": None, "p95": None}
    result = {
        "version": "phone-observations-v1",
        "ttft_ms": unavailable | {"reason": "No target first-token telemetry on SIP media"},
        "ttfs_ms": unavailable
        | {"reason": "No shared remote playback/capture clock; see acknowledgment delay proxy"},
    }
    if not media or not summaries:
        return result | {"response_delay_proxy": {"status": "unavailable"}}
    rate, segments = speech_segments(directory / "audio/received.wav", 500)
    with wave.open(str(directory / "audio/received.wav")) as handle:
        captured = handle.getnframes()
    offsets, offset = [], 0
    for event in media:
        offsets.append(offset)
        offset += event["payload"]["samples"]
    chunks = [int(e["payload"]["chunk"]) for e in media]
    stamps = [e["observed_monotonic_ns"] for e in media]
    if (
        offset != captured
        or rate != 8000
        or any(b != a + 1 for a, b in zip(chunks, chunks[1:], strict=False))
        or any(b < a for a, b in zip(stamps, stamps[1:], strict=False))
    ):
        return result | {
            "response_delay_proxy": {
                "status": "unavailable",
                "reason": "Carrier media does not exactly account for the received recording",
            }
        }

    def receipt_time(sample):
        index = min(bisect_right(offsets, sample) - 1, len(media) - 1)
        event = media[index]
        # End-of-block receipt was logged after recording. Interpolate within that
        # block only; do not subtract the unrelated carrier timestamp.
        remaining = offsets[index] + event["payload"]["samples"] - sample
        return event["observed_monotonic_ns"] / 1e9 - remaining / rate

    speech = merge([(receipt_time(a), receipt_time(b)) for a, b in segments], gap=0.3)
    starts, acks = {}, {}
    for event in events:
        payload = event["payload"]
        if event["kind"] == "audio_submitted":
            starts.setdefault(payload["item_id"], event["observed_monotonic_ns"] / 1e9)
        elif (
            event["kind"] == "playback_progress" and payload.get("boundary") == "carrier_checkpoint"
        ):
            acks[payload["item_id"]] = event
    items = summaries[-1]["items"]
    rows = []
    for item in items:
        row = {"item_id": item["item_id"], "delay_ms": None}
        rows.append(row)
        ack = acks.get(item["item_id"])
        if not ack or item["generated_ms"] - item["played_ms"] > 1:
            row["status"] = "incomplete_or_interrupted_playback"
            continue
        end = ack["observed_monotonic_ns"] / 1e9
        limit = min((t for t in starts.values() if t > end), default=receipt_time(captured))
        row.update(ack_event_sequence=ack["sequence"], observed_wait_ms=(limit - end) * 1000)
        start = starts.get(item["item_id"])
        if start is None:
            row["status"] = "missing_submission"
            continue
        if any(a < end and b > start for a, b in speech):
            row["status"] = "speech_observed_before_final_ack"
            continue
        onset = next((a for a, _ in speech if end < a < limit), None)
        row["status"] = "answered_after_ack" if onset is not None else "no_reply_before_next_item"
        if onset is not None:
            row["delay_ms"] = (onset - end) * 1000
    result["response_delay_proxy"] = {
        "status": "measured",
        "boundary": "final_carrier_playback_ack_received_to_target_speech_block_received",
        "clock": "worker monotonic receipt observations; 8 kHz blocks interpolated locally",
        "limitations": "Not exact remote TTFS. Includes network asymmetry, trailing playback "
        "silence and local recording/event overhead. Energy speech boundaries are estimates. "
        "Unanswered closing items are not automatically failures; overlap is not automatically "
        "a bad interruption. Quantiles describe observations in this call, not model tails.",
        "counts": dict(Counter(r["status"] for r in rows)),
        "opportunities": rows,
        "delay_ms": distribution([r["delay_ms"] for r in rows if r["delay_ms"] is not None]),
    }
    evaluation_path = directory / "evaluation/auto-v2/result.json"
    provider_path = directory / "provider/rumik-call.json"
    evaluation = json.loads(evaluation_path.read_text()) if evaluation_path.exists() else {}
    provider = json.loads(provider_path.read_text()) if provider_path.exists() else {}
    transcripts = (evaluation.get("judge") or {}).get("transcripts", [])
    reference = " ".join(
        t["text"]
        for t in sorted(transcripts, key=lambda t: t["evidence"]["start_seconds"])
        if t["source"] == "audio/sent.wav"
    )
    entries = provider.get("transcript") or []
    if not isinstance(entries, list):
        entries = []
    hypothesis = " ".join(
        t.get("content", t.get("text", "")) for t in entries if t.get("role") == "user"
    )
    complete = all(i["generated_ms"] - i["played_ms"] <= 1 for i in items)
    result["wer"] = {
        "status": "provisional" if reference and entries and complete else "unavailable",
        "reference": "Independent transcription of submitted employee audio",
        "hypothesis": "Hosted Rumik post-call user-role transcript",
        "all_items_playback_acknowledged": complete,
        "human_reference_review": False,
        "limitations": "ASR-to-ASR discrepancy, not gold-reference WER. Carrier acknowledgment "
        "does not prove remote hearing. Script differences and transcription errors count. "
        "Incomplete playback prevents comparison with the full submitted transcript.",
        "reference_text": reference,
        "hypothesis_text": hypothesis,
        "counts": word_errors(reference, hypothesis)
        if reference and entries and complete
        else None,
    }
    return result
