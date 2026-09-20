# Rumik personal-assistant benchmark

Benchmark a **hosted Rumik assistant acting on a user's behalf**. Rumik receives the user's assignment and speaks with a simulated restaurant employee, delivery agent, driver, or support representative. OpenAI Realtime plays that other person. Only Rumik is the target being evaluated; this is not a Rumik-versus-OpenAI comparison.

This follows the Rumik team direction relayed by the user on 2026-09-20. It supersedes the earlier assumption that Rumik represents a business answering an OpenAI customer's request. Indian settings, Hinglish, booking, cancellation, negotiation and delivery coordination guide the intended dataset; domain workflows and coverage remain a separate workstream.

**Status: role-separated single-call implementation; live qualification pending.** The harness delivers a private user task through its authenticated before-call callback, gives the counterpart separately scoped business tools, records audio/actions, and grades final state. No live provider success is claimed. The only supplied workflow is an infrastructure fixture.

```mermaid
flowchart LR
    U[User request and permissions] --> R[Hosted Rumik assistant]
    R <-->|Browser or phone audio| S[OpenAI simulated other person]
    S -->|Role-permitted tools| B[Isolated business records]
    R -->|Only user-authorized tools| B
    R --> E[Recordings and action evidence]
    S --> E
    B --> E
    E --> G[Rules, optional model judge, human review]
```

Rumik receives only the user's assignment and information it is entitled to access. The counterpart receives its own role, facts, received audio, and permitted tool results. Neither receives grading answers. For a restaurant call, the restaurant side owns reservation mutations; Rumik cannot directly edit the restaurant's records unless a scenario explicitly represents a legitimate user-facing tool.

The current browser and phone adapters connect a **single conversation**. The phone adapter dials into Rumik, so it measures conversation behavior only. Rumik choosing and dialing a destination, tasks spanning several calls and user approvals, and operating District/Uber apps are not implemented. Cases requesting outbound initiation or multiple calls are rejected before dispatch; they are never silently reduced to one inbound call. A longer duration limit permits a longer conversation, not a multi-call task.

Read [the role and scope contract](docs/SCOPE.md) and [case migration instructions](docs/RUNNING.md#supply-workflows-and-cases) before supplying new data.

## Start without providers

Use Python 3.12, uv, and Node 22 or newer. Run from the repository root:

```sh
uv sync --locked
npm --prefix browser ci --ignore-scripts
npm --prefix browser run build
uv run --locked voice-bench status
uv run --locked voice-bench plan --config configs/local.toml
```

These status and planning commands make no provider calls and create no evidence. The checked-in configurations have zero funded budgets. They cannot execute live calls. Dependencies are locked in `uv.lock` and `browser/package-lock.json`; installation accesses package registries.

To run the first deliverable, start a local PostgreSQL database:

```sh
docker compose --profile database up -d postgres
export DATABASE_URL=postgresql://voice_bench:local_only@127.0.0.1:5432/voice_bench
uv run --locked voice-bench fixture --config configs/local.toml
```

The fixture creates two isolated attempts, changes one permitted field, rejects a forbidden change, replays an operation safely, reopens persisted state, and seals inspectable evidence. Its output is **harness validation**, never a benchmark result or dataset coverage claim. The returned artifact directory contains initial/final state, tool audits, events, and checksums. Database integration tests also verify persistence in a fresh Python process.

## Commands and boundaries

- `status`, `plan`, `batch plan`, imports, and health routes are provider-free.
- `fixture`, `db-init`, and reports use PostgreSQL where needed; they make no provider calls.
- `inspect`, ordinary `evaluate`, and review import/export use saved local evidence.
- `run --live` and `batch run --live` explicitly start funded provider activity.
- `evaluate --with-model` explicitly enables paid transcription and text judgment.
- `batch recover --remote` polls providers and may hang up abandoned calls. It never starts a conversation.
- `upload` explicitly writes a sealed attempt and versioned results to configured S3-compatible storage.

See [Running and qualifying the benchmark](docs/RUNNING.md) for full commands, execution-case contracts, callback configuration, and recovery.

## Development checks

```sh
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked pytest
```

Database and Chromium checks are opt-in locally. For the complete provider-free suite:

```sh
uv run --locked playwright install chromium
export TEST_DATABASE_URL=postgresql://voice_bench:local_only@127.0.0.1:5432/voice_bench
RUN_BROWSER_TESTS=1 uv run --locked pytest
```

Each database test creates and removes its own schema. Use a dedicated development database. Without these settings, pytest explicitly skips the database/browser checks. CI supplies PostgreSQL, installs Chromium, and enables both. Python tests reject connections to non-loopback addresses and remove provider credentials.

## Repository map

| Package | Responsibility |
| --- | --- |
| `controller/` | Attempt lifecycle, reservations, cleanup and leases |
| `caller/` | OpenAI counterpart audio, permitted business tools and playback truncation |
| `channels/browser/`, `browser/` | Chromium audio worklets and LiveKit bridge |
| `channels/phone/` | Plivo calls, authenticated streams, codec conversion and checkpoints |
| `target/rumik/` | Hosted personal-assistant snapshots, call setup and evidence |
| `business/`, `storage.py` | Versioned workflows, transactional state and tool audits |
| `evidence/` | Local manifests, checksum verification and immutable object uploads |
| `evaluation/` | Deterministic checks, captured-audio transcription, judge and human review |
| `batches.py`, `runtime.py` | Paired plans, frozen settings, dispatch, recovery and accounting |
| `api/` | Health, authenticated business tools and carrier callbacks |

There is no management dashboard or HTTP call-start endpoint. `/healthz` reports process health; `/readyz` remains 503 while live qualification is unproven. Starting the standalone API does not connect providers or a database. The explicit live command composes the authenticated callback server and worker.

Read [implementation milestones](docs/IMPLEMENTATION.md), [architecture](docs/ARCHITECTURE.md), [evaluation](docs/EVALUATION.md), and [container instructions](infra/README.md). Dataset design and real workflows remain a separate workstream.
