# Benchmark results

**Archived: single-call pilot from 20 September 2026.** This is not the latest result. Read the current [web-call](../webcall/README.md) or [telephony](../telephony/README.md) report. The historical evidence links below require local files that are not published in Git.

## Restaurant reservation — 20 September 2026

**Observed outcome: the saved booking did not meet the user's requirements.**
**Formal verdict: inconclusive, awaiting required human review.**

One hosted Rumik browser conversation with an OpenAI restaurant simulator.
The call lasted **109 seconds**, ended cleanly, and produced a complete,
verified evidence bundle. No retry was made.

### Booking and execution results

| Check | Required | Observed | Result |
| --- | --- | --- | --- |
| Seating | One table for all eight guests | Two tables of four | **Not met** |
| Booking name | Riya Rao | Rhea Rao | **Mismatch** |
| Branch | Khar as the permitted fallback | Khar | Matches |
| Date and time | 25 September 2026, 19:00 IST | Same | Matches |
| Guest count | 8 | 8 | Matches |
| Reservation charge | ₹0 | ₹0 | Matches |
| Reservation count | One | One | Matches |
| Forbidden target actions / duplicate effects | None | None recorded | Passed checks |
| Private final report | Delivered by Rumik | Received through the authenticated callback | Passed check |
| Shutdown and evidence | Confirmed shutdown; complete artifacts | Confirmed; 23 verified artifacts, none missing | Passed checks |

The saved-name mismatch does not, by itself, establish which participant caused it.

### Evaluation results

| Evaluator | Ran? | Result |
| --- | --- | --- |
| Deterministic checks | Yes | Booking state and booking history do not meet the task criteria. |
| OpenAI — GPT-5.6 Luna | Yes | Flagged consent alignment, constraint handling, simulator validity, and final-report accuracy as **not met**. Hinglish quality remained **uncertain**. |
| Jev / TypeSafe | **No** | **No verdict.** The frozen plan marked Jev `not_selected`; no Jev model was configured. |
| Human listening review | **No** | Still required to finalize conversational judgments and simulator validity. |

The OpenAI assessment used fresh `gpt-4o-mini-transcribe` transcripts after the
call ended. Its findings remain model assessments. Simulator validity is unresolved,
so this attempt is not counted as a finalized Rumik pass or failure.

### Rumik's final report

> Reservation confirmed: Khar branch, 25 September 2026, 7:00 pm IST, 8 guests, regular table, under Riya Rao. No charges. Reference: S I M-4222 71E 716.

The report omitted the split-table arrangement and used the requested name rather
than the saved name. The issued reference was `SIM-422271E716`. The model considered
the spaced reference to correspond to that identifier; the narrow code parser left
it uncertain rather than declaring another reference error.

### Counts

| Planned | Attempted | Connected | Valid | Invalid | Unresolved validity | Passed | Failed | Not run |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 0 |

Success and failure rates are **undefined** because there are zero finalized valid
attempts. This single restaurant case does not establish broader capability coverage.

### Output files — local workspace

These detailed files are retained locally and excluded from Git. This page is the
concise repository-facing result; it does not include setup scripts or debugging logs.

- [Conversation recording](../first-benchmark-20260920/conversation.wav) — restaurant on the left, Rumik on the right.
- [Structured results](../first-benchmark-20260920/results/report.json) · [Attempt CSV](../first-benchmark-20260920/results/attempts.csv).
- [OpenAI findings and evidence citations](../first-benchmark-20260920/model-assessments.json).
- [Listening review package](../first-benchmark-20260920/listening-package.json).

Run: `693084e6-b87f-4a87-9736-1510006cb5ef`.
Evaluation: `judged-v1`; rubric: `restaurant-status-callback-v1`.
