"""Composition root for explicit live commands. Ordinary imports remain provider-free."""

import asyncio
import os
from pathlib import Path
from uuid import uuid4

from voice_bench.batches import make_plan
from voice_bench.evidence.local import canonical, digest, publish


def validate_live(config, cases):
    from voice_bench.business.environment import WORKFLOWS

    for case in cases:
        case.require_supported_execution()
        if case.workflow == "mock_restaurant_natural" and case.workflow_version in {"5", "6"}:
            turn = config.counterpart.turn_detection
            if turn.get("type") != "semantic_vad" or turn.get("eagerness") != "low":
                raise ValueError(
                    "Natural restaurant workflow 5 and later requires semantic_vad with low "
                    "eagerness to avoid replying to pauses inside a caller's turn"
                )
            if {"threshold", "prefix_padding_ms", "silence_duration_ms"}.intersection(turn):
                raise ValueError("Remove server_vad-only settings from semantic_vad configuration")
        if case.workflow == "mock_restaurant_natural" and (
            config.counterpart.max_output_tokens < 2048
            or config.counterpart.interrupt_after_ms is not None
            or config.channels != ("browser",)
        ):
            raise ValueError(
                "Natural restaurant qualification requires browser audio, at least 2048 "
                "output tokens and no timed interruption"
            )
        if config.purpose == "benchmark" and (case.harness_fixture or not case.evaluation_rubric):
            raise ValueError(
                "Benchmark batches require non-fixture cases with explicit frozen rubrics"
            )

    if (
        config.limits.max_total_call_minutes <= 0
        or config.limits.max_spend_inr <= 0
        or config.runtime.cost_ceiling_inr_per_attempt <= 0
    ):
        raise ValueError(
            "Positive funded limits and a conservative per-attempt cost ceiling are required"
        )
    if not config.runtime.rate_card_version:
        raise ValueError("A versioned rate card is required")
    costs = config.runtime.cost_components_inr_per_attempt
    required_costs = {"counterpart", "target"} | (
        {"carrier"} if "phone" in config.channels else set()
    )
    if not required_costs.issubset(costs) or any(
        not cost.is_finite() or cost <= 0 for cost in costs.values()
    ):
        raise ValueError(
            "Positive counterpart, target, and applicable carrier cost ceilings are required"
        )
    if sum(costs.values()) > config.runtime.cost_ceiling_inr_per_attempt:
        raise ValueError("Per-attempt ceiling must cover every configured component")
    if not config.target.agent_ref or not config.target.deployed_version:
        raise ValueError("The intended target and deployed version are required")
    if not all(
        (
            config.counterpart.model,
            config.counterpart.voice,
            config.counterpart.instructions,
            config.counterpart.turn_detection,
        )
    ):
        raise ValueError(
            "Explicit OpenAI counterpart model, voice, instructions, and turn detection required"
        )
    if config.counterpart.turn_detection.get("type") not in {"server_vad", "semantic_vad"}:
        raise ValueError("Unsupported counterpart turn-detection mode")
    recovery = config.counterpart.silence_recovery_seconds
    prompts = config.counterpart.max_silence_recovery_prompts
    if bool(recovery) != bool(prompts) or recovery >= config.counterpart.conversation_idle_seconds:
        raise ValueError("Silence recovery needs a prompt allowance and must precede idle timeout")
    if not config.runtime.public_base_url.startswith("https://"):
        raise ValueError("A public HTTPS endpoint for authenticated business tools is required")
    for case in cases:
        if (case.workflow, case.workflow_version) not in WORKFLOWS:
            raise ValueError("Workflow implementation is not registered")
        workflow = WORKFLOWS[(case.workflow, case.workflow_version)]
        workflow.initialize(case.initial_state)
        if not set(case.target_tools).issubset(workflow.tools | {"submit_user_report"}) or not set(
            case.counterpart_tools
        ).issubset(workflow.tools):
            raise ValueError("A participant tool is not declared by the workflow")
        if not set(case.counterpart_tools).issubset(workflow.tool_definitions):
            raise ValueError("Counterpart tools require descriptions and parameter schemas")
    required = ["DATABASE_URL", "RUMIK_API_KEY", "OPENAI_API_KEY", "BENCH_TOOLS_SECRET"]
    if "phone" in config.channels:
        required += ["PLIVO_AUTH_ID", "PLIVO_AUTH_TOKEN"]
        if not config.runtime.caller_number or not config.runtime.target_number:
            raise ValueError("Intended benchmark phone endpoints are required")
        if not config.target.plivo_sip_trunk_id or not config.target.plivo_termination_uri:
            raise ValueError("An existing Plivo SIP trunk ID and termination URI are required")
    if any(not os.environ.get(key) for key in required):
        missing = [key for key in required if not os.environ.get(key)]
        raise ValueError("Missing runtime settings: " + ", ".join(missing))


async def execute_batch(
    config, cases, *, repetitions=1, seed=0, port=8000, resume_batch=None, evaluation_rubric=None
):
    from voice_bench.restaurant_case import CASE_ID
    from voice_bench.restaurant_hard_cases import HARD_IDS

    if any(case.case_id in HARD_IDS for case in cases) and (
        not {c.case_id for c in cases}.issubset(HARD_IDS)
        or repetitions != 1
        or config.channels != ("browser",)
        or config.limits.max_attempts_per_case != 1
        or config.limits.max_concurrent_calls != 1
        or config.limits.max_call_seconds > 600
        or config.counterpart.interrupt_after_ms is not None
    ):
        raise ValueError(
            "Hard restaurant variants require browser, one attempt each, concurrency "
            "one, at most 600 seconds and no timed counterpart interruption; "
            "run the unchanged baseline separately"
        )

    if any(case.case_id == CASE_ID for case in cases) and (
        len(cases) != 1
        or repetitions != 1
        or config.channels != ("browser",)
        or config.limits.max_attempts_per_case != 1
        or config.limits.max_concurrent_calls != 1
        or config.limits.max_call_seconds > 300
        or config.counterpart.interrupt_after_ms is not None
    ):
        raise ValueError(
            "Restaurant pilot requires one case, one browser attempt, concurrency one, "
            "at most 300 seconds and no injected interruption"
        )
    validate_live(config, cases)
    if evaluation_rubric is not None:
        from voice_bench.evaluation.pipeline import validate

        if resume_batch:
            raise ValueError("Full evaluation cannot redispatch a resumed batch")
        validate(config, cases, evaluation_rubric, repetitions=repetitions)
    import uvicorn

    from voice_bench.api.app import create_app
    from voice_bench.business.environment import BusinessService
    from voice_bench.caller.openai_realtime import OpenAICounterpart
    from voice_bench.channels.browser.adapter import BrowserAdapter
    from voice_bench.channels.phone.adapter import PhoneAdapter, PhoneHub, PlivoClient
    from voice_bench.contracts import PlannedRun
    from voice_bench.controller.runner import Controller
    from voice_bench.storage import PostgresStore
    from voice_bench.target.rumik.client import RumikClient, qualify_snapshot, snapshot_digest

    store = PostgresStore(os.environ["DATABASE_URL"])
    await asyncio.to_thread(store.migrate)
    target = RumikClient(os.environ["RUMIK_API_KEY"])
    carrier = (
        PlivoClient(os.environ["PLIVO_AUTH_ID"], os.environ["PLIVO_AUTH_TOKEN"])
        if "phone" in config.channels
        else None
    )
    hub = PhoneHub(store, config, carrier) if carrier else None
    batch_id = resume_batch or uuid4()
    server = uvicorn.Server(
        uvicorn.Config(
            create_app(
                store,
                os.environ["BENCH_TOOLS_SECRET"],
                hub,
                callback_log=config.artifact_root / str(batch_id) / "callback-requests.jsonl",
            ),
            host="0.0.0.0",
            port=port,
            log_level="warning",
            access_log=False,
        )
    )
    serving = asyncio.create_task(server.serve())
    results = []
    evaluations = {}
    created = False
    stop_reason = None
    try:
        async with asyncio.timeout(10):
            while not server.started:
                if serving.done():
                    serving.result()
                    raise RuntimeError("Callback server failed to start")
                await asyncio.sleep(0.05)
        snapshot = await target.snapshot(
            config.target.agent_ref, sip_trunk_id=config.target.plivo_sip_trunk_id
        )
        qualify_snapshot(snapshot, config)
        if any(case.workflow == "mock_restaurant_natural" for case in cases):
            from voice_bench.target.rumik.setup import natural_setup_issues

            if issues := natural_setup_issues(snapshot, config):
                raise ValueError("; ".join(issues))
        if hub:
            hub.agent_id = snapshot["agent"]["id"]
        identity = snapshot_digest(snapshot)
        plans = make_plan(cases, config.channels, repetitions, seed, batch_id)
        dependencies = {}
        for name in ("uv.lock", "browser/package-lock.json"):
            path = Path(name)
            if path.exists():
                dependencies[name] = digest(path.read_bytes())
        from voice_bench.evidence.source import source_snapshot

        source_files, source_archive = await asyncio.to_thread(source_snapshot)
        frozen = {
            "config": config.model_dump(mode="json"),
            "target": snapshot,
            "dependencies": dependencies,
            "source_files": source_files,
            "seed": seed,
            "cases": [c.model_dump(mode="json") for c in cases],
            "source_digest": digest(
                b"".join(
                    p.relative_to(Path(__file__).parent).as_posix().encode() + p.read_bytes()
                    for p in sorted(Path(__file__).parent.rglob("*.py"))
                )
            ),
            "tool_credential_digest": digest(os.environ["BENCH_TOOLS_SECRET"].encode()),
            "evaluation_pipeline": evaluation_rubric.model_dump(mode="json")
            if evaluation_rubric
            else None,
        }
        config_digest = digest(canonical(frozen))
        if resume_batch:
            previous = await asyncio.to_thread(store.batch, batch_id)
            if previous["config_digest"] != config_digest:
                raise ValueError(
                    "Resume requires the original configuration, cases, code, and dependencies"
                )
            prior_runs = await asyncio.to_thread(store.runs, batch_id)
            if any(
                not r["termination_confirmed"] or not r.get("evidence_sealed") for r in prior_runs
            ):
                raise ValueError("Reconcile all unfinished attempts before resuming dispatch")
            plans = [PlannedRun.model_validate(p) for p in previous["plans"]]
        else:
            await asyncio.to_thread(
                store.create_batch,
                batch_id,
                {
                    "plans": [p.model_dump(mode="json") for p in plans],
                    "limits": config.limits.model_dump(mode="json"),
                    "frozen": frozen,
                    "config_digest": config_digest,
                    "status": "running",
                },
            )
            publish(config.artifact_root / str(batch_id) / "config.json", canonical(frozen))
            publish(config.artifact_root / str(batch_id) / "source-snapshot.tar.gz", source_archive)
        created = True
        case_lookup = {c.case_id: c for c in cases}
        # Serial dispatch is the default; the reservation layer enforces account-wide limits.
        for plan in plans:
            # Preserve room for a maximum-length recording and evidence finalization.
            # Existing evidence is never removed to make another paid attempt fit.
            import shutil

            if shutil.disk_usage(config.artifact_root).free < 180 * 1024 * 1024:
                stop_reason = "insufficient_disk_for_next_attempt"
                break
            attempts = [
                r
                for r in await asyncio.to_thread(store.runs, batch_id)
                if r["plan_id"] == str(plan.plan_id)
            ]
            if attempts:
                latest = max(attempts, key=lambda item: item["attempt"])
                failed_execution = latest.get("result", {}).get("error") or latest.get("recovery")
                if not failed_execution or len(attempts) >= config.limits.max_attempts_per_case:
                    continue
            current = await target.snapshot(
                config.target.agent_ref, sip_trunk_id=config.target.plivo_sip_trunk_id
            )
            if snapshot_digest(current) != identity:
                stop_reason = "target_configuration_drift"
                break
            channel = (
                BrowserAdapter(target, store)
                if plan.channel == "browser"
                else PhoneAdapter(target, hub)
            )
            counterpart = OpenAICounterpart(
                config.counterpart, os.environ["OPENAI_API_KEY"], business=BusinessService(store)
            )
            controller = Controller(
                store,
                config,
                channel,
                counterpart,
                target,
                target_agent_id=snapshot["agent"]["id"],
                target_agent_aliases=[
                    value for value in (snapshot["agent"].get("handle"),) if value
                ],
                full_evaluation=evaluation_rubric is not None,
            )
            result = await controller.execute(plan, case_lookup[plan.case_id], config_digest)
            results.append(result.model_dump(mode="json"))
            if evaluation_rubric is not None:
                from voice_bench.evaluation.pipeline import evaluate_attempt

                evaluations[str(result.run_id)] = await evaluate_attempt(
                    store,
                    config,
                    config.artifact_root / str(batch_id) / str(result.run_id),
                    evaluation_rubric,
                )
            if not result.termination_confirmed:
                stop_reason = "unresolved_call_termination"
                break
            if result.error == "ValueError" and not result.connected:
                stop_reason = "execution_precondition_or_budget"
                break
    except BaseException as exc:
        stop_reason = type(exc).__name__
        raise
    finally:
        server.should_exit = True
        try:
            await asyncio.wait_for(serving, 10)
        finally:
            await target.close()
            if carrier:
                await carrier.close()
        if created:
            completion = {
                "worker_stopped": True,
                "attempts_finished": len(results),
                "stop_reason": stop_reason,
                "results": results,
            }
            with store.locked_batch(batch_id) as (_, batch):
                batch["status"] = "needs_attention" if stop_reason else "execution_finished"
                batch["completion"] = completion
            publish(
                config.artifact_root / str(batch_id) / f"completion-{uuid4()}.json",
                canonical(completion),
            )
    full_report = None
    if evaluation_rubric is not None:
        from voice_bench.evaluation.pipeline import export_full_report

        full_report = await asyncio.to_thread(
            export_full_report, store, batch_id, config, evaluations
        )
    return {
        "batch_id": str(batch_id),
        "attempts": results,
        "stop_reason": stop_reason,
        "full_report": full_report,
    }
