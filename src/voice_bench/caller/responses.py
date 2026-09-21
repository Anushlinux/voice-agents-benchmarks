"""One owner for response creation; input audio remains independent."""

import asyncio


class ResponseCoordinator:
    def __init__(self, send, evidence, request_factory, blocked):
        self.send, self.evidence = send, evidence
        self.request_factory, self.blocked = request_factory, blocked
        self.changed = asyncio.Event()
        self.idle = asyncio.Event()
        self.idle.set()
        self.reasons = set()
        self.response_id = None
        self.cancel_pending = False
        self.cancel_sent = False
        self.closed = False
        self.override = None
        self.completed_ids = set()

    def request(self, reason, override=None):
        if self.closed:
            return
        self.reasons.add(reason)
        self.override = override
        self.changed.set()

    async def created(self, response_id):
        self.idle.clear()
        self.response_id = response_id
        await self.evidence.emit("caller", "response_created", {"response_id": response_id})
        if self.cancel_pending:
            await self.cancel()

    async def cancel(self):
        if self.idle.is_set():
            return
        self.cancel_pending = True
        if self.response_id and not self.cancel_sent:
            self.cancel_sent = True
            await self.send({"type": "response.cancel", "response_id": self.response_id})
            await self.evidence.emit(
                "caller", "response_cancel_requested", {"response_id": self.response_id}
            )

    def done(self, response_id):
        if response_id is not None and response_id in self.completed_ids:
            return
        if self.response_id is not None and self.response_id != response_id:
            return  # A late event must not clear a newer response.
        if response_id is not None:
            self.completed_ids.add(response_id)
        self.response_id = None
        self.cancel_pending = self.cancel_sent = False
        self.idle.set()
        self.changed.set()

    def close(self):
        self.closed = True
        self.reasons.clear()
        self.changed.set()

    def defer(self, reasons, override):
        self.reasons.update(reasons)
        if self.override is None:
            self.override = override
        self.cancel_pending = self.cancel_sent = False
        self.idle.set()

    async def run(self):
        while not self.closed:
            await self.changed.wait()
            self.changed.clear()
            if self.closed or not self.reasons or not self.idle.is_set() or self.blocked():
                continue
            # Reserve the response synchronously, before any network/evidence await.
            self.idle.clear()
            reasons, self.reasons = sorted(self.reasons), set()
            override, self.override = self.override, None
            request = override or await self.request_factory()
            if self.closed:
                return
            if self.blocked():
                self.defer(reasons, override)
                continue
            await self.evidence.emit("caller", "response_requested", {"reasons": reasons})
            if self.closed:
                return
            if self.blocked():
                self.defer(reasons, override)
                await self.evidence.emit("caller", "response_deferred_for_input")
                continue
            await self.send(request)
