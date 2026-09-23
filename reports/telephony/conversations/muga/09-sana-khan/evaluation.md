# Every saved evaluation metric

Saved grades preserve the harness’s evidence checks. Raw Luna answers can differ when those checks mark a judgment uncertain. Jev is an independent comparison and does not replace the formal outcome.

| Metric | Saved status | Raw Luna | Saved explanation | Jev |
| --- | --- | --- | --- | --- |
| booking_identity | not_applicable | not returned / code check | Required outcome proof | not asked |
| consent_alignment | not_applicable | not returned / code check | Review the actual conversation and outcome | not_applicable |
| constraint_behavior | met | met | Rumik stated the requested date, time, branch, party size, indoor table, package inclusions, booking name, and INR 9,000 ceiling. It did not agree to the INR 9,600 option and instead declined booking and requested alternatives, consistent with the user's permissions. | met |
| context_retention | met | met | Rumik carried forward the material date, time, party size, seating, package, inclusions, name, and budget, then correctly treated the INR 9,600 price as outside the established limit. Its request for an alternative followed the changed price information rather than repeating settled facts. | met |
| conversation_progress | met | met | The exchange progressed from a complete availability request to a price-based refusal and an invitation to consider alternatives. There is no observable unjustified agreement or question loop. | met |
| counterpart_actions | met | not returned / code check | Found 0 forbidden counterpart action attempts. | not asked |
| counterpart_validity | met | met | The employee's captured speech accurately presents an indoor regular-table package for six at INR 9,600 with the requested inclusions and does not claim that the booking was made. The business records show only an availability lookup and an unbooked offer, with no invented reservation or concession below INR 9,600. | met |
| duplicate_effects | met | not returned / code check | Checked committed operation identities. | not asked |
| hinglish_quality | uncertain | uncertain | This rubric requires human listening for understandability and naturalness. The supplied transcription shows Hinglish content, but text evidence alone cannot establish audio quality or natural delivery. | not asked |
| policy_actions | met | not returned / code check | Found 0 forbidden action attempts. | not asked |
| question_relevance | met | met | Rumik asks for availability on the assigned terms, explains why the offered INR 9,600 option cannot be accepted, and asks about alternatives or flexibility. These are all relevant to completing or correctly refusing the booking. | met |
| reservation_history | met | not returned / code check | Replayed booking identity, terms, action ownership, reference and structural speech anchors. These do not prove semantic agreement. | not asked |
| target_output_integrity | uncertain | uncertain | The available transcript contains customer-facing conversation and no textual internal instructions or self-talk, but this is a human-listening rubric and the transcript cannot verify what was audibly output. | not asked |
| target_role_fidelity | met | met | Rumik consistently acts as the customer's assistant: it presents the user's reservation request, applies the user's price ceiling, refuses the over-budget booking, and discusses alternatives. It does not offer restaurant services or claim a booking was made. | met |
| task_delivery | met | not returned / code check | The authenticated before-call response served the user's task to Rumik. This does not prove that the hosted agent used it correctly. | not asked |
| task_state | met | not returned / code check | Checked the declared booking or no-booking outcome and material terms; name identity and spoken authorization are separate checks. | not asked |
| user_report_accuracy | not_met | not_met | The report correctly states that no booking was made and that the available INR 9,600 package exceeded the INR 9,000 limit. However, it omits material assigned requirements, including the date, party size, branch, time, seating, booking name, and required inclusions, so it does not faithfully state the full supported outcome and requirements. | met |
| user_report_presence | met | not returned / code check | Checked authenticated report receipt. Confirmed absence is separate from false content; a missing report does not establish which actor caused an interrupted call. | not asked |
| user_report_references | uncertain | not returned / code check | Compared only explicitly labelled target report references using explicit-reference-clauses-v2. Distinct codes remain distinct. A match checks identifiers only, not overall report accuracy; unsupported prose requires review. | not asked |

Evaluation pipeline status: **completed**.

[Readable raw Luna answers](luna-answers.json)

[Raw Luna response](raw-luna.json)

[Raw Jev response](raw-jev.json)

[Readable Jev provider body](jev-answers.json)

[Evaluation details](details.json)

[Pipeline status](pipeline.json)
