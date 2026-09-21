# 02 Kabir Sethi — Mulberry 1.5

Expected outcome: **book**. Recorded business outcome: **book** (matches).
Simulation validity: **valid**. Formal outcome: **failed**. Deterministic checks: not all met. Private report: received. Ending: counterpart_finish.

| Metric | Value |
| --- | --- |
| Call duration | 79 s |
| TTFS ms mean / p50 / p90 / p95 | 2,408 / 2,068 / 3,188 / 3,188 (n=3) |
| TTFT per employee turn ms | 1,568 / 1,283 / 2,237 / 2,237 (n=3) |
| Provider LLM first byte ms | 294 / 321 / 346 / 350 (n=11) |
| WER (ASR-to-ASR) | 15.7% |
| Highest completion tokens in a turn | 316 |
| Luna not met / uncertain | user_report_accuracy |
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

> Booked indoor regular table for 5 at Domlur on 2026-10-03 at 20:00 under Kabir Sethi, no reservation charge, reference SIM-718266.

Raw evidence: `artifacts/f65d8b78-d09a-4eb7-af40-f98efd8803ce/8f965bce-ba03-4cba-a958-4790636c1ba4/`.
