import json
from types import SimpleNamespace
from uuid import uuid4

import pytest

from voice_bench.batches import report
from voice_bench.evaluation.progress import evaluation_progress
from voice_bench.evaluation.report_assertions import compare_references
from voice_bench.evaluation.scoring import deterministic, save_evaluation
from voice_bench.evaluation.timeline import audio_clock_spans
from voice_bench.evidence.local import LocalEvidence, canonical, digest, publish
from voice_bench.fixture import fixture_case


@pytest.mark.parametrize(
    "text,issued,status",
    [
        ("Reference: AB-73X91.", ["AB73X91"], "met"),
        ("Reference number: ab73x91.", ["AB-73X91"], "met"),
        ("Reference numbers provided: AB73 and X91.", ["AB-73X91"], "not_met"),
        ("Reference: AB73X92.", ["AB-73X91"], "not_met"),
        ("Reference numbers: AB73X91, CD42Z.", ["CD42Z", "AB-73X91"], "met"),
        ("Reference numbers: AB73X91 and AB73X91.", ["AB-73X91"], "not_met"),
        ("Reference: AB73X91.", [], "not_met"),
        ("Booking confirmed.", ["AB-73X91"], "uncertain"),
        ("Reference: AB73 then correction X91.", ["AB-73X91"], "uncertain"),
        ("Wrong reference: AB73. Correct reference: X91.", ["X91"], "uncertain"),
        ("Reference: AB73. Reference: X91.", ["AB-73X91"], "uncertain"),
        ("Reference: AB73 X91.", ["AB-73X91"], "uncertain"),
        # The live September 22 report: no colon, label opened by a comma.
        ("Reservation confirmed, reference SIM-441311", ["SIM-441311"], "met"),
        ("Reservation confirmed, reference SIM-441311.", ["SIM-441312"], "not_met"),
        ("Reference SIM441311.", ["SIM-441311"], "met"),
        ("Reference AB73 then correction X91.", ["AB-73X91"], "uncertain"),
        ("The reference was unclear, so nothing was booked.", [], "uncertain"),
    ],
)
def test_reference_regression_cases_preserve_assertions_and_uncertainty(text, issued, status):
    result = compare_references(text, [{"reference": r} for r in issued])
    assert result["comparison"] == status
    for clause in result["clauses"]:
        assert text[clause["start"] : clause["end"]] == clause["text"]
    # Extraction must not change when the answer changes.
    other = compare_references(text, [{"reference": "DIFFERENT3"}])
    assert other["clauses"] == result["clauses"]


def block(offset, sample, count=100, rate=100):
    return {
        "payload": {"recording_offset": offset, "sample": sample, "samples": count, "rate": rate}
    }


def test_audio_mapping_keeps_clock_gaps_and_rejects_missing_interiors():
    mapped = audio_clock_spans(50, 250, [block(0, 1000), block(100, 1100), block(200, 1600)], 100)
    assert mapped["spans"] == [
        {"start_seconds": 10.5, "end_seconds": 12.0},
        {"start_seconds": 16.0, "end_seconds": 16.5},
    ]
    assert (
        audio_clock_spans(0, 300, [block(0, 1000), block(200, 1200)], 100)["status"] == "uncertain"
    )
    assert (
        audio_clock_spans(0, 200, [block(0, 1000), block(100, 500)], 100)["status"] == "uncertain"
    )
    assert audio_clock_spans(0, 100, [block(0, 0, rate=200)], 100)["status"] == "uncertain"
    assert audio_clock_spans(0, 100, [], 100)["status"] == "uncertain"


def test_review_progress_does_not_treat_model_answers_as_human_review():
    case = {
        "criteria": {"required_metrics": ["consent"]},
        "evaluation_rubric": {
            "metrics": [
                {"name": "consent", "method": "human", "role": "requirement", "applies": True}
            ]
        },
    }
    metrics = [{"name": "consent", "status": "met"}]
    assert evaluation_progress(case, metrics)["status"] == "awaiting_required_review"
    assert (
        evaluation_progress(case, metrics, reviewed=True, reviewed_checks={"consent"})["status"]
        == "checks_resolved"
    )
    assert evaluation_progress(case, metrics, reviewed=True)["status"] == "awaiting_required_review"
    assert evaluation_progress(case, [], reviewed=True)["pending_metrics"] == ["consent"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "owner,expected",
    [
        ("harness", "uncertain"),
        ("simulator", "uncertain"),
        ("unknown", "uncertain"),
        ("target", "not_met"),
    ],
)
async def test_execution_failure_is_not_automatically_target_failure(tmp_path, owner, expected):
    evidence = LocalEvidence(tmp_path, uuid4(), uuid4())
    await evidence.json("config/case.json", fixture_case().model_dump(mode="json"))
    await evidence.json("business/final.json", {"note": "initial"})
    await evidence.json("business/audit.json", [])
    await evidence.json("result.json", {"error": "failure", "attribution": owner})
    await evidence.finalize(evidence.run_id)
    metrics = deterministic(evidence.directory)
    by_name = {m.name: m for m in metrics}
    assert by_name["call_reliability"].status == expected
    assert by_name["execution_reliability"].status == "not_met"


@pytest.mark.asyncio
async def test_selected_missing_evaluation_or_review_cannot_fall_back_to_pass(tmp_path):
    batch_id, run_id = uuid4(), uuid4()
    run = {
        "run_id": str(run_id),
        "plan_id": "p1",
        "context": {"case_id": "c1", "channel": "browser", "repetition": 1},
        "attempt": 1,
        "dispatch_intent": True,
        "connected": True,
        "termination_confirmed": True,
        "result": {"validity": "valid", "outcome": "passed"},
    }
    store = SimpleNamespace(batch=lambda _: {"plans": [{"plan_id": "p1"}]}, runs=lambda _: [run])
    result = report(store, batch_id, tmp_path, evaluation_version="missing")
    assert result["counts"]["passed"] == 0
    assert result["pass_rate"]["value"] is None
    assert result["attempts"][0]["evaluation_selection"]["evaluation"] == "missing"
    evidence = LocalEvidence(tmp_path, batch_id, run_id)
    await evidence.json("config/case.json", fixture_case().model_dump(mode="json"))
    await evidence.finalize(run_id)
    evaluation_path = save_evaluation(evidence.directory, "v1", [], validity="valid")
    result = report(store, batch_id, tmp_path, evaluation_version="v1", review_version="missing")
    assert result["attempts"][0]["evaluation_progress"]["status"] == "missing_selected_stage"
    review = {
        "evaluation_version": "v1",
        "evaluation_sha256": "0" * 64,
        "validity": "valid",
        "outcome": "passed",
    }
    publish(evidence.directory / "review/r1/result.json", canonical(review))
    with pytest.raises(ValueError, match="checksum"):
        report(store, batch_id, tmp_path, evaluation_version="v1", review_version="r1")
    review["evaluation_sha256"] = digest(evaluation_path.read_bytes())
    publish(evidence.directory / "review/r2/result.json", canonical(review))
    assert (
        report(store, batch_id, tmp_path, evaluation_version="v1", review_version="r2")["attempts"][
            0
        ]["evaluation_selection"]["review"]
        == "loaded"
    )
    with pytest.raises(ValueError, match="before"):
        report(store, batch_id, tmp_path, review_version="r2")


def test_benchmark_purpose_requires_frozen_rubric_before_provider_setup():
    from pathlib import Path

    from voice_bench.runtime import validate_live
    from voice_bench.settings import load_config

    config = load_config(Path("configs/local.toml"))
    assert config.purpose == "development"
    with pytest.raises(ValueError, match="frozen rubrics"):
        validate_live(config.model_copy(update={"purpose": "benchmark"}), [fixture_case()])


@pytest.mark.asyncio
async def test_unreviewed_legacy_human_metrics_cannot_make_completed_benchmark(tmp_path):
    from voice_bench.models import MetricResult

    evidence = LocalEvidence(tmp_path, uuid4(), uuid4())
    case = fixture_case().model_dump(mode="json")
    case["workflow"] = "mock_restaurant_reservation"
    case["criteria"] = {"required_metrics": ["consent_alignment"], "reservation_expected": {}}
    await evidence.json("config/case.json", case)
    ref = await evidence.json("business/final.json", {})
    await evidence.finalize(evidence.run_id)
    metric = MetricResult(
        name="consent_alignment", status="met", explanation="Model says consent", evidence=(ref,)
    )
    path = save_evaluation(evidence.directory, "unreviewed", [metric], validity="valid")
    result = json.loads(path.read_text())
    assert result["outcome"] == "unresolved"
    assert result["evaluation_progress"]["status"] == "awaiting_required_review"
