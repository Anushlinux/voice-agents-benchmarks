from collections.abc import AsyncIterator
from typing import Protocol

from voice_bench.models import AudioFrame, CallRequest, EvidenceEvent


class AudioSession(Protocol):
    """Receive loops must remain active while the caller sends speech."""

    async def send_audio(self, frame: AudioFrame) -> None: ...

    def received_audio(self) -> AsyncIterator[AudioFrame]: ...

    def events(self) -> AsyncIterator[EvidenceEvent]: ...

    async def close(self, reason: str) -> None: ...


class ChannelAdapter(Protocol):
    async def connect(self, request: CallRequest) -> AudioSession: ...
