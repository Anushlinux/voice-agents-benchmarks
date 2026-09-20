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
2. Reserve funded limits and correlate the provider call ID with the attempt.
3. Connect Chromium/LiveKit or the existing Plivo route.
4. The hosted agent invokes the authenticated before-call endpoint. It verifies the provider/run/agent mapping and returns the user's task. The controller waits for that response to be served within the setup deadline.
5. Start the OpenAI counterpart with its own brief and role-permitted tool definitions. Speech perception uses received audio only.
6. Handle counterpart tools through the worker-bound attempt; handle Rumik tools through authenticated provider correlation. Reject unauthorized actions and keep their evidence.
7. Confirm call termination, settle business state, seal recordings and audits, then evaluate.

`target/task-delivery.json` records the call identity and task checksum. It proves the harness served the task, not that Rumik incorporated it into its instructions. The hosted agent must be configured to consume this before-call response; this remains a required live qualification check.

## Audio and tools

Chromium joins the registered LiveKit room. Generated counterpart audio becomes the virtual microphone and subscribed Rumik audio becomes the counterpart's hearing. Independent queues preserve simultaneous send/receive and capture. On interruption, queued playback is cleared and the model conversation is truncated to confirmed playback.

The OpenAI counterpart uses a server-side Realtime WebSocket. Business calls use a separate worker so audio reception continues while a tool runs. Arguments are executed only after their containing model response completes successfully; cancelled or incomplete responses cannot mutate records. Operation identities are scoped to the actor and attempt, so repeats replay safely and the two actors cannot collide.

The Plivo adapter currently dials into the Rumik-connected number. Authenticated callbacks, unique route reservations, 8 kHz mu-law audio, conversion and playback checkpoints remain in place. This is labeled `harness_connected`; it does not implement Rumik-originated dialing. Outbound and multi-call execution fail before dispatch, without a fallback.

## Evidence and grading

Business mutations and audits commit together in PostgreSQL. Audits identify target, counterpart or local harness operations. A forbidden target action contributes to target policy failure. A forbidden counterpart action invalidates the simulation instead of failing Rumik. Conversational validity also requires model/human review: business permission alone does not prove that a concession or booking was justified by the conversation.

Raw evidence stays immutable. Rescoring writes a new version. Legacy evidence remains readable with its original roles; new execution rejects old customer-style case inputs instead of silently reversing them. For compatibility, the internal `caller/` package, event source `caller`, `config/caller-effective.json` and timing keys retain their names; for schema 2 they describe the counterpart, not the user or Rumik.

Browser, carrier, provider and local clocks are labeled separately. Rendered browser audio and carrier checkpoint receipt have different observation boundaries. Reports retain planned, attempted, valid, invalid, unresolved, passed and failed counts and label task scope and call initiation. A valid target-side drop remains a failure.

## Deployment and remaining work

Develop and inspect locally. Reported calls should run on a qualified fixed India worker with locked dependencies. Rumik hosts the target. PostgreSQL stores attempt state; checksummed local evidence can be explicitly uploaded to immutable S3-compatible storage. No cloud infrastructure is provisioned here. Imports, status, planning and health routes remain provider-free.

Long conversations fit the current single-call lifecycle within explicit time/spend limits. Completing a user task across calls, approvals, transfers between independently modeled participants, and app actions needs a task coordinator and additional adapters. They are not provided by retry or batch support. Recovery finalizes abandoned attempts; it never resumes a conversation or chooses the next business to call.

Live Rumik task consumption, counterpart audio/tools and the telephone path still require qualification. `/healthz` reports process health; `/readyz` remains 503. See [running instructions](RUNNING.md) and [implementation status](IMPLEMENTATION.md).
