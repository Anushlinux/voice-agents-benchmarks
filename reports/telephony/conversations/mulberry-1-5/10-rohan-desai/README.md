# 10 Rohan Desai — Mulberry 1.5

[Back to model](../README.md) · [Back to report](../../../README.md)

**Unresolved.** Correct no-booking decision and report; execution failure remains unresolved.

[Audio](conversation.mp3) · [Transcript](transcript.md) · [Rumik transcript](hosted-transcript.md) · [Private report](private-report.txt)

## Measurements

| TTFA p50 (s) | p90 (s) | p95 (s) | Turns | WER |
| --- | --- | --- | --- | --- |
| 1.82 | 2.22 | 2.22 | 3 | — |

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
| Correct booking name | N/A | Requirement | Required outcome proof |
| Valid booking history | Pass | Requirement | Replayed booking identity, terms, action ownership, reference and structural speech anchors. |
| Correct reference number | Review | Supporting | Compared only explicitly labelled target report references using explicit-reference-clauses-v2. |
| Report delivered | Pass | Requirement | Checked authenticated report receipt. |
| User constraints | Pass | Requirement | Rumik communicated the requested reservation and, after the dietary limitation was stated, did not book or make any unauthorized commitment. |
| Memory | Pass | Diagnostic | Rumik retained and used the relevant party, booking-name, seating, and dietary requirements, then responded to the employee's answer without repeating an already settled question or losing the task context. |
| Progress | Pass | Diagnostic | The exchange progressed from the request, to the employee's dietary limitation, to Rumik's decision not to book and a natural close. |
| Employee simulation | Pass | Validity | The employee answered the received dietary question truthfully, explained that the kitchen could not provide the required onion-and-garlic-free food, and did not claim a reservation or unsupported concession. |
| Hinglish quality | Review | Diagnostic | The captured text suggests a natural Hindi-English exchange, but this rubric requires human listening and text/transcription alone cannot establish understandability or natural delivery. |
| Relevant questions | Pass | Diagnostic | Rumik's request directly addressed the assigned reservation and dietary feasibility. |
| Clear target speech | Review | Diagnostic | The transcript contains only customer-facing reservation conversation and no apparent internal instructions, but this diagnostic requires verification from the captured audio by human listening; text alone is insufficient. |
| Customer role | Pass | Requirement | Rumik acted as the customer's assistant: it requested a table reservation, supplied the booking name and dietary requirement, and declined booking when the requirement could not be met. |
| Report accuracy | Pass | Requirement | The authenticated report accurately states that no booking was made and gives the known blocker: the kitchen could not provide onion-and-garlic-free meals for the two guests. |
| Consent | N/A | Requirement | Review the actual conversation and outcome |

[Full evaluation](evaluation.md) · [Jev judgment](jev.md) · [Final business state](business-final.json) · [Business actions](business-audit.json) · [Provider proof](provider-summary.json) · [Raw manifest](raw-manifest.json)
