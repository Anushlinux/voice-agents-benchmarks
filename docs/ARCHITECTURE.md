# Architecture

The short data-flow diagram is in [README.md](../README.md). This document
records the implemented boundaries without turning the benchmark into a
large evaluation platform.

## Deployment

- Develop and inspect evidence locally.
- Run reported conversations on a fixed India cloud VM using the same container
  and locked dependencies. Qualify CPU load, audio pacing and media connectivity.
- Rumik hosts the target. We do not operate its recognition/reasoning/voice stack.
- PostgreSQL holds run metadata, leases, provider bindings and isolated synthetic business state. Business changes and tool audit entries commit in one transaction.
- Local evidence is sealed with checksums; explicit uploads use immutable S3-compatible object keys.
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

`CallerBrief` deliberately has no evaluator fields. The dataset authoring format remains separate. `ExecutionCase` is the internal input contract; the controller passes only its `caller` field to the customer simulator.

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

Qualify number provisioning, media routing and trusted context-field values before live execution. Start serially; require unique number mappings
before concurrency. Ambiguous association is a setup failure, not a guessed match.
Outbound Rumik-to-simulator calls are a later alternative, not a silent fallback.

## Run lifecycle and recovery

Prepared → connecting → in conversation → finalizing → grading → reviewed.
Failures are recorded at the stage where they occur. Phase, test validity,
failure attribution and task outcome are separate concepts.

The controller reserves funded ceilings before dispatch, applies setup/conversation/finalization timeouts, preserves every attempt, and requires reconciliation before retrying an uncertain start. A disconnected call
cannot resume as the same attempt. Finalization waits for call termination,
artifact storage and settled business state. Missing evidence stays visible.

## Implemented provider choices

The customer uses OpenAI Realtime directly over a server-side WebSocket. Its input is received PCM audio and the customer brief. Model, voice, turn detection and instructions are explicit configuration. On an interruption, the transport clears queued playback and reports confirmed progress; the customer truncates the model conversation to that played portion. Controlled interruption uses a separate configured timing behavior.

Chromium/LiveKit is the browser path. The bridge is bundled locally, publishes a generated microphone track, and captures subscribed target audio through audio worklets. Independent bounded queues preserve simultaneous send/receive. Generated, submitted, rendered and received recordings have distinct meanings.

Plivo is the telephone path. The adapter uses signed HTTP/WebSocket callbacks, an attempt-specific stream token, mu-law at 8 kHz, streaming conversion to PCM and explicit playback checkpoints. Ordinary silent media frames count as a healthy stream; missing media or unacknowledged playback is recorded as a transport problem.

Rumik tools are HTTP business endpoints, not an MCP requirement. There is no Pipecat or Sarvam caller dependency. Cekura is a design reference and is not called by this repository.

See [running instructions](RUNNING.md) for workflow registration, costs, recovery and qualification limitations.
