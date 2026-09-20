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
