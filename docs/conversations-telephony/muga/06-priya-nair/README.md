# 06 Priya Nair — Muga

**Unresolved.** Employee saved the wrong name and gave an incomplete reference.

[Audio](conversation.mp3) · [Transcript](transcript.md) · [Rumik transcript](hosted-transcript.md) · [Private report](private-report.txt)

## Measurements

| TTFA p50 (s) | p90 (s) | p95 (s) | Turns | WER |
| --- | --- | --- | --- | --- |
| 2.48 | 3.62 | 3.62 | 4 | 23.7% |

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
| Correct booking name | Review | Requirement | Exact normalized names match; different spelling or script needs semantic review, not an automatic wrong-person verdict. |
| Valid booking history | Pass | Requirement | Replayed booking identity, terms, action ownership, reference and structural speech anchors. |
| Correct reference number | Review | Supporting | Compared only explicitly labelled target report references using explicit-reference-clauses-v2. |
| Report delivered | Pass | Requirement | Checked authenticated report receipt. |
| Consent | Pass | Requirement | The target first requested availability for the relevant date, time, seating, inclusions, party size, and budget, then clearly agreed to book the offered option. |
| User constraints | Pass | Requirement | The target communicated the required party size, Powai branch, date, 20:00 time, indoor regular seating, per-person starter/main/rice-or-bread inclusions, and INR 10,500 limit, and agreed to the offered INR 9,800 option. |
| Memory | Pass | Diagnostic | The target states the material requirements once, asks for availability, and then accepts the presented option without an unjustified repetition loop. |
| Progress | Pass | Diagnostic | The exchange progresses from the target's request, to availability and option details, to an explicit booking request and closing. |
| Employee simulation | Fail | Validity | The counterpart used the permitted availability, offer, and reservation tools, but the delivered reference is not faithful to the issued reference. |
| Hinglish quality | Review | Diagnostic | This rubric requires human listening for understandability and naturalness. |
| Relevant questions | Pass | Diagnostic | The target asks for availability after stating the booking requirements, accepts the offered option, and does not introduce unrelated questions or answers. |
| Clear target speech | Review | Diagnostic | The transcript contains customer-facing booking conversation and no textual internal turn-management instructions, but this diagnostic specifically requires verification against captured audio. |
| Customer role | Pass | Requirement | The target acts as the caller's customer assistant: it requests the dinner arrangement, asks about availability, authorizes booking of the option, and closes the call. |
| Report accuracy | Fail | Requirement | The report correctly states the main booking terms, but it reports the booking as under Priya Nair while the committed business record is under Rumik, and it reports reference “SIM 00 119” rather than preserving the issued reference SIM-001119. |

[Full evaluation](evaluation.md) · [Jev judgment](jev.md) · [Final business state](business-final.json) · [Business actions](business-audit.json) · [Provider proof](provider-summary.json) · [Raw manifest](raw-manifest.json)

[Back to report](../../../TELEPHONY_RESULTS.md)
