"""PostgreSQL persistence. Construction and imports never open connections."""

from contextlib import contextmanager
from copy import deepcopy
from datetime import UTC, datetime
from uuid import UUID

from voice_bench.evidence.local import canonical, digest
from voice_bench.numbers import endpoint_digits

SCHEMA = """
CREATE TABLE IF NOT EXISTS vb_batches (
 id uuid PRIMARY KEY, data jsonb NOT NULL
);
CREATE TABLE IF NOT EXISTS vb_runs (
 id uuid PRIMARY KEY, batch_id uuid NOT NULL REFERENCES vb_batches(id),
 data jsonb NOT NULL, lease_owner text, lease_until timestamptz
);
CREATE TABLE IF NOT EXISTS vb_bindings (
 provider text NOT NULL, call_id text NOT NULL,
 run_id uuid NOT NULL REFERENCES vb_runs(id), PRIMARY KEY(provider, call_id)
);
CREATE UNIQUE INDEX IF NOT EXISTS vb_one_call_per_provider_attempt
 ON vb_bindings(provider,run_id);
CREATE TABLE IF NOT EXISTS vb_routes (
 caller text NOT NULL, agent text NOT NULL, run_id uuid NOT NULL REFERENCES vb_runs(id),
 bound_call text, PRIMARY KEY(caller, agent), UNIQUE(run_id)
);
CREATE TABLE IF NOT EXISTS vb_callbacks (
 provider text NOT NULL, event_id text NOT NULL, fingerprint text NOT NULL,
 PRIMARY KEY(provider, event_id)
);
"""


class PostgresStore:
    def __init__(self, dsn: str):
        self.dsn = dsn

    def connect(self):
        import psycopg
        from psycopg.rows import dict_row

        return psycopg.connect(self.dsn, row_factory=dict_row, connect_timeout=5)

    @staticmethod
    def json(value):
        import json

        from psycopg.types.json import Jsonb

        return Jsonb(json.loads(canonical(value)))

    def migrate(self):
        with self.connect() as conn:
            if conn.info.encoding != "utf-8":
                raise ValueError("Benchmark database must use UTF8 encoding")
            conn.execute("SELECT pg_advisory_xact_lock(81203499)")
            conn.execute(SCHEMA)

    def create_batch(self, batch_id, data):
        with self.connect() as conn:
            conn.execute("INSERT INTO vb_batches VALUES (%s,%s)", (batch_id, self.json(data)))

    def batch(self, batch_id):
        with self.connect() as conn:
            row = conn.execute("SELECT data FROM vb_batches WHERE id=%s", (batch_id,)).fetchone()
            if row is None:
                raise KeyError("Unknown batch")
            return row["data"]

    @contextmanager
    def locked_batch(self, batch_id):
        with self.connect() as conn:
            row = conn.execute(
                "SELECT data FROM vb_batches WHERE id=%s FOR UPDATE", (batch_id,)
            ).fetchone()
            if row is None:
                raise KeyError("Unknown batch")
            data = row["data"]
            yield conn, data
            conn.execute("UPDATE vb_batches SET data=%s WHERE id=%s", (self.json(data), batch_id))

    def create_run(self, batch_id, run_id, data):
        with self.locked_batch(batch_id) as (conn, batch):
            plan_id = data["plan_id"]
            if plan_id not in {p["plan_id"] for p in batch["plans"]}:
                raise ValueError("Attempt does not belong to the saved batch plan")
            rows = conn.execute(
                "SELECT data FROM vb_runs WHERE batch_id=%s", (batch_id,)
            ).fetchall()
            attempts = [r["data"] for r in rows if r["data"]["plan_id"] == plan_id]
            if any(not r.get("termination_confirmed", False) for r in attempts):
                raise ValueError("Previous attempt has unresolved termination")
            if len(attempts) >= batch["limits"]["max_attempts_per_case"]:
                raise ValueError("Attempt limit reached")
            data = {
                **deepcopy(data),
                "attempt": len(attempts) + 1,
                "phase": "prepared",
                "audit": [],
                "operations": {},
                "accept_tools": True,
                "connected": False,
                "termination_confirmed": False,
            }
            conn.execute(
                "INSERT INTO vb_runs(id,batch_id,data) VALUES (%s,%s,%s)",
                (run_id, batch_id, self.json(data)),
            )

    def run(self, run_id):
        with self.connect() as conn:
            row = conn.execute("SELECT data FROM vb_runs WHERE id=%s", (run_id,)).fetchone()
            if row is None:
                raise KeyError("Unknown run")
            return row["data"]

    @contextmanager
    def locked_run(self, run_id):
        with self.connect() as conn:
            row = conn.execute(
                "SELECT data FROM vb_runs WHERE id=%s FOR UPDATE", (run_id,)
            ).fetchone()
            if row is None:
                raise KeyError("Unknown run")
            data = row["data"]
            yield data
            conn.execute("UPDATE vb_runs SET data=%s WHERE id=%s", (self.json(data), run_id))

    def update_run(self, run_id, **updates):
        with self.locked_run(run_id) as run:
            run.update(updates)

    def runs(self, batch_id):
        with self.connect() as conn:
            return [
                {"run_id": str(r["id"]), **r["data"]}
                for r in conn.execute(
                    "SELECT id,data FROM vb_runs WHERE batch_id=%s ORDER BY id", (batch_id,)
                )
            ]

    def bind(self, provider, call_id, run_id):
        with self.connect() as conn:
            conn.execute(
                "INSERT INTO vb_bindings VALUES (%s,%s,%s) ON CONFLICT DO NOTHING",
                (provider, call_id, run_id),
            )
            row = conn.execute(
                "SELECT run_id FROM vb_bindings WHERE provider=%s AND call_id=%s",
                (provider, call_id),
            ).fetchone()
            if row is None or row["run_id"] != UUID(str(run_id)):
                raise ValueError("Provider call is already bound to another run")

    def resolve(self, provider, call_id):
        with self.connect() as conn:
            row = conn.execute(
                "SELECT run_id FROM vb_bindings WHERE provider=%s AND call_id=%s",
                (provider, call_id),
            ).fetchone()
            if row is None:
                raise KeyError("Uncorrelated provider call")
            return row["run_id"]

    def bindings(self, run_id):
        with self.connect() as conn:
            return list(
                conn.execute("SELECT provider,call_id FROM vb_bindings WHERE run_id=%s", (run_id,))
            )

    def reserve_route(self, caller, agent, run_id):
        with self.connect() as conn:
            conn.execute(
                "INSERT INTO vb_routes(caller,agent,run_id) VALUES (%s,%s,%s)",
                (endpoint_digits(caller) or caller, agent, run_id),
            )

    def bind_phone(self, caller, agent, call_id):
        caller = endpoint_digits(caller) or caller
        with self.connect() as conn:
            row = conn.execute(
                "SELECT * FROM vb_routes WHERE caller=%s AND agent=%s FOR UPDATE", (caller, agent)
            ).fetchone()
            if row is None or row["bound_call"] not in (None, call_id):
                raise ValueError("Missing, stale, or conflicting phone reservation")
            run = conn.execute(
                "SELECT data FROM vb_runs WHERE id=%s FOR UPDATE", (row["run_id"],)
            ).fetchone()["data"]
            if run["phase"] not in {"connecting", "in_conversation"} or not run["accept_tools"]:
                raise ValueError("Phone reservation is no longer accepting calls")
            conn.execute(
                "INSERT INTO vb_bindings VALUES ('rumik',%s,%s) ON CONFLICT DO NOTHING",
                (call_id, row["run_id"]),
            )
            bound = conn.execute(
                "SELECT run_id FROM vb_bindings WHERE provider='rumik' AND call_id=%s", (call_id,)
            ).fetchone()
            if bound is None or bound["run_id"] != row["run_id"]:
                raise ValueError("Call ID conflict")
            conn.execute(
                "UPDATE vb_routes SET bound_call=%s WHERE caller=%s AND agent=%s",
                (call_id, caller, agent),
            )
            return row["run_id"]

    def release_route(self, run_id):
        with self.connect() as conn:
            conn.execute("DELETE FROM vb_routes WHERE run_id=%s", (run_id,))

    def claim(self, run_id, owner, seconds=30):
        with self.connect() as conn:
            row = conn.execute(
                "UPDATE vb_runs SET lease_owner=%s, lease_until=now()+(%s * interval '1 second') "
                "WHERE id=%s AND (lease_until IS NULL OR lease_until<now() OR lease_owner=%s) "
                "RETURNING id",
                (owner, seconds, run_id, owner),
            ).fetchone()
            return row is not None

    def expire_lease(self, run_id, owner):
        with self.connect() as conn:
            conn.execute(
                "UPDATE vb_runs SET lease_until=NULL,lease_owner=NULL "
                "WHERE id=%s AND lease_owner=%s",
                (run_id, owner),
            )

    def callback_once(self, provider, event_id, payload):
        fingerprint = digest(canonical(payload))
        with self.connect() as conn:
            row = conn.execute(
                "INSERT INTO vb_callbacks VALUES (%s,%s,%s) "
                "ON CONFLICT DO NOTHING RETURNING event_id",
                (provider, event_id, fingerprint),
            ).fetchone()
            if row:
                return True
            saved = conn.execute(
                "SELECT fingerprint FROM vb_callbacks WHERE provider=%s AND event_id=%s",
                (provider, event_id),
            ).fetchone()
            if saved["fingerprint"] != fingerprint:
                raise ValueError("Conflicting duplicate callback")
            return False


def audit_entry(tool, arguments, operation_id, result, replay=False):
    return {
        "tool": tool,
        "arguments": deepcopy(arguments),
        "operation_id": operation_id,
        "result": deepcopy(result),
        "replay": replay,
        "at": datetime.now(UTC).isoformat(),
    }
