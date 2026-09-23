# Four restaurant cases: baseline plus three challenges

**September 21 repair:** tool-count speech challenges described below are now
audit-only and rejected by live execution. Use the [current running guide](RUNNING.md)
for new calls. Historical definitions and evidence are preserved.

The original reconstructed booking case is unchanged. Three authored variants add
negotiation, dietary requirements and opportunities for Rumik to correct the
restaurant while it is speaking. Rumik represents Riya; OpenAI plays the restaurant
employee. There is no third participant. These are four cases in one task family,
not evidence of delivery, ride booking, District operation or multi-call capability.

All businesses, inventory, prices and operational rules are fictional. The source
is the same Taskmaster-1 record documented in [the baseline guide](RESTAURANT_PILOT.md).
The source contributes the preferred-restaurant failure and fallback structure.
The Indian setting, shared desk, one-table rule and all challenge events are
adaptations. The local package preserves the original transcript, source bytes,
CC BY 4.0 attribution and baseline unchanged. The original separately authored
single-case package was unavailable; that baseline was reconstructed from the
supplied request and handoff. The new variants are newly authored extensions.

## Cases and private information

All cases request eight people at 19:00 Asia/Kolkata on 25 September 2026, one
regular table, Bandra first then Khar if necessary. All five physical inventory
options are preserved. Matching availability must be disclosed directly.

| Case suffix | Customer assignment | Restaurant challenge |
| --- | --- | --- |
| `001` | Original free reservation | Bandra unavailable; authorized Khar fallback |
| `001_hard_1` | Same constraints; correct inaccurate readbacks | Time misread, then seating misread during a later confirmation |
| `001_hard_2` | Dining package at most INR 12,000 including all charges; no payment authority | INR 13,200 opening offer; negotiation allowed to INR 12,000; time misread after agreement |
| `001_hard_3` | Same price cap; two guests need food without both onion and garlic | Negotiation, dietary clarification, seating misread, brief birthday question |

Rumik receives only `user_task`: the customer's request, facts, constraints and
permissions. It receives neither event definitions nor restaurant pricing policy.
OpenAI receives its counterpart brief, inventory and restaurant policy, its own
tools and the audio received from Rumik. It receives no private customer spending
ceiling or grading answer. Learning a budget from Rumik's speech is allowed.
Only the evaluator receives the full case and expected outcomes.

Dataset briefs and challenge instructions are written in English. Each Rumik
request explicitly requires natural Hinglish speech during the call; the dataset
text itself does not need to be in Hinglish. The restaurant also retains its
Hinglish speaking instruction. No reference dialogue is supplied or replayed.
The dietary event acknowledges already-clear exclusions instead of asking the
caller to repeat them. Vegetarian alone does not mean no onion and garlic;
other restrictions sometimes associated with Jain food are not inferred.

## Workflow version 2

The original version-1 free-reservation workflow is unchanged. Version 2 exposes
these tools only to the restaurant:

1. `check_availability` returns physically available branch options.
2. `quote_reservation` creates a quote for an option. The opening dining total is
   separate from the zero reservation charge. Hard 1 has no dining package and
   uses a zero total.
3. `counteroffer` accepts a caller's proposed total within restaurant policy.
4. `set_dietary_requirements` records how many guests need both exclusions.
5. `prepare_confirmation` saves exact current terms and a trusted event cutoff.
6. `record_reservation` accepts the current confirmation ID and saves those terms
   only when later playback and response evidence is present.

Each changed quote gets a new identity and invalidates the prior confirmation.
After a spoken correction or unrelated question, the employee must prepare a new
accurate readback and obtain fresh acceptance. Old acceptance cannot authorize a
new price, seating arrangement, name or dietary requirement. Quote history,
confirmations, rejected actions and idempotent replays remain in the audit.
Attempt identity, operation identity and reservation references come from the
harness. Attempts have independent state. No payment, cancellation, correction
or external booking integration is added.

Business rules do not enforce the evaluator's preferred answer. For example, the
INR 13,200 opening quote can be booked physically. If Rumik authorizes it, the
saved mistake remains visible to grading. The same applies to wrong times,
bar seats or split tables. A spoken wrong commitment can fail constraint review
even if it is not saved or a later commitment is correct. A simulator silently
changing what Rumik accepted invalidates the test.

Structural consent checks establish speech order and identity, not meaning.
Human listening must verify a complete accurate readback followed by Rumik's
acceptance of those exact terms. A correction, refusal or answer about birthdays
is not acceptance. A simulator confirmation flag cannot replace this evidence.

## Event scheduling and audio proof

Schema-2 inputs have optional `conversation_events`, defaulting to none. Each has
an ID, trigger tool, occurrence, prerequisite tools, kind, field, permitted spoken
value, instruction and evidence requirements. Occurrences count successful
trigger operations after all prerequisites have succeeded. Replayed operations
do not count twice. The fixture defines:

- Hard 1: first eligible prepared confirmation misreads time; second misreads seating.
- Hard 2: first prepared confirmation after availability and counteroffer misreads time.
- Hard 3: first quote after availability clarifies dietary meaning; first prepared
  confirmation after negotiation and dietary accommodation misreads seating;
  second briefly asks about birthdays. A later readback must be accurate.

The worker requests the event for one response using response metadata, then
links the echoed response ID to generated audio item IDs and actual browser
playback. This metadata support is unit-tested with the installed SDK contract;
its behavior against the hosted service still needs live qualification. A request
or a generated transcript is never proof that the mistake was spoken.

Audio sending and receiving stay simultaneous. The timed OpenAI-interrupts-Rumik
setting is disabled. Rumik chooses when to speak; the harness does not inject a
correction or demand a particular response. The employee yields to received speech.

Offline observation measures non-silent overlap from recorded played/received
WAV tracks mapped to the named browser audio clock. It reports overlap duration,
playback cancellation and the last rendered sample time. Missing audio mappings
leave overlap uncertain. The RMS detector is a coarse speech-activity measure:
noise can trigger it, so a human must confirm that the overlapping sound was a
relevant Rumik correction, the intended mistake was audible, playback stopped
appropriately and the conversation resumed with correct terms. Provider clocks
are never treated as browser timestamps.

A delivered challenge without overlapping speech reports `interruption_not_observed`.
A missing or unverified spoken challenge reports `untested`. Neither by itself
fails task completion. `interruption_demonstrated` requires captured overlap and
a listening review confirming delivery, correction and resumption.

## Evaluation and reports

Versioned evaluation and review files retain existing validity/outcome fields and
also report pass/fail/invalid/inconclusive. They contain separate `dimensions` for
task completion, constraint preservation, negotiation, dietary requirements,
Hinglish quality, simulator validity and interruption behavior. Batch JSON and CSV
retain those dimensions and per-event details. No single composite score hides a
missing interruption opportunity.

State checks compare complete booking terms, all committed bookings, quote and
confirmation history, fresh consent anchors and the harness-issued reference.
Human checks inspect Bandra-first behavior, all spoken commitments, negotiation,
dietary understanding, consent, simulator validity and natural Hinglish. Review
export includes one evidence-backed entry per planned conversation event.

Actual native Rumik post-call report evidence remains required. There is still no
dedicated native report-delivery integration. Review may identify an actual report
inside the sealed provider response; it cannot substitute a harness-written
summary, booking state or transcript. Missing report proof remains inconclusive.
A valid interaction demonstrating a Rumik error is a failure. Simulator or
infrastructure compromise is invalid. Missing or unresolved proof is inconclusive.

## Local preparation and execution gates

The local working set is indexed in `datasets/README.md`. The three authored
specifications are in `datasets/authored/restaurant-challenges.json`; their
execution inputs are in `datasets/generated/restaurant-challenges.json`. The
baseline has its own authored and generated files. Original packages, the combined
catalog, profile expansions, plans and validation records are preserved under
`datasets/archive/2026-09-20/`. Dataset files must stay out of Git.

These remain three variants of one restaurant task, not broad personal-assistant
coverage. See `datasets/REVIEW.md` for the review and
`datasets/proposed/indian-assistant-v2.md` for non-executable new designs. Run the
baseline and challenges separately so they retain their five- and ten-minute
limits, respectively. Use one attempt per selected case and concurrency one.

```sh
dataset_check_dir=$(mktemp -d)
uv run --locked voice-bench restaurant prepare-hard \
  --baseline datasets/generated/restaurant-baseline.json \
  --variants datasets/authored/restaurant-challenges.json \
  --output "$dataset_check_dir/challenges.json"

uv run --locked voice-bench restaurant preflight \
  --config configs/restaurant-hard.local.toml \
  --cases datasets/generated/restaurant-challenges.json

uv run --locked voice-bench batch plan \
  --config configs/restaurant-hard.local.toml \
  --cases datasets/generated/restaurant-challenges.json --repetitions 1
```

Preparation, preflight and planning make no provider calls. Outputs cannot be
overwritten through the preparation command. Both local configs have zero funding.
Live execution additionally needs the intended deployed target/version, model and
voice, fixed event and grading versions, authenticated callback connectivity,
database, funded limits, verified task consumption and an explicitly requested run.
Do not start a substitute run when these are absent. Preserve all failed-attempt
artifacts and do not silently retry.

Synthetic unit interactions and synthetic WAV tones validate harness mechanics;
they are neither extra datapoints nor live benchmark results. This design borrows
explicit business rules/tools and state-based evaluation from
[τ-bench task evaluation](https://github.com/sierra-research/tau2-bench/blob/main/docs/evaluation.md),
and separates task difficulty from interaction difficulty as in its
[voice framework](https://github.com/sierra-research/tau2-bench/blob/main/src/tau2/voice/README.md).
It does not import those datasets or claim identical metrics or coverage.
