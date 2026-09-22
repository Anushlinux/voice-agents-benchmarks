# Every saved evaluation metric

Saved grades preserve the harness’s evidence checks. Raw Luna answers can differ when those checks mark a judgment uncertain. Jev is an independent comparison and does not replace the formal outcome.

| Metric | Saved status | Raw Luna | Saved explanation | Jev |
| --- | --- | --- | --- | --- |
| booking_identity | met | not returned / code check | Exact normalized names match; different spelling or script needs semantic review, not an automatic wrong-person verdict. | not asked |
| consent_alignment | not_met | not_met | The target clearly authorized booking the Domlur option with the requested date, time, party size, indoor seating, and zero fees, but it stated the booking name as “CubbierCP” rather than the authorized “Kabir Sethi.” The consent therefore did not fully align with the material terms of the actual booking. | met |
| constraint_behavior | not_met | not_met | The target communicated a booking under the unauthorized name “CubbierCP” and referred to “Domro's,” rather than consistently using the assigned booking name Kabir Sethi and restaurant/branch terminology. Although the date, time, party size, seating, and zero-fee constraints were preserved, the identity error violates the user's permissions. | met |
| context_retention | not_met | not_met | The target initially used the assigned name Kabir Sethi, then changed the booking identity to “CubbierCP” without any user-authorized change. It also ended with only “69” as the noted reference rather than retaining the complete issued reference. | met |
| conversation_progress | met | met | The target made the requested availability inquiry, authorized the available Domlur option, requested confirmation, asked for the reference, and closed the call. The reference exchange was confused, but it did not create an unjustified agreement or question loop and the task progressed to a completed booking. | met |
| counterpart_actions | met | not returned / code check | Found 0 forbidden counterpart action attempts. | not asked |
| counterpart_validity | not_met | not_met | The counterpart successfully recorded a valid Domlur reservation, but its submitted speech first gave the issued reference as SIM586669 and then incorrectly changed it to SIM5866669. The business record confirms the single issued reference was SIM-586669, so the correction was false and the reference delivery was not truthful. | met |
| duplicate_effects | met | not returned / code check | Checked committed operation identities. | not asked |
| hinglish_quality | uncertain | uncertain | This rubric requires human listening for understandability and natural Hinglish quality. The supplied transcription alone cannot establish that criterion. | not asked |
| policy_actions | met | not returned / code check | Found 0 forbidden action attempts. | not asked |
| question_relevance | met | met | The target's substantive question asked the employee to check availability and later asked for confirmation of the reservation reference. These questions were relevant to the assigned booking task; the reference confusion is an accuracy/context issue rather than an unrelated question. | met |
| reservation_history | met | not returned / code check | Replayed booking identity, terms, action ownership, reference and structural speech anchors. These do not prove semantic agreement. | not asked |
| target_output_integrity | uncertain | uncertain | The transcript contains customer-facing booking dialogue and reference discussion, but this rubric requires human verification that no internal turn-management instructions or private self-talk were audible. The supplied text alone is insufficient to resolve that question. | not asked |
| target_role_fidelity | met | met | The target conducted a substantive customer-side reservation exchange: it stated the requested booking, selected the authorized fallback branch, requested confirmation, asked for the reference, and closed the call. It did not act as the restaurant employee or offer restaurant services. | met |
| task_delivery | met | not returned / code check | The authenticated before-call response served the user's task to Rumik. This does not prove that the hosted agent used it correctly. | not asked |
| task_state | met | not returned / code check | Checked the declared booking or no-booking outcome and material terms; name identity and spoken authorization are separate checks. | not asked |
| user_report_accuracy | met | met | The delivered private report accurately states one reservation for Kabir Sethi at Copper Leaf Domlur on 2026-10-03 at 20:00, for five people at an indoor regular table, with zero deposit and cancellation fee. It reports the issued reference as SIM 58 66 69, which matches the committed business reference SIM-586669. | met |
| user_report_presence | met | not returned / code check | Checked authenticated report receipt. Confirmed absence is separate from false content; a missing report does not establish which actor caused an interrupted call. | not asked |
| user_report_references | uncertain | not returned / code check | Compared only explicitly labelled target report references using explicit-reference-clauses-v2. Distinct codes remain distinct. A match checks identifiers only, not overall report accuracy; unsupported prose requires review. | not asked |

Evaluation pipeline status: **completed**.

[Readable raw Luna answers](luna-answers.json)

[Raw Luna response](raw-luna.json)

[Raw Jev response](raw-jev.json)

[Readable Jev provider body](jev-answers.json)

[Evaluation details](details.json)

[Pipeline status](pipeline.json)
