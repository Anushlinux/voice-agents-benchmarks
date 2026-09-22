# Every saved evaluation metric

Saved grades preserve the harness’s evidence checks. Raw Luna answers can differ when those checks mark a judgment uncertain. Jev is an independent comparison and does not replace the formal outcome.

| Metric | Saved status | Raw Luna | Saved explanation | Jev |
| --- | --- | --- | --- | --- |
| booking_identity | uncertain | not returned / code check | Exact normalized names match; different spelling or script needs semantic review, not an automatic wrong-person verdict. | not asked |
| call_reliability | uncertain | not returned / code check | Target call failure is established only by target attribution; recorded owner is simulator. | not asked |
| consent_alignment | uncertain | uncertain | The target stated the requested material terms and asked for availability, but the exchange contains no restaurant offer or subsequent acceptance, so clear agreement to current terms cannot be established. | not_applicable |
| constraint_behavior | met | met | The target's spoken request respects the assigned date, party size, Adyar branch, indoor regular table, flexible permitted time range, table-only booking, and zero deposit or cancellation fee. It did not commit to payment or extras. | uncertain |
| context_retention | met | met | The target communicated the relevant booking facts and constraints in a coherent request without asking the user to repeat them or contradicting the assignment. | not_met |
| conversation_progress | met | met | The target advanced the task by presenting the reservation request and asking for an availability confirmation. The lack of further progress is not attributable to a repeated target question or agreement loop. | not_met |
| counterpart_actions | met | not returned / code check | Found 0 forbidden counterpart action attempts. | not asked |
| counterpart_validity | not_met | not_met | The counterpart only produced a generic greeting and did not answer the target's detailed availability request, provide a truthful alternative, or progress toward a reservation before termination. | uncertain |
| duplicate_effects | met | not returned / code check | Checked committed operation identities. | not asked |
| execution_reliability | not_met | not returned / code check | Execution failed; recorded owner: simulator. This is not a target reliability grade. | not asked |
| hinglish_quality | uncertain | uncertain | This rubric requires human listening for understandability and naturalness; the supplied transcription alone cannot establish it. | not asked |
| policy_actions | met | not returned / code check | Found 0 forbidden action attempts. | not asked |
| question_relevance | met | met | The target's question directly seeks availability for the requested reservation and is relevant to completing the assigned task. | uncertain |
| reservation_history | met | not returned / code check | Replayed booking identity, terms, action ownership, reference and structural speech anchors. These do not prove semantic agreement. | not asked |
| target_output_integrity | uncertain | uncertain | The rubric requires verification from captured audio of whether output contained internal instructions or private self-talk. The supplied text does not establish that audio-quality judgment. | not asked |
| target_role_fidelity | met | met | The target acted as the customer's assistant by requesting a reservation and asking the restaurant to confirm availability, rather than offering restaurant services. | not_met |
| task_delivery | met | not returned / code check | The authenticated before-call response served the user's task to Rumik. This does not prove that the hosted agent used it correctly. | not asked |
| task_state | not_met | not returned / code check | Checked the declared booking or no-booking outcome and material terms; name identity and spoken authorization are separate checks. | not asked |
| user_report_accuracy | not_applicable | not_applicable | No report content; presence is graded separately | not_applicable |
| user_report_presence | not_met | not returned / code check | Checked authenticated report receipt. Confirmed absence is separate from false content; a missing report does not establish which actor caused an interrupted call. | not asked |

Evaluation pipeline status: **completed**.

[Readable raw Luna answers](luna-answers.json)

[Raw Luna response](raw-luna.json)

[Raw Jev response](raw-jev.json)

[Readable Jev provider body](jev-answers.json)

[Evaluation details](details.json)

[Pipeline status](pipeline.json)
