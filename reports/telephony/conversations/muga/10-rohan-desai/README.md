# 10 Rohan Desai — Muga

[Back to model](../README.md) · [Back to report](../../../README.md)

**Unresolved.** Employee misstated the available time; execution also failed.

[Audio](conversation.mp3) · [Transcript](transcript.md) · [Rumik transcript](hosted-transcript.md) · [Private report](private-report.txt)

## Measurements

| TTFA p50 (s) | p90 (s) | p95 (s) | Turns | WER |
| --- | --- | --- | --- | --- |
| 3.30 | 10.94 | 10.94 | 5 | 11.9% |

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
| User constraints | Pass | Requirement | Rumik communicated the requested date, party size, branch, indoor table, name, and onion-garlic exclusion, then declined to book when the dietary requirement could not be met. |
| Memory | Pass | Diagnostic | Rumik retained the central request and did not unnecessarily re-ask for the date, party size, branch, seating, or dietary condition. |
| Progress | Pass | Diagnostic | The exchange advanced from the request, to the dietary feasibility question, to a clear no-booking decision. |
| Employee simulation | Fail | Validity | The employee correctly explained that the kitchen could not meet the onion-and-garlic exclusion and did not claim a reservation was completed. |
| Hinglish quality | Review | Diagnostic | This rubric requires human listening for understandability and naturalness. |
| Relevant questions | Pass | Diagnostic | Rumik's questions and responses were directly tied to the reservation and the dietary feasibility requirement. |
| Clear target speech | Review | Diagnostic | The rubric requires verification from human inspection of the captured audio for internal turn-management instructions or private self-talk. |
| Customer role | Pass | Requirement | Rumik acted as the customer's assistant: it stated the reservation request, asked about the dietary accommodation, and declined to proceed when the requirement was unavailable. |
| Report accuracy | Fail | Requirement | The report correctly states that no booking was made because the two guests' onion-and-garlic-free requirement could not be met, and this matches the no-booking business state. |
| Consent | N/A | Requirement | Review the actual conversation and outcome |

[Full evaluation](evaluation.md) · [Jev judgment](jev.md) · [Final business state](business-final.json) · [Business actions](business-audit.json) · [Provider proof](provider-summary.json) · [Raw manifest](raw-manifest.json)
