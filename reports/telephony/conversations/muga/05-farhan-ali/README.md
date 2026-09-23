# 05 Farhan Ali — Muga

[Back to model](../README.md) · [Back to report](../../../README.md)

**Unresolved.** Booking saved; employee gave inconsistent reference numbers.

[Audio](conversation.mp3) · [Transcript](transcript.md) · [Rumik transcript](hosted-transcript.md) · [Private report](private-report.txt)

## Measurements

| TTFA p50 (s) | p90 (s) | p95 (s) | Turns | WER |
| --- | --- | --- | --- | --- |
| 2.08 | 3.24 | 3.24 | 7 | 36.4% |

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
| Correct reference number | Review | Supporting | Compared only explicitly labelled target report references using explicit-reference-clauses-v2. |
| Report delivered | Pass | Requirement | Checked authenticated report receipt. |
| Consent | Pass | Requirement | The target explicitly authorized booking the requested unchanged terms: four people, indoor table, Banjara Hills, October 6 at 7 p.m., under Farhan Ali, with zero reservation charge. |
| User constraints | Pass | Requirement | The target requested and accepted terms consistent with the assignment: four guests, indoor table, allowed branch and time, Farhan Ali, and zero reservation charge. |
| Memory | Pass | Diagnostic | The target retained the established party size, name, date, seating, branch, time, and zero-charge requirements and did not unnecessarily re-ask for them. |
| Progress | Pass | Diagnostic | The exchange progressed from availability and booking terms to reservation completion and reference clarification. |
| Employee simulation | Fail | Validity | The employee used the availability, offer, and reservation tools and ultimately recorded the correct booking, but the spoken reference delivery was not a clear, faithful delivery of the single issued reference. |
| Hinglish quality | Review | Diagnostic | This rubric requires human listening to assess understandability and natural Hinglish. |
| Relevant questions | Pass | Diagnostic | The target's substantive questions concern availability, reservation charge, and the exact issued reference. |
| Clear target speech | Review | Diagnostic | This rubric requires verification by human listening to the captured audio for internal turn-management instructions or private self-talk. |
| Customer role | Pass | Requirement | The target acts as the caller/customer assistant: it states the booking request, authorizes the reservation, asks for the charge and reference, corrects the reference, and ends the call. |
| Report accuracy | Fail | Requirement | The latest report correctly states the booking details, seating, party size, date, time, name, branch, and zero reservation charge, but it reports the issued reference as "SIM-92 5680" rather than preserving the single issued reference identity "SIM-925680". |

[Full evaluation](evaluation.md) · [Jev judgment](jev.md) · [Final business state](business-final.json) · [Business actions](business-audit.json) · [Provider proof](provider-summary.json) · [Raw manifest](raw-manifest.json)
