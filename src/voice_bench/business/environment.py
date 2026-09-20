"""Registered, versioned workflow implementations; no arbitrary executable dataset code."""

from copy import deepcopy
from typing import Protocol

from voice_bench.evidence.local import canonical, digest
from voice_bench.storage import audit_entry


class Workflow(Protocol):
    name: str
    version: str
    tools: frozenset[str]

    def initialize(self, supplied: dict) -> dict: ...

    def execute(self, state: dict, tool: str, arguments: dict) -> dict: ...


class FixtureWorkflow:
    """Infrastructure fixture only: change a note on the fixture-owned record."""

    name = "harness_record"
    version = "1"
    tools = frozenset({"get_record", "set_note"})

    def initialize(self, supplied):
        if (
            not isinstance(supplied.get("records"), dict)
            or supplied.get("owned_record") not in supplied["records"]
            or any(not isinstance(r.get("note"), str) for r in supplied["records"].values())
        ):
            raise ValueError("Invalid harness record initial state")
        return deepcopy(supplied)

    def execute(self, state, tool, arguments):
        if tool not in self.tools:
            return {"ok": False, "error": "unknown_tool"}
        expected = {"record_id"} if tool == "get_record" else {"record_id", "note"}
        if set(arguments) != expected or not isinstance(arguments.get("record_id"), str):
            return {"ok": False, "error": "invalid_arguments"}
        record_id = arguments["record_id"]
        if record_id != state["owned_record"] or record_id not in state["records"]:
            return {"ok": False, "error": "forbidden_record"}
        if tool == "set_note":
            note = arguments["note"]
            if not isinstance(note, str) or len(note) > 500:
                return {"ok": False, "error": "invalid_note"}
            state["records"][record_id]["note"] = note
        return {"ok": True, "record": deepcopy(state["records"][record_id])}


class BusinessService:
    def __init__(self, store, workflows=None):
        self.store = store
        self.workflows = workflows if workflows is not None else WORKFLOWS

    def execute(self, run_id, tool, arguments, request_id):
        if not request_id:
            raise ValueError("An operation ID is required")
        with self.store.locked_run(run_id) as run:
            fingerprint = digest(canonical({"tool": tool, "arguments": arguments}))
            old = run["operations"].get(request_id)
            replay = False
            if old:
                replay = old["fingerprint"] == fingerprint
                result = old["result"] if replay else {"ok": False, "error": "operation_conflict"}
            elif not run["accept_tools"]:
                result = {"ok": False, "error": "attempt_closed"}
            else:
                workflow = self.workflows[(run["workflow"], run["workflow_version"])]
                state = deepcopy(run["state"])
                result = workflow.execute(state, tool, arguments)
                if result["ok"]:
                    run["state"] = state
                run["operations"][request_id] = {"fingerprint": fingerprint, "result": result}
            run["audit"].append(audit_entry(tool, arguments, request_id, result, replay))
            return deepcopy(result)

    def execute_call(self, call_id, tool, arguments, operation_id):
        return self.execute(self.store.resolve("rumik", call_id), tool, arguments, operation_id)

    def record_request(self, call_id, tool, raw_body):
        run_id = self.store.resolve("rumik", call_id)
        with self.store.locked_run(run_id) as run:
            requests = run.setdefault("incoming_requests", [])
            requests.append({"sequence": len(requests), "tool": tool, "body": raw_body})
        return run_id

    def seal(self, run_id):
        with self.store.locked_run(run_id) as run:
            run["accept_tools"] = False
            return {
                "state": deepcopy(run["state"]),
                "audit": deepcopy(run["audit"]),
                "incoming_requests": deepcopy(run.get("incoming_requests", [])),
                "carrier_callbacks": deepcopy(run.get("carrier_callbacks", {})),
            }


WORKFLOWS = {(FixtureWorkflow.name, FixtureWorkflow.version): FixtureWorkflow()}
