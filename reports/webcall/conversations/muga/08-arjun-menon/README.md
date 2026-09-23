# 08 Arjun Menon — Muga

[Back to model](../README.md) · [Back to report](../../../README.md)

Expected outcome: **no booking**. Recorded business outcome: **no booking** (matches).
Simulation validity: **valid**. Formal outcome: **failed**. Deterministic checks: all met. Private report: received. Ending: counterpart_finish.

| Metric | Value |
| --- | --- |
| Call duration | 96 s |
| TTFS ms mean / p50 / p90 / p95 | 2,664 / 2,351 / 3,331 / 3,331 (n=3) |
| TTFT per employee turn ms | — (n=0) |
| Provider LLM first byte ms | — (n=0) |
| WER (ASR-to-ASR) | 18.6% |
| Highest completion tokens in a turn | — |
| Luna not met / uncertain | constraint_behavior |
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

> No booking made. Reason: No indoor regular table free reservation available for 3 guests on 2026-10-09 between 19:00 and 19:30 at River Mint Fort Kochi, as only slots at 18:00 and 20:15 are offered, which are outside the allowed window.

Raw evidence: `artifacts/9e75406e-6e55-4eda-aaf2-9864a630ae05/6a659edd-2f38-4e7a-ac42-a422303687f1/`.
