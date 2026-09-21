"""Local, versioned measurements with explicit clocks and missing-data denominators."""

import json
import math
import unicodedata
from collections import Counter

from voice_bench.evaluation.conversation_timing import measure


def distribution(values):
    """Nearest-rank quantiles over observations, never averages of case quantiles."""
    ordered = sorted(values)
    return {
        "n": len(ordered),
        "mean": sum(ordered) / len(ordered) if ordered else None,
        **{
            f"p{q}": ordered[math.ceil(len(ordered) * q / 100) - 1] if ordered else None
            for q in (50, 90, 95)
        },
        "quantile_method": "nearest_rank",
    }


def words(text):
    normalized = unicodedata.normalize("NFKC", text).casefold()
    return "".join(
        " " if unicodedata.category(c)[0] in {"P", "S"} else c for c in normalized
    ).split()


def word_errors(reference, hypothesis):
    """Word-level Levenshtein counts; preserve numbers, names and original scripts."""
    ref, hyp = words(reference), words(hypothesis)
    previous = [(i, 0, i, 0) for i in range(len(hyp) + 1)]
    for i, expected in enumerate(ref, 1):
        current = [(i, 0, 0, i)]
        for j, actual in enumerate(hyp, 1):
            if expected == actual:
                current.append(previous[j - 1])
                continue
            cost, s, ins, d = previous[j - 1]
            substitution = (cost + 1, s + 1, ins, d)
            cost, s, ins, d = current[j - 1]
            insertion = (cost + 1, s, ins + 1, d)
            cost, s, ins, d = previous[j]
            deletion = (cost + 1, s, ins, d + 1)
            current.append(min((substitution, deletion, insertion), key=lambda v: v[0]))
        previous = current
    errors, substitutions, insertions, deletions = previous[-1]
    return {
        "reference_words": len(ref),
        "hypothesis_words": len(hyp),
        "substitutions": substitutions,
        "insertions": insertions,
        "deletions": deletions,
        "errors": errors,
        "wer": errors / len(ref) if ref else None,
    }


def first_token_times(events):
    """Audio-clock times of Rumik's first text packet per generation, in order.

    These are the `bot-llm-text` lifecycle packets Rumik publishes into the room,
    stamped by the browser with the same audio clock as the recordings. They are
    observations of arrival at the browser, not internal generation timestamps.
    """
    from voice_bench.evaluation.target_timing import generation_windows

    times = []
    for row in generation_windows(events):
        first = row.get("first_text")
        if first and first.get("audio_context_seconds") is not None:
            times.append(first["audio_context_seconds"])
    return sorted(times)


def response_opportunities(events, activity):
    """One opportunity per played employee item, rather than per acoustic pause.

    These are playback items, not human annotated semantic turns. A closing utterance
    may need no reply. Overlap is observable but does not establish a bad interruption.
    """
    if activity.get("status") != "measured":
        return {"status": "unavailable", "reason": "Shared audio clock is incomplete"}
    summaries = [e["payload"] for e in events if e["kind"] == "counterpart_playback_summary"]
    if not summaries:
        return {"status": "unavailable", "reason": "Missing final playback item summary"}
    items = {i["item_id"]: i for i in summaries[-1]["items"]}
    bounds = {}
    for event in events:
        if event["kind"] != "playback_progress" or event["clock_id"] != "chromium-audio-context":
            continue
        p = event["payload"]
        start, end = p["sample"] / p["rate"], (p["sample"] + p["samples"]) / p["rate"]
        old = bounds.get(p["item_id"], (start, end))
        bounds[p["item_id"]] = (min(old[0], start), max(old[1], end))
    ordered = sorted(bounds.items(), key=lambda pair: pair[1][0])
    rows = []
    capture_start, capture_end = activity["coverage_seconds"]
    target = activity["speaker_activity"]["target"]
    employee = activity["speaker_activity"]["counterpart"]
    first_tokens = first_token_times(events)
    for index, (item_id, (start, end)) in enumerate(ordered):
        item = items.get(item_id)
        row = {
            "item_id": item_id,
            "playback_start_seconds": start,
            "playback_end_seconds": end,
            "turn_index": index + 1,
            "clock_id": "chromium-audio-context",
            "target_first_token_seconds": None,
            "ttft_ms": None,
            "ttft_status": "no_first_text_packet_observed",
        }
        rows.append(row)
        if not item or start < capture_start or end > capture_end:
            row["status"] = "incomplete_evidence"
            continue
        row["target_interruption_signaled"] = item["interrupted_by_target"]
        # The caller can mark an interruption after the entire item was rendered.
        # Exclude an interrupted delivery only when some generated audio was lost;
        # a complete item still uses the captured speech to decide overlap/reply.
        if item["interrupted_by_target"] and item["generated_ms"] - item["played_ms"] > 1:
            row["status"] = "interrupted_playback"
            continue
        if item["generated_ms"] - item["played_ms"] > 1:
            row["status"] = "incomplete_playback"
            continue
        speech = [(max(a, start), min(b, end)) for a, b in employee if a < end and b > start]
        if not speech:
            row["status"] = "no_detected_employee_speech"
            continue
        speech_start, speech_end = speech[0][0], speech[-1][1]
        row["speech_start_seconds"] = speech_start
        row["speech_end_seconds"] = speech_end
        limit = min(
            capture_end, ordered[index + 1][1][0] if index + 1 < len(ordered) else capture_end
        )
        # First text token Rumik published after this item, on the shared audio clock.
        token = next((t for t in first_tokens if speech_end <= t < limit), None)
        if token is not None:
            row.update(
                target_first_token_seconds=token,
                ttft_ms=(token - speech_end) * 1000,
                ttft_status="measured_first_text_packet_after_rendered_speech",
            )
        if any(a < speech_end and b > speech_start for a, b in target):
            row["status"] = "overlap"
            continue
        onset = next((a for a, _ in target if speech_end <= a < limit), None)
        if onset is None:
            row.update(status="no_observed_reply", observed_wait_ms=(limit - speech_end) * 1000)
        else:
            row.update(
                status="answered",
                target_speech_start_seconds=onset,
                ttfs_ms=(onset - speech_end) * 1000,
            )
    samples = [r["ttfs_ms"] for r in rows if r["status"] == "answered"]
    token_samples = [r["ttft_ms"] for r in rows if r.get("ttft_ms") is not None]
    return {
        "status": "measured",
        "clock": "chromium-audio-context",
        "boundary": "last_employee_speech_rendered_to_first_target_speech_captured",
        "algorithm": "played-item-rms20ms-merge300ms-v2",
        "rms_threshold": activity["rms_threshold"],
        "semantic_turns_annotated": False,
        "counts": dict(Counter(r["status"] for r in rows)),
        "opportunities": rows,
        "ttfs_ms": distribution(samples),
        "ttft_ms": distribution(token_samples),
        "ttft_boundary": "last_employee_speech_rendered_to_first_target_text_packet_received",
        "aat_response_ms": distribution(samples)["mean"],
        "limitations": "Item boundaries and energy-based speech are estimates. No-reply items "
        "include closings. Overlap is not automatically an endpointing error. "
        "Unanswered items are retained separately, not converted to zero or a timeout latency.",
    }


def measure_attempt(directory):
    events = [json.loads(line) for line in (directory / "events.jsonl").read_text().splitlines()]
    activity = measure(directory)
    evaluation = json.loads((directory / "evaluation/auto-v2/result.json").read_text())
    provider_path = directory / "provider/rumik-call.json"
    provider = json.loads(provider_path.read_text()) if provider_path.exists() else {}
    transcripts = (evaluation.get("judge") or {}).get("transcripts", [])
    reference = " ".join(
        t["text"]
        for t in sorted(transcripts, key=lambda t: t["evidence"]["start_seconds"])
        if t["source"] == "audio/played.wav"
    )
    entries = provider.get("transcript") or []
    if not isinstance(entries, list):
        entries = []
    hypothesis = " ".join(
        t.get("content", t.get("text", "")) for t in entries if t.get("role") == "user"
    )
    wer = {
        "status": "provisional" if reference and entries else "unavailable",
        "reference": "Independent gpt-4o-mini-transcribe transcription "
        "of actually played employee audio",
        "hypothesis": "Hosted Rumik post-call user-role transcript",
        "human_reference_review": False,
        "normalization": "NFKC, casefold, punctuation/symbol separators; "
        "no transliteration or number rewriting",
        "limitations": "ASR-to-ASR discrepancy, not gold-reference recognition accuracy. "
        "Independent transcription errors, incomplete provider logs and Hinglish script "
        "differences can inflate this value. No internal STT trace is available.",
        "reference_text": reference,
        "hypothesis_text": hypothesis,
        "counts": word_errors(reference, hypothesis) if reference and entries else None,
    }
    from voice_bench.evaluation.target_timing import measure as target_timing

    return {
        "version": "full-cohort-metrics-v4-ttft",
        "call_timestamps": {
            "worker_observations": [
                {
                    "kind": e["kind"],
                    "utc": e["observed_at"],
                    "clock_id": e["clock_id"],
                    "monotonic_ns": e["observed_monotonic_ns"],
                    "event_sequence": e["sequence"],
                }
                for e in events
                if e["kind"]
                in {
                    "registration_requested",
                    "registered",
                    "browser_start_requested",
                    "connected",
                    "target_report_received",
                    "counterpart_hangup_requested",
                    "target_hangup_after_report",
                    "conversation_idle_timeout",
                    "finalized",
                }
            ],
            "provider_observations": {
                name: provider.get(name) for name in ("createdAt", "startedAt", "endedAt")
            },
            "limitations": "Worker and provider UTC timestamps are separate observations. "
            "Turn latency uses browser sample time only, not their difference.",
        },
        "response_timing": response_opportunities(events, activity),
        "wer": wer,
        "ttft": target_timing(events),
        "endpointing_accuracy": {
            "status": "unavailable",
            "reason": "No hosted endpoint decisions or reviewed semantic end-of-turn labels",
            "numerator": None,
            "denominator": None,
            "observable_proxy": "response_timing opportunity counts: overlap, "
            "interrupted playback and no observed reply",
        },
        "activity": activity,
    }
