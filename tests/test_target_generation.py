import json

from voice_bench.evaluation.target_generation import target_generation_diagnostics


def event(data, *, trusted=True):
    return {
        "kind": "target_text_observation",
        "sequence": 12,
        "clock_id": "chromium-audio-context",
        "payload": {
            "remote_audio_participant": trusted,
            "audio_context_seconds": 8.5,
            "text": json.dumps({"label": "rtvi-ai", "type": "metrics", "data": data}),
        },
    }


def test_saved_reasoning_only_signature_does_not_invent_limit_or_spoken_output():
    result = target_generation_diagnostics(
        [event({"tokens": [{"completion_tokens": 400, "reasoning_tokens": 397}]})]
    )
    assert result["reasoning_dominated_samples"] == 1
    assert result["usage_samples"][0]["non_reasoning_tokens"] == 3
    assert result["usage_samples"][0]["sequence"] == 12
    assert "max_completion_tokens" not in result
    assert "do not prove" in result["interpretation"]


def test_missing_malformed_untrusted_and_capped_telemetry_remains_unknown():
    rows = [
        event({"tokens": [{"completion_tokens": 400, "reasoning_tokens": 397}]}, trusted=False),
        event({"tokens": [{"completion_tokens": 3, "reasoning_tokens": 400}]}),
        event({"tokens": [{"completion_tokens": True, "reasoning_tokens": 0}]}),
        event({"tokens": [{"completion_tokens": 400}]}),
        event({"tokens": None}),
        {"kind": "target_text_observation", "payload": {"kind": "capture_limit"}, "sequence": 20},
        event(None),
    ]
    result = target_generation_diagnostics(rows)
    assert result["status"] == "unavailable"
    assert not result["usage_samples"]
    assert result["capture_limits"] == [{"sequence": 20, "lane": "all"}]


def test_normal_answer_and_tool_budget_is_not_called_reasoning_starvation():
    result = target_generation_diagnostics(
        [event({"tokens": [{"completion_tokens": 400, "reasoning_tokens": 150}]})]
    )
    assert result["status"] == "observed"
    assert not result["reasoning_dominated_samples"]
