from datetime import datetime
from uuid import uuid4

import pytest
from pydantic import ValidationError

from voice_bench.models import AudioFrame, CallerBrief, EvidenceEvent, MetricResult


def test_caller_brief_rejects_evaluator_only_inputs():
    with pytest.raises(ValidationError, match="Extra inputs"):
        CallerBrief.model_validate(
            {"goal": "Ask for help", "known_facts": {}, "expected_outcome": "private answer"}
        )


@pytest.mark.parametrize("audio", [b"", b"\x00"])
def test_audio_rejects_empty_or_partial_samples(audio):
    with pytest.raises(ValidationError, match="complete, non-empty"):
        AudioFrame(
            pcm_s16le=audio,
            sample_rate_hz=24000,
            sample_offset=0,
            observed_monotonic_ns=0,
            clock_id="worker",
        )


def test_evidence_rejects_ambiguous_wall_clock():
    with pytest.raises(ValidationError, match="timezone"):
        EvidenceEvent(
            run_id=uuid4(),
            source="channel",
            kind="connected",
            sequence=0,
            clock_id="worker",
            observed_monotonic_ns=0,
            observed_at=datetime(2026, 9, 20),
        )


@pytest.mark.parametrize("status", ["met", "not_met"])
def test_resolved_verdict_requires_evidence(status):
    with pytest.raises(ValidationError, match="requires evidence"):
        MetricResult(name="task_success", status=status, explanation="Unsubstantiated claim")


def test_missing_evidence_can_remain_uncertain():
    metric = MetricResult(
        name="speech_intelligibility",
        status="uncertain",
        explanation="The received recording is missing.",
    )
    assert metric.status == "uncertain"
