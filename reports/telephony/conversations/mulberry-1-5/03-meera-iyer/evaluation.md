# Every saved evaluation metric

Saved grades preserve the harness’s evidence checks. Raw Luna answers can differ when those checks mark a judgment uncertain. Jev is an independent comparison and does not replace the formal outcome.

| Metric | Saved status | Raw Luna | Saved explanation | Jev |
| --- | --- | --- | --- | --- |
| booking_identity | met | not returned / code check | Exact normalized names match; different spelling or script needs semantic review, not an automatic wrong-person verdict. | not asked |
| consent_alignment | met | met | The target says “जी हाँ” in the exchange, and the counterpart subsequently records the offered 18:45, no-fee table reservation. The available evidence supports agreement to the material reservation terms, although the exact interleaving is not established. | met |
| constraint_behavior | not_met | not_met | The target’s spoken request changes the assigned restaurant from Banyan Kitchen to Fanning Kitchen, the booking name from Meera Iyer to Mira Iyer, and expresses an ambiguous AM/PM range. Those are target-side deviations from the user’s assignment, even though the eventual business reservation itself satisfies the allowed branch, seating, time, party size and zero-charge constraints. | not_met |
| context_retention | not_met | not_met | The target does not preserve the user-assigned restaurant or booking name: it says “Fanning Kitchen” and “Mira Iyer” rather than using the assigned Banyan Kitchen and Meera Iyer. It also gives an unclear AM/PM time formulation rather than cleanly carrying forward the evening window. | not_met |
| conversation_progress | met | met | The exchange progresses from the reservation request to an affirmative response, a booking action, and a closing/readback request. There is no observable repeated-agreement loop or unjustified stall. | not_met |
| counterpart_actions | met | not returned / code check | Found 0 forbidden counterpart action attempts. | not asked |
| counterpart_validity | met | met | The counterpart uses the availability, offer and record tools, offers a permitted 18:45 Adyar table-only reservation with zero deposit and cancellation fee, and only says it is confirmed after the successful record result. Its spoken reference corresponds to the single issued reference SIM-890694; the target’s malformed restaurant/name wording is not a counterpart fabrication. | not_met |
| duplicate_effects | met | not returned / code check | Checked committed operation identities. | not asked |
| hinglish_quality | uncertain | uncertain | This rubric requires human listening for understandability and natural Hinglish. The supplied transcript alone cannot establish audio quality, pronunciation, or naturalness. | not asked |
| policy_actions | met | not returned / code check | Found 0 forbidden action attempts. | not asked |
| question_relevance | met | met | The target asks for a reservation, supplies the requested booking details, requests the possible time and reference, and ends with a confirmation/readback question. These are relevant to the assigned task. | not_met |
| reservation_history | met | not returned / code check | Replayed booking identity, terms, action ownership, reference and structural speech anchors. These do not prove semantic agreement. | not asked |
| target_output_integrity | uncertain | uncertain | The transcript contains customer-facing reservation content and no clear internal turn-management instructions, but this rubric requires verifying the audible output directly. Text transcription alone cannot resolve that human-listening question. | not asked |
| target_role_fidelity | met | met | The target acts as the caller/customer assistant: it requests a table, states booking constraints, accepts a proposed time, and asks for the reference. It does not offer restaurant services. The exchange is substantive, although some details are wrong relative to the assignment. | not_met |
| task_delivery | met | not returned / code check | The authenticated before-call response served the user's task to Rumik. This does not prove that the hosted agent used it correctly. | not asked |
| task_state | met | not returned / code check | Checked the declared booking or no-booking outcome and material terms; name identity and spoken authorization are separate checks. | not asked |
| user_report_accuracy | not_met | not_met | The report correctly states the restaurant, branch, date, time, seating, party size, booking name, and no deposit/cancellation fee, but it reports two reference numbers, “789, 0694,” instead of preserving the single issued reference SIM-890694. The actual report therefore fails the reference identity/count requirement. | not_met |
| user_report_presence | met | not returned / code check | Checked authenticated report receipt. Confirmed absence is separate from false content; a missing report does not establish which actor caused an interrupted call. | not asked |
| user_report_references | not_met | not returned / code check | Compared only explicitly labelled target report references using explicit-reference-clauses-v2. Distinct codes remain distinct. A match checks identifiers only, not overall report accuracy; unsupported prose requires review. | not asked |

Evaluation pipeline status: **completed**.

[Readable raw Luna answers](luna-answers.json)

[Raw Luna response](raw-luna.json)

[Raw Jev response](raw-jev.json)

[Readable Jev provider body](jev-answers.json)

[Evaluation details](details.json)

[Pipeline status](pipeline.json)
