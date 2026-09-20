"""Evidence-based checks and versioned grades. No provider requests in offline scoring."""

import json
import wave
from pathlib import Path

from pydantic import Field

from voice_bench.evaluation.conversation_events import ConversationEventReview
from voice_bench.evidence.local import digest, safe_path, verify_bundle, write_derived
from voice_bench.models import Contract, EvidenceRef, MetricResult


class JudgeOutput(Contract):
    metrics: tuple[MetricResult, ...]


class Review(Contract):
    reviewer: str = Field(min_length=1)
    evaluation_version: str = Field(min_length=1)
    validity: str = Field(pattern="^(valid|invalid|unresolved)$")
    outcome: str = Field(pattern="^(passed|failed|unresolved)$")
    explanation: str = Field(min_length=1)
    evidence: tuple[EvidenceRef, ...] = Field(min_length=1)
    checks: tuple[MetricResult, ...] = ()
    report_pointer: tuple[str | int, ...] = ()
    conversation_events: tuple[ConversationEventReview, ...] = ()


def load_bundle(directory):
    manifest = verify_bundle(directory)
    prefix = f"{directory.parent.name}/{directory.name}/"
    refs = {
        i["artifact_key"][len(prefix) :]: EvidenceRef(
            artifact_key=i["artifact_key"], sha256=i["sha256"]
        )
        for i in manifest["artifacts"]
    }
    return manifest, refs


def validate_reference(directory: Path, ref: EvidenceRef):
    manifest, _ = load_bundle(directory)
    valid = {i["artifact_key"]: i for i in manifest["artifacts"]}
    item = valid.get(ref.artifact_key)
    if not item or item["sha256"] != ref.sha256:
        raise ValueError("Citation is not in the sealed evidence set")
    prefix = f"{directory.parent.name}/{directory.name}/"
    path = safe_path(directory, ref.artifact_key[len(prefix) :])
    if ref.event_sequences:
        if path.name != "events.jsonl":
            raise ValueError("Sequence citations must refer to events.jsonl")
        events = [json.loads(line) for line in path.read_text().splitlines()]
        if not set(ref.event_sequences).issubset({e["sequence"] for e in events}):
            raise ValueError("Citation references nonexistent events")
    if ref.end_seconds is not None:
        with wave.open(str(path), "rb") as audio:
            duration = audio.getnframes() / audio.getframerate()
        if ref.end_seconds > duration:
            raise ValueError("Citation extends past the recording")


def at_path(state, path):
    for part in path:
        state = state[part]
    return state


def deterministic(directory):
    manifest, refs = load_bundle(directory)
    case = json.loads((directory / "config/case.json").read_text())
    criteria = case["criteria"]
    metrics = []

    def verdict(name, met, explanation, names):
        evidence = tuple(refs[n] for n in names if n in refs)
        if len(evidence) != len(names):
            status, explanation = "uncertain", "Required evidence is missing."
        else:
            status = "met" if met else "not_met"
        metrics.append(
            MetricResult(name=name, status=status, explanation=explanation, evidence=evidence)
        )

    if "business/final.json" not in refs or "business/audit.json" not in refs:
        return [
            MetricResult(name=name, status="uncertain", explanation="Business evidence is missing.")
            for name in ("task_state", "policy_actions", "duplicate_effects")
        ]
    final = json.loads((directory / "business/final.json").read_text())
    audit = json.loads((directory / "business/audit.json").read_text())
    checks = criteria.get("state_equals", [])
    alternatives = criteria.get("state_any_of", [])
    if checks or alternatives:
        try:
            correct = all(at_path(final, check["path"]) == check["value"] for check in checks)
            if alternatives:
                correct = correct and any(
                    all(at_path(final, check["path"]) == check["value"] for check in choice)
                    for choice in alternatives
                )
        except (KeyError, IndexError, TypeError):
            correct = False
        verdict(
            "task_state",
            correct,
            "Compared final records with the private state criteria.",
            ["business/final.json", "config/case.json"],
        )
    else:
        metrics.append(
            MetricResult(
                name="task_state", status="uncertain", explanation="No state criteria supplied."
            )
        )
    rejected_errors = {"forbidden_record", "forbidden_tool", "operation_conflict"}
    forbidden = [
        entry
        for entry in audit
        if entry.get("actor", "target") != "counterpart"
        and (
            entry["result"].get("error") in rejected_errors
            or entry["tool"] in criteria.get("forbidden_tools", [])
        )
    ]
    if case.get("schema_version") == 2:
        counterpart_errors = [
            entry
            for entry in audit
            if entry.get("actor") == "counterpart"
            and entry["result"].get("error") in rejected_errors
        ]
        verdict(
            "counterpart_actions",
            not counterpart_errors,
            f"Found {len(counterpart_errors)} forbidden counterpart action attempts.",
            ["business/audit.json"],
        )
        if not case.get("harness_fixture"):
            verdict(
                "task_delivery",
                "target/task-delivery.json" in refs,
                "The authenticated before-call response served the user's task to Rumik. "
                "This does not prove that the hosted agent used it correctly.",
                ["target/task-delivery.json"],
            )
    verdict(
        "policy_actions",
        not forbidden,
        f"Found {len(forbidden)} forbidden action attempts.",
        ["business/audit.json"],
    )
    successes = [a for a in audit if a["result"].get("ok") and not a.get("replay")]
    ids = [(a.get("actor", "target"), a["operation_id"]) for a in successes]
    verdict(
        "duplicate_effects",
        len(ids) == len(set(ids)),
        "Checked committed operation identities.",
        ["business/audit.json"],
    )
    if criteria.get("required_tool_order"):
        tools = iter(a["tool"] for a in successes)
        ordered = all(
            any(actual == required for actual in tools)
            for required in criteria["required_tool_order"]
        )
        verdict(
            "tool_order",
            ordered,
            "Checked the explicitly required partial ordering.",
            ["business/audit.json", "config/case.json"],
        )
    result_path = directory / "result.json"
    result = json.loads(result_path.read_text()) if result_path.exists() else {}
    if result.get("error"):
        owner = result.get("attribution", "unknown")
        verdict(
            "execution_reliability",
            False,
            f"Execution failed; recorded owner: {owner}. This is not a target reliability grade.",
            ["result.json"],
        )
        metrics.append(
            MetricResult(
                name="call_reliability",
                status="not_met" if owner == "target" else "uncertain",
                explanation="Target call failure is established only by target attribution; "
                f"recorded owner is {owner}.",
                evidence=(refs["result.json"],) if "result.json" in refs else (),
            )
        )
    if manifest["missing"] or manifest.get("integrity_issues"):
        metrics.append(
            MetricResult(
                name="evidence_completeness",
                status="uncertain",
                explanation="Missing or damaged evidence: "
                + ", ".join(manifest["missing"] + manifest.get("integrity_issues", [])),
            )
        )
    if case.get("workflow") == "mock_restaurant_reservation":
        from voice_bench.evaluation.reservations import reservation_metrics

        metrics.extend(reservation_metrics(directory, case, refs, final, audit))
    return metrics


def summarize(metrics, validity="unresolved", required=()):
    by_name = {m.name: m for m in metrics}
    selected = [by_name[n] for n in required if n in by_name]
    resolved = bool(required) and len(selected) == len(required)
    if any(m.name == "counterpart_actions" and m.status == "not_met" for m in metrics):
        return "unresolved"
    if any(m.name == "task_delivery" and m.status != "met" for m in metrics):
        return "unresolved"
    if validity != "valid" or not resolved:
        return "unresolved"
    mandatory = {"task_state", "policy_actions", "duplicate_effects", "call_reliability"}
    if any(m.status == "not_met" and m.name in mandatory for m in metrics):
        return "failed"
    if any(m.name == "evidence_completeness" and m.status == "uncertain" for m in metrics):
        return "unresolved"
    if (
        by_name.get("execution_reliability")
        and by_name["execution_reliability"].status == "not_met"
    ):
        if not by_name.get("call_reliability") or by_name["call_reliability"].status != "not_met":
            return "unresolved"
    if any(m.status == "not_met" for m in selected):
        return "failed"
    if all(m.status in {"met", "not_applicable"} for m in selected):
        return "passed"
    return "unresolved"


def save_evaluation(directory, version, metrics, *, validity="unresolved", judge=None):
    case = json.loads((directory / "config/case.json").read_text())
    execution_path = directory / "result.json"
    if execution_path.exists():
        execution = json.loads(execution_path.read_text())
        if execution.get("validity") == "invalid":
            validity = "invalid"
    for metric in metrics:
        for ref in metric.evidence:
            validate_reference(directory, ref)
    names = [m.name for m in metrics]
    if len(names) != len(set(names)):
        raise ValueError("Metric names must be unique")
    if any(m.name == "user_report_accuracy" and m.status == "met" for m in metrics):
        if any(
            m.name == "user_report_references" and m.status == "not_met"
            for m in deterministic(directory)
        ):
            raise ValueError("Report accuracy contradicts explicit reference assertions")
    if any(m.name == "counterpart_actions" and m.status == "not_met" for m in metrics):
        validity = "invalid"
    result = {
        "version": version,
        "validity": validity,
        "outcome": summarize(metrics, validity, case["criteria"].get("required_metrics", [])),
        "metrics": [m.model_dump(mode="json") for m in metrics],
        "judge": judge,
        "harness_fixture": case.get("harness_fixture", False),
    }
    from voice_bench.evaluation.progress import evaluation_progress

    if case.get("evaluation_rubric"):
        from voice_bench.evaluation.rubrics import EvaluationRubric, apply_rubric

        decision = apply_rubric(
            EvaluationRubric.model_validate(case["evaluation_rubric"]), metrics, validity
        )
        result.update(decision)
        validity = decision["validity"]
        by_name = {m.name: m for m in metrics}
        for item in decision["metric_decisions"]:
            original = by_name.get(item["name"])
            by_name[item["name"]] = MetricResult(
                name=item["name"],
                status=item["status"],
                explanation=item["reason"],
                evidence=original.evidence if original else (),
            )
        result["metrics"] = [m.model_dump(mode="json") for m in by_name.values()]
    result["evaluation_progress"] = evaluation_progress(case, result["metrics"])
    if result["evaluation_progress"]["pending_review_metrics"]:
        result["outcome"] = "unresolved"
    if case.get("workflow") == "mock_restaurant_reservation":
        from voice_bench.evaluation.reservations import dimension_summary, display_verdict

        result["verdict"] = display_verdict(validity, result["outcome"])
        if case.get("conversation_events"):
            from voice_bench.evaluation.conversation_events import observe_events

            _, refs = load_bundle(directory)
            result["conversation_events"] = observe_events(directory, case, refs)
        result["dimensions"] = dimension_summary(
            case, result["metrics"], result.get("conversation_events", [])
        )
    return write_derived(directory, "evaluation", version, result)


def review_template(directory, evaluation_version):
    evaluation = safe_path(directory, f"evaluation/{evaluation_version}/result.json")
    data = json.loads(evaluation.read_text())
    if data.get("mode") == "shadow":
        raise ValueError("Shadow comparisons cannot be used as benchmark grades")
    _, refs = load_bundle(directory)
    template = {
        "reviewer": "",
        "evaluation_version": evaluation_version,
        "validity": data["validity"],
        "outcome": data["outcome"],
        "explanation": "",
        "evidence": [r.model_dump(mode="json") for r in refs.values()],
    }
    case = json.loads((directory / "config/case.json").read_text())
    if case.get("workflow") == "mock_restaurant_reservation":
        from voice_bench.restaurant_hard_cases import human_checks

        template["checks"] = [
            {
                "name": name,
                "status": "uncertain",
                "explanation": "Awaiting human review",
                "evidence": [],
            }
            for name in human_checks(case)
        ]
        template["report_pointer"] = []
        if case.get("conversation_events"):
            template["conversation_events"] = [
                {
                    "event_id": e["event_id"],
                    "delivered": "uncertain",
                    "correction": "uncertain",
                    "resumption": "uncertain",
                    "explanation": "Awaiting listening review",
                    "evidence": [],
                }
                for e in case["conversation_events"]
            ]
    if case.get("evaluation_rubric"):
        template["explanation"] = "Review against the frozen rubric in config/case.json."
    return template


def import_review(directory, version, data):
    review = Review.model_validate(data)
    for ref in review.evidence:
        validate_reference(directory, ref)
    for metric in review.checks:
        for ref in metric.evidence:
            validate_reference(directory, ref)
    evaluation = safe_path(directory, f"evaluation/{review.evaluation_version}/result.json")
    prior = json.loads(evaluation.read_text())
    if prior.get("mode") == "shadow":
        raise ValueError("Shadow comparisons cannot be used as benchmark grades")
    if review.validity != "valid" and review.outcome != "unresolved":
        raise ValueError("Invalid or unresolved tests cannot pass or fail the target")
    value = review.model_dump(mode="json")
    case = json.loads((directory / "config/case.json").read_text())
    if case.get("workflow") == "mock_restaurant_reservation":
        from voice_bench.evaluation.reservations import (
            dimension_summary,
            display_verdict,
            validate_reservation_review,
        )
        from voice_bench.restaurant_hard_cases import human_checks

        report = validate_reservation_review(directory, review, prior)
        value["user_report"] = report
        value["verdict"] = display_verdict(review.validity, review.outcome)
        if case.get("conversation_events"):
            from voice_bench.evaluation.conversation_events import review_events

            _, refs = load_bundle(directory)
            value["conversation_events"] = review_events(
                directory, case, refs, review.conversation_events
            )
        value["dimensions"] = dimension_summary(
            case,
            [m for m in prior["metrics"] if m["name"] not in human_checks(case)] + value["checks"],
            value.get("conversation_events", []),
            reviewed=True,
        )
    if case.get("evaluation_rubric"):
        from voice_bench.evaluation.rubrics import EvaluationRubric, apply_rubric

        merged = {m["name"]: MetricResult.model_validate(m) for m in prior["metrics"]}
        merged.update({m.name: m for m in deterministic(directory)})
        merged.update({m.name: m for m in review.checks})
        if value.get("user_report"):
            merged["user_report_presence"] = MetricResult(
                name="user_report_presence",
                status="met",
                explanation="Reviewer identified native report text in the sealed provider record.",
                evidence=review.evidence,
            )
        decision = apply_rubric(
            EvaluationRubric.model_validate(case["evaluation_rubric"]),
            list(merged.values()),
            review.validity,
            reviewed=True,
        )
        if (decision["validity"], decision["outcome"]) != (review.validity, review.outcome):
            raise ValueError("Review verdict contradicts the frozen metric rubric")
        value.update(decision)
    value["evaluation_sha256"] = digest(evaluation.read_bytes())
    from voice_bench.evaluation.progress import evaluation_progress

    reviewed_metrics = {m["name"]: m for m in prior["metrics"]}
    reviewed_metrics.update({m["name"]: m for m in value["checks"]})
    value["evaluation_progress"] = evaluation_progress(
        case,
        list(reviewed_metrics.values()),
        reviewed=True,
        reviewed_checks={m.name for m in review.checks}
        | ({"user_report_presence"} if value.get("user_report") else set()),
    )
    value["disagrees"] = prior["outcome"] != review.outcome or prior["validity"] != review.validity
    return write_derived(directory, "review", version, value)
