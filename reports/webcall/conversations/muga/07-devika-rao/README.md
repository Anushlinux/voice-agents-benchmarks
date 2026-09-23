# 07 Devika Rao — Muga

[Back to model](../README.md) · [Back to report](../../../README.md)

Expected outcome: **book**. Recorded business outcome: **no booking** (does not match).
Simulation validity: **invalid**. Formal outcome: **unresolved**. Deterministic checks: not all met. Private report: received. Ending: counterpart_finish.

| Metric | Value |
| --- | --- |
| Call duration | 131 s |
| TTFS ms mean / p50 / p90 / p95 | 2,825 / 2,475 / 3,655 / 3,655 (n=4) |
| TTFT per employee turn ms | — (n=0) |
| Provider LLM first byte ms | — (n=0) |
| WER (ASR-to-ASR) | 14.0% |
| Highest completion tokens in a turn | — |
| Luna not met / uncertain | counterpart_validity, user_report_accuracy, context_retention |
| Jev not met / uncertain | counterpart_validity, constraint_behavior, target_role_fidelity, question_relevance, context_retention, conversation_progress |
| Luna = Jev | 2/8 |

## Files

- [conversation.mp3](conversation.mp3) — synchronized recording; left channel restaurant employee, right channel Rumik.
- [transcript.md](transcript.md) — independent transcription of the recording (gpt-4o-mini-transcribe).
- [hosted-transcript.md](hosted-transcript.md) — Rumik's own saved transcript, including what its speech recognition heard.
- [evaluation.md](evaluation.md) — every metric with the judge's explanation, timing table and pipeline status.
- [private-report.txt](private-report.txt) — the exact report Rumik sent to its user through the authenticated tool.
- [measurements-v2.json](measurements-v2.json), [turn-timestamps.csv](turn-timestamps.csv), [diagnostics-v1.json](diagnostics-v1.json) — raw measurements.

## Private report

> No reservation could be made because on 2026-10-08 at 19:30 indoor regular table for 8 guests with a package under INR 13000 was not available at Saffron Terrace, Koregaon Park.

Raw evidence: `artifacts/9e75406e-6e55-4eda-aaf2-9864a630ae05/b1f30e14-b556-4b90-a48e-b09bd4a99dc2/`.
