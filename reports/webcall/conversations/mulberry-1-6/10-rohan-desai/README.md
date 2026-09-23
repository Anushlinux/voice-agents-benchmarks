# 10 Rohan Desai — Mulberry 1.6

[Back to model](../README.md) · [Back to report](../../../README.md)

Expected outcome: **no booking**. Recorded business outcome: **no booking** (matches).
Simulation validity: **valid**. Formal outcome: **failed**. Deterministic checks: all met. Private report: received. Ending: target_hangup.

| Metric | Value |
| --- | --- |
| Call duration | 60 s |
| TTFS ms mean / p50 / p90 / p95 | — (n=0) |
| TTFT per employee turn ms | 1,075 / 808 / 1,944 / 1,944 (n=3) |
| Provider LLM first byte ms | 387 / 339 / 367 / 1,371 (n=11) |
| WER (ASR-to-ASR) | 8.7% |
| Highest completion tokens in a turn | 215 |
| Luna not met / uncertain | user_report_accuracy |
| Jev not met / uncertain | none |
| Luna = Jev | 7/8 |

## Files

- [conversation.mp3](conversation.mp3) — synchronized recording; left channel restaurant employee, right channel Rumik.
- [transcript.md](transcript.md) — independent transcription of the recording (gpt-4o-mini-transcribe).
- [hosted-transcript.md](hosted-transcript.md) — Rumik's own saved transcript, including what its speech recognition heard.
- [evaluation.md](evaluation.md) — every metric with the judge's explanation, timing table and pipeline status.
- [private-report.txt](private-report.txt) — the exact report Rumik sent to its user through the authenticated tool.
- [measurements-v2.json](measurements-v2.json), [turn-timestamps.csv](turn-timestamps.csv), [diagnostics-v1.json](diagnostics-v1.json) — raw measurements.

## Private report

> Reservation not booked because onion‑garlic free meals are not available.

Raw evidence: `artifacts/8c9f849c-c24c-416c-8b41-8d8a4cddd92e/1fb8bc73-81f2-4404-be31-d5fe9095d13c/`.
