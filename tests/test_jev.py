import io
import json
import wave
from contextlib import contextmanager
from copy import deepcopy
from decimal import Decimal
from pathlib import Path
from uuid import uuid4

import httpx
import pytest
import pytest_asyncio

from voice_bench.cli import main
from voice_bench.evaluation.jev import JevConfig, JevRubric, evaluate, prepare, validate_response
from voice_bench.evaluation.scoring import review_template, save_evaluation
from voice_bench.evidence.local import LocalEvidence
from voice_bench.fixture import fixture_case
from voice_bench.settings import load_config


@pytest.fixture
def rubric():
    return JevRubric(
        version="unit-only-v1",
        questions={
            "choice": {
                "type": "choice",
                "instructions": "Was the request followed?",
                "criteria": {"yes": "Evidence supports adherence", "unknown": "Insufficient proof"},
            },
            "score": {
                "type": "score",
                "instructions": "Rate clarity of the text",
                "criteria": ["Unclear", "Clear"],
            },
            "noul": {"type": "noul", "instructions": "Does the target claim completion?"},
        },
    )


def response():
    return {
        "model": "jev-test-resolved",
        "usage": {"input_tokens": 10, "output_tokens": 0},
        "answers": {
            "choice": {
                "type": "choice",
                "choice": "yes",
                "confidence": 0.8,
                "probabilities": {"yes": 0.9, "unknown": 0.1},
            },
            "score": {
                "type": "score",
                "score": 0.75,
                "confidence": 0.5,
                "legend": {"0": "Unclear", "1": "Clear"},
                "probabilities": {"0": 0.25, "1": 0.75},
            },
            "noul": {"type": "noul", "noul": 0.6},
        },
    }


@pytest_asyncio.fixture
async def bundle(tmp_path):
    case = fixture_case()
    evidence = LocalEvidence(tmp_path, uuid4(), uuid4())
    await evidence.json("config/case.json", case.model_dump(mode="json"))
    await evidence.json("business/initial.json", case.initial_state)
    await evidence.json("business/final.json", case.initial_state)
    await evidence.json("business/audit.json", [])
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as audio:
        audio.setparams((1, 2, 8000, 0, "NONE", "none"))
        audio.writeframes(b"\0\0" * 8000)
    transcripts = []
    for name in ("received", "played", "sent"):
        ref = await evidence.store_artifact(evidence.run_id, f"audio/{name}.wav", buffer.getvalue())
        ref = ref.model_copy(update={"start_seconds": 0, "end_seconds": 1})
        transcripts.append(
            {
                "source": f"audio/{name}.wav",
                "text": f"test-only-{name}",
                "evidence": ref.model_dump(mode="json"),
            }
        )
    await evidence.finalize(evidence.run_id)
    save_evaluation(
        evidence.directory,
        "source",
        [],
        judge={"transcripts": transcripts, "response_id": "must-not-be-sent", "verdict": "biased"},
    )
    return evidence.directory


class BudgetStore:
    def __init__(self):
        self.batch = {"limits": {"max_spend_inr": "2"}}

    @contextmanager
    def locked_batch(self, batch_id):
        yield None, self.batch


def config():
    value = load_config(Path("configs/local.toml"))
    return value.model_copy(
        update={
            "jev": JevConfig(model="jev-test", cost_ceiling_inr=Decimal("1")),
            "runtime": value.runtime.model_copy(update={"rate_card_version": "unit"}),
            "limits": value.limits.model_copy(update={"max_spend_inr": Decimal("2")}),
        }
    )


@pytest.mark.asyncio
async def test_prepare_is_offline_and_only_sends_selected_text_evidence(bundle, rubric):
    directory = bundle
    prepared = prepare(directory, "source", rubric, config().jev)
    state = prepared["request"]["state"]
    assert [t["source"] for t in state["transcripts"]] == ["audio/received.wav", "audio/played.wav"]
    assert state["user_task"] == fixture_case().user_task.model_dump(mode="json")
    assert "biased" not in json.dumps(prepared)
    assert "must-not-be-sent" not in json.dumps(prepared)
    assert len(prepared["source_evaluation"]["sha256"]) == 64
    with pytest.raises(ValueError, match="not truncated"):
        prepare(
            directory, "source", rubric, config().jev.model_copy(update={"max_request_bytes": 1})
        )
    with pytest.raises(ValueError, match="Invalid source"):
        prepare(directory, "../source", rubric, config().jev)
    (directory / "audio/received.wav").write_bytes(b"tampered")
    with pytest.raises(ValueError, match="checksum"):
        prepare(directory, "source", rubric, config().jev)


@pytest.mark.parametrize(
    "damage", ["nan", "bool", "partial", "sum", "choice", "score", "legend", "type"]
)
def test_response_rejects_malformed_or_partial_decisions(rubric, damage):
    body = response()
    if damage == "nan":
        body["answers"]["noul"]["noul"] = float("nan")
    elif damage == "bool":
        body["answers"]["noul"]["noul"] = True
    elif damage == "partial":
        del body["answers"]["noul"]
    elif damage == "sum":
        body["answers"]["choice"]["probabilities"]["yes"] = 0.5
    elif damage == "choice":
        body["answers"]["choice"]["choice"] = "unknown"
    elif damage == "score":
        body["answers"]["score"]["score"] = 0.2
    elif damage == "legend":
        body["answers"]["score"]["legend"]["1"] = "Changed rubric"
    elif damage == "type":
        body["answers"]["noul"]["type"] = "choice"
    with pytest.raises(ValueError):
        validate_response(body, rubric.model_dump(mode="json")["questions"])


@pytest.mark.asyncio
async def test_paid_shadow_preserves_evidence_and_cannot_be_reviewed_as_grade(
    bundle, rubric, monkeypatch
):
    directory = bundle
    monkeypatch.setenv("TYPESAFE_API_KEY", "unit-secret")
    store = BudgetStore()
    calls = []

    def handler(request):
        calls.append(request)
        assert request.url == "https://api.typesafe.ai/v1/systemone"
        assert request.headers["authorization"] == "Bearer unit-secret"
        return httpx.Response(200, json=response())

    with pytest.raises(ValueError, match="--live"):
        await evaluate(directory, "source", rubric, config(), "shadow", store)
    assert not calls and "reservations" not in store.batch
    manifest = (directory / "manifest.json").read_bytes()
    path = await evaluate(
        directory,
        "source",
        rubric,
        config(),
        "shadow",
        store,
        live=True,
        transport=httpx.MockTransport(handler),
    )
    result = json.loads(path.read_bytes())
    assert result["status"] == "completed" and result["outcome"] == "unresolved"
    assert result["metrics"] == [] and result["mode"] == "shadow"
    assert result["answers"]["noul"]["noul"] == 0.6
    assert result["resolved_model"] == "jev-test-resolved"
    assert "unit-secret" not in path.read_text()
    assert (directory / "manifest.json").read_bytes() == manifest
    assert next(iter(store.batch["reservations"].values()))["provider"] == "typesafe"
    with pytest.raises(ValueError, match="Shadow"):
        review_template(directory, "shadow")
    with pytest.raises(ValueError, match="already exists"):
        await evaluate(directory, "source", rubric, config(), "shadow", store, live=True)
    assert len(calls) == 1


@pytest.mark.asyncio
async def test_openrouter_uses_only_selected_provider_and_preserves_route(
    bundle, rubric, monkeypatch
):
    cfg = config()
    cfg = cfg.model_copy(
        update={
            "jev": cfg.jev.model_copy(
                update={"provider": "openrouter", "model": "typesafe/jev-1.13"}
            )
        }
    )
    monkeypatch.setenv("TYPESAFE_API_KEY", "wrong-provider-secret")
    store = BudgetStore()
    with pytest.raises(ValueError, match="OPENROUTER_API_KEY"):
        await evaluate(bundle, "source", rubric, cfg, "router", store, live=True)
    assert "reservations" not in store.batch
    monkeypatch.setenv("OPENROUTER_API_KEY", "router-secret")
    calls = []

    def handler(request):
        calls.append(request)
        assert str(request.url) == "https://openrouter.ai/api/alpha/decisions"
        assert request.headers["authorization"] == "Bearer router-secret"
        assert json.loads(request.content)["model"] == "typesafe/jev-1.13"
        return httpx.Response(429, json={"error": "limited"})

    with pytest.raises(ValueError, match="budget retained"):
        await evaluate(
            bundle,
            "source",
            rubric,
            cfg,
            "router",
            store,
            live=True,
            transport=httpx.MockTransport(handler),
        )
    assert len(calls) == 1
    result = json.loads((bundle / "evaluation/router/result.json").read_bytes())
    assert result["config"]["provider"] == "openrouter"
    assert result["endpoint"] == "https://openrouter.ai/api/alpha/decisions"
    assert result["status"] == "error"
    assert next(iter(store.batch["reservations"].values()))["provider"] == "openrouter"
    assert "router-secret" not in json.dumps(result)


@pytest.mark.asyncio
@pytest.mark.parametrize("failure", ["timeout", "rate_limit", "bad_json", "bad_answer"])
async def test_jev_failures_are_saved_and_never_retried(bundle, rubric, monkeypatch, failure):
    directory = bundle
    monkeypatch.setenv("TYPESAFE_API_KEY", "unit-secret")
    store = BudgetStore()
    calls = []

    def handler(request):
        calls.append(request)
        if failure == "timeout":
            raise httpx.ReadTimeout("test", request=request)
        if failure == "rate_limit":
            return httpx.Response(429, json={"error": "limited"})
        if failure == "bad_json":
            return httpx.Response(200, text="not json")
        return httpx.Response(200, json={"answers": {}})

    with pytest.raises(ValueError, match="budget retained"):
        await evaluate(
            directory,
            "source",
            rubric,
            config(),
            "failed",
            store,
            live=True,
            transport=httpx.MockTransport(handler),
        )
    assert len(calls) == 1
    saved = json.loads((directory / "evaluation/failed/result.json").read_bytes())
    assert saved["status"] == "error" and saved["outcome"] == "unresolved"
    assert len(store.batch["reservations"]) == 1
    assert (directory / "evaluation/failed/request.json").exists()


@pytest.mark.asyncio
async def test_saved_transcript_cannot_claim_different_audio_source(bundle, rubric):
    directory = bundle
    source = directory / "evaluation/source/result.json"
    value = json.loads(source.read_bytes())
    value["judge"]["transcripts"][0]["evidence"] = deepcopy(
        value["judge"]["transcripts"][1]["evidence"]
    )
    source.write_text(json.dumps(value))
    with pytest.raises(ValueError, match="does not match"):
        prepare(directory, "source", rubric, config().jev)


def test_jev_cli_refuses_live_without_switch_before_opening_database(tmp_path, capsys):
    rubric = tmp_path / "rubric.json"
    rubric.write_text(
        json.dumps(
            {
                "version": "unit",
                "questions": {"check": {"type": "noul", "instructions": "Is the claim supported?"}},
            }
        )
    )
    assert (
        main(
            [
                "jev",
                "evaluate",
                str(tmp_path),
                "--source-version",
                "source",
                "--rubric",
                str(rubric),
                "--config",
                "configs/local.toml",
                "--version",
                "v1",
            ]
        )
        == 2
    )
    assert "--live" in capsys.readouterr().err
