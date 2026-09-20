from typing import Protocol

from voice_bench.channels.interfaces import AudioSession
from voice_bench.evidence.interfaces import EvidenceSink
from voice_bench.models import CounterpartBrief, RunContext


class CounterpartSimulator(Protocol):
    """Receives its role, channel audio and permitted tool results, never private user goals."""

    async def converse(
        self,
        run: RunContext,
        brief: CounterpartBrief,
        session: AudioSession,
        evidence: EvidenceSink,
        *,
        conversation_events: tuple = (),
        scenario_policy=None,
    ) -> None: ...
