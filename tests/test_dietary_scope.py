"""The employee can reserve a table without inventing personal dietary facts."""

from copy import deepcopy

import pytest
from test_natural_restaurant import catalog as catalog
from test_natural_restaurant import context, query

from voice_bench.business.environment import WORKFLOWS
from voice_bench.business.natural_restaurant import (
    NaturalRestaurantWorkflow,
    NaturalRestaurantWorkflowV2,
)
from voice_bench.restaurant_natural import convert_catalog, user_instructions


def ready(catalog):
    case = convert_catalog(catalog)[0]
    workflow = WORKFLOWS[(case.workflow, case.workflow_version)]
    state = workflow.initialize(case.initial_state)
    workflow.execute(state, "check_availability", query(), context=context())
    return workflow, state


def test_table_only_offer_does_not_require_dietary_survey(catalog):
    workflow, state = ready(catalog)
    assert isinstance(workflow, NaturalRestaurantWorkflowV2)
    schema = workflow.tool_definitions["offer_reservation"]["parameters"]
    assert schema["required"] == ["option_id"]
    offer = workflow.execute(
        state, "offer_reservation", {"option_id": "evening"}, context=context(10)
    )
    assert offer["ok"]
    # Zero requests does not assert what the guests eat; it promises no special meals.
    assert offer["offer"]["terms"]["without_onion_garlic_guests"] == 0
    assert not state["bookings"]
    assert "table-only" in state["lookups"][-1]["result"]["instruction"]


@pytest.mark.parametrize("count,expected", [(2, True), (5, False), (-1, False), (True, False)])
def test_requested_dietary_accommodations_still_require_capacity(catalog, count, expected):
    workflow, state = ready(catalog)
    result = workflow.execute(
        state,
        "offer_reservation",
        {"option_id": "evening", "without_onion_garlic_guests": count},
        context=context(10),
    )
    assert result["ok"] is expected
    if expected:
        assert result["offer"]["terms"]["without_onion_garlic_guests"] == count
    else:
        assert state["offers"] == []


def test_missing_acceptance_is_explained_without_relaxing_booking_guard(catalog):
    workflow, state = ready(catalog)
    offer = workflow.execute(
        state, "offer_reservation", {"option_id": "evening"}, context=context(10)
    )["offer"]
    arguments = {"offer_id": offer["offer_id"], "booking_name": "Asha Rao"}
    rejected = workflow.execute(state, "record_reservation", arguments, context=context())
    assert rejected["error"] == "fresh_conversation_evidence_required"
    assert "offer/acceptance" in rejected["instruction"]
    assert "not missing dietary information" in rejected["instruction"]
    assert state["bookings"] == []
    accepted = workflow.execute(
        state,
        "record_reservation",
        arguments,
        context=dict(context(operation="book"), consent_anchors={"event_sequences": [11, 12]}),
    )
    assert accepted["ok"]
    assert len(state["bookings"]) == 1


def test_version_one_is_preserved_and_new_cases_keep_private_dietary_authority(catalog):
    original = deepcopy(catalog)
    case = convert_catalog(catalog)[0]
    assert catalog == original
    assert case.workflow_version == "5" and case.version.startswith("8-")
    assert case.completion == "target_report_then_conversation_end"
    assert "2 guests need food without onion and garlic." in case.user_task.constraints
    assert case.criteria["dietary_guests"] == 2
    assert case.user_task.request not in str(case.counterpart.model_dump())
    old = WORKFLOWS[(case.workflow, "1")]
    assert type(old) is NaturalRestaurantWorkflow
    assert (
        "without_onion_garlic_guests"
        in old.tool_definitions["offer_reservation"]["parameters"]["required"]
    )
    state = old.initialize(case.initial_state)
    old.execute(state, "check_availability", query(), context=context())
    assert old.execute(state, "offer_reservation", {"option_id": "evening"}, context=context()) == {
        "ok": False,
        "error": "invalid_arguments",
    }


def test_free_table_does_not_mean_free_meals_or_authorize_a_purchase(catalog):
    spec = catalog["cases"][0]
    spec["permissions"]["may_agree_pay_at_visit_total_inr_up_to"] = 0
    case = convert_catalog(catalog)[0]
    words = " ".join(case.user_task.constraints + case.user_task.permissions)
    assert "total reservation charge must not exceed INR 0" in words
    assert "does not require free meals" in words
    assert "Reservation-related charges due at the visit may total at most INR 0" in words
    assert "Do not buy meals or agree to a mandatory dining package" in words
    assert "Do not make any payment" in words
    assert case.criteria["user_constraints"]["max_total_inr"] == 0
    package = {**spec["user_constraints"], "booking_kind": "dining_package", "max_total_inr": 2000}
    constraints, permissions = user_instructions(package, spec["permissions"])
    package_words = " ".join(constraints + permissions)
    assert "total dining-package charge must not exceed INR 2000" in package_words
    assert "does not require free meals" not in package_words


def test_price_scope_reaches_lookup_offer_and_saved_booking(catalog):
    workflow, state = ready(catalog)
    terms = state["lookups"][-1]["result"]["matching_options"][0]
    assert terms["pricing"]["reservation_charge_inr"] == 0
    assert terms["pricing"]["meal_total_inr"] is None
    assert terms["pricing"]["total_scope"] == "reservation_only"
    offered = workflow.execute(
        state, "offer_reservation", {"option_id": "evening"}, context=context(10)
    )
    saved = workflow.execute(
        state,
        "record_reservation",
        {"offer_id": offered["offer"]["offer_id"], "booking_name": "Asha Rao"},
        context=dict(context(operation="book"), consent_anchors={"event_sequences": [11, 12]}),
    )
    assert saved["ok"]
    assert saved["reservation"]["pricing"] == terms["pricing"]
    assert saved["reference_delivery"]["version"] == "natural-reference-v2"
    assert type(WORKFLOWS[(workflow.name, "2")]) is NaturalRestaurantWorkflowV2


def test_zero_priced_meal_package_is_rejected_before_a_call(catalog):
    for option in catalog["cases"][0]["counterpart_brief"]["business_options"]:
        option["booking_kind"] = "dining_package"
    with pytest.raises(ValueError, match="positive price"):
        convert_catalog(catalog)


def test_paid_package_reports_the_full_party_meal_price(catalog):
    from voice_bench.business.natural_restaurant import NaturalRestaurantWorkflowV3

    option = deepcopy(catalog["cases"][0]["counterpart_brief"]["business_options"][0])
    option.update(
        booking_kind="dining_package", total_inr=3600, deposit_inr=600, remaining_due_inr=3000
    )
    workflow = NaturalRestaurantWorkflowV3()
    state = workflow.initialize({"options": [option], "offer_conditions": {}, "bookings": []})
    result = workflow.execute(state, "check_availability", query(), context=context())
    priced = result["other_time_options"][0]
    assert priced["pricing"]["meal_total_inr"] == 3600
    assert priced["pricing"]["total_scope"] == "dining_package"
    assert (
        priced["deposit_inr"] + priced["remaining_due_inr"] == priced["pricing"]["meal_total_inr"]
    )


def test_reference_guidance_preserves_every_character_and_historical_workflow():
    from voice_bench.business.natural_restaurant import NaturalRestaurantWorkflowV3
    from voice_bench.business.reservations import natural_reference_delivery

    code = "SIM-AF0351DC2A"
    delivery = natural_reference_delivery(code)
    assert delivery["reference"] == code
    assert delivery["spoken_characters"] == [
        "S for Sierra",
        "I for India",
        "M for Mike",
        "hyphen",
        "A for Alpha",
        "F for Foxtrot",
        "zero",
        "three",
        "five",
        "one",
        "D for Delta",
        "C for Charlie",
        "two",
        "A for Alpha",
    ]
    assert "Do not demand a readback" in delivery["instruction"]
    assert "missing or different characters" in delivery["instruction"]
    assert type(WORKFLOWS[("mock_restaurant_natural", "3")]) is NaturalRestaurantWorkflowV3
