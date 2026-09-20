"""Explicit batch plans, accounting, and crash reconciliation."""

import asyncio
import csv
import io
import json
import random
from uuid import UUID, uuid4, uuid5

from voice_bench.contracts import ExecutionCase, PlannedRun
from voice_bench.evidence.local import (
    canonical,
    digest,
    publish,
    safe_path,
    verify_bundle,
    write_derived,
)


def load_cases(path):
    cases = [ExecutionCase.model_validate(item) for item in json.loads(path.read_text())]
    keys = [c.case_id for c in cases]
    if not cases or len(set(keys)) != len(keys):
        raise ValueError("Cases must be nonempty and have unique IDs")
    return cases


def make_plan(cases, channels, repetitions=1, seed=0, batch_id=None):
    if repetitions < 1 or not channels:
        raise ValueError("Positive repetitions and at least one channel are required")
    batch_id = batch_id or uuid4()
    rng = random.Random(seed)
    pairs = [(c, repetition) for c in cases for repetition in range(1, repetitions + 1)]
    rng.shuffle(pairs)
    result = []
    for case, repetition in pairs:
        order = list(channels)
        rng.shuffle(order)
        for channel in order:
            result.append(
                PlannedRun(
                    plan_id=uuid5(
                        batch_id, f"{case.case_id}:{case.version}:{repetition}:{channel}"
                    ),
                    batch_id=batch_id,
                    case_id=case.case_id,
                    case_version=case.version,
                    channel=channel,
                    repetition=repetition,
                    order=len(result),
                    task_scope=case.task_scope,
                    call_initiation=case.call_initiation,
                )
            )
    return result


def report(store, batch_id, root, *, evaluation_version=None, review_version=None):
    batch = store.batch(batch_id)
    plans = batch["plans"]
    runs = store.runs(batch_id)
    rows = []
    for run in runs:
        result = dict(run.get("result", {}))
        directory = root / str(batch_id) / run["run_id"]
        if evaluation_version:
            path = safe_path(directory, f"evaluation/{evaluation_version}/result.json")
            if path.exists():
                verify_bundle(directory)
                result.update(json.loads(path.read_text()))
        if review_version:
            path = safe_path(directory, f"review/{review_version}/result.json")
            if path.exists():
                verify_bundle(directory)
                review = json.loads(path.read_text())
                if review["evaluation_version"] != evaluation_version:
                    raise ValueError("Review references a different evaluation version")
                result.update(review)
        rows.append(
            {
                "run_id": run["run_id"],
                "plan_id": run["plan_id"],
                "case_id": run["context"]["case_id"],
                "channel": run["context"]["channel"],
                "repetition": run["context"]["repetition"],
                "attempt": run["attempt"],
                "attempted": bool(run.get("dispatch_intent")),
                "connected": run["connected"],
                "validity": result.get("validity", "unresolved"),
                "outcome": result.get("outcome", "unresolved"),
                "termination_confirmed": run["termination_confirmed"],
                "harness_fixture": run.get("harness_fixture", False),
                "task_scope": run.get("task_scope", "legacy_unspecified"),
                "call_initiation": run.get("call_initiation", "legacy_unspecified"),
            }
        )
    counts = {
        "planned": len(plans),
        "attempted": sum(r["attempted"] for r in rows),
        "connected": sum(r["connected"] for r in rows),
    }
    for name in ("valid", "invalid", "unresolved"):
        counts[name] = sum(r["attempted"] and r["validity"] == name for r in rows)
    for name in ("passed", "failed"):
        counts[name] = sum(
            r["attempted"] and r["validity"] == "valid" and r["outcome"] == name for r in rows
        )
    attempted_plans = {r["plan_id"] for r in rows if r["attempted"]}
    counts["not_run"] = sum(p["plan_id"] not in attempted_plans for p in plans)
    counts["outcome_unresolved"] = sum(
        r["attempted"] and r["outcome"] == "unresolved" for r in rows
    )
    counts["attempt_records"] = len(rows)
    return {
        "batch_id": str(batch_id),
        "counts": counts,
        "attempts": rows,
        "pass_rate": {
            "numerator": counts["passed"],
            "denominator": counts["valid"],
            "unit": "valid attempts",
            "value": counts["passed"] / counts["valid"] if counts["valid"] else None,
        },
        "planned_items": plans,
        "status": batch.get("status", "prepared"),
        "evaluation_version": evaluation_version,
        "review_version": review_version,
    }


def export_report(result, destination):
    destination.mkdir(parents=True, exist_ok=True)
    publish(destination / "report.json", canonical(result))
    output = io.StringIO()
    fields = (
        list(result["attempts"][0])
        if result["attempts"]
        else ["run_id", "plan_id", "channel", "validity", "outcome"]
    )
    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()
    writer.writerows(result["attempts"])
    publish(destination / "attempts.csv", output.getvalue().encode())


def finalize_batch(store, batch_id, root, version, *, evaluation_version=None, review_version=None):
    """Seal accounting only after dispatch is stopped and every attempt is settled."""
    import re

    if not re.fullmatch(r"[A-Za-z0-9_-]+", version):
        raise ValueError("Invalid report version")
    with store.locked_batch(batch_id) as (_, batch):
        if not batch.get("completion", {}).get("worker_stopped"):
            raise ValueError("Worker shutdown must be recorded before batch finalization")
        runs = store.runs(batch_id)
        if any(not r.get("evidence_sealed") or not r["termination_confirmed"] for r in runs):
            raise ValueError("Reconcile and seal all attempts before finalizing the batch")
        result = report(
            store,
            batch_id,
            root,
            evaluation_version=evaluation_version,
            review_version=review_version,
        )
        gaps = (
            result["counts"]["not_run"]
            + result["counts"]["unresolved"]
            + result["counts"]["outcome_unresolved"]
        )
        result["status"] = "finalized_with_gaps" if gaps else "finalized"
        result["worker_stopped"] = True
        path = safe_path(root, f"{batch_id}/finalization-{version}.json")
        publish(path, canonical(result))
        batch["status"] = result["status"]
        batch.setdefault("finalizations", {})[version] = {
            "sha256": digest(canonical(result)),
            "path": str(path),
        }
    return result


async def recover(store, batch_id, root, target, carrier=None):
    """Reconcile abandoned attempts. Never dispatch or continue a conversation here."""
    from voice_bench.business.environment import BusinessService
    from voice_bench.controller.budget import release
    from voice_bench.evidence.local import LocalEvidence

    recovered = []
    for run in await asyncio.to_thread(store.runs, batch_id):
        if run.get("termination_confirmed") and run.get("evidence_sealed"):
            continue
        run_id = UUID(run["run_id"])
        owner = str(uuid4())
        if not await asyncio.to_thread(store.claim, run_id, owner):
            continue
        try:
            confirmed = not run.get("dispatch_intent")
            bindings = await asyncio.to_thread(store.bindings, run_id)
            records = {}
            statuses = []
            for binding in bindings:
                if binding["provider"] == "rumik":
                    record = await target.call(binding["call_id"])
                    record.pop("recordingUrl", None)
                    records["rumik"] = record
                    statuses.append(record.get("status") in {"completed", "failed", "expired"})
                elif binding["provider"] == "plivo" and carrier:
                    await carrier.hangup(binding["call_id"])
                    record = await carrier.call(binding["call_id"])
                    records["plivo"] = record
                    statuses.append(
                        record.get("call_status")
                        in {"completed", "failed", "busy", "no-answer", "cancel"}
                    )
            if statuses:
                confirmed = all(statuses)
            if run.get("dispatch_intent") and run["context"]["channel"] == "phone":
                # A terminated Rumik leg alone does not establish carrier termination.
                confirmed = confirmed and "plivo" in records
            business = await asyncio.to_thread(BusinessService(store).seal, run_id)
            directory = root / str(batch_id) / str(run_id)
            recovery = {
                "termination_confirmed": confirmed,
                "records": records,
                "business": business,
                "validity": "unresolved",
                "outcome": "unresolved",
            }
            if (directory / "manifest.json").exists():
                write_derived(directory, "review", f"recovery-{uuid4()}", recovery)
            else:
                evidence = LocalEvidence(root, batch_id, run_id, recovering=True)
                await evidence.json(f"recovery/{uuid4()}.json", recovery)
                for name, value in (
                    ("business/final.json", business["state"]),
                    ("business/audit.json", business["audit"]),
                    ("result.json", {**recovery, "error": "worker_restarted"}),
                ):
                    if not (directory / name).exists():
                        await evidence.json(name, value)
                await evidence.finalize(
                    run_id,
                    expected=(
                        "result.json",
                        "business/final.json",
                        "audio/received.wav",
                        "audio/sent.wav",
                    ),
                )
            await asyncio.to_thread(
                store.update_run,
                run_id,
                termination_confirmed=confirmed,
                evidence_sealed=True,
                phase="grading",
                recovery=recovery,
            )
            await asyncio.to_thread(release, store, run_id, confirmed)
            if confirmed:
                await asyncio.to_thread(store.release_route, run_id)
            recovered.append({"run_id": str(run_id), "termination_confirmed": confirmed})
        finally:
            await asyncio.to_thread(store.expire_lease, run_id, owner)
    return recovered
