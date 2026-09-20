"""Synthetic, provider-free checks of profile isolation and grading semantics."""

import asyncio
import json
from copy import deepcopy
from uuid import uuid4

import pytest
from test_caller import Session, Socket, caller
from test_reservations import bundle, human_review
from test_reservations import custom_case as custom_case
from test_reservations import inventory as inventory
from test_restaurant_hard import challenge
from test_restaurant_hard import variant_specs as variant_specs

from voice_bench.caller.conversation_events import ConversationEventDriver
from voice_bench.cli import dispatch, parser
from voice_bench.contracts import ExecutionCase
from voice_bench.design import prepare_case
from voice_bench.errors import CallerFailure
from voice_bench.evaluation.rubrics import EvaluationRubric, MetricDefinition, apply_rubric
from voice_bench.evaluation.scoring import import_review, save_evaluation
from voice_bench.evidence.local import LocalEvidence
from voice_bench.models import EvidenceRef, MetricResult
from voice_bench.restaurant_case import import_case
from voice_bench.restaurant_hard_cases import convert_variants
from voice_bench.scenarios import ScenarioPolicy, effective_counterpart


@pytest.mark.parametrize("profile", ["straightforward", "concise", "clarification_seeking"])
def test_profile_preserves_task_state_permissions_and_source(custom_case, profile):
    source = import_case(*custom_case)
    before = deepcopy(source.model_dump(mode="json"))
    case = prepare_case(source, profile)
    assert source.model_dump(mode="json") == before
    assert case.case_id == source.case_id and case.version != source.version
    for name in ("user_task", "initial_state", "target_tools", "counterpart_tools", "counterpart"):
        assert getattr(case, name) == getattr(source, name)
    brief = effective_counterpart(case.counterpart, case.counterpart_profile, case.scenario_policy)
    assert "User-only" not in brief.model_dump_json()
    assert "Evaluator-only" not in brief.model_dump_json()
    assert brief.known_facts == source.counterpart.known_facts
    assert "never" in brief.model_dump_json().lower()
    definitions = {m.name: m for m in case.evaluation_rubric.metrics}
    assert not definitions["negotiation_behavior"].applies
    assert not definitions["dietary_understanding"].applies
    assert definitions["counterpart_validity"].role == "validity"
    assert ExecutionCase.model_validate_json(case.model_dump_json()) == case
    with pytest.raises(ValueError, match="already prepared"):
        prepare_case(case, profile)


def test_preparation_rejects_unknown_or_dropped_required_metrics(custom_case):
    case = import_case(*custom_case)
    case.criteria["required_metrics"].append("undefined_measurement")
    with pytest.raises(ValueError, match="Undefined"):
        prepare_case(case, "concise")
    case.criteria["required_metrics"].pop()
    data = prepare_case(case, "concise").model_dump(mode="json")
    data["evaluation_rubric"]["metrics"] = [
        m for m in data["evaluation_rubric"]["metrics"] if m["name"] != "policy_actions"
    ]
    with pytest.raises(ValueError, match="exactly"):
        ExecutionCase.model_validate(data)


def test_hard_variants_keep_events_and_capability_applicability(variant_specs):
    for index, source in enumerate(convert_variants(*variant_specs)):
        case = prepare_case(source, "concise")
        assert case.conversation_events == source.conversation_events
        assert case.criteria["reservation_expected"] == source.criteria["reservation_expected"]
        definitions = {m.name: m for m in case.evaluation_rubric.metrics}
        assert definitions["negotiation_behavior"].applies == (index > 0)
        assert definitions["dietary_understanding"].applies == (index == 2)


def test_cli_prepares_without_overwriting_source_or_existing_output(custom_case, tmp_path):
    source = tmp_path / "input.json"
    source.write_text(json.dumps([import_case(*custom_case).model_dump(mode="json")]))
    original = source.read_bytes()
    output = tmp_path / "prepared.json"
    args = parser().parse_args(
        [
            "design",
            "prepare",
            "--cases",
            str(source),
            "--profile",
            "concise",
            "--output",
            str(output),
        ]
    )
    result = dispatch(args)
    assert result["provider_calls"] == result["live_attempts"] == 0
    assert source.read_bytes() == original
    assert json.loads(output.read_text())[0]["counterpart_profile"]["profile_id"] == "concise"
    with pytest.raises(FileExistsError):
        dispatch(args)


def definition(name="task", **changes):
    return MetricDefinition.model_validate(
        {
            "name": name,
            "description": "Synthetic check",
            "method": "code",
            "role": "requirement",
            "applicability_reason": "Synthetic requirement",
            "required_evidence": ["business/final.json"],
            "pass_rule": "Expected state",
            **changes,
        }
    )


def metric(name="task", status="met", evidence="business/final.json"):
    return MetricResult(
        name=name,
        status=status,
        explanation="Synthetic evidence-backed judgment",
        evidence=(EvidenceRef(artifact_key=f"batch/run/{evidence}", sha256="a" * 64),),
    )


@pytest.mark.parametrize(
    "status,expected",
    [
        ("met", "passed"),
        ("not_met", "failed"),
        ("uncertain", "unresolved"),
        ("not_applicable", "unresolved"),
    ],
)
def test_explicit_status_rules(status, expected):
    rubric = EvaluationRubric(version="test", metrics=(definition(),))
    assert apply_rubric(rubric, [metric(status=status)], "valid")["outcome"] == expected
    assert apply_rubric(rubric, [], "valid")["outcome"] == "unresolved"
    assert apply_rubric(rubric, [metric(evidence="other.json")], "valid")["outcome"] == "unresolved"


def test_not_applicable_is_declared_and_human_checks_need_review():
    rubric = EvaluationRubric(
        version="test",
        metrics=(
            definition(method="human"),
            definition("unused", applies=False),
        ),
    )
    assert apply_rubric(rubric, [metric()], "valid")["outcome"] == "unresolved"
    result = apply_rubric(rubric, [metric()], "valid", reviewed=True)
    assert result["outcome"] == "passed"
    assert result["metric_decisions"][1]["status"] == "not_applicable"


@pytest.mark.parametrize(
    "quality,validity", [("met", "valid"), ("not_met", "invalid"), ("uncertain", "unresolved")]
)
def test_simulator_validity_is_separate_from_task_failure(quality, validity):
    rubric = EvaluationRubric(
        version="test",
        metrics=(
            definition(),
            definition("simulator", role="validity"),
        ),
    )
    result = apply_rubric(rubric, [metric(status="not_met"), metric("simulator", quality)], "valid")
    assert result["validity"] == validity
    assert result["outcome"] == ("failed" if validity == "valid" else "unresolved")


def test_missing_prerequisite_and_valid_target_drop():
    rubric = EvaluationRubric(
        version="test",
        metrics=(
            definition(),
            definition("delivery", role="prerequisite"),
        ),
    )
    checks = [metric(), metric("call_reliability", "not_met", "result.json")]
    assert apply_rubric(rubric, checks, "valid")["outcome"] == "unresolved"
    checks.append(metric("delivery"))
    assert apply_rubric(rubric, checks, "valid")["outcome"] == "failed"


def test_custom_rubric_cannot_hide_a_supported_forbidden_attempt():
    rubric = EvaluationRubric(version="test", metrics=(definition(),))
    checks = [metric(), metric("policy_actions", "not_met", "business/audit.json")]
    assert apply_rubric(rubric, checks, "valid")["outcome"] == "failed"
    declared = EvaluationRubric(version="test", metrics=(definition("task_state"),))
    result = apply_rubric(declared, [metric("task_state", "not_met", "unrelated.json")], "valid")
    assert result["outcome"] == "unresolved"


@pytest.mark.asyncio
async def test_event_conflict_rejection_and_stable_priority(tmp_path):
    events = [challenge("low"), challenge("high").model_copy(update={"priority": 2})]
    driver = ConversationEventDriver(events, ScenarioPolicy())
    driver.after_tool("check_availability", {"ok": True}, "availability")
    with pytest.raises(CallerFailure, match="compete"):
        driver.after_tool("prepare_confirmation", {"ok": True}, "confirmation")
    assert not driver.pending
    driver = ConversationEventDriver(events, ScenarioPolicy(event_conflicts="priority_order"))
    driver.after_tool("check_availability", {"ok": True}, "availability")
    driver.after_tool("prepare_confirmation", {"ok": True}, "confirmation")
    driver.after_tool("prepare_confirmation", {"ok": True}, "confirmation")
    evidence = LocalEvidence(tmp_path, uuid4(), uuid4())
    try:
        for expected in ("high", "low"):
            request = await driver.response_request(evidence, "Only counterpart facts")
            assert request["response"]["metadata"]["conversation_event_id"] == expected
        assert not driver.pending
        driver.after_tool("prepare_confirmation", {"ok": True}, "new-confirmation")
        assert not driver.pending  # One-time events stay one-time.
    finally:
        evidence.close_writer()


def test_event_queue_is_bounded():
    driver = ConversationEventDriver(
        [challenge("one"), challenge("two")],
        ScenarioPolicy(event_conflicts="priority_order", max_pending_events=1),
    )
    driver.after_tool("check_availability", {"ok": True})
    with pytest.raises(CallerFailure, match="bound"):
        driver.after_tool("prepare_confirmation", {"ok": True})


@pytest.mark.asyncio
async def test_profile_reaches_simulator_without_private_task(custom_case, tmp_path):
    case = prepare_case(import_case(*custom_case), "concise")
    brief = effective_counterpart(case.counterpart, case.counterpart_profile, case.scenario_policy)
    evidence = LocalEvidence(tmp_path, uuid4(), uuid4())
    socket, session = Socket(), Session(evidence, 24000)
    task = asyncio.create_task(
        caller(socket).converse(
            None, brief, session, evidence, scenario_policy=case.scenario_policy
        )
    )
    try:
        async with asyncio.timeout(5):
            update = await socket.sent.get()
            instructions = update["session"]["instructions"]
            assert "Give brief answers" in instructions
            assert "User-only" not in instructions and "Evaluator-only" not in instructions
    finally:
        task.cancel()
        await asyncio.gather(task, return_exceptions=True)
        await session.close("test")
        evidence.close_writer()


@pytest.mark.asyncio
async def test_prepared_case_grades_and_human_review_enforces_frozen_rubric(
    custom_case, inventory, tmp_path
):
    case = prepare_case(import_case(*custom_case), "straightforward")
    directory, result = await bundle(tmp_path, case, inventory)
    original_manifest = (directory / "manifest.json").read_bytes()
    assert result["outcome"] == "unresolved"
    assert result["rubric_version"] == "restaurant-status-v1"
    assert any(
        d["name"] == "counterpart_validity" and d["status"] == "uncertain"
        for d in result["metric_decisions"]
    )
    review = human_review(directory)
    path = import_review(directory, "review-v1", review)
    assert json.loads(path.read_text())["outcome"] == "passed"
    assert (directory / "manifest.json").read_bytes() == original_manifest
    review["checks"] = [c for c in review["checks"] if c["name"] != "consent_alignment"]
    with pytest.raises(ValueError, match="human check"):
        import_review(directory, "incomplete", review)
    with pytest.raises(FileExistsError):
        save_evaluation(directory, "rules-v1", [], validity="valid")


@pytest.mark.asyncio
@pytest.mark.parametrize("invalid", [False, True])
async def test_new_rubric_separates_valid_failure_from_invalid_simulator(
    custom_case, inventory, tmp_path, invalid
):
    case = prepare_case(import_case(*custom_case), "concise")
    directory, _ = await bundle(tmp_path, case, inventory, option="0")
    review = human_review(directory, outcome="failed", invalid=invalid)
    result = json.loads(import_review(directory, "review-v1", review).read_text())
    assert result["validity"] == ("invalid" if invalid else "valid")
    assert result["outcome"] == ("unresolved" if invalid else "failed")


def test_callback_rubric_uses_authenticated_report_artifacts(custom_case):
    from voice_bench.evaluation.catalog import restaurant_rubric

    source = import_case(*custom_case)
    source.criteria["user_report_source"] = "target_callback"
    rubric = restaurant_rubric(source)
    metrics = {m.name: m for m in rubric.metrics}
    assert rubric.version == "restaurant-status-callback-v1"
    assert metrics["user_report_presence"].method == "code"
    assert set(metrics["user_report_presence"].required_evidence) == {
        "target/user-report.json",
        "target/task-delivery.json",
        "target/report-requests.json",
    }
    assert metrics["user_report_accuracy"].required_evidence == (
        "target/user-report.json",
        "business/final.json",
    )
    source.criteria.pop("user_report_source")
    assert restaurant_rubric(source).version == "restaurant-status-v1"
