# 02 Kabir Sethi — Muga

**Unresolved.** Simulation needs review; report truncates the reference. Jev request failed.

[Audio](conversation.mp3) · [Transcript](transcript.md) · [Rumik transcript](hosted-transcript.md) · [Private report](private-report.txt)

## Measurements

| TTFA p50 (s) | p90 (s) | p95 (s) | Turns | WER |
| --- | --- | --- | --- | --- |
| 2.34 | 2.75 | 3.66 | 11 | — |

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
| Correct reference number | Fail | Supporting | Compared only explicitly labelled target report references using explicit-reference-clauses-v2. |
| Report delivered | Pass | Requirement | Checked authenticated report receipt. |
| Consent | Pass | Requirement | The user's request authorized one booking and explicitly allowed Domlur if Indiranagar was unavailable. |
| User constraints | Pass | Requirement | The target's spoken terms preserve the requested date, time, party size, indoor table, Domlur fallback, table-only booking, and no-deposit/no-fee requirement. |
| Memory | Review | Diagnostic | Unsupported judge claim: The judgment lacks a quoted observation from the assessed target. |
| Progress | Review | Diagnostic | Unsupported judge claim: A speech claim attributes the quoted window to the wrong speaker. |
| Employee simulation | Review | Validity | Unsupported judge claim: A speech claim attributes the quoted window to the wrong speaker. |
| Hinglish quality | Review | Diagnostic | This rubric requires human listening for understandability and naturalness. |
| Relevant questions | Pass | Diagnostic | The captured target speech asks about availability, uses the authorized Domlur fallback, requests the booking, and asks for the confirmation reference. |
| Clear target speech | Review | Diagnostic | Unsupported judge claim: A speech claim attributes the quoted window to the wrong speaker. |
| Customer role | Review | Requirement | Unsupported judge claim: A speech claim attributes the quoted window to the wrong speaker. |
| Report accuracy | Fail | Requirement | The report correctly states the date, time, party size, seating, branch, booking name, and no-fee terms, but it reports the reference as SIM-98. |

[Full evaluation](evaluation.md) · [Jev judgment](jev.md) · [Final business state](business-final.json) · [Business actions](business-audit.json) · [Provider proof](provider-summary.json) · [Raw manifest](raw-manifest.json)

[Back to report](../../../TELEPHONY_RESULTS.md)
