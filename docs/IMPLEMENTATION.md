# Implementation roadmap

## Foundation — implemented

- [x] Package layout following the agreed six-part data flow.
- [x] Provider-independent caller, audio, business, evidence and grading contracts.
- [x] Offline configuration/status CLI and an import-safe local API.
- [x] Development configuration, dependency lock, checks and CI definition.
- [x] Optional local containers; no production deployment or providers connected.

All milestones below are unfinished. Check boxes describe implementation state,
not account capabilities or benchmark results.

## 1. Business isolation and evidence

- [ ] Implement a local append-only event log and immutable artifact store.
- [ ] Add manifests, checksums, explicit missing-evidence status and rescoring paths.
- [ ] Implement run-scoped business state with request and mutation logs.
- [ ] Add call-ID mapping, authenticated HTTP tools and duplicate request handling.
- [ ] Verify two runs cannot read or mutate each other's records.

Acceptance: a deterministic local fixture proves isolated state and an auditable
mutation, including a rejected action. Label it a harness fixture, not a dataset
case or a Rumik result. The dataset workstream supplies actual workflow semantics.

## 2. One real browser conversation

- [ ] Qualify a deployed Hinglish Rumik configuration and snapshot all inputs.
- [ ] Implement registration, call correlation and Chromium/LiveKit audio transport.
- [ ] Add a caller with controlled facts and independent send/receive loops.
- [ ] Capture sent/received speech, caller decisions, events and final state.
- [ ] Exercise one permitted business action and an incorrect-action control.
- [ ] Prove cleanup and finalization for normal exit, timeout and dropped transport.

Acceptance: listen to the actual recording, match the tool action to the final
state, and show that neither caller nor evaluator relied on a hidden transcript.
Live testing begins only with explicit budget and intended target configuration.

## 3. Equivalent real telephone conversation

- [ ] Verify phone-capable Rumik configuration, number access and India media route.
- [ ] Implement Plivo dialing, answer instructions, media stream and hangup.
- [ ] Validate callback authentication and unambiguous run correlation.
- [ ] Save both providers' call identifiers and available evidence.
- [ ] Qualify playback timing and simultaneous speaking/listening.

Acceptance: a real numbered call completes the same permitted business action.
Prove setup failure, one-way-audio detection, disconnect handling and duration
limits before automating batches. Do not substitute degraded browser audio.

## 4. Trustworthy scoring and review

- [ ] Implement outcome and policy checks against action logs and final state.
- [ ] Add clock-aware audio timing and interruption measures.
- [ ] Add evidence-citing rubric assessment with an uncertain result.
- [ ] Record human review of both passes and failures.
- [ ] Validate graders with deliberately known successes, failures and evidence gaps.

Acceptance: no spoken completion claim can pass a failed business action; an
invalid simulator run is not labeled a target failure; missing evidence cannot
silently produce a passing metric.

## 5. Repeated cloud batches

- [ ] Add PostgreSQL persistence and durable object storage.
- [ ] Implement scheduling, runtime budgets, attempt retention and crash recovery.
- [ ] Pin worker region, dependencies and configurations for a reported batch.
- [ ] Interleave browser/phone execution and preserve case/repetition pairing.
- [ ] Export per-run and aggregate results with all denominators and exclusions.
- [ ] Verify the controller finalized and compute stopped before declaring completion.

Acceptance: an interrupted batch can recover without duplicate calls or lost
evidence, and every planned run is accounted for.

## Later, only if useful

- Optional Vercel controls and evidence review interface.
- Rumik outbound-to-simulator telephone direction.
- Native LiveKit / direct Rumik WebSocket diagnostics, labeled separately.

## Inputs needed before live qualification

Target access and configuration; chosen call direction and intended numbers;
account capacity and media route; maximum minutes/spend; caller configuration;
workflow tool semantics; evidence availability. Dataset size and contents remain
the separate dataset workstream's responsibility.
