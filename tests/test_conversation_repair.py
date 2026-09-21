import asyncio
import json
import struct
import wave
from decimal import Decimal
from pathlib import Path
from uuid import uuid4

import pytest
from test_natural_restaurant import catalog as catalog

from voice_bench.caller.responses import ResponseCoordinator
from voice_bench.controller.budget import reserve, reserve_grading
from voice_bench.evaluation.conversation_timing import summarize_activity
from voice_bench.evaluation.full_report import synchronized_audio
from voice_bench.evaluation.jev import JevRubric
from voice_bench.evaluation.pipeline import evaluate_attempt, validate
from voice_bench.evaluation.progress import evaluation_progress
from voice_bench.evaluation.rubrics import apply_rubric
from voice_bench.evaluation.scoring import load_bundle
from voice_bench.evidence.local import LocalEvidence
from voice_bench.models import EvidenceRef, MetricResult
from voice_bench.restaurant_natural import convert_catalog, natural_rubric, user_instructions
from voice_bench.settings import load_config


def configuration(tmp_path):
    c = load_config(Path("configs/local.toml"))
    return c.model_copy(
        update={
            "artifact_root": tmp_path,
            "channels": ("browser",),
            "limits": c.limits.model_copy(
                update={
                    "max_spend_inr": Decimal(155),
                    "max_total_call_minutes": 10,
                    "max_attempts_per_case": 1,
                }
            ),
            "runtime": c.runtime.model_copy(
                update={"cost_ceiling_inr_per_attempt": Decimal(130), "rate_card_version": "test"}
            ),
            "counterpart": c.counterpart.model_copy(update={"model": "gpt-realtime"}),
            "judge": c.judge.model_copy(
                update={
                    "model": "gpt-5.6-luna",
                    "transcription_model": "gpt-4o-mini-transcribe",
                    "rubric_version": "natural-restaurant-auto-v2",
                    "cost_ceiling_inr": Decimal(20),
                }
            ),
            "jev": c.jev.model_copy(
                update={
                    "provider": "openrouter",
                    "model": "typesafe/jev-1.13",
                    "cost_ceiling_inr": Decimal(5),
                }
            ),
        }
    )


def jev_rubric():
    return JevRubric.model_validate(
        {
            "version": "test",
            "questions": {
                "counterpart_validity": {
                    "type": "choice",
                    "instructions": "Was the employee truthful?",
                    "criteria": {"met": "Yes", "not_met": "No", "uncertain": "Unknown"},
                }
            },
        }
    )


def test_english_authority_preserves_restrictions_and_rejects_unknown_fields(catalog):
    spec = catalog["cases"][0]
    spec["permissions"].update(
        may_confirm_one_booking=True,
        may_change_date_or_party_size=False,
        may_agree_pay_at_visit_total_inr_up_to=12000,
        when_no_authorized_option_exists="Do not book; report the reason.",
    )
    case = convert_catalog(catalog, automated=True)[0]
    words = " ".join(case.user_task.constraints + case.user_task.permissions)
    for phrase in [
        "2026-10-01",
        "4 people",
        "19:00",
        "Khar",
        "Asha Rao",
        "2 guests",
        "one table",
        "Do not make any payment",
        "Do not agree to a deposit",
        "Do not agree to a cancellation fee",
        "Do not buy extras",
        "Do not change the date or party size",
        "12000",
        "Do not book",
    ]:
        assert phrase in words
    assert "{" not in words and "option_id" not in words
    assert "Only if no authorized option exists: Do not book; report the reason." in words
    assert "Do not book; report the reason." not in case.user_task.permissions
    assert "Asha Rao" not in json.dumps(case.counterpart.model_dump())
    spec["permissions"]["new_authority"] = True
    with pytest.raises(ValueError, match="Unrecognized"):
        user_instructions(spec["user_constraints"], spec["permissions"])


def test_automated_rubric_resolves_task_but_keeps_listening_separate():
    rubric = natural_rubric(True, automated=True)
    metrics = [
        MetricResult(
            name=d.name,
            status="met",
            explanation="Synthetic evidence",
            evidence=tuple(
                EvidenceRef(artifact_key="b/r/" + n, sha256="a" * 64) for n in d.required_evidence
            ),
        )
        for d in rubric.metrics
    ]
    result = apply_rubric(rubric, metrics, "valid")
    assert result["outcome"] == "passed"
    normalized = [{"name": d["name"], "status": d["status"]} for d in result["metric_decisions"]]
    progress = evaluation_progress(
        {"evaluation_rubric": rubric.model_dump(mode="json")}, normalized
    )
    assert progress["status"] == "checks_resolved"
    assert set(progress["pending_diagnostic_review_metrics"]) == {
        "hinglish_quality",
        "target_output_integrity",
    }
    assert apply_rubric(natural_rubric(True), metrics, "valid")["outcome"] == "unresolved"
    metrics = [
        m.model_copy(update={"status": "not_met"}) if m.name == "task_state" else m for m in metrics
    ]
    assert apply_rubric(rubric, metrics, "valid")["outcome"] == "failed"


def test_timing_retains_long_responses_and_terminal_silence():
    result = summarize_activity({"counterpart": [[1, 2], [18, 19]], "target": [[15, 16]]}, 0, 40)
    assert result["replies"]["target"]["response_gaps"][0]["gap_ms"] == 13000
    assert result["replies"]["counterpart"]["response_gaps"][0]["gap_ms"] == 2000
    assert [s["duration_seconds"] for s in result["long_silence_intervals"]] == [13, 21]


def test_report_audio_aligns_both_speakers_without_overwriting(tmp_path):
    (tmp_path / "audio").mkdir()
    events = []
    for name, kind, start, level in (
        ("played", "rendered_block", 0, 1000),
        ("received", "received_block", 800, 2000),
    ):
        with wave.open(str(tmp_path / f"audio/{name}.wav"), "wb") as audio:
            audio.setparams((1, 2, 8000, 0, "NONE", "none"))
            audio.writeframes(struct.pack("<h", level) * 1600)
        events.append(
            {
                "kind": kind,
                "clock_id": "chromium-audio-context",
                "payload": {"rate": 8000, "sample": start, "samples": 1600, "recording_offset": 0},
            }
        )
    (tmp_path / "events.jsonl").write_text("\n".join(json.dumps(e) for e in events))
    output = tmp_path / "conversation.wav"
    assert synchronized_audio(tmp_path, output)["duration_seconds"] == 0.3
    with wave.open(str(output), "rb") as audio:
        samples = list(struct.iter_unpack("<hh", audio.readframes(audio.getnframes())))
    assert samples[0] == (1000, 0)
    assert samples[800] == (1000, 2000)
    assert samples[1600] == (0, 2000)
    with pytest.raises(FileExistsError):
        synchronized_audio(tmp_path, output)


@pytest.mark.asyncio
async def test_response_creation_coalesces_and_late_done_cannot_clear_new_response(tmp_path):
    sink = LocalEvidence(tmp_path, uuid4(), uuid4())
    sent = asyncio.Queue()
    blocked = False

    async def request():
        return {"type": "response.create"}

    coordinator = ResponseCoordinator(sent.put, sink, request, lambda: blocked)
    task = asyncio.create_task(coordinator.run())
    try:
        coordinator.request("tool_results")
        coordinator.request("committed_input")
        assert await asyncio.wait_for(sent.get(), 1) == {"type": "response.create"}
        await coordinator.created("first")
        await coordinator.cancel()
        await coordinator.cancel()
        assert await sent.get() == {"type": "response.cancel", "response_id": "first"}
        assert sent.empty()
        coordinator.request("new_input")
        coordinator.done("first")
        assert await asyncio.wait_for(sent.get(), 1) == {"type": "response.create"}
        coordinator.done("first")
        assert not coordinator.idle.is_set()
        await coordinator.created("second")
        blocked = True
        coordinator.request("tool_results")
        coordinator.done("second")
        await asyncio.sleep(0)
        assert sent.empty()
        coordinator.close()
        blocked = False
        coordinator.request("shutdown_race")
        await task
        assert sent.empty()
    finally:
        task.cancel()
        await asyncio.gather(task, return_exceptions=True)
        await sink.finalize(sink.run_id)


def test_all_stages_funded_atomically_and_claimed_once(store, prepared, tmp_path):
    plans, (rid, _) = prepared
    c = configuration(tmp_path)
    with store.locked_batch(plans[0].batch_id) as (_, b):
        b["limits"]["max_spend_inr"] = "155"
    too_small = c.model_copy(
        update={"limits": c.limits.model_copy(update={"max_spend_inr": Decimal(154)})}
    )
    with pytest.raises(ValueError, match="budget"):
        reserve(store, plans[0].batch_id, rid, too_small, full_evaluation=True)
    assert not store.run(rid).get("reservation")
    reserve(store, plans[0].batch_id, rid, c, full_evaluation=True)
    reservations = store.batch(plans[0].batch_id)["reservations"]
    assert sum(Decimal(r["cost"]) for r in reservations.values()) == 155
    reserve_grading(store, plans[0].batch_id, rid, "auto-v2", c, prepaid=True)
    with pytest.raises(ValueError, match="already dispatched"):
        reserve_grading(store, plans[0].batch_id, rid, "auto-v2", c, prepaid=True)


def test_full_evaluation_rejects_missing_jev_before_dispatch(tmp_path, catalog, monkeypatch):
    c = configuration(tmp_path)
    cases = convert_catalog(catalog, automated=True)
    monkeypatch.setenv("OPENAI_API_KEY", "unit")
    monkeypatch.setenv("OPENROUTER_API_KEY", "unit")
    validate(c, cases, jev_rubric())
    with pytest.raises(ValueError, match="Jev"):
        validate(
            c.model_copy(update={"jev": c.jev.model_copy(update={"model": ""})}),
            cases,
            jev_rubric(),
        )
    monkeypatch.delenv("OPENROUTER_API_KEY")
    with pytest.raises(ValueError, match="OPENROUTER"):
        validate(c, cases, jev_rubric())


@pytest.mark.asyncio
@pytest.mark.parametrize("failure", [None, "judge", "jev"])
async def test_pipeline_attempts_both_judges_and_never_retries(
    tmp_path, catalog, monkeypatch, failure
):
    c = configuration(tmp_path)
    case = convert_catalog(catalog, automated=True)[0]
    sink = LocalEvidence(tmp_path, uuid4(), uuid4())
    for filename, value in {
        "config/case.json": case.model_dump(mode="json"),
        "business/initial.json": case.initial_state,
        "business/final.json": case.initial_state,
        "business/audit.json": [],
        "result.json": {"termination_confirmed": True},
        "target/report-requests.json": [],
        "target/task-delivery.json": {"sha256": "unit"},
    }.items():
        await sink.json(filename, value)
    await sink.emit("controller", "done")
    await sink.finalize(sink.run_id)
    calls = []

    def reserve_fake(*args, **kwargs):
        assert kwargs["prepaid"]
        calls.append("reserve")

    async def judge_fake(*args, **kwargs):
        calls.append("luna")
        if failure == "judge":
            raise ValueError("Synthetic judge failure")
        _, refs = load_bundle(sink.directory)
        return (), {"transcripts": [], "resolved_model": c.judge.model}

    async def jev_fake(*args, **kwargs):
        assert kwargs["prepaid"] and kwargs["live"]
        calls.append("jev")
        if failure == "jev":
            raise ValueError("Synthetic Jev failure")
        path = sink.directory / "evaluation/jev-auto-v2/result.json"
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps({"status": "completed", "answers": {}}))
        return path

    monkeypatch.setattr("voice_bench.controller.budget.reserve_grading", reserve_fake)
    monkeypatch.setattr("voice_bench.evaluation.openai_judge.judge", judge_fake)
    monkeypatch.setattr("voice_bench.evaluation.jev.evaluate", jev_fake)
    result = await evaluate_attempt(None, c, sink.directory, jev_rubric())
    assert calls == ["reserve", "luna", "jev"]
    assert result["status"] == ("incomplete" if failure else "completed")
    assert not result["conversation_accepted"]
    with pytest.raises(ValueError, match="already exists"):
        await evaluate_attempt(None, c, sink.directory, jev_rubric())
    assert calls == ["reserve", "luna", "jev"]
