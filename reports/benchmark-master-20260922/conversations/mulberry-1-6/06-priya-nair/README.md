# 06 Priya Nair — Mulberry 1.6

Expected outcome: **book**. Recorded business outcome: **no booking** (does not match).
Simulation validity: **invalid**. Formal outcome: **unresolved**. Deterministic checks: not all met. Private report: received. Ending: counterpart_finish.

| Metric | Value |
| --- | --- |
| Call duration | 69 s |
| TTFS ms mean / p50 / p90 / p95 | 2,819 / 2,219 / 3,419 / 3,419 (n=2) |
| TTFT per employee turn ms | 1,821 / 1,273 / 2,368 / 2,368 (n=2) |
| Provider LLM first byte ms | 293 / 318 / 349 / 349 (n=8) |
| WER (ASR-to-ASR) | 21.6% |
| Highest completion tokens in a turn | 359 |
| Luna not met / uncertain | counterpart_validity, user_report_accuracy |
| Jev not met / uncertain | counterpart_validity, constraint_behavior, target_role_fidelity, question_relevance, context_retention, conversation_progress |
| Luna = Jev | 1/8 |

## Files

- [conversation.mp3](conversation.mp3) — synchronized recording; left channel restaurant employee, right channel Rumik.
- [transcript.md](transcript.md) — independent transcription of the recording (gpt-4o-mini-transcribe).
- [hosted-transcript.md](hosted-transcript.md) — Rumik's own saved transcript, including what its speech recognition heard.
- [evaluation.md](evaluation.md) — every metric with the judge's explanation, timing table and pipeline status.
- [private-report.txt](private-report.txt) — the exact report Rumik sent to its user through the authenticated tool.
- [measurements-v2.json](measurements-v2.json), [turn-timestamps.csv](turn-timestamps.csv), [diagnostics-v1.json](diagnostics-v1.json) — raw measurements.

## Private report

> Could not make the reservation because the only available dining package exceeds the budget limit of INR 10,500 (offered at INR 11,900).

Raw evidence: `artifacts/ed8bb1e2-4d90-49c2-b581-491987cb498f/f50b65b8-d2c5-4ac0-8780-ba392ecac6af/`.
