# 06 Priya Nair — Mulberry 1.5

Expected outcome: **book**. Recorded business outcome: **book** (matches).
Simulation validity: **valid**. Formal outcome: **failed**. Deterministic checks: all met. Private report: received. Ending: target_hangup.

| Metric | Value |
| --- | --- |
| Call duration | 132 s |
| TTFS ms mean / p50 / p90 / p95 | 2,371 / 2,135 / 3,075 / 3,075 (n=6) |
| TTFT per employee turn ms | 1,638 / 1,368 / 2,276 / 2,276 (n=6) |
| Provider LLM first byte ms | 270 / 320 / 383 / 454 (n=25) |
| WER (ASR-to-ASR) | 25.2% |
| Highest completion tokens in a turn | 392 |
| Luna not met / uncertain | user_report_accuracy, target_role_fidelity, question_relevance |
| Jev not met / uncertain | none |
| Luna = Jev | 5/8 |

## Files

- [conversation.mp3](conversation.mp3) — synchronized recording; left channel restaurant employee, right channel Rumik.
- [transcript.md](transcript.md) — independent transcription of the recording (gpt-4o-mini-transcribe).
- [hosted-transcript.md](hosted-transcript.md) — Rumik's own saved transcript, including what its speech recognition heard.
- [evaluation.md](evaluation.md) — every metric with the judge's explanation, timing table and pipeline status.
- [private-report.txt](private-report.txt) — the exact report Rumik sent to its user through the authenticated tool.
- [measurements-v2.json](measurements-v2.json), [turn-timestamps.csv](turn-timestamps.csv), [diagnostics-v1.json](diagnostics-v1.json) — raw measurements.

## Private report

> Reservation for 7 people on 2026-10-07 at 20:00 under Priya Nair, indoor regular table, dining package total INR 9,800, reference सिम 385061.

Raw evidence: `artifacts/f65d8b78-d09a-4eb7-af40-f98efd8803ce/49fbd498-9f9e-4d5d-8e94-53530f00c159/`.
