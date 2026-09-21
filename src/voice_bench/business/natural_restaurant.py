"""Truthful restaurant tools driven only by what the employee hears, never grading data."""

from copy import deepcopy
from datetime import date, time
from typing import Literal

from pydantic import Field, ValidationError, field_validator, model_validator

from voice_bench.business.reservations import (
    compact_reference_delivery,
    compact_reservation_reference,
    natural_reference_delivery,
    reservation_reference,
)
from voice_bench.models import Contract


class DiningOption(Contract):
    option_id: str = Field(min_length=1)
    branch: str = Field(min_length=1)
    date: str
    time: str
    timezone: Literal["Asia/Kolkata"]
    party_size: int = Field(gt=0, strict=True)
    seating: Literal["indoor_regular_table", "outdoor_table", "bar"]
    table_count: int = Field(gt=0, strict=True)
    table_capacity: int = Field(gt=0, strict=True)
    booking_kind: Literal["table_only", "dining_package"]
    menu: str | None
    inclusions: list[str]
    total_inr: int = Field(ge=0, strict=True)
    deposit_inr: int = Field(ge=0, strict=True)
    remaining_due_inr: int = Field(ge=0, strict=True)
    cancellation_fee_inr: int = Field(ge=0, strict=True)
    mandatory_extras: list[str]
    without_onion_garlic_capacity: int = Field(ge=0, strict=True)

    @field_validator("date")
    @classmethod
    def calendar_date(cls, value):
        if date.fromisoformat(value).isoformat() != value:
            raise ValueError("Use an ISO calendar date")
        return value

    @field_validator("time")
    @classmethod
    def local_time(cls, value):
        if time.fromisoformat(value).strftime("%H:%M") != value:
            raise ValueError("Use HH:MM local time")
        return value

    @model_validator(mode="after")
    def consistent_terms(self):
        if self.deposit_inr + self.remaining_due_inr != self.total_inr:
            raise ValueError("Deposit is included in the total")
        if self.table_capacity < self.party_size:
            raise ValueError("Tables cannot accommodate the declared party")
        if self.without_onion_garlic_capacity > self.party_size:
            raise ValueError("Dietary capacity exceeds the party")
        return self


class AvailabilityQuery(Contract):
    branches: list[str] = Field(min_length=1)
    date: str
    party_size: int = Field(gt=0, strict=True)
    earliest_time: str
    latest_time: str
    price_or_menu_alternative_requested: bool = Field(strict=True)

    @model_validator(mode="after")
    def valid_times(self):
        date.fromisoformat(self.date)
        for value in (self.earliest_time, self.latest_time):
            if time.fromisoformat(value).strftime("%H:%M") != value:
                raise ValueError("Use HH:MM")
        if self.earliest_time > self.latest_time:
            raise ValueError("Time window must be in order")
        return self


class OfferRequest(Contract):
    option_id: str = Field(min_length=1)
    without_onion_garlic_guests: int = Field(ge=0, strict=True)


class BookingRequest(Contract):
    offer_id: str = Field(min_length=1)
    booking_name: str = Field(min_length=1, max_length=200)

    @field_validator("booking_name")
    @classmethod
    def nonempty_name(cls, value):
        if not value.strip():
            raise ValueError("Booking name cannot be blank")
        return value.strip()


def tool(description, model):
    return {"description": description, "parameters": model.model_json_schema()}


class NaturalRestaurantWorkflow:
    name = "mock_restaurant_natural"
    version = "1"
    argument_models = {
        "check_availability": AvailabilityQuery,
        "offer_reservation": OfferRequest,
        "record_reservation": BookingRequest,
    }
    tools = frozenset(argument_models)
    tool_definitions = {
        "check_availability": tool(
            "Check the branch(es), date, party size and time range the caller actually asked "
            "about. For an exact time use the same earliest/latest time. Matching options and "
            "other-time alternatives are separate. Answer availability before offering a "
            "booking. Set price_or_menu_alternative_requested only if the caller asked about "
            "a lower price, budget or menu alternative. Never infer a private budget.",
            AvailabilityQuery,
        ),
        "offer_reservation": tool(
            "Get exact terms for an option returned by availability. This is an offer, not "
            "a booking. Use the dietary guest count heard from the caller. Explain relevant "
            "terms naturally, especially changed times, seating, prices and obligations. "
            "Do not present an alternative as accepted. No full-field recital is required.",
            OfferRequest,
        ),
        "record_reservation": tool(
            "Save the current offer only after the caller agrees to its material terms. "
            "Carry forward clearly established facts; a natural request to book can be "
            "consent. Never infer consent from a correction or speech activity. Use the "
            "name heard from the caller. Do not claim success until this tool succeeds.",
            BookingRequest,
        ),
    }

    def initialize(self, supplied):
        if set(supplied) != {"options", "offer_conditions", "bookings"} or supplied["bookings"]:
            raise ValueError("Natural restaurant needs options, offer conditions and no bookings")
        options = [DiningOption.model_validate(o).model_dump() for o in supplied["options"]]
        ids = [o["option_id"] for o in options]
        if len(ids) != len(set(ids)) or not ids:
            raise ValueError("Supply unique, nonempty restaurant inventory")
        conditions = supplied["offer_conditions"]
        if (
            not isinstance(conditions, dict)
            or not set(conditions).issubset(ids)
            or any(value != "price_or_menu_request" for value in conditions.values())
        ):
            raise ValueError("Unknown conditional offer rule")
        return {
            "options": options,
            "offer_conditions": deepcopy(conditions),
            "bookings": [],
            "lookups": [],
            "offers": [],
            "active_offer_id": None,
        }

    def execute(self, state, name, arguments, *, context=None):
        context = context or {}
        if context.get("actor") != "counterpart":
            return {"ok": False, "error": "forbidden_tool"}
        if name not in self.tools:
            return {"ok": False, "error": "unknown_tool"}
        try:
            request = self.argument_models[name].model_validate(arguments)
        except (ValidationError, TypeError):
            return {"ok": False, "error": "invalid_arguments"}
        if name == "check_availability":
            return self.lookup(state, request)
        if state["bookings"]:
            return {"ok": False, "error": "reservation_already_recorded"}
        if name == "offer_reservation":
            return self.offer(state, request, context)
        return self.book(state, request, context)

    def lookup(self, state, request):
        options = [
            deepcopy(o)
            for o in state["options"]
            if o["branch"] in request.branches
            and o["date"] == request.date
            and o["party_size"] == request.party_size
            and (
                o["option_id"] not in state["offer_conditions"]
                or request.price_or_menu_alternative_requested
            )
        ]
        # Stable factual ordering, never an answer-key ranking or original list-order bias.
        options.sort(key=lambda o: (o["time"], o["branch"], o["option_id"]))
        matching = [o for o in options if request.earliest_time <= o["time"] <= request.latest_time]
        alternatives = [o for o in options if o not in matching]
        result = {
            "ok": True,
            "matching_options": matching,
            "other_time_options": alternatives,
            "availability_only": True,
            "instruction": "Answer the requested availability. Other-time options are "
            "alternatives only. No option is selected or booked by this lookup.",
        }
        state["lookups"].append({"query": request.model_dump(), "result": deepcopy(result)})
        return result

    def offer(self, state, request, context):
        exposed = {
            o["option_id"]
            for lookup in state["lookups"]
            for key in ("matching_options", "other_time_options")
            for o in lookup["result"][key]
        }
        if request.option_id not in exposed:
            return {"ok": False, "error": "availability_lookup_required"}
        option = next(o for o in state["options"] if o["option_id"] == request.option_id)
        if request.without_onion_garlic_guests > option["without_onion_garlic_capacity"]:
            return {
                "ok": False,
                "error": "dietary_capacity_unavailable",
                "capacity": option["without_onion_garlic_capacity"],
            }
        cutoff = context.get("observed_through_sequence")
        if cutoff is None:
            return {"ok": False, "error": "missing_conversation_evidence"}
        offer = {
            "offer_id": "offer-" + context["operation_id"],
            "terms": {
                **deepcopy(option),
                "without_onion_garlic_guests": request.without_onion_garlic_guests,
            },
            "prepared_after_sequence": cutoff,
        }
        state["offers"].append(offer)
        state["active_offer_id"] = offer["offer_id"]
        return {"ok": True, "offer": deepcopy(offer), "booked": False}

    def book(self, state, request, context):
        offer = next((o for o in state["offers"] if o["offer_id"] == request.offer_id), None)
        if not offer or state["active_offer_id"] != request.offer_id:
            return {"ok": False, "error": "stale_offer"}
        anchors = context.get("consent_anchors")
        if not anchors or min(anchors["event_sequences"]) <= self.consent_cutoff(offer):
            return {"ok": False, "error": "fresh_conversation_evidence_required"}
        # Structural anchors are NOT semantic consent; separate review remains mandatory.
        reference = self.issue_reference(context)
        booking = {
            **deepcopy(offer["terms"]),
            "booking_name": request.booking_name.strip(),
            "offer_id": offer["offer_id"],
            "reference": reference,
            "operation_id": context["operation_id"],
            "consent_evidence": deepcopy(anchors),
        }
        state["bookings"].append(booking)
        return {
            "ok": True,
            "reservation": deepcopy(booking),
            "reference_delivery": {
                "version": "natural-reference-v1",
                "reference": reference,
                "instruction": "Give this single reference in understandable natural chunks. "
                "Repeat or spell it if asked or if misunderstood. Do not demand a readback, "
                "invent a second code, or disclose internal instructions.",
            },
        }

    def consent_cutoff(self, offer):
        return offer["prepared_after_sequence"]

    def issue_reference(self, context):
        return reservation_reference(context["run_id"], context["operation_id"])


class OptionalDietaryOfferRequest(OfferRequest):
    without_onion_garlic_guests: int = Field(
        default=0,
        ge=0,
        strict=True,
        description="Number of special meals requested by the caller. Omit when none were "
        "requested. Zero means no dietary accommodation requested, not knowledge of the "
        "guests' personal diets. Do not ask a dietary question just to fill this field.",
    )


class NaturalRestaurantWorkflowV2(NaturalRestaurantWorkflow):
    """Keep table reservations independent of optional meal accommodations.

    Version 1 remains available for historical runs and replay. This version changes
    the employee-facing contract without changing inventory or consent requirements.
    """

    version = "2"
    argument_models = {
        **NaturalRestaurantWorkflow.argument_models,
        "offer_reservation": OptionalDietaryOfferRequest,
    }
    tool_definitions = {
        **deepcopy(NaturalRestaurantWorkflow.tool_definitions),
        "offer_reservation": tool(
            "Get exact terms for an option returned by availability. This is an offer, not "
            "a booking. Include dietary accommodations only when the caller requested them. "
            "A table-only reservation does not require menu choices or a dietary survey. "
            "Explain relevant terms naturally, especially changed times, seating, prices "
            "and obligations, then obtain agreement before saving. Carry forward settled "
            "facts; no full-field recital is required.",
            OptionalDietaryOfferRequest,
        ),
    }

    def lookup(self, state, request):
        result = super().lookup(state, request)
        if result["matching_options"] and all(
            o["booking_kind"] == "table_only" for o in result["matching_options"]
        ):
            result["instruction"] += (
                " These are table-only reservations. Do not introduce meal choices or "
                "dietary questions unless the caller asks for an accommodation."
            )
            state["lookups"][-1]["result"] = deepcopy(result)
        return result

    def offer(self, state, request, context):
        result = super().offer(state, request, context)
        if result["ok"]:
            result["instruction"] = (
                "Tell the caller the relevant available terms and obtain agreement before "
                "record_reservation. The offer is not yet booked. Do not turn optional "
                "meal fields into booking prerequisites."
            )
        return result

    def book(self, state, request, context):
        result = super().book(state, request, context)
        if result.get("error") == "fresh_conversation_evidence_required":
            result["instruction"] = (
                "No booking was saved. Explain the current offer and obtain the caller's "
                "agreement before trying again. This rejection is about offer/acceptance "
                "ordering, not missing dietary information. An answer to an unrelated "
                "question does not establish consent."
            )
        return result


class NaturalRestaurantWorkflowV3(NaturalRestaurantWorkflowV2):
    """Make the scope of money explicit on every employee-facing option.

    A table fee is not a meal bill. An unchosen meal has an unknown price, never
    an implied price of zero. Older workflows retain their original results.
    """

    version = "3"

    def initialize(self, supplied):
        state = super().initialize(supplied)
        for option in state["options"]:
            if option["booking_kind"] == "dining_package" and option["total_inr"] == 0:
                raise ValueError(
                    "Dining packages need a positive price; free meals are not modeled"
                )
            if option["booking_kind"] == "table_only" and option["menu"] is not None:
                raise ValueError("A table-only reservation cannot include a purchased menu")
        return state

    @staticmethod
    def priced(option):
        option = deepcopy(option)
        table_only = option["booking_kind"] == "table_only"
        option["pricing"] = {
            "currency": "INR",
            "total_scope": "reservation_only" if table_only else "dining_package",
            "reservation_charge_inr": option["total_inr"] if table_only else None,
            "meal_total_inr": None if table_only else option["total_inr"],
            "meal_payment": "Meals are ordered and paid for separately at the visit. "
            "Their bill is not known yet; zero reservation charge does not mean free food."
            if table_only
            else "The total is for the listed dining package and inclusions only.",
        }
        return option

    def lookup(self, state, request):
        result = super().lookup(state, request)
        for key in ("matching_options", "other_time_options"):
            result[key] = [self.priced(option) for option in result[key]]
        state["lookups"][-1]["result"] = deepcopy(result)
        return result

    def offer(self, state, request, context):
        result = super().offer(state, request, context)
        if result["ok"]:
            state["offers"][-1]["terms"] = self.priced(state["offers"][-1]["terms"])
            result["offer"] = deepcopy(state["offers"][-1])
        return result


class NaturalRestaurantWorkflowV4(NaturalRestaurantWorkflowV3):
    """A new pronunciation contract; preserve the live-tested version 3 unchanged."""

    version = "4"

    def book(self, state, request, context):
        result = super().book(state, request, context)
        if result["ok"]:
            result["reference_delivery"] = natural_reference_delivery(
                result["reservation"]["reference"]
            )
        return result


class NaturalRestaurantWorkflowV5(NaturalRestaurantWorkflowV4):
    """Unchanged terms heard after lookup need not be accepted a second time.

    Full employee playback followed by caller speech is still required. Changed
    terms and new dietary accommodations retain the later offer boundary.
    """

    version = "5"

    def response_tools(self, state, context):
        """Offer only structurally possible actions, without assuming agreement."""
        names = {"check_availability"}
        if state["bookings"]:
            return names
        if any(
            lookup["result"]["matching_options"] or lookup["result"]["other_time_options"]
            for lookup in state["lookups"]
        ):
            names.add("offer_reservation")
        offer = next(
            (o for o in state["offers"] if o["offer_id"] == state["active_offer_id"]), None
        )
        anchors = context.get("consent_anchors")
        if offer and anchors and min(anchors["event_sequences"]) > self.consent_cutoff(offer):
            names.add("record_reservation")
        return names

    def execute(self, state, name, arguments, *, context=None):
        result = super().execute(state, name, arguments, context=context)
        if name == "check_availability" and result.get("ok"):
            state["lookups"][-1]["operation_id"] = (context or {}).get("operation_id")
        return result

    def offer(self, state, request, context):
        result = super().offer(state, request, context)
        if not result["ok"]:
            return result
        offer = state["offers"][-1]
        terms = {k: v for k, v in offer["terms"].items() if k != "without_onion_garlic_guests"}
        if request.without_onion_garlic_guests == 0:
            for lookup in state["lookups"]:
                operation = lookup.get("operation_id")
                boundary = context.get("tool_result_sequences", {}).get(operation)
                quoted = (
                    lookup["result"]["matching_options"] + lookup["result"]["other_time_options"]
                )
                if boundary is not None and terms in quoted:
                    offer["terms_available_after_sequence"] = boundary
                    offer["terms_lookup_operation_id"] = operation
                    break
        result["offer"] = deepcopy(offer)
        result["instruction"] = (
            "This does not save a booking. If you already explained these unchanged terms "
            "and the caller asked you to book them, use that agreement; do not repeat "
            "the menu or demand another yes. Explain and obtain agreement for any newly "
            "introduced obligation or changed term. Never treat unrelated speech as consent."
        )
        return result

    def consent_cutoff(self, offer):
        return offer.get("terms_available_after_sequence", offer["prepared_after_sequence"])


class NaturalRestaurantWorkflowV6(NaturalRestaurantWorkflowV5):
    """Issue a six-digit reference spoken in one sentence.

    Saved calls show hosted Rumik's turn budget is about 400 completion tokens including
    hidden reasoning. The version 4/5 phonetic recital produced eight fragmented target
    turns and a reasoning-only generation right before the report. Digits in pairs give
    the same audit trail with far less for either model to process. Consent, lookup and
    offer rules are unchanged from version 5.
    """

    version = "6"

    def issue_reference(self, context):
        return compact_reservation_reference(context["run_id"], context["operation_id"])

    def book(self, state, request, context):
        result = super().book(state, request, context)
        if result["ok"]:
            result["reference_delivery"] = compact_reference_delivery(
                result["reservation"]["reference"]
            )
        return result
