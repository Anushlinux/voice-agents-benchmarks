import json
from pathlib import Path
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from voice_bench.api.app import create_app
from voice_bench.batches import make_plan
from voice_bench.business.environment import BusinessService
from voice_bench.contracts import ExecutionCase
from voice_bench.controller.runner import Controller
from voice_bench.evaluation.scoring import deterministic, save_evaluation
from voice_bench.evidence.local import LocalEvidence
from voice_bench.fixture import fixture_case
from voice_bench.models import CounterpartBrief, UserTask
from voice_bench.runtime import validate_live
from voice_bench.settings import load_config


def test_legacy_customer_input_cannot_silently_reverse_roles():
    data = fixture_case().model_dump(mode="json")
    data["caller"] = data.pop("counterpart")
    data.pop("user_task")
    data.pop("schema_version")
    with pytest.raises(ValidationError):
        ExecutionCase.model_validate(data)


@pytest.mark.parametrize("field", ["user_task", "criteria", "initial_state", "target_transcript"])
def test_counterpart_brief_rejects_private_inputs(field):
    data = fixture_case().counterpart.model_dump()
    data[field] = {"secret": "must not reach the simulated person"}
    with pytest.raises(ValidationError):
        CounterpartBrief.model_validate(data)


def test_user_task_rejects_counterpart_private_state():
    data = fixture_case().user_task.model_dump()
    data["counterpart"] = {"minimum_deposit": 700}
    with pytest.raises(ValidationError):
        UserTask.model_validate(data)


@pytest.mark.parametrize(
    "updates",
    [
        {"task_scope": "multi_call"},
        {"call_initiation": "rumik_outbound"},
    ],
)
@pytest.mark.asyncio
async def test_unsupported_scope_can_be_planned_but_cannot_dispatch(updates):
    case = fixture_case().model_copy(update=updates)
    plan = make_plan([case], ["phone"])[0]
    assert plan.task_scope == case.task_scope
    assert plan.call_initiation == case.call_initiation
    # No store/channel is supplied: rejecting unsupported scope must precede any work.
    config = load_config(Path("configs/local.toml"))
    with pytest.raises(ValueError, match="not implemented"):
        await Controller(None, config, None, None).execute(plan, case, "test")
    with pytest.raises(ValueError, match="not implemented"):
        validate_live(config, [case])


def serve(store, run_id, call_id="known"):
    store.bind("rumik", call_id, run_id)
    return BusinessService(store).serve_user_task(call_id, "test-agent")


def test_before_call_delivers_only_user_task_to_correlated_agent(store, prepared):
    _, (first, second) = prepared
    store.bind("rumik", "known", first)
    body = {"call_id": "known", "agent_id": "test-agent"}
    headers = {"Authorization": "Bearer test-secret"}
    with TestClient(create_app(store, "test-secret")) as client:
        assert client.post("/tools/rumik/before-call", json=body).status_code == 401
        wrong = client.post(
            "/tools/rumik/before-call", json={**body, "agent_id": "wrong"}, headers=headers
        )
        assert wrong.status_code == 409
        assert not store.run(first).get("user_task_served")
        unknown = client.post(
            "/tools/rumik/before-call", json={**body, "call_id": "unknown"}, headers=headers
        )
        assert unknown.status_code == 409
        response = client.post("/tools/rumik/before-call", json=body, headers=headers)
        assert response.json()["benchmark_ready"] is True
        assert response.json()["user_task"] == fixture_case().user_task.model_dump(mode="json")
        assert json.loads(response.json()["user_task_json"]) == response.json()["user_task"]
        assert set(response.json()) == {"benchmark_ready", "user_task", "user_task_json"}
        assert not store.run(second).get("user_task_served")
        BusinessService(store).seal(first)
        assert (
            client.post("/tools/rumik/before-call", json=body, headers=headers).status_code == 409
        )


def test_business_mutations_follow_role_permissions_and_attempt_isolation(store, prepared):
    _, (first, second) = prepared
    service = BusinessService(store)
    args = {"record_id": "owned", "note": "updated"}
    assert (
        service.execute(first, "set_note", args, "before-task", actor="counterpart")["error"]
        == "forbidden_tool"
    )
    serve(store, first)
    definitions = service.counterpart_tools(first)
    assert {d["name"] for d in definitions} == {"business_get_record", "business_set_note"}
    assert "initial" not in json.dumps(definitions)
    assert service.execute_call("known", "set_note", args, "same-id")["error"] == "forbidden_tool"
    assert service.execute(first, "set_note", args, "same-id", actor="counterpart")["ok"]
    assert service.execute(first, "set_note", args, "same-id", actor="counterpart")["ok"]
    run = store.run(first)
    assert run["audit"][-1]["replay"]
    assert run["state"]["records"]["owned"]["note"] == "updated"
    assert store.run(second)["state"]["records"]["owned"]["note"] == "initial"
    assert [a["actor"] for a in run["audit"][-3:]] == ["target", "counterpart", "counterpart"]
    service.seal(first)
    assert (
        service.execute(first, "set_note", args, "late", actor="counterpart")["error"]
        == "attempt_closed"
    )


def test_user_authorized_target_tool_is_available_only_when_granted(store, prepared):
    _, (first, _) = prepared
    serve(store, first)
    with store.locked_run(first) as run:
        run["tool_access"]["target"] = ["get_record"]
    service = BusinessService(store)
    assert service.execute_call("known", "get_record", {"record_id": "owned"}, "read")["ok"]
    assert (
        service.execute_call("known", "set_note", {"record_id": "owned", "note": "x"}, "write")[
            "error"
        ]
        == "forbidden_tool"
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "actor,validity,outcome",
    [
        ("target", "valid", "failed"),
        ("counterpart", "invalid", "unresolved"),
    ],
)
async def test_grading_attributes_forbidden_actions_to_the_correct_party(
    tmp_path, actor, validity, outcome
):
    case = fixture_case()
    evidence = LocalEvidence(tmp_path, uuid4(), uuid4())
    await evidence.json("config/case.json", case.model_dump(mode="json"))
    await evidence.json("business/final.json", {"records": {"owned": {"note": "updated"}}})
    await evidence.json(
        "business/audit.json",
        [
            {
                "actor": actor,
                "tool": "set_note",
                "arguments": {},
                "operation_id": "bad",
                "result": {"ok": False, "error": "forbidden_tool"},
            }
        ],
    )
    await evidence.finalize(evidence.run_id)
    metrics = deterministic(evidence.directory)
    path = save_evaluation(evidence.directory, "roles-v2", metrics, validity="valid")
    result = json.loads(path.read_text())
    assert result["validity"] == validity and result["outcome"] == outcome


@pytest.mark.asyncio
async def test_correct_state_without_task_delivery_cannot_pass(tmp_path):
    case = fixture_case().model_copy(update={"harness_fixture": False})
    evidence = LocalEvidence(tmp_path, uuid4(), uuid4())
    await evidence.json("config/case.json", case.model_dump(mode="json"))
    await evidence.json("business/final.json", {"records": {"owned": {"note": "updated"}}})
    await evidence.json("business/audit.json", [])
    await evidence.finalize(evidence.run_id)
    path = save_evaluation(
        evidence.directory, "v2", deterministic(evidence.directory), validity="valid"
    )
    assert json.loads(path.read_text())["outcome"] == "unresolved"


def test_callback_diagnostics_capture_rejections_without_secrets(store, prepared, tmp_path):
    log = tmp_path / "callback-requests.jsonl"
    app = create_app(store, "private-secret", callback_log=log)
    with TestClient(app) as client:
        assert (
            client.post(
                "/tools/rumik/before-call", json={"call_id": "x", "agent_id": "x"}
            ).status_code
            == 401
        )
        assert (
            client.post("/tools/rumik/before-call", json={"private": "private-task"}).status_code
            == 422
        )
        _, (run_id, _) = prepared
        store.bind("rumik", "known", run_id)
        assert (
            client.post(
                "/tools/rumik/before-call",
                json={"call_id": "known", "agent_id": "test-agent"},
                headers={"Authorization": "Bearer private-secret"},
            ).status_code
            == 200
        )
    text = log.read_text()
    entries = [json.loads(line) for line in text.splitlines()]
    assert [entry["status"] for entry in entries if entry["event"] == "finished"] == [401, 422, 200]
    assert len([entry for entry in entries if entry["event"] == "arrived"]) == 3
    assert "private-secret" not in text and "private-task" not in text


def test_task_delivery_accepts_only_frozen_aliases_of_the_expected_agent(store, prepared):
    _, (first, second) = prepared
    store.bind("rumik", "known-alias", first)
    with store.locked_run(first) as run:
        run["target_agent_aliases"] = ["ua_verified_handle"]
    service = BusinessService(store)
    with pytest.raises(ValueError):
        service.serve_user_task("known-alias", "another-agent")
    assert not store.run(first).get("user_task_served")
    service.serve_user_task("known-alias", "ua_verified_handle")
    assert store.run(first)["user_task_delivery"]["agent_id"] == "ua_verified_handle"
    assert not store.run(second).get("user_task_served")
    service.seal(first)
    with pytest.raises(ValueError):
        service.serve_user_task("known-alias", "ua_verified_handle")


def test_target_report_requires_scoped_identity_and_preserves_original_output(store, prepared):
    _, (first, second) = prepared
    store.bind("rumik", "report-call", first)
    headers = {"Authorization": "Bearer test-secret"}
    body = {
        "call_id": "report-call",
        "agent_id": "test-agent",
        "report": "Booking could not be completed.",
    }
    with TestClient(create_app(store, "test-secret")) as client:
        assert client.post("/tools/rumik/submit-user-report", json=body).status_code == 401
        assert (
            client.post("/tools/rumik/submit-user-report", json=body, headers=headers).status_code
            == 409
        )
        with store.locked_run(first) as run:
            run["tool_access"]["target"] = ["submit_user_report"]
        BusinessService(store).serve_user_task("report-call", "test-agent")
        assert (
            client.post(
                "/tools/rumik/submit-user-report",
                json={**body, "agent_id": "other"},
                headers=headers,
            ).status_code
            == 409
        )
        assert (
            client.post("/tools/rumik/submit-user-report", json=body, headers=headers).status_code
            == 200
        )
        assert (
            client.post("/tools/rumik/submit-user-report", json=body, headers=headers).status_code
            == 200
        )
        assert (
            client.post(
                "/tools/rumik/submit-user-report",
                json={**body, "report": "Changed outcome"},
                headers=headers,
            ).status_code
            == 409
        )
        saved = store.run(first)
        assert saved["target_user_report"]["text"] == body["report"]
        assert saved["target_user_report"]["source"] == "authenticated_rumik_tool"
        assert not store.run(second).get("target_user_report")
        assert saved["state"] == fixture_case().initial_state
        BusinessService(store).seal(first)
        assert (
            client.post("/tools/rumik/submit-user-report", json=body, headers=headers).status_code
            == 409
        )


def test_report_completion_needs_explicit_target_permission():
    data = fixture_case().model_dump()
    data["completion"] = "target_report_then_hangup"
    with pytest.raises(ValidationError):
        ExecutionCase.model_validate(data)


def test_report_correction_preserves_history_and_cannot_change_closed_or_other_call(
    store, prepared
):
    _, (first, second) = prepared
    store.bind("rumik", "revisable-report", first)
    service = BusinessService(store)
    with store.locked_run(first) as run:
        run["tool_access"]["target"] = ["submit_user_report"]
        run["report_policy"] = "revisable_until_close"
    service.serve_user_task("revisable-report", "test-agent")
    # Reproduce the two Sana submissions: a premature report followed by correction.
    original = "No booking: the only package costs INR 10,800, above the INR 9,000 limit."
    corrected = "No booking: packages cost INR 10,800 and INR 9,600, both above INR 9,000."
    first_result = service.submit_user_report("revisable-report", "test-agent", original)
    assert first_result["report_revision"] == 1
    assert not service.submit_user_report("revisable-report", "other-agent", corrected)["ok"]
    revised = service.submit_user_report("revisable-report", "test-agent", corrected)
    assert revised["report_saved"] and revised["report_revision"] == 2
    assert service.submit_user_report("revisable-report", "test-agent", corrected) == revised
    saved = store.run(first)
    assert [r["text"] for r in saved["target_report_history"]] == [original, corrected]
    assert saved["target_report_history"][1]["supersedes_revision"] == 1
    assert saved["target_user_report"]["text"] == corrected
    assert len(saved["target_report_requests"]) == 4
    assert not store.run(second).get("target_user_report")
    service.seal(first)
    assert not service.submit_user_report("revisable-report", "test-agent", original)["ok"]
    assert store.run(first)["target_user_report"] == saved["target_user_report"]
