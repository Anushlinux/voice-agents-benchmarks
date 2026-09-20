import io
import json
import struct
import wave
from types import SimpleNamespace
from uuid import uuid4

import pytest

from voice_bench.contracts import JudgeConfig
from voice_bench.evaluation.openai_judge import judge
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
    citation_name = "audio/received.wav"

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
        assert prompt["target_user_report"] == final_report
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
                    ),
                )
            ),
            id="fake-response",
            usage=None,
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
    assert metrics[0].status == "met"
    assert metrics[0].evidence == (ref,)
    assert metadata["transcripts"][0]["source"] == "audio/received.wav"
    metric_name = "invented_metric"
    with pytest.raises(ValueError, match="exactly the requested"):
        await judge(evidence.directory, config, client=client)
    metric_name = "counterpart_validity"
    citation_name = "invented.wav"
    with pytest.raises(ValueError, match="unknown evidence"):
        await judge(evidence.directory, config, client=client)
