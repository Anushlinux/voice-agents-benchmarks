# 03 Meera Iyer — Mulberry 1.5

[Back to model](../README.md) · [Back to report](../../../README.md)

Expected outcome: **book**. Recorded business outcome: **book** (matches).
Simulation validity: **unresolved**. Formal outcome: **unresolved**. Deterministic checks: all met. Private report: received. Ending: counterpart_finish.

| Metric | Value |
| --- | --- |
| Call duration | 101 s |
| TTFS ms mean / p50 / p90 / p95 | 2,226 / 1,916 / 3,196 / 3,196 (n=4) |
| TTFT per employee turn ms | 1,454 / 1,139 / 2,283 / 2,283 (n=4) |
| Provider LLM first byte ms | 254 / 311 / 350 / 354 (n=13) |
| WER (ASR-to-ASR) | 22.9% |
| Highest completion tokens in a turn | 400 (1 turn(s) at the 400 ceiling) |
| Luna not met / uncertain | counterpart_validity, consent_alignment, user_report_accuracy |
| Jev not met / uncertain | counterpart_validity, constraint_behavior, user_report_accuracy, target_role_fidelity, question_relevance, context_retention, conversation_progress |
| Luna = Jev | 1/8 |

## Files

- [conversation.mp3](conversation.mp3) — synchronized recording; left channel restaurant employee, right channel Rumik.
- [transcript.md](transcript.md) — independent transcription of the recording (gpt-4o-mini-transcribe).
- [hosted-transcript.md](hosted-transcript.md) — Rumik's own saved transcript, including what its speech recognition heard.
- [evaluation.md](evaluation.md) — every metric with the judge's explanation, timing table and pipeline status.
- [private-report.txt](private-report.txt) — the exact report Rumik sent to its user through the authenticated tool.
- [measurements-v2.json](measurements-v2.json), [turn-timestamps.csv](turn-timestamps.csv), [diagnostics-v1.json](diagnostics-v1.json) — raw measurements.

## Private report

> Booked indoor regular table for 2 on 2026-10-04 at 6:45 PM under Meera Iyer, no charge, reference SIM-92-691.

Raw evidence: `artifacts/f65d8b78-d09a-4eb7-af40-f98efd8803ce/9dfb4bbd-6b4b-49f5-be16-73263237b724/`.
