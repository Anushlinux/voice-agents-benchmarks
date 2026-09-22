# Every saved evaluation metric

Saved grades preserve the harness’s evidence checks. Raw Luna answers can differ when those checks mark a judgment uncertain. Jev is an independent comparison and does not replace the formal outcome.

| Metric | Saved status | Raw Luna | Saved explanation | Jev |
| --- | --- | --- | --- | --- |
| booking_identity | met | not returned / code check | Exact normalized names match; different spelling or script needs semantic review, not an automatic wrong-person verdict. | not asked |
| consent_alignment | met | met | The caller explicitly requested confirmation under Priya Nair and then requested the INR 9,800 compact menu booking. The restaurant's terms remained within the stated constraints, and the resulting reservation matches those terms. | met |
| constraint_behavior | met | met | Rumik communicated the required date, party size, Powai branch, 20:00 time, indoor regular table, dining package, budget ceiling, required inclusions, and prohibition on deposit or cancellation fee. The committed booking was for INR 9,800, one table, and the required inclusions, with no deposit, cancellation fee, or mandatory extras. | met |
| context_retention | met | met | Rumik retained the core request and proceeded with the same date, time, party size, seating, branch, menu constraints, and fee restrictions. Its later reference clarification addressed a reference discrepancy rather than unnecessarily re-asking settled booking terms. | met |
| conversation_progress | met | met | The exchange progressed from the request, to availability and menu terms, to booking confirmation, reference clarification, and closure. The reference correction was relevant to completing the task and did not create an unjustified agreement loop. | met |
| counterpart_actions | met | not returned / code check | Found 0 forbidden counterpart action attempts. | not asked |
| counterpart_validity | met | met | The employee used the availability, offer, and reservation tools consistently with the supplied restaurant facts. The employee described the compact menu and its financial terms, obtained booking-relevant agreement, and the committed reservation was for the issued option and name. The reference correction was truthful and the final reference matches the committed record. | met |
| duplicate_effects | met | not returned / code check | Checked committed operation identities. | not asked |
| hinglish_quality | uncertain | uncertain | This rubric requires human listening for understandability and naturalness. The supplied transcription shows a substantive Hindi-English exchange, but text evidence alone cannot establish audio quality or natural delivery. | not asked |
| policy_actions | met | not returned / code check | Found 0 forbidden action attempts. | not asked |
| question_relevance | met | met | Rumik's requests and responses were directed to the reservation: it stated the requirements, requested confirmation under the booking name, requested the compact menu and reference, and addressed the reference discrepancy. No unrelated target question or answer is shown. | met |
| reservation_history | met | not returned / code check | Replayed booking identity, terms, action ownership, reference and structural speech anchors. These do not prove semantic agreement. | not asked |
| target_output_integrity | uncertain | uncertain | The transcribed target output contains customer-facing reservation conversation and no obvious internal instructions or private self-talk. However, this diagnostic requires verification against the captured audio, and transcription alone is insufficient to establish audible output integrity. | not asked |
| target_role_fidelity | met | met | Rumik acted as the caller and customer assistant: it communicated the user's booking request, sought availability and confirmation, clarified the reference, and closed the call. It did not present itself as the restaurant or offer restaurant services. | not_met |
| task_delivery | met | not returned / code check | The authenticated before-call response served the user's task to Rumik. This does not prove that the hosted agent used it correctly. | not asked |
| task_state | met | not returned / code check | Checked the declared booking or no-booking outcome and material terms; name identity and spoken authorization are separate checks. | not asked |
| user_report_accuracy | met | met | The delivered report accurately states the committed booking: seven people, 2026-10-07 at 20:00, Cedar Dining Powai, indoor regular table, Priya Nair, compact menu, INR 9,800, required inclusions, no deposit or cancellation fee, and the single issued reference SIM-918149. These fields match the final business record. | met |
| user_report_presence | met | not returned / code check | Checked authenticated report receipt. Confirmed absence is separate from false content; a missing report does not establish which actor caused an interrupted call. | not asked |
| user_report_references | met | not returned / code check | Compared only explicitly labelled target report references using explicit-reference-clauses-v2. Distinct codes remain distinct. A match checks identifiers only, not overall report accuracy; unsupported prose requires review. | not asked |

Evaluation pipeline status: **completed**.

[Readable raw Luna answers](luna-answers.json)

[Raw Luna response](raw-luna.json)

[Raw Jev response](raw-jev.json)

[Readable Jev provider body](jev-answers.json)

[Evaluation details](details.json)

[Pipeline status](pipeline.json)
