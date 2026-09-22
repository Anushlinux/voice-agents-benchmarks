# Rumik with Plivo

Plivo owns the carrier side, including benchmark phone endpoints and SIP trunking.
Rumik hosts the assistant. Local setup commands do not rent numbers, register
trunks, deploy agents or start paid activity.

## Current executable phone path

The harness's Plivo Voice API adapter dials the designated target number and
streams the simulated counterpart's audio. The target number's Plivo inbound
SIP route connects to Rumik. Simultaneous audio, signed callbacks, per-attempt
provider bindings, funding and carrier hangup remain in that adapter.
This measures one harness-connected conversation, not autonomous outbound behavior.

Plivo Voice API media/control and Zentrunk SIP service are distinct surfaces.
Do not assume a Voice API UUID can control a Zentrunk leg. Qualify each direction
using its own provider identity. Plivo documents separate
[inbound and outbound trunks](https://www.plivo.com/docs/sip-trunking).

For phone runs, set `target.plivo_sip_trunk_id` to the existing trunk UUID registered
in Rumik, and `target.plivo_termination_uri` to its existing Plivo outbound endpoint.
The runtime snapshots the trunk and checks its number, agent assignment, active
status, stored authentication and exact termination URI before dispatch. The
snapshot is frozen with the batch and checked for drift. This checks configuration
consistency, not connectivity or secret equality.

## Direct SIP destination without a rented number

Rumik registers SIP trunks for Indian `+91` mobile numbers only, and it publishes one
SIP origination host for every registered number (`GET /v1/sip-trunks/origination-uri`).
When the Plivo account has no rentable number, the harness can still connect one
conversation by dialing that host directly: set `runtime.target_sip_uri` to
`sip:<registered +91 number>@<origination host>` while `runtime.target_number` stays the
registered number. Plivo places the leg as an outbound SIP call from
`runtime.caller_number`; the registered trunk, its assigned agent, termination URI and
stored authentication are still checked before dispatch.

Carrier callbacks and the target's before-call identity may format the same number with
or without a plus sign, or wrap it in a SIP URI. Correlation compares the subscriber
digits, which must still match exactly. A before-call naming the target's handle maps to
the same reserved route as its canonical ID. Non-secret carrier callback facts (numbers,
call state, hangup cause, stream acceptance or rejection reason) are appended to the
batch's `callback-requests.jsonl`, and the first stream event plus any stream failure
are recorded in the attempt's evidence, so a failed telephone attempt remains diagnosable.
Connectivity and conversation evidence must be checked in the individual live run;
the configured route alone does not prove a successful conversation.

## Task delivery without dataset changes

Rumik's before-call tools fill prompt variables from response outputs. The callback
now returns `user_task_json` alongside `user_task`; both contain only the user's
assignment, facts, constraints and permissions. They exclude hidden counterpart
facts, grading answers and business records.

Set `target.task_variable` (default `benchmark_user_task`) and the real HTTPS
callback base URL, then generate a reviewable configuration plan offline:

```sh
voice-bench target prepare --config configs/live.local.toml \
  --output reports/rumik-setup.json
```

The plan includes the HTTP body, output mapping, variable declaration, prompt
instruction and Plivo route. Supply the bearer secret from `BENCH_TOOLS_SECRET`
when configuring the hosted tool, and bind the variable to its actual returned
tool ID. The generated plan does not mutate an account.

Use the task variable in the deployed prompt and leave its default empty. Live
preflight checks the prompt reference, variable/tool linkage, callback URL,
trusted identity bindings, output mapping and stored bearer authentication. The
controller still waits for the correlated callback before starting the counterpart.

A saved target snapshot can be checked without provider access:

```sh
voice-bench target check --config configs/live.local.toml \
  --snapshot reports/target-snapshot.json
```

`configured: true` is not proof of hosted task consumption or working audio.
Changing configuration requires a new frozen batch, not resume.

## Outbound primitive and remaining executor

Rumik documents [`POST /v1/calls`](https://docs.rumik.ai/api-reference/calls/place-an-outbound-call)
with `agentId`, `toNumber` and `fromTrunkId`. The client implements this operation
with an explicit Plivo trunk UUID, allowlisted benchmark destination and no retry.
It cannot fall back to Rumik's shared number or number rental.

This is a client primitive, **not an executable outbound benchmark**. The CLI
continues to reject `rumik_outbound`. Completing that path still requires:

1. A counterpart endpoint receiving the Rumik-to-Plivo outbound leg.
2. Correlation before before-call tools run, including callbacks racing the dial
   response and starts with no returned call ID.
3. Documented duration enforcement and termination/reconciliation for the relevant
   SIP leg, including calls that never reach the counterpart endpoint.
4. Protocol/integration tests followed by an authorized real call.

A harness-selected destination is not evidence that Rumik chose where to call.

## Full-task and report contract gaps

The public docs reviewed on 2026-09-20 describe individual calls, before/during-call
tools and call records. They do not document a persistent user-task API for
cross-call memory, approvals, autonomous destination selection or user-report
delivery. Confirm that product interface with Rumik before implementing its task
executor. The harness must not make those choices and credit them to Rumik.

The [`GET /v1/calls/{id}`](https://docs.rumik.ai/api-reference/calls/get-a-call)
`summary` is explicitly an on-demand dashboard summary. Review now rejects
`summary` and `transcript` as user-report pointers. Native report delivery remains
an integration gap; missing proof remains inconclusive, not a target failure.

Sources: [agents API](https://docs.rumik.ai/agents-api),
[variables and tools](https://docs.rumik.ai/variables-and-tools),
[register a SIP trunk](https://docs.rumik.ai/api-reference/sip-trunks/register-a-sip-trunk),
[get a SIP trunk](https://docs.rumik.ai/api-reference/sip-trunks/get-a-sip-trunk).

## SIP authentication and phone diagnostics

A SIP `407 Unauthorized` response is an authentication challenge, not proof that
an active Rumik trunk is missing. Configure `PLIVO_SIP_AUTH_USERNAME` and
`PLIVO_SIP_AUTH_PASSWORD` together for an authenticated direct SIP destination.
The adapter sends them only in Plivo's `sip_auth_username` / `sip_auth_password`
dial fields. They do not belong in the run configuration, source snapshot or
recorded evidence. Preserve the origination URI's `;transport=tcp` parameter.
See [Plivo SIP authentication](https://www.plivo.com/docs/voice/concepts/sip-authentication).

For programmatic runners, resolve `artifact_root` to an absolute path before
calling `execute_batch`. The TOML loader resolves relative paths against the
configuration file; direct Pydantic construction does not do that conversion.

Completed Plivo call records may have no `call_status`. Reconciliation and recovery
use the final `end_time` or `hangup_cause_name`, not the legacy `call_state`.
Signed early hangup callbacks wake the connection wait immediately, including
`no-answer`, `failed`, `cancel`, `busy` and `timeout` outcomes.

WebSocket authentication checks the configured public URL and the stream signature,
plus the per-attempt token. The Python Plivo SDK's URL validator rejects `wss://`
before checking a signature, so stream verification uses its signing helpers
directly. A captured live handshake verified that Plivo signs the `http://`
form of the public URL even though the connection uses `wss://`. Verification
accepts that signed form while retaining the configured host/path, shared-secret
HMAC and per-attempt token checks. This does not allow plaintext media transport.
Missing or invalid signatures remain rejected.

Live Plivo streams can start at event number zero, identify the account by an
internal numeric ID, and reuse an event number for a playback acknowledgment.
The stream is authenticated with the account secret and bound to its exact call
UUID. Audio continuity is checked using consecutive `media.chunk` values, so
duplicate or missing audio still fails the run. Shared event-number irregularities
are retained as diagnostics rather than disconnecting otherwise intact audio.

Reservation evidence supports both browser rendering and Plivo playback checkpoints.
A telephone booking requires acknowledgment of the complete preceding counterpart
utterance, followed by a completed received speech turn. It references `audio/sent.wav`,
`audio/received.wav` and the checkpoint events, without calling submitted audio a
remote recording. This establishes observed ordering; whether the spoken reply
actually accepts the terms still requires review.

A smoke case that needs a final user report must grant `submit_user_report` in
`target_tools`, set `completion` to `target_report_then_conversation_end` (or the
stricter target-hangup mode), and use `criteria.user_report_source: target_callback`.
An older counterpart-completion case does not establish report delivery.
