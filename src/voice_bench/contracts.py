"""Execution inputs, not a dataset authoring format."""

from decimal import Decimal
from typing import Any, Literal
from uuid import UUID

from pydantic import Field, model_validator

from voice_bench.models import (
    Channel,
    Contract,
    CounterpartBrief,
    FailureAttribution,
    UserTask,
    Validity,
)


class ExecutionCase(Contract):
    case_id: str = Field(min_length=1)
    version: str = Field(min_length=1)
    workflow: str = Field(min_length=1)
    workflow_version: str = Field(min_length=1)
    schema_version: Literal[2]
    user_task: UserTask
    counterpart: CounterpartBrief
    target_tools: tuple[str, ...] = ()
    counterpart_tools: tuple[str, ...] = ()
    task_scope: Literal["single_call", "multi_call"]
    call_initiation: Literal["harness_connected", "rumik_outbound"]
    initial_state: dict[str, Any]
    criteria: dict[str, Any]
    harness_fixture: bool = False

    @model_validator(mode="after")
    def validate_tool_names(self):
        import re

        for names in (self.target_tools, self.counterpart_tools):
            if len(names) != len(set(names)) or any(
                not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{0,63}", name) for name in names
            ):
                raise ValueError("Tool names must be unique identifiers within each role")
        return self

    def require_supported_execution(self):
        if self.task_scope != "single_call":
            raise ValueError(
                "Multi-call tasks need a task coordinator; execution is not implemented"
            )
        if self.call_initiation != "harness_connected":
            raise ValueError("Rumik outbound dialing is not implemented; no inbound fallback")


class PlannedRun(Contract):
    plan_id: UUID
    batch_id: UUID
    case_id: str
    case_version: str
    channel: Channel
    repetition: int = Field(ge=1)
    order: int = Field(ge=0)
    task_scope: Literal["single_call", "multi_call", "legacy_unspecified"] = "legacy_unspecified"
    call_initiation: Literal["harness_connected", "rumik_outbound", "legacy_unspecified"] = (
        "legacy_unspecified"
    )


class AttemptResult(Contract):
    run_id: UUID
    connected: bool = False
    validity: Validity = Validity.UNRESOLVED
    attribution: FailureAttribution = FailureAttribution.UNKNOWN
    outcome: Literal["passed", "failed", "unresolved"] = "unresolved"
    termination_confirmed: bool = False
    error: str | None = None


class CounterpartConfig(Contract):
    model: str = ""
    voice: str = ""
    instructions: str = ""
    turn_detection: dict[str, Any] = Field(default_factory=dict)
    # An explicit counterpart behavior, independent of the target's interruption behavior.
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
