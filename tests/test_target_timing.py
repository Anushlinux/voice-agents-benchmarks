"""TTFT from Rumik's own lifecycle packets: same browser clock at both ends, no guessing."""

import json

import pytest

from voice_bench.evaluation.target_timing import generation_windows, measure


def packet(sequence, ms, kind, data=None, *, trusted=True):
    body = {"label": "rtvi-ai", "type": kind}
    if data is not None:
        body["data"] = data
    return {
        "kind": "target_text_observation",
        "sequence": sequence,
        "payload": {
            "kind": "data_packet",
            "remote_audio_participant": trusted,
            "performance_ms": ms,
            "audio_context_seconds": ms / 1000,
            "text": json.dumps(body),
        },
    }


def test_first_token_is_measured_from_rumiks_own_end_of_speech_packet():
    events = [
        packet(1, 1000, "user-stopped-speaking"),
        packet(2, 1010, "bot-llm-started"),
        packet(3, 1015, "bot-llm-text", {"text": ""}),
        packet(4, 1480, "bot-llm-text", {"text": "Namaste"}),
        packet(5, 1500, "bot-llm-text", {"text": ", kripya"}),
        packet(
            6,
            1600,
            "metrics",
            {
                "tokens": [{"completion_tokens": 211, "reasoning_tokens": 189}],
                "ttfb": [{"processor": "CerebrasLLMService#0", "value": 0.353}],
            },
        ),
        packet(7, 1605, "bot-llm-stopped"),
        packet(8, 1610, "bot-tts-started"),
        packet(9, 1900, "bot-started-speaking"),
    ]
    rows = generation_windows(events)
    assert len(rows) == 1
    row = rows[0]
    assert row["classification"] == "text"
    assert row["ttft_ms"] == pytest.approx(480)
    assert row["llm_started_to_first_text_ms"] == pytest.approx(470)
    assert row["user_stopped_to_bot_speaking_ms"] == pytest.approx(900)
    assert row["provider_llm_ttfb_ms"] == pytest.approx(353)
    assert row["usage"]["completion_tokens"] == 211
    assert row["chained_after_tool_call"] is False
    result = measure(events)
    assert result["status"] == "measured"
    assert result["ttft_ms"]["n"] == 1 and result["ttft_ms"]["p50"] == pytest.approx(480)
    assert result["completion_tokens"] == [211]


def test_interrupted_silent_and_tool_call_windows_are_kept_apart_from_ttft():
    events = [
        packet(1, 1000, "user-stopped-speaking"),
        packet(2, 1005, "bot-llm-started"),
        packet(3, 1200, "bot-interrupted"),
        packet(4, 1210, "bot-llm-stopped"),
        packet(5, 3000, "user-stopped-speaking"),
        packet(6, 3005, "bot-llm-started"),
        packet(
            7, 3700, "metrics", {"tokens": [{"completion_tokens": 400, "reasoning_tokens": 397}]}
        ),
        packet(8, 3705, "bot-llm-stopped"),
        packet(9, 9000, "user-stopped-speaking"),
        packet(10, 9005, "bot-llm-started"),
        packet(
            11, 9600, "metrics", {"tokens": [{"completion_tokens": 134, "reasoning_tokens": 108}]}
        ),
        packet(12, 9601, "llm-function-call-started"),
        packet(13, 9602, "bot-llm-stopped"),
        packet(14, 9700, "bot-llm-started"),
        packet(15, 9950, "bot-llm-text", {"text": "Thank you"}),
        packet(16, 9990, "bot-llm-stopped"),
    ]
    rows = generation_windows(events)
    assert [r["classification"] for r in rows] == [
        "interrupted_before_text",
        "completed_without_text",
        "tool_call_without_text",
        "text",
    ]
    assert rows[1]["usage"] == {
        "completion_tokens": 400,
        "reasoning_tokens": 397,
        "prompt_tokens": None,
    }
    assert rows[3]["chained_after_tool_call"] is True
    assert rows[3]["ttft_ms"] == pytest.approx(950)
    result = measure(events)
    assert result["counts"] == {
        "interrupted_before_text": 1,
        "completed_without_text": 1,
        "tool_call_without_text": 1,
        "text": 1,
    }
    assert result["ttft_ms"]["n"] == 1
    assert result["completion_tokens"] == [400, 134]


def test_untrusted_or_malformed_packets_and_missing_trigger_produce_no_latency():
    events = [
        packet(1, 100, "bot-llm-started"),
        packet(2, 300, "bot-llm-text", {"text": "hello"}),
        packet(3, 310, "bot-llm-stopped"),
        packet(4, 500, "user-stopped-speaking", trusted=False),
        {
            "kind": "target_text_observation",
            "sequence": 5,
            "payload": {
                "kind": "data_packet",
                "remote_audio_participant": True,
                "text": "not json",
            },
        },
        packet(6, 800, "bot-llm-started"),
        packet(7, 900, "bot-llm-text", {"text": 7}),
    ]
    rows = generation_windows(events)
    assert rows[0]["ttft_ms"] is None
    assert rows[0]["llm_started_to_first_text_ms"] == pytest.approx(200)
    assert rows[1]["ended"] == "unterminated" and rows[1]["produced_text"] is False
    assert measure([])["status"] == "unavailable"
    assert measure(events)["ttft_ms"]["n"] == 0
