# 02 Kabir Sethi — Muga

Expected outcome: **book**. Recorded business outcome: **book** (matches).
Simulation validity: **valid**. Formal outcome: **failed**. Deterministic checks: all met. Private report: received. Ending: counterpart_finish.

| Metric | Value |
| --- | --- |
| Call duration | 170 s |
| TTFS ms mean / p50 / p90 / p95 | 3,532 / 3,316 / 5,396 / 5,396 (n=5) |
| TTFT per employee turn ms | — (n=0) |
| Provider LLM first byte ms | — (n=0) |
| WER (ASR-to-ASR) | 50.0% |
| Highest completion tokens in a turn | — |
| Luna not met / uncertain | constraint_behavior, user_report_accuracy, context_retention |
| Jev not met / uncertain | counterpart_validity, constraint_behavior, user_report_accuracy, target_role_fidelity, question_relevance, context_retention, conversation_progress |
| Luna = Jev | 4/8 |

## Files

- [conversation.mp3](conversation.mp3) — synchronized recording; left channel restaurant employee, right channel Rumik.
- [transcript.md](transcript.md) — independent transcription of the recording (gpt-4o-mini-transcribe).
- [hosted-transcript.md](hosted-transcript.md) — Rumik's own saved transcript, including what its speech recognition heard.
- [evaluation.md](evaluation.md) — every metric with the judge's explanation, timing table and pipeline status.
- [private-report.txt](private-report.txt) — the exact report Rumik sent to its user through the authenticated tool.
- [measurements-v2.json](measurements-v2.json), [turn-timestamps.csv](turn-timestamps.csv), [diagnostics-v1.json](diagnostics-v1.json) — raw measurements.

## Private report

> Reservation confirmed: Kabir Sethi, 5 guests, indoor regular table, all together, reservation only, no charge, date 2026-10-03, time 20:00, branch Domlur, reference S4CR. All user constraints satisfied.

Raw evidence: `artifacts/9e75406e-6e55-4eda-aaf2-9864a630ae05/ef99178c-0a58-4b7c-bfc0-62ef56304fdf/`.
