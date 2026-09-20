# Reusable profiles, bounded scenarios and explicit grading

This is the first implementation of the design improvements discussed from the
provided Cekura screenshots. It extends the existing restaurant workflow; it does
not copy Cekura datasets, infer undocumented scoring scales, or add live results.
No Cekura integration is used.

## Prepare a new version offline

List the supported behavior profiles:

```sh
uv run --locked voice-bench design profiles
```

Prepare a profile and explicit rubric for an existing restaurant case file:

```sh
uv run --locked voice-bench design prepare \
  --cases datasets/tm1_restaurant_mumbai_hinglish_001/execution-cases.json \
  --profile concise \
  --output datasets/restaurant-concise.design1.json

uv run --locked voice-bench batch plan \
  --config configs/restaurant-pilot.local.toml \
  --cases datasets/restaurant-concise.design1.json
```

The same preparation accepts the existing hard-case input file. Plan those cases
with `configs/restaurant-hard.local.toml`. Preparation and planning never connect
to providers, initialize a database, or spend a live-call budget. The input must
already exist; these commands do not acquire or invent a dataset. Outputs cannot
overwrite an existing file. Prepared dataset files remain ignored by Git.

Preparation preserves the original case ID, user task, counterpart facts, tools,
business state, challenge events and existing required metrics. It creates a new
case version such as `1.design1.concise` and records the source case version and
hash. Prepare each profile from the original source, not from another profile.
Run different profiles as separate batches with matching target settings. The
same task under three profiles is one underlying task, not three task families.

Existing cases without the new optional fields retain their previous execution
and grading behavior. Saved evidence is never rewritten by preparation or grading.

## What profiles control

| Profile | Behavior |
| --- | --- |
| `straightforward` | Direct, cooperative, complete answers |
| `concise` | Brief answers without omitting material business or confirmation terms |
| `clarification_seeking` | Clarify genuinely ambiguous details without re-asking clear facts |

Profiles do not change voice selection, speech rate, accent, noise, inventory or
tool permissions. They are instructions to the counterpart, not verified claims
about its behavior. Listening review must confirm compliance.

The worker composes a counterpart-only brief and seals its exact contents in
`config/counterpart-brief.json`. Only that brief reaches the simulator. User task,
private constraints and grading criteria are not inputs to the composition function.
Rumik continues to receive only its separately scoped task through the existing
authenticated callback. The model judge sees the saved effective counterpart brief.

## Conditional behavior and event conflicts

The bounded fallback policy tells the counterpart to use only assigned facts,
received audio and permitted tool results. Unknown information stays unknown.
Corrections and refusals persist; changed terms require fresh confirmation.
Style never overrides business rules or a declared challenge. Completion requires
an evidenced outcome, appropriate refusal or explicit ending request.

These semantic rules are prompt instructions, not a deterministic natural-language
state machine. The runtime does not claim to recognize every repeated question or
prove that a fallback was obeyed. That remains simulator-validity review.

Existing conditional events still trigger on successful tool operations and
prerequisites. Replayed operations do not retrigger them. Each declared event is
queued once. A new scenario policy rejects competing pending events by default;
such a conflict is a simulator failure, not a target failure. It never silently
drops a challenge or combines two into one response.

Advanced authored cases may explicitly select `event_conflicts: priority_order`.
Higher numeric `priority` runs first, with stable order for ties. The default
maximum is four pending events; overflow stops the simulator. Priority ordering
does not establish that a deferred challenge remains contextually suitable. Use
separate triggers when ordering matters, and review actual delivery. Legacy cases
without a policy retain their existing queue behavior.

An event request or generated audio is not delivery proof. Existing playback,
overlap and content-review checks remain necessary. A missing challenge remains
untested for that capability and does not by itself fail the booking task.

## Metric definitions and verdicts

Prepared cases freeze the `restaurant-status-v1` rubric in `evaluation_rubric`.
Every definition specifies its method, responsibility, applicability, evidence
requirements, passing behavior and missing-evidence rule. Undefined required
metrics and mismatches between the rubric and existing required metrics are rejected.

| Responsibility | Effect |
| --- | --- |
| Requirement | A supported failure fails a valid task; all must pass for success |
| Validity | Simulator failure invalidates the test; missing review leaves validity unresolved |
| Prerequisite | Task-delivery proof is needed before attributing a task outcome |
| Diagnostic | Reported separately; does not decide task success |

The initial catalog covers existing state, authorization, duplicate-operation,
reservation history, confirmation, negotiation, dietary, language, simulator and
user-report checks. Negotiation and dietary checks are explicitly not applicable
when the source case does not require them. No numerical score or latency threshold
has been invented. The current catalog uses `met`, `not_met`, `uncertain` and
`not_applicable`.

Missing measurements or required citations remain uncertain. A required applicable
metric cannot be skipped by returning `not_applicable`. Human/listening checks
cannot be resolved by a text model alone. Valid target-side drops remain failures.
An already observed, supported target failure can fail a valid test even when a
different task check is uncertain; uncertainty alone cannot become failure.

Evaluation output includes `rubric_version` and a decision/reason for every declared
metric. Human review imports must agree with the frozen rubric as well as the
existing restaurant evidence rules. The native user report still requires a pointer
into sealed provider evidence; harness summaries and call transcripts cannot replace it.
Review never edits raw evidence. Batch JSON and CSV include case version, profile,
rubric version and individual metric decisions.

## Verification and remaining work

Synthetic tests exercise role isolation, source preservation, event conflicts,
priority and queue bounds, missing-evidence handling, applicability, simulator
invalidity, actual simulator request construction, and the saved-evaluation/human-
review path. They do not establish live counterpart compliance or provider behavior.

Controlled noise mixing, qualified accent/speech-speed profiles, a human-labeled
grader calibration collection and aggregate coverage comparisons remain later
work. Existing audio capture and tool/state assertions are reused. This change
adds no dashboard, dependency or provider service and authorizes no live runs.
