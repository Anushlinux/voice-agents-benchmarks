from collections.abc import AsyncIterator
from typing import Protocol

from voice_bench.evidence.interfaces import EvidenceSink
from voice_bench.models import AudioFrame, CallRequest, EvidenceEvent


class AudioSession(Protocol):
    """Receive loops must remain active while the caller sends speech."""

    async def send_audio(self, frame: AudioFrame) -> None: ...

    def received_audio(self) -> AsyncIterator[AudioFrame]: ...

    def check_health(self) -> None: ...

    def events(self) -> AsyncIterator[EvidenceEvent]: ...

    async def close(self, reason: str) -> None: ...

    async def drain(self) -> None: ...

    async def cancel_playback(self) -> dict[str, int]:
        """Cancel caller output and return confirmed played milliseconds per item."""
        ...


class ChannelAdapter(Protocol):
    async def connect(self, request: CallRequest, evidence: EvidenceSink) -> AudioSession: ...

    async def reconcile(self, run_id, evidence: EvidenceSink) -> bool: ...
