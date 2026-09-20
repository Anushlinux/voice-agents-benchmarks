import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from voice_bench.api.app import create_app
from voice_bench.business.environment import BusinessService
from voice_bench.storage import PostgresStore


def test_isolation_duplicates_rejected_actions_and_reopening(store, prepared):
    _, (first, second) = prepared
    business = BusinessService(store)
    args = {"record_id": "owned", "note": "changed"}
    with ThreadPoolExecutor(max_workers=4) as pool:
        replies = list(
            pool.map(lambda _: business.execute(first, "set_note", args, "op"), range(8))
        )
    assert all(r == replies[0] and r["ok"] for r in replies)
    assert sum(not x["replay"] for x in store.run(first)["audit"]) == 1
    rejected = business.execute(first, "set_note", {"record_id": "other", "note": "bad"}, "no")
    assert rejected["error"] == "forbidden_record"
    assert (
        business.execute(first, "set_note", {**args, "note": "conflict"}, "op")["error"]
        == "operation_conflict"
    )
    reopened = PostgresStore(store.dsn)
    assert reopened.run(first)["state"]["records"]["owned"]["note"] == "changed"
    assert reopened.run(second)["state"]["records"]["owned"]["note"] == "initial"
    assert reopened.run(first)["state"]["records"]["other"]["note"] == "unchanged"
    # A fresh interpreter has no in-process state from this test.
    subprocess.run(
        [
            sys.executable,
            "-c",
            "import os; from voice_bench.storage import PostgresStore; "
            "s=PostgresStore(os.environ['FIXTURE_DATABASE_URL']); "
            "state=s.run(os.environ['FIXTURE_RUN_ID'])['state']; "
            "assert state['records']['owned']['note']=='changed'",
        ],
        env={**os.environ, "FIXTURE_DATABASE_URL": store.dsn, "FIXTURE_RUN_ID": str(first)},
        check=True,
        timeout=10,
    )
    business.seal(first)
    assert business.execute(first, "set_note", args, "late")["error"] == "attempt_closed"


def test_transaction_rolls_back_both_state_and_audit(store, prepared):
    _, (run_id, _) = prepared
    before = store.run(run_id)
    with pytest.raises(RuntimeError), store.locked_run(run_id) as run:
        run["state"] = {"corrupt": True}
        run["audit"].append({"corrupt": True})
        raise RuntimeError("crash")
    assert store.run(run_id) == before


def test_authenticated_tools_reject_forged_run_ids(store, prepared):
    _, (first, second) = prepared
    store.bind("rumik", "known", first)
    client = TestClient(create_app(store, "test-secret"))
    body = {
        "call_id": "known",
        "operation_id": "op",
        "arguments": {"record_id": "owned", "note": "x"},
    }
    assert client.post("/tools/rumik/set_note", json=body).status_code == 401
    headers = {"Authorization": "Bearer test-secret"}
    assert (
        client.post(
            "/tools/rumik/set_note", json={**body, "run_id": str(second)}, headers=headers
        ).status_code
        == 422
    )
    assert (
        client.post(
            "/tools/rumik/set_note", json={**body, "call_id": "unknown"}, headers=headers
        ).status_code
        == 409
    )
    assert client.post("/tools/rumik/set_note", json=body, headers=headers).json()["ok"]
    assert len(store.run(first)["incoming_requests"]) == 2
    assert store.run(second)["state"]["records"]["owned"]["note"] == "initial"


def test_call_mapping_phone_reservation_and_lease_conflicts(store, prepared):
    _, (first, second) = prepared
    store.bind("rumik", "call", first)
    store.bind("rumik", "call", first)
    with pytest.raises(ValueError):
        store.bind("rumik", "call", second)
    with pytest.raises(ValueError):
        store.bind("rumik", "second-call", first)
    store.reserve_route("+100", "agent", first)
    store.update_run(first, phase="connecting")
    assert store.bind_phone("+100", "agent", "call") == first
    with pytest.raises(ValueError):
        store.bind_phone("+100", "agent", "another-call")
    assert store.claim(first, "worker-a")
    assert not store.claim(first, "worker-b")
    store.expire_lease(first, "worker-b")
    assert not store.claim(first, "worker-b")
    store.expire_lease(first, "worker-a")
    assert store.claim(first, "worker-b")


def test_uncertain_attempt_cannot_retry(store, prepared):
    plans, (first, _) = prepared
    original = store.run(first)
    with pytest.raises(ValueError, match="unresolved"):
        store.create_run(plans[0].batch_id, uuid4(), original)
    store.update_run(first, termination_confirmed=True)
    second = uuid4()
    store.create_run(plans[0].batch_id, second, original)
    assert store.run(second)["attempt"] == 2
