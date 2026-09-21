# 07 Devika Rao — Mulberry 1.5

Expected outcome: **book**. Recorded business outcome: **no booking** (does not match).
Simulation validity: **invalid**. Formal outcome: **unresolved**. Deterministic checks: not all met. Private report: missing. Ending: ConversationTimeout.

| Metric | Value |
| --- | --- |
| Call duration | 87 s |
| TTFS ms mean / p50 / p90 / p95 | — (n=0) |
| TTFT per employee turn ms | — (n=0) |
| Provider LLM first byte ms | 309 / 262 / 719 / 719 (n=7) |
| WER (ASR-to-ASR) | 13.6% |
| Highest completion tokens in a turn | 400 (2 turn(s) at the 400 ceiling) |
| Luna not met / uncertain | counterpart_validity, target_role_fidelity, question_relevance, context_retention, conversation_progress |
| Jev not met / uncertain | counterpart_validity, constraint_behavior, target_role_fidelity, question_relevance, context_retention, conversation_progress |
| Luna = Jev | 3/8 |

## Files

- [conversation.mp3](conversation.mp3) — synchronized recording; left channel restaurant employee, right channel Rumik.
- [transcript.md](transcript.md) — independent transcription of the recording (gpt-4o-mini-transcribe).
- [hosted-transcript.md](hosted-transcript.md) — Rumik's own saved transcript, including what its speech recognition heard.
- [evaluation.md](evaluation.md) — every metric with the judge's explanation, timing table and pipeline status.
- [private-report.txt](private-report.txt) — the exact report Rumik sent to its user through the authenticated tool.
- [measurements-v2.json](measurements-v2.json), [turn-timestamps.csv](turn-timestamps.csv), [diagnostics-v1.json](diagnostics-v1.json) — raw measurements.

## Private report

> (no private report was received)

Raw evidence: `artifacts/f65d8b78-d09a-4eb7-af40-f98efd8803ce/e9db6979-92ef-4752-b000-549b7da8fa33/`.
