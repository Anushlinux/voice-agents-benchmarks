# Rumik personal-assistant benchmark

**Master benchmark report (22 September 2026):** [Muga vs Mulberry 1.5 vs Mulberry 1.6 on all ten cases, with every recording, transcript, Rumik transcript, private report and evaluation](reports/benchmark-master-20260922/README.md).

**Earlier 10-case Muga results (21 September 2026):** [Read the complete plain-English report, evaluations, conversation audio and transcripts](reports/full-dataset-preflight-20260921/simple-report/README.md). All ten cases ran; the saved overall grades are 0 passed, 2 failed and 8 unresolved. The report explains the observed failures and grading limits.

**Latest diagnostic qualification:** the browser now records audio transport and
connection observations, and full reports separate observed task completion from
failure attribution. One unchanged Priya call stalled after the greeting despite
complete employee playback and continuing received packets. All evaluations
completed; conversation reliability is **not qualified**. The investigation stopped
after one call, with INR 155 reserved from the INR 465 ceiling. See
`reports/conversation-foundation-20260921/README.md` and the
[repair guide](docs/CONVERSATION_REPAIR.md). Older results below remain historical.

**Latest Aditi Shah rerun:** the reservation succeeded and the charge/cutoff defects did not recur, but the overall test failed because the reported reference lost a letter. Shared fixes and the separate, locally tested pronunciation follow-up are documented in [the repair guide](docs/CONVERSATION_REPAIR.md). Local evidence: `reports/harness-repair-rerun-20260921/README.md`.

The latest functional test deployed hosted version 5 and ran the Aditi Shah case
once with a 15-second silence limit. Rumik responded and submitted a report, but no
booking was made. The run exposed an overly broad zero-spending instruction and a
post-report timer that cut off active speech. Both judges completed. Local corrections
passed 75 checks but have not been rerun live. See
`reports/functional-run-20260921/README.md` for the recording and exact outcome.

**Current status: caller-role and full-evaluation repairs are implemented, but the
single September 21 qualification call did not pass conversation acceptance.**
Both Luna and Jev completed. Rumik stated the customer request, then stalled;
the employee also attempted a premature booking. No booking or private report
was produced. The local diagnostic report is
`reports/repair-implementation-20260921T103008Z/README.md`. Read the
[repair and verification guide](docs/CONVERSATION_REPAIR.md). The local audit is in
`reports/conversation-root-cause-audit-20260921/README.md`; repair artifacts and
validation are in `reports/restaurant-repair-20260921/`. Historical grades are
preserved and should be read with the audit's attribution and evidence limits.

The follow-up stall diagnosis and local fixes are in
`reports/dietary-stall-debug-20260921/README.md`. The optional dietary-field contract
and revised side-question guidance have passed local tests; no second call or
deployment has been made.

The full evaluation mode is `batch run --live --with-evaluation --jev-rubric
configs/restaurant-jev-rubric.json`, alongside the required `--config` and `--cases`.
It reserves all stages before calling, then saves rules, Luna, independent Jev,
recordings and the final report together. Human listening status stays separate.

Benchmark a **hosted Rumik assistant acting on a user's behalf**. Rumik receives the user's assignment and speaks with a simulated restaurant employee, delivery agent, driver, or support representative. OpenAI Realtime plays that other person. Only Rumik is the target being evaluated; this is not a Rumik-versus-OpenAI comparison.

This follows the Rumik team direction relayed by the user on 2026-09-20. It supersedes the earlier assumption that Rumik represents a business answering an OpenAI customer's request. Indian settings, spoken Hinglish, booking, cancellation, negotiation and delivery coordination guide the intended dataset; domain workflows and coverage remain a separate workstream.

Dataset instructions may be written in English. Explicitly instruct Rumik to speak Hinglish during the call; do not translate the dataset into Hinglish merely to set the speaking language.

The new restaurant workflow separates availability lookup, a current offer and
an evidenced booking. Ten natural cases are prepared offline, including useful
no-booking outcomes. Old tool-count speech challenges are retired from live
execution because their mistakes were not grounded in previously heard terms.
The old baseline, challenge definitions and evidence remain available for audit.
Telephone qualification and the repaired hosted behavior remain unproven.

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

Dataset-independent additions include [Rumik task setup and Plivo SIP checks](docs/RUMIK_PLIVO_SETUP.md)
and [Jev shadow evaluation](docs/JEV.md). Jev compares saved text evidence without
changing benchmark verdicts. The Rumik outbound client operation is implemented,
but a complete outbound executor, multi-call tasks and native user-report delivery
remain unsupported. No new live qualification is claimed.

[Reusable benchmark design](docs/BENCHMARK_DESIGN.md) adds opt-in counterpart
behavior profiles, bounded scenario policies and explicit restaurant metric rubrics.
`voice-bench design prepare` produces a new case version offline while preserving
the source task and business state. Saved results retain their semantics. Event-bearing cases are now audit-only.

## Local dataset review

Start at `datasets/README.md` for the reorganized local dataset. Two authored
files and two generated files hold the existing four restaurant cases; source
attribution is separate, and original packages and preparation outputs are
preserved in an archive. `datasets/REVIEW.md` explains the limits of these cases.
Eight new Indian personal-assistant task designs are documented separately as
proposals, with their missing workflow support stated explicitly. They are not
executable cases or additional live coverage.

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
