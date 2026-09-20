"""Expose unfinished evaluation stages without inventing a completed assessment."""


def evaluation_progress(case, metrics, *, reviewed=False, reviewed_checks=()):
    by_name = {m["name"]: m for m in metrics}
    definitions = (case.get("evaluation_rubric") or {}).get("metrics", [])
    required = (
        [d["name"] for d in definitions if d["applies"] and d["role"] != "diagnostic"]
        if definitions
        else case["criteria"].get("required_metrics", [])
    )
    human = {d["name"] for d in definitions if d["method"] == "human" and d["applies"]}
    if case.get("workflow") == "mock_restaurant_reservation":
        from voice_bench.restaurant_hard_cases import human_checks

        human.update(human_checks(case))
    pending = [
        name
        for name in required
        if name not in by_name
        or by_name[name]["status"] in {"uncertain", "not_applicable"}
        or (name in human and (not reviewed or name not in reviewed_checks))
    ]
    review_pending = [name for name in pending if name in human]
    return {
        "status": "awaiting_required_review"
        if review_pending
        else ("awaiting_required_checks" if pending else "checks_resolved"),
        "pending_metrics": pending,
        "pending_review_metrics": review_pending,
        "human_review_imported": reviewed,
    }
