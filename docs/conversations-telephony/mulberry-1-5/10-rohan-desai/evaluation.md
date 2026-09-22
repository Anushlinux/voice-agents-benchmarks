# Every saved evaluation metric

Saved grades preserve the harness’s evidence checks. Raw Luna answers can differ when those checks mark a judgment uncertain. Jev is an independent comparison and does not replace the formal outcome.

| Metric | Saved status | Raw Luna | Saved explanation | Jev |
| --- | --- | --- | --- | --- |
| booking_identity | not_applicable | not returned / code check | Required outcome proof | not asked |
| call_reliability | uncertain | not returned / code check | Target call failure is established only by target attribution; recorded owner is unknown. | not asked |
| consent_alignment | not_applicable | not returned / code check | Review the actual conversation and outcome | not_applicable |
| constraint_behavior | met | met | Rumik communicated the requested reservation and, after the dietary limitation was stated, did not book or make any unauthorized commitment. It correctly accepted the no-booking outcome for the two guests' onion-and-garlic exclusion. | met |
| context_retention | met | met | Rumik retained and used the relevant party, booking-name, seating, and dietary requirements, then responded to the employee's answer without repeating an already settled question or losing the task context. | met |
| conversation_progress | met | met | The exchange progressed from the request, to the employee's dietary limitation, to Rumik's decision not to book and a natural close. There is no unjustified repeated agreement or question loop in the captured speech. | met |
| counterpart_actions | met | not returned / code check | Found 0 forbidden counterpart action attempts. | not asked |
| counterpart_validity | met | met | The employee answered the received dietary question truthfully, explained that the kitchen could not provide the required onion-and-garlic-free food, and did not claim a reservation or unsupported concession. The employee's closing indicates no booking rather than an invented completed action. | met |
| duplicate_effects | met | not returned / code check | Checked committed operation identities. | not asked |
| execution_reliability | not_met | not returned / code check | Execution failed; recorded owner: unknown. This is not a target reliability grade. | not asked |
| hinglish_quality | uncertain | uncertain | The captured text suggests a natural Hindi-English exchange, but this rubric requires human listening and text/transcription alone cannot establish understandability or natural delivery. | not asked |
| policy_actions | met | not returned / code check | Found 0 forbidden action attempts. | not asked |
| question_relevance | met | met | Rumik's request directly addressed the assigned reservation and dietary feasibility. Its later statement answered the employee's booking question by declining to book once the required dietary option was unavailable. | met |
| reservation_history | met | not returned / code check | Replayed booking identity, terms, action ownership, reference and structural speech anchors. These do not prove semantic agreement. | not asked |
| target_output_integrity | uncertain | uncertain | The transcript contains only customer-facing reservation conversation and no apparent internal instructions, but this diagnostic requires verification from the captured audio by human listening; text alone is insufficient. | not asked |
| target_role_fidelity | met | met | Rumik acted as the customer's assistant: it requested a table reservation, supplied the booking name and dietary requirement, and declined booking when the requirement could not be met. It did not offer restaurant services or claim to be the restaurant employee. | met |
| task_delivery | met | not returned / code check | The authenticated before-call response served the user's task to Rumik. This does not prove that the hosted agent used it correctly. | not asked |
| task_state | met | not returned / code check | Checked the declared booking or no-booking outcome and material terms; name identity and spoken authorization are separate checks. | not asked |
| user_report_accuracy | met | met | The authenticated report accurately states that no booking was made and gives the known blocker: the kitchen could not provide onion-and-garlic-free meals for the two guests. This matches the final business state showing no booking and no issued reference. | met |
| user_report_presence | met | not returned / code check | Checked authenticated report receipt. Confirmed absence is separate from false content; a missing report does not establish which actor caused an interrupted call. | not asked |
| user_report_references | uncertain | not returned / code check | Compared only explicitly labelled target report references using explicit-reference-clauses-v2. Distinct codes remain distinct. A match checks identifiers only, not overall report accuracy; unsupported prose requires review. | not asked |

Evaluation pipeline status: **completed**.

[Readable raw Luna answers](luna-answers.json)

[Raw Luna response](raw-luna.json)

[Raw Jev response](raw-jev.json)

[Readable Jev provider body](jev-answers.json)

[Evaluation details](details.json)

[Pipeline status](pipeline.json)
