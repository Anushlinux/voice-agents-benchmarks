"""Derived audio windows and event anchors; never invent word timing or clock alignment."""

import json
import wave

from voice_bench.models import EvidenceRef

ANCHOR_KINDS = {
    "business_tool_result",
    "reference_delivery_requested",
    "target_speech_detected",
    "target_speech_stopped",
    "response_done",
    "reservation_action",
    "business_action",
    "tool_result",
    "target_report_received",
    "end_call_requested",
    "ending_after_target_report",
    "failure",
    "termination_unconfirmed",
    "finalized",
    "counterpart_playback_interrupted",
    "caller_playback_cancelled",
    "scenario_event_requested",
    "scenario_event_delivered",
    "conversation_event_requested",
    "conversation_event_response",
    "conversation_event_audio",
    "conversation_event_status",
    "counterpart_incomplete",
    "conversation_idle_timeout",
    "bridge_error",
}


def audio_clock_spans(start, end, blocks, rate):
    """Map the entire half-open recording range, retaining holes and discontinuities."""
    cursor, spans = start, []
    for event in blocks:
        block = event["payload"]
        left, right = block["recording_offset"], block["recording_offset"] + block["samples"]
        if right <= start or left >= end:
            continue
        if block["rate"] != rate or left > cursor or left < cursor and cursor != start:
            return {
                "status": "uncertain",
                "reason": "Incomplete or conflicting audio clock mapping",
            }
        a, b = max(start, left), min(end, right)
        mapped_a, mapped_b = block["sample"] + a - left, block["sample"] + b - left
        if spans and mapped_a < spans[-1]["end_sample"]:
            return {"status": "uncertain", "reason": "Audio clock moved backwards"}
        if spans and mapped_a == spans[-1]["end_sample"]:
            spans[-1]["end_sample"] = mapped_b
        else:
            spans.append({"start_sample": mapped_a, "end_sample": mapped_b})
        cursor = b
    if cursor != end or not spans:
        return {"status": "uncertain", "reason": "No complete browser sample mapping"}
    return {
        "status": "mapped",
        "clock_id": "chromium-audio-context",
        "sample_rate_hz": rate,
        "spans": [
            {"start_seconds": s["start_sample"] / rate, "end_seconds": s["end_sample"] / rate}
            for s in spans
        ],
    }


def build_timeline(directory, transcripts, refs):
    events = (
        [json.loads(line) for line in (directory / "events.jsonl").read_text().splitlines()]
        if "events.jsonl" in refs
        else []
    )
    sources, windows, anchors = {}, [], []
    for index, transcript in enumerate(transcripts, 1):
        source_id = f"speech-window-{index:04}"
        ref = EvidenceRef.model_validate(transcript["evidence"])
        original = refs.get(transcript["source"])
        if not original or (ref.artifact_key, ref.sha256) != (
            original.artifact_key,
            original.sha256,
        ):
            raise ValueError("Transcript does not cite its sealed recording")
        if ref.start_seconds is None or ref.end_seconds is None:
            raise ValueError("Transcript must identify a bounded recording window")
        with wave.open(str(directory / transcript["source"]), "rb") as audio:
            rate, frames = audio.getframerate(), audio.getnframes()
        start, end = round(ref.start_seconds * rate), round(ref.end_seconds * rate)
        if not 0 <= start < end <= frames:
            raise ValueError("Transcript range is outside its recording")
        kind = {"audio/played.wav": "rendered_block", "audio/received.wav": "received_block"}.get(
            transcript["source"]
        )
        blocks = [
            e for e in events if e["kind"] == kind and e["clock_id"] == "chromium-audio-context"
        ]
        mapping = audio_clock_spans(start, end, blocks, rate)
        sources[source_id] = ref
        windows.append(
            {
                "source_id": source_id,
                "speaker": "target"
                if transcript["source"] == "audio/received.wav"
                else "counterpart",
                "category": "transcribed_speech",
                "text": transcript["text"],
                "transcription_status": transcript.get("transcription_status", "historical"),
                "recording_start_seconds": ref.start_seconds,
                "recording_end_seconds": ref.end_seconds,
                "text_timing": "window_only_not_word_or_utterance_timestamps",
                "delivery_boundary": {
                    "audio/played.wav": "browser_render",
                    "audio/received.wav": "target_audio_capture",
                }.get(transcript["source"], "submitted_not_confirmed_played"),
                "clock_mapping": mapping,
            }
        )
    for event in events:
        if event["kind"] not in ANCHOR_KINDS:
            continue
        source_id = f"event-{event['sequence']}"
        sources[source_id] = refs["events.jsonl"].model_copy(
            update={"event_sequences": (event["sequence"],)}
        )
        anchors.append(
            {
                "source_id": source_id,
                "category": "event_observation",
                "sequence": event["sequence"],
                "kind": event["kind"],
                "observed_clock_id": event["clock_id"],
                "observed_monotonic_ns": event["observed_monotonic_ns"],
                "payload": event["payload"],
            }
        )
    return {
        "version": "evidence-timeline-v1",
        "limitations": [
            "Text belongs to its entire recording window; "
            "exact words and utterance timing are unknown.",
            "Overlapping windows remain overlapping. List order does not imply dialogue order.",
            "Event receipt time is not browser playback time; do not subtract different clocks.",
            "Tool output establishes business facts, never that a fact was spoken.",
            "Mapped playback proves local rendering, not remote perception or semantic consent.",
        ],
        "speech_windows": windows,
        "event_anchors": anchors,
    }, sources
