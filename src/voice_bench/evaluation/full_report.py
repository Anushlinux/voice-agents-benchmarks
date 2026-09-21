"""Local report artifacts derived from sealed evidence; no provider requests."""

import json
import sys
import wave
from array import array

from voice_bench.evidence.local import canonical, digest, publish, verify_bundle


def synchronized_audio(directory, destination):
    events = [json.loads(line) for line in (directory / "events.jsonl").read_text().splitlines()]
    blocks = [
        e["payload"] | {"kind": e["kind"]}
        for e in events
        if e["kind"] in {"rendered_block", "received_block"}
        and e["clock_id"] == "chromium-audio-context"
    ]
    if not blocks or len({b["rate"] for b in blocks}) != 1:
        return {"status": "unavailable", "reason": "Missing consistent browser clock mappings"}
    rate = blocks[0]["rate"]
    origin = min(b["sample"] for b in blocks)
    end = max(b["sample"] + b["samples"] for b in blocks)
    if end - origin > rate * 3600:
        return {"status": "unavailable", "reason": "Report audio exceeds one hour"}
    stereo = array("h", [0]) * (2 * (end - origin))
    for channel, (name, kind) in enumerate(
        (("played", "rendered_block"), ("received", "received_block"))
    ):
        with wave.open(str(directory / f"audio/{name}.wav"), "rb") as handle:
            if (handle.getnchannels(), handle.getsampwidth(), handle.getframerate()) != (
                1,
                2,
                rate,
            ):
                raise ValueError("Unsupported recording format")
            track = array("h")
            track.frombytes(handle.readframes(handle.getnframes()))
        if sys.byteorder != "little":
            track.byteswap()
        for block in blocks:
            if block["kind"] != kind:
                continue
            start, count = block["recording_offset"], block["samples"]
            offset = block["sample"] - origin
            if not 0 <= start < start + count <= len(track):
                raise ValueError("Audio mapping exceeds the captured recording")
            stereo[2 * offset + channel : 2 * (offset + count) + channel : 2] = track[
                start : start + count
            ]
    if sys.byteorder != "little":
        stereo.byteswap()
    with destination.open("xb") as output:
        with wave.open(output, "wb") as handle:
            handle.setparams((2, 2, rate, 0, "NONE", "none"))
            handle.writeframes(stereo.tobytes())
    return {
        "status": "created",
        "sha256": digest(destination.read_bytes()),
        "origin_sample": origin,
        "rate": rate,
        "duration_seconds": (end - origin) / rate,
        "clock": "chromium-audio-context",
        "left": "restaurant employee",
        "right": "received Rumik audio",
    }


def write_attempt_report(directory, destination, pipeline):
    from voice_bench.evaluation.cohort_metrics import measure_attempt
    from voice_bench.evaluation.diagnostics import conversation_diagnostics

    verify_bundle(directory)
    destination.mkdir(parents=True, exist_ok=False)

    def read(name):
        path = directory / name
        return json.loads(path.read_text()) if path.exists() else {}

    case = read("config/case.json")
    evaluation = read("evaluation/auto-v2/result.json")
    jev = read("evaluation/jev-auto-v2/result.json")
    diagnostics = conversation_diagnostics(directory, pipeline)
    publish(destination / "diagnostics-v1.json", canonical(diagnostics))
    try:
        measurements = measure_attempt(directory)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        measurements = {"status": "unavailable", "reason": type(exc).__name__}
    publish(destination / "measurements-v2.json", canonical(measurements))
    details = {
        "case": case,
        "execution": read("result.json"),
        "pipeline": pipeline,
        "business_state": read("business/final.json"),
        "business_audit": read("business/audit.json"),
        "private_report": read("target/user-report.json"),
        "evaluation": evaluation,
        "jev": jev,
        "diagnostics": diagnostics,
        "measurements": measurements,
        "raw_directory": str(directory.resolve()),
    }
    publish(destination / "details.json", canonical(details))
    try:
        audio = synchronized_audio(directory, destination / "conversation.wav")
    except (ValueError, OSError) as exc:
        audio = {"status": "error", "error_type": type(exc).__name__}
    publish(destination / "audio-provenance.json", canonical(audio))
    windows = (evaluation.get("judge") or {}).get("transcripts", [])
    lines = [
        "# Independent audio transcription",
        "",
        "Times are recording windows, not exact word or turn timestamps.",
        "",
    ]
    for entry in windows:
        ref = entry["evidence"]
        speaker = "Rumik" if entry["source"] == "audio/received.wav" else "Restaurant employee"
        lines.extend(
            [
                f"**{speaker}, {ref['start_seconds']:.2f}–{ref['end_seconds']:.2f}s**",
                "",
                entry["text"] or "[No transcribed speech]",
                "",
            ]
        )
    publish(destination / "transcript.md", "\n".join(lines).encode())
    text = [
        "# Conversation and benchmark result",
        "",
        f"Automated outcome: **{evaluation.get('outcome', 'unresolved')}**. "
        f"Simulation validity: **{evaluation.get('validity', 'unresolved')}**.",
        "",
        f"Full evaluation: **{pipeline.get('status', 'not_run')}**. "
        f"Conversation repair accepted: **{pipeline.get('conversation_accepted', False)}**.",
        "",
        "Human listening is pending. Text judges cannot establish acoustic naturalness "
        "or prove that suspected self-talk was audible.",
        "",
        case.get("user_task", {}).get("request", "Task evidence missing"),
        "",
        "[Independent transcript](transcript.md) · "
        "[All metrics and raw judge answers](details.json) · "
        "[Failure evidence and uncertainty](diagnostics-v1.json) · "
        "[Timing, WER and endpointing availability](measurements-v2.json)",
        "",
        f"Observed task completion: **{diagnostics['observed_task_completion']}**. "
        f"Established failure owner: **{diagnostics['established_failure_owner']}**. "
        "Missing required outputs remain visible even when their cause is unknown.",
        "",
        "Left audio: restaurant employee. Right audio: received Rumik.",
        "",
    ]
    if audio["status"] == "created":
        text.extend([f"![Full conversation]({(destination / 'conversation.wav').resolve()})", ""])
    text.extend(["## Evaluation stages", "", "| Stage | Status |", "| --- | --- |"])
    for name, stage in pipeline.get("stages", {}).items():
        text.append(f"| {name} | {stage['status']} |")
    text.extend(["", "## Metrics", "", "| Metric | Result | Explanation |", "| --- | --- | --- |"])
    for metric in evaluation.get("metrics", []):
        explanation = metric["explanation"].replace("|", "/").replace("\n", " ")
        text.append(f"| {metric['name']} | {metric['status']} | {explanation} |")
    text.extend(
        [
            "",
            "## Private report",
            "",
            details["private_report"].get("text", "No private report received."),
            "",
            "## Business outcome",
            "",
            "```json",
            json.dumps(details["business_state"].get("bookings", []), ensure_ascii=False, indent=2),
            "```",
            "",
            "## Silence and response timing",
            "",
            "```json",
            json.dumps(pipeline.get("conversation_timing", {}), indent=2),
            "```",
            "",
            "## Employee speech delivery",
            "",
            "Local playback completeness is checked separately from task success. "
            "Interruptions still need conversation review; local playback does not prove "
            "remote hearing.",
            "",
            "```json",
            json.dumps(pipeline.get("playback_integrity", {}), indent=2),
            "```",
            "",
            "## Independent Jev assessment",
            "",
            "```json",
            json.dumps(
                jev.get("answers", pipeline.get("stages", {}).get("jev", {})),
                ensure_ascii=False,
                indent=2,
            ),
            "```",
            "",
            "Jev is an independent comparison and cannot override verified business records.",
            "All attempts and incomplete stages remain in the batch counts.",
        ]
    )
    publish(destination / "README.md", "\n".join(text).encode())
