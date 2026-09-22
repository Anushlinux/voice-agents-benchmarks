# 09 Sana Khan — Muga

**Failed.** Correctly declined the price; report omitted required task details.

[Audio](conversation.mp3) · [Transcript](transcript.md) · [Rumik transcript](hosted-transcript.md) · [Private report](private-report.txt)

## Measurements

| TTFA p50 (s) | p90 (s) | p95 (s) | Turns | WER |
| --- | --- | --- | --- | --- |
| 2.35 | 2.54 | 2.54 | 3 | 34.9% |

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
| Correct booking name | N/A | Requirement | Required outcome proof |
| Valid booking history | Pass | Requirement | Replayed booking identity, terms, action ownership, reference and structural speech anchors. |
| Correct reference number | Review | Supporting | Compared only explicitly labelled target report references using explicit-reference-clauses-v2. |
| Report delivered | Pass | Requirement | Checked authenticated report receipt. |
| User constraints | Pass | Requirement | Rumik stated the requested date, time, branch, party size, indoor table, package inclusions, booking name, and INR 9,000 ceiling. |
| Memory | Pass | Diagnostic | Rumik carried forward the material date, time, party size, seating, package, inclusions, name, and budget, then correctly treated the INR 9,600 price as outside the established limit. |
| Progress | Pass | Diagnostic | The exchange progressed from a complete availability request to a price-based refusal and an invitation to consider alternatives. |
| Employee simulation | Pass | Validity | The employee's captured speech accurately presents an indoor regular-table package for six at INR 9,600 with the requested inclusions and does not claim that the booking was made. |
| Hinglish quality | Review | Diagnostic | This rubric requires human listening for understandability and naturalness. |
| Relevant questions | Pass | Diagnostic | Rumik asks for availability on the assigned terms, explains why the offered INR 9,600 option cannot be accepted, and asks about alternatives or flexibility. |
| Clear target speech | Review | Diagnostic | The available transcript contains customer-facing conversation and no textual internal instructions or self-talk, but this is a human-listening rubric and the transcript cannot verify what was audibly output. |
| Customer role | Pass | Requirement | Rumik consistently acts as the customer's assistant: it presents the user's reservation request, applies the user's price ceiling, refuses the over-budget booking, and discusses alternatives. |
| Report accuracy | Fail | Requirement | The report correctly states that no booking was made and that the available INR 9,600 package exceeded the INR 9,000 limit. |
| Consent | N/A | Requirement | Review the actual conversation and outcome |

[Full evaluation](evaluation.md) · [Jev judgment](jev.md) · [Final business state](business-final.json) · [Business actions](business-audit.json) · [Provider proof](provider-summary.json) · [Raw manifest](raw-manifest.json)

[Back to report](../../../TELEPHONY_RESULTS.md)
