# Every saved evaluation metric

Saved grades preserve the harness’s evidence checks. Raw Luna answers can differ when those checks mark a judgment uncertain. Jev is an independent comparison and does not replace the formal outcome.

| Metric | Saved status | Raw Luna | Saved explanation | Jev |
| --- | --- | --- | --- | --- |
| booking_identity | met | not returned / code check | Exact normalized names match; different spelling or script needs semantic review, not an automatic wrong-person verdict. | not asked |
| consent_alignment | met | met | The caller explicitly requested confirmation of a free indoor regular table for four at the earliest qualifying time, and the recorded offer matched those unchanged material terms. The business record shows the accepted 19:00 Banjara Hills option was saved. | met |
| constraint_behavior | met | met | The target's request and the recorded outcome preserve the authorized date, party size, allowed branch, indoor regular table, table-only booking, zero reservation charge, and no deposit or fees. The business record also confirms meals were separate and not purchased as part of the reservation. | not_met |
| context_retention | met | met | The target carried forward the booking name, date, party size, seating, branch/time window, and no-fee table-only constraints rather than unnecessarily asking the caller to restate them. The later request specifically selected the qualifying 19:00 Banjara Hills option. | met |
| conversation_progress | met | met | The exchange moved from the caller's request to availability, confirmation, reference handling, and termination without a repeated-question loop. The business audit records an availability lookup, offer, and one reservation. | met |
| counterpart_actions | met | not returned / code check | Found 0 forbidden counterpart action attempts. | not asked |
| counterpart_validity | met | met | The counterpart used the permitted availability, offer, and recording tools; the saved reservation matches the supplied option, name, and zero-fee terms. Its spoken availability and reference are consistent with the business results, and there is no evidence of an unsupported concession or invented booking. | met |
| duplicate_effects | met | not returned / code check | Checked committed operation identities. | not asked |
| hinglish_quality | uncertain | uncertain | This rubric requires human listening for understandability and naturalness. The supplied transcription alone cannot establish audio quality or natural delivery. | not asked |
| policy_actions | met | not returned / code check | Found 0 forbidden action attempts. | not asked |
| question_relevance | met | met | The target asked for the requested reservation, including the relevant date, time, branch, party size, seating, fees, and reference. Its later confirmation/reference exchange remained related to completing the booking. | met |
| reservation_history | met | not returned / code check | Replayed booking identity, terms, action ownership, reference and structural speech anchors. These do not prove semantic agreement. | not asked |
| target_output_integrity | uncertain | uncertain | This is a human-listening rubric. The transcript does not establish whether any audible output contained internal turn-management instructions or private self-talk. | not asked |
| target_role_fidelity | not_met | not_met | The target initially states the customer's request appropriately, but later speaks as though it is the restaurant confirming the booking and issuing the reference, rather than continuing as the caller/customer assistant. The target output includes “आपकी बुकिंग कन्फर्म हो गई है” and a reference readback attributed to the caller side. | met |
| task_delivery | met | not returned / code check | The authenticated before-call response served the user's task to Rumik. This does not prove that the hosted agent used it correctly. | not asked |
| task_state | met | not returned / code check | Checked the declared booking or no-booking outcome and material terms; name identity and spoken authorization are separate checks. | not asked |
| user_report_accuracy | not_met | not_met | The report correctly states the date, time, branch, party size, seating, name, and no-deposit/no-fee outcome, but it reports “PIM 856277” while the committed reservation reference is “SIM-856277.” The reference identity and prefix are materially wrong, so the report is not accurate. | not_met |
| user_report_presence | met | not returned / code check | Checked authenticated report receipt. Confirmed absence is separate from false content; a missing report does not establish which actor caused an interrupted call. | not asked |
| user_report_references | uncertain | not returned / code check | Compared only explicitly labelled target report references using explicit-reference-clauses-v2. Distinct codes remain distinct. A match checks identifiers only, not overall report accuracy; unsupported prose requires review. | not asked |

Evaluation pipeline status: **completed**.

[Readable raw Luna answers](luna-answers.json)

[Raw Luna response](raw-luna.json)

[Raw Jev response](raw-jev.json)

[Readable Jev provider body](jev-answers.json)

[Evaluation details](details.json)

[Pipeline status](pipeline.json)
