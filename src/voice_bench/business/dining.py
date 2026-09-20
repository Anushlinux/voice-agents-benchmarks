"""Version 2: fictional quotes and dining arrangements, with fresh consent on each revision."""

from copy import deepcopy
from uuid import UUID, uuid5

from voice_bench.business.reservations import ReservationWorkflow


def definition(description, properties):
    return {
        "description": description,
        "parameters": {
            "type": "object",
            "properties": properties,
            "required": list(properties),
            "additionalProperties": False,
        },
    }


class DiningWorkflow(ReservationWorkflow):
    version = "2"
    tool_definitions = {
        "check_availability": ReservationWorkflow.tool_definitions["check_availability"],
        "quote_reservation": definition(
            "Create the opening all-inclusive offer for an available option. "
            "No reservation is made.",
            {"option_id": {"type": "string"}},
        ),
        "counteroffer": definition(
            "Evaluate the caller's counteroffer against restaurant policy. This replaces the "
            "active quote on success but makes no booking. Never infer the caller's budget.",
            {"quote_id": {"type": "string"}, "total_inr": {"type": "integer", "minimum": 0}},
        ),
        "set_dietary_requirements": definition(
            "Confirm how many guests need food WITHOUT BOTH onion and garlic. Vegetarian alone "
            "does not imply this. Replaces the quote; requires a fresh readback and acceptance.",
            {
                "quote_id": {"type": "string"},
                "without_onion_garlic_guests": {"type": "integer", "minimum": 0},
            },
        ),
        "prepare_confirmation": definition(
            "Prepare exact current terms for readback; not a booking. Read every term and wait "
            "for explicit acceptance. After any correction or changed terms, call this again "
            "and provide a fresh accurate readback. "
            "Never book against an intentionally wrong readback.",
            {"quote_id": {"type": "string"}, "booking_name": {"type": "string"}},
        ),
        "record_reservation": definition(
            "Save precisely the current prepared terms after a fresh complete accurate readback "
            "and spoken acceptance. Old quote/confirmation IDs and old consent "
            "cannot authorize it.",
            {"confirmation_id": {"type": "string"}},
        ),
    }
    tools = frozenset(tool_definitions)

    def initialize(self, supplied):
        if set(supplied) != {"inventory", "bookings", "dining_policy"}:
            raise ValueError("Dining input needs inventory, empty bookings and dining policy")
        base = super().initialize({k: supplied[k] for k in ("inventory", "bookings")})
        policy = supplied["dining_policy"]
        required = {"opening_total_inr", "minimum_total_inr", "max_without_onion_garlic_guests"}
        if (
            not isinstance(policy, dict)
            or set(policy) != required
            or any(type(v) is not int or v < 0 for v in policy.values())
            or policy["minimum_total_inr"] > policy["opening_total_inr"]
        ):
            raise ValueError("Invalid fictional dining policy")
        return {
            **base,
            "dining_policy": deepcopy(policy),
            "quotes": [],
            "confirmations": [],
            "active_quote_id": None,
            "active_confirmation_id": None,
        }

    @staticmethod
    def identity(context, prefix):
        return prefix + uuid5(UUID(context["run_id"]), prefix + context["operation_id"]).hex[:12]

    def new_quote(self, state, terms, context):
        quote = {**deepcopy(terms), "quote_id": self.identity(context, "Q-")}
        state["quotes"].append(quote)
        state["active_quote_id"] = quote["quote_id"]
        state["active_confirmation_id"] = None
        return {"ok": True, "quote": deepcopy(quote)}

    def execute(self, state, tool, arguments, *, context=None):
        context = context or {}
        if context.get("actor") != "counterpart":
            return {"ok": False, "error": "forbidden_tool"}
        if tool not in self.tools:
            return {"ok": False, "error": "unknown_tool"}
        schema = self.tool_definitions[tool]["parameters"]["properties"]
        if not isinstance(arguments, dict) or set(arguments) != set(schema):
            return {"ok": False, "error": "invalid_arguments"}
        for key, spec in schema.items():
            value = arguments[key]
            if (
                spec["type"] == "string"
                and (not isinstance(value, str) or not value.strip())
                or spec["type"] == "integer"
                and (type(value) is not int or value < 0)
            ):
                return {"ok": False, "error": "invalid_arguments"}
        if tool == "check_availability":
            return super().execute(state, tool, arguments, context=context)
        if state["bookings"]:
            return {"ok": False, "error": "reservation_already_recorded"}
        if tool == "quote_reservation":
            option = next(
                (s for s in state["inventory"] if s["option_id"] == arguments["option_id"]), None
            )
            if option is None:
                return {"ok": False, "error": "unavailable_option"}
            return self.new_quote(
                state,
                {
                    **option,
                    "dining_total_inr": state["dining_policy"]["opening_total_inr"],
                    "without_onion_garlic_guests": 0,
                    "all_inclusive": True,
                    "deposit_inr": 0,
                    "cancellation_fee_inr": 0,
                    "payment_status": "not_requested",
                },
                context,
            )
        if tool == "record_reservation":
            return self.record(state, arguments, context)
        quote = next((q for q in state["quotes"] if q["quote_id"] == arguments["quote_id"]), None)
        if quote is None or quote["quote_id"] != state["active_quote_id"]:
            return {"ok": False, "error": "stale_quote"}
        if tool == "counteroffer":
            total = arguments["total_inr"]
            policy = state["dining_policy"]
            if not policy["minimum_total_inr"] <= total <= quote["dining_total_inr"]:
                return {"ok": False, "error": "offer_outside_policy"}
            return self.new_quote(state, {**quote, "dining_total_inr": total}, context)
        if tool == "set_dietary_requirements":
            count = arguments["without_onion_garlic_guests"]
            if count > min(
                quote["party_size"], state["dining_policy"]["max_without_onion_garlic_guests"]
            ):
                return {"ok": False, "error": "dietary_capacity_unavailable"}
            return self.new_quote(state, {**quote, "without_onion_garlic_guests": count}, context)
        cutoff = context.get("observed_through_sequence")
        if cutoff is None:
            return {"ok": False, "error": "missing_confirmation_evidence"}
        confirmation = {
            "confirmation_id": self.identity(context, "C-"),
            "terms": {**deepcopy(quote), "booking_name": arguments["booking_name"]},
            "prepared_after_sequence": cutoff,
        }
        state["confirmations"].append(confirmation)
        state["active_confirmation_id"] = confirmation["confirmation_id"]
        return {"ok": True, "confirmation": deepcopy(confirmation)}

    def record(self, state, arguments, context):
        confirmation = next(
            (
                c
                for c in state["confirmations"]
                if c["confirmation_id"] == arguments["confirmation_id"]
            ),
            None,
        )
        if (
            not confirmation
            or state["active_confirmation_id"] != arguments["confirmation_id"]
            or confirmation["terms"]["quote_id"] != state["active_quote_id"]
        ):
            return {"ok": False, "error": "stale_confirmation"}
        anchors = context.get("consent_anchors")
        if (
            not anchors
            or min(anchors["event_sequences"]) <= confirmation["prepared_after_sequence"]
        ):
            return {"ok": False, "error": "fresh_consent_required"}
        terms = confirmation["terms"]
        # Run v1 physical/consent validation directly, using its two-argument tool schema.
        base = ReservationWorkflow()
        result = base.execute(
            state,
            "record_reservation",
            {
                "option_id": terms["option_id"],
                "booking_name": terms["booking_name"],
            },
            context=context,
        )
        if result["ok"]:
            state["bookings"][-1].update(deepcopy(terms))
            state["bookings"][-1]["confirmation_id"] = confirmation["confirmation_id"]
            result["reservation"] = deepcopy(state["bookings"][-1])
        return result
