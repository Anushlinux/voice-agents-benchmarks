"""Evidence-based checks and versioned grades. No provider requests in offline scoring."""

import json
import wave
from pathlib import Path

from pydantic import Field

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
    forbidden = [
        entry
        for entry in audit
        if entry["result"].get("error") in {"forbidden_record", "operation_conflict"}
        or entry["tool"] in criteria.get("forbidden_tools", [])
    ]
    verdict(
        "policy_actions",
        not forbidden,
        f"Found {len(forbidden)} forbidden action attempts.",
        ["business/audit.json"],
    )
    successes = [a for a in audit if a["result"].get("ok") and not a.get("replay")]
    ids = [a["operation_id"] for a in successes]
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
        verdict(
            "call_reliability",
            False,
            "Execution recorded a call or harness failure.",
            ["result.json"],
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
    return metrics


def summarize(metrics, validity="unresolved", required=()):
    by_name = {m.name: m for m in metrics}
    selected = [by_name[n] for n in required if n in by_name]
    resolved = bool(required) and len(selected) == len(required)
    if validity != "valid" or not resolved:
        return "unresolved"
    mandatory = {"task_state", "policy_actions", "duplicate_effects", "call_reliability"}
    if any(m.status == "not_met" and m.name in mandatory for m in metrics):
        return "failed"
    if any(m.name == "evidence_completeness" and m.status == "uncertain" for m in metrics):
        return "unresolved"
    if any(m.status == "not_met" for m in selected):
        return "failed"
    if all(m.status in {"met", "not_applicable"} for m in selected):
        return "passed"
    return "unresolved"


def save_evaluation(directory, version, metrics, *, validity="unresolved", judge=None):
    case = json.loads((directory / "config/case.json").read_text())
    for metric in metrics:
        for ref in metric.evidence:
            validate_reference(directory, ref)
    names = [m.name for m in metrics]
    if len(names) != len(set(names)):
        raise ValueError("Metric names must be unique")
    result = {
        "version": version,
        "validity": validity,
        "outcome": summarize(metrics, validity, case["criteria"].get("required_metrics", [])),
        "metrics": [m.model_dump(mode="json") for m in metrics],
        "judge": judge,
        "harness_fixture": case.get("harness_fixture", False),
    }
    return write_derived(directory, "evaluation", version, result)


def review_template(directory, evaluation_version):
    evaluation = safe_path(directory, f"evaluation/{evaluation_version}/result.json")
    data = json.loads(evaluation.read_text())
    _, refs = load_bundle(directory)
    return {
        "reviewer": "",
        "evaluation_version": evaluation_version,
        "validity": data["validity"],
        "outcome": data["outcome"],
        "explanation": "",
        "evidence": [r.model_dump(mode="json") for r in refs.values()],
    }


def import_review(directory, version, data):
    review = Review.model_validate(data)
    for ref in review.evidence:
        validate_reference(directory, ref)
    evaluation = safe_path(directory, f"evaluation/{review.evaluation_version}/result.json")
    prior = json.loads(evaluation.read_text())
    if review.validity != "valid" and review.outcome != "unresolved":
        raise ValueError("Invalid or unresolved tests cannot pass or fail the target")
    value = review.model_dump(mode="json")
    value["evaluation_sha256"] = digest(evaluation.read_bytes())
    value["disagrees"] = prior["outcome"] != review.outcome or prior["validity"] != review.validity
    return write_derived(directory, "review", version, value)
