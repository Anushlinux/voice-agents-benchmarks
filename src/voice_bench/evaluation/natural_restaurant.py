"""Outcome checks for natural bookings and useful refusals, separate from speech judgments."""

import json
import unicodedata

from voice_bench.business.reservations import consent_anchors, issued_reference
from voice_bench.models import MetricResult


def normalized_name(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def consent_boundary(case, offer, events):
    """Reconstruct the quoted terms from evidence, not a claimed earlier cutoff."""
    prepared = offer["prepared_after_sequence"]
    if (
        case.get("workflow_version") not in {"5", "6"}
        or "terms_available_after_sequence" not in offer
    ):
        return prepared
    terms = offer["terms"]
    if terms.get("without_onion_garlic_guests") != 0:
        return prepared
    quoted = {k: v for k, v in terms.items() if k != "without_onion_garlic_guests"}
    for event in events:
        payload = event.get("payload", {})
        result = payload.get("result", {})
        if (
            event.get("kind") == "business_tool_result"
            and payload.get("actor") == "counterpart"
            and payload.get("tool") == "check_availability"
            and payload.get("operation_id") == offer.get("terms_lookup_operation_id")
            and event["sequence"] == offer["terms_available_after_sequence"]
            and event["sequence"] <= prepared
            and result.get("ok")
            and quoted in result.get("matching_options", []) + result.get("other_time_options", [])
        ):
            return event["sequence"]
    return prepared


def natural_metrics(directory, case, refs, final, audit):
    criteria = case["criteria"]
    bookings = final.get("bookings", [])
    metrics = []

    def add(name, status, explanation, files):
        if not set(files).issubset(refs):
            status, explanation = "uncertain", "Required evidence is missing"
        metrics.append(
            MetricResult(
                name=name,
                status=status,
                explanation=explanation,
                evidence=tuple(refs[f] for f in files if f in refs),
            )
        )

    def load(name, fallback):
        return json.loads((directory / name).read_text()) if name in refs else fallback

    options = {o["option_id"]: o for o in case["initial_state"]["options"]}
    state_ok = len(bookings) == criteria["required_booking_count"]
    for booking in bookings:
        option = options.get(booking.get("option_id"), {})
        state_ok = state_ok and booking.get("option_id") in criteria["acceptable_option_ids"]
        state_ok = state_ok and bool(option) and all(booking.get(k) == v for k, v in option.items())
        state_ok = (
            state_ok and booking.get("without_onion_garlic_guests") == criteria["dietary_guests"]
        )
    add(
        "task_state",
        "met" if state_ok else "not_met",
        "Checked the declared booking or no-booking outcome and material terms; "
        "name identity and spoken authorization are separate checks.",
        ("business/final.json", "config/case.json"),
    )
    identity = "not_applicable" if not criteria["required_booking_count"] else "uncertain"
    if bookings and all(
        normalized_name(b.get("booking_name", "")) == normalized_name(criteria["booking_name"])
        for b in bookings
    ):
        identity = "met"
    add(
        "booking_identity",
        identity,
        "Exact normalized names match; different spelling or script needs semantic review, "
        "not an automatic wrong-person verdict.",
        ("business/final.json", "config/case.json"),
    )

    operations = [
        a
        for a in audit
        if a["tool"] == "record_reservation" and a["result"].get("ok") and not a.get("replay")
    ]
    events = (
        [json.loads(line) for line in (directory / "events.jsonl").read_text().splitlines()]
        if "events.jsonl" in refs
        else []
    )
    history = [a["result"].get("reservation") for a in operations]
    history_ok = history == bookings and final.get("options") == case["initial_state"]["options"]
    history_ok = (
        history_ok and final.get("offer_conditions") == case["initial_state"]["offer_conditions"]
    )
    for action, booking in zip(operations, bookings, strict=False):
        anchors = booking.get("consent_evidence", {})
        cutoff = anchors.get("observed_through_sequence", -1)
        preceding = [e for e in events if e["sequence"] <= cutoff]
        commits = [
            e
            for e in events
            if e["kind"] == "reservation_action"
            and e["payload"].get("operation_id") == action["operation_id"]
            and e["payload"].get("result", {}).get("reservation") == booking
        ]
        offers = [
            a["result"]["offer"]
            for a in audit
            if a["tool"] == "offer_reservation" and a["result"].get("ok") and not a.get("replay")
        ]
        offer = next((o for o in offers if o["offer_id"] == booking.get("offer_id")), None)
        history_ok = history_ok and (
            action.get("actor") == "counterpart"
            and booking.get("reference")
            == issued_reference(
                case.get("workflow_version"), directory.name, action["operation_id"]
            )
            and booking.get("operation_id") == action["operation_id"]
            and bool(commits)
            and cutoff < commits[0]["sequence"]
            and consent_anchors(preceding) == anchors
            and bool(offer)
            and all(booking.get(k) == v for k, v in offer["terms"].items())
            and min(anchors.get("event_sequences", [-1])) > consent_boundary(case, offer, events)
        )
    add(
        "reservation_history",
        "met" if history_ok else "not_met",
        "Replayed booking identity, terms, action ownership, reference and structural speech "
        "anchors. These do not prove semantic agreement.",
        ("business/audit.json", "business/final.json", "config/case.json", "events.jsonl"),
    )

    report = load("target/user-report.json", {})
    if report:
        from voice_bench.evaluation.report_assertions import reference_metric

        metrics.append(reference_metric(report, final, refs))
    delivery = load("target/task-delivery.json", {})
    result = load("result.json", {})
    requests = load("target/report-requests.json", [])
    report_ok = (
        report.get("source") == "authenticated_rumik_tool"
        and report.get("run_id") == directory.name
        and report.get("call_id") == delivery.get("call_id")
        and report.get("task_sha256") == delivery.get("sha256")
        and bool(report.get("text", "").strip())
        and any(
            r.get("result", {}).get("report_saved") and r.get("report") == report.get("text")
            for r in requests
        )
    )
    presence = (
        "met"
        if report_ok
        else (
            "not_met"
            if result.get("termination_confirmed") and "target/report-requests.json" in refs
            else "uncertain"
        )
    )
    add(
        "user_report_presence",
        presence,
        "Checked authenticated report receipt. Confirmed absence is separate from false content; "
        "a missing report does not establish which actor caused an interrupted call.",
        ("target/report-requests.json", "target/task-delivery.json", "result.json")
        + (("target/user-report.json",) if report_ok else ()),
    )
    return metrics
