# 01 Aditi Shah — Mulberry 1.5

**Unresolved.** Booking saved, but employee conversation and reference loop were invalid.

[Audio](conversation.mp3) · [Transcript](transcript.md) · [Rumik transcript](hosted-transcript.md) · [Private report](private-report.txt)

## Measurements

| TTFA p50 (s) | p90 (s) | p95 (s) | Turns | WER |
| --- | --- | --- | --- | --- |
| 2.22 | 6.01 | 6.01 | 8 | 36.9% |

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
| Consent | Pass | Requirement | The target clearly requests booking the stated reservation and explicitly asks for booking without charge or deposit. |
| User constraints | Fail | Requirement | The target's spoken request uses a name transcribed as “पितिशा,” rather than the authorized booking name Aditi Shah. |
| Memory | Fail | Diagnostic | After stating the reservation request, the target abandons the restaurant-booking context and spends the remainder of its captured speech discussing and repeating a reference number. |
| Progress | Fail | Diagnostic | The exchange does not progress through a coherent reservation decision. |
| Employee simulation | Fail | Validity | The counterpart's captured speech is not a coherent reservation-employee response: it repeats the caller's request, produces garbled reference-number dialogue, and appears to assert confirmation without clearly communicating the accepted terms. |
| Hinglish quality | Review | Diagnostic | This rubric requires human listening for understandability and naturalness. |
| Relevant questions | Fail | Diagnostic | The target's later questions are about adding and reconciling a reference number rather than helping complete the assigned reservation. |
| Clear target speech | Review | Diagnostic | Determining whether the audible output contains internal turn-management instructions or private self-talk requires human listening. |
| Customer role | Fail | Requirement | The target initially acts as a customer requesting a reservation, but then shifts into a prolonged reference-number discussion rather than maintaining a coherent customer-assistant booking exchange. |
| Report accuracy | Pass | Requirement | The latest accepted report accurately states the booked date, time, branch, party size, seating, booking name, no reservation charge and the issued reference in a hyphenated form that matches the issued reference under the supplied normalization. |

[Full evaluation](evaluation.md) · [Jev judgment](jev.md) · [Final business state](business-final.json) · [Business actions](business-audit.json) · [Provider proof](provider-summary.json) · [Raw manifest](raw-manifest.json)

[Back to report](../../../TELEPHONY_RESULTS.md)
