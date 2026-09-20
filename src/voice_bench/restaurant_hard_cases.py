"""Offline conversion of three authored variants; dataset content stays outside Git."""

import json
from copy import deepcopy

from voice_bench.business.dining import DiningWorkflow
from voice_bench.contracts import ExecutionCase
from voice_bench.evidence.local import canonical, digest, publish
from voice_bench.models import CounterpartBrief, UserTask
from voice_bench.restaurant_case import CASE_ID, HUMAN_CHECKS, RULE_CHECKS, pilot_blockers

HARD_IDS = tuple(CASE_ID + "_hard_" + str(n) for n in (1, 2, 3))


def human_checks(case):
    checks = list(HUMAN_CHECKS)
    if case.get("workflow_version") == "2":
        expected = case["criteria"]["reservation_expected"]
        if expected["dining_total_inr"]:
            checks.append("negotiation_behavior")
        if expected["without_onion_garlic_guests"]:
            checks.append("dietary_understanding")
    return tuple(checks)


def convert_variants(baseline, specifications):
    base = ExecutionCase.model_validate(baseline)
    if base.case_id != CASE_ID or base.workflow_version != "1":
        raise ValueError("Use the unchanged selected baseline")
    if not isinstance(specifications, list) or [s.get("case_id") for s in specifications] != list(
        HARD_IDS
    ):
        raise ValueError("Supply exactly hard_1, hard_2 and hard_3 in order")
    workflow = DiningWorkflow()
    cases = []
    for spec in specifications:
        if spec["parent_case_id"] != CASE_ID or not spec.get("authored_extensions"):
            raise ValueError("Each authored variant needs its parent and extension notes")
        initial = {
            "inventory": deepcopy(base.initial_state["inventory"]),
            "bookings": [],
            "dining_policy": spec["dining_policy"],
        }
        state = workflow.initialize(initial)
        expected = spec["expected_outcome"]
        policy = state["dining_policy"]
        physical_keys = set(state["inventory"][0]) - {"option_id"}
        if not physical_keys.issubset(expected) or not any(
            all(slot[k] == expected[k] for k in physical_keys) for slot in state["inventory"]
        ):
            raise ValueError("No physical inventory option satisfies the variant")
        if (
            not policy["minimum_total_inr"]
            <= expected["dining_total_inr"]
            <= policy["opening_total_inr"]
            or type(expected["without_onion_garlic_guests"]) is not int
            or not 0
            <= expected["without_onion_garlic_guests"]
            <= min(expected["party_size"], policy["max_without_onion_garlic_guests"])
            or expected.get("deposit_inr") != 0
            or expected.get("cancellation_fee_inr") != 0
            or expected.get("payment_status") != "not_requested"
            or expected.get("all_inclusive") is not True
        ):
            raise ValueError("Price, dietary or payment requirements are infeasible")
        user = UserTask.model_validate(spec["agent_brief"])
        if expected["dining_total_inr"] > user.known_facts.get("dining_budget_inr", 0):
            raise ValueError("Expected price exceeds the customer's budget")
        counterpart = CounterpartBrief.model_validate(spec["simulator_brief"])
        counterpart = counterpart.model_copy(
            update={
                "known_facts": {
                    **counterpart.known_facts,
                    "inventory": state["inventory"],
                    "dining_policy": policy,
                }
            }
        )
        criteria = {
            "reservation_expected": expected,
            "state_equals": [{"path": ["bookings", 0, k], "value": v} for k, v in expected.items()],
            "required_metrics": list(RULE_CHECKS) + ["dining_terms_history"],
            "rubrics": spec["rubrics"],
            "provenance": {
                **deepcopy(base.criteria["provenance"]),
                "parent_case_id": CASE_ID,
                "authored_variant": True,
                "authored_extensions": spec["authored_extensions"],
                "variant_spec_sha256": digest(canonical(spec)),
            },
        }
        case = ExecutionCase(
            case_id=spec["case_id"],
            version="1",
            workflow=workflow.name,
            workflow_version="2",
            schema_version=2,
            user_task=user,
            counterpart=counterpart,
            target_tools=(),
            counterpart_tools=tuple(workflow.tool_definitions),
            task_scope="single_call",
            call_initiation="harness_connected",
            initial_state=initial,
            criteria=criteria,
            conversation_events=spec["conversation_events"],
        )
        case.criteria["required_metrics"].extend(human_checks(case.model_dump(mode="json")))
        cases.append(case)
    return cases


def prepare_hard(baseline_path, variants_path, output):
    original = json.loads(baseline_path.read_text())
    if len(original) != 1:
        raise ValueError("Baseline file must contain one case")
    cases = convert_variants(original[0], json.loads(variants_path.read_text()))
    publish(output, canonical([c.model_dump(mode="json") for c in cases]))
    return {
        "hard_cases": str(output.resolve()),
        "hard_case_count": 3,
        "baseline_case_count": 1,
        "total_case_count": 4,
        "live_attempts": 0,
    }


def hard_blockers(config, cases):
    # Reuse provider-free settings checks without implying live qualification.
    result = pilot_blockers(config, cases)
    result["blockers"] = [
        b
        for b in result["blockers"]
        if b
        not in {
            "Supply exactly the selected restaurant case",
            "Pilot requires one attempt, concurrency one and at most 300 seconds",
        }
    ]
    if not cases or not {c.case_id for c in cases}.issubset(HARD_IDS):
        result["blockers"].append("Select only the authored hard restaurant variants")
    if (
        config.limits.max_attempts_per_case != 1
        or config.limits.max_concurrent_calls != 1
        or config.limits.max_call_seconds > 600
        or config.counterpart.interrupt_after_ms is not None
    ):
        result["blockers"].append(
            "Hard cases require one attempt each, concurrency one, at most "
            "600 seconds and no timed counterpart interruption"
        )
    result.pop("case_id")
    result["case_ids"] = [c.case_id for c in cases]
    result["counts"].update(planned=len(cases), not_run=len(cases))
    return result
