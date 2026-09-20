"""Load local planning configuration without credentials or network activity."""

import tomllib
from decimal import Decimal
from pathlib import Path
from typing import Literal
from uuid import UUID

from pydantic import Field, field_validator

from voice_bench.contracts import CounterpartConfig, JudgeConfig, RuntimeConfig
from voice_bench.evaluation.jev import JevConfig
from voice_bench.models import Channel, Contract


class TargetConfig(Contract):
    agent_ref: str = ""
    deployed_version: str = ""
    task_variable: str = Field(
        default="benchmark_user_task", pattern=r"^[A-Za-z][A-Za-z0-9_]{0,63}$"
    )
    plivo_sip_trunk_id: UUID | None = None
    plivo_termination_uri: str = ""


class RunLimits(Contract):
    max_call_seconds: int = Field(gt=0)
    max_concurrent_calls: int = Field(gt=0)
    max_attempts_per_case: int = Field(gt=0)
    max_total_call_minutes: int = Field(ge=0)
    max_spend_inr: Decimal = Field(ge=0, allow_inf_nan=False)


class BenchmarkConfig(Contract):
    name: str = Field(min_length=1)
    purpose: Literal["development", "qualification", "benchmark"] = "development"
    channels: tuple[Channel, ...] = Field(min_length=1)
    artifact_root: Path
    target: TargetConfig
    limits: RunLimits
    counterpart: CounterpartConfig = Field(default_factory=CounterpartConfig)
    judge: JudgeConfig = Field(default_factory=JudgeConfig)
    jev: JevConfig = Field(default_factory=JevConfig)
    runtime: RuntimeConfig = Field(default_factory=RuntimeConfig)

    @field_validator("channels")
    @classmethod
    def unique_channels(cls, value: tuple[Channel, ...]) -> tuple[Channel, ...]:
        if len(value) != len(set(value)):
            raise ValueError("Each channel must appear only once")
        return value


def load_config(path: Path) -> BenchmarkConfig:
    """Resolve artifact paths relative to the config file's parent directory."""
    path = path.resolve()
    with path.open("rb") as handle:
        config = BenchmarkConfig.model_validate(tomllib.load(handle))
    artifact_root = config.artifact_root
    if not artifact_root.is_absolute():
        artifact_root = (path.parent / artifact_root).resolve()
    return config.model_copy(update={"artifact_root": artifact_root})
