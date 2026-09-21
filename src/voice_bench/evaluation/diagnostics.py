"""Versioned observations, separate from task grades and causal attribution."""

import json

from voice_bench.evaluation.playback import playback_integrity
from voice_bench.evaluation.target_generation import target_generation_diagnostics


def conversation_diagnostics(directory, pipeline):
    def read(name):
        path = directory / name
        return json.loads(path.read_text()) if path.exists() else {}

    events = [json.loads(line) for line in (directory / "events.jsonl").read_text().splitlines()]
    generation = target_generation_diagnostics(events)
    execution = read("result.json")
    evaluation = read("evaluation/auto-v2/result.json")
    case = read("config/case.json")
    report = read("target/user-report.json")
    state = read("business/final.json")
    playback = pipeline.get("playback_integrity") or playback_integrity(directory)
    transport = [e for e in events if e["kind"] == "transport_observation"]
    stats = [e for e in transport if e["payload"].get("name") == "audio_transport_stats"]
    required_report = case.get("completion", "counterpart") != "counterpart"
    symptoms = []
    if generation["reasoning_dominated_samples"]:
        symptoms.append("target_generation_dominated_by_reasoning")
    if required_report and not report:
        symptoms.append("required_private_report_missing")
    if any(e["kind"] == "conversation_idle_timeout" for e in events):
        symptoms.append("conversation_inactivity_stop")
    if playback["status"] == "failed":
        symptoms.append("counterpart_output_or_playback_incomplete")
    if any(e["kind"] == "bridge_error" for e in events):
        symptoms.append("browser_bridge_error")
    if not execution.get("termination_confirmed"):
        symptoms.append("termination_unconfirmed")

    def anchor(event):
        return {
            "artifact": "events.jsonl",
            "sequence": event["sequence"],
            "kind": event["kind"],
            "clock_id": event["clock_id"],
            "observed_at": event["observed_at"],
            "payload": event["payload"],
        }

    stages = {
        "connected",
        "target_speech_detected",
        "target_audio_committed",
        "response_created",
        "response_done",
        "business_tool_result",
        "target_report_received",
        "closing_playback_complete",
        "counterpart_hangup_requested",
        "target_hangup_after_report",
        "playback_progress",
    }
    progress = [
        e
        for e in events
        if e["kind"] in stages
        and (e["kind"] != "response_done" or e["payload"].get("status") == "completed")
        and (
            e["kind"] != "business_tool_result" or e["payload"].get("result", {}).get("ok") is True
        )
    ]
    # Anchor the last observed progress per kind, without treating unrelated
    # timestamps as a common clock or claiming playback establishes hearing.
    last = {e["kind"]: anchor(e) for e in progress}
    decisive = [
        e
        for e in events
        if e["kind"]
        in {
            "conversation_idle_timeout",
            "bridge_error",
            "failure",
            "target_report_idle_timeout",
            "response_cancel_requested",
            "cancelled_tools_discarded",
            "business_tool_result",
            "counterpart_playback_summary",
        }
    ]
    groups = {}
    for e in stats:
        payload = e["payload"]
        key = (payload.get("direction"), payload.get("track_id"))
        group = groups.setdefault(
            key,
            {"direction": key[0], "track_id": key[1], "samples": 0, "available": 0},
        )
        group["samples"] += 1
        group["available"] += payload.get("status") == "available"
        group.setdefault("first", anchor(e))
        group["last"] = anchor(e)
    unknown = [
        "Local playback and outgoing packets do not prove remote perception.",
        "Missing or unchanged packet counters can reflect silence handling; they do not "
        "establish target failure.",
        "Provider-reported generation events are passive client observations. They do not "
        "expose the configured output limit or provider finish_reason and may be incomplete.",
        "Repetition, irrelevant questions and semantic consent require conversation review.",
    ]
    if not stats:
        unknown.append(
            "This attempt has no transport statistics; historical evidence is unchanged."
        )
    observed_completion = (
        "incomplete"
        if required_report and not report
        else "completed"
        if pipeline.get("conversation_accepted")
        else "unresolved"
    )
    return {
        "version": "conversation-diagnostics-v1",
        "simulation_validity": evaluation.get("validity", "unresolved"),
        "automated_target_outcome": evaluation.get("outcome", "unresolved"),
        "observed_task_completion": observed_completion,
        "observed_completion_boundary": "Required task outputs received by the harness; "
        "this is not a causal target grade.",
        "private_report_required": required_report,
        "private_report_received": bool(report),
        "recorded_bookings": len(state.get("bookings", [])),
        "symptoms": symptoms,
        "established_failure_owner": execution.get("attribution", "unknown"),
        "failure_owner_source": "result.json; transport observations never infer ownership",
        "last_completed_step": next(
            (
                anchor(e)
                for e in reversed(progress)
                if e["kind"] not in {"target_speech_detected", "response_created"}
            ),
            None,
        ),
        "last_observed_steps": last,
        "event_anchors": [anchor(e) for e in decisive],
        "transport": {
            "status": "observed" if stats else "unavailable",
            "tracks": list(groups.values()),
            "lifecycle": [
                anchor(e) for e in transport if e["payload"].get("name") != "audio_transport_stats"
            ],
        },
        "target_generation": generation,
        "audio_references": [
            name
            for name in ("audio/played.wav", "audio/received.wav")
            if (directory / name).exists()
        ],
        "silence_intervals": pipeline.get("conversation_timing", {}).get("long_silence_intervals"),
        "human_listening_review": False,
        "remaining_uncertainty": unknown,
    }
