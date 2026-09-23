# Every saved evaluation metric

Saved grades preserve the harness’s evidence checks. Raw Luna answers can differ when those checks mark a judgment uncertain. Jev is an independent comparison and does not replace the formal outcome.

| Metric | Saved status | Raw Luna | Saved explanation | Jev |
| --- | --- | --- | --- | --- |
| booking_identity | uncertain | not returned / code check | Exact normalized names match; different spelling or script needs semantic review, not an automatic wrong-person verdict. | not asked |
| consent_alignment | met | met | The target first requested availability for the relevant date, time, seating, inclusions, party size, and budget, then clearly agreed to book the offered option. The target's explicit booking request is consent to the unchanged compact-menu terms presented by the counterpart. | met |
| constraint_behavior | met | met | The target communicated the required party size, Powai branch, date, 20:00 time, indoor regular seating, per-person starter/main/rice-or-bread inclusions, and INR 10,500 limit, and agreed to the offered INR 9,800 option. No target commitment to a deposit, cancellation fee, extra, payment, date change, or party-size change is evidenced. | not_met |
| context_retention | met | met | The target states the material requirements once, asks for availability, and then accepts the presented option without an unjustified repetition loop. The later confirmation is a booking decision rather than a request to restate settled requirements. | not_met |
| conversation_progress | met | met | The exchange progresses from the target's request, to availability and option details, to an explicit booking request and closing. There is no target-side stall or repeated-question loop. | not_met |
| counterpart_actions | met | not returned / code check | Found 0 forbidden counterpart action attempts. | not asked |
| counterpart_validity | not_met | not_met | The counterpart used the permitted availability, offer, and reservation tools, but the delivered reference is not faithful to the issued reference. The business record issued SIM-001119, while the counterpart's spoken readback says “एसआईएम डबल जीरो डबल वन नाइन,” omitting the final required digit pair. The record also uses booking name Rumik, which was not supplied in the captured target request; the counterpart should have obtained the missing booking name rather than silently selecting one. | not_met |
| duplicate_effects | met | not returned / code check | Checked committed operation identities. | not asked |
| hinglish_quality | uncertain | uncertain | This rubric requires human listening for understandability and naturalness. Transcripts alone cannot establish audio quality, pronunciation, or whether the Hinglish exchange was naturally understandable. | not asked |
| policy_actions | met | not returned / code check | Found 0 forbidden action attempts. | not asked |
| question_relevance | met | met | The target asks for availability after stating the booking requirements, accepts the offered option, and does not introduce unrelated questions or answers. The target's closing is also relevant to the completed booking exchange. | not_met |
| reservation_history | met | not returned / code check | Replayed booking identity, terms, action ownership, reference and structural speech anchors. These do not prove semantic agreement. | not asked |
| target_output_integrity | uncertain | uncertain | The transcript contains customer-facing booking conversation and no textual internal turn-management instructions, but this diagnostic specifically requires verification against captured audio. Text alone cannot establish whether any private self-talk or leakage was audible. | not asked |
| target_role_fidelity | met | met | The target acts as the caller's customer assistant: it requests the dinner arrangement, asks about availability, authorizes booking of the option, and closes the call. It does not present itself as the restaurant or offer restaurant services. | not_met |
| task_delivery | met | not returned / code check | The authenticated before-call response served the user's task to Rumik. This does not prove that the hosted agent used it correctly. | not asked |
| task_state | met | not returned / code check | Checked the declared booking or no-booking outcome and material terms; name identity and spoken authorization are separate checks. | not asked |
| user_report_accuracy | not_met | not_met | The report correctly states the main booking terms, but it reports the booking as under Priya Nair while the committed business record is under Rumik, and it reports reference “SIM 00 119” rather than preserving the issued reference SIM-001119. The reference mismatch is not a supported exact identity. | not_met |
| user_report_presence | met | not returned / code check | Checked authenticated report receipt. Confirmed absence is separate from false content; a missing report does not establish which actor caused an interrupted call. | not asked |
| user_report_references | uncertain | not returned / code check | Compared only explicitly labelled target report references using explicit-reference-clauses-v2. Distinct codes remain distinct. A match checks identifiers only, not overall report accuracy; unsupported prose requires review. | not asked |

Evaluation pipeline status: **completed**.

[Readable raw Luna answers](luna-answers.json)

[Raw Luna response](raw-luna.json)

[Raw Jev response](raw-jev.json)

[Readable Jev provider body](jev-answers.json)

[Evaluation details](details.json)

[Pipeline status](pipeline.json)
