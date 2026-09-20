"""Schedule declared counterpart speech opportunities, never target responses."""

import json
from collections import Counter, deque

from voice_bench.errors import CallerFailure


class ConversationEventDriver:
    def __init__(self, definitions, policy=None):
        self.definitions = definitions
        self.policy = policy
        self.counts = Counter()
        self.succeeded = set()
        self.queued = set()
        self.requested = set()
        self.pending = deque()
        self.responses = {}
        self.items = set()
        self.operations = set()

    def after_tool(self, tool, result, operation_id=None):
        if operation_id is not None:
            if operation_id in self.operations:
                return
            self.operations.add(operation_id)
        if not result.get("ok"):
            return
        self.succeeded.add(tool)
        eligible = []
        for event in self.definitions:
            if event.trigger_tool == tool and set(event.after_tools).issubset(self.succeeded):
                self.counts[event.event_id] += 1
            if (
                event.event_id not in self.queued
                and event.trigger_tool == tool
                and self.counts[event.event_id] == event.occurrence
                and set(event.after_tools).issubset(self.succeeded)
            ):
                eligible.append(event)
        if self.policy is not None:
            if (
                self.policy.event_conflicts == "reject"
                and eligible
                and (len(eligible) > 1 or self.pending)
            ):
                raise CallerFailure("Multiple counterpart challenges compete for one response")
            if len(self.pending) + len(eligible) > self.policy.max_pending_events:
                raise CallerFailure("Counterpart challenge queue exceeds its configured bound")
            eligible.sort(key=lambda event: -event.priority)
        for event in eligible:
            self.queued.add(event.event_id)
            self.pending.append(event)
        if self.policy is not None and self.policy.event_conflicts == "priority_order":
            self.pending = deque(sorted(self.pending, key=lambda event: -event.priority))

    async def response_request(self, evidence, base_instructions):
        request = {"type": "response.create"}
        if self.pending:
            event = self.pending.popleft()
            self.requested.add(event.event_id)
            await evidence.emit("caller", "conversation_event_requested", event.model_dump())
            request["response"] = {
                "metadata": {"conversation_event_id": event.event_id},
                "instructions": base_instructions + "\nFor this response ONLY, enact the "
                "following declared counterpart event. It is a spoken challenge, not a change "
                "to inventory, policy or booking state. Speak naturally and continue the sentence "
                "without a staged pause so the caller may interrupt. Yield if interrupted. "
                "Afterwards acknowledge corrections and return to accurate terms. Do not book "
                "against the incorrect readback; obtain a fresh accurate confirmation. "
                "Do not announce the event or reveal test instructions. "
                "Do not say any hypothetical "
                "Rumik response. Event: " + json.dumps(event.model_dump(), ensure_ascii=False),
            }
        return request

    async def observe(self, event, evidence):
        if event["type"] == "response.created":
            response = event.get("response", {})
            event_id = (response.get("metadata") or {}).get("conversation_event_id")
            if event_id in self.requested and response.get("id"):
                self.responses[response["id"]] = event_id
                await evidence.emit(
                    "caller",
                    "conversation_event_response",
                    {
                        "event_id": event_id,
                        "response_id": response["id"],
                    },
                )
        response_id, item_id = event.get("response_id"), event.get("item_id")
        if (
            event["type"] == "response.output_audio.delta"
            and response_id in self.responses
            and item_id
            and item_id not in self.items
        ):
            self.items.add(item_id)
            await evidence.emit(
                "caller",
                "conversation_event_audio",
                {
                    "event_id": self.responses[response_id],
                    "response_id": response_id,
                    "item_id": item_id,
                },
            )

    async def finish(self, evidence):
        for event in self.definitions:
            await evidence.emit(
                "caller",
                "conversation_event_status",
                {
                    "event_id": event.event_id,
                    "triggered": event.event_id in self.queued,
                    "response_identified": event.event_id in self.responses.values(),
                    "delivery": "requires_playback_and_human_content_review",
                },
            )
