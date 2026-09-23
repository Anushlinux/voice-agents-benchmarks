# 01 Aditi Shah — Mulberry 1.6

[Back to model](../README.md) · [Back to report](../../../README.md)

Expected outcome: **book**. Recorded business outcome: **book** (matches).
Simulation validity: **valid**. Formal outcome: **passed**. Deterministic checks: all met. Private report: received. Ending: target_hangup.

| Metric | Value |
| --- | --- |
| Call duration | 138 s |
| TTFS ms mean / p50 / p90 / p95 | 2,685 / 2,337 / 4,017 / 4,017 (n=8) |
| TTFT per employee turn ms | 1,650 / 1,341 / 2,863 / 2,863 (n=6) |
| Provider LLM first byte ms | 329 / 337 / 440 / 447 (n=25) |
| WER (ASR-to-ASR) | 23.9% |
| Highest completion tokens in a turn | 400 (3 turn(s) at the 400 ceiling) |
| Luna not met / uncertain | none |
| Jev not met / uncertain | none |
| Luna = Jev | 8/8 |

## Files

- [conversation.mp3](conversation.mp3) — synchronized recording; left channel restaurant employee, right channel Rumik.
- [transcript.md](transcript.md) — independent transcription of the recording (gpt-4o-mini-transcribe).
- [hosted-transcript.md](hosted-transcript.md) — Rumik's own saved transcript, including what its speech recognition heard.
- [evaluation.md](evaluation.md) — every metric with the judge's explanation, timing table and pipeline status.
- [private-report.txt](private-report.txt) — the exact report Rumik sent to its user through the authenticated tool.
- [measurements-v2.json](measurements-v2.json), [turn-timestamps.csv](turn-timestamps.csv), [diagnostics-v1.json](diagnostics-v1.json) — raw measurements.

## Private report

> Booked indoor regular table for 3 on 2026-10-02 at 19:30 under name Aditi Shah, no reservation charge, reference SIM-98-5180.

Raw evidence: `artifacts/ed8bb1e2-4d90-49c2-b581-491987cb498f/c394b6c7-ba66-45a3-8c67-d61ed8a1b388/`.
