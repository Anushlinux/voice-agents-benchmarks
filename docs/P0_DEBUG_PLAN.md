# Ground-up investigation: restaurant conversations that stall

Status: active. The September 22 Mulberry verification reproduced the failure.
A booking alone, a watchdog hangup, or passing unit tests cannot close this issue.

## Required outcome

Understand where each observed failure starts, repair the components we own, and
verify that hosted Rumik can complete the original restaurant tasks: acknowledge a
supported result, submit an accurate private report, and end the conversation
normally. The employee must remain truthful, obtain actual agreement and perform
only permitted business actions. No-booking cases must also conclude correctly.
Do not make the benchmark easier, fabricate target answers, remove reports from
acceptance, or label silence as success to obtain a green result.

## Investigation order and proof

| Stage | Question | Evidence or experiment | Completion criterion |
| --- | --- | --- | --- |
| 1. Freeze | What code, case, prompts, tools and provider configuration actually ran? | Saved source archive, configuration snapshots, task delivery, manifest, raw events and audio | Reproducible inventory; old evidence unchanged |
| 2. Reconstruct | At which boundary does the unanswered turn stop progressing? | Employee generated/rendered audio; target-side transcript and generation events; target synthesis events; captured audio; report ledger | One timeline with event sequences and explicitly separate clocks; distinguish missing telemetry from absent activity |
| 3. Task and prompts | Does Rumik receive the correct task? Do either actor's instructions conflict or require needless exchanges? | Authenticated delivery, frozen prompt and tool descriptions, actual spoken request | Identify contradictions; prepare reviewable prompt candidates; do not assume prompt changes work |
| 4. Transport | Are audio samples dropped, delayed, muted, clipped, duplicated or echoed? | Real browser tests; generated vs played audio; native received recording; packet/track observations; target-side transcripts | Explain discrepancies; uninterrupted two-way audio remains supported |
| 5. Turn ownership | Do pauses, cancellations, tool continuations or stale responses create false turns or lose answers? | Reproduce live event order using the real response coordinator with synthetic provider events | Regressions demonstrate valid sequencing through interruptions and slow tools |
| 6. Employee business actions | Why does the employee book before asking? | Replay lookup → offer → attempted booking before speech; compare available tool definitions with action preconditions | Do not advertise structurally impossible actions; still audit and reject any attempted bypass; semantic agreement still required |
| 7. Target generation | Does generation produce text, tool calls and speech after recognized input? | Correlate generation start/stop, usage, text and synthesis observations; compare silent and answered turns | Identify the first missing stage; token-limit explanation stays a hypothesis unless an intervention or explicit provider result establishes it |
| 8. Report and close | Does reporting fail, or is it never attempted? Can closure race with speech? | Callback request ledger, tool configuration, controller state, closing-playback tests | Accurate report saved; closing speech drained; normal end reason and confirmed provider termination |
| 9. Controlled live isolation | Which specific change fixes the failure? | One variable changed at a time; short acoustic/control task, then original restaurant case; fixed Mulberry target unless prompt is the chosen variable | Separate diagnostic controls from benchmark coverage; no retries disguised as independent coverage |
| 10. Qualification | Does the repair hold beyond a single easy success? | Repeated original failed case, then all ten executable cases including legitimate no-booking outcomes, with full evidence and evaluation | Report every attempt and invalid run; no common unexplained stall; truthful task outcomes and normal closure; scope of proof stated exactly |

## What the latest evidence establishes

Batch `f10d7597-4972-4f1a-a906-2a2641b0c126`, run
`d82da3f4-9f1f-4beb-8d5c-32aef2435d8a`:

- The employee chained lookup, offer and attempted booking without an intervening
  spoken offer or new target reply. The action guard rejected the premature request.
  The session nevertheless advertised the booking tool throughout this sequence.
- After the later spoken offer and agreement, the correct synthetic booking was saved.
- Target-side `user-llm-text` observations include the final reference segment and
  acknowledgement question, then both parts of the follow-up. This supports actual
  target-side recognition of these inputs; it is stronger than local playback alone.
- Each of those last three completed generations reports 400 completion tokens,
  including 396–397 reasoning tokens. No target speech follows the reference.
  The actual configured limit and provider finish reason are unavailable.
- The reference recital is split into eight target-side recognized input segments.
  The service repeatedly starts and interrupts generation during the recital.
  These are target-side observations; OpenAI's low-eagerness setting controls the
  employee's hearing and does not configure Rumik's own turn detection.
- The case says to deliver the reference naturally and spell it when needed; the
  business tool result instead requires every character to be spelled using examples.
  This conflict is owned here, but its contribution to target silence is unproven.
- No report request arrived. This call does not establish a callback HTTP failure.
- Formal simulation validity is invalid because of the premature booking attempt;
  the outcome is unresolved. Missing acknowledgement and report remain observable.

## Competing explanations and next discriminating checks

| Explanation | Current evidence | Next check |
| --- | --- | --- |
| Audio never reached Rumik | Contradicted for the final unanswered inputs by target-side recognized text | Correlate all failed and successful turns; inspect recordings for local loss separately |
| Target turn detector fragments employee speech | Observed during greeting, offer and reference | Compare generation interruptions with acoustic pauses; control experiment with equivalent concise speech, preserving meaning |
| Target completion allowance is consumed by reasoning | Repeated 400/396–397 pattern; limit itself unknown | Compare completed generations with/without output; controlled prompt-only experiment if public API cannot adjust allowance |
| Counterpart tool continuation fabricates agreement | Premature booking is observed despite instructions | Derive advertised tools from current business prerequisites; replay event sequence and attempted bypass |
| Prompt/report-tool workload stalls final response | Plausible; deployed target prompt is lengthy and the report follows closing | Audit syntax/binding; prepare minimal equivalent prompt and isolate it in a bounded live test |
| Harness cancels or cuts off a real target reply | No received reply after reference; local employee playback passed | Trace target synthesis/text vs native incoming capture, and interruption ownership; never infer spoken audio from generated text |
| Controller closes before completion | Inactivity timeout is downstream of silence in this run | Regression-test report/closing races and preserve end reason; do not extend timers as a substitute for fixing response generation |

## Live experiment boundary

The prior one-call ₹155 allowance is exhausted. Read-only analysis, code repair and
provider-free tests continue now. Before any additional paid run, prepare the exact
case, prompt/configuration changes, number of calls, total reserved spend and stop
conditions for approval. The earlier temporary tunnel approval does not itself fund
another call. No new key, deployment or provider call is needed for the offline work.

Proposed sequence: first qualify the employee's action ordering offline; then choose
the smallest live intervention that distinguishes the leading explanations. Avoid
changing transport, both prompts, reference format and timeout in the same call.
Any temporary shared callback changes must be snapshotted and restored. No automatic
paid retries. A successful diagnostic control is not restaurant-suite qualification.

## Closure audit

Before declaring fixed, inspect the actual final code and live artifacts against
every stage above. Require relevant Python tests, ruff checks and formatting, real
browser transport checks for transport changes, verified evidence bundles, complete
cohort counts, final reports, confirmed termination, restored callback settings and
stopped temporary compute. Record unresolved provider-internal questions honestly.
If evidence only supports a narrower conclusion, keep the issue open.

## Current progress after the one-call authorization

The proposed four-call comparison was reduced by the user to one attempt. That
attempt started at Rumik but never connected because Chromium's audio clock stayed
at zero. The shorter prompt therefore has no live conversational result. Rumik
subsequently confirmed `failed / never_connected`, zero duration and zero credits
charged. Recovery confirmed termination and released the reservation; the original
agent version and callback settings were restored and temporary services stopped.

The response-tool projection passes exact replay of the prior connected call.
The final browser repair uses Chromium's silent output and checks local audio
readiness before any provider registration/start. It distinguishes a known local
preflight failure from an uncertain registration. Validation: 344 Python tests
including PostgreSQL and Chromium, 12 JavaScript tests, and 20 fresh preparations
using production browser flags. No additional live call ran.

Stages 1–2 now have a saved reconstruction of 11 existing attempts; stages 4–6
have additional local repairs and regressions. Generation/report root cause and
connected live qualification remain incomplete. Findings and exact proof are in
`reports/p0-ground-up-debug-20260922/README.md`. The goal remains active.

## Stage 7 finding: the repeated 400-token ceiling

Aggregating every captured usage packet across all eleven connected attempts: 30
generations, 21 distinct completion counts scattered from 11 to 391, then exactly 400
nine times and never higher. The nine split differently between reasoning and visible
tokens (396+4, 397+3, 301+99, 196+204, 163+237), which is the outside signature of a
maximum-tokens setting rather than a coincidence of content. Seven were silent turns
and two were mid-sentence cutoffs. This is the first missing stage for every stalled
call whose capture survived: generation completes with nothing to synthesize.

Harness mitigations now in the tree (compact numeric reference spoken in one sentence,
a prompt roughly half the size, a one-or-two-sentence report, list-free employee turns)
reduce the reasoning load at the turns where the ceiling was hit. They do not change
the ceiling. The discriminating live check is the same original Aditi case under the
frozen new configuration, reading `max_completion_observed` and
`samples_at_max_completion` from the generation diagnostics afterward.
