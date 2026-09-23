# 08 Arjun Menon — Mulberry 1.6

[Back to model](../README.md) · [Back to report](../../../README.md)

Expected outcome: **no booking**. Recorded business outcome: **no booking** (matches).
Simulation validity: **valid**. Formal outcome: **passed**. Deterministic checks: all met. Private report: received. Ending: target_hangup.

| Metric | Value |
| --- | --- |
| Call duration | 58 s |
| TTFS ms mean / p50 / p90 / p95 | 2,835 / 2,055 / 3,615 / 3,615 (n=2) |
| TTFT per employee turn ms | 1,869 / 1,172 / 2,565 / 2,565 (n=2) |
| Provider LLM first byte ms | 378 / 339 / 632 / 632 (n=9) |
| WER (ASR-to-ASR) | 20.9% |
| Highest completion tokens in a turn | 400 (1 turn(s) at the 400 ceiling) |
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

> No reservation could be made because the only available times (6:00 pm or 8:15 pm) fall outside the allowed window of 19:00‑19:30.

Raw evidence: `artifacts/ed8bb1e2-4d90-49c2-b581-491987cb498f/3d3775be-057d-4f30-8b65-99c8d755f712/`.
