# 03 Meera Iyer — Muga

[Back to model](../README.md) · [Back to report](../../../README.md)

**Unresolved.** Employee stopped after greeting; no booking or report.

[Audio](conversation.mp3) · [Transcript](transcript.md) · [Rumik transcript](hosted-transcript.md) · [Private report](private-report.txt)

## Measurements

| TTFA p50 (s) | p90 (s) | p95 (s) | Turns | WER |
| --- | --- | --- | --- | --- |
| 1.98 | 1.98 | 1.98 | 1 | — |

[TTFA proof](ttfa.json) · [WER proof](wer.md)

## Metric results

Pass / Fail = saved check result. Review = unresolved; N/A = not applicable. Diagnostic checks do not decide the overall result.

| Metric | Result | Role | Evidence / reason |
| --- | --- | --- | --- |
| Employee tools used correctly | Pass | Validity | Found 0 forbidden counterpart action attempts. |
| Task delivered | Pass | Prerequisite | The authenticated before-call response served the user's task to Rumik. |
| Allowed actions only | Pass | Requirement | Found 0 forbidden action attempts. |
| No duplicate bookings | Pass | Requirement | Checked committed operation identities. |
| Execution completed | Fail | Supporting | Execution failed; recorded owner: simulator. |
| Call reliability | Review | Supporting | Target call failure is established only by target attribution; recorded owner is simulator. |
| Correct final booking state | Fail | Requirement | Checked the declared booking or no-booking outcome and material terms; name identity and spoken authorization are separate checks. |
| Correct booking name | Review | Requirement | Exact normalized names match; different spelling or script needs semantic review, not an automatic wrong-person verdict. |
| Valid booking history | Pass | Requirement | Replayed booking identity, terms, action ownership, reference and structural speech anchors. |
| Report delivered | Fail | Requirement | Checked authenticated report receipt. |
| Consent | Review | Requirement | The target stated the requested material terms and asked for availability, but the exchange contains no restaurant offer or subsequent acceptance, so clear agreement to current terms cannot be established. |
| User constraints | Pass | Requirement | The target's spoken request respects the assigned date, party size, Adyar branch, indoor regular table, flexible permitted time range, table-only booking, and zero deposit or cancellation fee. |
| Memory | Pass | Diagnostic | The target communicated the relevant booking facts and constraints in a coherent request without asking the user to repeat them or contradicting the assignment. |
| Progress | Pass | Diagnostic | The target advanced the task by presenting the reservation request and asking for an availability confirmation. |
| Employee simulation | Fail | Validity | The counterpart only produced a generic greeting and did not answer the target's detailed availability request, provide a truthful alternative, or progress toward a reservation before termination. |
| Hinglish quality | Review | Diagnostic | This rubric requires human listening for understandability and naturalness; the supplied transcription alone cannot establish it. |
| Relevant questions | Pass | Diagnostic | The target's question directly seeks availability for the requested reservation and is relevant to completing the assigned task. |
| Clear target speech | Review | Diagnostic | The rubric requires verification from captured audio of whether output contained internal instructions or private self-talk. |
| Customer role | Pass | Requirement | The target acted as the customer's assistant by requesting a reservation and asking the restaurant to confirm availability, rather than offering restaurant services. |
| Report accuracy | N/A | Requirement | No report content; presence is graded separately |

[Full evaluation](evaluation.md) · [Jev judgment](jev.md) · [Final business state](business-final.json) · [Business actions](business-audit.json) · [Provider proof](provider-summary.json) · [Raw manifest](raw-manifest.json)
