"""Explicitly funded full evaluation; no provider work at import or validation time."""

import asyncio
import json
import os
from decimal import Decimal
from uuid import UUID

from voice_bench.evaluation.jev import PROVIDERS
from voice_bench.evidence.local import canonical, publish, verify_bundle


def validate(config, cases, rubric, *, repetitions=1):
    if not rubric.questions or not config.jev.model or config.jev.cost_ceiling_inr <= 0:
        raise ValueError("Full evaluation requires a configured, funded Jev rubric and model")
    if not all((config.judge.model, config.judge.transcription_model, config.judge.rubric_version)):
        raise ValueError("Full evaluation requires explicit judge and transcription models")
    if config.judge.cost_ceiling_inr <= 0:
        raise ValueError("Full evaluation requires funded transcription and judgment")
    if config.counterpart.model != "gpt-realtime" or config.judge.model != "gpt-5.6-luna":
        raise ValueError("This evaluation profile requires gpt-realtime and gpt-5.6-luna")
    if any(
        not c.evaluation_rubric or c.evaluation_rubric.version != config.judge.rubric_version
        for c in cases
    ):
        raise ValueError("Judge rubric version must match every frozen case")
    for key in ("OPENAI_API_KEY", PROVIDERS[config.jev.provider][1]):
        if not os.environ.get(key):
            raise ValueError(f"Full evaluation requires {key}")
    per_attempt = (
        config.runtime.cost_ceiling_inr_per_attempt
        + config.judge.cost_ceiling_inr
        + config.jev.cost_ceiling_inr
    )
    attempts = len(cases) * len(config.channels) * repetitions
    if per_attempt * attempts > config.limits.max_spend_inr:
        raise ValueError("Full conversation and evaluations exceed the funded budget")
    if config.limits.max_attempts_per_case != 1:
        raise ValueError("Full evaluation dispatch does not automatically retry calls")


async def evaluate_attempt(store, config, directory, rubric):
    from voice_bench.controller.budget import reserve_grading
    from voice_bench.evaluation.conversation_timing import measure
    from voice_bench.evaluation.jev import evaluate as evaluate_jev
    from voice_bench.evaluation.openai_judge import judge
    from voice_bench.evaluation.playback import playback_integrity
    from voice_bench.evaluation.scoring import deterministic, save_evaluation
    from voice_bench.evaluation.timing import browser_timing, caller_processing

    audit = directory / "evaluation/auto-v2"
    if (audit / "pipeline.json").exists() or (audit / "result.json").exists():
        raise ValueError("Automatic evaluation already exists; never redispatch its requests")
    stages = {}
    try:
        verify_bundle(directory)
        execution = json.loads((directory / "result.json").read_text())
        if not execution.get("termination_confirmed"):
            raise ValueError("Termination must be confirmed before remote evaluation")
        base = await asyncio.to_thread(deterministic, directory)
        save_evaluation(
            directory, "rules-v2", base, validity=execution.get("validity", "unresolved")
        )
        stages["rules"] = {"status": "completed"}
    except Exception as exc:
        stages["rules"] = {"status": "error", "error_type": type(exc).__name__}
        for stage in ("openai", "jev"):
            stages[stage] = {"status": "not_run", "reason": "unsealed_or_incomplete_execution"}
        result = {"status": "incomplete", "stages": stages, "conversation_accepted": False}
        publish(audit / "pipeline.json", canonical(result))
        return result

    bid, rid = UUID(directory.parent.name), UUID(directory.name)
    metadata, extra = {}, ()
    try:
        await asyncio.to_thread(reserve_grading, store, bid, rid, "auto-v2", config, prepaid=True)
        publish(
            audit / "dispatch.json",
            canonical(
                {
                    "judge": config.judge.model_dump(mode="json"),
                    "automatic_retry": False,
                }
            ),
        )
        extra, metadata = await judge(directory, config.judge, audit_directory=audit)
        stages["openai"] = {"status": "completed", "model": metadata.get("resolved_model")}
    except Exception as exc:
        stages["openai"] = {"status": "error", "error_type": type(exc).__name__}
        # Keep successful transcription windows usable by Jev if text judgment failed.
        metadata = {
            "transcripts": [
                json.loads(p.read_text()) for p in sorted(audit.glob("transcript-*.json"))
            ]
        }
    metadata.update(
        {
            "timing": await asyncio.to_thread(browser_timing, directory),
            "conversation_timing": await asyncio.to_thread(measure, directory),
            "caller_processing": caller_processing(directory),
            "playback_integrity": playback_integrity(directory),
            "human_listening_review": False,
            "stage_status": stages["openai"],
        }
    )
    if {m.name for m in base} & {m.name for m in extra}:
        raise ValueError("Model metrics cannot replace deterministic metrics")
    quality = next((m for m in extra if m.name == "counterpart_validity"), None)
    validity = {"met": "valid", "not_met": "invalid"}.get(
        quality.status if quality else None, "unresolved"
    )
    save_evaluation(directory, "auto-v2", base + list(extra), validity=validity, judge=metadata)
    try:
        jev_result_path = await evaluate_jev(
            directory, "auto-v2", rubric, config, "jev-auto-v2", store, live=True, prepaid=True
        )
        if json.loads(jev_result_path.read_text()).get("status") != "completed":
            raise ValueError("Jev did not save a completed result")
        stages["jev"] = {"status": "completed"}
    except Exception as exc:
        stages["jev"] = {"status": "error", "error_type": type(exc).__name__}
    evaluated = json.loads((audit / "result.json").read_text())
    jev_path = directory / "evaluation/jev-auto-v2/result.json"
    jev = json.loads(jev_path.read_text()) if jev_path.exists() else {}
    comparisons = []
    for metric in evaluated["metrics"]:
        answer = jev.get("answers", {}).get(metric["name"])
        if answer:
            choice = answer.get("choice")
            comparisons.append(
                {
                    "metric": metric["name"],
                    "luna_or_rules": metric["status"],
                    "jev": answer,
                    "disagreement": choice != metric["status"]
                    if choice in {"met", "not_met", "uncertain", "not_applicable"}
                    else None,
                }
            )
    timing = metadata["conversation_timing"]
    complete = all(s["status"] == "completed" for s in stages.values())
    result = {
        "status": "completed" if complete else "incomplete",
        "stages": stages,
        "automated_outcome": evaluated["outcome"],
        "validity": evaluated["validity"],
        "review_status": evaluated["evaluation_progress"],
        "human_listening_review": False,
        "conversation_timing": timing,
        "playback_integrity": metadata["playback_integrity"],
        "jev_comparisons": comparisons,
        "conversation_accepted": bool(
            complete
            and evaluated["outcome"] == "passed"
            and timing.get("status") == "measured"
            and not timing["long_silence_intervals"]
            and metadata["playback_integrity"]["status"] == "passed"
        ),
        "interpretation": "Automated task result; acoustic naturalness and self-talk "
        "need listening.",
    }
    publish(audit / "pipeline.json", canonical(result))
    return result


def export_full_report(store, batch_id, config, evaluations):
    from voice_bench.batches import export_report, report
    from voice_bench.evaluation.full_report import write_attempt_report

    destination = config.artifact_root / str(batch_id) / "full-report"
    result = report(store, batch_id, config.artifact_root, evaluation_version="auto-v2")
    result["evaluation_pipeline"] = evaluations
    result["complete_evaluation"] = bool(evaluations) and all(
        e.get("status") == "completed" for e in evaluations.values()
    )
    result["reserved_total_inr"] = str(
        sum(
            (Decimal(r["cost"]) for r in store.batch(batch_id).get("reservations", {}).values()),
            Decimal(0),
        )
    )
    export_report(result, destination)
    links = []
    for attempt in result["attempts"]:
        rid = attempt["run_id"]
        directory = config.artifact_root / str(batch_id) / rid
        write_attempt_report(directory, destination / rid, evaluations.get(rid, {}))
        links.append(f"- [{attempt['case_id']}]({rid}/README.md)")
    publish(
        destination / "README.md",
        (
            "# Full benchmark report\n\n"
            "Rumik is the evaluated customer assistant. OpenAI is the restaurant employee.\n\n"
            f"Counts: `{json.dumps(result['counts'])}`.\n\n"
            f"All requested evaluation stages completed: **{result['complete_evaluation']}**. "
            f"Reserved spending ceiling: INR {result['reserved_total_inr']} (not an invoice).\n\n"
            "Automated task results and human listening status are reported separately.\n\n"
            + "\n".join(links)
            + "\n"
        ).encode(),
    )
    return str(destination / "README.md")
