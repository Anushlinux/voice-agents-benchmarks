from typing import Protocol
from uuid import UUID

from voice_bench.models import EvidenceEvent, EvidenceRef


class EvidenceSink(Protocol):
    async def append(self, event: EvidenceEvent) -> None: ...

    async def store_artifact(
        self, run_id: UUID, name: str, content: bytes, media_type: str
    ) -> EvidenceRef: ...

    async def finalize(self, run_id: UUID) -> tuple[EvidenceRef, ...]: ...
