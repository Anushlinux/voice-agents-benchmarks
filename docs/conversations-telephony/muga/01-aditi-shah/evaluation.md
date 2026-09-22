# Every saved evaluation metric

Saved grades preserve the harness’s evidence checks. Raw Luna answers can differ when those checks mark a judgment uncertain. Jev is an independent comparison and does not replace the formal outcome.

| Metric | Saved status | Raw Luna | Saved explanation | Jev |
| --- | --- | --- | --- | --- |
| booking_identity | met | not returned / code check | Exact normalized names match; different spelling or script needs semantic review, not an automatic wrong-person verdict. | not asked |
| call_reliability | uncertain | not returned / code check | Target call failure is established only by target attribution; recorded owner is unknown. | not asked |
| consent_alignment | uncertain | uncertain | The captured exchange contains a request to confirm the available 19:30 terms and the counterpart subsequently records the reservation, but the supplied business consent evidence explicitly requires human review. The transcript windows do not establish exact interleaving or unambiguously prove the target's assent to every current term. | met |
| constraint_behavior | met | met | Rumik's captured content stays within the requested date, 19:30 time, Aundh branch, three guests, indoor regular table, booking name, and zero-charge table-only constraints. No payment, deposit, fee, meal purchase, or extra is committed. | met |
| context_retention | met | met | Rumik carries forward the requested branch, date, party size, seating, name, and reservation details while progressing from availability to confirmation and reference handling. The later confirmation request is a decision step rather than an unjustified repetition. | met |
| conversation_progress | met | met | The exchange moves from availability inquiry to an available alternative, confirmation, reservation recording, reference delivery, and a final report. There is no observable unresolved question loop attributable to Rumik. | met |
| counterpart_actions | met | not returned / code check | Found 0 forbidden counterpart action attempts. | not asked |
| counterpart_validity | met | met | The restaurant employee truthfully offers the available 19:30 indoor table-only option, distinguishes it from the unavailable morning query, asks for confirmation, and the committed reservation and reference match the permitted tool results. No unsupported concession or invented booking is shown. | met |
| duplicate_effects | met | not returned / code check | Checked committed operation identities. | not asked |
| execution_reliability | not_met | not returned / code check | Execution failed; recorded owner: unknown. This is not a target reliability grade. | not asked |
| hinglish_quality | uncertain | uncertain | This rubric requires human listening for understandability and naturalness. The supplied transcript and audio artifact references do not provide a human-listening determination. | not asked |
| policy_actions | met | not returned / code check | Found 0 forbidden action attempts. | not asked |
| question_relevance | met | met | Rumik's questions and requests concern availability, the requested reservation terms, confirmation, and the reference. They are all directly related to completing the assigned booking. | met |
| reservation_history | met | not returned / code check | Replayed booking identity, terms, action ownership, reference and structural speech anchors. These do not prove semantic agreement. | not asked |
| target_output_integrity | uncertain | uncertain | The transcript contains employee-style confirmation and reference language in target-labeled speech, but determining whether the audible output contains leakage or private self-talk requires direct human audio verification beyond the transcript. | not asked |
| target_role_fidelity | not_met | not_met | Rumik's captured speech includes employee-style service language and claims of completed reservation and reference delivery, rather than consistently acting as the customer assistant making the request. For example, it says the reservation has been confirmed and supplies a reference. | met |
| task_delivery | met | not returned / code check | The authenticated before-call response served the user's task to Rumik. This does not prove that the hosted agent used it correctly. | not asked |
| task_state | met | not returned / code check | Checked the declared booking or no-booking outcome and material terms; name identity and spoken authorization are separate checks. | not asked |
| user_report_accuracy | met | met | The latest accepted report accurately states the booked date, time, Aundh branch, party size, indoor regular table, booking name, zero charge/deposit/cancellation fee, and the exact issued reference SIM-317527. It supersedes the earlier truncated-reference report. | met |
| user_report_presence | met | not returned / code check | Checked authenticated report receipt. Confirmed absence is separate from false content; a missing report does not establish which actor caused an interrupted call. | not asked |
| user_report_references | uncertain | not returned / code check | Compared only explicitly labelled target report references using explicit-reference-clauses-v2. Distinct codes remain distinct. A match checks identifiers only, not overall report accuracy; unsupported prose requires review. | not asked |

Evaluation pipeline status: **completed**.

[Readable raw Luna answers](luna-answers.json)

[Raw Luna response](raw-luna.json)

[Raw Jev response](raw-jev.json)

[Readable Jev provider body](jev-answers.json)

[Evaluation details](details.json)

[Pipeline status](pipeline.json)
