# 05 Farhan Ali — Mulberry 1.5

Expected outcome: **book**. Recorded business outcome: **book** (matches).
Simulation validity: **valid**. Formal outcome: **failed**. Deterministic checks: not all met. Private report: received. Ending: counterpart_finish.

| Metric | Value |
| --- | --- |
| Call duration | 81 s |
| TTFS ms mean / p50 / p90 / p95 | 2,571 / 2,584 / 3,104 / 3,104 (n=3) |
| TTFT per employee turn ms | 1,885 / 2,003 / 2,473 / 2,473 (n=3) |
| Provider LLM first byte ms | 292 / 293 / 365 / 417 (n=10) |
| WER (ASR-to-ASR) | 18.5% |
| Highest completion tokens in a turn | 400 (1 turn(s) at the 400 ceiling) |
| Luna not met / uncertain | constraint_behavior, context_retention |
| Jev not met / uncertain | counterpart_validity, constraint_behavior, target_role_fidelity, question_relevance, context_retention, conversation_progress |
| Luna = Jev | 4/8 |

## Files

- [conversation.mp3](conversation.mp3) — synchronized recording; left channel restaurant employee, right channel Rumik.
- [transcript.md](transcript.md) — independent transcription of the recording (gpt-4o-mini-transcribe).
- [hosted-transcript.md](hosted-transcript.md) — Rumik's own saved transcript, including what its speech recognition heard.
- [evaluation.md](evaluation.md) — every metric with the judge's explanation, timing table and pipeline status.
- [private-report.txt](private-report.txt) — the exact report Rumik sent to its user through the authenticated tool.
- [measurements-v2.json](measurements-v2.json), [turn-timestamps.csv](turn-timestamps.csv), [diagnostics-v1.json](diagnostics-v1.json) — raw measurements.

## Private report

> Booked 6 Oct 2026 at 7:30pm indoor regular table for 4 under Farhan Ali, no charge, reference SIM-641022

Raw evidence: `artifacts/f65d8b78-d09a-4eb7-af40-f98efd8803ce/11403373-e2eb-4fe4-83b0-e2f9d0c3a603/`.
