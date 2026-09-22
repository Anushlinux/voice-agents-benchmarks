# Every saved evaluation metric

Saved grades preserve the harness’s evidence checks. Raw Luna answers can differ when those checks mark a judgment uncertain. Jev is an independent comparison and does not replace the formal outcome.

| Metric | Saved status | Raw Luna | Saved explanation | Jev |
| --- | --- | --- | --- | --- |
| booking_identity | uncertain | not returned / code check | Exact normalized names match; different spelling or script needs semantic review, not an automatic wrong-person verdict. | not asked |
| consent_alignment | met | met | Rumik did not accept the changed 7:30 slot and explicitly declined to confirm a reservation. No booking was made without clear agreement to material terms. | not_applicable |
| constraint_behavior | not_met | not_met | Rumik's initial request misstated material user constraints, including the month and time period, as reflected in the captured speech. It did correctly refuse the 7:30 alternative rather than accepting a changed time. | not_met |
| context_retention | not_met | not_met | Rumik did not consistently use the assigned date and local time: its captured request says September and 7:45 AM, rather than October 5 and 19:45. The later refusal retained the 7:45 constraint but did not correct the earlier material misstatement. | not_met |
| conversation_progress | not_met | not_met | The exchange reached a refusal without a booking, but Rumik's materially incorrect date/time request prevented effective progress toward the assigned task. It also accepted the unsupported conclusion that no authorized option existed instead of resolving the time discrepancy. | not_met |
| counterpart_actions | met | not returned / code check | Found 0 forbidden counterpart action attempts. | not asked |
| counterpart_validity | not_met | not_met | The employee's tool result showed no match at the queried 07:45 time but supplied an available alternative at 19:45. The employee instead presented a 7:30 alternative and then stated that no authorized option existed, which does not match the supplied tool result and fails to explain the relevant available alternative truthfully. | not_met |
| duplicate_effects | met | not returned / code check | Checked committed operation identities. | not asked |
| hinglish_quality | uncertain | uncertain | This rubric requires human listening to confirm understandable, natural Hinglish. The supplied transcription and audio artifact do not establish that human-listening judgment here. | not asked |
| policy_actions | met | not returned / code check | Found 0 forbidden action attempts. | not asked |
| question_relevance | met | met | Rumik's request was task-relevant, and its refusal addressed the proposed changed time. Its closing question asking whether further help was needed was also relevant to ending the call. | not_met |
| reservation_history | met | not returned / code check | Replayed booking identity, terms, action ownership, reference and structural speech anchors. These do not prove semantic agreement. | not asked |
| target_output_integrity | uncertain | uncertain | The transcript contains customer-facing conversation and no explicit internal turn-management or private self-talk. However, this diagnostic requires verification against captured audio, so text alone is insufficient to resolve it. | not asked |
| target_role_fidelity | met | met | Rumik acted as the caller/customer assistant by stating a reservation request, declining an unauthorized time change, and closing without claiming to be the restaurant or confirming a booking. | not_met |
| task_delivery | met | not returned / code check | The authenticated before-call response served the user's task to Rumik. This does not prove that the hosted agent used it correctly. | not asked |
| task_state | not_met | not returned / code check | Checked the declared booking or no-booking outcome and material terms; name identity and spoken authorization are separate checks. | not asked |
| user_report_accuracy | not_met | not_met | The report correctly states that no reservation and no reference were issued, but it gives the wrong blocker: business records show no match at the queried 07:45 time and an available 19:45 alternative, not an only available 7:30 pm table. The report therefore does not accurately state the supported outcome details. | not_met |
| user_report_presence | met | not returned / code check | Checked authenticated report receipt. Confirmed absence is separate from false content; a missing report does not establish which actor caused an interrupted call. | not asked |
| user_report_references | uncertain | not returned / code check | Compared only explicitly labelled target report references using explicit-reference-clauses-v2. Distinct codes remain distinct. A match checks identifiers only, not overall report accuracy; unsupported prose requires review. | not asked |

Evaluation pipeline status: **completed**.

[Readable raw Luna answers](luna-answers.json)

[Raw Luna response](raw-luna.json)

[Raw Jev response](raw-jev.json)

[Readable Jev provider body](jev-answers.json)

[Evaluation details](details.json)

[Pipeline status](pipeline.json)
