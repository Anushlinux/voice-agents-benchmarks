"""Prepare opt-in benchmark design versions without rewriting source cases."""

from voice_bench.contracts import ExecutionCase
from voice_bench.evaluation.catalog import restaurant_rubric
from voice_bench.evidence.local import canonical, digest
from voice_bench.scenarios import CounterpartProfile, ScenarioPolicy


def prepare_case(case, profile_id):
    if case.counterpart_profile or case.scenario_policy or case.evaluation_rubric:
        raise ValueError("Prepare from an unmodified source case, not an already prepared variant")
    profile = CounterpartProfile(profile_id=profile_id)
    data = case.model_dump(mode="json")
    # Keep task identity stable; different profiles are versions, not new task coverage.
    data["version"] = f"{case.version}.design1.{profile.profile_id}"
    data["counterpart_profile"] = profile.model_dump(mode="json")
    data["scenario_policy"] = ScenarioPolicy().model_dump(mode="json")
    data["evaluation_rubric"] = restaurant_rubric(case).model_dump(mode="json")
    data["criteria"].setdefault("provenance", {})["design_source"] = {
        "case_id": case.case_id,
        "version": case.version,
        "sha256": digest(canonical(case.model_dump(mode="json"))),
    }
    return ExecutionCase.model_validate(data)
