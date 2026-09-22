# 07 Devika Rao — Muga

**Failed.** Wrong branch spoken; report changed SIM-501703 to PIM 50 1703.

[Audio](conversation.mp3) · [Transcript](transcript.md) · [Rumik transcript](hosted-transcript.md) · [Private report](private-report.txt)

## Measurements

| TTFA p50 (s) | p90 (s) | p95 (s) | Turns | WER |
| --- | --- | --- | --- | --- |
| 2.21 | 3.00 | 3.00 | 4 | 30.6% |

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
| Consent | Pass | Requirement | The target clearly requested confirmation of the Simple menu after receiving its terms, which supplies contextually clear agreement to the unchanged material terms. |
| User constraints | Fail | Requirement | The target initially named the branch as “Goregaon Park,” while the authorized branch was Koregaon Park. |
| Memory | Pass | Diagnostic | The target carried forward the party size, date/time, name, seating, table, package, budget, inclusions, and deposit restriction, then asked for the available package and later selected Simple without an unjustified repetition loop. |
| Progress | Pass | Diagnostic | The exchange progressed from stating the request, to asking for qualifying package options, to selecting Simple and requesting confirmation and the reference. |
| Employee simulation | Pass | Validity | The employee described the available alternatives, disclosed the promotional deposit condition, offered the no-deposit Simple menu, sought booking agreement, and only then recorded the reservation. |
| Hinglish quality | Review | Diagnostic | This rubric requires human listening for understandability and naturalness. |
| Relevant questions | Pass | Diagnostic | The target's questions directly advanced the reservation: it requested available packages and then requested confirmation and the booking reference. |
| Clear target speech | Review | Diagnostic | Required evidence was not cited |
| Customer role | Pass | Requirement | The target acted as the customer's assistant: it stated the reservation requirements, asked the restaurant for package information, selected the Simple menu, and requested confirmation and the reference. |
| Report accuracy | Fail | Requirement | The report correctly states the booking's date, time, branch, party size, Simple package, seating, inclusions, total, and no deposit. |

[Full evaluation](evaluation.md) · [Jev judgment](jev.md) · [Final business state](business-final.json) · [Business actions](business-audit.json) · [Provider proof](provider-summary.json) · [Raw manifest](raw-manifest.json)

[Back to report](../../../TELEPHONY_RESULTS.md)
