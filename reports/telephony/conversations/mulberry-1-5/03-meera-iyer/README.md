# 03 Meera Iyer — Mulberry 1.5

[Back to model](../README.md) · [Back to report](../../../README.md)

**Failed.** Wrong task details spoken; report split one reference into two.

[Audio](conversation.mp3) · [Transcript](transcript.md) · [Rumik transcript](hosted-transcript.md) · [Private report](private-report.txt)

## Measurements

| TTFA p50 (s) | p90 (s) | p95 (s) | Turns | WER |
| --- | --- | --- | --- | --- |
| 2.16 | 2.49 | 2.49 | 3 | 23.5% |

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
| Correct reference number | Fail | Supporting | Compared only explicitly labelled target report references using explicit-reference-clauses-v2. |
| Report delivered | Pass | Requirement | Checked authenticated report receipt. |
| Consent | Pass | Requirement | The target says “जी हाँ” in the exchange, and the counterpart subsequently records the offered 18:45, no-fee table reservation. |
| User constraints | Fail | Requirement | The target’s spoken request changes the assigned restaurant from Banyan Kitchen to Fanning Kitchen, the booking name from Meera Iyer to Mira Iyer, and expresses an ambiguous AM/PM range. |
| Memory | Fail | Diagnostic | The target does not preserve the user-assigned restaurant or booking name: it says “Fanning Kitchen” and “Mira Iyer” rather than using the assigned Banyan Kitchen and Meera Iyer. |
| Progress | Pass | Diagnostic | The exchange progresses from the reservation request to an affirmative response, a booking action, and a closing/readback request. |
| Employee simulation | Pass | Validity | The counterpart uses the availability, offer and record tools, offers a permitted 18:45 Adyar table-only reservation with zero deposit and cancellation fee, and only says it is confirmed after the successful record result. |
| Hinglish quality | Review | Diagnostic | This rubric requires human listening for understandability and natural Hinglish. |
| Relevant questions | Pass | Diagnostic | The target asks for a reservation, supplies the requested booking details, requests the possible time and reference, and ends with a confirmation/readback question. |
| Clear target speech | Review | Diagnostic | The transcript contains customer-facing reservation content and no clear internal turn-management instructions, but this rubric requires verifying the audible output directly. |
| Customer role | Pass | Requirement | The target acts as the caller/customer assistant: it requests a table, states booking constraints, accepts a proposed time, and asks for the reference. |
| Report accuracy | Fail | Requirement | The report correctly states the restaurant, branch, date, time, seating, party size, booking name, and no deposit/cancellation fee, but it reports two reference numbers, “789, 0694,” instead of preserving the single issued reference SIM-890694. |

[Full evaluation](evaluation.md) · [Jev judgment](jev.md) · [Final business state](business-final.json) · [Business actions](business-audit.json) · [Provider proof](provider-summary.json) · [Raw manifest](raw-manifest.json)
