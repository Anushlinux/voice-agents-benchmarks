import io
import json
import struct
import wave
from types import SimpleNamespace
from uuid import uuid4

import pytest

from voice_bench.contracts import JudgeConfig
from voice_bench.evaluation.openai_judge import judge
from voice_bench.evaluation.speech_support import SpeechClaim
from voice_bench.evidence.local import LocalEvidence
from voice_bench.fixture import fixture_case


@pytest.mark.asyncio
@pytest.mark.parametrize("with_played", [True, False])
@pytest.mark.parametrize("amplitude", [2, 4096])
async def test_model_judge_transcribes_captured_audio_and_rejects_invented_citations(
    tmp_path, with_played, amplitude
):
    evidence = LocalEvidence(tmp_path, uuid4(), uuid4())
    await evidence.json("config/case.json", fixture_case().model_dump(mode="json"))
    await evidence.json("business/final.json", {"note": "initial"})
    await evidence.json("business/audit.json", [])
    final_report = {"text": "Reference numbers: SIM3453 and F8061B."}
    await evidence.json("target/user-report.json", final_report)
    report_requests = [
        {"report": final_report["text"], "result": {"report_saved": True}},
        {"report": "Corrected reference: SIM-3453F8061B.", "result": {"ok": False}},
    ]
    await evidence.json("target/report-requests.json", report_requests)
    await evidence.json("result.json", {"error": "cancelled", "attribution": "harness"})
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as audio:
        audio.setparams((1, 2, 8000, 0, "NONE", "none"))
        audio.writeframes(struct.pack("<h", amplitude) * 8000)
    ref = await evidence.store_artifact(evidence.run_id, "audio/received.wav", buffer.getvalue())
    await evidence.store_artifact(evidence.run_id, "audio/sent.wav", buffer.getvalue())
    if with_played:
        await evidence.store_artifact(evidence.run_id, "audio/played.wav", buffer.getvalue())
    await evidence.finalize(evidence.run_id)
    config = JudgeConfig(
        model="test-judge", transcription_model="test-transcribe", rubric_version="1"
    )
    calls = []
    metric_name = "counterpart_validity"
    citation_name = "speech-window-0002"

    async def transcribe(**args):
        calls.append("transcribe")
        assert args["file"][1][:4] == b"RIFF"
        return SimpleNamespace(text="The target CLAIMED it changed the note.")

    async def parse(**args):
        calls.append("judge")
        assert args["model"] == "test-judge"
        prompt = json.loads(args["input"])
        assert prompt["state"] == {"note": "initial"}
        assert prompt["user_task"]["request"] == fixture_case().user_task.request
        assert prompt["counterpart_brief"]["role"] == "Synthetic record custodian"
        assert prompt["benchmark_roles"]["received_audio"] == "Rumik"
        assert prompt["requested_metrics"] == ["counterpart_validity"]
        schema = args["text_format"].model_json_schema()
        assert (
            schema["$defs"]["RequestedMetric"]["properties"]["name"]["const"]
            == "counterpart_validity"
        )
        assert "counterpart_validity" in args["instructions"]
        assert "counterpart never receives the private user_task" in args["instructions"]
        assert (
            "employee to know or correct undisclosed private instructions" in args["instructions"]
        )
        assert prompt["target_user_report"] == final_report
        assert prompt["target_report_requests"] == report_requests
        assert "rejected correction was attempted, not delivered" in args["instructions"]
        assert prompt["execution_result"]["attribution"] == "harness"
        assert "human-listening-only" in args["instructions"]
        assert [t["source"] for t in prompt["transcripts"]] == [
            "audio/received.wav",
            "audio/played.wav" if with_played else "audio/sent.wav",
        ]
        metric_schema = args["text_format"].model_fields["metrics"].annotation.__args__[0]
        return SimpleNamespace(
            output_parsed=args["text_format"].model_construct(
                metrics=(
                    metric_schema.model_construct(
                        name=metric_name,
                        status="met",
                        explanation="Adhered to brief.",
                        evidence=(citation_name,),
                        speech_claims=(
                            SpeechClaim(
                                source_id=citation_name,
                                speaker="counterpart",
                                quote="The target CLAIMED it changed the note.",
                            ),
                        )
                        if amplitude > 2
                        else (),
                    ),
                )
            ),
            id="fake-response",
            usage=None,
            model_dump_json=lambda **_: '{"id":"fake-response"}',
        )

    client = SimpleNamespace(
        audio=SimpleNamespace(transcriptions=SimpleNamespace(create=transcribe)),
        responses=SimpleNamespace(parse=parse),
    )
    metrics, metadata = await judge(evidence.directory, config, client=client)
    assert calls == (["judge"] if amplitude <= 2 else ["transcribe", "transcribe", "judge"])
    if amplitude <= 2:
        assert all(t["text"] == "" for t in metadata["transcripts"])
        assert all(
            t["transcription_status"] == "skipped_near_silence" for t in metadata["transcripts"]
        )
    assert metrics[0].status == ("met" if amplitude > 2 else "uncertain")
    assert metrics[0].evidence == (
        ref.model_copy(
            update={
                "start_seconds": 0.0,
                "end_seconds": 1.0,
                "artifact_key": ref.artifact_key.replace(
                    "received.wav", "played.wav" if with_played else "sent.wav"
                ),
            }
        ),
    )
    assert metadata["transcripts"][0]["source"] == "audio/received.wav"
    metric_name = "invented_metric"
    with pytest.raises(ValueError, match="exactly the requested"):
        await judge(evidence.directory, config, client=client)
    metric_name = "counterpart_validity"
    citation_name = "invented.wav"
    with pytest.raises(ValueError, match="unknown evidence"):
        await judge(evidence.directory, config, client=client)
    audit = evidence.directory / "evaluation/rejected-business-citation"
    citation_name = "business/final.json"
    with pytest.raises(ValueError, match="speech window"):
        await judge(evidence.directory, config, client=client, audit_directory=audit)
    diagnostic = json.loads((audit / "error.json").read_text())
    assert diagnostic["code"] == "missing_speech_evidence"
    assert diagnostic["metric"] == "counterpart_validity"
    assert (audit / "judge-response.json").exists()


@pytest.mark.asyncio
async def test_report_false_positive_is_rejected_with_retained_diagnostic(tmp_path):
    evidence = LocalEvidence(tmp_path, uuid4(), uuid4())
    case = fixture_case().model_dump(mode="json")
    case["criteria"]["rubrics"] = {"user_report_accuracy": "Report the actual issued reference."}
    await evidence.json("config/case.json", case)
    await evidence.json("business/final.json", {"bookings": [{"reference": "ZX-893K22"}]})
    await evidence.json("business/audit.json", [])
    await evidence.json("target/user-report.json", {"text": "Reference numbers: ZX893 and K22."})
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as audio:
        audio.setparams((1, 2, 8000, 0, "NONE", "none"))
        audio.writeframes(struct.pack("<h", 4096) * 8000 * 3)
    await evidence.store_artifact(evidence.run_id, "audio/received.wav", buffer.getvalue())
    await evidence.finalize(evidence.run_id)
    durations = []

    async def transcribe(**args):
        with wave.open(io.BytesIO(args["file"][1]), "rb") as chunk:
            durations.append(chunk.getnframes() / chunk.getframerate())
        return SimpleNamespace(text="Booking discussed.")

    async def parse(**args):
        prompt = json.loads(args["input"])
        assert len(prompt["evaluation_timeline"]["speech_windows"]) == 2
        assert prompt["derived_reference_comparison"]["comparison"] == "not_met"
        model = args["text_format"]
        metric = model.model_fields["metrics"].annotation.__args__[0]
        return SimpleNamespace(
            output_parsed=model.model_construct(
                metrics=(
                    metric.model_construct(
                        name="counterpart_validity",
                        status="uncertain",
                        explanation="Needs listening",
                        evidence=(),
                    ),
                    metric.model_construct(
                        name="user_report_accuracy",
                        status="met",
                        explanation="Incorrect model approval",
                        evidence=("target/user-report.json", "business/final.json"),
                    ),
                )
            ),
            model_dump_json=lambda **_: '{"incorrect_approval":true}',
        )

    client = SimpleNamespace(
        audio=SimpleNamespace(transcriptions=SimpleNamespace(create=transcribe)),
        responses=SimpleNamespace(parse=parse),
    )
    audit = evidence.directory / "evaluation/false-positive"
    config = JudgeConfig(
        model="fake",
        transcription_model="fake",
        rubric_version="test",
        transcription_chunk_seconds=2,
    )
    with pytest.raises(ValueError, match="contradicts"):
        await judge(evidence.directory, config, client=client, audit_directory=audit)
    assert durations == [2.0, 1.0]
    assert json.loads((audit / "error.json").read_text())["code"] == "reference_contradiction"
    assert json.loads((audit / "judge-response.json").read_text())["incorrect_approval"]
    assert not (audit / "result.json").exists()


@pytest.mark.asyncio
async def test_missing_report_does_not_discard_other_judgments(tmp_path):
    evidence = LocalEvidence(tmp_path, uuid4(), uuid4())
    case = fixture_case().model_dump(mode="json")
    case["criteria"]["rubrics"] = {"user_report_accuracy": "Judge actual report content."}
    for path, value in {
        "config/case.json": case,
        "business/final.json": {},
        "business/audit.json": [],
        "result.json": {"termination_confirmed": True},
        "target/report-requests.json": [],
    }.items():
        await evidence.json(path, value)
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as audio:
        audio.setparams((1, 2, 8000, 0, "NONE", "none"))
        audio.writeframes(b"\x00\x00" * 8000)
    for path in ("audio/received.wav", "audio/played.wav"):
        await evidence.store_artifact(evidence.run_id, path, buffer.getvalue())
    await evidence.finalize(evidence.run_id)

    async def parse(**args):
        parsed = args["text_format"].model_validate(
            {
                "metrics": [
                    {
                        "name": "counterpart_validity",
                        "status": "uncertain",
                        "explanation": "Needs listening",
                        "evidence": [],
                    },
                    {
                        "name": "user_report_accuracy",
                        "status": "not_met",
                        "explanation": "No report",
                        "evidence": ["result.json"],
                    },
                ]
            }
        )
        return SimpleNamespace(
            output_parsed=parsed, id="mock", usage=None, model_dump_json=lambda **_: '{"id":"mock"}'
        )

    client = SimpleNamespace(responses=SimpleNamespace(parse=parse))
    metrics, _ = await judge(
        evidence.directory,
        JudgeConfig(model="mock", transcription_model="mock", rubric_version="1"),
        client=client,
    )
    assert {m.name: m.status for m in metrics} == {
        "counterpart_validity": "uncertain",
        "user_report_accuracy": "not_applicable",
    }
