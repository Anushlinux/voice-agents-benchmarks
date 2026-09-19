# Architecture

The short data-flow diagram is in [README.md](../README.md). This document
records how to implement its boundaries without turning the benchmark into a
large evaluation platform.

## Deployment

- Develop and inspect evidence locally.
- Run reported conversations on a fixed India cloud VM using the same container
  and locked dependencies. Qualify CPU load, audio pacing and media connectivity.
- Rumik hosts the target. We do not operate its recognition/reasoning/voice stack.
- PostgreSQL will hold run metadata and isolated synthetic business state.
- Local artifact storage comes first; object storage follows before cloud batches.
- Vercel may host controls and a reviewer, but no frontend is needed for the first
  usable benchmark. Long-lived audio and browser work belong to the worker.

Vercel Functions and Vercel Sandbox are different deployment options. Current
Vercel documentation supports WebSockets, but function duration still bounds a
connection. Verify current Sandbox regions before using it for India media.
No cloud infrastructure is provisioned by this repository.

## Data boundaries

| Recipient | May receive | Must not receive |
| --- | --- | --- |
| Caller simulator | Customer brief, own speech state, received channel audio | Hidden expected outcomes, business database access, target transcript as perception |
| Hosted target | Business instructions, allowed tools, caller audio, permitted tool results | Caller hidden plan or evaluator answers |
| Business tools | Authenticated context, correlated run ID, operation arguments | Authority to mutate another run or production records |
| Evaluator | Private criteria, finalized evidence, state snapshots | Permission to repair the completed conversation |
| Human reviewer | Evidence, grades, uncertainty and configuration | An unexplained aggregate score as the only proof |

`CallerBrief` deliberately has no evaluator fields. The final scenario file
format is not chosen here: a future loader separates caller, environment and
evaluation inputs before handing them to these components.

## Browser flow

1. Controller creates a run and fresh business state.
2. Rumik registration returns a call ID before the target begins.
3. Controller persists the call-to-run mapping, then starts the web call.
4. Chromium joins the provided LiveKit room. Generated speech becomes the virtual
   microphone; subscribed audio is the customer's hearing.
5. Target HTTP tools access the run's business environment.
6. Separate send/receive loops capture audio and events through hangup.

API keys stay on the backend. Only short-lived room credentials reach the page.
Any direct WebSocket or native LiveKit diagnostic path gets a distinct label.

## Phone flow

1. Controller reserves a unique pending mapping for the caller number and target.
2. Plivo dials the Rumik-connected number and streams the answered call to us.
3. Rumik's before-call tool binds its call ID to that reserved run.
4. Received carrier audio drives the caller; generated speech returns over the
   bidirectional stream. Actual number-to-number calling remains in the path.
5. Capture carrier events, Rumik status, audio and business actions.

Confirm number provisioning, media routing and the meaning of context fields
before implementing correlation. Start serially; require unique number mappings
before concurrency. Ambiguous association is a setup failure, not a guessed match.
Outbound Rumik-to-simulator calls are a later alternative, not a silent fallback.

## Run lifecycle and recovery

Prepared → connecting → in conversation → finalizing → grading → reviewed.
Failures are recorded at the stage where they occur. Phase, test validity,
failure attribution and task outcome are separate concepts.

The future controller must enforce budgets during execution, preserve every
attempt, and reconcile an uncertain dial before retrying. A disconnected call
cannot resume as the same attempt. Finalization waits for call termination,
artifact storage and settled business state. Missing evidence stays visible.

## Implementation choices still open

Pipecat is the candidate caller/media framework; Chromium/LiveKit is the browser
path; Plivo is the first phone candidate. Speech and reasoning providers remain
subject to qualification, with Sarvam speech and a pinned text model as initial
candidates. Those SDKs are deliberately not dependencies until adapters are built.

Rumik tools are HTTP business endpoints, not an MCP requirement. Cekura is a
design reference rather than a runtime dependency.
