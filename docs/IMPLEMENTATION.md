# Implementation milestones and proof

## Personal-assistant role update

The direction relayed by the user on 2026-09-20 supersedes the original customer-to-business assumption. Current code supplies schema-2 user/counterpart briefs, authenticated user-task delivery, per-role business tools, counterpart audio/tool handling, actor-aware audits and grading, and explicit unsupported-scope rejection. The runtime supports harness-connected single conversations only. No outbound or multi-call integration is claimed.

The tests cover role separation, task delivery, tool ownership, cancelled tool responses, simulator-invalid grading and unsupported-scope refusal alongside existing harness checks. Provider responses remain simulated. Real hosted task consumption, Realtime conversation/tool behavior and Rumik/Plivo connectivity require qualification. Domain workflows and datasets are not supplied by the infrastructure fixture.

Local verification for this change: Ruff lint and format checks passed; the provider-free suite passed all 80 tests with PostgreSQL and Chromium enabled. After final scope-label and setup-accounting edits, all 29 affected role/controller/report tests passed again. Tests used the existing dependency environment (`uv run --no-sync`); dependencies and lockfiles were unchanged. The temporary PostgreSQL server was stopped. No container rebuild or live provider run was performed for this update.

## Earlier infrastructure milestones

The six milestones are implemented before the role update. Local proof is separate from container integration and live qualification. The initial fixture is usable independently of all providers.

| Milestone | Implemented behavior | Relevant validation |
| --- | --- | --- |
| 1. Business and evidence | PostgreSQL state, atomic mutations/audits, provider mappings, authenticated tools, idempotency, immutable artifacts and checksums | Isolation, concurrent duplicates, conflicting IDs, rejected requests, transaction rollback, fresh-process reads, corrupt/torn evidence |
| 2. Controller and limits | Fresh attempt IDs, persisted dispatch intent, phase/validity/outcome separation, conservative reservations, leases, cancellation and bounded cleanup | Zero-budget block, setup failure, timeout, cancellation, unresolved termination, retained capacity |
| 3. Counterpart and browser | OpenAI Realtime WebSocket, received-audio perception and scoped business tools, truncation to played audio, Rumik registration before redemption, bundled Chromium/LiveKit worklets | Simulated model messages and rejected starts; local Chromium simultaneous audio, playback cancellation and cleanup |
| 4. Telephone | Plivo dialing, signed callbacks/media, unique route reservations, before-call binding, 8 kHz mu-law conversion, checkpoints and hangup | Forged signatures/tokens, duplicate callbacks, early setup failure, wrong-call media, codec and stream sequence checks |
| 5. Scoring and review | State/policy/duplicate/order checks, compatible-clock timing, explicit audio transcription, structured judge citations and versioned human review | False success prevention, target-drop failure, missing evidence, citation validation, review disagreement |
| 6. Batches and packaging | Paired randomized plans, frozen settings, drift checks, PostgreSQL recovery, S3 conditional writes, JSON/CSV accounting, worker image and India deployment settings | Plan reproducibility, budget reservations, recovery without redial, torn-log preservation, object collision checks and report denominators |

## Proof levels

1. **Unit and protocol validation:** implemented and exercised locally, including PostgreSQL and a real Chromium audio graph. Provider responses are simulated. The browser test exercises worklets, capture, rendering, cancellation and cleanup; it does not establish LiveKit-to-Rumik connectivity.
2. **Container validation:** Dockerfile, Compose settings and CI checks are supplied. An intermediate Linux arm64 worker image built successfully. Container startup then encountered a host disk-space failure; the integrated database/browser/object-store check is unverified. The final source needs a fresh image build and smoke test on a host with adequate disk, including the configured Linux amd64 India environment.
3. **Live qualification:** pending. An explicitly authorized browser call and equivalent phone call must perform an observable action, save usable recordings and receive human listening review.

## Operating limits

The first worker dispatches serially. Database reservations enforce a shared concurrency ceiling for workers using the same database. This does not account for unrelated calls made outside the benchmark; provider account capacity must also be qualified.

Spending limits reserve the operator's conservative maximum before dispatch, including counterpart, target and applicable carrier components. Model transcription/judgment has a separate reservation. Duration limits bound ongoing activity. These reservations are not real-time provider billing or a guarantee against an incorrectly estimated rate card. Unknown costs and unconfirmed termination never release budget as if they were free.

An uncertain start with no authoritative call identity stays unresolved. Recovery cannot safely infer that a call never existed. It retains the reservation and prevents another attempt until authoritative reconciliation is possible. Recovery does not resume a broken audio conversation.

Browser timing uses one audio-context sample clock. Carrier checkpoint receipt is a different observation boundary; telephone response-gap percentiles remain uncertain until a defensible media-clock mapping is qualified. Audio intelligibility and interruption quality require human listening.

## Required qualification inputs

Supply actual counterpart/judge/transcription model IDs, voice and behavior, a deployed target version, phone-capable engine, intended phone endpoints, public authenticated callback URL, funded component ceilings and rate-card version, workflow implementations/cases, grading rubrics and required metrics. No values or dataset coverage are invented by the harness.
