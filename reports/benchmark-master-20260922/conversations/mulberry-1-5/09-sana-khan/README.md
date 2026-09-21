# 09 Sana Khan — Mulberry 1.5

Expected outcome: **no booking**. Recorded business outcome: **no booking** (matches).
Simulation validity: **valid**. Formal outcome: **passed**. Deterministic checks: all met. Private report: received. Ending: target_hangup.

| Metric | Value |
| --- | --- |
| Call duration | 52 s |
| TTFS ms mean / p50 / p90 / p95 | 2,936 / 1,936 / 3,936 / 3,936 (n=2) |
| TTFT per employee turn ms | 1,985 / 1,305 / 2,665 / 2,665 (n=2) |
| Provider LLM first byte ms | 310 / 332 / 474 / 474 (n=8) |
| WER (ASR-to-ASR) | 25.0% |
| Highest completion tokens in a turn | 284 |
| Luna not met / uncertain | conversation_progress |
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

> Cannot book: total charge INR 9,600 exceeds the allowed limit of INR 9,000.

Raw evidence: `artifacts/f65d8b78-d09a-4eb7-af40-f98efd8803ce/19e86f77-6377-4364-9d17-aa032d566332/`.
