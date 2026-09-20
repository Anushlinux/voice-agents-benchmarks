"""Execution inputs, not a dataset authoring format."""

from decimal import Decimal
from typing import Any, Literal
from uuid import UUID

from pydantic import Field

from voice_bench.models import CallerBrief, Channel, Contract, FailureAttribution, Validity


class ExecutionCase(Contract):
    case_id: str = Field(min_length=1)
    version: str = Field(min_length=1)
    workflow: str = Field(min_length=1)
    workflow_version: str = Field(min_length=1)
    caller: CallerBrief
    initial_state: dict[str, Any]
    criteria: dict[str, Any]
    harness_fixture: bool = False


class PlannedRun(Contract):
    plan_id: UUID
    batch_id: UUID
    case_id: str
    case_version: str
    channel: Channel
    repetition: int = Field(ge=1)
    order: int = Field(ge=0)


class AttemptResult(Contract):
    run_id: UUID
    connected: bool = False
    validity: Validity = Validity.UNRESOLVED
    attribution: FailureAttribution = FailureAttribution.UNKNOWN
    outcome: Literal["passed", "failed", "unresolved"] = "unresolved"
    termination_confirmed: bool = False
    error: str | None = None


class CallerConfig(Contract):
    model: str = ""
    voice: str = ""
    instructions: str = ""
    turn_detection: dict[str, Any] = Field(default_factory=dict)
    # An explicit caller behavior, independent of the target's interruption behavior.
    interrupt_after_ms: int | None = Field(default=None, gt=0)
    max_output_tokens: int = Field(default=512, gt=0)


class JudgeConfig(Contract):
    model: str = ""
    transcription_model: str = ""
    rubric_version: str = ""
    max_output_tokens: int = Field(default=2048, gt=0)
    cost_ceiling_inr: Decimal = Field(default=Decimal(0), ge=0, allow_inf_nan=False)


class RuntimeConfig(Contract):
    public_base_url: str = ""
    caller_number: str = ""
    target_number: str = ""
    region: str = "ap-south-1"
    setup_timeout_seconds: int = Field(default=45, gt=0)
    finalize_timeout_seconds: int = Field(default=30, gt=0)
    media_timeout_seconds: int = Field(default=15, gt=0)
    # Operator-supplied conservative maximums, not current provider prices.
    cost_ceiling_inr_per_attempt: Decimal = Field(default=Decimal(0), ge=0, allow_inf_nan=False)
    cost_components_inr_per_attempt: dict[str, Decimal] = Field(default_factory=dict)
    rate_card_version: str = ""
    artifact_bucket: str = ""
    artifact_endpoint_url: str = ""


class PlaybackProgress(Contract):
    item_id: str
    played_ms: int = Field(ge=0)
    boundary: Literal["browser_render", "carrier_checkpoint", "unconfirmed"]
    clock_id: str


class ToolRequest(Contract):
    call_id: str = Field(min_length=1, max_length=200)
    operation_id: str = Field(min_length=1, max_length=200)
    arguments: dict[str, Any]
