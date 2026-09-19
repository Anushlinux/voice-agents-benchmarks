from typing import Any, Protocol

from voice_bench.models import EvidenceRef, MetricResult, RunContext


class Evaluator(Protocol):
    """Only this boundary receives private criteria and the finalized evidence set."""

    async def evaluate(
        self,
        run: RunContext,
        criteria: dict[str, Any],
        evidence: tuple[EvidenceRef, ...],
    ) -> tuple[MetricResult, ...]: ...
