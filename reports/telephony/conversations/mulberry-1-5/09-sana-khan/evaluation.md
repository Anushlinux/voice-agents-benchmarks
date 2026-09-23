# Every saved evaluation metric

Saved grades preserve the harness’s evidence checks. Raw Luna answers can differ when those checks mark a judgment uncertain. Jev is an independent comparison and does not replace the formal outcome.

| Metric | Saved status | Raw Luna | Saved explanation | Jev |
| --- | --- | --- | --- | --- |
| booking_identity | not_applicable | not returned / code check | Required outcome proof | not asked |
| consent_alignment | not_applicable | not returned / code check | Review the actual conversation and outcome | not_applicable |
| constraint_behavior | uncertain | met | Required measurement is missing | met |
| context_retention | uncertain | met | Required measurement is missing | met |
| conversation_progress | uncertain | met | Required measurement is missing | met |
| counterpart_actions | met | not returned / code check | Found 0 forbidden counterpart action attempts. | not asked |
| counterpart_validity | uncertain | met | Required measurement is missing | met |
| duplicate_effects | met | not returned / code check | Checked committed operation identities. | not asked |
| hinglish_quality | uncertain | uncertain | Required measurement is missing | not asked |
| policy_actions | met | not returned / code check | Found 0 forbidden action attempts. | not asked |
| question_relevance | uncertain | met | Required measurement is missing | met |
| reservation_history | met | not returned / code check | Replayed booking identity, terms, action ownership, reference and structural speech anchors. These do not prove semantic agreement. | not asked |
| target_output_integrity | uncertain | uncertain, uncertain | Required measurement is missing | not asked |
| target_role_fidelity | uncertain | met | Required measurement is missing | met |
| task_delivery | met | not returned / code check | The authenticated before-call response served the user's task to Rumik. This does not prove that the hosted agent used it correctly. | not asked |
| task_state | met | not returned / code check | Checked the declared booking or no-booking outcome and material terms; name identity and spoken authorization are separate checks. | not asked |
| user_report_accuracy | uncertain | met | Required measurement is missing | met |
| user_report_presence | met | not returned / code check | Checked authenticated report receipt. Confirmed absence is separate from false content; a missing report does not establish which actor caused an interrupted call. | not asked |
| user_report_references | uncertain | not returned / code check | Compared only explicitly labelled target report references using explicit-reference-clauses-v2. Distinct codes remain distinct. A match checks identifiers only, not overall report accuracy; unsupported prose requires review. | not asked |

Evaluation pipeline status: **incomplete**.

[Readable raw Luna answers](luna-answers.json)

[Raw Luna response](raw-luna.json)

[Raw Jev response](raw-jev.json)

[Readable Jev provider body](jev-answers.json)

[Evaluation details](details.json)

[Pipeline status](pipeline.json)
