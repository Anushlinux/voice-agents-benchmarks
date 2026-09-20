import os
import socket
from uuid import uuid4

import pytest


@pytest.fixture(autouse=True)
def no_provider_network(monkeypatch):
    original = socket.socket.connect

    def connect(sock, address):
        if isinstance(address, tuple) and address[0] not in {"127.0.0.1", "localhost", "::1"}:
            raise AssertionError("Tests must not connect to provider networks")
        return original(sock, address)

    monkeypatch.setattr(socket.socket, "connect", connect)
    for key in ("OPENAI_API_KEY", "RUMIK_API_KEY", "PLIVO_AUTH_ID", "PLIVO_AUTH_TOKEN"):
        monkeypatch.delenv(key, raising=False)


@pytest.fixture
def store():
    dsn = os.environ.get("TEST_DATABASE_URL")
    if not dsn:
        pytest.skip("Set TEST_DATABASE_URL to an isolated PostgreSQL database")
    import psycopg
    from psycopg.conninfo import make_conninfo

    from voice_bench.storage import PostgresStore

    schema = "test_" + uuid4().hex
    with psycopg.connect(dsn) as conn:
        conn.execute(f'CREATE SCHEMA "{schema}"')
    scoped = PostgresStore(make_conninfo(dsn, options=f"-c search_path={schema}"))
    scoped.migrate()
    yield scoped
    with psycopg.connect(dsn) as conn:
        conn.execute(f'DROP SCHEMA "{schema}" CASCADE')


@pytest.fixture
def prepared(store):
    from voice_bench.batches import make_plan
    from voice_bench.fixture import fixture_case

    case = fixture_case()
    plans = make_plan([case], ["browser"], repetitions=2)
    store.create_batch(
        plans[0].batch_id,
        {
            "plans": [p.model_dump(mode="json") for p in plans],
            "limits": {"max_attempts_per_case": 2},
        },
    )
    ids = []
    for plan in plans:
        run_id = uuid4()
        store.create_run(
            plan.batch_id,
            run_id,
            {
                "plan_id": str(plan.plan_id),
                "workflow": case.workflow,
                "workflow_version": case.workflow_version,
                "state": case.initial_state,
                "context": {
                    "case_id": case.case_id,
                    "channel": "browser",
                    "repetition": plan.repetition,
                },
            },
        )
        ids.append(run_id)
    return plans, ids
