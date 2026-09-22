"""Execution inputs, not a dataset authoring format."""

from decimal import Decimal
from typing import Any, Literal
from uuid import UUID

from pydantic import Field, model_validator

from voice_bench.evaluation.rubrics import EvaluationRubric
from voice_bench.models import (
    Channel,
    Contract,
    CounterpartBrief,
    FailureAttribution,
    UserTask,
    Validity,
)
from voice_bench.scenarios import CounterpartProfile, ScenarioPolicy


class ConversationEvent(Contract):
    """Counterpart-only challenge; never an instruction or scripted reply for Rumik."""

    event_id: str = Field(min_length=1, max_length=64, pattern=r"^[a-zA-Z0-9_-]+$")
    trigger_tool: str = Field(min_length=1)
    occurrence: int = Field(default=1, ge=1)
    priority: int = Field(default=0, ge=0, le=100)
    after_tools: tuple[str, ...] = ()
    kind: Literal["misread", "clarification", "distraction"]
    field: str = Field(min_length=1)
    spoken_value: str = Field(min_length=1)
    instruction: str = Field(min_length=1)
    required_evidence: tuple[str, ...] = (
        "played_audio",
        "received_audio",
        "event_link",
        "human_content_review",
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
    # Legacy cases retain their first-final-report contract. New cases can permit
    # corrections while the call is open without erasing earlier submissions.
    report_policy: Literal["final_once", "revisable_until_close"] = "final_once"
    completion: Literal[
        "counterpart", "target_report_then_hangup", "target_report_then_conversation_end"
    ] = "counterpart"
    counterpart_tools: tuple[str, ...] = ()
    task_scope: Literal["single_call", "multi_call"]
    call_initiation: Literal["harness_connected", "rumik_outbound"]
    initial_state: dict[str, Any]
    criteria: dict[str, Any]
    harness_fixture: bool = False
    conversation_events: tuple[ConversationEvent, ...] = ()
    counterpart_profile: CounterpartProfile | None = None
    scenario_policy: ScenarioPolicy | None = None
    evaluation_rubric: EvaluationRubric | None = None

    @model_validator(mode="after")
    def validate_tool_names(self):
        import re

        if self.completion != "counterpart" and "submit_user_report" not in self.target_tools:
            raise ValueError("Report completion requires the explicit target reporting tool")

        for names in (self.target_tools, self.counterpart_tools):
            if len(names) != len(set(names)) or any(
                not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{0,63}", name) for name in names
            ):
                raise ValueError("Tool names must be unique identifiers within each role")
        ids = [e.event_id for e in self.conversation_events]
        if len(set(ids)) != len(ids):
            raise ValueError("Conversation event IDs must be unique")
        for event in self.conversation_events:
            if not {event.trigger_tool, *event.after_tools}.issubset(self.counterpart_tools):
                raise ValueError("Event triggers must name granted counterpart tools")
        if self.evaluation_rubric is not None:
            required = set(self.criteria.get("required_metrics", []))
            declared = {
                m.name
                for m in self.evaluation_rubric.metrics
                if m.applies and m.role != "diagnostic"
            }
            if not required or required != declared:
                raise ValueError("Rubric must cover exactly the required metrics")
        return self

    def require_supported_execution(self):
        if self.conversation_events:
            raise ValueError(
                "Legacy tool-count speech challenges are retired from live execution: "
                "they do not establish previously heard or agreed terms. Use a natural "
                "case without injected speech; historical evidence remains reviewable."
            )
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
    conversation_end: Literal["target_hangup", "counterpart_finish"] | None = None
    error: str | None = None
    failure_stage: (
        Literal["preparation", "connection", "task_delivery", "conversation", "shutdown"] | None
    ) = None


class CounterpartFinished(Contract):
    """Explicit employee hangup intent, returned only after closing playback drains."""

    tool_call_id: str = Field(min_length=1)


class CounterpartConfig(Contract):
    model: str = ""
    voice: str = ""
    instructions: str = ""
    turn_detection: dict[str, Any] = Field(default_factory=dict)
    # An explicit counterpart behavior, independent of the target's interruption behavior.
    interrupt_after_ms: int | None = Field(default=None, gt=0)
    max_output_tokens: int = Field(default=2048, gt=0)
    # Diagnostic stop, never a target failure or an invented continuation.
    conversation_idle_seconds: float = Field(default=45, gt=0)
    silence_recovery_seconds: float = Field(default=0, ge=0)
    max_silence_recovery_prompts: int = Field(default=0, ge=0, le=2)


class JudgeConfig(Contract):
    model: str = ""
    transcription_model: str = ""
    rubric_version: str = ""
    max_output_tokens: int = Field(default=2048, gt=0)
    transcription_chunk_seconds: int = Field(default=15, ge=1, le=180)
    cost_ceiling_inr: Decimal = Field(default=Decimal(0), ge=0, allow_inf_nan=False)


class RuntimeConfig(Contract):
    public_base_url: str = ""
    caller_number: str = ""
    target_number: str = ""
    # Optional direct SIP destination for the carrier leg, such as the target's SIP
    # origination host. target_number stays the number registered on that trunk.
    target_sip_uri: str = ""
    region: str = "ap-south-1"
    setup_timeout_seconds: int = Field(default=45, gt=0)
    finalize_timeout_seconds: int = Field(default=30, gt=0)
    media_timeout_seconds: int = Field(default=15, gt=0)
    post_report_hangup_seconds: float = Field(default=30, gt=0)
    # Let trailing received speech clear after an explicit employee finish.
    conversation_end_quiet_seconds: float = Field(default=1, gt=0)
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
