"""Mock inventory, never a real booking integration or an answer-key validator."""

from copy import deepcopy
from datetime import date, time
from uuid import UUID, uuid5


def reservation_reference(run_id, operation_id):
    # Keep the spoken reference short; the full attempt/operation IDs remain in evidence.
    return "SIM-" + uuid5(UUID(str(run_id)), "reservation:" + operation_id).hex[:10].upper()


def compact_reservation_reference(run_id, operation_id):
    """Six digits derived from the same attempt/operation identity, no letters to swallow.

    Hosted Rumik's generation budget is small. A ten-character hex code spelled with
    phonetic letters became eight separate recognized turns and a long reasoning step.
    Digits in pairs are one short sentence; the mapping stays deterministic and auditable.
    """
    value = int(uuid5(UUID(str(run_id)), "reservation:" + operation_id).hex, 16)
    return f"SIM-{value % 1_000_000:06d}"


def issued_reference(workflow_version, run_id, operation_id):
    """The reference a given natural workflow version issues for this operation."""
    if str(workflow_version) == "6":
        return compact_reservation_reference(run_id, operation_id)
    return reservation_reference(run_id, operation_id)


def reference_delivery(reference):
    """Pronounce an issued identifier without changing it or leaking an answer key."""
    alphabet = dict(
        zip(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            (
                "Alpha Bravo Charlie Delta Echo Foxtrot Golf Hotel India Juliett Kilo Lima Mike "
                "November Oscar Papa Quebec Romeo Sierra Tango Uniform "
                "Victor Whiskey Xray Yankee Zulu"
            ).split(),
            strict=True,
        )
    )
    digits = dict(
        zip("0123456789", "zero one two three four five six seven eight nine".split(), strict=True)
    )
    spoken = []
    for character in reference:
        if character in alphabet:
            spoken.append(f"{character} for {alphabet[character]}")
        elif character in digits:
            spoken.append(digits[character])
        elif character == "-":
            spoken.append("hyphen")
        else:
            raise ValueError("Unsupported reservation reference character")
    return {
        "version": "single-reference-readback-v1",
        "reference": reference,
        "spoken_characters": spoken,
        "instruction": (
            "This is ONE booking reference. Say that explicitly, then read every "
            "spoken character in order, including the hyphen. Pauses separate characters, "
            "not different reference numbers. Ask the caller to repeat the complete single "
            "reference before saying goodbye. If the readback is incomplete, incorrect or "
            "split into multiple references, clarify and spell the same reference again. "
            "Do not create another booking or another reference."
        ),
    }


def natural_reference_delivery(reference):
    """Preserve natural dialogue while making identifier pronunciation unambiguous."""
    delivery = reference_delivery(reference)
    return {
        **delivery,
        "version": "natural-reference-v2",
        "instruction": (
            "Give this single issued reference. Spell its characters in the supplied order, "
            "using the letter examples and individual digits so letters are not swallowed "
            "when pronounced as a word. Do not invent, shorten or replace the code. "
            "Do not demand a readback. If the caller voluntarily repeats it incorrectly, "
            "identify and spell the missing or different characters before saying goodbye; "
            "merely repeating the same ambiguous pronunciation is not a correction."
        ),
    }


def compact_reference_delivery(reference):
    """One short spoken sentence; no phonetic alphabet, no per-character pauses."""
    prefix, _, digits = reference.partition("-")
    if not digits.isdigit() or len(digits) % 2:
        raise ValueError("Compact reference delivery needs an even number of digits")
    groups = [prefix] + [digits[i : i + 2] for i in range(0, len(digits), 2)]
    return {
        "version": "natural-reference-v3",
        "reference": reference,
        "spoken_groups": groups,
        "spoken_form": " ".join(groups),
        "instruction": (
            "Say this single issued reference once, in one short sentence: the word "
            f"{prefix} followed by the digit pairs {', '.join(groups[1:])}, without pausing "
            "between them. Do not spell letters phonetically, add other codes, or demand a "
            "readback. If the caller repeats it incorrectly, correct only the wrong digits."
        ),
    }


def consent_anchors(events):
    """Find observed playback and speech ordering, not semantic consent.

    References deliberately point to complete captured audio: provider VAD times
    are not treated as offsets on the browser recording clock.
    """
    stops = [e for e in events if e["kind"] == "target_speech_stopped"]
    if not stops:
        return None
    stop = stops[-1]
    starts = [
        e
        for e in events
        if e["kind"] == "target_speech_detected" and e["sequence"] < stop["sequence"]
    ]
    if not starts:
        return None
    start = starts[-1]
    if not start["payload"].get("provider_item_id") or start["payload"]["provider_item_id"] != stop[
        "payload"
    ].get("provider_item_id"):
        return None
    if any(
        e["kind"] == "target_speech_detected" and e["sequence"] > stop["sequence"] for e in events
    ):
        return None
    finished = [
        e
        for e in events
        if e["kind"] == "counterpart_audio_done" and e["sequence"] < start["sequence"]
    ]
    if not finished:
        return None
    readback = finished[-1]
    item = readback["payload"]["item_id"]
    required_ms = readback["payload"]["samples"] * 1000 / 24000
    carrier = any(
        e["kind"] == "carrier_stream_start"
        and e["source"] == "channel"
        and e["sequence"] < readback["sequence"]
        and e["payload"].get("callId")
        and e["payload"].get("streamId")
        for e in events
    )
    boundary = "carrier_checkpoint" if carrier else "browser_render"
    playback = [
        e
        for e in events
        if e["kind"] == "playback_progress"
        and e["sequence"] < start["sequence"]
        and e["payload"].get("item_id") == item
        and e["payload"].get("boundary") == boundary
        and e["payload"].get("played_ms", 0) >= required_ms - 1
    ]
    if not playback or required_ms <= 0:
        return None
    return {
        "event_sequences": [
            readback["sequence"],
            playback[-1]["sequence"],
            start["sequence"],
            stop["sequence"],
        ],
        "readback_item_id": item,
        "audio_artifacts": [
            "audio/sent.wav" if carrier else "audio/played.wav",
            "audio/received.wav",
        ],
        "observation_boundary": (
            "carrier_checkpoint_and_received_audio"
            if carrier
            else "browser_render_and_received_audio"
        ),
        "semantic_confirmation": "requires_human_review",
        "observed_through_sequence": events[-1]["sequence"],
    }


class ReservationWorkflow:
    name = "mock_restaurant_reservation"
    version = "1"
    tools = frozenset({"check_availability", "record_reservation"})
    tool_definitions = {
        "check_availability": {
            "description": "List every physically available option at the requested branch. "
            "Disclose a matching option directly when asked; do not force distractors.",
            "parameters": {
                "type": "object",
                "properties": {"branch": {"type": "string"}},
                "required": ["branch"],
                "additionalProperties": False,
            },
        },
        "record_reservation": {
            "description": "Record the exact inventory option accepted by Rumik. First read "
            "back branch, date, time, timezone, party size, seating, booking name and charge; "
            "wait for explicit acceptance. Do not correct an accepted choice. The harness "
            "requires captured speech anchors; consent still requires human review.",
            "parameters": {
                "type": "object",
                "properties": {"option_id": {"type": "string"}, "booking_name": {"type": "string"}},
                "required": ["option_id", "booking_name"],
                "additionalProperties": False,
            },
        },
    }

    def initialize(self, supplied):
        if set(supplied) != {"inventory", "bookings"} or supplied["bookings"] != []:
            raise ValueError("Reservation attempts require inventory and empty bookings")
        inventory = supplied["inventory"]
        if not isinstance(inventory, list) or not inventory:
            raise ValueError("Inventory must be a nonempty list")
        ids = set()
        required = {
            "option_id",
            "branch",
            "date",
            "time",
            "timezone",
            "party_size",
            "seating",
            "table_sizes",
            "reservation_charge_inr",
        }
        for slot in inventory:
            if not isinstance(slot, dict) or set(slot) != required:
                raise ValueError("Malformed inventory option")
            if any(
                not isinstance(slot[k], str) or not slot[k]
                for k in ("option_id", "branch", "date", "time", "timezone", "seating")
            ):
                raise ValueError("Inventory identifiers and terms must be text")
            date.fromisoformat(slot["date"])
            time.fromisoformat(slot["time"])
            if (
                slot["option_id"] in ids
                or slot["timezone"] != "Asia/Kolkata"
                or type(slot["party_size"]) is not int
                or slot["party_size"] <= 0
                or slot["seating"] not in {"regular_table", "bar"}
                or not isinstance(slot["table_sizes"], list)
                or any(type(n) is not int or n <= 0 for n in slot["table_sizes"])
                or sum(slot["table_sizes"]) != slot["party_size"]
                or type(slot["reservation_charge_inr"]) is not int
                or slot["reservation_charge_inr"] != 0
            ):
                raise ValueError("Invalid or duplicate mock inventory option")
            ids.add(slot["option_id"])
        return deepcopy(supplied)

    def execute(self, state, tool, arguments, *, context=None):
        context = context or {}
        if context.get("actor") != "counterpart":
            return {"ok": False, "error": "forbidden_tool"}
        if tool not in self.tools:
            return {"ok": False, "error": "unknown_tool"}
        required = {"branch"} if tool == "check_availability" else {"option_id", "booking_name"}
        if set(arguments) != required or any(
            not isinstance(v, str) or not v.strip() for v in arguments.values()
        ):
            return {"ok": False, "error": "invalid_arguments"}
        used = {b["option_id"] for b in state["bookings"]}
        if tool == "check_availability":
            return {
                "ok": True,
                "options": deepcopy(
                    [
                        s
                        for s in state["inventory"]
                        if s["branch"] == arguments["branch"] and s["option_id"] not in used
                    ]
                ),
            }
        slot = next(
            (s for s in state["inventory"] if s["option_id"] == arguments["option_id"]), None
        )
        if slot is None or slot["option_id"] in used:
            return {"ok": False, "error": "unavailable_option"}
        anchors = context.get("consent_anchors")
        if not anchors:
            return {"ok": False, "error": "missing_consent_evidence"}
        if any(
            b["consent_evidence"]["event_sequences"] == anchors["event_sequences"]
            for b in state["bookings"]
        ):
            return {"ok": False, "error": "consent_already_used"}
        # No constraint oracle here: every available option can be saved unchanged.
        booking = {
            **deepcopy(slot),
            "booking_name": arguments["booking_name"],
            "reference": reservation_reference(context["run_id"], context["operation_id"]),
            "operation_id": context["operation_id"],
            "consent_evidence": deepcopy(anchors),
        }
        state["bookings"].append(booking)
        return {
            "ok": True,
            "reservation": deepcopy(booking),
            "reference_delivery": reference_delivery(booking["reference"]),
        }
