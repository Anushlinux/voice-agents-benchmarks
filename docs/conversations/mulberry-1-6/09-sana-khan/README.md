# 09 Sana Khan — Mulberry 1.6

Expected outcome: **no booking**. Recorded business outcome: **no booking** (matches).
Simulation validity: **valid**. Formal outcome: **passed**. Deterministic checks: all met. Private report: received. Ending: target_hangup.

| Metric | Value |
| --- | --- |
| Call duration | 55 s |
| TTFS ms mean / p50 / p90 / p95 | 4,763 / 4,093 / 5,433 / 5,433 (n=2) |
| TTFT per employee turn ms | 3,756 / 3,040 / 4,472 / 4,472 (n=2) |
| Provider LLM first byte ms | 357 / 328 / 445 / 445 (n=6) |
| WER (ASR-to-ASR) | 21.6% |
| Highest completion tokens in a turn | 301 |
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

> Cannot book because the total charge of INR 9,600 exceeds the allowed limit of INR 9,000.

Raw evidence: `artifacts/ed8bb1e2-4d90-49c2-b581-491987cb498f/8344b3ec-4ed9-406f-9d64-01f835647c11/`.
