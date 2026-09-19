from typing import Any, Protocol
from uuid import UUID


class BusinessEnvironment(Protocol):
    async def prepare(self, run_id: UUID, initial_state: dict[str, Any]) -> None: ...

    async def execute(
        self, run_id: UUID, tool: str, arguments: dict[str, Any], request_id: str
    ) -> dict[str, Any]: ...

    async def snapshot(self, run_id: UUID) -> dict[str, Any]: ...
