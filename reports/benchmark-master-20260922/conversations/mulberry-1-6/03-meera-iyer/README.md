# 03 Meera Iyer — Mulberry 1.6

Expected outcome: **book**. Recorded business outcome: **book** (matches).
Simulation validity: **invalid**. Formal outcome: **unresolved**. Deterministic checks: all met. Private report: received. Ending: target_hangup.

| Metric | Value |
| --- | --- |
| Call duration | 92 s |
| TTFS ms mean / p50 / p90 / p95 | 2,627 / 2,323 / 3,803 / 3,803 (n=5) |
| TTFT per employee turn ms | 1,561 / 1,403 / 2,641 / 2,641 (n=5) |
| Provider LLM first byte ms | 247 / 293 / 343 / 350 (n=20) |
| WER (ASR-to-ASR) | 25.6% |
| Highest completion tokens in a turn | 400 (2 turn(s) at the 400 ceiling) |
| Luna not met / uncertain | counterpart_validity, user_report_accuracy |
| Jev not met / uncertain | none |
| Luna = Jev | — |

## Files

- [conversation.mp3](conversation.mp3) — synchronized recording; left channel restaurant employee, right channel Rumik.
- [transcript.md](transcript.md) — independent transcription of the recording (gpt-4o-mini-transcribe).
- [hosted-transcript.md](hosted-transcript.md) — Rumik's own saved transcript, including what its speech recognition heard.
- [evaluation.md](evaluation.md) — every metric with the judge's explanation, timing table and pipeline status.
- [private-report.txt](private-report.txt) — the exact report Rumik sent to its user through the authenticated tool.
- [measurements-v2.json](measurements-v2.json), [turn-timestamps.csv](turn-timestamps.csv), [diagnostics-v1.json](diagnostics-v1.json) — raw measurements.

## Private report

> Booked indoor regular table for 2 at Banyan Kitchen Adyar on 2026-10-04 at 19:30 under Meera Iyer, no charge, reference 14712.

Raw evidence: `artifacts/ed8bb1e2-4d90-49c2-b581-491987cb498f/11305410-de36-4d83-a8c0-fa5b8a689888/`.
