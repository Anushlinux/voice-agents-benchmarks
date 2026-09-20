import io
import json
import wave
from types import SimpleNamespace
from uuid import uuid4

import pytest

from voice_bench.contracts import JudgeConfig
from voice_bench.evaluation.openai_judge import judge
from voice_bench.evaluation.scoring import JudgeOutput
from voice_bench.evidence.local import LocalEvidence
from voice_bench.fixture import fixture_case
from voice_bench.models import EvidenceRef, MetricResult


@pytest.mark.asyncio
async def test_model_judge_transcribes_captured_audio_and_rejects_invented_citations(tmp_path):
    evidence = LocalEvidence(tmp_path, uuid4(), uuid4())
    await evidence.json("config/case.json", fixture_case().model_dump(mode="json"))
    await evidence.json("business/final.json", {"note": "initial"})
    await evidence.json("business/audit.json", [])
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as audio:
        audio.setparams((1, 2, 8000, 0, "NONE", "none"))
        audio.writeframes(b"\x00\x10" * 8000)
    ref = await evidence.store_artifact(evidence.run_id, "audio/received.wav", buffer.getvalue())
    await evidence.finalize(evidence.run_id)
    config = JudgeConfig(
        model="test-judge", transcription_model="test-transcribe", rubric_version="1"
    )
    calls = []

    async def transcribe(**args):
        calls.append("transcribe")
        assert args["file"][1][:4] == b"RIFF"
        return SimpleNamespace(text="The target CLAIMED it changed the note.")

    async def parse(**args):
        calls.append("judge")
        assert args["model"] == "test-judge"
        assert json.loads(args["input"])["state"] == {"note": "initial"}
        return SimpleNamespace(
            output_parsed=JudgeOutput(
                metrics=(
                    MetricResult(
                        name="caller_validity",
                        status="met",
                        explanation="Adhered to brief.",
                        evidence=(ref,),
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
    assert calls == ["transcribe", "judge"]
    assert metrics[0].status == "met"
    assert metadata["transcripts"][0]["source"] == "audio/received.wav"
    ref = EvidenceRef(artifact_key=ref.artifact_key, sha256="0" * 64)
    with pytest.raises(ValueError, match="sealed evidence"):
        await judge(evidence.directory, config, client=client)
