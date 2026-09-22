import json
import struct
import wave

import pytest

from voice_bench.evaluation.phone_metrics import measure


def fixture(tmp_path, *, incomplete=False, gap=False):
    (tmp_path / "audio").mkdir()
    events = []

    def event(kind, seconds, payload):
        events.append(
            {
                "kind": kind,
                "payload": payload,
                "observed_monotonic_ns": int(seconds * 1e9),
                "sequence": len(events) + 1,
            }
        )

    event("audio_submitted", 0.1, {"item_id": "a"})
    event("playback_progress", 0.5, {"item_id": "a", "boundary": "carrier_checkpoint"})
    pcm = b""
    for i in range(100):
        # Speech starts at 0.8 seconds. Each block receipt is its end time.
        pcm += struct.pack("<h", 2000 if 40 <= i < 60 else 0) * 160
        event(
            "carrier_media",
            (i + 1) * 0.02,
            {"samples": 160, "chunk": i + (1 if gap and i >= 50 else 0)},
        )
    event(
        "counterpart_playback_summary",
        2,
        {"items": [{"item_id": "a", "generated_ms": 400, "played_ms": 200 if incomplete else 400}]},
    )
    with wave.open(str(tmp_path / "audio/received.wav"), "wb") as handle:
        handle.setparams((1, 2, 8000, 0, "NONE", "none"))
        handle.writeframes(pcm)
    (tmp_path / "events.jsonl").write_text("\n".join(json.dumps(e) for e in events))
    (tmp_path / "evaluation/auto-v2").mkdir(parents=True)
    (tmp_path / "evaluation/auto-v2/result.json").write_text(
        json.dumps(
            {
                "judge": {
                    "transcripts": [
                        {
                            "source": "audio/sent.wav",
                            "text": "book four",
                            "evidence": {"start_seconds": 0},
                        }
                    ]
                }
            }
        )
    )
    (tmp_path / "provider").mkdir()
    (tmp_path / "provider/rumik-call.json").write_text(
        json.dumps({"transcript": [{"role": "user", "content": "book five"}]})
    )
    return tmp_path


def test_phone_proxy_preserves_boundaries_and_wer_denominator(tmp_path):
    result = measure(fixture(tmp_path))
    assert result["ttft_ms"]["status"] == result["ttfs_ms"]["status"] == "unavailable"
    delay = result["response_delay_proxy"]["delay_ms"]
    assert delay["n"] == 1
    assert delay["p50"] == pytest.approx(300)
    assert result["wer"]["counts"]["reference_words"] == 2
    assert result["wer"]["counts"]["wer"] == 0.5


def test_incomplete_playback_cannot_score_full_submitted_transcript(tmp_path):
    result = measure(fixture(tmp_path, incomplete=True))
    assert result["wer"]["status"] == "unavailable"
    assert result["response_delay_proxy"]["delay_ms"]["n"] == 0
    assert result["response_delay_proxy"]["delay_ms"]["p95"] is None


def test_audio_gap_cannot_be_interpreted_as_silence(tmp_path):
    result = measure(fixture(tmp_path, gap=True))
    assert result["response_delay_proxy"]["status"] == "unavailable"


def test_standard_report_includes_phone_wer_without_fabricating_browser_timing(tmp_path):
    from voice_bench.evaluation.cohort_metrics import measure_attempt

    result = measure_attempt(fixture(tmp_path))
    assert result["wer"]["counts"]["wer"] == 0.5
    assert result["telephone"]["response_delay_proxy"]["delay_ms"]["n"] == 1
    assert result["response_timing"]["status"] == "unavailable"
    assert result["ttft"]["status"] == "unavailable"
