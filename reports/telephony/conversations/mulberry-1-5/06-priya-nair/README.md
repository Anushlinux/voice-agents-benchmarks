# 06 Priya Nair — Mulberry 1.5

[Back to model](../README.md) · [Back to report](../../../README.md)

**Passed.** Correct ₹9,800 booking, consent, name and reference; accurate report.

[Audio](conversation.mp3) · [Transcript](transcript.md) · [Rumik transcript](hosted-transcript.md) · [Private report](private-report.txt)

## Measurements

| TTFA p50 (s) | p90 (s) | p95 (s) | Turns | WER |
| --- | --- | --- | --- | --- |
| 1.86 | 2.54 | 2.54 | 5 | 26.7% |

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
| Consent | Pass | Requirement | The caller explicitly requested confirmation under Priya Nair and then requested the INR 9,800 compact menu booking. |
| User constraints | Pass | Requirement | Rumik communicated the required date, party size, Powai branch, 20:00 time, indoor regular table, dining package, budget ceiling, required inclusions, and prohibition on deposit or cancellation fee. |
| Memory | Pass | Diagnostic | Rumik retained the core request and proceeded with the same date, time, party size, seating, branch, menu constraints, and fee restrictions. |
| Progress | Pass | Diagnostic | The exchange progressed from the request, to availability and menu terms, to booking confirmation, reference clarification, and closure. |
| Employee simulation | Pass | Validity | The employee used the availability, offer, and reservation tools consistently with the supplied restaurant facts. |
| Hinglish quality | Review | Diagnostic | This rubric requires human listening for understandability and naturalness. |
| Relevant questions | Pass | Diagnostic | Rumik's requests and responses were directed to the reservation: it stated the requirements, requested confirmation under the booking name, requested the compact menu and reference, and addressed the reference discrepancy. |
| Clear target speech | Review | Diagnostic | The transcribed target output contains customer-facing reservation conversation and no obvious internal instructions or private self-talk. |
| Customer role | Pass | Requirement | Rumik acted as the caller and customer assistant: it communicated the user's booking request, sought availability and confirmation, clarified the reference, and closed the call. |
| Report accuracy | Pass | Requirement | The delivered report accurately states the committed booking: seven people, 2026-10-07 at 20:00, Cedar Dining Powai, indoor regular table, Priya Nair, compact menu, INR 9,800, required inclusions, no deposit or cancellation fee, and the single issued reference SIM-918149. |

[Full evaluation](evaluation.md) · [Jev judgment](jev.md) · [Final business state](business-final.json) · [Business actions](business-audit.json) · [Provider proof](provider-summary.json) · [Raw manifest](raw-manifest.json)
