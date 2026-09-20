# One adapted restaurant case

This pilot prepares one Taskmaster-derived Hinglish conversation. Hosted Rumik
represents the user; the OpenAI counterpart plays the fictional restaurant's
central reservations desk. Execution uses browser audio connected by the harness.
It does not measure Rumik choosing or dialing a telephone destination.

The selected source is Taskmaster-1 conversation
`dlg-00055f4e-4a46-48bf-8d99-4e477663eb23`, instruction `restaurant-table-2`.
The separate adapted package was unavailable: the local case was reconstructed
from the supplied handoff and request. It is not a recovered original package.
The full downloaded source is preserved separately from the adaptation.

## Local inputs and offline preparation

The local working set is indexed in `datasets/README.md`. The authored baseline
is `datasets/authored/restaurant-baseline.json`, its generated execution input is
`datasets/generated/restaurant-baseline.json`, and its original source record and
attribution are in `datasets/sources/taskmaster1/`. The original packages, hashes,
transcript extract and historical handoff documents are preserved under
`datasets/archive/2026-09-20/`. Dataset files must stay out of Git. There is no
fabricated reference conversation or pilot transcript.

The importer verifies the exact source ID, instruction, 20 utterances and Git blob
`21836935dbc399bf5ff5710d53d5326cc2d74ade`. It requires five physical options with
exactly one matching outcome and emits a single schema-2 `ExecutionCase`.
It reads only local files and fails if its output already exists.

```sh
dataset_check_dir=$(mktemp -d)
uv run --locked voice-bench restaurant prepare \
  --case datasets/authored/restaurant-baseline.json \
  --source datasets/sources/taskmaster1/sample.json \
  --output "$dataset_check_dir/baseline.json"

uv run --locked voice-bench restaurant preflight \
  --config configs/restaurant-pilot.local.toml \
  --cases datasets/generated/restaurant-baseline.json
```

The supplied local config has zero funding and cannot start a call. Preflight
lists absent settings without loading `.env`, opening a database, or contacting
providers. It reports live qualification as pending even when fields are filled:
having settings is not proof that the hosted integration works.

## Mock booking and evidence

`mock_restaurant_reservation` version 1 exposes `check_availability(branch)` and
`record_reservation(option_id, booking_name)` only to the counterpart. Rumik gets
no business mutation tools. Each attempt owns independent inventory and bookings.
The mock cannot contact a booking platform or charge money.

Availability returns all unreserved options at the branch. Every listed option
is physically bookable, including options that violate the user's constraints.
The workflow never reads expected outcomes. A wrong booking stays wrong.

Workflow execution now accepts a keyword-only trusted `context`; the business
service supplies actor, attempt and operation identity. Its optional
`observations` argument is populated by the audio worker, never HTTP/model
arguments. Existing workflows may ignore this context.

Before a reservation write, the worker snapshots its own events. The service
requires a completed counterpart audio item, full browser playback evidence, and
a later completed Rumik speech segment with matching provider item IDs. It stores
these anchors with the selected terms and returns an attempt-specific reference.
Repeated operation IDs replay the original result. Reusing a speech segment for
a second booking is rejected. Rejected requests remain in the audit.

**These checks establish observed speech order, not semantic consent.** A human
must listen and verify that the desk read every term and Rumik accepted that exact
option. The latest speech could be a refusal or a different choice; such a saved
booking makes the simulation invalid. No `confirmed: true` model argument is
accepted as evidence. Missing structural anchors prevent the write; an unresolved
semantic check prevents a passing verdict.

Audio references cover the saved played/received recordings. Provider voice
activity times remain labeled as the OpenAI input-buffer clock, not browser
recording offsets. Browser rendering is local playback evidence, not proof of
remote hearing. Audio send and receive remain independent.

## Evaluation and human review

Ordinary `evaluate` remains offline. Reservation checks cover exactly one booking,
all expected terms, every committed action, the harness-issued reference, and
speech/booking evidence links. Earlier wrong commitments cannot be erased by a
correct final record. A correct state alone remains inconclusive.

Use the existing evaluation and review commands from RUNNING.md. Restaurant review
exports additionally include five `checks`: counterpart validity, consent alignment,
constraint behavior, Hinglish quality, and user-report accuracy. Each resolved
check needs an explanation and checksummed artifact citations. Speech checks
require both played and received audio; report accuracy requires the saved provider
record and final booking state. Listen to audio rather than treating text as proof
of language quality. No exact wording, minimum turns, or latency threshold is imposed.

If the saved native Rumik call response contains its actual post-call user report,
set `report_pointer` in the review to the sequence of JSON object keys/list indices
that identifies that report text. For example, a provider field nested under two
objects would be represented by a two-element array. Do not guess provider field
names: inspect the actual saved response. The review copies the identified text
verbatim into its immutable result and checks its provenance against the raw record.
Review its details and reference against the booking; never supply a harness-written
summary, a restaurant utterance, or the whole call transcript as the user report.

There is currently no dedicated native post-call report delivery integration. If
the provider record lacks a real report, leave the pointer empty and the report
check uncertain. That is an integration gap, not proof Rumik failed to report.

A restaurant pass requires all state/evidence checks and all five human checks,
confirmed termination, and an actual provider-native report. Human review cannot
override a deterministic booking mismatch into a pass. A valid observed Rumik
error is a failure. Simulator errors are invalid; missing proof is inconclusive.
The existing `validity` and `outcome` fields remain; restaurant evaluation/review
results also include `verdict` as `pass`, `fail`, `invalid`, or `inconclusive`.

## Live pilot gate

Keep the pilot to one case, one browser attempt, concurrency one, a five-minute
conversation limit, and no deliberate interruptions. The live dispatcher enforces
these limits for this selected case. Existing live validation additionally requires
positive funded limits and component cost ceilings, target/version, model/voice,
credentials, and a public authenticated callback URL.

Complete callback, database and audio setup before running the explicitly live
command in RUNNING.md with this case and `--repetitions 1`. Hosted consumption of
the private user task still needs live qualification; serving the callback alone
does not prove it. No target deployment or account reconfiguration is performed.
Preserve failure evidence and stop after the one attempt; do not automatically retry.

Deliver sealed audio, events, booking audits/state, native report if available, and
versioned evaluation/review. Report planned/attempted/valid/invalid/unresolved/
passed/failed/not-run counts. Do not infer reliability percentages or broader
dataset coverage from this single case. Synthetic tests validate the harness only.

For initial connection qualification under a small spending limit, the duration
cap may be shorter than 300 seconds. Record the actual cap with the run. A short
qualification attempt is not equivalent to a full-duration benchmark; a harness
timeout must not be presented as proof that Rumik cannot complete the task.

## Completion with a private target report

An explicitly versioned run can use `completion = "target_report_then_hangup"`
and grant the target `submit_user_report`. This adds a private output channel for
Rumik's own final text; it does not grant restaurant tools or create a booking.
The restaurant counterpart cannot call or see this tool. The callback authenticates
both the registered call and its frozen target identity, requires task delivery,
and saves the first report unchanged. An identical retry is harmless; a different
replacement or a request after sealing is rejected and retained.

This protocol delivers the report after the restaurant exchange and before native
hangup. It is distinct from the original case's post-call report requirement. Save
it under a new case version, update the report-delivery instruction and rubric,
and keep the expected reservation unchanged. Never relabel old attempts.

The controller continues recording after the counterpart's goodbye, waits for
Rumik's report and then closes the call itself. It records `end_call_requested`,
stops counterpart generation, and allows at most two seconds for queued playback
(less when the configured finalization allowance is shorter). Playback errors or
a stalled queue do not prevent cleanup and provider termination checks.
It retains `target/user-report.json` plus `target/report-requests.json`.
A report can truthfully describe failure; neither report delivery nor hangup
proves a correct reservation. The provider may also hang up, but a missing native
hangup does not prolong a reported task. The configured duration and funded limits
still apply as safety backstops. No report is synthesized by the harness, and no
missing report is filled from the expected answer.

Successful booking tool results include `reference_delivery`, version
`single-reference-readback-v1`. The counterpart must identify the code as one
reference, spell each character including the hyphen, and request a complete
readback before goodbye. This preserves the issued reference and uses only the
counterpart's permitted booking result. The delivery instruction is recorded in
evidence; actual speech and readback compliance still require audio review.

For this protocol, set `criteria.user_report_source` to `target_callback`.
Report-presence evaluation checks the receipt's call, attempt and task binding.
A review may cite `target/user-report.json` and use `report_pointer = ["text"]`.
Accuracy, consent and natural speech still need evidence-backed review; the
original post-call protocol continues to reject dashboard summaries and restaurant
transcripts as user reports.
