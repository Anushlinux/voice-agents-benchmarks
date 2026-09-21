"""Reproduce lookup/offer/book chaining without making any provider calls."""

import asyncio
import json
from contextlib import nullcontext
from copy import deepcopy
from types import SimpleNamespace
from uuid import uuid4

import pytest
from test_caller import Session, Socket, caller
from test_natural_restaurant import catalog as catalog
from test_natural_restaurant import query
from test_reservations import observations

from voice_bench.business.environment import BusinessService
from voice_bench.business.natural_restaurant import NaturalRestaurantWorkflowV5
from voice_bench.evidence.local import LocalEvidence
from voice_bench.restaurant_natural import convert_catalog


def make_service(catalog, run_id):
    case = convert_catalog(catalog)[0]
    workflow = NaturalRestaurantWorkflowV5()
    run = {
        "workflow": workflow.name,
        "workflow_version": workflow.version,
        "state": workflow.initialize(case.initial_state),
        "user_task_served": True,
        "accept_tools": True,
        "operations": {},
        "audit": [],
        "tool_access": {"counterpart": sorted(workflow.tools)},
    }

    def read(key):
        assert key == run_id
        return deepcopy(run)

    return (
        case,
        run,
        BusinessService(SimpleNamespace(run=read, locked_run=lambda key: nullcontext(run))),
    )


def names(service, run_id, events):
    return {
        t["name"].removeprefix("business_")
        for t in service.counterpart_response_tools(run_id, events)
    }


@pytest.mark.asyncio
async def test_live_chaining_cannot_advertise_booking_until_heard_offer_and_reply(
    catalog, tmp_path
):
    sink = LocalEvidence(tmp_path, uuid4(), uuid4())
    _, run, service = make_service(catalog, sink.run_id)
    await sink.emit("controller", "connected")

    async def execute(tool, args, operation):
        result = service.execute(
            sink.run_id,
            tool,
            args,
            operation,
            actor="counterpart",
            observations=await sink.event_snapshot(),
        )
        await sink.emit(
            "business",
            "business_tool_result",
            {
                "actor": "counterpart",
                "operation_id": operation,
                "tool": tool,
                "result": result,
            },
        )
        return result

    assert names(service, sink.run_id, await sink.event_snapshot()) == {"check_availability"}
    await execute("check_availability", query(), "lookup")
    assert names(service, sink.run_id, await sink.event_snapshot()) == {
        "check_availability",
        "offer_reservation",
    }
    offer = await execute("offer_reservation", {"option_id": "evening"}, "offer")
    args = {"offer_id": offer["offer"]["offer_id"], "booking_name": "Asha Rao"}
    assert "record_reservation" not in names(service, sink.run_id, await sink.event_snapshot())
    # An unadvertised tool can still be hallucinated: preserve the failed attempt.
    result = await execute("record_reservation", args, "premature")
    assert result["error"] == "fresh_conversation_evidence_required"
    assert not run["state"]["bookings"]
    assert run["audit"][-1]["operation_id"] == "premature"

    # A complete employee utterance followed by a target reply provides structural
    # evidence only. The model still decides whether the actual reply was consent.
    for event in observations(sink.run_id):
        await sink.emit(event["source"], event["kind"], event["payload"])
    heard = await sink.event_snapshot()
    assert "record_reservation" in names(service, sink.run_id, heard)
    foreign = [{**e, "run_id": str(uuid4())} for e in heard]
    assert "record_reservation" not in names(service, sink.run_id, foreign)
    run["tool_access"]["counterpart"].remove("record_reservation")
    assert "record_reservation" not in names(service, sink.run_id, heard)
    run["tool_access"]["counterpart"].append("record_reservation")

    # A changed obligation invalidates that old response; it must not be used to
    # enable a new booking. Keeping identical terms does not demand a second yes.
    changed = await execute(
        "offer_reservation",
        {
            "option_id": "evening",
            "without_onion_garlic_guests": 2,
        },
        "changed",
    )
    assert "record_reservation" not in names(service, sink.run_id, await sink.event_snapshot())
    for event in observations(sink.run_id):
        await sink.emit(event["source"], event["kind"], event["payload"])
    args["offer_id"] = changed["offer"]["offer_id"]
    assert (await execute("record_reservation", args, "confirmed"))["ok"]
    assert names(service, sink.run_id, await sink.event_snapshot()) == {"check_availability"}
    await sink.finalize(sink.run_id)


@pytest.mark.asyncio
async def test_real_response_coordinator_sends_current_tool_subset(catalog, tmp_path):
    sink = LocalEvidence(tmp_path, uuid4(), uuid4())
    case, _, service = make_service(catalog, sink.run_id)
    session, socket = Session(sink, 24000), Socket()
    simulator = caller(socket)
    simulator.business = service
    task = asyncio.create_task(
        simulator.converse(
            SimpleNamespace(run_id=sink.run_id),
            case.counterpart,
            session,
            sink,
        )
    )
    try:
        async with asyncio.timeout(3):
            await socket.sent.get()
            await socket.incoming.put({"type": "session.updated", "session": {}})
            await socket.incoming.put({"type": "input_audio_buffer.committed", "item_id": "ask"})
            request = await socket.sent.get()
            assert request["type"] == "response.create"
            assert {t["name"] for t in request["response"]["tools"]} == {
                "business_check_availability",
                "finish_counterpart",
            }
            assert case.user_task.request not in json.dumps(request)
            # Drive the same function-only continuation seen in the live failure.
            await socket.incoming.put({"type": "response.created", "response": {"id": "lookup"}})
            await socket.incoming.put(
                {
                    "type": "response.function_call_arguments.done",
                    "response_id": "lookup",
                    "call_id": "lookup",
                    "name": "business_check_availability",
                    "arguments": json.dumps(query()),
                }
            )
            await socket.incoming.put(
                {
                    "type": "response.done",
                    "response": {"id": "lookup", "status": "completed"},
                }
            )
            assert json.loads((await socket.sent.get())["item"]["output"])["ok"]
            request = await socket.sent.get()
            assert {t["name"] for t in request["response"]["tools"]} == {
                "business_check_availability",
                "business_offer_reservation",
                "finish_counterpart",
            }
    finally:
        task.cancel()
        await asyncio.gather(task, return_exceptions=True)
        await session.close("test")
