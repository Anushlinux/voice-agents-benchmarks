import json
from uuid import uuid4

import pytest

from voice_bench.batches import export_report, finalize_batch, make_plan, recover, report
from voice_bench.evaluation.scoring import (
    deterministic,
    import_review,
    save_evaluation,
    summarize,
    validate_reference,
)
from voice_bench.evidence.local import LocalEvidence
from voice_bench.fixture import execute_fixture, fixture_case
from voice_bench.models import EvidenceRef, MetricResult


@pytest.mark.asyncio
async def test_fixture_and_scoring_cannot_turn_forbidden_action_into_pass(store, tmp_path):
    fixture = await execute_fixture(store, tmp_path)
    directory = tmp_path / fixture["batch_id"] / fixture["run_ids"][0]
    metrics = deterministic(directory)
    by_name = {m.name: m for m in metrics}
    assert by_name["task_state"].status == "met"
    assert by_name["policy_actions"].status == "not_met"
    assert summarize(metrics, "valid", ["task_state"]) == "failed"
    assert summarize(metrics, "invalid", ["task_state"]) == "unresolved"
    path = save_evaluation(directory, "v1", metrics, validity="valid")
    assert json.loads(path.read_text())["outcome"] == "failed"
    with pytest.raises(FileExistsError):
        save_evaluation(directory, "v1", metrics)
    with pytest.raises(ValueError, match="sealed"):
        validate_reference(directory, EvidenceRef(artifact_key="another/run/file", sha256="a" * 64))
    event_ref = EvidenceRef(
        artifact_key=f"{fixture['batch_id']}/{fixture['run_ids'][0]}/events.jsonl",
        sha256=next(r.sha256 for m in metrics for r in m.evidence),
    )
    with pytest.raises(ValueError):
        validate_reference(directory, event_ref)
    review = {
        "reviewer": "tester",
        "evaluation_version": "v1",
        "validity": "valid",
        "outcome": "failed",
        "explanation": "Reviewed the rejected action.",
        "evidence": [by_name["policy_actions"].evidence[0].model_dump(mode="json")],
    }
    result = import_review(directory, "review-1", review)
    assert not json.loads(result.read_text())["disagrees"]


def test_valid_target_drop_is_failure_even_if_task_completed():
    ref = EvidenceRef(artifact_key="result.json", sha256="a" * 64)
    metrics = [
        MetricResult(name="task_state", status="met", explanation="State correct", evidence=(ref,)),
        MetricResult(
            name="call_reliability", status="not_met", explanation="Target drop", evidence=(ref,)
        ),
    ]
    assert summarize(metrics, "valid", ["task_state"]) == "failed"


def test_batch_plan_pairs_channels_and_repetitions():
    batch_id = uuid4()
    first = make_plan([fixture_case()], ["browser", "phone"], 3, 7, batch_id)
    second = make_plan([fixture_case()], ["browser", "phone"], 3, 7, batch_id)
    assert first == second and len(first) == 6
    assert len({p.plan_id for p in first}) == 6
    for repetition in range(1, 4):
        assert {p.channel for p in first if p.repetition == repetition} == {"browser", "phone"}


def test_report_accounts_for_not_run_and_all_attempts(store, prepared, tmp_path):
    plans, (first, _) = prepared
    store.update_run(
        first,
        dispatch_intent=True,
        connected=True,
        termination_confirmed=True,
        result={"validity": "valid", "outcome": "failed"},
    )
    result = report(store, plans[0].batch_id, tmp_path)
    assert result["counts"]["planned"] == 2
    assert result["counts"]["attempted"] == 1
    assert result["counts"]["not_run"] == 1
    assert result["counts"]["failed"] == 1
    assert result["pass_rate"]["denominator"] == 1
    export_report(result, tmp_path / "report")
    assert (tmp_path / "report/attempts.csv").exists()


@pytest.mark.asyncio
async def test_recovery_never_redials_and_preserves_sealed_evidence(store, prepared, tmp_path):
    plans, (first, second) = prepared
    store.update_run(first, dispatch_intent=True, phase="connecting")
    store.bind("rumik", "known", first)
    store.update_run(second, termination_confirmed=True, evidence_sealed=True)
    evidence = LocalEvidence(tmp_path, plans[0].batch_id, first)
    await evidence.json("source.json", {"original": True})
    await evidence.finalize(first)
    before = (evidence.directory / "manifest.json").read_bytes()

    class Target:
        async def call(self, call_id):
            assert call_id == "known"
            return {"status": "completed"}

    result = await recover(store, plans[0].batch_id, tmp_path, Target())
    assert result == [{"run_id": str(first), "termination_confirmed": True}]
    assert (evidence.directory / "manifest.json").read_bytes() == before
    assert store.run(first)["evidence_sealed"]


@pytest.mark.asyncio
async def test_phone_recovery_holds_unknown_carrier_and_preserves_torn_log(
    store, prepared, tmp_path
):
    plans, (first, second) = prepared
    context = store.run(first)["context"] | {"channel": "phone"}
    store.update_run(first, dispatch_intent=True, context=context)
    store.update_run(second, termination_confirmed=True, evidence_sealed=True)
    store.bind("rumik", "known", first)
    evidence = LocalEvidence(tmp_path, plans[0].batch_id, first)
    torn = b'{"sequence":0,"partial":'
    (evidence.directory / "events.jsonl").write_bytes(torn)
    evidence.close_writer()  # Simulate the old process exiting before recovery.

    class Target:
        async def call(self, call_id):
            return {"status": "completed"}

    result = await recover(store, plans[0].batch_id, tmp_path, Target())
    assert not result[0]["termination_confirmed"]
    assert (evidence.directory / "events.jsonl").read_bytes() == torn
    manifest = json.loads((evidence.directory / "manifest.json").read_text())
    assert manifest["integrity_issues"] == ["event_log_incomplete_or_invalid"]


def test_batch_finalization_requires_shutdown_and_records_coverage_gaps(store, prepared, tmp_path):
    plans, ids = prepared
    batch_id = plans[0].batch_id
    with pytest.raises(ValueError, match="shutdown"):
        finalize_batch(store, batch_id, tmp_path, "v1")
    with store.locked_batch(batch_id) as (_, batch):
        batch["completion"] = {"worker_stopped": True}
    with pytest.raises(ValueError, match="Reconcile"):
        finalize_batch(store, batch_id, tmp_path, "v1")
    for run_id in ids:
        store.update_run(run_id, termination_confirmed=True, evidence_sealed=True)
    result = finalize_batch(store, batch_id, tmp_path, "v1")
    assert result["status"] == "finalized_with_gaps"
    assert result["counts"]["not_run"] == 2
    with pytest.raises(FileExistsError):
        finalize_batch(store, batch_id, tmp_path, "v1")


@pytest.mark.asyncio
async def test_phone_recovery_accepts_final_cdr_without_call_status(store, prepared, tmp_path):
    plans, (first, second) = prepared
    store.update_run(
        first, dispatch_intent=True, context=store.run(first)["context"] | {"channel": "phone"}
    )
    store.update_run(second, termination_confirmed=True, evidence_sealed=True)
    store.bind("plivo", "rejected-call", first)
    evidence = LocalEvidence(tmp_path, plans[0].batch_id, first)
    await evidence.json("source.json", {"original": True})
    await evidence.finalize(first)
    original_manifest = (evidence.directory / "manifest.json").read_bytes()

    class Carrier:
        async def hangup(self, call_id):
            assert call_id == "rejected-call"

        async def call(self, call_id):
            return {
                "call_uuid": call_id,
                "hangup_cause_name": "Rejected",
                "hangup_cause_code": 3020,
                "end_time": "2026-09-22 06:55:12+00:00",
            }

    result = await recover(store, plans[0].batch_id, tmp_path, None, Carrier())
    assert result == [{"run_id": str(first), "termination_confirmed": True}]
    assert (evidence.directory / "manifest.json").read_bytes() == original_manifest
