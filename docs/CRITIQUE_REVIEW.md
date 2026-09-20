# Review of the external critique

The critique gets the main conclusion right: the saved work demonstrates useful
integration debugging, not a completed performance benchmark. The core architecture
does not need replacing. The largest problems are the path from evidence to a
judgment, incomplete qualification, and the narrow set of conversations actually run.

This review checked the current source, original saved case and report, event logs,
and sealed evidence. It did not call providers, transcribe audio again, or perform a
human listening review. Seven local evidence bundles passed checksum verification;
five record connected attempts. These are not seven independent benchmark tasks.
The audit is at `reports/critique-audit-20260920/evidence-audit.json`.

## What the other model got right, and what the source changes

| Concern | Finding after inspecting the source | Action or remaining work |
| --- | --- | --- |
| The conversation was too easy to demonstrate broad ability | Fair. One cooperative booking does not establish negotiation, correction, dietary handling, or task-family coverage. | Preserve the baseline. Harder restaurant definitions already exist. Dataset development is separate; no new cases or live coverage were invented here. |
| Reference delivery became more helpful | Fair experimental concern. The current workflow deliberately requests clearer reference delivery and readback. That tests a different condition from target-initiated clarification. | Case, counterpart settings, and source code are already frozen in batch evidence. Compare separately authored conditions in a future dataset version; do not revise historical expectations. |
| Consent rules might be too procedural | A reasonable design question, not an established bug. Stored structural anchors cannot prove semantic agreement. | Keep the historical readback rules. A reviewer must distinguish protocol compliance from whether the parties agreed. Future explicit-versus-contextual confirmation rules belong in authored cases. |
| Browser lifecycle is broken | The reported failures are real, but current code already stops on the private final report and reconciles after media cleanup errors. | Retain those fixes. Current code passed local lifecycle and browser tests. Hosted Rumik qualification remains unproven. |
| Reliability blames the target for harness errors | Confirmed code defect: every execution error previously emitted the same failing call-reliability metric. | Separate execution reliability from target call reliability; export attribution and recorded failure stage. Unknown transport ownership remains unknown. |
| Judges lack aligned conversational evidence | Confirmed. Independent three-minute transcript blocks do not support precise ordering. Browser sample mappings exist, but were not supplied to the judge. | Add bounded, cited audio windows, browser-clock mappings, gaps, and event anchors. Record every future counterpart tool result with its operation identity. This improves navigation and evidence structure; it does not supply word timestamps or resolve old consent. |
| Judges confuse business facts with spoken content | Confirmed risk, including the saved claim about alternatives present only in tool output. | Type evidence categories and require speech-window citations for resolved conversational judgments. A business citation alone is rejected. Citation validation still cannot establish that every sentence follows from its evidence. |
| Shared transcription can mislead multiple judges | Correct. Two judges using the same transcript do not independently verify the audio. | Preserve original transcripts. Listening and versioned corrections remain required. No new transcript or language-quality claim was manufactured. |
| Human review never finished | Correct. The implementation already supported review import/export, but its outputs did not clearly expose pending stages. | Export pending required checks and listening reviews. Legacy restaurant results cannot become completed outcomes solely from model answers. Prepare a listening worksheet with initially unresolved verdicts. |
| Report-reference accuracy needs a stronger check | Confirmed. The saved report asserts two identifiers; the database contains one. | Add a conservative, versioned reference extractor and comparison. Reject model approval that contradicts a recognized mismatch, and prevent a human pass from bypassing it. Other report fields still need review. |
| Evaluation selection and reporting are incomplete | Correct, plus an additional source-level defect: selecting a missing evaluation silently fell back to the execution result. | Missing selected stages now remain explicit and unresolved. Reviews must match both the selected evaluation version and its checksum. No newest-or-most-favorable selection is introduced. |
| Judge validation errors are hard to diagnose | Confirmed. The constrained metric schema and code-resolved citations already existed; safe diagnostics did not. | Save structured validation codes and affected metrics, while retaining rejected responses and excluding provider exception bodies. |
| The grader was developed on the same example | Correct. Repairing a regression is legitimate but is not independent calibration. | Add synthetic reference, missing-evidence, clock-gap, and export regressions using other identifiers. These are software tests, not unseen human-reviewed grader calibration or Rumik performance data. |
| Voice capabilities, telephone, outbound orchestration, and Jev are undemonstrated | Correct scope/proof limitations. The optional Jev integration already exists and does not generate counterpart speech. | Keep these boundaries explicit. Do not add app integrations or run paid shadow evaluations merely to fill a checkbox. |

## Changes and why they matter

**Results must say which stages actually ran.** New reports identify missing selected
evaluations and reviews instead of silently substituting another result. They retain
failure attribution, lifecycle stage, and both pass and failure rate denominators.
A partial review cannot count an unreviewed model answer as completed human review.
Selecting a review whose evaluated bytes have changed is rejected.

**A target failure and a failed experiment are different.** `execution_reliability`
records an execution error. `call_reliability` fails only for explicitly recorded
target attribution. Harness, simulator, or unknown ownership leaves target reliability
uncertain. A valid, attributable target failure remains a failure. The controller now
records the stage where a failure was observed; this is not a claim to know its root
cause. Historical stages are not reconstructed by guessing.

**The judge needs evidence it can cite precisely.** New model evaluations use
`typed-evidence-timeline-v4`. The configurable transcription window defaults to 15
seconds instead of 180. Each window identifies its speaker, recording range, and
capture or playback boundary. Complete browser mappings place the range on the
browser sample clock. Gaps and overlaps are retained. Tool/event observations stay
on their own clocks and are never silently converted into spoken content. The latency
extractor now also rejects missing interior clock mappings; mapping just the two
endpoints of a speech interval is insufficient.

These windows are not utterance timestamps. Shorter chunks can split sentences and
increase request overhead. The setting is saved in the judge configuration, and the
new transcription protocol still needs calibration before comparisons with old
results. Telephone and unmapped audio remain unaligned. A better-shaped input alone
does not prove a more accurate judge.

**Extract what the target actually asserted before comparing it.** The new
`explicit-reference-clauses-v1` check receives only target report text during
extraction. It preserves the supporting text span and the number of asserted codes.
Comparison ignores ASCII case and hyphens only; it never joins two codes. Repeated
codes retain multiplicity. Unsupported wording, corrections, or multiple declaration
clauses remain uncertain. A matching identifier does not prove overall report accuracy.

This is deliberately a narrow English labelled-reference grammar, not a general
multilingual report parser. Branch, date, time, party size, charge, false-success
claims, and ambiguous references still require semantic review. The original report
format and target instructions were not changed to make this check pass.

**Name the experiment before running it.** Configuration now records `purpose` as
`development` (default), `qualification`, or `benchmark`, and includes it in the
frozen configuration. Benchmark dispatch rejects infrastructure fixtures and cases
without explicit evaluation rubrics. Old batches remain `legacy_unspecified`;
a label alone never proves qualification or statistical comparability.

## Saved evidence recheck

A new offline evaluation, `critique-rules-v1`, was written for the full conversation.
It reports execution reliability as not met, target call reliability as uncertain,
and the reported reference comparison as not met. The overall outcome remains
unresolved. All old evaluations, manifests, recordings, and reports were preserved.

The new listening package is at
`reports/critique-audit-20260920/listening-package-v2.json`. It contains source references,
clock-aware windows, event anchors, the explicit reference comparison, and a review
worksheet. It links local recordings; it is not a portable copy or an imported review.
The historical transcript still has its original broad ranges.

To prepare another package without providers:

```sh
voice-bench review package /absolute/path/to/attempt \
  --version existing-evaluation-version --file /absolute/path/to/new-package.json
```

To declare future run and transcription settings in a TOML configuration:

```toml
# Top-level field; save before running the batch.
purpose = "qualification"

[judge]
# Keep the explicitly chosen model, rubric and funding fields as well.
transcription_chunk_seconds = 15
```

## Remaining proof and decisions

1. Qualify the unchanged current browser flow against hosted Rumik under explicitly
   funded limits. Check task consumption, simultaneous audio, report receipt,
   shutdown, and complete evidence together.
2. Listen to the disputed reference and consent exchanges, then assess Hinglish
   quality. Record exact ranges and any transcript corrections separately. Do not
   treat either model's assessment as the listening ground truth.
3. Freeze the evaluator and assess an independently reviewed calibration set.
   Passing the new software regressions does not establish model accuracy.
4. Run the existing harder cases under fixed settings only after qualification.
   Repetitions measure variability within those cases, not general consumer-task
   coverage. A twelve-call pilot would be a diagnostic choice, not a statistical
   guarantee.
5. Qualify telephone separately. Decide whether Jev is required or optional for a
   specific future evaluation plan, and run it explicitly if selected. Its absence
   does not explain speech naturalness.
6. Complete current-source container and worker qualification, actual usage/cost
   accounting, and a portable evidence package if sharing recordings is intended.
   These are still open; no provider activity, deployment, or public upload occurred.

The local validation used Python 3.12 and the existing locked environment, with a
fresh temporary PostgreSQL database and the installed Chromium. Tests block provider
networks and remove provider credentials. Unit/integration checks do not replace
live qualification or human listening. Final check counts are recorded in the task
response after the last code changes: **240 passed, zero skipped**, including the
PostgreSQL and Chromium checks. `ruff check`, `ruff format --check`, and
`git diff --check` passed. Three existing dependency deprecation warnings remain.
The temporary test database was stopped after validation. No dependencies were
changed, no paid calls were made, and no container or hosted-worker proof is claimed.
