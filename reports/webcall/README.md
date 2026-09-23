# Web-call benchmark

**Latest published web-call report: 21–22 September 2026.**

[All benchmark reports](../README.md) · [All conversations and audio](conversations/README.md) · [Muga](conversations/muga/README.md) · [Mulberry 1.5](conversations/mulberry-1-5/README.md) · [Mulberry 1.6](conversations/mulberry-1-6/README.md)

Hosted [Rumik](https://rumik.ai) acts as a customer's personal assistant and talks to a simulated restaurant over browser audio to book a table. The restaurant employee is simulated by OpenAI `gpt-realtime`, which hears Rumik's actual audio and can only use the restaurant's own availability, offer and booking tools. Every call is a real full-duplex browser call to the hosted Rumik agent; nothing is scripted and no call is retried.

Ten authored Hinglish restaurant cases are used. Seven expect a booking under the customer's constraints; three expect Rumik to decline correctly because no permitted option exists. Each model ran every case once.

**Read the proof, not just the table.** Every case links to the recording, the independent transcript, Rumik's own transcript, the exact private report Rumik sent its user, and the full evaluation with the judge's reasoning.

## Headline

| Measure | Muga | Mulberry 1.5 | Mulberry 1.6 |
| --- | --- | --- | --- |
| Attempted / connected | 10 / 10 | 10 / 10 | 10 / 10 |
| Conversations completed with a private report | 3 | 9 | 10 |
| Business outcome matches the case | 8 | 9 | 8 |
| All deterministic checks met | 2 | 6 | 7 |
| Simulation valid / invalid / unresolved | 5 / 5 / 0 | 6 / 2 / 2 | 6 / 4 / 0 |
| Formal outcome passed / failed / unresolved | 0 / 2 / 8 | 2 / 4 / 4 | 4 / 2 / 4 |
| Ended by Rumik hangup / employee finish / inactivity timeout | 0 / 3 / 6 | 4 / 5 / 1 | 8 / 2 / 0 |
| Rumik generations at the 400-token ceiling | not captured | 5 | 10 |
| TTFS ms mean / p50 / p90 / p95 | 3,102 / 2,816 / 4,457 / 4,819 (n=23) | 2,479 / 2,223 / 3,188 / 3,196 (n=27) | 2,964 / 2,384 / 4,384 / 4,809 (n=34) |
| TTFT per employee turn ms mean / p50 / p90 / p95 | not captured (see notes) | 1,726 / 1,568 / 2,425 / 2,473 (n=27) | 1,935 / 1,372 / 3,171 / 3,727 (n=32) |
| TTFT per Rumik generation ms | not captured (see notes) | 944 / 560 / 1,744 / 1,944 (n=34) | 1,166 / 641 / 2,509 / 3,030 (n=36) |
| Provider LLM first byte ms | not captured (see notes) | 287 / 322 / 371 / 440 (n=121) | 308 / 329 / 409 / 448 (n=140) |
| WER pooled, ASR-to-ASR | 24.6% over 1356 words | 21.0% over 813 words | 22.6% over 965 words |
| Call duration s mean / p50 / p90 / p95 | 133 / 131 / 158 / 170 (n=10) | 86 / 81 / 101 / 132 (n=10) | 86 / 69 / 138 / 141 (n=10) |

**Important comparability note.** Muga ran on 21 September on the pre-repair harness (long prompt A, spelled hex references, no silence follow-up), which is where most of its inactivity timeouts come from. Mulberry 1.5 and 1.6 ran on 22 September on the repaired harness with prompt v8 and the compact numeric reference. The two Mulberry cohorts are directly comparable with each other; Muga is the historical baseline and its lower completion rate is mostly the harness, not the voice. Muga's calls also predate the capture of Rumik's lifecycle packets, so TTFT is not available for it.

## How the benchmark works

1. **Case.** A private user task (request, constraints, permissions) is delivered to Rumik through an authenticated before-call tool. The employee gets only its own brief and restaurant policies. Neither side sees the grading rules.
2. **Call.** The harness joins Rumik's browser call, records both directions and plays the employee's speech into the room. Audio is simultaneous, so interruptions are real.
3. **Business tools.** The employee must look up availability, prepare an offer, and only then record a reservation; the recorder demands that the offer was actually played and that the caller spoke afterwards. Every request is audited and rejected requests are kept.
4. **Private report.** Rumik must send the outcome to its user through an authenticated tool before hanging up. The report is the user-facing deliverable.
5. **Evaluation.** Deterministic checks on the sealed business state and event log, then two independent LLM judges, then this report. Grades are frozen per batch and never edited.

## What the metrics mean

- **Business outcome** — did the restaurant record what the case expected (a booking with the right terms, or deliberately no booking)? Read from sealed business state, never from speech.
- **Deterministic checks** — task state, booking identity, immutable reservation history, no forbidden actions, no duplicates, authenticated task delivery, authenticated report receipt.
- **Luna** — `gpt-5.6-luna` reads the independent transcript, business record and report against the frozen rubric and answers eight questions: counterpart validity, constraint behaviour, consent alignment, report accuracy, role fidelity, question relevance, context retention, conversation progress. Its explanations are in each case's `evaluation.md`.
- **Jev** — `typesafe/jev-1.13` answers the same eight questions independently with a probability per choice. It is a second opinion and does not change grades. Luna = Jev counts agreements out of comparable questions.
- **Formal outcome** — passed only when every required deterministic and Luna requirement is met on a valid simulation; failed when any requirement is not met; unresolved when the simulation is invalid (an employee fault) or a requirement stays uncertain.
- **TTFS** (time to first speech) — end of the employee's rendered speech to the first Rumik speech captured, on the browser audio clock, per employee turn.
- **TTFT** (time to first token) — from the lifecycle packets Rumik publishes into the call. *Per employee turn*: end of employee speech to Rumik's first text token, same clock as TTFS. *Per Rumik generation*: Rumik's own end-of-speech decision to its first token. *Provider LLM first byte*: Rumik's self-reported LLM latency. All include network transit and are upper bounds.
- **WER** — word error rate between an independent transcription of the employee's played audio and Rumik's own recognition transcript. Two machine transcripts, so provisional; it is not a human-scored recognition accuracy.
- Distributions are mean / p50 / p90 / p95 in milliseconds over individual observations, nearest-rank quantiles.

## Muga

Pre-repair harness: target prompt A (3,041 characters), workflow 5, phonetically spelled hex reference, no silence follow-up. Run on 21 September 2026 as the historical baseline.

Batches: `9e75406e-6e55-4eda-aaf2-9864a630ae05`.

| Case | Expected | Business outcome | Simulation | Formal | Deterministic | Luna not met / uncertain | Jev not met / uncertain | Luna = Jev | Report | Ending | Dur s | TTFS p50 (n) | TTFT p50 (n) | Max tokens | WER | Proof |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [01 Aditi Shah](conversations/muga/01-aditi-shah/README.md) | book | ✓ book | invalid | unresolved | not met | counterpart validity | none | 7/8 | no | inactivity timeout | 149 | 2,919 (3) | — (0) | — | 16.4% | [audio](conversations/muga/01-aditi-shah/conversation.mp3) · [transcript](conversations/muga/01-aditi-shah/transcript.md) · [Rumik transcript](conversations/muga/01-aditi-shah/hosted-transcript.md) · [evaluation](conversations/muga/01-aditi-shah/evaluation.md) · [report](conversations/muga/01-aditi-shah/private-report.txt) |
| [02 Kabir Sethi](conversations/muga/02-kabir-sethi/README.md) | book | ✓ book | valid | failed | all met | constraint behavior, user report accuracy, context retention | counterpart validity, constraint behavior, user report accuracy, target role fidelity, question relevance, context retention, conversation progress | 4/8 | yes | employee finished | 170 | 3,316 (5) | — (0) | — | 50.0% | [audio](conversations/muga/02-kabir-sethi/conversation.mp3) · [transcript](conversations/muga/02-kabir-sethi/transcript.md) · [Rumik transcript](conversations/muga/02-kabir-sethi/hosted-transcript.md) · [evaluation](conversations/muga/02-kabir-sethi/evaluation.md) · [report](conversations/muga/02-kabir-sethi/private-report.txt) |
| [03 Meera Iyer](conversations/muga/03-meera-iyer/README.md) | book | ✓ book | invalid | unresolved | not met | counterpart validity, consent alignment | counterpart validity, constraint behavior, target role fidelity, question relevance, context retention, conversation progress | 2/8 | no | inactivity timeout | 158 | 2,397 (2) | — (0) | — | 19.5% | [audio](conversations/muga/03-meera-iyer/conversation.mp3) · [transcript](conversations/muga/03-meera-iyer/transcript.md) · [Rumik transcript](conversations/muga/03-meera-iyer/hosted-transcript.md) · [evaluation](conversations/muga/03-meera-iyer/evaluation.md) · [report](conversations/muga/03-meera-iyer/private-report.txt) |
| [04 Nisha Mehta](conversations/muga/04-nisha-mehta/README.md) | book | ✓ book | invalid | unresolved | not met | counterpart validity, consent alignment, conversation progress | counterpart validity, constraint behavior, target role fidelity, question relevance, context retention, conversation progress | 3/8 | no | inactivity timeout | 157 | 2,261 (2) | — (0) | — | 34.4% | [audio](conversations/muga/04-nisha-mehta/conversation.mp3) · [transcript](conversations/muga/04-nisha-mehta/transcript.md) · [Rumik transcript](conversations/muga/04-nisha-mehta/hosted-transcript.md) · [evaluation](conversations/muga/04-nisha-mehta/evaluation.md) · [report](conversations/muga/04-nisha-mehta/private-report.txt) |
| [05 Farhan Ali](conversations/muga/05-farhan-ali/README.md) | book | ✓ book | valid | unresolved | not met | none | none | 8/8 | no | inactivity timeout | 157 | 2,855 (2) | — (0) | — | 17.2% | [audio](conversations/muga/05-farhan-ali/conversation.mp3) · [transcript](conversations/muga/05-farhan-ali/transcript.md) · [Rumik transcript](conversations/muga/05-farhan-ali/hosted-transcript.md) · [evaluation](conversations/muga/05-farhan-ali/evaluation.md) · [report](conversations/muga/05-farhan-ali/private-report.txt) |
| [06 Priya Nair](conversations/muga/06-priya-nair/README.md) | book | ✗ no booking | valid | unresolved | not met | consent alignment, conversation progress | counterpart validity, constraint behavior, target role fidelity, question relevance, context retention, conversation progress | 1/8 | no | inactivity timeout | 118 | 3,247 (1) | — (0) | — | 23.9% | [audio](conversations/muga/06-priya-nair/conversation.mp3) · [transcript](conversations/muga/06-priya-nair/transcript.md) · [Rumik transcript](conversations/muga/06-priya-nair/hosted-transcript.md) · [evaluation](conversations/muga/06-priya-nair/evaluation.md) · [report](conversations/muga/06-priya-nair/private-report.txt) |
| [07 Devika Rao](conversations/muga/07-devika-rao/README.md) | book | ✗ no booking | invalid | unresolved | not met | counterpart validity, user report accuracy, context retention | counterpart validity, constraint behavior, target role fidelity, question relevance, context retention, conversation progress | 2/8 | yes | employee finished | 131 | 2,475 (4) | — (0) | — | 14.0% | [audio](conversations/muga/07-devika-rao/conversation.mp3) · [transcript](conversations/muga/07-devika-rao/transcript.md) · [Rumik transcript](conversations/muga/07-devika-rao/hosted-transcript.md) · [evaluation](conversations/muga/07-devika-rao/evaluation.md) · [report](conversations/muga/07-devika-rao/private-report.txt) |
| [08 Arjun Menon](conversations/muga/08-arjun-menon/README.md) | no booking | ✓ no booking | valid | failed | all met | constraint behavior | none | 7/8 | yes | employee finished | 96 | 2,351 (3) | — (0) | — | 18.6% | [audio](conversations/muga/08-arjun-menon/conversation.mp3) · [transcript](conversations/muga/08-arjun-menon/transcript.md) · [Rumik transcript](conversations/muga/08-arjun-menon/hosted-transcript.md) · [evaluation](conversations/muga/08-arjun-menon/evaluation.md) · [report](conversations/muga/08-arjun-menon/private-report.txt) |
| [09 Sana Khan](conversations/muga/09-sana-khan/README.md) | no booking | ✓ no booking | invalid | unresolved | not met | counterpart validity, constraint behavior, context retention, conversation progress | constraint behavior, target role fidelity, question relevance, context retention, conversation progress | 5/8 | no | inactivity timeout | 127 | 2,259 (1) | — (0) | — | 15.2% | [audio](conversations/muga/09-sana-khan/conversation.mp3) · [transcript](conversations/muga/09-sana-khan/transcript.md) · [Rumik transcript](conversations/muga/09-sana-khan/hosted-transcript.md) · [evaluation](conversations/muga/09-sana-khan/evaluation.md) · [report](conversations/muga/09-sana-khan/private-report.txt) |
| [10 Rohan Desai](conversations/muga/10-rohan-desai/README.md) | no booking | ✓ no booking | valid | unresolved | not met | constraint behavior, target role fidelity, question relevance, context retention, conversation progress | counterpart validity, constraint behavior, target role fidelity, question relevance, context retention, conversation progress | 5/8 | no | inactivity timeout | 68 | — (0) | — (0) | — | 0.0% | [audio](conversations/muga/10-rohan-desai/conversation.mp3) · [transcript](conversations/muga/10-rohan-desai/transcript.md) · [Rumik transcript](conversations/muga/10-rohan-desai/hosted-transcript.md) · [evaluation](conversations/muga/10-rohan-desai/evaluation.md) · [report](conversations/muga/10-rohan-desai/private-report.txt) |

Private reports Rumik sent its user:

- **01 Aditi Shah:** (no report received)
- **02 Kabir Sethi:** Reservation confirmed: Kabir Sethi, 5 guests, indoor regular table, all together, reservation only, no charge, date 2026-10-03, time 20:00, branch Domlur, reference S4CR. All user constraints satisfied.
- **03 Meera Iyer:** (no report received)
- **04 Nisha Mehta:** (no report received)
- **05 Farhan Ali:** (no report received)
- **06 Priya Nair:** (no report received)
- **07 Devika Rao:** No reservation could be made because on 2026-10-08 at 19:30 indoor regular table for 8 guests with a package under INR 13000 was not available at Saffron Terrace, Koregaon Park.
- **08 Arjun Menon:** No booking made. Reason: No indoor regular table free reservation available for 3 guests on 2026-10-09 between 19:00 and 19:30 at River Mint Fort Kochi, as only slots at 18:00 and 20:15 are offered, which are outside the allowed window.
- **09 Sana Khan:** (no report received)
- **10 Rohan Desai:** (no report received)

## Mulberry 1.5

Repaired harness: prompt natural-caller-v8, workflow 6 with the compact numeric reference, one ten-second silence follow-up. Run on 22 September 2026.

Batches: `f65d8b78-d09a-4eb7-af40-f98efd8803ce`.

| Case | Expected | Business outcome | Simulation | Formal | Deterministic | Luna not met / uncertain | Jev not met / uncertain | Luna = Jev | Report | Ending | Dur s | TTFS p50 (n) | TTFT p50 (n) | Max tokens | WER | Proof |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [01 Aditi Shah](conversations/mulberry-1-5/01-aditi-shah/README.md) | book | ✓ book | invalid | unresolved | not met | counterpart validity, constraint behavior, context retention | none | 5/8 | yes | Rumik hung up | 98 | 2,216 (4) | 1,485 (4) | 366 | 27.2% | [audio](conversations/mulberry-1-5/01-aditi-shah/conversation.mp3) · [transcript](conversations/mulberry-1-5/01-aditi-shah/transcript.md) · [Rumik transcript](conversations/mulberry-1-5/01-aditi-shah/hosted-transcript.md) · [evaluation](conversations/mulberry-1-5/01-aditi-shah/evaluation.md) · [report](conversations/mulberry-1-5/01-aditi-shah/private-report.txt) |
| [02 Kabir Sethi](conversations/mulberry-1-5/02-kabir-sethi/README.md) | book | ✓ book | valid | failed | not met | user report accuracy | none | 7/8 | yes | employee finished | 79 | 2,068 (3) | 1,283 (3) | 316 | 15.7% | [audio](conversations/mulberry-1-5/02-kabir-sethi/conversation.mp3) · [transcript](conversations/mulberry-1-5/02-kabir-sethi/transcript.md) · [Rumik transcript](conversations/mulberry-1-5/02-kabir-sethi/hosted-transcript.md) · [evaluation](conversations/mulberry-1-5/02-kabir-sethi/evaluation.md) · [report](conversations/mulberry-1-5/02-kabir-sethi/private-report.txt) |
| [03 Meera Iyer](conversations/mulberry-1-5/03-meera-iyer/README.md) | book | ✓ book | unresolved | unresolved | all met | counterpart validity, consent alignment, user report accuracy | counterpart validity, constraint behavior, user report accuracy, target role fidelity, question relevance, context retention, conversation progress | 1/8 | yes | employee finished | 101 | 1,916 (4) | 1,139 (4) | 400 ⚠1 | 22.9% | [audio](conversations/mulberry-1-5/03-meera-iyer/conversation.mp3) · [transcript](conversations/mulberry-1-5/03-meera-iyer/transcript.md) · [Rumik transcript](conversations/mulberry-1-5/03-meera-iyer/hosted-transcript.md) · [evaluation](conversations/mulberry-1-5/03-meera-iyer/evaluation.md) · [report](conversations/mulberry-1-5/03-meera-iyer/private-report.txt) |
| [04 Nisha Mehta](conversations/mulberry-1-5/04-nisha-mehta/README.md) | book | ✓ book | valid | failed | all met | constraint behavior, user report accuracy | none | 6/8 | yes | employee finished | 92 | 2,625 (3) | 2,016 (3) | 336 | 20.2% | [audio](conversations/mulberry-1-5/04-nisha-mehta/conversation.mp3) · [transcript](conversations/mulberry-1-5/04-nisha-mehta/transcript.md) · [Rumik transcript](conversations/mulberry-1-5/04-nisha-mehta/hosted-transcript.md) · [evaluation](conversations/mulberry-1-5/04-nisha-mehta/evaluation.md) · [report](conversations/mulberry-1-5/04-nisha-mehta/private-report.txt) |
| [05 Farhan Ali](conversations/mulberry-1-5/05-farhan-ali/README.md) | book | ✓ book | valid | failed | not met | constraint behavior, context retention | counterpart validity, constraint behavior, target role fidelity, question relevance, context retention, conversation progress | 4/8 | yes | employee finished | 81 | 2,584 (3) | 2,003 (3) | 400 ⚠1 | 18.5% | [audio](conversations/mulberry-1-5/05-farhan-ali/conversation.mp3) · [transcript](conversations/mulberry-1-5/05-farhan-ali/transcript.md) · [Rumik transcript](conversations/mulberry-1-5/05-farhan-ali/hosted-transcript.md) · [evaluation](conversations/mulberry-1-5/05-farhan-ali/evaluation.md) · [report](conversations/mulberry-1-5/05-farhan-ali/private-report.txt) |
| [06 Priya Nair](conversations/mulberry-1-5/06-priya-nair/README.md) | book | ✓ book | valid | failed | all met | user report accuracy, target role fidelity, question relevance | none | 5/8 | yes | Rumik hung up | 132 | 2,135 (6) | 1,368 (6) | 392 | 25.2% | [audio](conversations/mulberry-1-5/06-priya-nair/conversation.mp3) · [transcript](conversations/mulberry-1-5/06-priya-nair/transcript.md) · [Rumik transcript](conversations/mulberry-1-5/06-priya-nair/hosted-transcript.md) · [evaluation](conversations/mulberry-1-5/06-priya-nair/evaluation.md) · [report](conversations/mulberry-1-5/06-priya-nair/private-report.txt) |
| [07 Devika Rao](conversations/mulberry-1-5/07-devika-rao/README.md) | book | ✗ no booking | invalid | unresolved | not met | counterpart validity, target role fidelity, question relevance, context retention, conversation progress | counterpart validity, constraint behavior, target role fidelity, question relevance, context retention, conversation progress | 3/8 | no | inactivity timeout | 87 | — (0) | — (0) | 400 ⚠2 | 13.6% | [audio](conversations/mulberry-1-5/07-devika-rao/conversation.mp3) · [transcript](conversations/mulberry-1-5/07-devika-rao/transcript.md) · [Rumik transcript](conversations/mulberry-1-5/07-devika-rao/hosted-transcript.md) · [evaluation](conversations/mulberry-1-5/07-devika-rao/evaluation.md) · [report](conversations/mulberry-1-5/07-devika-rao/private-report.txt) |
| [08 Arjun Menon](conversations/mulberry-1-5/08-arjun-menon/README.md) | no booking | ✓ no booking | unresolved | unresolved | all met | counterpart validity, user report accuracy, target role fidelity, question relevance, conversation progress | none | 3/8 | yes | Rumik hung up | 63 | — (0) | 767 (3) | 319 | 19.6% | [audio](conversations/mulberry-1-5/08-arjun-menon/conversation.mp3) · [transcript](conversations/mulberry-1-5/08-arjun-menon/transcript.md) · [Rumik transcript](conversations/mulberry-1-5/08-arjun-menon/hosted-transcript.md) · [evaluation](conversations/mulberry-1-5/08-arjun-menon/evaluation.md) · [report](conversations/mulberry-1-5/08-arjun-menon/private-report.txt) |
| [09 Sana Khan](conversations/mulberry-1-5/09-sana-khan/README.md) | no booking | ✓ no booking | valid | passed | all met | conversation progress | none | 7/8 | yes | Rumik hung up | 52 | 1,936 (2) | 1,305 (2) | 284 | 25.0% | [audio](conversations/mulberry-1-5/09-sana-khan/conversation.mp3) · [transcript](conversations/mulberry-1-5/09-sana-khan/transcript.md) · [Rumik transcript](conversations/mulberry-1-5/09-sana-khan/hosted-transcript.md) · [evaluation](conversations/mulberry-1-5/09-sana-khan/evaluation.md) · [report](conversations/mulberry-1-5/09-sana-khan/private-report.txt) |
| [10 Rohan Desai](conversations/mulberry-1-5/10-rohan-desai/README.md) | no booking | ✓ no booking | valid | passed | all met | none | none | 8/8 | yes | employee finished | 77 | 2,223 (2) | 1,568 (2) | 400 ⚠1 | 8.7% | [audio](conversations/mulberry-1-5/10-rohan-desai/conversation.mp3) · [transcript](conversations/mulberry-1-5/10-rohan-desai/transcript.md) · [Rumik transcript](conversations/mulberry-1-5/10-rohan-desai/hosted-transcript.md) · [evaluation](conversations/mulberry-1-5/10-rohan-desai/evaluation.md) · [report](conversations/mulberry-1-5/10-rohan-desai/private-report.txt) |

Private reports Rumik sent its user:

- **01 Aditi Shah:** Reservation confirmed for 2 Oct 2026 at 7:30 pm for 3 people, indoor regular table, Aundh branch Neem Courtyard, under Aditi Shah, no charge, reference SIM-09-7939.
- **02 Kabir Sethi:** Booked indoor regular table for 5 at Domlur on 2026-10-03 at 20:00 under Kabir Sethi, no reservation charge, reference SIM-718266.
- **03 Meera Iyer:** Booked indoor regular table for 2 on 2026-10-04 at 6:45 PM under Meera Iyer, no charge, reference SIM-92-691.
- **04 Nisha Mehta:** Booked indoor regular table for 6 on 2026-10-05 at 19:45 under Nisha Mehta, no reservation charge, reference SIM-27-1196.
- **05 Farhan Ali:** Booked 6 Oct 2026 at 7:30pm indoor regular table for 4 under Farhan Ali, no charge, reference SIM-641022
- **06 Priya Nair:** Reservation for 7 people on 2026-10-07 at 20:00 under Priya Nair, indoor regular table, dining package total INR 9,800, reference सिम 385061.
- **07 Devika Rao:** (no report received)
- **08 Arjun Menon:** No authorized time slot available as only 19:00-19:30 is allowed, so no reservation could be made.
- **09 Sana Khan:** Cannot book: total charge INR 9,600 exceeds the allowed limit of INR 9,000.
- **10 Rohan Desai:** No booking was made because the kitchen cannot meet the onion‑ and garlic‑free requirement for the two guests.

## Mulberry 1.6

Same repaired harness and settings as Mulberry 1.5; the second batch holds the two cases a conservative drift stop skipped. Run on 22 September 2026.

Batches: `ed8bb1e2-4d90-49c2-b581-491987cb498f`, `8c9f849c-c24c-416c-8b41-8d8a4cddd92e`.

| Case | Expected | Business outcome | Simulation | Formal | Deterministic | Luna not met / uncertain | Jev not met / uncertain | Luna = Jev | Report | Ending | Dur s | TTFS p50 (n) | TTFT p50 (n) | Max tokens | WER | Proof |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [01 Aditi Shah](conversations/mulberry-1-6/01-aditi-shah/README.md) | book | ✓ book | valid | passed | all met | none | none | 8/8 | yes | Rumik hung up | 138 | 2,337 (8) | 1,341 (6) | 400 ⚠3 | 23.9% | [audio](conversations/mulberry-1-6/01-aditi-shah/conversation.mp3) · [transcript](conversations/mulberry-1-6/01-aditi-shah/transcript.md) · [Rumik transcript](conversations/mulberry-1-6/01-aditi-shah/hosted-transcript.md) · [evaluation](conversations/mulberry-1-6/01-aditi-shah/evaluation.md) · [report](conversations/mulberry-1-6/01-aditi-shah/private-report.txt) |
| [02 Kabir Sethi](conversations/mulberry-1-6/02-kabir-sethi/README.md) | book | ✓ book | valid | passed | all met | none | none | 8/8 | yes | Rumik hung up | 119 | 2,332 (5) | 1,160 (5) | 400 ⚠1 | 28.9% | [audio](conversations/mulberry-1-6/02-kabir-sethi/conversation.mp3) · [transcript](conversations/mulberry-1-6/02-kabir-sethi/transcript.md) · [Rumik transcript](conversations/mulberry-1-6/02-kabir-sethi/hosted-transcript.md) · [evaluation](conversations/mulberry-1-6/02-kabir-sethi/evaluation.md) · [report](conversations/mulberry-1-6/02-kabir-sethi/private-report.txt) |
| [03 Meera Iyer](conversations/mulberry-1-6/03-meera-iyer/README.md) | book | ✓ book | invalid | unresolved | all met | counterpart validity, user report accuracy | none | — | yes | Rumik hung up | 92 | 2,323 (5) | 1,403 (5) | 400 ⚠2 | 25.6% | [audio](conversations/mulberry-1-6/03-meera-iyer/conversation.mp3) · [transcript](conversations/mulberry-1-6/03-meera-iyer/transcript.md) · [Rumik transcript](conversations/mulberry-1-6/03-meera-iyer/hosted-transcript.md) · [evaluation](conversations/mulberry-1-6/03-meera-iyer/evaluation.md) · [report](conversations/mulberry-1-6/03-meera-iyer/private-report.txt) |
| [04 Nisha Mehta](conversations/mulberry-1-6/04-nisha-mehta/README.md) | book | ✗ no booking | invalid | unresolved | not met | counterpart validity, user report accuracy, question relevance, context retention, conversation progress | counterpart validity, constraint behavior, user report accuracy, target role fidelity, question relevance, context retention, conversation progress | 5/8 | yes | Rumik hung up | 57 | 2,969 (2) | 2,025 (2) | 372 | 23.0% | [audio](conversations/mulberry-1-6/04-nisha-mehta/conversation.mp3) · [transcript](conversations/mulberry-1-6/04-nisha-mehta/transcript.md) · [Rumik transcript](conversations/mulberry-1-6/04-nisha-mehta/hosted-transcript.md) · [evaluation](conversations/mulberry-1-6/04-nisha-mehta/evaluation.md) · [report](conversations/mulberry-1-6/04-nisha-mehta/private-report.txt) |
| [05 Farhan Ali](conversations/mulberry-1-6/05-farhan-ali/README.md) | book | ✓ book | valid | failed | not met | constraint behavior | counterpart validity, constraint behavior, user report accuracy, target role fidelity, question relevance, context retention, conversation progress | 2/8 | yes | employee finished | 74 | 2,384 (3) | 1,347 (3) | 400 ⚠1 | 26.2% | [audio](conversations/mulberry-1-6/05-farhan-ali/conversation.mp3) · [transcript](conversations/mulberry-1-6/05-farhan-ali/transcript.md) · [Rumik transcript](conversations/mulberry-1-6/05-farhan-ali/hosted-transcript.md) · [evaluation](conversations/mulberry-1-6/05-farhan-ali/evaluation.md) · [report](conversations/mulberry-1-6/05-farhan-ali/private-report.txt) |
| [06 Priya Nair](conversations/mulberry-1-6/06-priya-nair/README.md) | book | ✗ no booking | invalid | unresolved | not met | counterpart validity, user report accuracy | counterpart validity, constraint behavior, target role fidelity, question relevance, context retention, conversation progress | 1/8 | yes | employee finished | 69 | 2,219 (2) | 1,273 (2) | 359 | 21.6% | [audio](conversations/mulberry-1-6/06-priya-nair/conversation.mp3) · [transcript](conversations/mulberry-1-6/06-priya-nair/transcript.md) · [Rumik transcript](conversations/mulberry-1-6/06-priya-nair/hosted-transcript.md) · [evaluation](conversations/mulberry-1-6/06-priya-nair/evaluation.md) · [report](conversations/mulberry-1-6/06-priya-nair/private-report.txt) |
| [07 Devika Rao](conversations/mulberry-1-6/07-devika-rao/README.md) | book | ✓ book | invalid | unresolved | all met | counterpart validity, consent alignment, conversation progress | none | 5/8 | yes | Rumik hung up | 141 | 3,064 (5) | 1,973 (5) | 400 ⚠2 | 19.5% | [audio](conversations/mulberry-1-6/07-devika-rao/conversation.mp3) · [transcript](conversations/mulberry-1-6/07-devika-rao/transcript.md) · [Rumik transcript](conversations/mulberry-1-6/07-devika-rao/hosted-transcript.md) · [evaluation](conversations/mulberry-1-6/07-devika-rao/evaluation.md) · [report](conversations/mulberry-1-6/07-devika-rao/private-report.txt) |
| [08 Arjun Menon](conversations/mulberry-1-6/08-arjun-menon/README.md) | no booking | ✓ no booking | valid | passed | all met | none | none | 8/8 | yes | Rumik hung up | 58 | 2,055 (2) | 1,172 (2) | 400 ⚠1 | 20.9% | [audio](conversations/mulberry-1-6/08-arjun-menon/conversation.mp3) · [transcript](conversations/mulberry-1-6/08-arjun-menon/transcript.md) · [Rumik transcript](conversations/mulberry-1-6/08-arjun-menon/hosted-transcript.md) · [evaluation](conversations/mulberry-1-6/08-arjun-menon/evaluation.md) · [report](conversations/mulberry-1-6/08-arjun-menon/private-report.txt) |
| [09 Sana Khan](conversations/mulberry-1-6/09-sana-khan/README.md) | no booking | ✓ no booking | valid | passed | all met | none | none | 8/8 | yes | Rumik hung up | 55 | 4,093 (2) | 3,040 (2) | 301 | 21.6% | [audio](conversations/mulberry-1-6/09-sana-khan/conversation.mp3) · [transcript](conversations/mulberry-1-6/09-sana-khan/transcript.md) · [Rumik transcript](conversations/mulberry-1-6/09-sana-khan/hosted-transcript.md) · [evaluation](conversations/mulberry-1-6/09-sana-khan/evaluation.md) · [report](conversations/mulberry-1-6/09-sana-khan/private-report.txt) |
| [10 Rohan Desai](conversations/mulberry-1-6/10-rohan-desai/README.md) | no booking | ✓ no booking | valid | failed | all met | user report accuracy | none | 7/8 | yes | Rumik hung up | 60 | — (0) | 808 (3) | 215 | 8.7% | [audio](conversations/mulberry-1-6/10-rohan-desai/conversation.mp3) · [transcript](conversations/mulberry-1-6/10-rohan-desai/transcript.md) · [Rumik transcript](conversations/mulberry-1-6/10-rohan-desai/hosted-transcript.md) · [evaluation](conversations/mulberry-1-6/10-rohan-desai/evaluation.md) · [report](conversations/mulberry-1-6/10-rohan-desai/private-report.txt) |

Private reports Rumik sent its user:

- **01 Aditi Shah:** Booked indoor regular table for 3 on 2026-10-02 at 19:30 under name Aditi Shah, no reservation charge, reference SIM-98-5180.
- **02 Kabir Sethi:** Booked indoor regular table for five at Domlur on 3 October 2026 at 8 pm under Kabir Sethi, no charges, reference SIM-401933.
- **03 Meera Iyer:** Booked indoor regular table for 2 at Banyan Kitchen Adyar on 2026-10-04 at 19:30 under Meera Iyer, no charge, reference 14712.
- **04 Nisha Mehta:** Could not book: requested time 7:50 pm does not match allowed reservation time 19:45 for 5 October 2026.
- **05 Farhan Ali:** Booked 6 Oct 2026 19:30 indoor regular table for 4 under Farhan Ali at Jubilee Hills, charge INR 0, reference SIM-84-6468.
- **06 Priya Nair:** Could not make the reservation because the only available dining package exceeds the budget limit of INR 10,500 (offered at INR 11,900).
- **07 Devika Rao:** Booked: 8 Oct 2026 19:30, Devika Rao, 8 persons, indoor regular table, total INR 12400, includes starter, main, rice/bread each, reference SIM-673238.
- **08 Arjun Menon:** No reservation could be made because the only available times (6:00 pm or 8:15 pm) fall outside the allowed window of 19:00‑19:30.
- **09 Sana Khan:** Cannot book because the total charge of INR 9,600 exceeds the allowed limit of INR 9,000.
- **10 Rohan Desai:** Reservation not booked because onion‑garlic free meals are not available.

## Judge verdicts per question

Count of cases per verdict. `n/a` means the question did not apply (for example consent on a no-booking case); `no answer` means Jev's response was rejected by the frozen validator.

| Question | Luna Muga | Jev Muga | Luna 1.5 | Jev 1.5 | Luna 1.6 | Jev 1.6 |
| --- | --- | --- | --- | --- | --- | --- |
| counterpart validity | met 5, not met 5 | met 4, not met 5, uncertain 1 | met 6, not met 2, uncertain 2 | met 7, not met 3 | met 6, not met 4 | no answer 1, met 6, not met 3 |
| constraint behavior | met 6, not met 3, uncertain 1 | met 3, not met 6, uncertain 1 | met 7, not met 3 | met 7, not met 3 | met 9, not met 1 | no answer 1, met 6, not met 3 |
| consent alignment | met 4, n/a 3, not met 2, uncertain 1 | met 5, n/a 5 | met 6, n/a 3, uncertain 1 | met 6, n/a 4 | met 6, n/a 3, not met 1 | no answer 1, met 4, n/a 5 |
| user report accuracy | met 1, n/a 7, not met 2 | met 2, n/a 7, not met 1 | met 4, n/a 1, not met 5 | met 8, n/a 1, not met 1 | met 6, not met 4 | no answer 1, met 7, not met 2 |
| target role fidelity | met 9, uncertain 1 | met 3, not met 7 | met 7, not met 1, uncertain 2 | met 7, not met 3 | met 10 | no answer 1, met 6, not met 3 |
| question relevance | met 9, uncertain 1 | met 3, not met 6, uncertain 1 | met 7, not met 1, uncertain 2 | met 7, not met 3 | met 9, not met 1 | no answer 1, met 6, not met 3 |
| context retention | met 6, not met 3, uncertain 1 | met 3, not met 6, uncertain 1 | met 7, not met 2, uncertain 1 | met 7, not met 3 | met 9, not met 1 | no answer 1, met 6, not met 3 |
| conversation progress | met 6, not met 3, uncertain 1 | met 3, not met 6, uncertain 1 | met 7, not met 1, uncertain 2 | met 7, not met 3 | met 8, not met 2 | no answer 1, met 6, not met 3 |

## Findings

1. **The repaired harness moved the failure from silence to content.** Muga on the old harness completed 3 of 10 conversations with a report and timed out 7 times. Mulberry 1.5 and 1.6 on the repaired harness completed 19 of 20. The remaining stall (Mulberry 1.5, Devika Rao) carries the known signature: Rumik's hosted LLM spends its whole 400-token completion budget on hidden reasoning and produces nothing. That limit is hosted configuration and still bit fifteen turns across the twenty Mulberry calls; fourteen recovered.
2. **Employee slips now cause most invalid simulations**: a mispronounced reference, an invented request during a silence follow-up, a confirmation announced before the tool result, an unrelated phrase, a missed budget-fitting menu, a booking recorded without clear consent. These are `gpt-realtime` faults and make the simulation invalid rather than grading Rumik.
3. **Rumik's own errors are about content**: an ignored branch-preference rule, an initial wrong time window, a role slip into the employee's position, a wrong readback of the customer's name, an invented time mismatch, and 'without onion and garlic' turned into 'free food'.
4. **Report accuracy is the most frequent failed requirement** in the Mulberry cohorts (9 of 19 reports): omitted booked terms, dropped reference digits, a reference written in Devanagari, a surname-only booking name recorded by the employee.
5. **Latency.** Rumik's self-reported LLM first byte is about 0.32 s. The caller waits about 1.4 to 1.6 s (p50) for the first token and 2.2 to 2.4 s (p50) for the first speech, so endpointing plus reasoning and then speech synthesis account for most of the perceived delay. Muga's TTFS is in the same range on the calls that did reply.
6. **WER** is 21 to 23 percent for both Mulberry cohorts and higher for Muga on this ASR-to-ASR comparison. Hinglish script differences inflate all three numbers; treat them as relative, not absolute recognition accuracy.
7. **Judges.** Luna and Jev agree on roughly six of eight questions per case; Jev leans toward 'met' with low confidence. Two Luna verdicts were downgraded to uncertain because the judge's quoted evidence did not match the transcript window; one Jev answer was rejected by the validator.

## Limits

One attempt per case per model; differences of one or two cases are not statistically meaningful. Muga is not on the same harness as the Mulberry cohorts. TTFT and TTFS are observed at the browser and include network transit. WER compares two machine transcripts. Human listening for Hinglish quality and output integrity is pending for every case. Formal grades come from the frozen rubric and can fail a call that completed the business task, for example on report completeness.

## Provenance

[Machine-readable summary](summary.json).

Recordings here are 64 kbps mp3 transcodes of the synchronized `conversation.wav` in each attempt's frozen report; raw evidence, frozen configuration, source snapshot and database ledgers are under `artifacts/<batch>/`. Per-attempt evaluations for the Mulberry cohorts are the regenerated `full-report-v2` (adds TTFT; grades unchanged). Investigation write-ups: `docs/CONVERSATION_REPAIR.md`, `docs/P0_DEBUG_PLAN.md`, `reports/p0-cohort-mulberry-20260922/`.
