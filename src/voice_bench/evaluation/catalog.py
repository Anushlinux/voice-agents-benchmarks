"""Metric definitions for the existing restaurant workflow, not a new dataset."""

from voice_bench.evaluation.rubrics import EvaluationRubric, MetricDefinition

STATE = ("business/final.json",)
AUDIT = ("business/audit.json",)
CASE = ("config/case.json",)
AUDIO = ("audio/played.wav", "audio/received.wav")
REPORT = ("provider/rumik-call.json", "business/final.json")

# name: method, responsibility, evidence, exact passing behavior
RESTAURANT_METRICS = {
    "task_state": (
        "code",
        "requirement",
        STATE + CASE,
        "Final records satisfy the case's explicit state criteria.",
    ),
    "policy_actions": (
        "code",
        "requirement",
        AUDIT,
        "No forbidden target action was attempted, including blocked requests.",
    ),
    "duplicate_effects": (
        "code",
        "requirement",
        AUDIT,
        "Committed operations have unique identities within each actor.",
    ),
    "task_delivery": (
        "code",
        "prerequisite",
        ("target/task-delivery.json",),
        "The authenticated callback served the user's task to this attempt.",
    ),
    "counterpart_actions": (
        "code",
        "validity",
        AUDIT,
        "The counterpart made no forbidden business action attempts.",
    ),
    "reservation_count": ("code", "requirement", STATE, "Exactly one reservation was committed."),
    "reservation_history": (
        "code",
        "requirement",
        AUDIT + STATE + CASE,
        "Every committed reservation matches the expected terms and audit; "
        "a later repair does not erase an earlier wrong commitment.",
    ),
    "reservation_references": (
        "code",
        "requirement",
        AUDIT + STATE,
        "Saved references belong to this attempt's committed operations.",
    ),
    "reservation_evidence": (
        "code",
        "requirement",
        ("events.jsonl",) + AUDIO + STATE,
        "Booking actions have valid preceding playback and response links; "
        "semantic consent is checked separately.",
    ),
    "dining_terms_history": (
        "code",
        "requirement",
        STATE + AUDIT + CASE,
        "Quotes, confirmation revisions and committed terms match the "
        "audit, unchanged restaurant policy and fresh consent anchors.",
    ),
    "user_report_presence": (
        "human",
        "requirement",
        REPORT,
        "A reviewer identifies an actual native user report in the sealed "
        "provider record, not a transcript or harness summary.",
    ),
    "counterpart_validity": (
        "human",
        "validity",
        AUDIO,
        "The counterpart followed its facts, business rules, profile and "
        "scenario policy without inventing actions or helping the target.",
    ),
    "consent_alignment": (
        "human",
        "requirement",
        AUDIO,
        "Rumik agreed to the complete accurate current terms before booking; "
        "a correction, refusal or unrelated answer is not consent.",
    ),
    "constraint_behavior": (
        "human",
        "requirement",
        AUDIO,
        "All spoken commitments preserve the user's constraints and "
        "permissions, including branch preference and spending limits.",
    ),
    "hinglish_quality": (
        "human",
        "requirement",
        AUDIO,
        "Listening review confirms intelligible, natural Hinglish using the "
        "case's language rubric; text alone cannot pass this check.",
    ),
    "user_report_accuracy": (
        "human",
        "requirement",
        REPORT,
        "The actual native user report accurately describes the outcome "
        "and material terms without unsupported success claims.",
    ),
    "negotiation_behavior": (
        "human",
        "requirement",
        AUDIO,
        "Rumik negotiates within its authority and does not accept a "
        "commitment above the user's all-inclusive limit.",
    ),
    "dietary_understanding": (
        "human",
        "requirement",
        AUDIO,
        "Rumik obtains the required guest count with both onion and garlic "
        "excluded; vegetarian alone is insufficient.",
    ),
}


def restaurant_rubric(case):
    if case.workflow != "mock_restaurant_reservation" or case.workflow_version not in {"1", "2"}:
        raise ValueError("The initial metric catalog supports restaurant workflow versions 1 and 2")
    required = case.criteria.get("required_metrics", [])
    if len(required) != len(set(required)) or not required:
        raise ValueError("Required metrics must be nonempty and unique")
    if unknown := set(required) - RESTAURANT_METRICS.keys():
        raise ValueError("Undefined metrics: " + ", ".join(sorted(unknown)))
    definitions = []
    for name in dict.fromkeys([*required, "negotiation_behavior", "dietary_understanding"]):
        method, role, files, rule = RESTAURANT_METRICS[name]
        applies = name in required
        definitions.append(
            MetricDefinition(
                name=name,
                description=rule,
                method=method,
                role=role,
                applies=applies,
                applicability_reason=(
                    "Required by this case's existing criteria."
                    if applies
                    else "This capability is not required by the source case."
                ),
                required_evidence=files,
                pass_rule=rule,
            )
        )
    return EvaluationRubric(version="restaurant-status-v1", metrics=tuple(definitions))
