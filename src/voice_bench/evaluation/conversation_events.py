"""Per-opportunity audio observations. Speech meaning is always a separate review."""

import json
import wave
from typing import Literal

from pydantic import Field

from voice_bench.evaluation.timing import speech_segments
from voice_bench.models import Contract, EvidenceRef


class ConversationEventReview(Contract):
    event_id: str
    delivered: Literal["met", "not_met", "uncertain"] = "uncertain"
    correction: Literal["met", "not_met", "uncertain", "not_applicable"] = "uncertain"
    resumption: Literal["met", "not_met", "uncertain"] = "uncertain"
    explanation: str = Field(min_length=1)
    evidence: tuple[EvidenceRef, ...] = ()


def merge(intervals):
    result = []
    for start, end in sorted(intervals):
        if result and start <= result[-1][1] + 1e-8:
            result[-1] = (result[-1][0], max(end, result[-1][1]))
        else:
            result.append((start, end))
    return result


def aligned_speech(directory, events, name, kind):
    rate, segments = speech_segments(directory / f"audio/{name}.wav", threshold=500)
    blocks = [
        e["payload"]
        for e in events
        if e["kind"] == kind and e["clock_id"] == "chromium-audio-context"
    ]
    if not blocks or any(b["rate"] != rate for b in blocks):
        raise ValueError("Missing or incompatible browser audio mapping")
    intervals = []
    for start, end in segments:
        coverage = []
        for block in blocks:
            left = max(start, block["recording_offset"])
            right = min(end, block["recording_offset"] + block["samples"])
            if right > left:
                origin = block["sample"] - block["recording_offset"]
                intervals.append(((origin + left) / rate, (origin + right) / rate))
                coverage.append((left, right))
        if sum(b - a for a, b in merge(coverage)) != end - start:
            raise ValueError("Speech includes an unmapped recording interval")
    return merge(intervals)


def observe_events(directory, case, refs):
    definitions = case.get("conversation_events", [])
    if not definitions:
        return []
    events = (
        [json.loads(line) for line in (directory / "events.jsonl").read_text().splitlines()]
        if "events.jsonl" in refs
        else []
    )
    tracks = None
    if {"audio/played.wav", "audio/received.wav"}.issubset(refs):
        try:
            tracks = (
                aligned_speech(directory, events, "played", "rendered_block"),
                aligned_speech(directory, events, "received", "received_block"),
            )
        except (ValueError, OSError, KeyError, wave.Error):
            pass
    output = []
    for definition in definitions:
        event_id = definition["event_id"]
        linked = [
            e
            for e in events
            if e["kind"] == "conversation_event_audio" and e["payload"]["event_id"] == event_id
        ]
        items = {e["payload"]["item_id"] for e in linked}
        playback = [
            e
            for e in events
            if e["kind"] == "playback_progress"
            and e["payload"].get("item_id") in items
            and e["payload"].get("boundary") == "browser_render"
            and e["clock_id"] == "chromium-audio-context"
            and all(k in e["payload"] for k in ("sample", "samples", "rate"))
        ]
        intervals = merge(
            [
                (
                    e["payload"]["sample"] / e["payload"]["rate"],
                    (e["payload"]["sample"] + e["payload"]["samples"]) / e["payload"]["rate"],
                )
                for e in playback
            ]
        )
        overlaps = []
        if intervals and tracks is not None:
            for left, right in intervals:
                for target_start, target_end in tracks[1]:
                    # Target must begin during this item, not already be talking before it.
                    if not intervals[0][0] <= target_start < intervals[-1][1]:
                        continue
                    for desk_start, desk_end in tracks[0]:
                        start = max(left, target_start, desk_start)
                        end = min(right, target_end, desk_end)
                        if end > start:
                            overlaps.append((start, end))
        cancellations = [
            e
            for e in events
            if e["kind"] == "counterpart_playback_interrupted"
            and e["payload"].get("item_id") in items
        ]
        output.append(
            {
                "event_id": event_id,
                "kind": definition["kind"],
                "requested": any(
                    e["kind"] == "conversation_event_requested"
                    and e["payload"]["event_id"] == event_id
                    for e in events
                ),
                "rendered_audio_observed": bool(intervals),
                "content_delivery": "requires_human_review" if intervals else "untested",
                "audio_overlap_status": "uncertain"
                if tracks is None
                else ("overlap_observed" if overlaps else "interruption_not_observed"),
                "overlap_ms": round(sum(b - a for a, b in merge(overlaps)) * 1000, 3)
                if tracks is not None
                else None,
                "playback_cancel_observed": bool(cancellations),
                "last_rendered_sample_time_seconds": intervals[-1][1] if intervals else None,
                "clock_id": "chromium-audio-context",
                "algorithm": "rms-20ms-v1-threshold500",
                "event_sequences": [e["sequence"] for e in linked + playback + cancellations],
                "correction_accuracy": "requires_human_review",
                "resumption_accuracy": "requires_human_review",
                "challenge_result": "untested",
            }
        )
    return output


def review_events(directory, case, refs, reviews):
    from voice_bench.evaluation.scoring import validate_reference

    observations = observe_events(directory, case, refs)
    known = {o["event_id"]: o for o in observations}
    seen = set()
    for review in reviews:
        if review.event_id not in known or review.event_id in seen:
            raise ValueError("Unknown or repeated conversation event review")
        seen.add(review.event_id)
        observation = known[review.event_id]
        for ref in review.evidence:
            validate_reference(directory, ref)
        if (
            review.delivered != "uncertain"
            or review.correction in {"met", "not_met"}
            or review.resumption != "uncertain"
        ):
            names = {r.artifact_key.split("/", 2)[-1] for r in review.evidence}
            if not {"events.jsonl", "audio/played.wav", "audio/received.wav"}.issubset(names):
                raise ValueError(
                    "Event judgments require both recorded audio tracks and event evidence"
                )
        if review.delivered == "met" and not observation["rendered_audio_observed"]:
            raise ValueError("An unplayed event cannot count as delivered")
        observation["human_review"] = review.model_dump(mode="json")
        observation["content_delivery"] = review.delivered
        observation["correction_accuracy"] = review.correction
        observation["resumption_accuracy"] = review.resumption
        if review.delivered == "met":
            if observation["kind"] != "misread":
                observation["challenge_result"] = "reviewed_conversation_event"
            elif observation["audio_overlap_status"] == "overlap_observed":
                observation["challenge_result"] = (
                    "interruption_demonstrated"
                    if review.correction == review.resumption == "met"
                    else "observed_overlap_requires_correction_review"
                )
            else:
                observation["challenge_result"] = observation["audio_overlap_status"]
    return observations
