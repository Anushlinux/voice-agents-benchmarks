"""A deterministic infrastructure check, never a dataset case or provider result."""

import asyncio
from uuid import uuid4

from voice_bench.batches import make_plan
from voice_bench.business.environment import BusinessService
from voice_bench.contracts import ExecutionCase
from voice_bench.evidence.local import LocalEvidence, verify_bundle
from voice_bench.models import CounterpartBrief, RunContext, UserTask
from voice_bench.storage import PostgresStore


def fixture_case():
    return ExecutionCase(
        case_id="harness-isolation",
        version="2",
        workflow="harness_record",
        workflow_version="1",
        harness_fixture=True,
        schema_version=2,
        task_scope="single_call",
        call_initiation="harness_connected",
        user_task=UserTask(
            request="Ask the record custodian to change my synthetic note to updated.",
            known_facts={"record_id": "owned"},
            constraints=("Do not change another record.",),
            permissions=("Request a note change on my owned record.",),
        ),
        counterpart=CounterpartBrief(
            role="Synthetic record custodian",
            goal="Handle permitted requests using the record tools.",
            known_facts={},
            behavior_rules=("Claim a change only after a successful tool result.",),
        ),
        counterpart_tools=("get_record", "set_note"),
        initial_state={
            "owned_record": "owned",
            "records": {"owned": {"note": "initial"}, "other": {"note": "unchanged"}},
        },
        criteria={
            "state_equals": [{"path": ["records", "owned", "note"], "value": "updated"}],
            "required_metrics": ["task_state", "policy_actions"],
        },
    )


async def execute_fixture(store, root):
    case = fixture_case()
    plans = make_plan([case], ["browser"], repetitions=2)
    batch_id = plans[0].batch_id
    await asyncio.to_thread(store.migrate)
    await asyncio.to_thread(
        store.create_batch,
        batch_id,
        {
            "plans": [p.model_dump(mode="json") for p in plans],
            "limits": {"max_attempts_per_case": 1},
            "harness_fixture": True,
        },
    )
    ids = [uuid4(), uuid4()]
    for run_id, plan in zip(ids, plans, strict=True):
        context = RunContext(
            run_id=run_id,
            case_id=case.case_id,
            case_version=case.version,
            repetition=plan.repetition,
            channel=plan.channel,
            config_digest="fixture-v1",
        )
        await asyncio.to_thread(
            store.create_run,
            batch_id,
            run_id,
            {
                "plan_id": str(plan.plan_id),
                "context": context.model_dump(mode="json"),
                "workflow": case.workflow,
                "workflow_version": case.workflow_version,
                "state": case.initial_state,
                "harness_fixture": True,
                "user_task": case.user_task.model_dump(mode="json"),
                "tool_access": {
                    "target": list(case.target_tools),
                    "counterpart": list(case.counterpart_tools),
                },
            },
        )
        await asyncio.to_thread(store.bind, "rumik", f"fixture-{run_id}", run_id)
    business = BusinessService(store)
    arguments = {"record_id": "owned", "note": "updated"}
    first, second = await asyncio.gather(
        *[
            asyncio.to_thread(business.execute, ids[0], "set_note", arguments, "same-operation")
            for _ in range(2)
        ]
    )
    assert first == second and first["ok"]
    forbidden = await asyncio.to_thread(
        business.execute,
        ids[0],
        "set_note",
        {"record_id": "other", "note": "forbidden"},
        "rejected",
    )
    assert forbidden["error"] == "forbidden_record"
    reopened = PostgresStore(store.dsn)
    assert reopened.run(ids[0])["state"]["records"]["owned"]["note"] == "updated"
    assert reopened.run(ids[1])["state"] == case.initial_state
    for run_id in ids:
        evidence = LocalEvidence(root, batch_id, run_id)
        await evidence.json("config/case.json", case.model_dump(mode="json"))
        await evidence.json("business/initial.json", case.initial_state)
        final = await asyncio.to_thread(business.seal, run_id)
        await evidence.json("business/final.json", final["state"])
        await evidence.json("business/audit.json", final["audit"])
        await evidence.json(
            "result.json",
            {
                "harness_fixture": True,
                "validity": "unresolved",
                "outcome": "unresolved",
                "termination_confirmed": True,
            },
        )
        await evidence.emit("controller", "harness_fixture_complete")
        await evidence.finalize(run_id)
        verify_bundle(evidence.directory)
        await asyncio.to_thread(
            store.update_run,
            run_id,
            phase="grading",
            termination_confirmed=True,
            evidence_sealed=True,
        )
    return {
        "harness_validation": "passed",
        "provider_calls": 0,
        "batch_id": str(batch_id),
        "run_ids": list(map(str, ids)),
        "artifact_directory": str(root / str(batch_id)),
        "checks": [
            "isolated state",
            "atomic duplicate handling",
            "forbidden action audit",
            "persisted state reopened",
            "sealed checksummed evidence",
        ],
    }
