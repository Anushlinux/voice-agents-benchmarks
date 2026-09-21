"""Auditable acoustic activity on the shared browser clock, not semantic turn labels."""

import json

from voice_bench.evaluation.timeline import audio_clock_spans
from voice_bench.evaluation.timing import speech_segments


def merge(intervals, gap=0):
    result = []
    for start, end in sorted(intervals):
        if result and start <= result[-1][1] + gap:
            result[-1][1] = max(result[-1][1], end)
        else:
            result.append([start, end])
    return result


def measure(directory, *, threshold=500, long_silence_seconds=10):
    try:
        events = [
            json.loads(line) for line in (directory / "events.jsonl").read_text().splitlines()
        ]
        tracks, coverage = {}, {}
        for speaker, name, kind in (
            ("counterpart", "played", "rendered_block"),
            ("target", "received", "received_block"),
        ):
            blocks = [
                e for e in events if e["kind"] == kind and e["clock_id"] == "chromium-audio-context"
            ]
            if not blocks:
                raise ValueError("Missing shared browser clock")
            coverage[speaker] = merge(
                [
                    (
                        e["payload"]["sample"] / e["payload"]["rate"],
                        (e["payload"]["sample"] + e["payload"]["samples"]) / e["payload"]["rate"],
                    )
                    for e in blocks
                ],
                gap=0.0001,
            )
            rate, segments = speech_segments(directory / f"audio/{name}.wav", threshold)
            mapped = []
            for start, end in segments:
                mapping = audio_clock_spans(start, end, blocks, rate)
                if mapping["status"] != "mapped":
                    raise ValueError("Incomplete speech clock mapping")
                mapped.extend((s["start_seconds"], s["end_seconds"]) for s in mapping["spans"])
            tracks[speaker] = merge(mapped, gap=0.3)
        if any(len(v) != 1 for v in coverage.values()):
            raise ValueError("Discontinuous capture; silence cannot be inferred from missing audio")
        start = max(v[0][0] for v in coverage.values())
        end = min(v[0][1] for v in coverage.values())
        if end <= start:
            raise ValueError("No simultaneous capture interval")
        return summarize_activity(tracks, start, end, threshold, long_silence_seconds)
    except (OSError, ValueError, KeyError) as exc:
        return {"status": "uncertain", "reason": str(exc)}


def summarize_activity(tracks, start, end, threshold=500, long_silence_seconds=10):
    active = merge(
        [
            (max(start, a), min(end, b))
            for spans in tracks.values()
            for a, b in spans
            if a < end and b > start
        ]
    )
    silence, cursor = [], start
    for a, b in active:
        if a > cursor:
            silence.append([cursor, a])
        cursor = max(cursor, b)
    if cursor < end:
        silence.append([cursor, end])
    replies = {}
    for speaker, spans in tracks.items():
        other = tracks["target" if speaker == "counterpart" else "counterpart"]
        gaps, unanswered = [], []
        for i, (a, b) in enumerate(spans):
            if b < start or b > end or any(x < b and y > a for x, y in other):
                continue
            limit = min(end, spans[i + 1][0] if i + 1 < len(spans) else end)
            following = next((x for x, _ in other if b <= x < limit), None)
            (gaps if following is not None else unanswered).append(
                {
                    "after_seconds": b,
                    "gap_ms": round(
                        ((following if following is not None else limit) - b) * 1000, 3
                    ),
                }
            )
        replies["target" if speaker == "counterpart" else "counterpart"] = {
            "response_gaps": gaps,
            "no_response_intervals": unanswered,
        }
    return {
        "status": "measured",
        "clock_id": "chromium-audio-context",
        "boundary": "browser_render_and_capture",
        "algorithm": "rms-20ms-merge300ms-v2",
        "rms_threshold": threshold,
        "activity_is_not_semantic_turns": True,
        "coverage_seconds": [start, end],
        "speaker_activity": tracks,
        "replies": replies,
        "long_silence_threshold_seconds": long_silence_seconds,
        "long_silence_intervals": [
            {
                "start_seconds": a,
                "end_seconds": b,
                "duration_seconds": b - a,
                "attribution": "unknown",
            }
            for a, b in silence
            if b - a >= long_silence_seconds
        ],
    }
