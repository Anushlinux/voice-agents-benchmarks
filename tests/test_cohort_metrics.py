import pytest

from voice_bench.evaluation.cohort_metrics import distribution, response_opportunities, word_errors


def test_word_error_denominator_insertions_and_empty_reference():
    score = word_errors("Book four guests at seven", "book five guests seven please")
    assert score["reference_words"] == 5
    assert score["errors"] == 3
    assert score["wer"] == pytest.approx(0.6)
    assert word_errors("", "hello")["wer"] is None
    assert word_errors("₹10,500 Nair", "10500 Nair")["wer"] != 0
    assert word_errors("नमस्ते", "namaste")["wer"] == 1


def test_quantiles_keep_observations_and_missing_values_separate():
    assert distribution([])["p95"] is None
    assert distribution(range(1, 101))["p90"] == 90
    assert distribution([100, 2000, 5000])["mean"] == pytest.approx(7100 / 3)


def test_item_boundaries_do_not_count_pauses_as_turns_or_censor_long_reply():
    items = [dict(item_id="a", generated_ms=4000, played_ms=4000, interrupted_by_target=False)]
    events = [dict(kind="counterpart_playback_summary", payload=dict(items=items))]
    events.append(
        dict(
            kind="playback_progress",
            clock_id="chromium-audio-context",
            payload=dict(item_id="a", sample=1000, samples=4000, rate=1000),
        )
    )
    activity = dict(
        status="measured",
        coverage_seconds=[0, 30],
        rms_threshold=500,
        speaker_activity=dict(counterpart=[[1, 2], [3, 4.9]], target=[[20, 21]]),
    )
    result = response_opportunities(events, activity)
    assert len(result["opportunities"]) == 1
    assert result["ttfs_ms"]["mean"] == pytest.approx(15100)
    items[0]["interrupted_by_target"] = True
    assert response_opportunities(events, activity)["counts"] == {"answered": 1}
    items[0]["played_ms"] = 3000
    assert response_opportunities(events, activity)["counts"] == {"interrupted_playback": 1}
    items[0].update(interrupted_by_target=False, played_ms=4000)
    activity["speaker_activity"]["target"] = []
    result = response_opportunities(events, activity)
    assert result["counts"] == {"no_observed_reply": 1}
    assert result["ttfs_ms"]["n"] == 0
    activity["speaker_activity"]["target"] = [[3.5, 4]]
    assert response_opportunities(events, activity)["counts"] == {"overlap": 1}
    items[0]["played_ms"] = 3000
    assert response_opportunities(events, activity)["counts"] == {"incomplete_playback": 1}
