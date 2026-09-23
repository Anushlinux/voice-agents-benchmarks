# 09 Sana Khan — Muga

[Back to model](../README.md) · [Back to report](../../../README.md)

Expected outcome: **no booking**. Recorded business outcome: **no booking** (matches).
Simulation validity: **invalid**. Formal outcome: **unresolved**. Deterministic checks: not all met. Private report: missing. Ending: ConversationTimeout.

| Metric | Value |
| --- | --- |
| Call duration | 127 s |
| TTFS ms mean / p50 / p90 / p95 | 2,259 / 2,259 / 2,259 / 2,259 (n=1) |
| TTFT per employee turn ms | — (n=0) |
| Provider LLM first byte ms | — (n=0) |
| WER (ASR-to-ASR) | 15.2% |
| Highest completion tokens in a turn | — |
| Luna not met / uncertain | counterpart_validity, constraint_behavior, context_retention, conversation_progress |
| Jev not met / uncertain | constraint_behavior, target_role_fidelity, question_relevance, context_retention, conversation_progress |
| Luna = Jev | 5/8 |

## Files

- [conversation.mp3](conversation.mp3) — synchronized recording; left channel restaurant employee, right channel Rumik.
- [transcript.md](transcript.md) — independent transcription of the recording (gpt-4o-mini-transcribe).
- [hosted-transcript.md](hosted-transcript.md) — Rumik's own saved transcript, including what its speech recognition heard.
- [evaluation.md](evaluation.md) — every metric with the judge's explanation, timing table and pipeline status.
- [private-report.txt](private-report.txt) — the exact report Rumik sent to its user through the authenticated tool.
- [measurements-v2.json](measurements-v2.json), [turn-timestamps.csv](turn-timestamps.csv), [diagnostics-v1.json](diagnostics-v1.json) — raw measurements.

## Private report

> (no private report was received)

Raw evidence: `artifacts/9e75406e-6e55-4eda-aaf2-9864a630ae05/30098486-a9ff-4352-8ab8-b989078c47f0/`.
