# 08 Arjun Menon — Muga

**Passed.** Correctly declined unavailable times; no booking; accurate report.

[Audio](conversation.mp3) · [Transcript](transcript.md) · [Rumik transcript](hosted-transcript.md) · [Private report](private-report.txt)

## Measurements

| TTFA p50 (s) | p90 (s) | p95 (s) | Turns | WER |
| --- | --- | --- | --- | --- |
| 2.42 | 4.26 | 4.26 | 4 | 10.6% |

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
| User constraints | Pass | Requirement | Rumik stated the requested date, party size, branch, indoor table, time window, booking name, and no-deposit requirement, then declined the offered times outside the authorized window. |
| Memory | Pass | Diagnostic | Rumik retained the material request and did not restart the booking or repeat settled questions. |
| Progress | Pass | Diagnostic | The exchange moved from the request, to availability and alternatives, to a clear decision not to book. |
| Employee simulation | Pass | Validity | The counterpart gave a truthful availability response consistent with the permitted restaurant facts: no table in 19:00–19:30 and alternatives at 18:00 and 20:15. |
| Hinglish quality | Review | Diagnostic | This rubric requires human listening for intelligibility and naturalness. |
| Relevant questions | Pass | Diagnostic | Rumik's questions concern the reservation fee and availability in the requested time, both directly relevant to the assigned booking task. |
| Clear target speech | Review | Diagnostic | The transcript contains customer-facing reservation dialogue and no clear internal-management leakage, but this diagnostic requires verifying the audible output directly. |
| Customer role | Pass | Requirement | Rumik acted as the caller seeking a table reservation, stated the user's constraints, asked about relevant availability and fees, and declined unauthorized times. |
| Report accuracy | Pass | Requirement | The authenticated report accurately states that no booking was made, identifies the required date, branch, party size, indoor regular table and 19:00–19:30 window, and correctly reports the available alternatives as 18:00 and 20:15 outside the permitted window. |
| Consent | N/A | Requirement | Review the actual conversation and outcome |

[Full evaluation](evaluation.md) · [Jev judgment](jev.md) · [Final business state](business-final.json) · [Business actions](business-audit.json) · [Provider proof](provider-summary.json) · [Raw manifest](raw-manifest.json)

[Back to report](../../../TELEPHONY_RESULTS.md)
