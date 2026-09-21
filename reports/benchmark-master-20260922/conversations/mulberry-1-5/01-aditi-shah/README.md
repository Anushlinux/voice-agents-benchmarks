# 01 Aditi Shah — Mulberry 1.5

Expected outcome: **book**. Recorded business outcome: **book** (matches).
Simulation validity: **invalid**. Formal outcome: **unresolved**. Deterministic checks: not all met. Private report: received. Ending: target_hangup.

| Metric | Value |
| --- | --- |
| Call duration | 98 s |
| TTFS ms mean / p50 / p90 / p95 | 2,481 / 2,216 / 3,156 / 3,156 (n=4) |
| TTFT per employee turn ms | 1,785 / 1,485 / 2,425 / 2,425 (n=4) |
| Provider LLM first byte ms | 286 / 332 / 371 / 642 (n=15) |
| WER (ASR-to-ASR) | 27.2% |
| Highest completion tokens in a turn | 366 |
| Luna not met / uncertain | counterpart_validity, constraint_behavior, context_retention |
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

> Reservation confirmed for 2 Oct 2026 at 7:30 pm for 3 people, indoor regular table, Aundh branch Neem Courtyard, under Aditi Shah, no charge, reference SIM-09-7939.

Raw evidence: `artifacts/f65d8b78-d09a-4eb7-af40-f98efd8803ce/b787571b-2d35-4137-9e42-044c600da8c6/`.
