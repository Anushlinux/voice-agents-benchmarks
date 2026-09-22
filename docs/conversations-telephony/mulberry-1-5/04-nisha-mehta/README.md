# 04 Nisha Mehta — Mulberry 1.5

**Unresolved.** Booking saved; report reference is wrong. Jev answer failed validation.

[Audio](conversation.mp3) · [Transcript](transcript.md) · [Rumik transcript](hosted-transcript.md) · [Private report](private-report.txt)

## Measurements

| TTFA p50 (s) | p90 (s) | p95 (s) | Turns | WER |
| --- | --- | --- | --- | --- |
| 2.06 | 2.60 | 2.60 | 7 | 30.6% |

[TTFA proof](ttfa.json) · [WER proof](wer.md)

## Metric results

Pass / Fail = saved check result. Review = unresolved; N/A = not applicable. Diagnostic checks do not decide the overall result.

| Metric | Result | Role | Evidence / reason |
| --- | --- | --- | --- |
| Employee tools used correctly | Pass | Validity | Found 0 forbidden counterpart action attempts. |
| Task delivered | Pass | Prerequisite | The authenticated before-call response served the user's task to Rumik. |
| Allowed actions only | Pass | Requirement | Found 0 forbidden action attempts. |
| No duplicate bookings | Pass | Requirement | Checked committed operation identities. |
| Execution completed | Fail | Supporting | Execution failed; recorded owner: unknown. |
| Call reliability | Review | Supporting | Target call failure is established only by target attribution; recorded owner is unknown. |
| Correct final booking state | Pass | Requirement | Checked the declared booking or no-booking outcome and material terms; name identity and spoken authorization are separate checks. |
| Correct booking name | Pass | Requirement | Exact normalized names match; different spelling or script needs semantic review, not an automatic wrong-person verdict. |
| Valid booking history | Pass | Requirement | Replayed booking identity, terms, action ownership, reference and structural speech anchors. |
| Correct reference number | Fail | Supporting | Compared only explicitly labelled target report references using explicit-reference-clauses-v2. |
| Report delivered | Pass | Requirement | Checked authenticated report receipt. |
| Consent | Pass | Requirement | The target requested the matching option, then clearly agreed when asked to confirm. |
| User constraints | Pass | Requirement | The target communicated the required date, time, branch, party size, indoor regular seating, single-table request, table-only intent, dietary preference for two guests, and no-charge requirement. |
| Memory | Pass | Diagnostic | The target retained the established booking details. |
| Progress | Pass | Diagnostic | The exchange progressed from the request, to availability and terms, to confirmation, reservation recording, reference correction, and reporting. |
| Employee simulation | Pass | Validity | The employee used the supplied availability and reservation tools, disclosed that the reservation was free and meals would be ordered and paid for separately, recorded two no-onion-and-garlic guests, and saved the accepted reservation only after confirmation. |
| Hinglish quality | Review | Diagnostic | This rubric requires human listening for understandability and naturalness. |
| Relevant questions | Pass | Diagnostic | The target's questions and answers were relevant to booking availability, confirmation, and resolving the reference discrepancy. |
| Clear target speech | Review | Diagnostic | This is a human-listening rubric. |
| Customer role | Pass | Requirement | The target acted as the customer's representative: it stated the restaurant reservation request, answered confirmation prompts, requested the reference, and sought correction of the reference. |
| Report accuracy | Fail | Requirement | The report correctly states the booking details, seating, party size, dietary note, and zero reservation charge, but it reports reference number 7376735. |

[Full evaluation](evaluation.md) · [Jev judgment](jev.md) · [Final business state](business-final.json) · [Business actions](business-audit.json) · [Provider proof](provider-summary.json) · [Raw manifest](raw-manifest.json)

[Back to report](../../../TELEPHONY_RESULTS.md)
