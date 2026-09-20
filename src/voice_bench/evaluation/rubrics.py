"""Explicit, versioned status rubrics; no implicit numeric or boolean conversion."""

from typing import Literal

from pydantic import Field, model_validator

from voice_bench.models import Contract


class MetricDefinition(Contract):
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    method: Literal["code", "human"]
    role: Literal["requirement", "validity", "prerequisite", "diagnostic"]
    applies: bool = True
    applicability_reason: str = Field(min_length=1)
    required_evidence: tuple[str, ...] = Field(min_length=1)
    pass_rule: str = Field(min_length=1)
    missing_evidence: Literal["uncertain"] = "uncertain"

    @model_validator(mode="after")
    def safe_evidence_names(self):
        if any(
            name.startswith("/") or ".." in name.split("/") or "\\" in name
            for name in self.required_evidence
        ):
            raise ValueError("Evidence requirements must be relative artifact names")
        return self


class EvaluationRubric(Contract):
    version: str = Field(min_length=1)
    metrics: tuple[MetricDefinition, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def unique_metrics(self):
        names = [m.name for m in self.metrics]
        if len(names) != len(set(names)):
            raise ValueError("Rubric metric names must be unique")
        if not any(m.applies and m.role == "requirement" for m in self.metrics):
            raise ValueError("A rubric needs an applicable task requirement")
        return self


def apply_rubric(rubric, metrics, validity, *, reviewed=False):
    """Interpret cited checks; callers validate citation hashes against the sealed bundle."""
    names = [m.name for m in metrics]
    if len(names) != len(set(names)):
        raise ValueError("Metric results must be unique")
    by_name = {m.name: m for m in metrics}
    decisions = []
    for definition in rubric.metrics:
        metric = by_name.get(definition.name)
        status, reason = "uncertain", "Required measurement is missing"
        if not definition.applies:
            status, reason = "not_applicable", definition.applicability_reason
        elif metric is not None:
            status, reason = metric.status, metric.explanation
            cited = {ref.artifact_key.split("/", 2)[-1] for ref in metric.evidence}
            if status == "not_applicable":
                status, reason = "uncertain", "Applicable metrics cannot be skipped"
            elif status in {"met", "not_met"}:
                if not set(definition.required_evidence).issubset(cited):
                    status, reason = "uncertain", "Required evidence was not cited"
                elif definition.method == "human" and not reviewed:
                    status, reason = "uncertain", "Listening or human review is required"
        decisions.append(
            {"name": definition.name, "role": definition.role, "status": status, "reason": reason}
        )
    active = [d for d in decisions if d["status"] != "not_applicable"]
    quality = [d for d in active if d["role"] == "validity"]
    prerequisites = [d for d in active if d["role"] == "prerequisite"]
    requirements = [d for d in active if d["role"] == "requirement"]
    if any(d["status"] == "not_met" for d in quality):
        validity = "invalid"
    elif validity != "invalid" and any(d["status"] != "met" for d in quality):
        validity = "unresolved"
    outcome = "unresolved"
    if validity == "valid" and all(d["status"] == "met" for d in prerequisites):
        if any(d["status"] == "not_met" for d in requirements):
            outcome = "failed"
        elif all(d["status"] == "met" for d in requirements):
            outcome = "passed"
    # Preserve core checks even when a custom rubric omits them. Declared checks use
    # their evidence-normalized decision; undeclared checks need the known artifact.
    core_evidence = {
        "task_state": {"business/final.json", "config/case.json"},
        "policy_actions": {"business/audit.json"},
        "duplicate_effects": {"business/audit.json"},
        "call_reliability": {"result.json"},
    }
    decision_by_name = {d["name"]: d for d in decisions}

    def core_failure(metric):
        if metric.name not in core_evidence or metric.status != "not_met":
            return False
        if metric.name in decision_by_name:
            return decision_by_name[metric.name]["status"] == "not_met"
        return core_evidence[metric.name].issubset(
            {ref.artifact_key.split("/", 2)[-1] for ref in metric.evidence}
        )

    if (
        validity == "valid"
        and all(d["status"] == "met" for d in prerequisites)
        and any(core_failure(m) for m in metrics)
    ):
        outcome = "failed"
    if any(m.name == "evidence_completeness" and m.status == "uncertain" for m in metrics):
        outcome = "unresolved"
    if (
        by_name.get("execution_reliability")
        and by_name["execution_reliability"].status == "not_met"
    ):
        if not by_name.get("call_reliability") or by_name["call_reliability"].status != "not_met":
            outcome = "unresolved"
    return {
        "rubric_version": rubric.version,
        "validity": validity,
        "outcome": outcome,
        "metric_decisions": decisions,
    }
