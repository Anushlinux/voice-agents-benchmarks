# Evidence and evaluation contract

## Role-specific evidence

Schema 2 gives the evaluator the user's request, facts, constraints and permissions separately from the counterpart's role, facts and business rules. Evaluate Rumik against the user's interests and authorization. Check a business-side booking through the counterpart's committed action and final state. Do not require Rumik to call a business-owned mutation directly.

Audits carry `actor`: `target`, `counterpart`, or `harness` for local controls. `policy_actions` checks forbidden target attempts; `counterpart_actions` invalidates tests with forbidden counterpart attempts. Duplicate detection includes actor identity. Spoken consent, negotiation limits and whether an action followed the conversation still need explicit rubrics and model/human review. Tool authorization alone cannot establish those facts.

`target/task-delivery.json` proves the authenticated harness callback served the task, not that the hosted agent understood or followed it. Missing delivery evidence cannot produce a schema-2 non-fixture pass. Outbound initiation, several-call tasks and app actions are not inferred from single-call evidence. Reports label the tested scope.

The judge uses `counterpart_validity` for schema 2. Old sealed cases remain readable under their original business-agent roles and `caller_validity`; do not silently reinterpret historical results. Legacy `caller` event/timing names refer to the counterpart for new cases.

## Main rule

The counterpart reacts to received audio and its role-permitted tool results. Rumik is evaluated as the user's assistant. The evaluator checks observable actions
and outcomes. A fluent transcript or spoken success claim does not prove success.

## Implemented evidence layout

```text
artifacts/<batch_id>/<run_id>/
  manifest.json
  config/                    # target, tools, variables, counterpart and grading snapshots
  audio/                     # source, sent and received audio, clearly labeled
  events.jsonl               # append-only events, named clocks and sequence numbers
  business/                  # initial state, tool audit and final state
  provider/                  # available call records, transcript and recordings
  evaluation/<version>/      # derived grades; never overwrite raw evidence
  review/                    # human decisions, evidence references and disagreement
```

The local fixture and controller write this layout. Batch-level frozen settings and completion/finalization records sit above attempt directories. Local artifacts are ignored by Git. Explicit S3 uploads use stable object keys, conditional writes and checksums.
Never preserve only an expiring recording link.

## Metrics

| Group | Measurements | Required evidence |
| --- | --- | --- |
| Task | Correct permitted outcome, appropriate refusal/escalation | Final state and action trace; audio where communication is part of success |
| Policy/actions | Forbidden attempts, incorrect records/arguments, duplicates | All tool requests/results, including rejected requests |
| Understanding | Entity use, necessary clarification, correction recovery | Delivered audio and subsequent actions |
| Conversation | Relevance, consistency, accurate explanations | Audio-backed transcript and explicit rubric |
| Audio | Intelligibility, interruption, pauses, overlap and recovery | Actual received audio and playback evidence |
| Timing | Setup, greeting, response gap, substantive reply, interruption stop | Defined boundaries on aligned media clocks |
| Reliability | Connection failures, drops, premature endings, one-way audio | Counterpart, carrier and target events |
| Test quality | Counterpart validity, missing evidence, judge errors | Counterpart decisions, recordings and human review |

No composite score, pass threshold, latency target or weighting is agreed yet.
Correct alternative paths must be accepted; do not require an exact tool sequence
unless ordering itself is a business rule.

## Timing

Primary response gap: end of delivered counterpart speech to beginning of received
target speech. Browser media clocks, carrier clocks and process monotonic clocks
are separate. Record their identity and uncertainty instead of subtracting
unrelated timestamps. Never call queued speech "delivered" without evidence.

Report counterpart processing separately. Carrier playback acknowledgments are useful
but their receipt time is not exact remote playout. Separate overlap turns from
ordinary response gaps, and report no-response turns alongside percentiles.
Internal target time-to-first-token is unavailable unless adequate telemetry exists.

## Grading

1. Code checks verify state, actions, ordering and measurable timing.
2. Model assessments use explicit rubrics and evidence references, and may abstain.
3. Human review checks apparent passes and failures, plus simulator validity.

The `MetricResult` contract requires evidence for resolved verdicts; the implemented
grader also checks artifact hashes, event identifiers and audio ranges. Whether a citation supports the interpretation remains part of judge/human validation.
Audio qualities cannot be inferred from text alone. Keep false passes, false
failures and unresolved review disagreements visible.

## Accounting

Record planned, attempted, connected, valid, invalid, unresolved, passed and failed
counts. These are not all disjoint categories: e.g. connected is a subset of
attempted. Define the denominator beside every reported rate.

Keep test validity separate from failure attribution (target, simulator, harness,
unknown). A target-side drop in a valid test remains a failure. A counterpart that
changes its assigned facts can invalidate a test. Unclear evidence stays unclear.

Show success among valid attempts and, if useful, success conditional on valid
connection. Do not use the conditional figure to hide connection failures.
Preserve every retry. Repetitions share a case and are not independent coverage;
respect that grouping in uncertainty estimates and channel comparisons.

## Current timing implementation

The offline timing function uses 20 ms root-mean-square energy windows and an explicit threshold. This is a simple reproducible speech-boundary estimate, not a human-validated speech detector. Browser recording offsets map onto one audio-context sample clock. Ordinary response gaps, overlapping segments and unanswered segments are reported separately with their observation boundary. Carrier playback acknowledgments are retained but are not converted into exact remote-playback timing. Missing clock mappings produce an uncertain result.

Human review remains required for intelligibility, whether an interruption was appropriate, and whether speech recovery sounded natural. No text-only quality score is presented as a listening result.

Counterpart turnaround is reported separately as observed voice-activity stop to first generated audio. Both observations must share a worker clock. This includes network and provider processing and is not internal target latency.
