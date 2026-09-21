# Rumik: complete results in plain English

**All 10 restaurant cases ran. Five calls produced bookings. Six calls had no final report to the user, and the four reports that arrived contained incorrect or outdated details.**

This is a clearer presentation of the saved results, not a new test or a change to any grade. The test includes employee and judge problems too, so not every negative result can be assigned to Rumik.

## 1. Overall results

| What we counted | Result |
| --- | --- |
| Calls planned / attempted / connected / not run | 10 / 10 / 10 / 0 |
| Did Rumik complete the user’s request? | 0 passed, 2 failed, 8 undecided |
| Quality of the simulations | 6 valid, 2 invalid, 2 uncertain |
| Recorded bookings | 5 |
| Final reports to the user | 6 missing; 4 received, all with errors |
| GPT evaluations | 10 completed |
| Jev evaluations | 10 responses received; 9 accepted by the result checker |

**“Undecided” does not mean successful.** It means the available evidence or grading could not support an overall verdict on whether Rumik completed the user’s request. A missing report remains a problem even when its cause is unknown. An invalid simulation stays in the report but cannot be treated as a clean test of Rumik.

**What counts as completing the request?** Rumik must follow the user’s limits, reach the correct booking or no-booking outcome, and report the final result accurately. The overall verdict covers the whole request, not just whether a booking exists.

## 2. What happened in every case

| Case | Task | Booking | Final report | Test quality | Request completed? | Conversation |
| --- | --- | --- | --- | --- | --- | --- |
| [01 Aditi](cases/01-aditi.md) | Simple table booking | No | Missing | Invalid | Undecided | [Audio + transcript](conversations/01-aditi/README.md) |
| [02 Kabir](cases/02-kabir.md) | Fallback to another branch | No | Missing | Valid | Undecided | [Audio + transcript](conversations/02-kabir/README.md) |
| [03 Meera](cases/03-meera.md) | Flexible booking time | Yes | Incorrect or outdated | Invalid | Undecided | [Audio + transcript](conversations/03-meera/README.md) |
| [04 Nisha](cases/04-nisha.md) | No onion or garlic for two guests | Yes | Incorrect or outdated | Valid | Failed | [Audio + transcript](conversations/04-nisha/README.md) |
| [05 Farhan](cases/05-farhan.md) | Choose the earliest time | Yes | Missing | Valid | Undecided | [Audio + transcript](conversations/05-farhan/README.md) |
| [06 Priya](cases/06-priya.md) | Smaller menu within ₹10,500 | Yes | Missing | Valid | Undecided | [Audio + transcript](conversations/06-priya/README.md) |
| [07 Devika](cases/07-devika.md) | No deposit; total within ₹13,000 | Yes | Incorrect or outdated | Uncertain | Undecided | [Audio + transcript](conversations/07-devika/README.md) |
| [08 Arjun](cases/08-arjun.md) | No table in the permitted time range | No | Missing | Uncertain | Undecided | [Audio + transcript](conversations/08-arjun/README.md) |
| [09 Sana](cases/09-sana.md) | No package within ₹9,000 | No | Incorrect or outdated | Valid | Failed | [Audio + transcript](conversations/09-sana/README.md) |
| [10 Rohan](cases/10-rohan.md) | Dietary requirement cannot be met | No | Missing | Valid | Undecided | [Audio + transcript](conversations/10-rohan/README.md) |

- **01 Aditi:** No booking or final report. Rumik stopped after the employee asked for confirmation. The employee also attempted to book too early; that attempt was blocked.
- **02 Kabir:** Only an opening exchange; no substantive request, booking or final report.
- **03 Meera:** Booked, but the final report changed the booking reference. The booking used “Meera” rather than the full name. One judge explanation also confuses the speakers.
- **04 Nisha:** Booked with the dietary requirement. The final report shortened the reference from SIM-1847C8FA18 to C8FA18. The judges disagree about consent.
- **05 Farhan:** Booked the 7 p.m. Banjara Hills option. No final report arrived.
- **06 Priya:** Booked the ₹9,800 compact menu. Rumik then stopped responding and no final report arrived.
- **07 Devika:** Reported “no booking” because of a deposit. The conversation continued and a ₹12,400 deposit-free booking was recorded, but the report was not updated. Consent needs review.
- **08 Arjun:** Stopped after the greeting. No booking or final report. Having no booking does not prove it completed the requested availability check.
- **09 Sana:** Correctly refused the ₹9,600 offer because the limit was ₹9,000. The final report incorrectly said the only available offer was ₹10,800.
- **10 Rohan:** No booking when the restaurant could not meet the dietary condition. No final report explaining the outcome arrived.

## 3. Speed and recognition measurements

**Time to first speech (TTFS)** is the measured wait between the employee finishing speaking and Rumik starting to speak. **AAT** means average response time here, using those same measurements. p50 is the median; p90 and p95 are the times within which 90% and 95% of measured responses started.

| Calls included | Measured responses | Average / AAT | p50 | p90 | p95 |
| --- | ---: | ---: | ---: | ---: | ---: |
| All 10 attempts | 21 | 3.57 s | 2.54 s | 3.91 s | 12.30 s |
| Only the 6 valid simulations | 12 | 4.21 s | 2.39 s | 12.30 s | 13.38 s |

These figures cover observed replies only. Seven other employee speech items had no observed reply before the next item or recording end. Some were closings, so they are not automatically missed turns. They were not entered as zero-second or invented timeout responses.

| Other requested measurement | Result | What it means |
| --- | --- | --- |
| Word error rate (WER), provisional | **20.69%**: 288 edits / 1,392 reference words, across 10 cases | Comparison of an independent machine transcript of employee audio with Rumik’s recorded transcript |
| Time to first token / text (TTFT) | **Not measurable: 0 of 10 calls have first-text timestamps** | Saved Rumik transcripts contain text and speaker roles, with no token arrival times |
| Endpointing accuracy | Not available | We lack Rumik’s turn-end decisions and reviewed labels for when each speaker finished |

WER is **not yet a human-verified recognition score**. The reference transcription can contain mistakes, and Hindi/English writing differences can inflate the number. Human listening review is pending. Audio response timing cannot substitute for TTFT or endpointing accuracy.

### TTFT: what we can calculate ourselves

**Yes, we can calculate observed TTFT ourselves when the first text arrives as a timed event.** For this voice benchmark, that would be the time from the employee finishing speaking to the first nonempty Rumik text chunk reaching the harness. The two timestamps must use the same clock, or a verified clock mapping, and belong to the same response. This measures the full wait for text, including turn detection and network delay. It differs from Rumik’s internal model-generation time.

**For these 10 saved calls, that first-text timestamp was not recorded.** We checked all 130,234 saved events and all 185 entries in Rumik’s post-call transcripts. Every transcript entry contains only `role` and `content`. The 28 timestamped transcript events belong to the simulated employee and mark a completed transcript; they are not Rumik’s first token. Provider callback records contain no additional timing events.

| TTFT coverage | Samples | Average | p50 | p90 | p95 |
| --- | ---: | --- | --- | --- | --- |
| All 10 calls inspected; 0 calls measurable | 0 | Not available | Not available | Not available | Not available |

The recorded audio lets us calculate **time to first speech (TTFS)**, which is already reported above. It cannot reveal when an earlier text token was generated or received. Transcribing the audio again would not recover that timestamp, and subtracting an assumed speech-generation delay would create an unsupported estimate.

For future calls, measuring observed TTFT requires a timestamped first-text stream from Rumik, correlated with the employee’s speech-end timestamp. Internal model TTFT additionally requires the model’s generation-start and first-token timestamps. No new calls or paid evaluations were run for this audit. [Read the per-case timing audit](ttft-audit.json).

### Measurements by case

All response times below are seconds. “—” means no response was available to time, not zero delay. WER is provisional in every row.

| Case | Speech replies timed | Average | p50 | p90 | p95 | TTFT | WER (edits / reference words) |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| 01 Aditi | 1 | 3.02 | 3.02 | 3.02 | 3.02 | Not available | 14.08% (10/71) |
| 02 Kabir | 0 | — | — | — | — | Not available | 13.04% (3/23) |
| 03 Meera | 5 | 2.57 | 2.33 | 3.91 | 3.91 | Not available | 22.50% (54/240) |
| 04 Nisha | 3 | 5.97 | 3.40 | 12.30 | 12.30 | Not available | 38.54% (74/192) |
| 05 Farhan | 2 | 2.39 | 2.24 | 2.54 | 2.54 | Not available | 13.64% (21/154) |
| 06 Priya | 2 | 2.29 | 2.19 | 2.39 | 2.39 | Not available | 10.81% (20/185) |
| 07 Devika | 3 | 2.88 | 2.66 | 3.38 | 3.38 | Not available | 23.51% (59/251) |
| 08 Arjun | 0 | — | — | — | — | Not available | 0.00% (0/19) |
| 09 Sana | 3 | 2.39 | 2.24 | 2.74 | 2.74 | Not available | 22.22% (38/171) |
| 10 Rohan | 2 | 8.04 | 2.70 | 13.38 | 13.38 | Not available | 10.47% (9/86) |

### Audio delivery and silence checks

These are automatic checks on local playback and recorded audio. They do not prove what the remote model heard or establish why it went silent. A silence interval is measured only where both recordings exist.

| Case | Local playback check | Silence intervals of at least 10 seconds | Longest such interval |
| --- | --- | ---: | ---: |
| 01 Aditi | Passed | 1 | 16.96 s |
| 02 Kabir | Passed | 1 | 17.33 s |
| 03 Meera | Passed | 0 | None |
| 04 Nisha | Passed | 2 | 12.30 s |
| 05 Farhan | Passed | 1 | 17.19 s |
| 06 Priya | Passed | 1 | 17.35 s |
| 07 Devika | Passed | 0 | None |
| 08 Arjun | Passed | 1 | 16.92 s |
| 09 Sana | Passed | 0 | None |
| 10 Rohan | Passed | 2 | 23.24 s |

## 4. Every GPT and Jev result

GPT was **gpt-5.6-luna**. Jev was **typesafe/jev-1.13**. “Meets” and “Does not meet” refer to one check, not the entire call. “Unclear” means there is insufficient evidence; “N/A” means that check does not apply. “Not returned” means there is no GPT answer for that check. Jev did not assess the two listening checks.

**Original opinion versus accepted grade:** the GPT column shows what GPT returned. The accepted-check column shows the result after the frozen evidence rules were applied. A missing citation can turn “Meets” or “Does not meet” into “Unclear.” These differences are preserved, not silently corrected.

Jev supplies choices and probabilities, not written explanations. Its original confidence values and full probability distributions are included in each linked case detail.

### Judge totals

The tables below show how often each judge returned each result. Each row totals 10 cases. Jev includes Aditi’s returned but unvalidated answers.

#### GPT results

| Check | Meets | Does not meet | Unclear | N/A | Not returned |
| --- | ---: | ---: | ---: | ---: | ---: |
| Respects the user’s limits | 10 | 0 | 0 | 0 | 0 |
| Remembers facts already supplied | 8 | 0 | 2 | 0 | 0 |
| Answers and asks relevant questions | 7 | 1 | 2 | 0 | 0 |
| Moves the conversation forward | 6 | 4 | 0 | 0 | 0 |
| Gets clear agreement before booking | 3 | 3 | 1 | 0 | 3 |
| Acts as the user’s assistant | 8 | 2 | 0 | 0 | 0 |
| Simulated employee follows its rules | 7 | 2 | 1 | 0 | 0 |
| Final report is accurate | 0 | 4 | 0 | 6 | 0 |
| Hinglish is clear and natural | 0 | 0 | 10 | 0 | 0 |
| Speech contains no internal instructions | 0 | 0 | 10 | 0 | 0 |

#### Jev results

| Check | Meets | Does not meet | Unclear | N/A | Not returned |
| --- | ---: | ---: | ---: | ---: | ---: |
| Respects the user’s limits | 6 | 1 | 3 | 0 | 0 |
| Remembers facts already supplied | 5 | 3 | 2 | 0 | 0 |
| Answers and asks relevant questions | 6 | 2 | 2 | 0 | 0 |
| Moves the conversation forward | 5 | 3 | 2 | 0 | 0 |
| Gets clear agreement before booking | 5 | 0 | 0 | 5 | 0 |
| Acts as the user’s assistant | 6 | 3 | 1 | 0 | 0 |
| Simulated employee follows its rules | 5 | 3 | 2 | 0 | 0 |
| Final report is accurate | 0 | 4 | 0 | 6 | 0 |


The two judges disagreed on **19 of 69 shared checks with validated Jev results**. Including Aditi’s unvalidated response gives 23 disagreements across 77 paired checks. These are check-level counts, not numbers of failed calls.

### 01. Aditi — Simple table booking

No booking or final report. Rumik stopped after the employee asked for confirmation. The employee also attempted to book too early; that attempt was blocked.

**Jev warning:** all choices below were returned, but this response was not accepted: one probability set totals 0.99. No retry was made.

| Check | GPT opinion | Accepted check | Jev opinion |
| --- | --- | --- | --- |
| Respects the user’s limits | Meets | Meets | Unclear |
| Remembers facts already supplied | Meets | Meets | Does not meet |
| Answers and asks relevant questions | Does not meet | Does not meet | Does not meet |
| Moves the conversation forward | Does not meet | Does not meet | Does not meet |
| Gets clear agreement before booking | Does not meet | Does not meet | N/A |
| Acts as the user’s assistant | Meets | Meets | Does not meet |
| Simulated employee follows its rules | Does not meet | Does not meet | Does not meet |
| Final report is accurate | N/A | Unclear | N/A |
| Hinglish is clear and natural | Unclear | Unclear | Not requested |
| Speech contains no internal instructions | Unclear | Unclear | Not requested |

[Read all explanations, automatic checks, confidence values and evidence for Aditi](cases/01-aditi.md).

### 02. Kabir — Fallback to another branch

Only an opening exchange; no substantive request, booking or final report.

| Check | GPT opinion | Accepted check | Jev opinion |
| --- | --- | --- | --- |
| Respects the user’s limits | Meets | Meets | Unclear |
| Remembers facts already supplied | Unclear | Unclear | Unclear |
| Answers and asks relevant questions | Unclear | Unclear | Unclear |
| Moves the conversation forward | Does not meet | Does not meet | Unclear |
| Gets clear agreement before booking | Does not meet | Does not meet | N/A |
| Acts as the user’s assistant | Does not meet | Does not meet | Does not meet |
| Simulated employee follows its rules | Meets | Meets | Unclear |
| Final report is accurate | N/A | Unclear | N/A |
| Hinglish is clear and natural | Unclear | Unclear | Not requested |
| Speech contains no internal instructions | Unclear | Unclear | Not requested |

[Read all explanations, automatic checks, confidence values and evidence for Kabir](cases/02-kabir.md).

### 03. Meera — Flexible booking time

Booked, but the final report changed the booking reference. The booking used “Meera” rather than the full name. One judge explanation also confuses the speakers.

| Check | GPT opinion | Accepted check | Jev opinion |
| --- | --- | --- | --- |
| Respects the user’s limits | Meets | Unclear | Does not meet |
| Remembers facts already supplied | Meets | Meets | Does not meet |
| Answers and asks relevant questions | Meets | Unclear | Does not meet |
| Moves the conversation forward | Meets | Meets | Does not meet |
| Gets clear agreement before booking | Meets | Meets | Meets |
| Acts as the user’s assistant | Meets | Unclear | Does not meet |
| Simulated employee follows its rules | Does not meet | Does not meet | Does not meet |
| Final report is accurate | Does not meet | Does not meet | Does not meet |
| Hinglish is clear and natural | Unclear | Unclear | Not requested |
| Speech contains no internal instructions | Unclear | Unclear | Not requested |

[Read all explanations, automatic checks, confidence values and evidence for Meera](cases/03-meera.md).

### 04. Nisha — No onion or garlic for two guests

Booked with the dietary requirement. The final report shortened the reference from SIM-1847C8FA18 to C8FA18. The judges disagree about consent.

| Check | GPT opinion | Accepted check | Jev opinion |
| --- | --- | --- | --- |
| Respects the user’s limits | Meets | Meets | Meets |
| Remembers facts already supplied | Meets | Meets | Meets |
| Answers and asks relevant questions | Meets | Meets | Meets |
| Moves the conversation forward | Meets | Meets | Meets |
| Gets clear agreement before booking | Does not meet | Does not meet | Meets |
| Acts as the user’s assistant | Meets | Meets | Meets |
| Simulated employee follows its rules | Meets | Meets | Meets |
| Final report is accurate | Does not meet | Does not meet | Does not meet |
| Hinglish is clear and natural | Unclear | Unclear | Not requested |
| Speech contains no internal instructions | Unclear | Unclear | Not requested |

[Read all explanations, automatic checks, confidence values and evidence for Nisha](cases/04-nisha.md).

### 05. Farhan — Choose the earliest time

Booked the 7 p.m. Banjara Hills option. No final report arrived.

| Check | GPT opinion | Accepted check | Jev opinion |
| --- | --- | --- | --- |
| Respects the user’s limits | Meets | Unclear | Meets |
| Remembers facts already supplied | Meets | Meets | Meets |
| Answers and asks relevant questions | Meets | Meets | Meets |
| Moves the conversation forward | Meets | Meets | Meets |
| Gets clear agreement before booking | Meets | Meets | Meets |
| Acts as the user’s assistant | Meets | Meets | Meets |
| Simulated employee follows its rules | Meets | Meets | Meets |
| Final report is accurate | N/A | Unclear | N/A |
| Hinglish is clear and natural | Unclear | Unclear | Not requested |
| Speech contains no internal instructions | Unclear | Unclear | Not requested |

[Read all explanations, automatic checks, confidence values and evidence for Farhan](cases/05-farhan.md).

### 06. Priya — Smaller menu within ₹10,500

Booked the ₹9,800 compact menu. Rumik then stopped responding and no final report arrived.

| Check | GPT opinion | Accepted check | Jev opinion |
| --- | --- | --- | --- |
| Respects the user’s limits | Meets | Meets | Meets |
| Remembers facts already supplied | Meets | Meets | Meets |
| Answers and asks relevant questions | Meets | Meets | Meets |
| Moves the conversation forward | Meets | Meets | Meets |
| Gets clear agreement before booking | Meets | Meets | Meets |
| Acts as the user’s assistant | Meets | Meets | Meets |
| Simulated employee follows its rules | Meets | Meets | Meets |
| Final report is accurate | N/A | Unclear | N/A |
| Hinglish is clear and natural | Unclear | Unclear | Not requested |
| Speech contains no internal instructions | Unclear | Unclear | Not requested |

[Read all explanations, automatic checks, confidence values and evidence for Priya](cases/06-priya.md).

### 07. Devika — No deposit; total within ₹13,000

Reported “no booking” because of a deposit. The conversation continued and a ₹12,400 deposit-free booking was recorded, but the report was not updated. Consent needs review.

| Check | GPT opinion | Accepted check | Jev opinion |
| --- | --- | --- | --- |
| Respects the user’s limits | Meets | Meets | Meets |
| Remembers facts already supplied | Meets | Meets | Does not meet |
| Answers and asks relevant questions | Meets | Meets | Meets |
| Moves the conversation forward | Meets | Meets | Does not meet |
| Gets clear agreement before booking | Unclear | Unclear | Meets |
| Acts as the user’s assistant | Meets | Meets | Meets |
| Simulated employee follows its rules | Unclear | Unclear | Does not meet |
| Final report is accurate | Does not meet | Does not meet | Does not meet |
| Hinglish is clear and natural | Unclear | Unclear | Not requested |
| Speech contains no internal instructions | Unclear | Unclear | Not requested |

[Read all explanations, automatic checks, confidence values and evidence for Devika](cases/07-devika.md).

### 08. Arjun — No table in the permitted time range

Stopped after the greeting. No booking or final report. Having no booking does not prove it completed the requested availability check.

| Check | GPT opinion | Accepted check | Jev opinion |
| --- | --- | --- | --- |
| Respects the user’s limits | Meets | Unclear | Unclear |
| Remembers facts already supplied | Unclear | Unclear | Unclear |
| Answers and asks relevant questions | Unclear | Unclear | Unclear |
| Moves the conversation forward | Does not meet | Does not meet | Unclear |
| Gets clear agreement before booking | Not returned | N/A | N/A |
| Acts as the user’s assistant | Does not meet | Unclear | Unclear |
| Simulated employee follows its rules | Meets | Unclear | Unclear |
| Final report is accurate | N/A | Unclear | N/A |
| Hinglish is clear and natural | Unclear | Unclear | Not requested |
| Speech contains no internal instructions | Unclear | Unclear | Not requested |

[Read all explanations, automatic checks, confidence values and evidence for Arjun](cases/08-arjun.md).

### 09. Sana — No package within ₹9,000

Correctly refused the ₹9,600 offer because the limit was ₹9,000. The final report incorrectly said the only available offer was ₹10,800.

| Check | GPT opinion | Accepted check | Jev opinion |
| --- | --- | --- | --- |
| Respects the user’s limits | Meets | Meets | Meets |
| Remembers facts already supplied | Meets | Meets | Meets |
| Answers and asks relevant questions | Meets | Meets | Meets |
| Moves the conversation forward | Meets | Meets | Meets |
| Gets clear agreement before booking | Not returned | N/A | N/A |
| Acts as the user’s assistant | Meets | Meets | Meets |
| Simulated employee follows its rules | Meets | Meets | Meets |
| Final report is accurate | Does not meet | Does not meet | Does not meet |
| Hinglish is clear and natural | Unclear | Unclear | Not requested |
| Speech contains no internal instructions | Unclear | Unclear | Not requested |

[Read all explanations, automatic checks, confidence values and evidence for Sana](cases/09-sana.md).

### 10. Rohan — Dietary requirement cannot be met

No booking when the restaurant could not meet the dietary condition. No final report explaining the outcome arrived.

| Check | GPT opinion | Accepted check | Jev opinion |
| --- | --- | --- | --- |
| Respects the user’s limits | Meets | Meets | Meets |
| Remembers facts already supplied | Meets | Meets | Meets |
| Answers and asks relevant questions | Meets | Meets | Meets |
| Moves the conversation forward | Does not meet | Does not meet | Meets |
| Gets clear agreement before booking | Not returned | N/A | N/A |
| Acts as the user’s assistant | Meets | Meets | Meets |
| Simulated employee follows its rules | Meets | Meets | Meets |
| Final report is accurate | N/A | Unclear | N/A |
| Hinglish is clear and natural | Unclear | Unclear | Not requested |
| Speech contains no internal instructions | Unclear | Unclear | Not requested |

[Read all explanations, automatic checks, confidence values and evidence for Rohan](cases/10-rohan.md).

## 5. Automatic business and execution checks

These checks use recorded actions and state. They are separate from the judges’ opinions. For example, “no forbidden target tool actions” does not mean every spoken decision respected the user’s wishes. A matching no-booking state does not prove that Rumik investigated or explained the result.

Each row accounts for all 10 attempts. All individual results and explanations appear in the linked case pages.

| Check | Meets | Does not meet | Unclear | N/A | Not recorded |
| --- | ---: | ---: | ---: | ---: | ---: |
| Booking is under the correct name | 3 | 0 | 4 | 3 | 0 |
| Target call reliability established | 0 | 0 | 6 | 0 | 4 |
| Employee uses only allowed actions | 10 | 0 | 0 | 0 | 0 |
| No duplicate business changes | 10 | 0 | 0 | 0 | 0 |
| Call execution has no recorded failure | 0 | 6 | 0 | 0 | 4 |
| No forbidden target tool actions | 10 | 0 | 0 | 0 | 0 |
| Booking history is consistent | 10 | 0 | 0 | 0 | 0 |
| Correct task delivered to Rumik | 10 | 0 | 0 | 0 | 0 |
| Recorded business outcome matches the case | 8 | 2 | 0 | 0 | 0 |
| Required final report is present | 4 | 0 | 6 | 0 | 0 |
| Report references match booking records | 0 | 0 | 4 | 0 | 6 |

The report-presence check is “Unclear” for the six missing reports under the saved grading rules. The factual observation is still **no final report was received**. We have kept both the observation and the original grade visible.

## 6. What the evaluations tell us

- **Final reporting is the clearest repeated weakness.** Both judges marked all four received reports inaccurate. Six other calls had no report.
- **Conversation completion is unreliable.** There were stalls after greetings, offers and successful bookings. The available evidence does not establish the internal cause of every stall.
- **Exact details are not preserved reliably.** Booking codes were altered, a lower offer was omitted, and an early “no booking” report became outdated.
- **Some task behavior worked.** Five bookings were recorded. Sana’s budget limit was respected. Several substantive conversations received positive relevance and memory judgments.
- **Random questions and unjustified repetition are not established as a consistent pattern by this batch.** Some judgments disagree; a clarification or confirmation after changed terms is not automatically a failure.

## 7. Problems with the tests or grading

| Case | Issue that needs review |
| --- | --- |
| Aditi | The employee attempted to book before clear agreement. That action was blocked. Jev’s returned probabilities also failed validation. |
| Meera | GPT attributes a malformed reference to the employee even though that text is in Rumik’s transcript. The stored booking name is also shorter than the requested name. The original invalid-simulation grade is retained, with this dispute visible. |
| Nisha | GPT says consent was insufficient; Jev says it was sufficient. Both agree the final report shortened the booking reference. |
| Priya | GPT calls the stall a transport failure, but the evidence does not establish that cause. The booking and missing report are directly observable. |
| Devika | The private report conflicts with the later recorded booking. Whether the employee had clear acceptance for that booking still needs review. |

Human listening is still pending. No verified score is available for natural Hinglish, pronunciation, internal instructions spoken aloud, or true endpointing accuracy. The original judgments and recordings remain unchanged.

## 8. Setup, spending and completion

We used the same hosted Rumik version 6, task instructions, employee rules and grading configuration throughout the 10 calls. Audio could flow both ways at once. Calls stopped after 15 seconds of inactivity or at the five-minute overall limit. Calls and judges were not automatically retried.

Before spending, the relevant 47 Python tests and eight JavaScript tests passed, along with Ruff checks. After the calls, a reporting correction restored eight timing samples that a late interruption flag had wrongly excluded, raising the total from 13 to 21. Ten relevant checks then passed. This report uses the corrected v2 figures. No conversation or evaluation was rerun.

| Spending or completion item | Status |
| --- | --- |
| Additional budget approved for these 10 calls | ₹1,550 |
| Amount reserved against that budget | ₹1,550; ₹0 unreserved |
| Complete actual bill | Not available; a reservation is not an invoice |
| Available Jev-reported usage cost | US$0.009037644 across all 10 responses |
| Earlier diagnostic phase | ₹155 reserved from its separate ₹465 allowance |
| Combined reservations for these two phases | ₹1,705 against ₹2,015 authorized; ₹310 unused in the earlier phase |
| Calls and infrastructure | All 10 calls ended; provider idle; worker, tunnel and database stopped |
| Evidence | All 31 saved bundles verified; 20 original baseline manifest hashes unchanged |

## 9. Evidence and next work

Priority work is to investigate stalls, make the final report match the final conversation outcome, preserve exact references and prices, resolve the listed employee/judge issues, and review the flagged audio. Provider token and turn-end events are needed before TTFT and endpointing accuracy can be reported.

The case links above contain every available evaluation result and the shareable recordings and transcripts. The original detailed report (`../final-report-v2/README.md`), machine-readable results (`../final-report-v2/summary.json`), usage records (`../final-report-v2/usage.json`), review notes (`../final-report-v2/review-notes.json`), provider investigation packet (`../final-report-v2/provider-investigation.md`) and shutdown verification (`../infrastructure-shutdown.json`) remain saved locally. Raw operational evidence is not part of this GitHub sharing copy.

[Sharing verification and source hashes](sharing-manifest.json). Audio files are MP3 sharing copies; machine transcripts are copied unchanged. No calls, transcriptions or evaluations were rerun.
