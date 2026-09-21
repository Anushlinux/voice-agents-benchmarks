"""Read passive target usage events without feeding them into either actor."""

import json


def target_generation_diagnostics(events):
    samples, models, capture_limits = [], set(), []
    for event in events:
        if event.get("kind") != "target_text_observation":
            continue
        payload = event.get("payload", {})
        if payload.get("kind") == "capture_limit":
            capture_limits.append(
                {"sequence": event.get("sequence"), "lane": payload.get("lane", "all")}
            )
        if payload.get("remote_audio_participant") is not True:
            continue
        try:
            packet = json.loads(payload.get("text", ""))
        except (ValueError, TypeError):
            continue
        if not isinstance(packet, dict) or packet.get("label") != "rtvi-ai":
            continue
        data = packet.get("data")
        if packet.get("type") != "metrics" or not isinstance(data, dict):
            continue
        for timing in data.get("ttfb", []) if isinstance(data.get("ttfb"), list) else []:
            if isinstance(timing, dict) and isinstance(timing.get("model"), str):
                models.add(timing["model"])
        for usage in data.get("tokens", []) if isinstance(data.get("tokens"), list) else []:
            if not isinstance(usage, dict):
                continue
            completion, reasoning = usage.get("completion_tokens"), usage.get("reasoning_tokens")
            if not (
                type(completion) is int and type(reasoning) is int and 0 <= reasoning <= completion
            ):
                continue
            samples.append(
                {
                    "artifact": "events.jsonl",
                    "sequence": event.get("sequence"),
                    "clock_id": event.get("clock_id"),
                    "audio_context_seconds": payload.get("audio_context_seconds"),
                    "completion_tokens": completion,
                    "reasoning_tokens": reasoning,
                    "non_reasoning_tokens": completion - reasoning,
                    # A symptom, not proof of finish_reason=length or audible output.
                    "reasoning_dominated": completion > 0
                    and reasoning / completion >= 0.98
                    and completion - reasoning <= 8,
                }
            )
    completions = [s["completion_tokens"] for s in samples]
    ceiling = max(completions) if completions else None
    return {
        "version": "target-generation-v1",
        "status": "observed" if samples else "unavailable",
        "boundary": "provider_reported_usage_received_by_browser",
        "models_observed": sorted(models),
        "usage_samples": samples,
        "reasoning_dominated_samples": sum(s["reasoning_dominated"] for s in samples),
        # Repeated identical maxima are the visible signature of a provider token limit.
        "max_completion_observed": ceiling,
        "samples_at_max_completion": sum(c == ceiling for c in completions),
        "capture_limits": capture_limits,
        "interpretation": (
            "Reasoning-dominated output can leave no useful spoken answer. Repeated completion "
            "counts suggest a budget boundary but do not prove the configured token limit. "
            "These events do not expose finish_reason, guarantee spoken delivery, or attribute "
            "every silent turn. Missing or capped telemetry is unknown, not zero generation."
        ),
    }
