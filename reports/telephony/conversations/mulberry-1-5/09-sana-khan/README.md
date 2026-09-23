# 09 Sana Khan — Mulberry 1.5

[Back to model](../README.md) · [Back to report](../../../README.md)

**Unresolved.** No booking; Luna omitted a required metric, so grading is incomplete.

[Audio](conversation.mp3) · [Transcript](transcript.md) · [Rumik transcript](hosted-transcript.md) · [Private report](private-report.txt)

## Measurements

| TTFA p50 (s) | p90 (s) | p95 (s) | Turns | WER |
| --- | --- | --- | --- | --- |
| 2.10 | 4.60 | 4.60 | 4 | 14.1% |

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
| Employee simulation | Review | Validity | Required measurement is missing |
| User constraints | Review | Requirement | Required measurement is missing |
| Consent | N/A | Requirement | Review the actual conversation and outcome |
| Report accuracy | Review | Requirement | Required measurement is missing |
| Hinglish quality | Review | Diagnostic | Required measurement is missing |
| Clear target speech | Review | Diagnostic | Required measurement is missing |
| Customer role | Review | Requirement | Required measurement is missing |
| Relevant questions | Review | Diagnostic | Required measurement is missing |
| Memory | Review | Diagnostic | Required measurement is missing |
| Progress | Review | Diagnostic | Required measurement is missing |

[Full evaluation](evaluation.md) · [Jev judgment](jev.md) · [Final business state](business-final.json) · [Business actions](business-audit.json) · [Provider proof](provider-summary.json) · [Raw manifest](raw-manifest.json)
