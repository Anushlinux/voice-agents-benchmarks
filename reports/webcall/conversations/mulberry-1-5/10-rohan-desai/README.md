# 10 Rohan Desai — Mulberry 1.5

[Back to model](../README.md) · [Back to report](../../../README.md)

Expected outcome: **no booking**. Recorded business outcome: **no booking** (matches).
Simulation validity: **valid**. Formal outcome: **passed**. Deterministic checks: all met. Private report: received. Ending: counterpart_finish.

| Metric | Value |
| --- | --- |
| Call duration | 77 s |
| TTFS ms mean / p50 / p90 / p95 | 2,693 / 2,223 / 3,163 / 3,163 (n=2) |
| TTFT per employee turn ms | 1,993 / 1,568 / 2,419 / 2,419 (n=2) |
| Provider LLM first byte ms | 352 / 329 / 496 / 496 (n=7) |
| WER (ASR-to-ASR) | 8.7% |
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

> No booking was made because the kitchen cannot meet the onion‑ and garlic‑free requirement for the two guests.

Raw evidence: `artifacts/f65d8b78-d09a-4eb7-af40-f98efd8803ce/9cf03508-2129-4fb5-9abb-6c6dd5b29979/`.
