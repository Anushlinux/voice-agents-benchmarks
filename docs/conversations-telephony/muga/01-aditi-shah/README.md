# 01 Aditi Shah — Muga

**Unresolved.** Booking and report match; spoken consent still needs review.

[Audio](conversation.mp3) · [Transcript](transcript.md) · [Rumik transcript](hosted-transcript.md) · [Private report](private-report.txt)

## Measurements

| TTFA p50 (s) | p90 (s) | p95 (s) | Turns | WER |
| --- | --- | --- | --- | --- |
| 3.04 | 3.27 | 3.27 | 7 | 26.1% |

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
| Correct reference number | Review | Supporting | Compared only explicitly labelled target report references using explicit-reference-clauses-v2. |
| Report delivered | Pass | Requirement | Checked authenticated report receipt. |
| User constraints | Pass | Requirement | Rumik's captured content stays within the requested date, 19:30 time, Aundh branch, three guests, indoor regular table, booking name, and zero-charge table-only constraints. |
| Memory | Pass | Diagnostic | Rumik carries forward the requested branch, date, party size, seating, name, and reservation details while progressing from availability to confirmation and reference handling. |
| Progress | Pass | Diagnostic | The exchange moves from availability inquiry to an available alternative, confirmation, reservation recording, reference delivery, and a final report. |
| Relevant questions | Pass | Diagnostic | Rumik's questions and requests concern availability, the requested reservation terms, confirmation, and the reference. |
| Consent | Review | Requirement | The captured exchange contains a request to confirm the available 19:30 terms and the counterpart subsequently records the reservation, but the supplied business consent evidence explicitly requires human review. |
| Employee simulation | Pass | Validity | The restaurant employee truthfully offers the available 19:30 indoor table-only option, distinguishes it from the unavailable morning query, asks for confirmation, and the committed reservation and reference match the permitted tool results. |
| Customer role | Fail | Requirement | Rumik's captured speech includes employee-style service language and claims of completed reservation and reference delivery, rather than consistently acting as the customer assistant making the request. |
| Report accuracy | Pass | Requirement | The latest accepted report accurately states the booked date, time, Aundh branch, party size, indoor regular table, booking name, zero charge/deposit/cancellation fee, and the exact issued reference SIM-317527. |
| Hinglish quality | Review | Diagnostic | This rubric requires human listening for understandability and naturalness. |
| Clear target speech | Review | Diagnostic | The transcript contains employee-style confirmation and reference language in target-labeled speech, but determining whether the audible output contains leakage or private self-talk requires direct human audio verification beyond the transcript. |

[Full evaluation](evaluation.md) · [Jev judgment](jev.md) · [Final business state](business-final.json) · [Business actions](business-audit.json) · [Provider proof](provider-summary.json) · [Raw manifest](raw-manifest.json)

[Back to report](../../../TELEPHONY_RESULTS.md)
