"""Reservation state checks plus evidence-backed human review requirements."""

import json

from voice_bench.business.reservations import consent_anchors, reservation_reference
from voice_bench.models import MetricResult
from voice_bench.restaurant_case import RULE_CHECKS
from voice_bench.restaurant_hard_cases import human_checks


def reservation_metrics(directory, case, refs, final, audit):
    expected = case["criteria"]["reservation_expected"]
    bookings = final.get("bookings", [])
    operations = [
        a
        for a in audit
        if a["tool"] == "record_reservation" and a["result"].get("ok") and not a.get("replay")
    ]
    metrics = []

    def add(name, met, explanation, files):
        evidence = tuple(refs[f] for f in files if f in refs)
        status = "uncertain" if len(evidence) != len(files) else ("met" if met else "not_met")
        metrics.append(
            MetricResult(name=name, status=status, explanation=explanation, evidence=evidence)
        )

    add(
        "reservation_count",
        len(bookings) == 1,
        "Exactly one saved reservation is required.",
        ["business/final.json"],
    )
    historical = [a["result"].get("reservation", {}) for a in operations]
    correct_history = (
        len(historical) == len(bookings)
        and historical == bookings
        and all(all(b.get(k) == v for k, v in expected.items()) for b in historical)
        and all(a.get("actor") == "counterpart" for a in operations)
    )
    add(
        "reservation_history",
        correct_history,
        "Every committed booking must match both the user's terms and the saved action history; "
        "later repairs cannot erase an incorrect commitment.",
        ["business/audit.json", "business/final.json", "config/case.json"],
    )
    references = (
        bool(bookings)
        and all(
            b.get("reference") == reservation_reference(directory.name, a["operation_id"])
            and b.get("operation_id") == a["operation_id"]
            for b, a in zip(bookings, operations, strict=False)
        )
        and len(bookings) == len(operations)
    )
    add(
        "reservation_references",
        references,
        "References must be allocated by this attempt.",
        ["business/audit.json", "business/final.json"],
    )
    events_path = directory / "events.jsonl"
    events = (
        [json.loads(line) for line in events_path.read_text().splitlines()]
        if "events.jsonl" in refs
        else []
    )
    evidence_ok = bool(bookings)
    for booking in bookings:
        commits = [
            e
            for e in events
            if e["kind"] == "reservation_action"
            and e["payload"].get("operation_id") == booking.get("operation_id")
            and e["payload"].get("result", {}).get("reservation") == booking
        ]
        anchors = booking.get("consent_evidence")
        if not commits or not anchors:
            evidence_ok = False
            continue
        # Verify the claimed anchors against events that actually preceded the write.
        cutoff = anchors.get("observed_through_sequence", -1)
        before = [e for e in events if e["sequence"] <= cutoff]
        if cutoff >= commits[0]["sequence"] or consent_anchors(before) != anchors:
            evidence_ok = False
    playback_file = (
        "audio/sent.wav"
        if any(e["kind"] == "carrier_stream_start" for e in events)
        else "audio/played.wav"
    )
    add(
        "reservation_evidence",
        evidence_ok,
        "Checked playback, response and booking event links. Speech meaning still needs review.",
        ["events.jsonl", playback_file, "audio/received.wav", "business/final.json"],
    )
    if case.get("workflow_version") == "2":
        quote_actions = [
            a["result"]["quote"]
            for a in audit
            if a["result"].get("ok")
            and not a.get("replay")
            and a["tool"] in {"quote_reservation", "counteroffer", "set_dietary_requirements"}
        ]
        confirmations = [
            a["result"]["confirmation"]
            for a in audit
            if a["result"].get("ok") and not a.get("replay") and a["tool"] == "prepare_confirmation"
        ]
        terms_ok = (
            quote_actions == final.get("quotes")
            and confirmations == final.get("confirmations")
            and final.get("dining_policy") == case["initial_state"]["dining_policy"]
        )
        for booking in bookings:
            confirmation = next(
                (
                    c
                    for c in confirmations
                    if c["confirmation_id"] == booking.get("confirmation_id")
                ),
                None,
            )
            quote = next(
                (q for q in quote_actions if q["quote_id"] == booking.get("quote_id")), None
            )
            terms_ok = terms_ok and bool(confirmation and quote)
            if confirmation and quote:
                terms_ok = (
                    terms_ok
                    and all(booking.get(k) == v for k, v in confirmation["terms"].items())
                    and all(booking.get(k) == v for k, v in quote.items())
                    and booking["quote_id"] == final.get("active_quote_id")
                    and booking["confirmation_id"] == final.get("active_confirmation_id")
                    and min(booking.get("consent_evidence", {}).get("event_sequences", [-1]))
                    > confirmation["prepared_after_sequence"]
                )
        add(
            "dining_terms_history",
            bool(bookings) and terms_ok,
            "Checked saved quotes, dietary terms, confirmation revisions and fresh consent "
            "against the committed history; unaccepted offers need not meet the customer's budget.",
            ["business/final.json", "business/audit.json", "config/case.json"],
        )
    if case["criteria"].get("user_report_source") == "target_callback":
        report_path = directory / "target/user-report.json"
        report = json.loads(report_path.read_text()) if "target/user-report.json" in refs else {}
        from voice_bench.evaluation.report_assertions import reference_metric

        metrics.append(reference_metric(report, final, refs))
        delivery_path = directory / "target/task-delivery.json"
        delivery = json.loads(delivery_path.read_text()) if delivery_path.exists() else {}
        add(
            "user_report_presence",
            report.get("source") == "authenticated_rumik_tool"
            and report.get("run_id") == directory.name
            and report.get("call_id") == delivery.get("call_id")
            and report.get("task_sha256") == delivery.get("sha256")
            and bool(report.get("text", "").strip()),
            "Authenticated target-authored final report received through the explicitly "
            "modeled private output tool; accuracy still requires review.",
            ["target/user-report.json", "target/task-delivery.json", "target/report-requests.json"],
        )
    else:
        metrics.append(
            MetricResult(
                name="user_report_presence",
                status="uncertain",
                explanation=(
                    "A provider-native post-call user report must be identified in the saved "
                    "provider record during human review. A call transcript or generated summary "
                    "is insufficient."
                ),
            )
        )
    return metrics


def validate_reservation_review(directory, review, prior):
    """A review can resolve semantics, but cannot manufacture state or a user report."""
    checks = {m.name: m for m in review.checks}
    case = json.loads((directory / "config/case.json").read_text())
    report_file = (
        "target/user-report.json"
        if case["criteria"].get("user_report_source") == "target_callback"
        else "provider/rumik-call.json"
    )
    required_human = human_checks(case)
    execution = json.loads((directory / "result.json").read_text())
    events = [json.loads(line) for line in (directory / "events.jsonl").read_text().splitlines()]
    telephone = any(e["kind"] == "carrier_stream_start" for e in events)
    if execution.get("validity") == "invalid" and review.validity != "invalid":
        raise ValueError(
            "Recorded simulator/infrastructure invalidity cannot become a target result"
        )
    if len(checks) != len(review.checks) or not set(checks).issubset(required_human):
        raise ValueError("Supply unique restaurant human checks only")
    if review.validity == "valid":
        metric = checks.get("counterpart_validity")
        if not metric or metric.status != "met":
            raise ValueError("Valid restaurant runs need an evidence-backed simulator review")
    if review.validity == "invalid":
        metric = checks.get("counterpart_validity")
        # An infrastructure-invalid result also needs no invented language judgment.
        if prior["validity"] != "invalid" and (not metric or metric.status != "not_met"):
            raise ValueError(
                "Identify invalid simulator behavior or a recorded infrastructure error"
            )
    for name, metric in checks.items():
        if metric.status in {"met", "not_met"}:
            suffixes = {ref.artifact_key.split("/", 2)[-1] for ref in metric.evidence}
            required = {"audio/played.wav", "audio/received.wav"}
            if telephone:
                required = {"audio/sent.wav", "audio/received.wav", "events.jsonl"}
            if name == "user_report_accuracy":
                required = {report_file, "business/final.json"}
            if not required.issubset(suffixes):
                raise ValueError("Human check lacks required captured evidence: " + name)
            if name == "user_report_accuracy" and not review.report_pointer:
                raise ValueError(
                    "Identify the actual provider-native post-call report; "
                    "missing report proof must remain uncertain"
                )
    if review.outcome == "passed":
        if not execution.get("termination_confirmed"):
            raise ValueError("A restaurant pass requires confirmed call termination")
        if prior["validity"] == "invalid":
            raise ValueError("A recorded invalid attempt cannot become a passing restaurant run")
        from voice_bench.evaluation.scoring import deterministic

        rules = {m.name: m for m in deterministic(directory)}
        required = set(RULE_CHECKS) - {"user_report_presence"}
        if report_file == "target/user-report.json":
            required.add("user_report_presence")
        if case.get("workflow_version") == "2":
            required.add("dining_terms_history")
        if (
            not required.issubset(rules)
            or any(rules[name].status != "met" for name in required)
            or any(
                rules[name].status != "met"
                for name in ("call_reliability", "evidence_completeness")
                if name in rules
            )
            or (
                "user_report_references" in rules
                and rules["user_report_references"].status == "not_met"
            )
        ):
            raise ValueError("A restaurant pass requires all deterministic evidence checks to pass")
        if set(checks) != set(required_human) or any(m.status != "met" for m in checks.values()):
            raise ValueError(
                "A restaurant pass requires every human check, including audio quality"
            )
        if not review.report_pointer:
            raise ValueError("Identify the actual provider-native post-call report")
    report = None
    if review.report_pointer:
        if review.report_pointer[0] in {"summary", "transcript"}:
            raise ValueError(
                "Dashboard summaries and call transcripts are not user-facing report delivery"
            )
        report = json.loads((directory / report_file).read_text())
        if report_file == "target/user-report.json" and (
            report.get("source") != "authenticated_rumik_tool"
            or report.get("run_id") != directory.name
            or list(review.report_pointer) != ["text"]
        ):
            raise ValueError("Report pointer must identify this attempt's target-authored text")
        try:
            for part in review.report_pointer:
                report = report[part]
        except (KeyError, IndexError, TypeError) as exc:
            raise ValueError("Report pointer does not identify saved provider content") from exc
        if not isinstance(report, str) or not report.strip():
            raise ValueError("Report pointer must identify nonempty provider text")
    if review.outcome == "failed":
        deterministic_failure = any(m["status"] == "not_met" for m in prior["metrics"])
        human_failure = any(
            m.status == "not_met" for n, m in checks.items() if n != "counterpart_validity"
        )
        if not deterministic_failure and not human_failure:
            raise ValueError("A failure needs an observed error, not missing proof")
    return report


def display_verdict(validity, outcome):
    if validity == "invalid":
        return "invalid"
    if validity == "valid" and outcome in {"passed", "failed"}:
        return {"passed": "pass", "failed": "fail"}[outcome]
    return "inconclusive"


def dimension_summary(case, metrics, events=(), *, reviewed=False):
    """Keep task and voice results separate; missing review cannot imply success."""
    by_name = {m["name"]: m["status"] for m in metrics}

    def combine(names):
        statuses = [by_name.get(name, "uncertain") for name in names]
        if "not_met" in statuses:
            return "not_met"
        return "met" if all(s == "met" for s in statuses) else "uncertain"

    expected = case["criteria"]["reservation_expected"]
    return {
        "task_completion": combine(
            [
                "task_state",
                "reservation_count",
                "reservation_history",
                "reservation_references",
                "reservation_evidence",
                "consent_alignment",
                "user_report_accuracy",
            ]
        ),
        "constraint_preservation": combine(["constraint_behavior", "policy_actions"]),
        "negotiation": combine(["negotiation_behavior"])
        if expected.get("dining_total_inr", 0)
        else "not_applicable",
        "dietary_requirements": combine(["dietary_understanding"])
        if expected.get("without_onion_garlic_guests", 0)
        else "not_applicable",
        "hinglish_quality": combine(["hinglish_quality"])
        if reviewed
        else "requires_listening_review",
        "simulator_validity": combine(["counterpart_validity", "counterpart_actions"]),
        "interruption_behavior": [
            {"event_id": e["event_id"], "result": e["challenge_result"]}
            for e in events
            if e["kind"] == "misread"
        ],
        "human_review_imported": reviewed,
    }
