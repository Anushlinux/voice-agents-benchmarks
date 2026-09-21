# Architecture

## Core flow

A user task goes to hosted Rumik. Rumik talks over audio with a simulated person. That person's business actions use isolated records. The evaluator checks the resulting conversation and state against the user's task.

The target is Rumik's hosted assistant, not a custom assistant using Rumik text-to-speech. The harness does not deploy or reconfigure the hosted agent. OpenAI Realtime supplies the other person and is not ranked as a competitor.

## Information boundaries

| Recipient | May receive | Must not receive |
| --- | --- | --- |
| Rumik | User request, known facts, constraints, permissions, counterpart audio, its permitted tool results | Counterpart's private strategy, unrestricted business state, grading criteria |
| Counterpart | Assigned role, own facts and behavior, received Rumik audio, its permitted tool results | Private user task, hidden expected outcomes, Rumik transcript as hearing, unrestricted database |
| Business service | Worker-bound run or authenticated provider identity, actor, operation and arguments | Authority to modify another attempt or production records |
| Evaluator/reviewer | Both briefs, criteria, finalized recordings, action audit and state | Permission to repair a completed conversation |

`ExecutionCase` schema 2 contains `UserTask` and `CounterpartBrief` separately. The controller passes only `case.counterpart` to the simulator. The authenticated before-call endpoint returns only `user_task` to Rumik. Tool grants are fixed per case and denied by default. Actor identity is supplied by the worker or endpoint, never model arguments.

Workflow implementations provide tool descriptions, parameter schemas and business rules. The counterpart gets only its granted definitions and results; it does not receive the whole initial state. For a reservation, the business side owns reservation changes. Rumik can use only explicitly modeled user-authorized tools.

## Single-call execution

1. Create independent state and persist the user's task, canonical target identity and role-specific tool grants.
2. Reserve funded limits. For browser calls, prepare Chromium and verify its local audio clock and mono microphone before registering or starting a hosted call; then correlate the provider call ID with the attempt.
3. Connect Chromium/LiveKit or the existing Plivo route.
4. The hosted agent invokes the authenticated before-call endpoint. It verifies the provider/run/agent mapping and returns the user's task. The controller waits for that response to be served within the setup deadline.
5. Start the OpenAI counterpart with its own brief and role-permitted tool definitions. Speech perception uses received audio only.
6. Handle counterpart tools through the worker-bound attempt; handle Rumik tools through authenticated provider correlation. Reject unauthorized actions and keep their evidence.
7. Confirm call termination, settle business state, seal recordings and audits, then evaluate.

`target/task-delivery.json` records the call identity and task checksum. It proves the harness served the task, not that Rumik incorporated it into its instructions. The hosted agent must be configured to consume this before-call response; this remains a required live qualification check.

## Audio and tools

Chromium joins the registered LiveKit room. Generated counterpart audio becomes the virtual microphone and subscribed Rumik audio becomes the counterpart's hearing. Independent queues preserve simultaneous send/receive and capture. On interruption, queued playback is cleared and the model conversation is truncated to confirmed playback.

The OpenAI counterpart uses a server-side Realtime WebSocket. Business calls use a separate worker so audio reception continues while a tool runs. Arguments are executed only after their containing model response completes successfully; cancelled or incomplete responses cannot mutate records. Operation identities are scoped to the actor and attempt, so repeats replay safely and the two actors cannot collide.

One response coordinator waits for committed caller input, including when a tool
finishes during a pause. It rechecks that condition after asynchronous preparation.
An interrupted response cannot send late audio or execute late proposed tools,
even if its completion acknowledgement races with cancellation. New natural
restaurant cases require semantic turn detection with low eagerness. This changes
how the model decides a spoken turn is complete; simultaneous audio remains enabled.
Browser events retain their individual sample clocks and ordering, but queued
events share a bridge call and durable write to prevent evidence overhead from
gradually delaying audio delivery. The queue remains bounded and fails explicitly.

`target_report_then_conversation_end` requires the saved private report and either
a remote hangup or explicit `finish_counterpart` after closing playback drains.
The controller preserves trailing received speech and waits for one second of
quiet before closing and verifying provider termination. A new caller turn during
closing playback withdraws the finish action. Report receipt or an ordinary return
from the counterpart cannot end the call. Tests of Rumik's own hangup retain the
stricter `target_report_then_hangup` policy; employee termination is recorded
separately and cannot count as a target hangup.

The Plivo adapter currently dials into the Rumik-connected number. Authenticated callbacks, unique route reservations, 8 kHz mu-law audio, conversion and playback checkpoints remain in place. This is labeled `harness_connected`; it does not implement Rumik-originated dialing. Outbound and multi-call execution fail before dispatch, without a fallback.

## Evidence and grading

Browser transport diagnostics are observations, not causal verdicts. Connection
and track lifecycle events accompany one-second audio packet statistics where
supported. Their browser clocks remain separate from worker receipt timestamps.
Missing packets can reflect normal silence handling. Neither packet delivery nor
local playback proves what the hosted model perceived. Versioned report diagnostics
keep observed task completion separate from simulation validity and failure owner.

New batches preserve a source-file checksum inventory and an archive of Python,
browser source, executed browser bundles and dependency locks. This includes
uncommitted source changes and excludes credentials, datasets and call evidence.

Business mutations and audits commit together in PostgreSQL. Audits identify target, counterpart or local harness operations. A forbidden target action contributes to target policy failure. A forbidden counterpart action invalidates the simulation instead of failing Rumik. Conversational validity also requires model/human review: business permission alone does not prove that a concession or booking was justified by the conversation.

Raw evidence stays immutable. Rescoring writes a new version. Legacy evidence remains readable with its original roles; new execution rejects old customer-style case inputs instead of silently reversing them. For compatibility, the internal `caller/` package, event source `caller`, `config/caller-effective.json` and timing keys retain their names; for schema 2 they describe the counterpart, not the user or Rumik.

Browser, carrier, provider and local clocks are labeled separately. Rendered browser audio and carrier checkpoint receipt have different observation boundaries. Reports retain planned, attempted, valid, invalid, unresolved, passed and failed counts and label task scope and call initiation. A valid target-side drop remains a failure.

## Deployment and remaining work

Develop and inspect locally. Reported calls should run on a qualified fixed India worker with locked dependencies. Rumik hosts the target. PostgreSQL stores attempt state; checksummed local evidence can be explicitly uploaded to immutable S3-compatible storage. No cloud infrastructure is provisioned here. Imports, status, planning and health routes remain provider-free.

Long conversations fit the current single-call lifecycle within explicit time/spend limits. Completing a user task across calls, approvals, transfers between independently modeled participants, and app actions needs a task coordinator and additional adapters. They are not provided by retry or batch support. Recovery finalizes abandoned attempts; it never resumes a conversation or chooses the next business to call.

Live Rumik task consumption, counterpart audio/tools and the telephone path still require qualification. `/healthz` reports process health; `/readyz` remains 503. See [running instructions](RUNNING.md) and [implementation status](IMPLEMENTATION.md).


## Persistence and report revisions

The browser audio clock owns playback pacing. Python fills a bounded lookahead
queue instead of sleeping for each audio chunk. Cancellation changes a generation
number so an old in-flight push cannot restart cancelled speech.

The synthetic microphone destination and LiveKit publication are explicitly mono.
A mono AudioWorklet does not make its MediaStream destination mono: Chromium's
default destination is stereo, and LiveKit infers stereo publication from that
track. Local Chromium validation checks the actual media-track settings. This
format correction still requires live qualification; it does not establish that
the earlier stereo format caused the observed silent turns. The unsuccessful
DTX-off diagnostic was removed, restoring normal silence suppression.

Browser audio and observations enter a bounded persistence queue. Disk writes do
not block live hearing or microphone scheduling. The queue flushes before business
mutations inspect speech evidence and before recordings are sealed. Overflow or
write failure invalidates the harness attempt; it cannot become a target failure.
Queued observations retain their original worker receipt times and browser sample
positions. A process crash can lose observations still in memory, so recovery must
remain incomplete rather than pretending the queue was durable. Finalized runs
require successful flushing and checksummed evidence.

The incoming media track also has a native WebM recording independent of Web
Audio. It is a diagnostic observation at the received-track boundary, not a copy
of hosted synthesis output. Agreement between the recordings cannot identify an
upstream failure owner.

New cases explicitly choose `revisable_until_close` for their private report. The
endpoint retains every accepted revision, every rejected request, and the latest
accepted report. Historical `final_once` cases retain their original behavior.
Revisions cannot mutate business state or cross an attempt boundary. A missing
report is retained as an empty request ledger. Local conversation timeouts are
reported as `ConversationTimeout`, without claiming a network failure.

Conversational judgments now include bounded quotations with speaker identities.
The evaluator checks these against the separate recording transcriptions. An
unsupported or wrong-speaker claim makes the affected metric uncertain; the raw
judge answer remains available. This cannot prove transcription accuracy or replace
human listening.

Each report exports `turn-timestamps.csv`: playback start/end, employee speech
end, first captured target speech, response duration and missing/overlap status.
Call lifecycle observations also retain worker UTC, monotonic timestamps and
provider timestamps separately. Target TTFT remains unavailable without an
exposed first-token event. Audio response latency is never relabeled as TTFT.

The browser uses Chromium's silent audio-output device for graph timing instead
of depending on the desktop's physical output device. A running context label is
insufficient: readiness requires clock advancement and the actual mono track
format. A failed local preparation occurs before provider actions. Its live
adapter can confirm that no call was requested; an uncertain registration remains
unresolved. This change passed local tests but still needs connected live proof.

Natural restaurant counterpart responses narrow their advertised business tools
to the current workflow prerequisites. Booking is offered only when an active
offer has complete employee playback followed by caller speech after its terms
boundary. This is structural evidence, not semantic consent. The model must still
hear agreement, the executor rechecks every action, and rejected attempts remain
in evidence. Neither private user constraints nor grading answers enter this
projection. The original session grants remain the maximum authority.
