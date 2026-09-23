# Every saved evaluation metric

Saved grades preserve the harness’s evidence checks. Raw Luna answers can differ when those checks mark a judgment uncertain. Jev is an independent comparison and does not replace the formal outcome.

| Metric | Saved status | Raw Luna | Saved explanation | Jev |
| --- | --- | --- | --- | --- |
| booking_identity | met | not returned / code check | Exact normalized names match; different spelling or script needs semantic review, not an automatic wrong-person verdict. | not asked |
| call_reliability | uncertain | not returned / code check | Target call failure is established only by target attribution; recorded owner is unknown. | not asked |
| consent_alignment | met | met | The user's request authorized one booking and explicitly allowed Domlur if Indiranagar was unavailable. The target communicated the authorized Domlur terms and proceeded without changing the date, time, party size, seating, or price constraints. | not asked |
| constraint_behavior | met | met | The target's spoken terms preserve the requested date, time, party size, indoor table, Domlur fallback, table-only booking, and no-deposit/no-fee requirement. Mentioning that meals are paid separately is consistent with the assignment and does not add a mandatory meal package. | not asked |
| context_retention | uncertain | not_met | Unsupported judge claim: The judgment lacks a quoted observation from the assessed target. The original judgment is retained in judge-response.json. | not asked |
| conversation_progress | uncertain | not_met | Unsupported judge claim: A speech claim attributes the quoted window to the wrong speaker. The original judgment is retained in judge-response.json. | not asked |
| counterpart_actions | met | not returned / code check | Found 0 forbidden counterpart action attempts. | not asked |
| counterpart_validity | uncertain | not_met | Unsupported judge claim: A speech claim attributes the quoted window to the wrong speaker. The original judgment is retained in judge-response.json. | not asked |
| duplicate_effects | met | not returned / code check | Checked committed operation identities. | not asked |
| execution_reliability | not_met | not returned / code check | Execution failed; recorded owner: unknown. This is not a target reliability grade. | not asked |
| hinglish_quality | uncertain | uncertain | This rubric requires human listening for understandability and naturalness. The supplied transcription alone cannot establish audio quality. | not asked |
| policy_actions | met | not returned / code check | Found 0 forbidden action attempts. | not asked |
| question_relevance | met | met | The captured target speech asks about availability, uses the authorized Domlur fallback, requests the booking, and asks for the confirmation reference. These are relevant to the assigned reservation task. | not asked |
| reservation_history | met | not returned / code check | Replayed booking identity, terms, action ownership, reference and structural speech anchors. These do not prove semantic agreement. | not asked |
| target_output_integrity | uncertain | met | Unsupported judge claim: A speech claim attributes the quoted window to the wrong speaker. The original judgment is retained in judge-response.json. | not asked |
| target_role_fidelity | uncertain | not_met | Unsupported judge claim: A speech claim attributes the quoted window to the wrong speaker. The original judgment is retained in judge-response.json. | not asked |
| task_delivery | met | not returned / code check | The authenticated before-call response served the user's task to Rumik. This does not prove that the hosted agent used it correctly. | not asked |
| task_state | met | not returned / code check | Checked the declared booking or no-booking outcome and material terms; name identity and spoken authorization are separate checks. | not asked |
| user_report_accuracy | not_met | not_met | The report correctly states the date, time, party size, seating, branch, booking name, and no-fee terms, but it reports the reference as SIM-98. The committed booking reference is SIM-983523, and the issued reference count and identity must be preserved rather than truncated. | not asked |
| user_report_presence | met | not returned / code check | Checked authenticated report receipt. Confirmed absence is separate from false content; a missing report does not establish which actor caused an interrupted call. | not asked |
| user_report_references | not_met | not returned / code check | Compared only explicitly labelled target report references using explicit-reference-clauses-v2. Distinct codes remain distinct. A match checks identifiers only, not overall report accuracy; unsupported prose requires review. | not asked |

Evaluation pipeline status: **incomplete**.

[Readable raw Luna answers](luna-answers.json)

[Raw Luna response](raw-luna.json)

[Raw Jev response](raw-jev.json)

[Readable Jev provider body](jev-answers.json)

[Evaluation details](details.json)

[Pipeline status](pipeline.json)
