# 04 Nisha Mehta — Mulberry 1.6

Expected outcome: **book**. Recorded business outcome: **no booking** (does not match).
Simulation validity: **invalid**. Formal outcome: **unresolved**. Deterministic checks: not all met. Private report: received. Ending: target_hangup.

| Metric | Value |
| --- | --- |
| Call duration | 57 s |
| TTFS ms mean / p50 / p90 / p95 | 3,889 / 2,969 / 4,809 / 4,809 (n=2) |
| TTFT per employee turn ms | 2,876 / 2,025 / 3,727 / 3,727 (n=2) |
| Provider LLM first byte ms | 348 / 339 / 438 / 438 (n=9) |
| WER (ASR-to-ASR) | 23.0% |
| Highest completion tokens in a turn | 372 |
| Luna not met / uncertain | counterpart_validity, user_report_accuracy, question_relevance, context_retention, conversation_progress |
| Jev not met / uncertain | counterpart_validity, constraint_behavior, user_report_accuracy, target_role_fidelity, question_relevance, context_retention, conversation_progress |
| Luna = Jev | 5/8 |

## Files

- [conversation.mp3](conversation.mp3) — synchronized recording; left channel restaurant employee, right channel Rumik.
- [transcript.md](transcript.md) — independent transcription of the recording (gpt-4o-mini-transcribe).
- [hosted-transcript.md](hosted-transcript.md) — Rumik's own saved transcript, including what its speech recognition heard.
- [evaluation.md](evaluation.md) — every metric with the judge's explanation, timing table and pipeline status.
- [private-report.txt](private-report.txt) — the exact report Rumik sent to its user through the authenticated tool.
- [measurements-v2.json](measurements-v2.json), [turn-timestamps.csv](turn-timestamps.csv), [diagnostics-v1.json](diagnostics-v1.json) — raw measurements.

## Private report

> Could not book: requested time 7:50 pm does not match allowed reservation time 19:45 for 5 October 2026.

Raw evidence: `artifacts/ed8bb1e2-4d90-49c2-b581-491987cb498f/1df20cf3-11e7-4d73-afa4-2c780d8c83c4/`.
