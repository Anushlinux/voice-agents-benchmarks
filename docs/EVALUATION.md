# Evidence and evaluation contract

## Main rule

The caller reacts to audio it receives. The evaluator checks observable actions
and outcomes. A fluent transcript or spoken success claim does not prove success.

## Evidence layout to implement

```text
artifacts/<batch_id>/<run_id>/
  manifest.json
  config/                    # target, tools, variables, caller and grading snapshots
  audio/                     # source, sent and received audio, clearly labeled
  events.jsonl               # append-only events, named clocks and sequence numbers
  business/                  # initial state, tool audit and final state
  provider/                  # available call records, transcript and recordings
  evaluation/<version>/      # derived grades; never overwrite raw evidence
  review/                    # human decisions, evidence references and disagreement
```

This is a proposed storage layout, not a generated run. Local artifacts are
ignored by Git. Future cloud artifacts use stable object keys and checksums.
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
| Reliability | Connection failures, drops, premature endings, one-way audio | Caller, carrier and target events |
| Test quality | Caller validity, missing evidence, judge errors | Caller decisions, recordings and human review |

No composite score, pass threshold, latency target or weighting is agreed yet.
Correct alternative paths must be accepted; do not require an exact tool sequence
unless ordering itself is a business rule.

## Timing

Primary response gap: end of delivered caller speech to beginning of received
target speech. Browser media clocks, carrier clocks and process monotonic clocks
are separate. Record their identity and uncertainty instead of subtracting
unrelated timestamps. Never call queued speech "delivered" without evidence.

Report caller processing separately. Carrier playback acknowledgments are useful
but their receipt time is not exact remote playout. Separate overlap turns from
ordinary response gaps, and report no-response turns alongside percentiles.
Internal target time-to-first-token is unavailable unless adequate telemetry exists.

## Grading

1. Code checks verify state, actions, ordering and measurable timing.
2. Model assessments use explicit rubrics and evidence references, and may abstain.
3. Human review checks apparent passes and failures, plus simulator validity.

The `MetricResult` contract requires evidence for resolved verdicts; the later
grader must also verify that the cited artifacts exist and support the claim.
Audio qualities cannot be inferred from text alone. Keep false passes, false
failures and unresolved review disagreements visible.

## Accounting

Record planned, attempted, connected, valid, invalid, unresolved, passed and failed
counts. These are not all disjoint categories: e.g. connected is a subset of
attempted. Define the denominator beside every reported rate.

Keep test validity separate from failure attribution (target, simulator, harness,
unknown). A target-side drop in a valid test remains a failure. A caller that
changes its assigned facts can invalidate a test. Unclear evidence stays unclear.

Show success among valid attempts and, if useful, success conditional on valid
connection. Do not use the conditional figure to hide connection failures.
Preserve every retry. Repetitions share a case and are not independent coverage;
respect that grouping in uncertainty estimates and channel comparisons.
