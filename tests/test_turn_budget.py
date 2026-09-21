"""Keep each hosted target turn small: short references, short prompts, one-sentence delivery.

These tests pin the harness-owned inputs that inflated Rumik's per-turn generation in saved
calls. They cannot prove the hosted model stays under its budget; only a live call can.
"""

import asyncio
import json
import re
from copy import deepcopy
from uuid import uuid4

import pytest
from test_caller import Session, Socket, caller
from test_natural_restaurant import catalog as catalog
from test_natural_restaurant import context, query
from test_rumik_setup import configured

from voice_bench.business.environment import WORKFLOWS
from voice_bench.business.natural_restaurant import (
    NaturalRestaurantWorkflowV5,
    NaturalRestaurantWorkflowV6,
)
from voice_bench.business.reservations import (
    compact_reference_delivery,
    compact_reservation_reference,
    issued_reference,
    reservation_reference,
)
from voice_bench.caller.instructions import counterpart_instructions
from voice_bench.evaluation.natural_restaurant import consent_boundary
from voice_bench.evaluation.target_generation import target_generation_diagnostics
from voice_bench.evidence.local import LocalEvidence
from voice_bench.models import CounterpartBrief
from voice_bench.restaurant_natural import convert_catalog
from voice_bench.target.rumik.setup import assistant_instructions, setup_plan


def test_compact_reference_is_six_digits_deterministic_and_version_scoped():
    run = str(uuid4())
    reference = compact_reservation_reference(run, "call_a")
    assert re.fullmatch(r"SIM-\d{6}", reference)
    assert reference == compact_reservation_reference(run, "call_a")
    assert reference != compact_reservation_reference(run, "call_b")
    assert issued_reference("6", run, "call_a") == reference
    assert issued_reference("5", run, "call_a") == reservation_reference(run, "call_a")
    assert issued_reference(None, run, "call_a") == reservation_reference(run, "call_a")


def test_compact_delivery_is_one_sentence_without_phonetic_spelling():
    delivery = compact_reference_delivery("SIM-482913")
    assert delivery["version"] == "natural-reference-v3"
    assert delivery["reference"] == "SIM-482913"
    assert delivery["spoken_groups"] == ["SIM", "48", "29", "13"]
    assert delivery["spoken_form"] == "SIM 48 29 13"
    assert "one short sentence" in delivery["instruction"]
    assert "Do not spell letters phonetically" in delivery["instruction"]
    assert "Sierra" not in json.dumps(delivery) and "spoken_characters" not in delivery
    with pytest.raises(ValueError):
        compact_reference_delivery("SIM-06BEAC71AB")


def booked(workflow, catalog):
    run_id = str(uuid4())
    state = workflow.initialize(convert_catalog(catalog)[0].initial_state)
    workflow.execute(state, "check_availability", query(), context=context(1, "lookup"))
    offer = workflow.execute(
        state, "offer_reservation", {"option_id": "evening"}, context=context(10)
    )["offer"]
    result = workflow.execute(
        state,
        "record_reservation",
        {"offer_id": offer["offer_id"], "booking_name": "Asha Rao"},
        context={
            **context(operation="book"),
            "run_id": run_id,
            "consent_anchors": {"event_sequences": [11, 12]},
        },
    )
    return run_id, state, result


def test_version_six_books_a_compact_reference_and_version_five_is_unchanged(catalog):
    six = WORKFLOWS[("mock_restaurant_natural", "6")]
    assert type(six) is NaturalRestaurantWorkflowV6
    run_id, state, result = booked(six, catalog)
    assert result["ok"]
    assert result["reservation"]["reference"] == compact_reservation_reference(run_id, "book")
    assert state["bookings"][0]["reference"] == result["reservation"]["reference"]
    assert result["reference_delivery"]["version"] == "natural-reference-v3"
    assert result["reference_delivery"]["reference"] == result["reservation"]["reference"]
    # Lookup, offer and consent rules are inherited unchanged from version 5.
    assert six.response_tools(state, {"consent_anchors": None}) == {"check_availability"}

    five_run, _, five = booked(NaturalRestaurantWorkflowV5(), catalog)
    assert five["reservation"]["reference"] == reservation_reference(five_run, "book")
    assert five["reference_delivery"]["version"] == "natural-reference-v2"
    assert five["reference_delivery"]["spoken_characters"][0] == "S for Sierra"


def test_new_cases_use_version_six_and_omit_a_zero_dietary_count(catalog):
    case = convert_catalog(catalog)[0]
    assert case.workflow_version == "6" and case.version == "10-natural-english"
    assert "2 guests need food without onion and garlic." in case.user_task.constraints
    spec = deepcopy(catalog)
    spec["cases"][0]["user_constraints"]["required_without_onion_garlic_guests"] = 0
    plain = convert_catalog(spec, automated=True)[0]
    assert plain.version == "10-natural-automated"
    assert not any("onion" in line for line in plain.user_task.constraints)
    assert plain.criteria["dietary_guests"] == 0


def test_evaluation_reconstructs_version_six_quotes_like_version_five():
    offer = {
        "prepared_after_sequence": 20,
        "terms_available_after_sequence": 2,
        "terms_lookup_operation_id": "lookup",
        "terms": {"time": "19:00", "without_onion_garlic_guests": 0},
    }
    events = [
        {
            "kind": "business_tool_result",
            "sequence": 2,
            "payload": {
                "actor": "counterpart",
                "tool": "check_availability",
                "operation_id": "lookup",
                "result": {"ok": True, "matching_options": [{"time": "19:00"}]},
            },
        }
    ]
    assert consent_boundary({"workflow_version": "6"}, offer, events) == 2
    assert consent_boundary({"workflow_version": "5"}, offer, events) == 2
    assert consent_boundary({"workflow_version": "4"}, offer, events) == 20


def test_target_prompt_is_compact_and_asks_for_a_short_report():
    prompt = assistant_instructions("benchmark_user_task")
    assert len(prompt) <= 2300, "the target prompt must not grow back into a long rulebook"
    assert "{benchmark_user_task}" in prompt and "{{benchmark_user_report}}" in prompt
    assert "{{end_call}}" in prompt and "report_saved" in prompt
    assert "one or two sentences" in prompt
    assert prompt.index("Acknowledge the result aloud") < prompt.index("Privately call")
    assert prompt.index("goodbye") < prompt.index("Privately call")
    config, _ = configured()
    plan = setup_plan(config)
    assert plan["prompt_version"] == "natural-caller-v8"
    # The live v7 report omitted the booked terms; the short report must still name them.
    report_step = prompt[prompt.index("Privately call") :]
    for term in ("date", "time", "name", "party size", "exact reference"):
        assert term in report_step
    assert "one or two sentences" in plan["report_tool"]["description"]
    assert "One or two sentences" in plan["report_tool"]["config"]["llmParams"][0]["description"]


def test_counterpart_delivers_the_reference_in_one_sentence_and_avoids_lists():
    brief = CounterpartBrief(role="Restaurant employee", goal="Handle requests", known_facts={})
    tools = [
        {"name": "business_" + name}
        for name in ("check_availability", "offer_reservation", "record_reservation")
    ]
    prompt = counterpart_instructions("Keep facts fixed.", brief, tools)
    assert "in one\n   short sentence" in prompt or "in one short sentence" in prompt.replace(
        "\n   ", " "
    )
    assert "Do not spell it out" in prompt.replace("\n   ", " ")
    assert "do not read lists" in prompt.replace("\n  ", " ")
    assert "then WAIT" in prompt


def test_generation_diagnostics_expose_the_repeated_ceiling_without_naming_a_limit():
    def event(completion, reasoning, sequence):
        return {
            "kind": "target_text_observation",
            "sequence": sequence,
            "payload": {
                "remote_audio_participant": True,
                "text": json.dumps(
                    {
                        "label": "rtvi-ai",
                        "type": "metrics",
                        "data": {
                            "tokens": [
                                {"completion_tokens": completion, "reasoning_tokens": reasoning}
                            ]
                        },
                    }
                ),
            },
        }

    result = target_generation_diagnostics(
        [event(146, 101, 1), event(400, 396, 2), event(400, 397, 3)]
    )
    assert result["max_completion_observed"] == 400
    assert result["samples_at_max_completion"] == 2
    assert result["reasoning_dominated_samples"] == 2
    assert "max_completion_tokens" not in result
    empty = target_generation_diagnostics([])
    assert empty["max_completion_observed"] is None
    assert empty["samples_at_max_completion"] == 0


class FullyPlayedSession(Session):
    async def cancel_playback(self):
        # 2400 generated samples at 24 kHz is 100 ms; resampling reports 99 ms rendered.
        return {"speech": 99}


@pytest.mark.asyncio
async def test_fully_played_item_one_millisecond_short_is_not_an_interruption(tmp_path):
    evidence = LocalEvidence(tmp_path, uuid4(), uuid4())
    session, socket = FullyPlayedSession(evidence, 24000), Socket()
    brief = CounterpartBrief(role="Record custodian", goal="Handle notes", known_facts={})
    task = asyncio.create_task(caller(socket).converse(None, brief, session, evidence))
    try:
        async with asyncio.timeout(5):
            await socket.sent.get()
            await socket.incoming.put({"type": "session.updated", "session": {"id": "fake"}})
            await socket.incoming.put({"type": "response.created", "response": {"id": "r1"}})
            await socket.incoming.put(
                {
                    "type": "response.output_audio.delta",
                    "response_id": "r1",
                    "item_id": "speech",
                    "delta": __import__("base64").b64encode(b"\x02\x00" * 2400).decode(),
                }
            )
            await socket.incoming.put(
                {"type": "response.done", "response": {"id": "r1", "status": "completed"}}
            )
            await socket.incoming.put({"type": "input_audio_buffer.speech_started"})
            await asyncio.sleep(0.1)
            assert socket.sent.empty(), "no truncate may be sent for fully played speech"
            kinds = [e["kind"] for e in await evidence.event_snapshot()]
            assert "counterpart_playback_interrupted" not in kinds
            await socket.incoming.put({"type": "input_audio_buffer.speech_stopped"})
            await socket.incoming.put({"type": "input_audio_buffer.committed"})
            await socket.incoming.put(
                {
                    "type": "response.function_call_arguments.done",
                    "name": "finish_counterpart",
                    "call_id": "finish",
                    "response_id": "closing",
                }
            )
            await socket.incoming.put(
                {"type": "response.done", "response": {"id": "closing", "status": "completed"}}
            )
            await task
            summary = next(
                e
                for e in await evidence.event_snapshot()
                if e["kind"] == "counterpart_playback_summary"
            )
            assert summary["payload"]["items"][0]["interrupted_by_target"] is False
    finally:
        task.cancel()
        await asyncio.gather(task, return_exceptions=True)
        await session.close("test")
