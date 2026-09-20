"""Offline inspection by default; paid execution requires explicit live/model switches."""

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from uuid import UUID

from voice_bench.readiness import scaffold_status
from voice_bench.settings import load_config


def database():
    from voice_bench.storage import PostgresStore

    if not os.environ.get("DATABASE_URL"):
        raise ValueError("DATABASE_URL is required for persistent operations")
    return PostgresStore(os.environ["DATABASE_URL"])


def parser():
    result = argparse.ArgumentParser(description=__doc__)
    commands = result.add_subparsers(dest="command", required=True)
    commands.add_parser("status")
    design = commands.add_parser("design", help="Provider-free profiles and restaurant rubrics")
    design_commands = design.add_subparsers(dest="action", required=True)
    design_commands.add_parser("profiles")
    prepare_design = design_commands.add_parser("prepare")
    prepare_design.add_argument("--cases", type=Path, required=True)
    prepare_design.add_argument(
        "--profile", choices=["straightforward", "concise", "clarification_seeking"], required=True
    )
    prepare_design.add_argument("--output", type=Path, required=True)
    target = commands.add_parser(
        "target", help="Prepare or inspect Rumik setup without provider calls"
    )
    target_commands = target.add_subparsers(dest="action", required=True)
    for name in ("prepare", "check"):
        sub = target_commands.add_parser(name)
        sub.add_argument("--config", type=Path, required=True)
        sub.add_argument(
            "--output" if name == "prepare" else "--snapshot", type=Path, required=True
        )
    jev = commands.add_parser("jev", help="Prepare or run a separate TypeSafe shadow evaluation")
    jev_commands = jev.add_subparsers(dest="action", required=True)
    for name in ("prepare", "evaluate"):
        sub = jev_commands.add_parser(name)
        sub.add_argument("directory", type=Path)
        sub.add_argument("--source-version", required=True)
        sub.add_argument("--rubric", type=Path, required=True)
        sub.add_argument("--config", type=Path, required=True)
        if name == "prepare":
            sub.add_argument("--output", type=Path, required=True)
        else:
            sub.add_argument("--version", required=True)
            sub.add_argument("--live", action="store_true")
    restaurant = commands.add_parser("restaurant")
    restaurant_commands = restaurant.add_subparsers(dest="action", required=True)
    prepare = restaurant_commands.add_parser("prepare")
    prepare.add_argument("--case", type=Path, required=True)
    prepare.add_argument("--source", type=Path, required=True)
    prepare.add_argument("--output", type=Path, required=True)
    hard = restaurant_commands.add_parser("prepare-hard")
    hard.add_argument("--baseline", type=Path, required=True)
    hard.add_argument("--variants", type=Path, required=True)
    hard.add_argument("--output", type=Path, required=True)
    preflight = restaurant_commands.add_parser("preflight")
    preflight.add_argument("--config", type=Path, required=True)
    preflight.add_argument("--cases", type=Path, required=True)
    plan = commands.add_parser("plan")
    plan.add_argument("--config", type=Path, required=True)
    commands.add_parser("db-init")
    fixture = commands.add_parser("fixture")
    fixture.add_argument("--config", type=Path, required=True)
    inspect = commands.add_parser("inspect")
    inspect.add_argument("directory", type=Path)
    evaluate = commands.add_parser("evaluate")
    evaluate.add_argument("directory", type=Path)
    evaluate.add_argument("--version", required=True)
    evaluate.add_argument("--with-model", action="store_true")
    evaluate.add_argument("--config", type=Path)
    review = commands.add_parser("review")
    review.add_argument("action", choices=["export", "import"])
    review.add_argument("directory", type=Path)
    review.add_argument("--version", required=True)
    review.add_argument("--file", type=Path)
    run = commands.add_parser("run")
    add_execution_args(run)
    batch = commands.add_parser("batch")
    batch_commands = batch.add_subparsers(dest="action", required=True)
    for name in ("plan", "run"):
        sub = batch_commands.add_parser(name)
        add_execution_args(sub)
        sub.add_argument("--repetitions", type=int, default=1)
        sub.add_argument("--seed", type=int, default=0)
    recover = batch_commands.add_parser("recover")
    recover.add_argument("batch_id", type=UUID)
    recover.add_argument("--config", type=Path, required=True)
    recover.add_argument("--remote", action="store_true")
    report = batch_commands.add_parser("report")
    report.add_argument("batch_id", type=UUID)
    report.add_argument("--config", type=Path, required=True)
    report.add_argument("--output", type=Path)
    report.add_argument("--evaluation-version")
    report.add_argument("--review-version")
    finalize = batch_commands.add_parser("finalize")
    finalize.add_argument("batch_id", type=UUID)
    finalize.add_argument("--config", type=Path, required=True)
    finalize.add_argument("--version", required=True)
    finalize.add_argument("--evaluation-version")
    finalize.add_argument("--review-version")
    upload = commands.add_parser("upload")
    upload.add_argument("directory", type=Path)
    upload.add_argument("--config", type=Path, required=True)
    return result


def add_execution_args(sub):
    sub.add_argument("--config", type=Path, required=True)
    sub.add_argument("--cases", type=Path, required=True)
    sub.add_argument("--live", action="store_true")
    sub.add_argument("--port", type=int, default=8000)
    sub.add_argument("--resume", type=UUID)


async def evaluate(args):
    from voice_bench.evaluation.scoring import deterministic, save_evaluation
    from voice_bench.evaluation.timing import browser_timing, caller_processing

    metrics = deterministic(args.directory)
    metadata = None
    validity = "unresolved"
    if args.with_model:
        if not args.config:
            raise ValueError("Model grading requires an explicit configuration")
        config = load_config(args.config)
        if config.limits.max_spend_inr <= 0:
            raise ValueError("Paid grading requires a positive funded budget")
        if (args.directory / "evaluation" / args.version / "result.json").exists():
            raise ValueError("Evaluation version already exists")
        from voice_bench.controller.budget import reserve_grading

        reserve_grading(
            database(),
            UUID(args.directory.parent.name),
            UUID(args.directory.name),
            args.version,
            config,
        )
        from voice_bench.evaluation.openai_judge import judge

        extra, metadata = await judge(
            args.directory,
            config.judge,
            audit_directory=args.directory / "evaluation" / args.version,
        )
        for metric in extra:
            if metric.name in {m.name for m in metrics}:
                raise ValueError("Model judge attempted to replace a deterministic verdict")
        metrics.extend(extra)
        quality = next(
            (m for m in extra if m.name in {"counterpart_validity", "caller_validity"}), None
        )
        if quality:
            validity = {"met": "valid", "not_met": "invalid"}.get(quality.status, "unresolved")
    execution = json.loads((args.directory / "result.json").read_text())
    if execution.get("validity") == "invalid":
        validity = "invalid"
    if not execution.get("termination_confirmed", False):
        validity = "unresolved"
    timing = browser_timing(args.directory)
    metadata = {
        **(metadata or {}),
        "timing": timing,
        "caller_processing": caller_processing(args.directory),
    }
    result = save_evaluation(
        args.directory, args.version, metrics, validity=validity, judge=metadata
    )
    return {"evaluation": str(result)}


async def recover(args):
    if not args.remote:
        raise ValueError("Recovery polls providers and may hang up calls; pass --remote explicitly")
    from voice_bench.batches import recover as reconcile
    from voice_bench.channels.phone.adapter import PlivoClient
    from voice_bench.target.rumik.client import RumikClient

    config = load_config(args.config)
    target = RumikClient(os.environ["RUMIK_API_KEY"])
    carrier = (
        PlivoClient(os.environ["PLIVO_AUTH_ID"], os.environ["PLIVO_AUTH_TOKEN"])
        if "phone" in config.channels
        else None
    )
    try:
        return await reconcile(database(), args.batch_id, config.artifact_root, target, carrier)
    finally:
        await target.close()
        if carrier:
            await carrier.close()


def dispatch(args):
    if args.command == "design":
        from voice_bench.batches import load_cases
        from voice_bench.design import prepare_case
        from voice_bench.evidence.local import canonical, publish
        from voice_bench.scenarios import PROFILE_RULES

        if args.action == "profiles":
            return {"profiles": PROFILE_RULES, "version": "1", "provider_calls": 0}
        source = load_cases(args.cases)
        cases = [prepare_case(case, args.profile) for case in source]
        publish(args.output, canonical([case.model_dump(mode="json") for case in cases]))
        return {
            "cases": str(args.output.resolve()),
            "case_count": len(cases),
            "profile": args.profile,
            "provider_calls": 0,
            "live_attempts": 0,
        }
    if args.command == "target":
        from voice_bench.evidence.local import canonical, publish
        from voice_bench.target.rumik.setup import check_setup, setup_plan

        config = load_config(args.config)
        if args.action == "check":
            return check_setup(json.loads(args.snapshot.read_bytes()), config)
        publish(args.output, canonical(setup_plan(config)))
        return {"setup_plan": str(args.output), "provider_calls": 0, "applied": False}
    if args.command == "jev":
        from voice_bench.evaluation.jev import JevRubric, prepare
        from voice_bench.evaluation.jev import evaluate as evaluate_jev
        from voice_bench.evidence.local import canonical, publish

        config = load_config(args.config)
        rubric = JevRubric.model_validate_json(args.rubric.read_bytes())
        if args.action == "prepare":
            prepared = prepare(args.directory, args.source_version, rubric, config.jev)
            publish(args.output, canonical(prepared))
            return {"request": str(args.output), "provider_calls": 0, "mode": "shadow"}
        if not args.live:
            raise ValueError("Jev sends saved text to TypeSafe; use --live explicitly")
        path = asyncio.run(
            evaluate_jev(
                args.directory,
                args.source_version,
                rubric,
                config,
                args.version,
                database(),
                live=True,
            )
        )
        return {"evaluation": str(path), "mode": "shadow", "benchmark_verdict_changed": False}
    if args.command == "restaurant":
        from voice_bench.batches import load_cases
        from voice_bench.restaurant_case import pilot_blockers, prepare
        from voice_bench.restaurant_hard_cases import HARD_IDS, hard_blockers, prepare_hard

        if args.action == "prepare":
            return prepare(args.case, args.source, args.output)
        if args.action == "prepare-hard":
            return prepare_hard(args.baseline, args.variants, args.output)
        cases = load_cases(args.cases)
        preflight = hard_blockers if any(c.case_id in HARD_IDS for c in cases) else pilot_blockers
        return preflight(load_config(args.config), cases)
    if args.command in {"status", "plan"}:
        result = scaffold_status()
        if args.command == "plan":
            result["config"] = load_config(args.config).model_dump(mode="json")
            result["message"] = "Configuration is valid. No calls or artifacts were created."
        return result
    if args.command == "db-init":
        database().migrate()
        return {"database": "initialized"}
    if args.command == "fixture":
        from voice_bench.fixture import execute_fixture

        return asyncio.run(execute_fixture(database(), load_config(args.config).artifact_root))
    if args.command == "inspect":
        from voice_bench.evidence.local import verify_bundle

        return verify_bundle(args.directory)
    if args.command == "evaluate":
        return asyncio.run(evaluate(args))
    if args.command == "review":
        from voice_bench.evaluation.scoring import import_review, review_template

        if args.action == "export":
            return review_template(args.directory, args.version)
        if args.file is None:
            raise ValueError("Review import requires --file")
        path = import_review(args.directory, args.version, json.loads(args.file.read_text()))
        return {"review": str(path)}
    if args.command == "upload":
        from voice_bench.evidence.s3 import S3Artifacts

        config = load_config(args.config)
        if not config.runtime.artifact_bucket:
            raise ValueError("Explicit artifact bucket required")
        return S3Artifacts(
            config.runtime.artifact_bucket,
            endpoint_url=config.runtime.artifact_endpoint_url or None,
            region=config.runtime.region,
        ).upload(args.directory)
    if args.command == "batch" and args.action == "recover":
        return asyncio.run(recover(args))
    if args.command == "batch" and args.action == "report":
        from voice_bench.batches import export_report, report

        result = report(
            database(),
            args.batch_id,
            load_config(args.config).artifact_root,
            evaluation_version=args.evaluation_version,
            review_version=args.review_version,
        )
        if args.output:
            export_report(result, args.output)
        return result
    if args.command == "batch" and args.action == "finalize":
        from voice_bench.batches import finalize_batch

        return finalize_batch(
            database(),
            args.batch_id,
            load_config(args.config).artifact_root,
            args.version,
            evaluation_version=args.evaluation_version,
            review_version=args.review_version,
        )
    from voice_bench.batches import load_cases, make_plan

    config = load_config(args.config)
    cases = load_cases(args.cases)
    repetitions = getattr(args, "repetitions", 1)
    seed = getattr(args, "seed", 0)
    if args.command == "batch" and args.action == "plan":
        return {
            "planned": [
                p.model_dump(mode="json")
                for p in make_plan(cases, config.channels, repetitions, seed)
            ],
            "provider_calls": 0,
        }
    if not args.live:
        raise ValueError("Execution requires the explicit --live switch")
    from voice_bench.runtime import execute_batch

    return asyncio.run(
        execute_batch(
            config,
            cases,
            repetitions=repetitions,
            seed=seed,
            port=args.port,
            resume_batch=args.resume,
        )
    )


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        result = dispatch(args)
    except (ValueError, OSError, KeyError) as exc:
        print(f"Configuration error: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:
        print(f"Operation failed: {type(exc).__name__}. Inspect saved evidence.", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, default=str))
    return 0
