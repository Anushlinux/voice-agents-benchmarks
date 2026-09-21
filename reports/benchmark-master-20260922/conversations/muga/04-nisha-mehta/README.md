# 04 Nisha Mehta — Muga

Expected outcome: **book**. Recorded business outcome: **book** (matches).
Simulation validity: **invalid**. Formal outcome: **unresolved**. Deterministic checks: not all met. Private report: missing. Ending: ConversationTimeout.

| Metric | Value |
| --- | --- |
| Call duration | 157 s |
| TTFS ms mean / p50 / p90 / p95 | 2,381 / 2,261 / 2,501 / 2,501 (n=2) |
| TTFT per employee turn ms | — (n=0) |
| Provider LLM first byte ms | — (n=0) |
| WER (ASR-to-ASR) | 34.4% |
| Highest completion tokens in a turn | — |
| Luna not met / uncertain | counterpart_validity, consent_alignment, conversation_progress |
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

Raw evidence: `artifacts/9e75406e-6e55-4eda-aaf2-9864a630ae05/03b4dc38-6fa9-47e1-8667-fc7f58cfd0a5/`.
