# 02 Kabir Sethi — Mulberry 1.6

Expected outcome: **book**. Recorded business outcome: **book** (matches).
Simulation validity: **valid**. Formal outcome: **passed**. Deterministic checks: all met. Private report: received. Ending: target_hangup.

| Metric | Value |
| --- | --- |
| Call duration | 119 s |
| TTFS ms mean / p50 / p90 / p95 | 2,640 / 2,332 / 4,092 / 4,092 (n=5) |
| TTFT per employee turn ms | 1,536 / 1,160 / 3,084 / 3,084 (n=5) |
| Provider LLM first byte ms | 322 / 330 / 469 / 505 (n=18) |
| WER (ASR-to-ASR) | 28.9% |
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

> Booked indoor regular table for five at Domlur on 3 October 2026 at 8 pm under Kabir Sethi, no charges, reference SIM-401933.

Raw evidence: `artifacts/ed8bb1e2-4d90-49c2-b581-491987cb498f/9a60190d-e54c-4bc7-8819-698584ead97a/`.
