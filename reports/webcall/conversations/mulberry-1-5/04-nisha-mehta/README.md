# 04 Nisha Mehta — Mulberry 1.5

[Back to model](../README.md) · [Back to report](../../../README.md)

Expected outcome: **book**. Recorded business outcome: **book** (matches).
Simulation validity: **valid**. Formal outcome: **failed**. Deterministic checks: all met. Private report: received. Ending: counterpart_finish.

| Metric | Value |
| --- | --- |
| Call duration | 92 s |
| TTFS ms mean / p50 / p90 / p95 | 2,565 / 2,625 / 3,125 / 3,125 (n=3) |
| TTFT per employee turn ms | 1,830 / 2,016 / 2,283 / 2,283 (n=3) |
| Provider LLM first byte ms | 292 / 315 / 413 / 440 (n=14) |
| WER (ASR-to-ASR) | 20.2% |
| Highest completion tokens in a turn | 336 |
| Luna not met / uncertain | constraint_behavior, user_report_accuracy |
| Jev not met / uncertain | none |
| Luna = Jev | 6/8 |

## Files

- [conversation.mp3](conversation.mp3) — synchronized recording; left channel restaurant employee, right channel Rumik.
- [transcript.md](transcript.md) — independent transcription of the recording (gpt-4o-mini-transcribe).
- [hosted-transcript.md](hosted-transcript.md) — Rumik's own saved transcript, including what its speech recognition heard.
- [evaluation.md](evaluation.md) — every metric with the judge's explanation, timing table and pipeline status.
- [private-report.txt](private-report.txt) — the exact report Rumik sent to its user through the authenticated tool.
- [measurements-v2.json](measurements-v2.json), [turn-timestamps.csv](turn-timestamps.csv), [diagnostics-v1.json](diagnostics-v1.json) — raw measurements.

## Private report

> Booked indoor regular table for 6 on 2026-10-05 at 19:45 under Nisha Mehta, no reservation charge, reference SIM-27-1196.

Raw evidence: `artifacts/f65d8b78-d09a-4eb7-af40-f98efd8803ce/7be17052-6d5d-48ba-9fb7-f8655e748244/`.
