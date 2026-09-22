# 05 Farhan Ali — Mulberry 1.5

**Failed.** Booking saved; report changed SIM-856277 to PIM 856277.

[Audio](conversation.mp3) · [Transcript](transcript.md) · [Rumik transcript](hosted-transcript.md) · [Private report](private-report.txt)

## Measurements

| TTFA p50 (s) | p90 (s) | p95 (s) | Turns | WER |
| --- | --- | --- | --- | --- |
| 2.12 | 4.36 | 4.36 | 4 | 33.0% |

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
| Consent | Pass | Requirement | The caller explicitly requested confirmation of a free indoor regular table for four at the earliest qualifying time, and the recorded offer matched those unchanged material terms. |
| User constraints | Pass | Requirement | The target's request and the recorded outcome preserve the authorized date, party size, allowed branch, indoor regular table, table-only booking, zero reservation charge, and no deposit or fees. |
| Memory | Pass | Diagnostic | The target carried forward the booking name, date, party size, seating, branch/time window, and no-fee table-only constraints rather than unnecessarily asking the caller to restate them. |
| Progress | Pass | Diagnostic | The exchange moved from the caller's request to availability, confirmation, reference handling, and termination without a repeated-question loop. |
| Employee simulation | Pass | Validity | The counterpart used the permitted availability, offer, and recording tools; the saved reservation matches the supplied option, name, and zero-fee terms. |
| Hinglish quality | Review | Diagnostic | This rubric requires human listening for understandability and naturalness. |
| Relevant questions | Pass | Diagnostic | The target asked for the requested reservation, including the relevant date, time, branch, party size, seating, fees, and reference. |
| Clear target speech | Review | Diagnostic | This is a human-listening rubric. |
| Customer role | Fail | Requirement | The target initially states the customer's request appropriately, but later speaks as though it is the restaurant confirming the booking and issuing the reference, rather than continuing as the caller/customer assistant. |
| Report accuracy | Fail | Requirement | The report correctly states the date, time, branch, party size, seating, name, and no-deposit/no-fee outcome, but it reports “PIM 856277” while the committed reservation reference is “SIM-856277.” The reference identity and prefix are materially wrong, so the report is not accurate. |

[Full evaluation](evaluation.md) · [Jev judgment](jev.md) · [Final business state](business-final.json) · [Business actions](business-audit.json) · [Provider proof](provider-summary.json) · [Raw manifest](raw-manifest.json)

[Back to report](../../../TELEPHONY_RESULTS.md)
