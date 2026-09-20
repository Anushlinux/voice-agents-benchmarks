# Rumik voice-agent benchmark

Benchmark a **hosted Rumik agent** through Chromium/LiveKit and real Plivo telephone calls. An OpenAI realtime audio customer listens to the channel and speaks back. Business tools run against isolated synthetic records. Grading checks saved actions and final state, then adds explicit model assessment and human review.

**Status: implementation available; live qualification pending.** The local fixture, PostgreSQL persistence, evidence storage, controller, provider adapters, grading, review, and batch commands are implemented. The provider-free suite includes real local Chromium audio processing and PostgreSQL transactions. This is not evidence that a real Rumik or Plivo call has succeeded. No provider conversations, provisioning, deployments, or paid evaluations have been run for this delivery.

```mermaid
flowchart LR
    P[Plan and limits] --> C[Controller]
    C --> O[OpenAI audio customer]
    O <-->|Audio| T[Chromium or Plivo]
    T <-->|Audio| R[Hosted Rumik agent]
    R -->|Authenticated tools| B[Isolated business records]
    B --> D[(PostgreSQL)]
    C --> E[Immutable evidence]
    T --> E
    B --> E
    E --> G[Rules, model judge, human review]
```

The customer receives only its brief and channel audio. Hidden business state, expected outcomes, and target transcripts are not customer inputs. Browser and phone attempts remain separate and retain their pairing in reports.

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
| `caller/` | OpenAI native-audio customer and playback truncation |
| `channels/browser/`, `browser/` | Chromium audio worklets and LiveKit bridge |
| `channels/phone/` | Plivo calls, authenticated streams, codec conversion and checkpoints |
| `target/rumik/` | Snapshots, registration, single-use token redemption and call evidence |
| `business/`, `storage.py` | Versioned workflows, transactional state and tool audits |
| `evidence/` | Local manifests, checksum verification and immutable object uploads |
| `evaluation/` | Deterministic checks, captured-audio transcription, judge and human review |
| `batches.py`, `runtime.py` | Paired plans, frozen settings, dispatch, recovery and accounting |
| `api/` | Health, authenticated business tools and carrier callbacks |

There is no management dashboard or HTTP call-start endpoint. `/healthz` reports process health; `/readyz` remains 503 while live qualification is unproven. Starting the standalone API does not connect providers or a database. The explicit live command composes the authenticated callback server and worker.

Read [implementation milestones](docs/IMPLEMENTATION.md), [architecture](docs/ARCHITECTURE.md), [evaluation](docs/EVALUATION.md), and [container instructions](infra/README.md). Dataset design and real workflows remain a separate workstream.
