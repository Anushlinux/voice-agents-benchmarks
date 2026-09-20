"""Offline import and preflight for the one explicitly selected adapted case."""

import hashlib
import json
import os
from pathlib import Path

from voice_bench.business.reservations import ReservationWorkflow
from voice_bench.contracts import ExecutionCase
from voice_bench.evidence.local import canonical, digest, publish
from voice_bench.models import CounterpartBrief, UserTask

CASE_ID = "tm1_restaurant_mumbai_hinglish_001"
CONVERSATION_ID = "dlg-00055f4e-4a46-48bf-8d99-4e477663eb23"
SOURCE_BLOB = "21836935dbc399bf5ff5710d53d5326cc2d74ade"
HUMAN_CHECKS = (
    "counterpart_validity",
    "consent_alignment",
    "constraint_behavior",
    "hinglish_quality",
    "user_report_accuracy",
)
RULE_CHECKS = (
    "task_state",
    "policy_actions",
    "duplicate_effects",
    "task_delivery",
    "counterpart_actions",
    "reservation_count",
    "reservation_history",
    "reservation_references",
    "reservation_evidence",
    "user_report_presence",
)


def import_case(case_path: Path, source_path: Path):
    raw = source_path.read_bytes()
    source = json.loads(raw)
    blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    if (
        source.get("conversation_id") != CONVERSATION_ID
        or source.get("instruction_id") != "restaurant-table-2"
        or len(source.get("utterances", [])) != 20
        or blob != SOURCE_BLOB
    ):
        raise ValueError("Selected Taskmaster source differs from the inspected record")
    supplied = json.loads(case_path.read_text())
    if supplied["case_id"] != CASE_ID or supplied["reconstructed_from_handoff"] is not True:
        raise ValueError("Expected exactly the reconstructed single case")
    workflow = ReservationWorkflow()
    state = workflow.initialize({"inventory": supplied["inventory"], "bookings": []})
    expected = supplied["expected_outcome"]
    if (
        len(state["inventory"]) != 5
        or sum(
            all(s.get(k) == v for k, v in expected.items() if k != "booking_name")
            for s in state["inventory"]
        )
        != 1
    ):
        raise ValueError("The five-option inventory must contain exactly one matching slot")
    counterpart = CounterpartBrief.model_validate(supplied["simulator_brief"])
    # Supply physical inventory, never annotations identifying the correct option.
    counterpart = counterpart.model_copy(
        update={
            "known_facts": {**counterpart.known_facts, "inventory": state["inventory"]},
        }
    )
    criteria = {
        "state_equals": [{"path": ["bookings", 0, k], "value": v} for k, v in expected.items()],
        "reservation_expected": expected,
        "required_metrics": list(RULE_CHECKS + HUMAN_CHECKS),
        "rubrics": supplied["rubrics"],
        "provenance": {
            "source_url": "https://raw.githubusercontent.com/google-research-datasets/"
            "Taskmaster/master/TM-1-2019/sample.json",
            "conversation_id": CONVERSATION_ID,
            "instruction_id": "restaurant-table-2",
            "source_sha256": digest(raw),
            "source_git_blob_sha": blob,
            "adapted_case_sha256": digest(case_path.read_bytes()),
            "license": "CC-BY-4.0",
            "reconstructed_from_handoff": True,
        },
    }
    return ExecutionCase(
        case_id=CASE_ID,
        version="1",
        workflow=workflow.name,
        workflow_version=workflow.version,
        schema_version=2,
        user_task=UserTask.model_validate(supplied["agent_brief"]),
        counterpart=counterpart,
        target_tools=(),
        counterpart_tools=("check_availability", "record_reservation"),
        task_scope="single_call",
        call_initiation="harness_connected",
        initial_state=state,
        criteria=criteria,
    )


def prepare(case_path, source_path, output):
    case = import_case(case_path, source_path)
    publish(output, canonical([case.model_dump(mode="json")]))
    return {
        "execution_cases": str(output.resolve()),
        "case_count": 1,
        "validation": "offline_fixture_only",
        "live_attempts": 0,
        "provenance": case.criteria["provenance"],
    }


def pilot_blockers(config, cases):
    """No network probes, secret loading, database connections or provider clients."""
    blockers = []
    if len(cases) != 1 or cases[0].case_id != CASE_ID:
        blockers.append("Supply exactly the selected restaurant case")
    if config.channels != ("browser",):
        blockers.append("Pilot requires browser only")
    if (
        config.limits.max_attempts_per_case != 1
        or config.limits.max_concurrent_calls != 1
        or config.limits.max_call_seconds > 300
    ):
        blockers.append("Pilot requires one attempt, concurrency one and at most 300 seconds")
    for label, value in {
        "Rumik agent": config.target.agent_ref,
        "deployed version": config.target.deployed_version,
        "counterpart model": config.counterpart.model,
        "counterpart voice": config.counterpart.voice,
        "counterpart instructions": config.counterpart.instructions,
        "turn detection": config.counterpart.turn_detection,
        "rate card": config.runtime.rate_card_version,
    }.items():
        if not value:
            blockers.append("Missing " + label)
    if not config.runtime.public_base_url.startswith("https://"):
        blockers.append("Missing public HTTPS callback endpoint")
    if config.limits.max_spend_inr <= 0 or config.limits.max_total_call_minutes <= 0:
        blockers.append("No funded spend/minute limits")
    costs = config.runtime.cost_components_inr_per_attempt
    if (
        any(costs.get(k, 0) <= 0 for k in ("target", "counterpart"))
        or config.runtime.cost_ceiling_inr_per_attempt <= 0
        or sum(costs.values()) > config.runtime.cost_ceiling_inr_per_attempt
    ):
        blockers.append("Missing or insufficient per-component and total attempt cost ceilings")
    for name in ("DATABASE_URL", "RUMIK_API_KEY", "OPENAI_API_KEY", "BENCH_TOOLS_SECRET"):
        if not os.environ.get(name):
            blockers.append("Not exported: " + name)
    blockers.extend(
        [
            "Live qualification pending: callback connectivity, hosted user-task consumption, "
            "database and two-way browser audio",
            "Native post-call Rumik report delivery is not integrated; "
            "missing report stays inconclusive",
        ]
    )
    return {
        "case_id": CASE_ID,
        "status": "blocked",
        "live_attempts": 0,
        "counts": {
            "planned": 1,
            "attempted": 0,
            "valid": 0,
            "invalid": 0,
            "unresolved": 0,
            "passed": 0,
            "failed": 0,
            "not_run": 1,
        },
        "blockers": blockers,
        "provider_calls": 0,
    }
