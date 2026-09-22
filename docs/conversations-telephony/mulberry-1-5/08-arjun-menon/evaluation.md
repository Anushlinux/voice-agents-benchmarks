# Every saved evaluation metric

Saved grades preserve the harness’s evidence checks. Raw Luna answers can differ when those checks mark a judgment uncertain. Jev is an independent comparison and does not replace the formal outcome.

| Metric | Saved status | Raw Luna | Saved explanation | Jev |
| --- | --- | --- | --- | --- |
| booking_identity | not_applicable | not returned / code check | Required outcome proof | not asked |
| consent_alignment | not_applicable | not returned / code check | Review the actual conversation and outcome | not_applicable |
| constraint_behavior | met | met | Rumik stated the requested date, party size, indoor regular table, booking name, no-deposit/no-cancellation-fee terms, and the restricted time window. It did not agree to an alternative time or any charge, and it correctly concluded that no booking was made. | met |
| context_retention | met | met | The exchange retains the requested party size, seating, date, name, and time restriction, and the target does not accept the offered out-of-window alternatives. It closes with no booking after the availability issue is communicated. | met |
| conversation_progress | met | met | The target makes the booking request, communicates the time constraint, responds to the alternatives, and ends with the correct no-booking decision rather than entering an unjustified agreement loop. | met |
| counterpart_actions | met | not returned / code check | Found 0 forbidden counterpart action attempts. | not asked |
| counterpart_validity | met | met | The counterpart truthfully states that no table is available in the requested window, identifies the two available alternatives, and does not claim a reservation or invent a reference. The final no-booking state is consistent with the restaurant record. | met |
| duplicate_effects | met | not returned / code check | Checked committed operation identities. | not asked |
| hinglish_quality | uncertain | uncertain | This rubric requires human listening for understandability and natural Hinglish. The supplied transcription alone cannot establish audio quality, naturalness, or acoustic intelligibility. | not asked |
| policy_actions | met | not returned / code check | Found 0 forbidden action attempts. | not asked |
| question_relevance | met | met | The target's questions and answers concern the requested reservation, availability, acceptable timing, and closure. No unrelated task content is evident in the captured target speech. | met |
| reservation_history | met | not returned / code check | Replayed booking identity, terms, action ownership, reference and structural speech anchors. These do not prove semantic agreement. | not asked |
| target_output_integrity | uncertain | uncertain | Whether the audible output contained internal turn-management instructions or private self-talk requires verification from the audio itself. The transcription does not prove the absence of such leakage acoustically. | not asked |
| target_role_fidelity | met | met | The target acts as the caller seeking a reservation, states the user's booking requirements, rejects unavailable times, and closes without booking. It does not present itself as the restaurant employee. | met |
| task_delivery | met | not returned / code check | The authenticated before-call response served the user's task to Rumik. This does not prove that the hosted agent used it correctly. | not asked |
| task_state | met | not returned / code check | Checked the declared booking or no-booking outcome and material terms; name identity and spoken authorization are separate checks. | not asked |
| user_report_accuracy | met | met | The private report accurately states that no qualifying indoor table for three was available in the requested Fort Kochi date/time window, that only earlier or later slots were offered, and that no reservation was made. This matches the final business state, which contains no booking and lists only 18:00 and 20:15 options. | met |
| user_report_presence | met | not returned / code check | Checked authenticated report receipt. Confirmed absence is separate from false content; a missing report does not establish which actor caused an interrupted call. | not asked |
| user_report_references | uncertain | not returned / code check | Compared only explicitly labelled target report references using explicit-reference-clauses-v2. Distinct codes remain distinct. A match checks identifiers only, not overall report accuracy; unsupported prose requires review. | not asked |

Evaluation pipeline status: **completed**.

[Readable raw Luna answers](luna-answers.json)

[Raw Luna response](raw-luna.json)

[Raw Jev response](raw-jev.json)

[Readable Jev provider body](jev-answers.json)

[Evaluation details](details.json)

[Pipeline status](pipeline.json)
