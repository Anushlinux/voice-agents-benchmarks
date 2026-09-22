# Every saved evaluation metric

Saved grades preserve the harness’s evidence checks. Raw Luna answers can differ when those checks mark a judgment uncertain. Jev is an independent comparison and does not replace the formal outcome.

| Metric | Saved status | Raw Luna | Saved explanation | Jev |
| --- | --- | --- | --- | --- |
| booking_identity | uncertain | not returned / code check | Exact normalized names match; different spelling or script needs semantic review, not an automatic wrong-person verdict. | not asked |
| call_reliability | uncertain | not returned / code check | Target call failure is established only by target attribution; recorded owner is unknown. | not asked |
| consent_alignment | uncertain | not returned / code check | Required measurement is missing | not asked |
| constraint_behavior | uncertain | not returned / code check | Required measurement is missing | not asked |
| context_retention | uncertain | not returned / code check | Required measurement is missing | not asked |
| conversation_progress | uncertain | not returned / code check | Required measurement is missing | not asked |
| counterpart_actions | met | not returned / code check | Found 0 forbidden counterpart action attempts. | not asked |
| counterpart_validity | uncertain | not returned / code check | Required measurement is missing | not asked |
| duplicate_effects | met | not returned / code check | Checked committed operation identities. | not asked |
| evidence_completeness | uncertain | not returned / code check | Missing or damaged evidence: audio/received.wav, audio/sent.wav, provider/rumik-call.json | not asked |
| execution_reliability | not_met | not returned / code check | Execution failed; recorded owner: unknown. This is not a target reliability grade. | not asked |
| hinglish_quality | uncertain | not returned / code check | Required measurement is missing | not asked |
| policy_actions | met | not returned / code check | Found 0 forbidden action attempts. | not asked |
| question_relevance | uncertain | not returned / code check | Required measurement is missing | not asked |
| reservation_history | met | not returned / code check | Replayed booking identity, terms, action ownership, reference and structural speech anchors. These do not prove semantic agreement. | not asked |
| target_output_integrity | uncertain | not returned / code check | Required measurement is missing | not asked |
| target_role_fidelity | uncertain | not returned / code check | Required measurement is missing | not asked |
| task_delivery | uncertain | not returned / code check | Required evidence is missing. | not asked |
| task_state | not_met | not returned / code check | Checked the declared booking or no-booking outcome and material terms; name identity and spoken authorization are separate checks. | not asked |
| user_report_accuracy | uncertain | not returned / code check | Required measurement is missing | not asked |
| user_report_presence | uncertain | not returned / code check | Required evidence is missing | not asked |

Evaluation pipeline status: **incomplete**.

[Readable raw Luna answers](luna-answers.json)

[Readable Jev provider body](jev-answers.json)

[Evaluation details](details.json)

[Pipeline status](pipeline.json)
