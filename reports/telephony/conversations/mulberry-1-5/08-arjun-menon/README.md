# 08 Arjun Menon — Mulberry 1.5

[Back to model](../README.md) · [Back to report](../../../README.md)

**Passed.** Correctly declined unavailable times; no booking; accurate report.

[Audio](conversation.mp3) · [Transcript](transcript.md) · [Rumik transcript](hosted-transcript.md) · [Private report](private-report.txt)

## Measurements

| TTFA p50 (s) | p90 (s) | p95 (s) | Turns | WER |
| --- | --- | --- | --- | --- |
| 2.12 | 2.56 | 2.56 | 4 | 17.1% |

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
| User constraints | Pass | Requirement | Rumik stated the requested date, party size, indoor regular table, booking name, no-deposit/no-cancellation-fee terms, and the restricted time window. |
| Memory | Pass | Diagnostic | The exchange retains the requested party size, seating, date, name, and time restriction, and the target does not accept the offered out-of-window alternatives. |
| Progress | Pass | Diagnostic | The target makes the booking request, communicates the time constraint, responds to the alternatives, and ends with the correct no-booking decision rather than entering an unjustified agreement loop. |
| Employee simulation | Pass | Validity | The counterpart truthfully states that no table is available in the requested window, identifies the two available alternatives, and does not claim a reservation or invent a reference. |
| Hinglish quality | Review | Diagnostic | This rubric requires human listening for understandability and natural Hinglish. |
| Relevant questions | Pass | Diagnostic | The target's questions and answers concern the requested reservation, availability, acceptable timing, and closure. |
| Clear target speech | Review | Diagnostic | Whether the audible output contained internal turn-management instructions or private self-talk requires verification from the audio itself. |
| Customer role | Pass | Requirement | The target acts as the caller seeking a reservation, states the user's booking requirements, rejects unavailable times, and closes without booking. |
| Report accuracy | Pass | Requirement | The private report accurately states that no qualifying indoor table for three was available in the requested Fort Kochi date/time window, that only earlier or later slots were offered, and that no reservation was made. |
| Consent | N/A | Requirement | Review the actual conversation and outcome |

[Full evaluation](evaluation.md) · [Jev judgment](jev.md) · [Final business state](business-final.json) · [Business actions](business-audit.json) · [Provider proof](provider-summary.json) · [Raw manifest](raw-manifest.json)
