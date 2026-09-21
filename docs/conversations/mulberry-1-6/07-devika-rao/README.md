# 07 Devika Rao — Mulberry 1.6

Expected outcome: **book**. Recorded business outcome: **book** (matches).
Simulation validity: **invalid**. Formal outcome: **unresolved**. Deterministic checks: all met. Private report: received. Ending: target_hangup.

| Metric | Value |
| --- | --- |
| Call duration | 141 s |
| TTFS ms mean / p50 / p90 / p95 | 3,280 / 3,064 / 4,424 / 4,424 (n=5) |
| TTFT per employee turn ms | 2,202 / 1,973 / 3,305 / 3,305 (n=5) |
| Provider LLM first byte ms | 269 / 319 / 364 / 365 (n=25) |
| WER (ASR-to-ASR) | 19.5% |
| Highest completion tokens in a turn | 400 (2 turn(s) at the 400 ceiling) |
| Luna not met / uncertain | counterpart_validity, consent_alignment, conversation_progress |
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

> Booked: 8 Oct 2026 19:30, Devika Rao, 8 persons, indoor regular table, total INR 12400, includes starter, main, rice/bread each, reference SIM-673238.

Raw evidence: `artifacts/8c9f849c-c24c-416c-8b41-8d8a4cddd92e/60aeb46c-929c-45c5-9420-b9bc6a342def/`.
