"""Shared boundary contracts, independent of any provider SDK.

These are execution contracts, not a finalized dataset format. Private business
state and evaluation criteria must never be added to participant briefs or CallRequest.
"""

from datetime import datetime
from enum import StrEnum
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class Contract(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class Channel(StrEnum):
    BROWSER = "browser"
    PHONE = "phone"


class RunPhase(StrEnum):
    PREPARED = "prepared"
    CONNECTING = "connecting"
    IN_CONVERSATION = "in_conversation"
    FINALIZING = "finalizing"
    GRADING = "grading"
    REVIEWED = "reviewed"
    FAILED = "failed"


class RunContext(Contract):
    run_id: UUID
    case_id: str = Field(min_length=1)
    case_version: str = Field(min_length=1)
    repetition: int = Field(ge=1)
    channel: Channel
    config_digest: str = Field(min_length=1)


class UserTask(Contract):
    """The user's assignment and authorization, delivered only to Rumik."""

    request: str = Field(min_length=1)
    known_facts: dict[str, Any]
    constraints: tuple[str, ...]
    permissions: tuple[str, ...]


class CounterpartBrief(Contract):
    """The other person's role and facts; never the user's private instructions."""

    role: str = Field(min_length=1)
    goal: str = Field(min_length=1)
    known_facts: dict[str, Any]
    behavior_rules: tuple[str, ...] = ()


class CallRequest(Contract):
    """Transport setup only: never contains hidden expected outcomes."""

    run: RunContext
    agent_ref: str = Field(min_length=1)
    max_duration_seconds: int = Field(gt=0)


class AudioFrame(Contract):
    """PCM at the adapter boundary; wire codecs are handled inside adapters.

    observed_monotonic_ns is local observation time, not proof of remote
    playout. Sample offsets and named clocks support later timeline alignment.
    """

    pcm_s16le: bytes
    sample_rate_hz: int = Field(gt=0)
    channels: Literal[1] = 1
    sample_offset: int = Field(ge=0)
    observed_monotonic_ns: int = Field(ge=0)
    clock_id: str = Field(min_length=1)
    item_id: str = ""

    @field_validator("pcm_s16le")
    @classmethod
    def require_complete_samples(cls, value: bytes) -> bytes:
        if not value or len(value) % 2:
            raise ValueError("PCM must contain complete, non-empty signed 16-bit samples")
        return value


class EvidenceEvent(Contract):
    schema_version: Literal[1] = 1
    run_id: UUID
    source: Literal["controller", "caller", "channel", "target", "business", "evaluation"]
    kind: str = Field(min_length=1)
    sequence: int = Field(ge=0)
    clock_id: str = Field(min_length=1)
    observed_monotonic_ns: int = Field(ge=0)
    observed_at: datetime
    payload: dict[str, Any] = Field(default_factory=dict)

    @field_validator("observed_at")
    @classmethod
    def require_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("Evidence timestamps must include a timezone")
        return value


class EvidenceRef(Contract):
    """Stable stored artifact identity, never an expiring provider URL."""

    artifact_key: str = Field(min_length=1)
    sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    event_sequences: tuple[int, ...] = ()
    start_seconds: float | None = Field(default=None, ge=0)
    end_seconds: float | None = Field(default=None, ge=0)

    @model_validator(mode="after")
    def valid_range(self):
        if (self.start_seconds is None) != (self.end_seconds is None):
            raise ValueError("Both audio range boundaries are required")
        if self.start_seconds is not None and self.end_seconds <= self.start_seconds:
            raise ValueError("Audio range must have positive duration")
        if any(n < 0 for n in self.event_sequences):
            raise ValueError("Event sequences must be nonnegative")
        return self


class MetricResult(Contract):
    name: str = Field(min_length=1)
    status: Literal["met", "not_met", "uncertain", "not_applicable"]
    explanation: str = Field(min_length=1)
    evidence: tuple[EvidenceRef, ...] = ()

    @model_validator(mode="after")
    def require_evidence_for_verdict(self) -> "MetricResult":
        if self.status in {"met", "not_met"} and not self.evidence:
            raise ValueError("A resolved metric verdict requires evidence references")
        return self


class Validity(StrEnum):
    VALID = "valid"
    INVALID = "invalid"
    UNRESOLVED = "unresolved"


class FailureAttribution(StrEnum):
    TARGET = "target"
    SIMULATOR = "simulator"
    HARNESS = "harness"
    UNKNOWN = "unknown"
