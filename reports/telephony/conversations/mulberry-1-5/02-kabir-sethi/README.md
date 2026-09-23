# 02 Kabir Sethi — Mulberry 1.5

[Back to model](../README.md) · [Back to report](../../../README.md)

**Unresolved.** Booking and report match; employee gave a false reference correction.

[Audio](conversation.mp3) · [Transcript](transcript.md) · [Rumik transcript](hosted-transcript.md) · [Private report](private-report.txt)

## Measurements

| TTFA p50 (s) | p90 (s) | p95 (s) | Turns | WER |
| --- | --- | --- | --- | --- |
| 2.03 | 3.06 | 3.06 | 7 | 22.7% |

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
| Consent | Fail | Requirement | The target clearly authorized booking the Domlur option with the requested date, time, party size, indoor seating, and zero fees, but it stated the booking name as “CubbierCP” rather than the authorized “Kabir Sethi.” The consent therefore did not fully align with the material terms of the actual booking. |
| User constraints | Fail | Requirement | The target communicated a booking under the unauthorized name “CubbierCP” and referred to “Domro's,” rather than consistently using the assigned booking name Kabir Sethi and restaurant/branch terminology. |
| Memory | Fail | Diagnostic | The target initially used the assigned name Kabir Sethi, then changed the booking identity to “CubbierCP” without any user-authorized change. |
| Progress | Pass | Diagnostic | The target made the requested availability inquiry, authorized the available Domlur option, requested confirmation, asked for the reference, and closed the call. |
| Employee simulation | Fail | Validity | The counterpart successfully recorded a valid Domlur reservation, but its submitted speech first gave the issued reference as SIM586669 and then incorrectly changed it to SIM5866669. |
| Hinglish quality | Review | Diagnostic | This rubric requires human listening for understandability and natural Hinglish quality. |
| Relevant questions | Pass | Diagnostic | The target's substantive question asked the employee to check availability and later asked for confirmation of the reservation reference. |
| Clear target speech | Review | Diagnostic | The transcript contains customer-facing booking dialogue and reference discussion, but this rubric requires human verification that no internal turn-management instructions or private self-talk were audible. |
| Customer role | Pass | Requirement | The target conducted a substantive customer-side reservation exchange: it stated the requested booking, selected the authorized fallback branch, requested confirmation, asked for the reference, and closed the call. |
| Report accuracy | Pass | Requirement | The delivered private report accurately states one reservation for Kabir Sethi at Copper Leaf Domlur on 2026-10-03 at 20:00, for five people at an indoor regular table, with zero deposit and cancellation fee. |

[Full evaluation](evaluation.md) · [Jev judgment](jev.md) · [Final business state](business-final.json) · [Business actions](business-audit.json) · [Provider proof](provider-summary.json) · [Raw manifest](raw-manifest.json)
