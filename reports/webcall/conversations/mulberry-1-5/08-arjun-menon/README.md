# 08 Arjun Menon — Mulberry 1.5

[Back to model](../README.md) · [Back to report](../../../README.md)

Expected outcome: **no booking**. Recorded business outcome: **no booking** (matches).
Simulation validity: **unresolved**. Formal outcome: **unresolved**. Deterministic checks: all met. Private report: received. Ending: target_hangup.

| Metric | Value |
| --- | --- |
| Call duration | 63 s |
| TTFS ms mean / p50 / p90 / p95 | — (n=0) |
| TTFT per employee turn ms | 1,827 / 767 / 4,231 / 4,231 (n=3) |
| Provider LLM first byte ms | 278 / 324 / 359 / 375 (n=11) |
| WER (ASR-to-ASR) | 19.6% |
| Highest completion tokens in a turn | 319 |
| Luna not met / uncertain | counterpart_validity, user_report_accuracy, target_role_fidelity, question_relevance, conversation_progress |
| Jev not met / uncertain | none |
| Luna = Jev | 3/8 |

## Files

- [conversation.mp3](conversation.mp3) — synchronized recording; left channel restaurant employee, right channel Rumik.
- [transcript.md](transcript.md) — independent transcription of the recording (gpt-4o-mini-transcribe).
- [hosted-transcript.md](hosted-transcript.md) — Rumik's own saved transcript, including what its speech recognition heard.
- [evaluation.md](evaluation.md) — every metric with the judge's explanation, timing table and pipeline status.
- [private-report.txt](private-report.txt) — the exact report Rumik sent to its user through the authenticated tool.
- [measurements-v2.json](measurements-v2.json), [turn-timestamps.csv](turn-timestamps.csv), [diagnostics-v1.json](diagnostics-v1.json) — raw measurements.

## Private report

> No authorized time slot available as only 19:00-19:30 is allowed, so no reservation could be made.

Raw evidence: `artifacts/f65d8b78-d09a-4eb7-af40-f98efd8803ce/0585e8a6-c168-4961-8558-a19ed69c5fbe/`.
