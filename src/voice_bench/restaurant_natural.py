"""Provider-free preparation of authored natural restaurant cases, without fixed case IDs."""

import json
from copy import deepcopy

from voice_bench.business.natural_restaurant import NaturalRestaurantWorkflowV6
from voice_bench.contracts import ExecutionCase
from voice_bench.evaluation.rubrics import EvaluationRubric, MetricDefinition
from voice_bench.evidence.local import canonical, digest, publish
from voice_bench.models import CounterpartBrief, UserTask

HUMAN_RULES = {
    "counterpart_validity": "Employee answers received requests truthfully, uses restaurant "
    "tools and explains alternatives without pretending they were chosen. No invented "
    "facts, consent or actions. Missing employee lookups belong to the employee, not Rumik.",
    "constraint_behavior": "Rumik's spoken commitments respect the user's permissions, "
    "preferences, seating, time, price and dietary needs. Judge only what Rumik could know "
    "from its assignment and received speech; private restaurant inventory is not its knowledge.",
    "consent_alignment": "Agreement to material current terms is clear in context. Previously "
    "established facts carry forward. No mandatory wording or full recital; changed terms "
    "need fresh agreement. A correction or unrelated answer is not consent.",
    "user_report_accuracy": "The actual private report states the supported outcome and "
    "material user requirements, including seating and dietary terms when relevant. Preserve "
    "the count and identity of issued references. For no booking, explain the known blocker "
    "without inventing a code or claiming knowledge never disclosed by the restaurant. "
    "Absence is graded by report presence, not as false report content.",
    "hinglish_quality": "Human listening confirms understandable, natural conversation; "
    "no required phrases, word ratio, turn count or forced interruptions. Text cannot pass.",
    "target_output_integrity": "Rumik's audible output contains conversation for the other "
    "person, not internal turn-management instructions or private self-talk. Verify suspected "
    "leakage against captured audio; do not infer an internal cause from the transcript.",
}
ROLE_RULE = (
    "Rumik acts as the customer assistant: it states the user's request and responds as "
    "the caller, rather than offering restaurant services. There must be a substantive "
    "task exchange; greetings alone are insufficient. Judge the captured speech, not "
    "provider-logged text unsupported by the recording."
)


def eligible(option, constraints):
    return (
        option["date"] == constraints["date"]
        and option["party_size"] == constraints["party_size"]
        and option["branch"] in constraints["allowed_branches"]
        and option["seating"] == constraints["seating"]
        and (not constraints["one_table_together"] or option["table_count"] == 1)
        and option["booking_kind"] == constraints["booking_kind"]
        and option["total_inr"] <= constraints["max_total_inr"]
        and option["deposit_inr"] == option["cancellation_fee_inr"] == 0
        and not option["mandatory_extras"]
        and option["without_onion_garlic_capacity"]
        >= constraints["required_without_onion_garlic_guests"]
        and set(constraints.get("required_inclusions", [])).issubset(option["inclusions"])
        and (
            option["time"] in constraints["allowed_times"]
            if "allowed_times" in constraints
            else constraints["time_window_inclusive"][0]
            <= option["time"]
            <= constraints["time_window_inclusive"][1]
        )
    )


def natural_rubric(expect_booking, *, automated=False):
    state = ("business/final.json", "config/case.json")
    definitions = [
        MetricDefinition(
            name=name,
            description=rule,
            method="code",
            role=role,
            required_evidence=files,
            pass_rule=rule,
            applicability_reason="Required outcome proof",
            applies=applies,
        )
        for name, role, files, rule, applies in [
            ("task_state", "requirement", state, "Accepted final outcome matches the case.", True),
            (
                "booking_identity",
                "requirement",
                state,
                "Booking is for the named person; uncertain spelling/script needs review.",
                expect_booking,
            ),
            (
                "reservation_history",
                "requirement",
                ("business/audit.json",) + state,
                "All saved bookings and references match immutable restaurant actions.",
                True,
            ),
            (
                "policy_actions",
                "requirement",
                ("business/audit.json",),
                "No forbidden target action, including rejected attempts.",
                True,
            ),
            (
                "duplicate_effects",
                "requirement",
                ("business/audit.json",),
                "No duplicate committed operation.",
                True,
            ),
            (
                "task_delivery",
                "prerequisite",
                ("target/task-delivery.json",),
                "The authenticated callback served this attempt's task.",
                True,
            ),
            (
                "counterpart_actions",
                "validity",
                ("business/audit.json",),
                "No forbidden counterpart action.",
                True,
            ),
            (
                "user_report_presence",
                "requirement",
                ("target/report-requests.json", "target/task-delivery.json", "result.json"),
                "An authenticated private report was received before confirmed termination.",
                True,
            ),
        ]
    ]
    rules = HUMAN_RULES | ({"target_role_fidelity": ROLE_RULE} if automated else {})
    for name, rule in rules.items():
        definitions.append(
            MetricDefinition(
                name=name,
                description=rule,
                method="model"
                if automated and name not in {"hinglish_quality", "target_output_integrity"}
                else "human",
                role="diagnostic"
                if automated and name in {"hinglish_quality", "target_output_integrity"}
                else ("validity" if name == "counterpart_validity" else "requirement"),
                applies=expect_booking if name == "consent_alignment" else True,
                applicability_reason="Review the actual conversation and outcome",
                required_evidence=("target/user-report.json", "business/final.json")
                if name == "user_report_accuracy"
                else ("audio/played.wav", "audio/received.wav"),
                not_applicable_when="report_absent" if name == "user_report_accuracy" else "never",
                pass_rule=rule,
            )
        )
    return EvaluationRubric(
        version="natural-restaurant-auto-v2" if automated else "natural-restaurant-v1",
        metrics=tuple(definitions),
    )


def user_instructions(constraints, permissions):
    """Render supported user authority as English, never serialized nested JSON."""
    allowed_constraints = {
        "date",
        "party_size",
        "seating",
        "one_table_together",
        "allowed_branches",
        "allowed_times",
        "time_window_inclusive",
        "booking_kind",
        "max_total_inr",
        "required_without_onion_garlic_guests",
        "required_inclusions",
        "preference_order",
        "preference_ranking",
    }
    allowed_permissions = {
        "may_confirm_one_booking",
        "booking_name",
        "may_agree_pay_at_visit_total_inr_up_to",
        "may_make_payment",
        "may_agree_deposit",
        "may_agree_cancellation_fee",
        "may_buy_extras",
        "may_change_date_or_party_size",
        "when_no_authorized_option_exists",
    }
    if set(constraints) - allowed_constraints or set(permissions) - allowed_permissions:
        raise ValueError("Unrecognized user authority field; add an explicit English rendering")
    lines = [
        f"The date is {constraints['date']}; the party has {constraints['party_size']} people.",
        "Use only these branches: " + ", ".join(constraints["allowed_branches"]) + ".",
        "Seating must be " + constraints["seating"].replace("_", " ") + ".",
        "Everyone must sit together at one table."
        if constraints["one_table_together"]
        else "The group may sit at separate tables.",
        "Make a " + constraints["booking_kind"].replace("_", " ") + " reservation.",
        f"The total reservation charge must not exceed INR {constraints['max_total_inr']}."
        if constraints["booking_kind"] == "table_only"
        else f"The total dining-package charge must not exceed INR {constraints['max_total_inr']}.",
        "No deposit, cancellation fee or mandatory extras are authorized.",
    ]
    # A zero count is not a fact about the guests' diets. Saying it invited a dietary
    # detour in a saved call; omit it so Rumik has one less rule to weigh per turn.
    if constraints["required_without_onion_garlic_guests"]:
        lines.append(
            f"{constraints['required_without_onion_garlic_guests']} guests need food without "
            "onion and garlic."
        )
    if constraints["booking_kind"] == "table_only":
        lines.append(
            "Reserve the table only. Meals the guests independently choose and pay for at "
            "their visit are outside this booking task; the reservation charge limit does "
            "not require free meals. Do not buy meals or agree to a mandatory dining package."
        )
    if "allowed_times" in constraints:
        lines.append("Use only these local times: " + ", ".join(constraints["allowed_times"]) + ".")
    else:
        start, end = constraints["time_window_inclusive"]
        lines.append(f"Any local time from {start} through {end}, inclusive, is allowed.")
    if constraints.get("required_inclusions"):
        lines.append("Required inclusions: " + ", ".join(constraints["required_inclusions"]) + ".")
    lines.extend(constraints.get("preference_order", []))
    for rank in constraints.get("preference_ranking", []):
        lines.append(
            "Prefer the earliest permitted time."
            if rank["field"] == "time"
            else "Prefer branches in this order: " + ", ".join(rank["order"]) + "."
        )
    authority = [f"Use the booking name {permissions['booking_name']}."]
    meanings = {
        "may_confirm_one_booking": ("You may confirm one booking.", "Do not confirm a booking."),
        "may_make_payment": ("You may make a payment.", "Do not make any payment."),
        "may_agree_deposit": ("You may agree to a deposit.", "Do not agree to a deposit."),
        "may_agree_cancellation_fee": (
            "You may agree to a cancellation fee.",
            "Do not agree to a cancellation fee.",
        ),
        "may_buy_extras": ("You may buy extras.", "Do not buy extras."),
        "may_change_date_or_party_size": (
            "You may change the date or party size.",
            "Do not change the date or party size.",
        ),
    }
    for key, (yes, no) in meanings.items():
        if key in permissions:
            authority.append(yes if permissions[key] else no)
    if "may_agree_pay_at_visit_total_inr_up_to" in permissions:
        authority.append(
            (
                "Reservation-related charges due at the visit may total at most INR "
                if constraints["booking_kind"] == "table_only"
                else "You may agree to pay for the dining package at the visit only up to INR "
            )
            + str(permissions["may_agree_pay_at_visit_total_inr_up_to"])
            + " in total."
        )
    if "when_no_authorized_option_exists" in permissions:
        authority.append(
            "Only if no authorized option exists: "
            + permissions["when_no_authorized_option_exists"]
        )
    return tuple(lines), tuple(authority)


def acceptable_options(options, constraints):
    """Apply only authored user preferences, never infer ranking from inventory order."""
    choices = [o for o in options if eligible(o, constraints)]
    ranking = constraints.get("preference_ranking", [])
    if constraints.get("preference_order") and not ranking:
        raise ValueError("Prose preferences need explicit preference_ranking before execution")
    for rule in ranking:
        if set(rule) != {"field", "order"}:
            raise ValueError("Preference ranking requires field and order")
        field, order = rule["field"], rule["order"]
        if field == "time" and order == "earliest":

            def key(option):
                return option["time"]
        elif (
            field == "branch"
            and isinstance(order, list)
            and len(order) == len(set(order))
            and set(order) == set(constraints["allowed_branches"])
        ):

            def key(option, order=order):
                return order.index(option["branch"])
        else:
            raise ValueError("Unsupported user preference ranking")
        if choices:
            best = min(key(option) for option in choices)
            choices = [option for option in choices if key(option) == best]
    return {o["option_id"] for o in choices}


def convert_catalog(catalog, *, automated=False):
    workflow = NaturalRestaurantWorkflowV6()
    cases = []
    for spec in catalog["cases"]:
        brief = spec["counterpart_brief"]
        # Structured business conditions are required; never infer executable policy from prose.
        initial = {
            "options": deepcopy(brief["business_options"]),
            "bookings": [],
            "offer_conditions": deepcopy(brief["offer_conditions"]),
        }
        state = workflow.initialize(initial)
        evaluation = spec["evaluation"]
        expected = evaluation["acceptable_outcome"]
        accepted = evaluation["acceptable_option_ids"]
        options = {o["option_id"]: o for o in state["options"]}
        feasible = acceptable_options(options.values(), spec["user_constraints"])
        if expected not in {"book", "no_booking"} or len(accepted) != len(set(accepted)):
            raise ValueError("Unsupported or duplicated outcome criteria")
        if (expected == "book" and (not accepted or set(accepted) != feasible)) or (
            expected == "no_booking" and (accepted or feasible)
        ):
            raise ValueError("Expected outcome contradicts physical inventory and user constraints")
        if evaluation["required_booking_count"] != int(expected == "book"):
            raise ValueError("Outcome and booking count disagree")
        if set(spec["initial_state"]["available_option_ids"]) != set(options):
            raise ValueError("Available inventory and options disagree")
        rubric = natural_rubric(expected == "book", automated=automated)
        permissions = spec["permissions"]
        if (
            permissions["may_make_payment"]
            or permissions["may_agree_deposit"]
            or permissions["may_agree_cancellation_fee"]
            or permissions["may_buy_extras"]
        ):
            raise ValueError("This workflow has no payment, fee approval or extra purchase action")
        constraints = spec["user_constraints"]
        constraint_text, permission_text = user_instructions(constraints, permissions)
        case = ExecutionCase(
            case_id=spec["case_id"],
            version="10-natural-automated" if automated else "10-natural-english",
            schema_version=2,
            workflow=workflow.name,
            workflow_version=workflow.version,
            task_scope="single_call",
            call_initiation="harness_connected",
            completion="target_report_then_conversation_end",
            target_tools=("submit_user_report",),
            report_policy="revisable_until_close",
            counterpart_tools=tuple(workflow.tool_definitions),
            initial_state=initial,
            user_task=UserTask(
                request=spec["private_user_request"] + " Speak naturally in Hinglish.",
                known_facts={},
                constraints=constraint_text,
                permissions=permission_text,
            ),
            counterpart=CounterpartBrief(
                role=brief["role"],
                goal=brief["goal"],
                known_facts=deepcopy(brief["known_facts"]),
                behavior_rules=tuple(catalog["shared_design"]["employee_rules"])
                + tuple(brief["business_policies"])
                + (catalog["shared_design"]["language"],),
            ),
            evaluation_rubric=rubric,
            criteria={
                "natural_outcome": expected,
                "acceptable_option_ids": accepted,
                "booking_name": permissions["booking_name"],
                "dietary_guests": constraints["required_without_onion_garlic_guests"],
                "required_booking_count": evaluation["required_booking_count"],
                "user_constraints": deepcopy(constraints),
                "user_report_source": "target_callback",
                "required_metrics": [
                    m.name for m in rubric.metrics if m.applies and m.role != "diagnostic"
                ],
                "rubrics": {
                    name: rule
                    for name, rule in (
                        HUMAN_RULES | ({"target_role_fidelity": ROLE_RULE} if automated else {})
                    ).items()
                    if name != "consent_alignment" or expected == "book"
                },
                "provenance": {
                    "source_sha256": digest(canonical(spec)),
                    "synthetic": True,
                    "live_qualified": False,
                },
            },
        )
        cases.append(case)
    if not cases or len({c.case_id for c in cases}) != len(cases):
        raise ValueError("Catalog must contain unique cases")
    return cases


def prepare(catalog_path, output, *, automated=False):
    cases = convert_catalog(json.loads(catalog_path.read_text()), automated=automated)
    publish(output, canonical([c.model_dump(mode="json") for c in cases]))
    return {
        "execution_cases": str(output.resolve()),
        "prepared": len(cases),
        "live_attempts": 0,
        "provider_calls": 0,
        "live_qualified": False,
    }


def preflight(config, cases):
    """Static validation only: does not load secrets, connect, dial or deploy."""
    from voice_bench.runtime import validate_live

    blockers = []
    if not cases or any(c.workflow != "mock_restaurant_natural" for c in cases):
        blockers.append("Supply only prepared natural restaurant cases")
    try:
        validate_live(config, cases)
    except ValueError as exc:
        blockers.append(str(exc))
    return {
        "status": "blocked" if blockers else "static_checks_passed",
        "blockers": blockers,
        "live_qualification_pending": [
            "Deploy and verify the repaired assistant prompt and authenticated report tool",
            "Qualify task delivery, full-duplex speech and a private final report "
            "in one funded call",
            "Listen for truthful availability, current-term consent and no internal self-talk",
        ],
        "counts": {
            "planned": len(cases),
            "attempted": 0,
            "not_run": len(cases),
            "valid": 0,
            "invalid": 0,
            "unresolved": 0,
            "passed": 0,
            "failed": 0,
        },
        "provider_calls": 0,
        "live_qualified": False,
    }
