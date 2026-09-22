# Telephony benchmark

**30 attempts · 20 connected calls · 10 cases per model.**

| Model | Connected | Passed | Failed | Unresolved |
| --- | --- | --- | --- | --- |
| Muga | 10/10 | 1 | 2 | 7 |
| Mulberry 1.5 | 10/10 | 2 | 2 | 6 |
| Mulberry 1.6 | 0/10 | 0 | 0 | 10 |

Mulberry 1.6: all 10 calls rejected (`USER_BUSY`); no audio or conversation scores.

## TTFA — response latency

Seconds from playback-finished acknowledgment to first response audio received. Lower is faster. p50 = median; p90/p95 = 90%/95% of measured turns responded within that time.

| Model | p50 (s) | p90 (s) | p95 (s) | Turns |
| --- | --- | --- | --- | --- |
| Muga | 2.42 | 3.62 | 4.26 | 50 |
| Mulberry 1.5 | 2.12 | 2.98 | 4.60 | 51 |
| Mulberry 1.6 | — | — | — | 0 |

## WER — word error rate

Errors ÷ reference words. These compare two machine transcripts; human-verified WER is pending. Different conversations and missing cases prevent a clean accuracy ranking.

| Model | WER | Errors / words | Usable cases |
| --- | --- | --- | --- |
| Muga | 24.1% | 222 / 920 | 8/10 |
| Mulberry 1.5 | 30.1% | 342 / 1138 | 9/10 |
| Mulberry 1.6 | — | — | 0/10 |

Same available case IDs (still different audio):

| Model | WER | Errors / words | Common cases |
| --- | --- | --- | --- |
| Muga | 25.9% | 208 / 802 | 7 |
| Mulberry 1.5 | 31.4% | 301 / 960 | 7 |

## TTFA for every case

All values in seconds. Each case links to its per-turn timestamps.

### Muga

| Case | p50 | p90 | p95 | Turns |
| --- | --- | --- | --- | --- |
| [01 Aditi Shah](conversations-telephony/muga/01-aditi-shah/ttfa.json) | 3.04 | 3.27 | 3.27 | 7 |
| [02 Kabir Sethi](conversations-telephony/muga/02-kabir-sethi/ttfa.json) | 2.34 | 2.75 | 3.66 | 11 |
| [03 Meera Iyer](conversations-telephony/muga/03-meera-iyer/ttfa.json) | 1.98 | 1.98 | 1.98 | 1 |
| [04 Nisha Mehta](conversations-telephony/muga/04-nisha-mehta/ttfa.json) | 2.52 | 4.30 | 4.30 | 4 |
| [05 Farhan Ali](conversations-telephony/muga/05-farhan-ali/ttfa.json) | 2.08 | 3.24 | 3.24 | 7 |
| [06 Priya Nair](conversations-telephony/muga/06-priya-nair/ttfa.json) | 2.48 | 3.62 | 3.62 | 4 |
| [07 Devika Rao](conversations-telephony/muga/07-devika-rao/ttfa.json) | 2.21 | 3.00 | 3.00 | 4 |
| [08 Arjun Menon](conversations-telephony/muga/08-arjun-menon/ttfa.json) | 2.42 | 4.26 | 4.26 | 4 |
| [09 Sana Khan](conversations-telephony/muga/09-sana-khan/ttfa.json) | 2.35 | 2.54 | 2.54 | 3 |
| [10 Rohan Desai](conversations-telephony/muga/10-rohan-desai/ttfa.json) | 3.30 | 10.94 | 10.94 | 5 |

### Mulberry 1.5

| Case | p50 | p90 | p95 | Turns |
| --- | --- | --- | --- | --- |
| [01 Aditi Shah](conversations-telephony/mulberry-1-5/01-aditi-shah/ttfa.json) | 2.22 | 6.01 | 6.01 | 8 |
| [02 Kabir Sethi](conversations-telephony/mulberry-1-5/02-kabir-sethi/ttfa.json) | 2.03 | 3.06 | 3.06 | 7 |
| [03 Meera Iyer](conversations-telephony/mulberry-1-5/03-meera-iyer/ttfa.json) | 2.16 | 2.49 | 2.49 | 3 |
| [04 Nisha Mehta](conversations-telephony/mulberry-1-5/04-nisha-mehta/ttfa.json) | 2.06 | 2.60 | 2.60 | 7 |
| [05 Farhan Ali](conversations-telephony/mulberry-1-5/05-farhan-ali/ttfa.json) | 2.12 | 4.36 | 4.36 | 4 |
| [06 Priya Nair](conversations-telephony/mulberry-1-5/06-priya-nair/ttfa.json) | 1.86 | 2.54 | 2.54 | 5 |
| [07 Devika Rao](conversations-telephony/mulberry-1-5/07-devika-rao/ttfa.json) | 2.04 | 5.34 | 5.34 | 6 |
| [08 Arjun Menon](conversations-telephony/mulberry-1-5/08-arjun-menon/ttfa.json) | 2.12 | 2.56 | 2.56 | 4 |
| [09 Sana Khan](conversations-telephony/mulberry-1-5/09-sana-khan/ttfa.json) | 2.10 | 4.60 | 4.60 | 4 |
| [10 Rohan Desai](conversations-telephony/mulberry-1-5/10-rohan-desai/ttfa.json) | 1.82 | 2.22 | 2.22 | 3 |

## WER for every case

Each value links to its reference transcript, recognized transcript and error counts. Missing values are not zero.

| Case | Muga: WER (errors/words) | Mulberry 1.5: WER (errors/words) |
| --- | --- | --- |
| 01 Aditi Shah | [26.1% (47/180)](conversations-telephony/muga/01-aditi-shah/wer.md) | [36.9% (80/217)](conversations-telephony/mulberry-1-5/01-aditi-shah/wer.md) |
| 02 Kabir Sethi | [Incomplete playback](conversations-telephony/muga/02-kabir-sethi/wer.md) | [22.7% (22/97)](conversations-telephony/mulberry-1-5/02-kabir-sethi/wer.md) |
| 03 Meera Iyer | [Incomplete playback](conversations-telephony/muga/03-meera-iyer/wer.md) | [23.5% (19/81)](conversations-telephony/mulberry-1-5/03-meera-iyer/wer.md) |
| 04 Nisha Mehta | [16.2% (17/105)](conversations-telephony/muga/04-nisha-mehta/wer.md) | [30.6% (55/180)](conversations-telephony/mulberry-1-5/04-nisha-mehta/wer.md) |
| 05 Farhan Ali | [36.4% (52/143)](conversations-telephony/muga/05-farhan-ali/wer.md) | [33.0% (31/94)](conversations-telephony/mulberry-1-5/05-farhan-ali/wer.md) |
| 06 Priya Nair | [23.7% (22/93)](conversations-telephony/muga/06-priya-nair/wer.md) | [26.7% (39/146)](conversations-telephony/mulberry-1-5/06-priya-nair/wer.md) |
| 07 Devika Rao | [30.6% (38/124)](conversations-telephony/muga/07-devika-rao/wer.md) | [46.3% (69/149)](conversations-telephony/mulberry-1-5/07-devika-rao/wer.md) |
| 08 Arjun Menon | [10.6% (10/94)](conversations-telephony/muga/08-arjun-menon/wer.md) | [17.1% (14/82)](conversations-telephony/mulberry-1-5/08-arjun-menon/wer.md) |
| 09 Sana Khan | [34.9% (22/63)](conversations-telephony/muga/09-sana-khan/wer.md) | [14.1% (13/92)](conversations-telephony/mulberry-1-5/09-sana-khan/wer.md) |
| 10 Rohan Desai | [11.9% (14/118)](conversations-telephony/muga/10-rohan-desai/wer.md) | [Incomplete playback](conversations-telephony/mulberry-1-5/10-rohan-desai/wer.md) |

Mulberry 1.6: WER and TTFA unavailable for every case because no call connected.

## Test results — what passed and why

Pass requires a valid employee simulation, completed prerequisites and all required checks passing. Unresolved means the evidence or simulation does not support a final verdict. Jev is reported separately.

### Muga

| Case / metric proof | Result | Reason |
| --- | --- | --- |
| [01 Aditi Shah](conversations-telephony/muga/01-aditi-shah/README.md) | Unresolved | Booking and report match; spoken consent still needs review. |
| [02 Kabir Sethi](conversations-telephony/muga/02-kabir-sethi/README.md) | Unresolved | Simulation needs review; report truncates the reference. Jev request failed. |
| [03 Meera Iyer](conversations-telephony/muga/03-meera-iyer/README.md) | Unresolved | Employee stopped after greeting; no booking or report. |
| [04 Nisha Mehta](conversations-telephony/muga/04-nisha-mehta/README.md) | Unresolved | Employee offered the wrong time; no booking. |
| [05 Farhan Ali](conversations-telephony/muga/05-farhan-ali/README.md) | Unresolved | Booking saved; employee gave inconsistent reference numbers. |
| [06 Priya Nair](conversations-telephony/muga/06-priya-nair/README.md) | Unresolved | Employee saved the wrong name and gave an incomplete reference. |
| [07 Devika Rao](conversations-telephony/muga/07-devika-rao/README.md) | Failed | Wrong branch spoken; report changed SIM-501703 to PIM 50 1703. |
| [08 Arjun Menon](conversations-telephony/muga/08-arjun-menon/README.md) | Passed | Correctly declined unavailable times; no booking; accurate report. |
| [09 Sana Khan](conversations-telephony/muga/09-sana-khan/README.md) | Failed | Correctly declined the price; report omitted required task details. |
| [10 Rohan Desai](conversations-telephony/muga/10-rohan-desai/README.md) | Unresolved | Employee misstated the available time; execution also failed. |

### Mulberry 1.5

| Case / metric proof | Result | Reason |
| --- | --- | --- |
| [01 Aditi Shah](conversations-telephony/mulberry-1-5/01-aditi-shah/README.md) | Unresolved | Booking saved, but employee conversation and reference loop were invalid. |
| [02 Kabir Sethi](conversations-telephony/mulberry-1-5/02-kabir-sethi/README.md) | Unresolved | Booking and report match; employee gave a false reference correction. |
| [03 Meera Iyer](conversations-telephony/mulberry-1-5/03-meera-iyer/README.md) | Failed | Wrong task details spoken; report split one reference into two. |
| [04 Nisha Mehta](conversations-telephony/mulberry-1-5/04-nisha-mehta/README.md) | Unresolved | Booking saved; report reference is wrong. Jev answer failed validation. |
| [05 Farhan Ali](conversations-telephony/mulberry-1-5/05-farhan-ali/README.md) | Failed | Booking saved; report changed SIM-856277 to PIM 856277. |
| [06 Priya Nair](conversations-telephony/mulberry-1-5/06-priya-nair/README.md) | Passed | Correct ₹9,800 booking, consent, name and reference; accurate report. |
| [07 Devika Rao](conversations-telephony/mulberry-1-5/07-devika-rao/README.md) | Unresolved | Employee booked without clear consent; simulation invalid. |
| [08 Arjun Menon](conversations-telephony/mulberry-1-5/08-arjun-menon/README.md) | Passed | Correctly declined unavailable times; no booking; accurate report. |
| [09 Sana Khan](conversations-telephony/mulberry-1-5/09-sana-khan/README.md) | Unresolved | No booking; Luna omitted a required metric, so grading is incomplete. |
| [10 Rohan Desai](conversations-telephony/mulberry-1-5/10-rohan-desai/README.md) | Unresolved | Correct no-booking decision and report; execution failure remains unresolved. |

## Jev judgment

Independent second opinion. These are individual checks, not an invented overall Jev score. Click a case for all eight judgments and the original response.

### Muga

| Case / full judgment | Employee simulation | Constraints | Consent | Report accuracy |
| --- | --- | --- | --- | --- |
| [01 Aditi Shah](conversations-telephony/muga/01-aditi-shah/jev.md) | Pass | Pass | Pass | Pass |
| [02 Kabir Sethi](conversations-telephony/muga/02-kabir-sethi/jev.md) | Error | Error | Error | Error |
| [03 Meera Iyer](conversations-telephony/muga/03-meera-iyer/jev.md) | Review | Review | N/A | N/A |
| [04 Nisha Mehta](conversations-telephony/muga/04-nisha-mehta/jev.md) | Fail | Fail | N/A | Fail |
| [05 Farhan Ali](conversations-telephony/muga/05-farhan-ali/jev.md) | Pass | Pass | Pass | Pass |
| [06 Priya Nair](conversations-telephony/muga/06-priya-nair/jev.md) | Fail | Fail | Pass | Fail |
| [07 Devika Rao](conversations-telephony/muga/07-devika-rao/jev.md) | Fail | Fail | Pass | Fail |
| [08 Arjun Menon](conversations-telephony/muga/08-arjun-menon/jev.md) | Pass | Pass | N/A | Pass |
| [09 Sana Khan](conversations-telephony/muga/09-sana-khan/jev.md) | Pass | Pass | N/A | Pass |
| [10 Rohan Desai](conversations-telephony/muga/10-rohan-desai/jev.md) | Pass | Pass | N/A | Pass |

### Mulberry 1.5

| Case / full judgment | Employee simulation | Constraints | Consent | Report accuracy |
| --- | --- | --- | --- | --- |
| [01 Aditi Shah](conversations-telephony/mulberry-1-5/01-aditi-shah/jev.md) | Pass | Pass | Pass | Pass |
| [02 Kabir Sethi](conversations-telephony/mulberry-1-5/02-kabir-sethi/jev.md) | Pass | Pass | Pass | Pass |
| [03 Meera Iyer](conversations-telephony/mulberry-1-5/03-meera-iyer/jev.md) | Fail | Fail | Pass | Fail |
| [04 Nisha Mehta](conversations-telephony/mulberry-1-5/04-nisha-mehta/jev.md) | Error | Error | Error | Error |
| [05 Farhan Ali](conversations-telephony/mulberry-1-5/05-farhan-ali/jev.md) | Pass | Fail | Pass | Fail |
| [06 Priya Nair](conversations-telephony/mulberry-1-5/06-priya-nair/jev.md) | Pass | Pass | Pass | Pass |
| [07 Devika Rao](conversations-telephony/mulberry-1-5/07-devika-rao/jev.md) | Pass | Pass | Pass | Pass |
| [08 Arjun Menon](conversations-telephony/mulberry-1-5/08-arjun-menon/jev.md) | Pass | Pass | N/A | Pass |
| [09 Sana Khan](conversations-telephony/mulberry-1-5/09-sana-khan/jev.md) | Pass | Pass | N/A | Pass |
| [10 Rohan Desai](conversations-telephony/mulberry-1-5/10-rohan-desai/jev.md) | Pass | Pass | N/A | Pass |

Jev errors: Muga/Kabir exceeded the token limit; Mulberry 1.5/Nisha returned an inconsistent choice. Mulberry 1.6 was not judged. N/A = check does not apply; Review = uncertain.

## Audio, transcripts and proof — all 30 attempts

| Case | Muga | Mulberry 1.5 | Mulberry 1.6 |
| --- | --- | --- | --- |
| 01 Aditi Shah | [Audio](conversations-telephony/muga/01-aditi-shah/conversation.mp3) · [Transcript](conversations-telephony/muga/01-aditi-shah/transcript.md) · [Proof](conversations-telephony/muga/01-aditi-shah/README.md) | [Audio](conversations-telephony/mulberry-1-5/01-aditi-shah/conversation.mp3) · [Transcript](conversations-telephony/mulberry-1-5/01-aditi-shah/transcript.md) · [Proof](conversations-telephony/mulberry-1-5/01-aditi-shah/README.md) | [Rejection proof](conversations-telephony/mulberry-1-6/01-aditi-shah/provider-summary.json) |
| 02 Kabir Sethi | [Audio](conversations-telephony/muga/02-kabir-sethi/conversation.mp3) · [Transcript](conversations-telephony/muga/02-kabir-sethi/transcript.md) · [Proof](conversations-telephony/muga/02-kabir-sethi/README.md) | [Audio](conversations-telephony/mulberry-1-5/02-kabir-sethi/conversation.mp3) · [Transcript](conversations-telephony/mulberry-1-5/02-kabir-sethi/transcript.md) · [Proof](conversations-telephony/mulberry-1-5/02-kabir-sethi/README.md) | [Rejection proof](conversations-telephony/mulberry-1-6/02-kabir-sethi/provider-summary.json) |
| 03 Meera Iyer | [Audio](conversations-telephony/muga/03-meera-iyer/conversation.mp3) · [Transcript](conversations-telephony/muga/03-meera-iyer/transcript.md) · [Proof](conversations-telephony/muga/03-meera-iyer/README.md) | [Audio](conversations-telephony/mulberry-1-5/03-meera-iyer/conversation.mp3) · [Transcript](conversations-telephony/mulberry-1-5/03-meera-iyer/transcript.md) · [Proof](conversations-telephony/mulberry-1-5/03-meera-iyer/README.md) | [Rejection proof](conversations-telephony/mulberry-1-6/03-meera-iyer/provider-summary.json) |
| 04 Nisha Mehta | [Audio](conversations-telephony/muga/04-nisha-mehta/conversation.mp3) · [Transcript](conversations-telephony/muga/04-nisha-mehta/transcript.md) · [Proof](conversations-telephony/muga/04-nisha-mehta/README.md) | [Audio](conversations-telephony/mulberry-1-5/04-nisha-mehta/conversation.mp3) · [Transcript](conversations-telephony/mulberry-1-5/04-nisha-mehta/transcript.md) · [Proof](conversations-telephony/mulberry-1-5/04-nisha-mehta/README.md) | [Rejection proof](conversations-telephony/mulberry-1-6/04-nisha-mehta/provider-summary.json) |
| 05 Farhan Ali | [Audio](conversations-telephony/muga/05-farhan-ali/conversation.mp3) · [Transcript](conversations-telephony/muga/05-farhan-ali/transcript.md) · [Proof](conversations-telephony/muga/05-farhan-ali/README.md) | [Audio](conversations-telephony/mulberry-1-5/05-farhan-ali/conversation.mp3) · [Transcript](conversations-telephony/mulberry-1-5/05-farhan-ali/transcript.md) · [Proof](conversations-telephony/mulberry-1-5/05-farhan-ali/README.md) | [Rejection proof](conversations-telephony/mulberry-1-6/05-farhan-ali/provider-summary.json) |
| 06 Priya Nair | [Audio](conversations-telephony/muga/06-priya-nair/conversation.mp3) · [Transcript](conversations-telephony/muga/06-priya-nair/transcript.md) · [Proof](conversations-telephony/muga/06-priya-nair/README.md) | [Audio](conversations-telephony/mulberry-1-5/06-priya-nair/conversation.mp3) · [Transcript](conversations-telephony/mulberry-1-5/06-priya-nair/transcript.md) · [Proof](conversations-telephony/mulberry-1-5/06-priya-nair/README.md) | [Rejection proof](conversations-telephony/mulberry-1-6/06-priya-nair/provider-summary.json) |
| 07 Devika Rao | [Audio](conversations-telephony/muga/07-devika-rao/conversation.mp3) · [Transcript](conversations-telephony/muga/07-devika-rao/transcript.md) · [Proof](conversations-telephony/muga/07-devika-rao/README.md) | [Audio](conversations-telephony/mulberry-1-5/07-devika-rao/conversation.mp3) · [Transcript](conversations-telephony/mulberry-1-5/07-devika-rao/transcript.md) · [Proof](conversations-telephony/mulberry-1-5/07-devika-rao/README.md) | [Rejection proof](conversations-telephony/mulberry-1-6/07-devika-rao/provider-summary.json) |
| 08 Arjun Menon | [Audio](conversations-telephony/muga/08-arjun-menon/conversation.mp3) · [Transcript](conversations-telephony/muga/08-arjun-menon/transcript.md) · [Proof](conversations-telephony/muga/08-arjun-menon/README.md) | [Audio](conversations-telephony/mulberry-1-5/08-arjun-menon/conversation.mp3) · [Transcript](conversations-telephony/mulberry-1-5/08-arjun-menon/transcript.md) · [Proof](conversations-telephony/mulberry-1-5/08-arjun-menon/README.md) | [Rejection proof](conversations-telephony/mulberry-1-6/08-arjun-menon/provider-summary.json) |
| 09 Sana Khan | [Audio](conversations-telephony/muga/09-sana-khan/conversation.mp3) · [Transcript](conversations-telephony/muga/09-sana-khan/transcript.md) · [Proof](conversations-telephony/muga/09-sana-khan/README.md) | [Audio](conversations-telephony/mulberry-1-5/09-sana-khan/conversation.mp3) · [Transcript](conversations-telephony/mulberry-1-5/09-sana-khan/transcript.md) · [Proof](conversations-telephony/mulberry-1-5/09-sana-khan/README.md) | [Rejection proof](conversations-telephony/mulberry-1-6/09-sana-khan/provider-summary.json) |
| 10 Rohan Desai | [Audio](conversations-telephony/muga/10-rohan-desai/conversation.mp3) · [Transcript](conversations-telephony/muga/10-rohan-desai/transcript.md) · [Proof](conversations-telephony/muga/10-rohan-desai/README.md) | [Audio](conversations-telephony/mulberry-1-5/10-rohan-desai/conversation.mp3) · [Transcript](conversations-telephony/mulberry-1-5/10-rohan-desai/transcript.md) · [Proof](conversations-telephony/mulberry-1-5/10-rohan-desai/README.md) | [Rejection proof](conversations-telephony/mulberry-1-6/10-rohan-desai/provider-summary.json) |

[Data](../reports/telephony-benchmark-20260922/report-v4/summary.json) · [CSV](../reports/telephony-benchmark-20260922/report-v4/cases.csv) · [TTFA timestamps](../reports/telephony-benchmark-20260922/report-v4/ttfa-observations.csv) · [Method](../reports/telephony-benchmark-20260922/report-v4/ttfa-methodology.json) · [Detailed methodology](../reports/telephony-benchmark-20260922/report-v3/README.md) · [Verification](../reports/telephony-benchmark-20260922/report-v4/verification.json)
