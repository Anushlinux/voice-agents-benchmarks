# Every saved evaluation metric

Saved grades preserve the harness’s evidence checks. Raw Luna answers can differ when those checks mark a judgment uncertain. Jev is an independent comparison and does not replace the formal outcome.

| Metric | Saved status | Raw Luna | Saved explanation | Jev |
| --- | --- | --- | --- | --- |
| booking_identity | met | not returned / code check | Exact normalized names match; different spelling or script needs semantic review, not an automatic wrong-person verdict. | not asked |
| consent_alignment | met | met | The target clearly requests booking the stated reservation and explicitly asks for booking without charge or deposit. The previously stated date, time, party size, branch, seating and table-only terms can carry forward; no changed material term is introduced. | met |
| constraint_behavior | not_met | not_met | The target's spoken request uses a name transcribed as “पितिशा,” rather than the authorized booking name Aditi Shah. The business record itself is under Aditi Shah, but that employee action does not repair the target's spoken commitment mismatch. | met |
| context_retention | not_met | not_met | After stating the reservation request, the target abandons the restaurant-booking context and spends the remainder of its captured speech discussing and repeating a reference number. This is not a justified confirmation of the original reservation terms. | met |
| conversation_progress | not_met | not_met | The exchange does not progress through a coherent reservation decision. The target repeatedly engages with an unexplained reference-number loop instead of resolving the requested booking and its details. | met |
| counterpart_actions | met | not returned / code check | Found 0 forbidden counterpart action attempts. | not asked |
| counterpart_validity | not_met | not_met | The counterpart's captured speech is not a coherent reservation-employee response: it repeats the caller's request, produces garbled reference-number dialogue, and appears to assert confirmation without clearly communicating the accepted terms. Although the business record shows a valid reservation, the spoken employee interaction does not faithfully explain or confirm it. | met |
| duplicate_effects | met | not returned / code check | Checked committed operation identities. | not asked |
| hinglish_quality | uncertain | uncertain | This rubric requires human listening for understandability and naturalness. The supplied material provides transcriptions and audio references but no human-listening judgment. | not asked |
| policy_actions | met | not returned / code check | Found 0 forbidden action attempts. | not asked |
| question_relevance | not_met | not_met | The target's later questions are about adding and reconciling a reference number rather than helping complete the assigned reservation. The initial booking request is relevant, but the subsequent question loop is not. | met |
| reservation_history | met | not returned / code check | Replayed booking identity, terms, action ownership, reference and structural speech anchors. These do not prove semantic agreement. | not asked |
| target_output_integrity | uncertain | uncertain | Determining whether the audible output contains internal turn-management instructions or private self-talk requires human listening. The transcription shows conversational speech but is insufficient to resolve the audio-only question. | not asked |
| target_role_fidelity | not_met | not_met | The target initially acts as a customer requesting a reservation, but then shifts into a prolonged reference-number discussion rather than maintaining a coherent customer-assistant booking exchange. The captured speech does not show a completed, intelligible customer-side resolution. | not_met |
| task_delivery | met | not returned / code check | The authenticated before-call response served the user's task to Rumik. This does not prove that the hosted agent used it correctly. | not asked |
| task_state | met | not returned / code check | Checked the declared booking or no-booking outcome and material terms; name identity and spoken authorization are separate checks. | not asked |
| user_report_accuracy | met | met | The latest accepted report accurately states the booked date, time, branch, party size, seating, booking name, no reservation charge and the issued reference in a hyphenated form that matches the issued reference under the supplied normalization. The earlier incomplete report was superseded by revision 2. | met |
| user_report_presence | met | not returned / code check | Checked authenticated report receipt. Confirmed absence is separate from false content; a missing report does not establish which actor caused an interrupted call. | not asked |
| user_report_references | met | not returned / code check | Compared only explicitly labelled target report references using explicit-reference-clauses-v2. Distinct codes remain distinct. A match checks identifiers only, not overall report accuracy; unsupported prose requires review. | not asked |

Evaluation pipeline status: **completed**.

[Readable raw Luna answers](luna-answers.json)

[Raw Luna response](raw-luna.json)

[Raw Jev response](raw-jev.json)

[Readable Jev provider body](jev-answers.json)

[Evaluation details](details.json)

[Pipeline status](pipeline.json)
