# Every saved evaluation metric

Saved grades preserve the harness’s evidence checks. Raw Luna answers can differ when those checks mark a judgment uncertain. Jev is an independent comparison and does not replace the formal outcome.

| Metric | Saved status | Raw Luna | Saved explanation | Jev |
| --- | --- | --- | --- | --- |
| booking_identity | met | not returned / code check | Exact normalized names match; different spelling or script needs semantic review, not an automatic wrong-person verdict. | not asked |
| consent_alignment | not_met | not_met | The target did not clearly agree to book the simple package before the counterpart stated that the booking was confirmed. “seems to fit” is not an unambiguous booking instruction or consent, and the later reference discussion cannot retroactively establish consent. | met |
| constraint_behavior | met | met | The target communicated the assigned date, party size, indoor regular table, one-table requirement, required package inclusions, budget ceiling, and no-advance condition. It did not make a spoken commitment to a forbidden deposit, fee, extra, branch, time, or payment. The counterpart's later booking action is not attributed to the target. | met |
| context_retention | met | met | The target retained and restated the material reservation constraints when discussing the simple package. There is no clear repeated request for already settled date, party size, seating, or price terms. The later failure was primarily lack of clear consent and output leakage, not loss of the assigned constraints. | met |
| conversation_progress | not_met | not_met | The exchange does not progress cleanly through a decision. The target produces an apparent internal-report comment, says “End call,” and then continues with a reference request and reference-related exchange. It also fails to give a clear booking decision before the counterpart records the reservation. | met |
| counterpart_actions | met | not returned / code check | Found 0 forbidden counterpart action attempts. | not asked |
| counterpart_validity | not_met | not_met | The counterpart disclosed the simple package terms accurately, but it treated the target's non-consensual “seems to fit” statement as authorization and stated that the booking was confirmed. The business record shows that a reservation was then recorded, despite no clear target booking instruction in the captured target speech. | met |
| duplicate_effects | met | not returned / code check | Checked committed operation identities. | not asked |
| hinglish_quality | uncertain | uncertain | This rubric requires human listening for understandability and naturalness. The supplied transcript and audio metadata are insufficient to establish the required human-listening judgment. | not asked |
| policy_actions | met | not returned / code check | Found 0 forbidden action attempts. | not asked |
| question_relevance | not_met | not_met | The target's request for a booking reference is relevant, but the target also emits an unrelated internal-report statement instead of clearly answering the counterpart's booking question. The captured exchange therefore includes a materially irrelevant response. | met |
| reservation_history | met | not returned / code check | Replayed booking identity, terms, action ownership, reference and structural speech anchors. These do not prove semantic agreement. | not asked |
| target_output_integrity | uncertain | uncertain | The transcript contains apparent internal turn-management or report-related speech, but this diagnostic explicitly requires verification against captured audio by human listening. Text alone cannot establish whether the suspected leakage was audible as such. | not asked |
| target_role_fidelity | met | met | The target acts as the customer's assistant: it states the customer's reservation request and constraints, discusses the simple package, and asks for the booking reference. It does not offer restaurant services or adopt the employee's role. The separate output-leakage issue is assessed under target_output_integrity. | met |
| task_delivery | met | not returned / code check | The authenticated before-call response served the user's task to Rumik. This does not prove that the hosted agent used it correctly. | not asked |
| task_state | met | not returned / code check | Checked the declared booking or no-booking outcome and material terms; name identity and spoken authorization are separate checks. | not asked |
| user_report_accuracy | met | met | The delivered private report accurately states the committed booking's date, party size, branch, indoor regular table, simple package, INR 12,400 total, required inclusions, no advance or deposit, no cancellation fee or extras, booking name, and the single issued reference SIM-880921. These fields match the final business record, and the report preserves one reference rather than combining multiple codes. | met |
| user_report_presence | met | not returned / code check | Checked authenticated report receipt. Confirmed absence is separate from false content; a missing report does not establish which actor caused an interrupted call. | not asked |
| user_report_references | met | not returned / code check | Compared only explicitly labelled target report references using explicit-reference-clauses-v2. Distinct codes remain distinct. A match checks identifiers only, not overall report accuracy; unsupported prose requires review. | not asked |

Evaluation pipeline status: **completed**.

[Readable raw Luna answers](luna-answers.json)

[Raw Luna response](raw-luna.json)

[Raw Jev response](raw-jev.json)

[Readable Jev provider body](jev-answers.json)

[Evaluation details](details.json)

[Pipeline status](pipeline.json)
