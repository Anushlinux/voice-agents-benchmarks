# 04 Nisha Mehta — Muga

[Back to model](../README.md) · [Back to report](../../../README.md)

**Unresolved.** Employee offered the wrong time; no booking.

[Audio](conversation.mp3) · [Transcript](transcript.md) · [Rumik transcript](hosted-transcript.md) · [Private report](private-report.txt)

## Measurements

| TTFA p50 (s) | p90 (s) | p95 (s) | Turns | WER |
| --- | --- | --- | --- | --- |
| 2.52 | 4.30 | 4.30 | 4 | 16.2% |

[TTFA proof](ttfa.json) · [WER proof](wer.md)

## Metric results

Pass / Fail = saved check result. Review = unresolved; N/A = not applicable. Diagnostic checks do not decide the overall result.

| Metric | Result | Role | Evidence / reason |
| --- | --- | --- | --- |
| Employee tools used correctly | Pass | Validity | Found 0 forbidden counterpart action attempts. |
| Task delivered | Pass | Prerequisite | The authenticated before-call response served the user's task to Rumik. |
| Allowed actions only | Pass | Requirement | Found 0 forbidden action attempts. |
| No duplicate bookings | Pass | Requirement | Checked committed operation identities. |
| Correct final booking state | Fail | Requirement | Checked the declared booking or no-booking outcome and material terms; name identity and spoken authorization are separate checks. |
| Correct booking name | Review | Requirement | Exact normalized names match; different spelling or script needs semantic review, not an automatic wrong-person verdict. |
| Valid booking history | Pass | Requirement | Replayed booking identity, terms, action ownership, reference and structural speech anchors. |
| Correct reference number | Review | Supporting | Compared only explicitly labelled target report references using explicit-reference-clauses-v2. |
| Report delivered | Pass | Requirement | Checked authenticated report receipt. |
| Consent | Pass | Requirement | Rumik did not accept the changed 7:30 slot and explicitly declined to confirm a reservation. |
| User constraints | Fail | Requirement | Rumik's initial request misstated material user constraints, including the month and time period, as reflected in the captured speech. |
| Memory | Fail | Diagnostic | Rumik did not consistently use the assigned date and local time: its captured request says September and 7:45 AM, rather than October 5 and 19:45. |
| Progress | Fail | Diagnostic | The exchange reached a refusal without a booking, but Rumik's materially incorrect date/time request prevented effective progress toward the assigned task. |
| Employee simulation | Fail | Validity | The employee's tool result showed no match at the queried 07:45 time but supplied an available alternative at 19:45. |
| Hinglish quality | Review | Diagnostic | This rubric requires human listening to confirm understandable, natural Hinglish. |
| Relevant questions | Pass | Diagnostic | Rumik's request was task-relevant, and its refusal addressed the proposed changed time. |
| Clear target speech | Review | Diagnostic | The transcript contains customer-facing conversation and no explicit internal turn-management or private self-talk. |
| Customer role | Pass | Requirement | Rumik acted as the caller/customer assistant by stating a reservation request, declining an unauthorized time change, and closing without claiming to be the restaurant or confirming a booking. |
| Report accuracy | Fail | Requirement | The report correctly states that no reservation and no reference were issued, but it gives the wrong blocker: business records show no match at the queried 07:45 time and an available 19:45 alternative, not an only available 7:30 pm table. |

[Full evaluation](evaluation.md) · [Jev judgment](jev.md) · [Final business state](business-final.json) · [Business actions](business-audit.json) · [Provider proof](provider-summary.json) · [Raw manifest](raw-manifest.json)
