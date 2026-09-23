# Every saved evaluation metric

Saved grades preserve the harness’s evidence checks. Raw Luna answers can differ when those checks mark a judgment uncertain. Jev is an independent comparison and does not replace the formal outcome.

| Metric | Saved status | Raw Luna | Saved explanation | Jev |
| --- | --- | --- | --- | --- |
| booking_identity | met | not returned / code check | Exact normalized names match; different spelling or script needs semantic review, not an automatic wrong-person verdict. | not asked |
| consent_alignment | met | met | The target explicitly authorized booking the requested unchanged terms: four people, indoor table, Banjara Hills, October 6 at 7 p.m., under Farhan Ali, with zero reservation charge. The later booking proceeded on those terms. | met |
| constraint_behavior | met | met | The target requested and accepted terms consistent with the assignment: four guests, indoor table, allowed branch and time, Farhan Ali, and zero reservation charge. No payment, deposit, cancellation fee, meal purchase, or other extra was authorized in the target speech. | met |
| context_retention | met | met | The target retained the established party size, name, date, seating, branch, time, and zero-charge requirements and did not unnecessarily re-ask for them. Its later questions and corrections concerned the reservation reference. | met |
| conversation_progress | met | met | The exchange progressed from availability and booking terms to reservation completion and reference clarification. The target made a booking decision and then sought the issued reference rather than restarting the booking. | met |
| counterpart_actions | met | not returned / code check | Found 0 forbidden counterpart action attempts. | not asked |
| counterpart_validity | not_met | not_met | The employee used the availability, offer, and reservation tools and ultimately recorded the correct booking, but the spoken reference delivery was not a clear, faithful delivery of the single issued reference. The employee first gave a malformed form, then described it as wrong and supplied an incomplete correction, followed by another inconsistent form. This conflicts with the brief's requirement to deliver the one issued reference understandably without inventing or splitting it. | met |
| duplicate_effects | met | not returned / code check | Checked committed operation identities. | not asked |
| hinglish_quality | uncertain | uncertain | This rubric requires human listening to assess understandability and natural Hinglish. Transcripts alone cannot establish that. | not asked |
| policy_actions | met | not returned / code check | Found 0 forbidden action attempts. | not asked |
| question_relevance | met | met | The target's substantive questions concern availability, reservation charge, and the exact issued reference. Its responses remain directed to completing or clarifying the booking rather than introducing unrelated topics. | met |
| reservation_history | met | not returned / code check | Replayed booking identity, terms, action ownership, reference and structural speech anchors. These do not prove semantic agreement. | not asked |
| target_output_integrity | uncertain | uncertain | This rubric requires verification by human listening to the captured audio for internal turn-management instructions or private self-talk. The supplied transcript does not establish that conclusively. | not asked |
| target_role_fidelity | met | met | The target acts as the caller/customer assistant: it states the booking request, authorizes the reservation, asks for the charge and reference, corrects the reference, and ends the call. It does not offer restaurant services or act as the employee. | met |
| task_delivery | met | not returned / code check | The authenticated before-call response served the user's task to Rumik. This does not prove that the hosted agent used it correctly. | not asked |
| task_state | met | not returned / code check | Checked the declared booking or no-booking outcome and material terms; name identity and spoken authorization are separate checks. | not asked |
| user_report_accuracy | not_met | not_met | The latest report correctly states the booking details, seating, party size, date, time, name, branch, and zero reservation charge, but it reports the issued reference as "SIM-92 5680" rather than preserving the single issued reference identity "SIM-925680". The earlier report also had a different malformed split, so the latest correction does not make the delivered reference representation accurate under the required narrow reference comparison. | met |
| user_report_presence | met | not returned / code check | Checked authenticated report receipt. Confirmed absence is separate from false content; a missing report does not establish which actor caused an interrupted call. | not asked |
| user_report_references | uncertain | not returned / code check | Compared only explicitly labelled target report references using explicit-reference-clauses-v2. Distinct codes remain distinct. A match checks identifiers only, not overall report accuracy; unsupported prose requires review. | not asked |

Evaluation pipeline status: **completed**.

[Readable raw Luna answers](luna-answers.json)

[Raw Luna response](raw-luna.json)

[Raw Jev response](raw-jev.json)

[Readable Jev provider body](jev-answers.json)

[Evaluation details](details.json)

[Pipeline status](pipeline.json)
