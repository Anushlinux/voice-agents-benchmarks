"""Synthetic regression coverage; these tests make no benchmark quality claims."""

import json
from copy import deepcopy
from pathlib import Path
from uuid import uuid4

import pytest
from test_reservations import observations

from voice_bench.business.environment import BusinessService
from voice_bench.business.natural_restaurant import NaturalRestaurantWorkflow
from voice_bench.evaluation.natural_restaurant import natural_metrics
from voice_bench.evaluation.rubrics import apply_rubric
from voice_bench.evaluation.scoring import import_review, load_bundle, save_evaluation
from voice_bench.evidence.local import LocalEvidence
from voice_bench.restaurant_natural import convert_catalog, natural_rubric, preflight
from voice_bench.settings import load_config


@pytest.fixture
def catalog():
    option = dict(
        option_id="evening",
        branch="Khar",
        date="2026-10-01",
        time="19:00",
        timezone="Asia/Kolkata",
        party_size=4,
        seating="indoor_regular_table",
        table_count=1,
        table_capacity=4,
        booking_kind="table_only",
        menu=None,
        inclusions=[],
        total_inr=0,
        deposit_inr=0,
        remaining_due_inr=0,
        cancellation_fee_inr=0,
        mandatory_extras=[],
        without_onion_garlic_capacity=4,
    )
    options = [
        dict(option, option_id="early", time="17:00"),
        option,
        dict(option, option_id="conditional", time="19:30"),
    ]
    return {
        "shared_design": {
            "employee_rules": ["Answer received questions truthfully."],
            "language": "Speak naturally in Hinglish.",
        },
        "cases": [
            {
                "case_id": "synthetic-natural",
                "private_user_request": (
                    "Book Khar at 19:00 for four under Asha Rao; two without onion/garlic."
                ),
                "permissions": {
                    "may_make_payment": False,
                    "may_agree_deposit": False,
                    "may_agree_cancellation_fee": False,
                    "may_buy_extras": False,
                    "booking_name": "Asha Rao",
                },
                "user_constraints": dict(
                    date=option["date"],
                    party_size=4,
                    allowed_branches=["Khar"],
                    allowed_times=["19:00"],
                    seating=option["seating"],
                    one_table_together=True,
                    booking_kind="table_only",
                    max_total_inr=0,
                    required_without_onion_garlic_guests=2,
                ),
                "counterpart_brief": {
                    "role": "Restaurant employee",
                    "goal": "Handle requests",
                    "known_facts": {"restaurant_name": "Synthetic restaurant"},
                    "business_policies": [],
                    "business_options": options,
                    "offer_conditions": {"conditional": "price_or_menu_request"},
                },
                "initial_state": {"available_option_ids": [o["option_id"] for o in options]},
                "evaluation": {
                    "acceptable_outcome": "book",
                    "acceptable_option_ids": ["evening"],
                    "required_booking_count": 1,
                },
            }
        ],
    }


def query(**changes):
    return dict(
        branches=["Khar"],
        date="2026-10-01",
        party_size=4,
        earliest_time="19:00",
        latest_time="19:00",
        price_or_menu_alternative_requested=False,
        **changes,
    )


def context(sequence=0, operation="offer"):
    return dict(
        actor="counterpart",
        observed_through_sequence=sequence,
        operation_id=operation,
        run_id=str(uuid4()),
    )


def test_lookup_answers_requested_time_without_selecting_first_inventory_item(catalog):
    workflow = NaturalRestaurantWorkflow()
    case = convert_catalog(catalog)[0]
    state = workflow.initialize(case.initial_state)
    answer = workflow.execute(state, "check_availability", query(), context=context())
    assert [o["option_id"] for o in answer["matching_options"]] == ["evening"]
    assert [o["option_id"] for o in answer["other_time_options"]] == ["early"]
    assert not state["bookings"] and state["active_offer_id"] is None
    flipped = deepcopy(case.initial_state)
    flipped["options"].reverse()
    assert (
        workflow.execute(
            workflow.initialize(flipped), "check_availability", query(), context=context()
        )
        == answer
    )
    assert "private_user_request" not in json.dumps(answer)
    assert "acceptable_option_ids" not in json.dumps(workflow.tool_definitions)
    assert "business_options" not in case.counterpart.known_facts
    assert case.user_task.request not in json.dumps(case.counterpart.model_dump())


def test_tools_require_lookup_fresh_current_offer_and_dietary_capacity(catalog):
    workflow = NaturalRestaurantWorkflow()
    state = workflow.initialize(convert_catalog(catalog)[0].initial_state)
    offer_args = {"option_id": "evening", "without_onion_garlic_guests": 2}
    assert (
        workflow.execute(state, "offer_reservation", offer_args, context=context())["error"]
        == "availability_lookup_required"
    )
    workflow.execute(state, "check_availability", query(), context=context())
    assert (
        workflow.execute(
            state, "offer_reservation", dict(offer_args, option_id="conditional"), context=context()
        )["error"]
        == "availability_lookup_required"
    )
    assert (
        workflow.execute(
            state,
            "offer_reservation",
            dict(offer_args, without_onion_garlic_guests=5),
            context=context(),
        )["error"]
        == "dietary_capacity_unavailable"
    )
    first = workflow.execute(state, "offer_reservation", offer_args, context=context(10, "one"))[
        "offer"
    ]
    second = workflow.execute(state, "offer_reservation", offer_args, context=context(20, "two"))[
        "offer"
    ]
    assert (
        workflow.execute(
            state,
            "record_reservation",
            {"offer_id": first["offer_id"], "booking_name": "Asha Rao"},
            context=context(),
        )["error"]
        == "stale_offer"
    )
    args = {"offer_id": second["offer_id"], "booking_name": "Asha Rao"}
    stale = dict(context(), consent_anchors={"event_sequences": [19, 21, 22, 23]})
    assert (
        workflow.execute(state, "record_reservation", args, context=stale)["error"]
        == "fresh_conversation_evidence_required"
    )
    fresh = dict(context(operation="book"), consent_anchors={"event_sequences": [21, 22, 23, 24]})
    saved = workflow.execute(state, "record_reservation", args, context=fresh)
    assert saved["ok"] and saved["reservation"]["time"] == "19:00"
    assert saved["reference_delivery"]["version"] == "natural-reference-v1"
    assert (
        workflow.execute(state, "record_reservation", args, context=fresh)["error"]
        == "reservation_already_recorded"
    )


def test_conditional_policy_and_argument_validation(catalog):
    workflow = NaturalRestaurantWorkflow()
    state = workflow.initialize(convert_catalog(catalog)[0].initial_state)
    args = query()
    args["price_or_menu_alternative_requested"] = True
    answer = workflow.execute(state, "check_availability", args, context=context())
    assert "conditional" in [o["option_id"] for o in answer["other_time_options"]]
    for bad in [
        dict(args, party_size=True),
        dict(args, earliest_time="20:00"),
        dict(args, price_or_menu_alternative_requested="false"),
        dict(args, criteria={}),
    ]:
        assert (
            workflow.execute(state, "check_availability", bad, context=context())["error"]
            == "invalid_arguments"
        )
    assert (
        workflow.execute(state, "check_availability", args, context={"actor": "target"})["error"]
        == "forbidden_tool"
    )


def test_compiler_accepts_multiple_real_outcomes_and_rejects_contradictory_no_booking(catalog):
    spec = catalog["cases"][0]
    spec["user_constraints"]["allowed_times"].append("17:00")
    spec["evaluation"]["acceptable_option_ids"].append("early")
    assert len(convert_catalog(catalog)[0].criteria["acceptable_option_ids"]) == 2
    spec["evaluation"] = {
        "acceptable_outcome": "no_booking",
        "acceptable_option_ids": [],
        "required_booking_count": 0,
    }
    with pytest.raises(ValueError, match="contradicts"):
        convert_catalog(catalog)
    spec["user_constraints"]["allowed_times"] = ["21:00"]
    case = convert_catalog(catalog)[0]
    assert not next(
        m.applies for m in case.evaluation_rubric.metrics if m.name == "consent_alignment"
    )
    result = preflight(load_config(Path("configs/local.toml")), [case])
    assert result["provider_calls"] == 0 and result["counts"]["not_run"] == 1
    assert not result["live_qualified"]


@pytest.mark.asyncio
async def test_no_booking_report_absence_and_name_review_are_separate(catalog, tmp_path):
    case = convert_catalog(catalog)[0].model_dump(mode="json")
    sink = LocalEvidence(tmp_path, uuid4(), uuid4())
    final = NaturalRestaurantWorkflow().initialize(case["initial_state"])
    case["criteria"].update(required_booking_count=0, acceptable_option_ids=[])
    for filename, value in {
        "business/final.json": final,
        "config/case.json": case,
        "business/audit.json": [],
        "target/report-requests.json": [],
        "target/task-delivery.json": {"call_id": "call", "sha256": "task"},
        "result.json": {"termination_confirmed": True},
    }.items():
        await sink.json(filename, value)
    await sink.emit("controller", "start")
    await sink.finalize(sink.run_id)
    _, refs = load_bundle(sink.directory)
    metrics = {m.name: m for m in natural_metrics(sink.directory, case, refs, final, [])}
    assert metrics["task_state"].status == "met"
    assert metrics["booking_identity"].status == "not_applicable"
    assert metrics["user_report_presence"].status == "not_met"
    result = apply_rubric(natural_rubric(False), list(metrics.values()), "valid", reviewed=True)
    assert (
        next(m["status"] for m in result["metric_decisions"] if m["name"] == "user_report_accuracy")
        == "not_applicable"
    )
    altered = deepcopy(final)
    altered["bookings"] = [
        dict(final["options"][1], booking_name="आशा राव", without_onion_garlic_guests=2)
    ]
    case["criteria"].update(required_booking_count=1, acceptable_option_ids=["evening"])
    metrics = {m.name: m for m in natural_metrics(sink.directory, case, refs, altered, [])}
    assert metrics["task_state"].status == "met"
    assert metrics["booking_identity"].status == "uncertain"
    altered["bookings"][0]["time"] = "17:00"
    assert (
        next(
            m.status
            for m in natural_metrics(sink.directory, case, refs, altered, [])
            if m.name == "task_state"
        )
        == "not_met"
    )


@pytest.mark.asyncio
async def test_natural_review_cannot_override_invalid_execution_or_code_checks(catalog, tmp_path):
    case = convert_catalog(catalog)[0]
    sink = LocalEvidence(tmp_path, uuid4(), uuid4())
    await sink.json("config/case.json", case.model_dump(mode="json"))
    await sink.json("result.json", {"validity": "invalid"})
    await sink.emit("controller", "start")
    await sink.finalize(sink.run_id)
    _, refs = load_bundle(sink.directory)
    save_evaluation(sink.directory, "one", [], validity="valid")
    review = dict(
        reviewer="tester",
        evaluation_version="one",
        validity="valid",
        outcome="unresolved",
        explanation="Synthetic regression",
        evidence=[refs["result.json"].model_dump(mode="json")],
    )
    with pytest.raises(ValueError, match="invalid execution"):
        import_review(sink.directory, "two", review)
    review.update(
        validity="invalid",
        checks=[
            dict(
                name="task_state", status="met", explanation="Override", evidence=review["evidence"]
            )
        ],
    )
    with pytest.raises(ValueError, match="human checks"):
        import_review(sink.directory, "three", review)


def test_postgres_natural_workflow_isolation_idempotence_and_wrong_offer_evidence(store, catalog):
    from voice_bench.batches import make_plan

    case = convert_catalog(catalog)[0]
    plans = make_plan([case], ["browser"], repetitions=2)
    plan = plans[0]
    store.create_batch(
        plan.batch_id,
        {
            "plans": [p.model_dump(mode="json") for p in plans],
            "limits": {"max_attempts_per_case": 1},
        },
    )
    ids = [uuid4(), uuid4()]
    for run_id, run_plan in zip(ids, plans, strict=True):
        store.create_run(
            plan.batch_id,
            run_id,
            dict(
                plan_id=str(run_plan.plan_id),
                workflow=case.workflow,
                workflow_version=case.workflow_version,
                state=NaturalRestaurantWorkflow().initialize(case.initial_state),
                user_task=case.user_task.model_dump(mode="json"),
                expected_agent_id="test",
                tool_access={"counterpart": list(case.counterpart_tools), "target": []},
            ),
        )
        store.bind("rumik", str(run_id), run_id)
    service = BusinessService(store)
    run_id = ids[0]
    service.serve_user_task(str(run_id), "test")
    assert service.execute(run_id, "check_availability", query(), "lookup", actor="counterpart")[
        "ok"
    ]
    # Preserve physically valid but unauthorized times instead of consulting an answer key.
    offer = service.execute(
        run_id,
        "offer_reservation",
        {"option_id": "early", "without_onion_garlic_guests": 2},
        "offer",
        actor="counterpart",
        observations=observations(run_id),
    )["offer"]
    later = observations(run_id)
    for event in later:
        event["sequence"] += 10
    args = {"offer_id": offer["offer_id"], "booking_name": "Asha Rao"}
    saved = service.execute(
        run_id, "record_reservation", args, "book", actor="counterpart", observations=later
    )
    assert saved["ok"] and saved["reservation"]["time"] == "17:00"
    assert (
        service.execute(
            run_id, "record_reservation", args, "book", actor="counterpart", observations=later
        )
        == saved
    )
    assert len(store.run(run_id)["state"]["bookings"]) == 1
    assert not store.run(ids[1])["state"]["bookings"]
    assert store.run(run_id)["audit"][-1]["replay"]


def test_user_preference_order_is_structured_and_equal_choices_are_all_accepted(catalog):
    spec = catalog["cases"][0]
    spec["user_constraints"]["allowed_times"] = ["17:00", "19:00"]
    with pytest.raises(ValueError, match="contradicts"):
        convert_catalog(catalog)  # An unstated tie-breaker cannot exclude a valid option.
    spec["user_constraints"]["preference_order"] = ["Choose the earliest time."]
    with pytest.raises(ValueError, match="preference_ranking"):
        convert_catalog(catalog)
    spec["user_constraints"]["preference_ranking"] = [{"field": "time", "order": "earliest"}]
    spec["evaluation"]["acceptable_option_ids"] = ["early"]
    assert convert_catalog(catalog)[0].criteria["acceptable_option_ids"] == ["early"]


@pytest.mark.asyncio
async def test_actual_injected_events_and_incomplete_responses_reach_judge_timeline(tmp_path):
    from voice_bench.evaluation.timeline import build_timeline

    sink = LocalEvidence(tmp_path, uuid4(), uuid4())
    await sink.emit("caller", "conversation_event_requested", {"id": "historical-mistake"})
    await sink.emit("caller", "counterpart_incomplete", {"policy": "stop_invalid_without_retry"})
    await sink.finalize(sink.run_id)
    _, refs = load_bundle(sink.directory)
    timeline, sources = build_timeline(sink.directory, [], refs)
    assert [a["kind"] for a in timeline["event_anchors"]] == [
        "conversation_event_requested",
        "counterpart_incomplete",
    ]
    assert sources["event-0"].event_sequences == (0,)


def test_retired_challenges_remain_readable_but_cannot_run(catalog):
    from test_restaurant_hard import challenge

    from voice_bench.contracts import ExecutionCase

    value = convert_catalog(catalog)[0].model_dump(mode="json")
    # Historical tool-count challenges are parseable for audit, but unsafe for a new call.
    value["conversation_events"] = [challenge().model_dump(mode="json")]
    event = value["conversation_events"][0]
    event["trigger_tool"] = "check_availability"
    case = ExecutionCase.model_validate(value)
    with pytest.raises(ValueError, match="retired"):
        case.require_supported_execution()
