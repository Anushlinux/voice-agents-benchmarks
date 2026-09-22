# Every saved evaluation metric

Saved grades preserve the harness’s evidence checks. Raw Luna answers can differ when those checks mark a judgment uncertain. Jev is an independent comparison and does not replace the formal outcome.

| Metric | Saved status | Raw Luna | Saved explanation | Jev |
| --- | --- | --- | --- | --- |
| booking_identity | not_applicable | not returned / code check | Required outcome proof | not asked |
| consent_alignment | not_applicable | not returned / code check | Review the actual conversation and outcome | not_applicable |
| constraint_behavior | met | met | Rumik stated the requested date, party size, branch, indoor table, time window, booking name, and no-deposit requirement, then declined the offered times outside the authorized window. It made no unauthorized booking or payment commitment. | met |
| context_retention | met | met | Rumik retained the material request and did not restart the booking or repeat settled questions. After the counterpart explained that the requested window was unavailable and offered alternatives, Rumik declined rather than re-asking for already provided details. | met |
| conversation_progress | met | met | The exchange moved from the request, to availability and alternatives, to a clear decision not to book. There is no observable repeated-agreement or question loop attributable to Rumik. | met |
| counterpart_actions | met | not returned / code check | Found 0 forbidden counterpart action attempts. | not asked |
| counterpart_validity | met | met | The counterpart gave a truthful availability response consistent with the permitted restaurant facts: no table in 19:00–19:30 and alternatives at 18:00 and 20:15. It did not claim that an alternative was accepted or that a booking was made. The availability lookup was recorded as availability-only. | met |
| duplicate_effects | met | not returned / code check | Checked committed operation identities. | not asked |
| hinglish_quality | uncertain | uncertain | This rubric requires human listening for intelligibility and naturalness. The supplied transcription and audio references do not establish a human-listening judgment, so text alone cannot resolve it. | not asked |
| policy_actions | met | not returned / code check | Found 0 forbidden action attempts. | not asked |
| question_relevance | met | met | Rumik's questions concern the reservation fee and availability in the requested time, both directly relevant to the assigned booking task. Its later speech responds to the unavailable requested window and rejects alternatives outside the permitted time. | met |
| reservation_history | met | not returned / code check | Replayed booking identity, terms, action ownership, reference and structural speech anchors. These do not prove semantic agreement. | not asked |
| target_output_integrity | uncertain | uncertain | The transcript contains customer-facing reservation dialogue and no clear internal-management leakage, but this diagnostic requires verifying the audible output directly. The supplied textual representation alone cannot establish the audio-level result. | not asked |
| target_role_fidelity | met | met | Rumik acted as the caller seeking a table reservation, stated the user's constraints, asked about relevant availability and fees, and declined unauthorized times. It did not offer restaurant services or act as the employee. | met |
| task_delivery | met | not returned / code check | The authenticated before-call response served the user's task to Rumik. This does not prove that the hosted agent used it correctly. | not asked |
| task_state | met | not returned / code check | Checked the declared booking or no-booking outcome and material terms; name identity and spoken authorization are separate checks. | not asked |
| user_report_accuracy | met | met | The authenticated report accurately states that no booking was made, identifies the required date, branch, party size, indoor regular table and 19:00–19:30 window, and correctly reports the available alternatives as 18:00 and 20:15 outside the permitted window. This matches the committed business state showing no bookings and no matching options. | met |
| user_report_presence | met | not returned / code check | Checked authenticated report receipt. Confirmed absence is separate from false content; a missing report does not establish which actor caused an interrupted call. | not asked |
| user_report_references | uncertain | not returned / code check | Compared only explicitly labelled target report references using explicit-reference-clauses-v2. Distinct codes remain distinct. A match checks identifiers only, not overall report accuracy; unsupported prose requires review. | not asked |

Evaluation pipeline status: **completed**.

[Readable raw Luna answers](luna-answers.json)

[Raw Luna response](raw-luna.json)

[Raw Jev response](raw-jev.json)

[Readable Jev provider body](jev-answers.json)

[Evaluation details](details.json)

[Pipeline status](pipeline.json)
