"""Timing on one browser sample clock. Telephone receipt clocks stay separate."""

import audioop
import json
import wave

from voice_bench.evaluation.timeline import audio_clock_spans


def speech_segments(path, threshold, minimum_ms=80):
    with wave.open(str(path), "rb") as handle:
        rate = handle.getframerate()
        if handle.getnchannels() != 1 or handle.getsampwidth() != 2:
            raise ValueError("Expected mono PCM16")
        block = max(1, rate // 50)
        position, start = 0, None
        segments = []
        while data := handle.readframes(block):
            speaking = audioop.rms(data, 2) >= threshold
            if speaking and start is None:
                start = position
            if not speaking and start is not None:
                if (position - start) * 1000 / rate >= minimum_ms:
                    segments.append((start, position))
                start = None
            position += len(data) // 2
        if start is not None and (position - start) * 1000 / rate >= minimum_ms:
            segments.append((start, position))
    return rate, segments


def browser_timing(directory, *, threshold=500, response_window_seconds=10):
    if not (directory / "events.jsonl").exists():
        return {"status": "uncertain", "reason": "Event clock mappings are missing"}
    try:
        events = [
            json.loads(line) for line in (directory / "events.jsonl").read_text().splitlines()
        ]
    except (ValueError, UnicodeError):
        return {"status": "uncertain", "reason": "Incomplete event log"}
    tracks = {}
    for name, kind in (("played", "rendered_block"), ("received", "received_block")):
        path = directory / f"audio/{name}.wav"
        blocks = [
            e["payload"]
            for e in events
            if e["kind"] == kind and e["clock_id"] == "chromium-audio-context"
        ]
        if not path.exists() or not blocks:
            return {"status": "uncertain", "reason": "No aligned browser playback/capture evidence"}
        rate, segments = speech_segments(path, threshold)

        tracks[name] = []
        for start, end in segments:
            mapping = audio_clock_spans(start, end, [{"payload": b} for b in blocks], rate)
            if mapping["status"] != "mapped" or len(mapping["spans"]) != 1:
                return {
                    "status": "uncertain",
                    "reason": "Speech interval lacks a continuous browser clock mapping",
                }
            span = mapping["spans"][0]
            tracks[name].append((span["start_seconds"], span["end_seconds"]))
    gaps, overlaps, unanswered = [], 0, 0
    for i, (start, end) in enumerate(tracks["played"]):
        if any(a < end and b > start for a, b in tracks["received"]):
            overlaps += 1
            continue
        limit = min(
            end + response_window_seconds,
            tracks["played"][i + 1][0] if i + 1 < len(tracks["played"]) else float("inf"),
        )
        next_speech = next((a for a, _ in tracks["received"] if end <= a < limit), None)
        if next_speech is None:
            unanswered += 1
        else:
            gaps.append(round((next_speech - end) * 1000, 3))
    ordered = sorted(gaps)
    overlap_lengths = [
        round((min(end, b) - max(start, a)) * 1000, 3)
        for start, end in tracks["played"]
        for a, b in tracks["received"]
        if a < end and b > start
    ]
    return {
        "status": "measured",
        "clock_id": "chromium-audio-context",
        "boundary": "browser_render_to_browser_capture",
        "algorithm": "rms-20ms-v1",
        "rms_threshold": threshold,
        "response_window_seconds": response_window_seconds,
        "response_gaps_ms": gaps,
        "overlap_segments": overlaps,
        "overlap_durations_ms": overlap_lengths,
        "no_response_segments": unanswered,
        "caller_segments": len(tracks["played"]),
        "p50_ms": ordered[(len(ordered) - 1) // 2] if ordered else None,
        "p95_ms": ordered[min(len(ordered) - 1, int(len(ordered) * 0.95))] if ordered else None,
    }


def caller_processing(directory):
    """Observed caller turnaround, explicitly including provider/network processing."""
    try:
        events = [
            json.loads(line) for line in (directory / "events.jsonl").read_text().splitlines()
        ]
    except (OSError, ValueError):
        return {"status": "uncertain", "reason": "Missing or incomplete event log"}
    stops, measurements = {}, []
    for event in events:
        if event["source"] != "caller":
            continue
        clock = event["clock_id"]
        if event["kind"] == "target_speech_stopped":
            stops[clock] = event["observed_monotonic_ns"]
        elif event["kind"] == "first_audio_generated" and clock in stops:
            elapsed = event["observed_monotonic_ns"] - stops.pop(clock)
            if elapsed >= 0:
                measurements.append({"clock_id": clock, "milliseconds": elapsed / 1_000_000})
    return {
        "status": "measured" if measurements else "uncertain",
        "boundary": "vad_stop_observed_to_first_generated_audio_observed",
        "includes_network_and_provider_processing": True,
        "measurements": measurements,
    }
