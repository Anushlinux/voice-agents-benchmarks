# 07 Devika Rao — Mulberry 1.5

[Back to model](../README.md) · [Back to report](../../../README.md)

**Unresolved.** Employee booked without clear consent; simulation invalid.

[Audio](conversation.mp3) · [Transcript](transcript.md) · [Rumik transcript](hosted-transcript.md) · [Private report](private-report.txt)

## Measurements

| TTFA p50 (s) | p90 (s) | p95 (s) | Turns | WER |
| --- | --- | --- | --- | --- |
| 2.04 | 5.34 | 5.34 | 6 | 46.3% |

[TTFA proof](ttfa.json) · [WER proof](wer.md)

## Metric results

Pass / Fail = saved check result. Review = unresolved; N/A = not applicable. Diagnostic checks do not decide the overall result.

| Metric | Result | Role | Evidence / reason |
| --- | --- | --- | --- |
| Employee tools used correctly | Pass | Validity | Found 0 forbidden counterpart action attempts. |
| Task delivered | Pass | Prerequisite | The authenticated before-call response served the user's task to Rumik. |
| Allowed actions only | Pass | Requirement | Found 0 forbidden action attempts. |
| No duplicate bookings | Pass | Requirement | Checked committed operation identities. |
| Correct final booking state | Pass | Requirement | Checked the declared booking or no-booking outcome and material terms; name identity and spoken authorization are separate checks. |
| Correct booking name | Pass | Requirement | Exact normalized names match; different spelling or script needs semantic review, not an automatic wrong-person verdict. |
| Valid booking history | Pass | Requirement | Replayed booking identity, terms, action ownership, reference and structural speech anchors. |
| Correct reference number | Pass | Supporting | Compared only explicitly labelled target report references using explicit-reference-clauses-v2. |
| Report delivered | Pass | Requirement | Checked authenticated report receipt. |
| Consent | Fail | Requirement | The target did not clearly agree to book the simple package before the counterpart stated that the booking was confirmed. |
| User constraints | Pass | Requirement | The target communicated the assigned date, party size, indoor regular table, one-table requirement, required package inclusions, budget ceiling, and no-advance condition. |
| Memory | Pass | Diagnostic | The target retained and restated the material reservation constraints when discussing the simple package. |
| Progress | Fail | Diagnostic | The exchange does not progress cleanly through a decision. |
| Employee simulation | Fail | Validity | The counterpart disclosed the simple package terms accurately, but it treated the target's non-consensual “seems to fit” statement as authorization and stated that the booking was confirmed. |
| Hinglish quality | Review | Diagnostic | This rubric requires human listening for understandability and naturalness. |
| Relevant questions | Fail | Diagnostic | The target's request for a booking reference is relevant, but the target also emits an unrelated internal-report statement instead of clearly answering the counterpart's booking question. |
| Clear target speech | Review | Diagnostic | The transcript contains apparent internal turn-management or report-related speech, but this diagnostic explicitly requires verification against captured audio by human listening. |
| Customer role | Pass | Requirement | The target acts as the customer's assistant: it states the customer's reservation request and constraints, discusses the simple package, and asks for the booking reference. |
| Report accuracy | Pass | Requirement | The delivered private report accurately states the committed booking's date, party size, branch, indoor regular table, simple package, INR 12,400 total, required inclusions, no advance or deposit, no cancellation fee or extras, booking name, and the single issued reference SIM-880921. |

[Full evaluation](evaluation.md) · [Jev judgment](jev.md) · [Final business state](business-final.json) · [Business actions](business-audit.json) · [Provider proof](provider-summary.json) · [Raw manifest](raw-manifest.json)
