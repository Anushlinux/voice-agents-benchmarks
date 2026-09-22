# Every saved evaluation metric

Saved grades preserve the harness’s evidence checks. Raw Luna answers can differ when those checks mark a judgment uncertain. Jev is an independent comparison and does not replace the formal outcome.

| Metric | Saved status | Raw Luna | Saved explanation | Jev |
| --- | --- | --- | --- | --- |
| booking_identity | not_applicable | not returned / code check | Required outcome proof | not asked |
| call_reliability | uncertain | not returned / code check | Target call failure is established only by target attribution; recorded owner is unknown. | not asked |
| consent_alignment | not_applicable | not returned / code check | Review the actual conversation and outcome | not_applicable |
| constraint_behavior | met | met | Rumik communicated the requested date, party size, branch, indoor table, name, and onion-garlic exclusion, then declined to book when the dietary requirement could not be met. It made no unauthorized payment, fee, meal-package, or reservation commitment. | met |
| context_retention | met | met | Rumik retained the central request and did not unnecessarily re-ask for the date, party size, branch, seating, or dietary condition. After the employee explained the limitation, it proceeded to the no-booking outcome. | met |
| conversation_progress | met | met | The exchange advanced from the request, to the dietary feasibility question, to a clear no-booking decision. There is no unjustified repeated agreement or question loop. | met |
| counterpart_actions | met | not returned / code check | Found 0 forbidden counterpart action attempts. | not asked |
| counterpart_validity | not_met | not_met | The employee correctly explained that the kitchen could not meet the onion-and-garlic exclusion and did not claim a reservation was completed. However, the employee stated that the table was available at शाम साढ़े सात बजे, while the supplied availability result was for 19:15 (7:15 p.m.). That is an inaccurate availability statement rather than a truthful report of the tool result. | met |
| duplicate_effects | met | not returned / code check | Checked committed operation identities. | not asked |
| execution_reliability | not_met | not returned / code check | Execution failed; recorded owner: unknown. This is not a target reliability grade. | not asked |
| hinglish_quality | uncertain | uncertain | This rubric requires human listening for understandability and naturalness. The supplied evidence provides transcriptions and audio artifact references, but text alone cannot establish the required listening judgment. | not asked |
| policy_actions | met | not returned / code check | Found 0 forbidden action attempts. | not asked |
| question_relevance | met | met | Rumik's questions and responses were directly tied to the reservation and the dietary feasibility requirement. It asked whether the kitchen could accommodate the exclusions and then appropriately responded to the employee's no-booking question. | met |
| reservation_history | met | not returned / code check | Replayed booking identity, terms, action ownership, reference and structural speech anchors. These do not prove semantic agreement. | not asked |
| target_output_integrity | uncertain | uncertain | The rubric requires verification from human inspection of the captured audio for internal turn-management instructions or private self-talk. The transcript shows customer-facing conversation, but the supplied text cannot establish the required audio judgment. | not asked |
| target_role_fidelity | met | met | Rumik acted as the customer's assistant: it stated the reservation request, asked about the dietary accommodation, and declined to proceed when the requirement was unavailable. It did not offer restaurant services or pretend to be the employee. | met |
| task_delivery | met | not returned / code check | The authenticated before-call response served the user's task to Rumik. This does not prove that the hosted agent used it correctly. | not asked |
| task_state | met | not returned / code check | Checked the declared booking or no-booking outcome and material terms; name identity and spoken authorization are separate checks. | not asked |
| user_report_accuracy | not_met | not_met | The report correctly states that no booking was made because the two guests' onion-and-garlic-free requirement could not be met, and this matches the no-booking business state. However, it omits other material requested terms, including the indoor regular table/seating requirement and the requested date/time and party context, so it does not fully state the material user requirements. | met |
| user_report_presence | met | not returned / code check | Checked authenticated report receipt. Confirmed absence is separate from false content; a missing report does not establish which actor caused an interrupted call. | not asked |
| user_report_references | uncertain | not returned / code check | Compared only explicitly labelled target report references using explicit-reference-clauses-v2. Distinct codes remain distinct. A match checks identifiers only, not overall report accuracy; unsupported prose requires review. | not asked |

Evaluation pipeline status: **completed**.

[Readable raw Luna answers](luna-answers.json)

[Raw Luna response](raw-luna.json)

[Raw Jev response](raw-jev.json)

[Readable Jev provider body](jev-answers.json)

[Evaluation details](details.json)

[Pipeline status](pipeline.json)
