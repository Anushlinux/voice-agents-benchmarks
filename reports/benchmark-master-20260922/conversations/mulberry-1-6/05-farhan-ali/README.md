# 05 Farhan Ali — Mulberry 1.6

Expected outcome: **book**. Recorded business outcome: **book** (matches).
Simulation validity: **valid**. Formal outcome: **failed**. Deterministic checks: not all met. Private report: received. Ending: counterpart_finish.

| Metric | Value |
| --- | --- |
| Call duration | 74 s |
| TTFS ms mean / p50 / p90 / p95 | 2,651 / 2,384 / 3,284 / 3,284 (n=3) |
| TTFT per employee turn ms | 1,627 / 1,347 / 2,212 / 2,212 (n=3) |
| Provider LLM first byte ms | 235 / 321 / 367 / 367 (n=9) |
| WER (ASR-to-ASR) | 26.2% |
| Highest completion tokens in a turn | 400 (1 turn(s) at the 400 ceiling) |
| Luna not met / uncertain | constraint_behavior |
| Jev not met / uncertain | counterpart_validity, constraint_behavior, user_report_accuracy, target_role_fidelity, question_relevance, context_retention, conversation_progress |
| Luna = Jev | 2/8 |

## Files

- [conversation.mp3](conversation.mp3) — synchronized recording; left channel restaurant employee, right channel Rumik.
- [transcript.md](transcript.md) — independent transcription of the recording (gpt-4o-mini-transcribe).
- [hosted-transcript.md](hosted-transcript.md) — Rumik's own saved transcript, including what its speech recognition heard.
- [evaluation.md](evaluation.md) — every metric with the judge's explanation, timing table and pipeline status.
- [private-report.txt](private-report.txt) — the exact report Rumik sent to its user through the authenticated tool.
- [measurements-v2.json](measurements-v2.json), [turn-timestamps.csv](turn-timestamps.csv), [diagnostics-v1.json](diagnostics-v1.json) — raw measurements.

## Private report

> Booked 6 Oct 2026 19:30 indoor regular table for 4 under Farhan Ali at Jubilee Hills, charge INR 0, reference SIM-84-6468.

Raw evidence: `artifacts/ed8bb1e2-4d90-49c2-b581-491987cb498f/831c5bee-d6e2-4a3f-a69f-faf4c5f062f9/`.
