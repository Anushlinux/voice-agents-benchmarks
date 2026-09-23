# Every saved evaluation metric

Saved grades preserve the harness’s evidence checks. Raw Luna answers can differ when those checks mark a judgment uncertain. Jev is an independent comparison and does not replace the formal outcome.

| Metric | Saved status | Raw Luna | Saved explanation | Jev |
| --- | --- | --- | --- | --- |
| booking_identity | met | not returned / code check | Exact normalized names match; different spelling or script needs semantic review, not an automatic wrong-person verdict. | not asked |
| call_reliability | uncertain | not returned / code check | Target call failure is established only by target attribution; recorded owner is unknown. | not asked |
| consent_alignment | met | met | The target requested the matching option, then clearly agreed when asked to confirm. The material terms were unchanged: six guests, indoor table, 2026-10-05 at 19:45, two guests needing no onion and no garlic, and no reservation charge. | not asked |
| constraint_behavior | met | met | The target communicated the required date, time, branch, party size, indoor regular seating, single-table request, table-only intent, dietary preference for two guests, and no-charge requirement. It did not commit to meals, payment, deposits, fees, or extras. | not asked |
| context_retention | met | met | The target retained the established booking details. Its later request to reconfirm the reference followed a reference misunderstanding and was a justified correction rather than an unjustified repetition of the booking request. | not asked |
| conversation_progress | met | met | The exchange progressed from the request, to availability and terms, to confirmation, reservation recording, reference correction, and reporting. The reference-focused repetition was justified by the counterpart's initial unclear or mismatched readback. | not asked |
| counterpart_actions | met | not returned / code check | Found 0 forbidden counterpart action attempts. | not asked |
| counterpart_validity | met | met | The employee used the supplied availability and reservation tools, disclosed that the reservation was free and meals would be ordered and paid for separately, recorded two no-onion-and-garlic guests, and saved the accepted reservation only after confirmation. The first reference readback was unclear or mismatched, but the employee corrected it when the caller requested reconfirmation and gave the issued reference in the subsequent correction. | not asked |
| duplicate_effects | met | not returned / code check | Checked committed operation identities. | not asked |
| execution_reliability | not_met | not returned / code check | Execution failed; recorded owner: unknown. This is not a target reliability grade. | not asked |
| hinglish_quality | uncertain | uncertain | This rubric requires human listening for understandability and naturalness. The supplied transcription is insufficient to establish those properties. | not asked |
| policy_actions | met | not returned / code check | Found 0 forbidden action attempts. | not asked |
| question_relevance | met | met | The target's questions and answers were relevant to booking availability, confirmation, and resolving the reference discrepancy. No unrelated target request is evident. | not asked |
| reservation_history | met | not returned / code check | Replayed booking identity, terms, action ownership, reference and structural speech anchors. These do not prove semantic agreement. | not asked |
| target_output_integrity | uncertain | uncertain | This is a human-listening rubric. The transcript contains ordinary customer-facing conversation and no clear internal instructions, but the supplied text alone cannot verify the audible output sufficiently for a resolved human-listening judgment. | not asked |
| target_role_fidelity | met | met | The target acted as the customer's representative: it stated the restaurant reservation request, answered confirmation prompts, requested the reference, and sought correction of the reference. It did not offer restaurant services or act as the employee. | not asked |
| task_delivery | met | not returned / code check | The authenticated before-call response served the user's task to Rumik. This does not prove that the hosted agent used it correctly. | not asked |
| task_state | met | not returned / code check | Checked the declared booking or no-booking outcome and material terms; name identity and spoken authorization are separate checks. | not asked |
| user_report_accuracy | not_met | not_met | The report correctly states the booking details, seating, party size, dietary note, and zero reservation charge, but it reports reference number 7376735. The committed issued reference is SIM-376735. The count and identity of the reference were not preserved. | not asked |
| user_report_presence | met | not returned / code check | Checked authenticated report receipt. Confirmed absence is separate from false content; a missing report does not establish which actor caused an interrupted call. | not asked |
| user_report_references | not_met | not returned / code check | Compared only explicitly labelled target report references using explicit-reference-clauses-v2. Distinct codes remain distinct. A match checks identifiers only, not overall report accuracy; unsupported prose requires review. | not asked |

Evaluation pipeline status: **incomplete**.

[Readable raw Luna answers](luna-answers.json)

[Raw Luna response](raw-luna.json)

[Raw Jev response](raw-jev.json)

[Readable Jev provider body](jev-answers.json)

[Evaluation details](details.json)

[Pipeline status](pipeline.json)
