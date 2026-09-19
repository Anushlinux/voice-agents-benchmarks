from typing import Protocol

from voice_bench.channels.interfaces import AudioSession
from voice_bench.evidence.interfaces import EvidenceSink
from voice_bench.models import CallerBrief, RunContext


class CallerSimulator(Protocol):
    """Receives customer facts and channel audio, never target transcripts or oracle state."""

    async def converse(
        self,
        run: RunContext,
        brief: CallerBrief,
        session: AudioSession,
        evidence: EvidenceSink,
    ) -> None: ...
