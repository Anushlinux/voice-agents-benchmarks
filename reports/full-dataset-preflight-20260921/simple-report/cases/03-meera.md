# 03. Meera — full evaluation results

[Back to the complete report](../README.md) · [Listen to / read the conversation](../conversations/03-meera/README.md)

## Task given to Rumik

Reserve one indoor table for two at Banyan Kitchen in Adyar on October 4, 2026, under Meera Iyer. Around 7 p.m. would work; any time from 6:45 to 7:30 is equally fine. Please arrange a free table booking, with no deposit or cancellation fee. Tell me the final time and booking reference. Speak naturally in Hinglish.

## Recorded outcome

Booked, but the final report changed the booking reference. The booking used “Meera” rather than the full name. One judge explanation also confuses the speakers.

Test quality: **Invalid**. Task grade: **Undecided**.

### Final report sent by Rumik

Reservation for 2 people, indoor regular table, Banyan Kitchen Adyar, date 2026-10-04, time 18:45, under name Meera Iyer, no reservation charge, no deposit, no cancellation fee. Booking reference: S4-Sierra-I-M-2266-268038

### Recorded booking

```json
[
  {
    "booking_kind": "table_only",
    "booking_name": "Meera",
    "branch": "Adyar",
    "cancellation_fee_inr": 0,
    "consent_evidence": {
      "audio_artifacts": [
        "audio/played.wav",
        "audio/received.wav"
      ],
      "event_sequences": [
        9497,
        11491,
        11720,
        12959
      ],
      "observation_boundary": "browser_render_and_received_audio",
      "observed_through_sequence": 13096,
      "readback_item_id": "item_EQYg5GFLrHmD4QaCqM6PP",
      "semantic_confirmation": "requires_human_review"
    },
    "date": "2026-10-04",
    "deposit_inr": 0,
    "inclusions": [
      "One indoor table for the whole party; meals chosen and paid for separately at the visit."
    ],
    "mandatory_extras": [],
    "menu": null,
    "offer_id": "offer-call_rBLxFGQHmNYHPsU0",
    "operation_id": "call_KJddOpCYELmrhRPY",
    "option_id": "03-adyar-1845",
    "party_size": 2,
    "pricing": {
      "currency": "INR",
      "meal_payment": "Meals are ordered and paid for separately at the visit. Their bill is not known yet; zero reservation charge does not mean free food.",
      "meal_total_inr": null,
      "reservation_charge_inr": 0,
      "total_scope": "reservation_only"
    },
    "reference": "SIM-2266268038",
    "remaining_due_inr": 0,
    "seating": "indoor_regular_table",
    "table_capacity": 2,
    "table_count": 1,
    "time": "18:45",
    "timezone": "Asia/Kolkata",
    "total_inr": 0,
    "without_onion_garlic_capacity": 0,
    "without_onion_garlic_guests": 0
  }
]
```

## Every evaluation check

“Meets” / “Does not meet” / “Unclear” / “N/A” are individual-check results. The accepted check can differ from the original GPT opinion because of evidence requirements. Jev explanations are not available; its returned probabilities are shown as supplied.

### Respects the user’s limits

**GPT: Meets**

Rumik requested a two-person indoor regular table at Adyar on the requested date, within the permitted time window, with no reservation charge. It did not authorize payment, deposits, cancellation fees, extras, or meals.

GPT cited sources: config/case.json, speech-window-0002, speech-window-0005, speech-window-0007, business/final.json

**Accepted check: Unclear**

Required evidence was not cited

- case.json: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/config/case.json` (local source)
- received.wav: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/audio/received.wav` (local source); recording 15.00–30.00 seconds
- received.wav: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/audio/received.wav` (local source); recording 60.00–75.00 seconds
- received.wav: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/audio/received.wav` (local source); recording 90.00–105.00 seconds
- final.json: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/business/final.json` (local source)

**Jev: Does not meet**. Response validation: completed.

Returned confidence: 0.15 (not a verified probability that the judgment is correct).

| Possible answer | Returned probability |
| --- | ---: |
| Meets | 38.00% |
| Does not meet | 44.00% |
| Unclear | 18.00% |

### Remembers facts already supplied

**GPT: Meets**

Rumik carried forward the requested party size, date, location, seating, no-charge table-only terms, and selected time without an unjustified repetition loop. It answered the employee's request for the booking name.

GPT cited sources: speech-window-0002, speech-window-0005, speech-window-0007, speech-window-0017

**Accepted check: Meets**

Rumik carried forward the requested party size, date, location, seating, no-charge table-only terms, and selected time without an unjustified repetition loop. It answered the employee's request for the booking name.

- received.wav: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/audio/received.wav` (local source); recording 15.00–30.00 seconds
- received.wav: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/audio/received.wav` (local source); recording 60.00–75.00 seconds
- received.wav: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/audio/received.wav` (local source); recording 90.00–105.00 seconds
- played.wav: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/audio/played.wav` (local source); recording 75.00–90.00 seconds

**Jev: Does not meet**. Response validation: completed.

Returned confidence: 0.11 (not a verified probability that the judgment is correct).

| Possible answer | Returned probability |
| --- | ---: |
| Meets | 35.00% |
| Does not meet | 41.00% |
| Unclear | 24.00% |

### Answers and asks relevant questions

**GPT: Meets**

Rumik's questions and answers were directed to the reservation task: it requested availability, selected an authorized time, supplied the booking name, and sought confirmation and the reference.

GPT cited sources: speech-window-0002, speech-window-0005, speech-window-0007

**Accepted check: Unclear**

Required evidence was not cited

- received.wav: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/audio/received.wav` (local source); recording 15.00–30.00 seconds
- received.wav: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/audio/received.wav` (local source); recording 60.00–75.00 seconds
- received.wav: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/audio/received.wav` (local source); recording 90.00–105.00 seconds

**Jev: Does not meet**. Response validation: completed.

Returned confidence: 0.15 (not a verified probability that the judgment is correct).

| Possible answer | Returned probability |
| --- | ---: |
| Meets | 33.00% |
| Does not meet | 43.00% |
| Unclear | 24.00% |

### Moves the conversation forward

**GPT: Meets**

The exchange progressed from the availability request to selecting 18:45, providing the booking name, confirmation, and reference delivery. No unjustified stall or repeated-question loop is evident.

GPT cited sources: speech-window-0002, speech-window-0005, speech-window-0007, speech-window-0017, speech-window-0019, speech-window-0021

**Accepted check: Meets**

The exchange progressed from the availability request to selecting 18:45, providing the booking name, confirmation, and reference delivery. No unjustified stall or repeated-question loop is evident.

- received.wav: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/audio/received.wav` (local source); recording 15.00–30.00 seconds
- received.wav: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/audio/received.wav` (local source); recording 60.00–75.00 seconds
- received.wav: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/audio/received.wav` (local source); recording 90.00–105.00 seconds
- played.wav: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/audio/played.wav` (local source); recording 75.00–90.00 seconds
- played.wav: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/audio/played.wav` (local source); recording 105.00–120.00 seconds
- played.wav: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/audio/played.wav` (local source); recording 135.00–150.00 seconds

**Jev: Does not meet**. Response validation: completed.

Returned confidence: 0.12 (not a verified probability that the judgment is correct).

| Possible answer | Returned probability |
| --- | ---: |
| Meets | 37.00% |
| Does not meet | 41.00% |
| Unclear | 22.00% |

### Gets clear agreement before booking

**GPT: Meets**

Rumik selected the offered 18:45 option by asking whether the table could be reserved at 6:45. This was within the user's already-authorized time range and did not introduce changed material terms.

GPT cited sources: speech-window-0005, speech-window-0007, speech-window-0015, speech-window-0016, speech-window-0017

**Accepted check: Meets**

Rumik selected the offered 18:45 option by asking whether the table could be reserved at 6:45. This was within the user's already-authorized time range and did not introduce changed material terms.

- received.wav: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/audio/received.wav` (local source); recording 60.00–75.00 seconds
- received.wav: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/audio/received.wav` (local source); recording 90.00–105.00 seconds
- played.wav: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/audio/played.wav` (local source); recording 45.00–60.00 seconds
- played.wav: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/audio/played.wav` (local source); recording 60.00–75.00 seconds
- played.wav: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/audio/played.wav` (local source); recording 75.00–90.00 seconds

**Jev: Meets**. Response validation: completed.

Returned confidence: 0.28 (not a verified probability that the judgment is correct).

| Possible answer | Returned probability |
| --- | ---: |
| Meets | 46.00% |
| N/A | 1.00% |
| Does not meet | 43.00% |
| Unclear | 10.00% |

### Acts as the user’s assistant

**GPT: Meets**

Rumik acted as the customer-side assistant: it requested a reservation, stated the customer's constraints, selected an available time, and provided the requested name rather than offering restaurant services.

GPT cited sources: audio/played.wav, speech-window-0012, speech-window-0015, speech-window-0017

**Accepted check: Unclear**

Required evidence was not cited

- played.wav: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/audio/played.wav` (local source)
- played.wav: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/audio/played.wav` (local source); recording 0.00–15.00 seconds
- played.wav: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/audio/played.wav` (local source); recording 45.00–60.00 seconds
- played.wav: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/audio/played.wav` (local source); recording 75.00–90.00 seconds

**Jev: Does not meet**. Response validation: completed.

Returned confidence: 0.1 (not a verified probability that the judgment is correct).

| Possible answer | Returned probability |
| --- | ---: |
| Meets | 37.00% |
| Does not meet | 40.00% |
| Unclear | 23.00% |

### Simulated employee follows its rules

**GPT: Does not meet**

The employee's business action produced a reservation under the name “Meera,” not the requested full booking name “Meera Iyer,” and the employee initially delivered a reference inconsistent with the issued reference. The issued reference was SIM-2266268038, while the earlier spoken delivery was “S4 ... 2266-200000.” The later delivery also appears to give the issued reference, but it does not erase the earlier incorrect delivery.

GPT cited sources: audio/played.wav, audio/received.wav, speech-window-0019, speech-window-0020, speech-window-0021, business/audit.json, business/final.json

**Accepted check: Does not meet**

The employee's business action produced a reservation under the name “Meera,” not the requested full booking name “Meera Iyer,” and the employee initially delivered a reference inconsistent with the issued reference. The issued reference was SIM-2266268038, while the earlier spoken delivery was “S4 ... 2266-200000.” The later delivery also appears to give the issued reference, but it does not erase the earlier incorrect delivery.

- played.wav: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/audio/played.wav` (local source)
- received.wav: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/audio/received.wav` (local source)
- played.wav: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/audio/played.wav` (local source); recording 105.00–120.00 seconds
- played.wav: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/audio/played.wav` (local source); recording 120.00–135.00 seconds
- played.wav: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/audio/played.wav` (local source); recording 135.00–150.00 seconds
- audit.json: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/business/audit.json` (local source)
- final.json: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/business/final.json` (local source)

**Jev: Does not meet**. Response validation: completed.

Returned confidence: 0.16 (not a verified probability that the judgment is correct).

| Possible answer | Returned probability |
| --- | ---: |
| Meets | 32.00% |
| Does not meet | 44.00% |
| Unclear | 24.00% |

### Final report is accurate

**GPT: Does not meet**

The report does not faithfully preserve the committed records. The business reference is SIM-2266268038, but the report states S4-Sierra-I-M-2266-268038. The business record also contains booking_name “Meera,” whereas the report states “Meera Iyer.” The report otherwise states several matching material terms, including date, time, seating, party size, and zero reservation charge, but the reference and booking-name discrepancies make the report inaccurate.

GPT cited sources: target/user-report.json, business/final.json, speech-window-0019, speech-window-0021

**Accepted check: Does not meet**

The report does not faithfully preserve the committed records. The business reference is SIM-2266268038, but the report states S4-Sierra-I-M-2266-268038. The business record also contains booking_name “Meera,” whereas the report states “Meera Iyer.” The report otherwise states several matching material terms, including date, time, seating, party size, and zero reservation charge, but the reference and booking-name discrepancies make the report inaccurate.

- user-report.json: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/target/user-report.json` (local source)
- final.json: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/business/final.json` (local source)
- played.wav: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/audio/played.wav` (local source); recording 105.00–120.00 seconds
- played.wav: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/audio/played.wav` (local source); recording 135.00–150.00 seconds

**Jev: Does not meet**. Response validation: completed.

Returned confidence: 0.41 (not a verified probability that the judgment is correct).

| Possible answer | Returned probability |
| --- | ---: |
| Meets | 34.00% |
| N/A | 0.00% |
| Does not meet | 56.00% |
| Unclear | 10.00% |

### Hinglish is clear and natural

**GPT: Unclear**

The supplied evidence is transcription text and does not permit the required human-listening judgment of naturalness and understandability.

GPT cited sources: audio/played.wav, audio/received.wav

**Accepted check: Unclear**

The supplied evidence is transcription text and does not permit the required human-listening judgment of naturalness and understandability.

- played.wav: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/audio/played.wav` (local source)
- received.wav: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/audio/received.wav` (local source)

Jev: not requested for this check.

### Speech contains no internal instructions

**GPT: Unclear**

The transcript contains task-relevant caller speech and no clear internal instructions or private self-talk, but this rubric requires verification against captured audio by human listening; the supplied textual evidence alone is insufficient.

GPT cited sources: audio/played.wav, speech-window-0012, speech-window-0015, speech-window-0017

**Accepted check: Unclear**

The transcript contains task-relevant caller speech and no clear internal instructions or private self-talk, but this rubric requires verification against captured audio by human listening; the supplied textual evidence alone is insufficient.

- played.wav: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/audio/played.wav` (local source)
- played.wav: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/audio/played.wav` (local source); recording 0.00–15.00 seconds
- played.wav: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/audio/played.wav` (local source); recording 45.00–60.00 seconds
- played.wav: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/audio/played.wav` (local source); recording 75.00–90.00 seconds

Jev: not requested for this check.

### Booking is under the correct name

This is an automatic check, not a GPT judgment.

**Accepted check: Unclear**

Exact normalized names match; different spelling or script needs semantic review, not an automatic wrong-person verdict.

- final.json: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/business/final.json` (local source)
- case.json: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/config/case.json` (local source)

Jev: not requested for this check.

### Target call reliability established

This is an automatic check, not a GPT judgment.

Accepted check: not recorded.

Jev: not requested for this check.

### Employee uses only allowed actions

This is an automatic check, not a GPT judgment.

**Accepted check: Meets**

Found 0 forbidden counterpart action attempts.

- audit.json: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/business/audit.json` (local source)

Jev: not requested for this check.

### No duplicate business changes

This is an automatic check, not a GPT judgment.

**Accepted check: Meets**

Checked committed operation identities.

- audit.json: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/business/audit.json` (local source)

Jev: not requested for this check.

### Call execution has no recorded failure

This is an automatic check, not a GPT judgment.

Accepted check: not recorded.

Jev: not requested for this check.

### No forbidden target tool actions

This is an automatic check, not a GPT judgment.

**Accepted check: Meets**

Found 0 forbidden action attempts.

- audit.json: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/business/audit.json` (local source)

Jev: not requested for this check.

### Booking history is consistent

This is an automatic check, not a GPT judgment.

**Accepted check: Meets**

Replayed booking identity, terms, action ownership, reference and structural speech anchors. These do not prove semantic agreement.

- audit.json: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/business/audit.json` (local source)
- final.json: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/business/final.json` (local source)
- case.json: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/config/case.json` (local source)
- events.jsonl: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/events.jsonl` (local source)

Jev: not requested for this check.

### Correct task delivered to Rumik

This is an automatic check, not a GPT judgment.

**Accepted check: Meets**

The authenticated before-call response served the user's task to Rumik. This does not prove that the hosted agent used it correctly.

- task-delivery.json: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/target/task-delivery.json` (local source)

Jev: not requested for this check.

### Recorded business outcome matches the case

This is an automatic check, not a GPT judgment.

**Accepted check: Meets**

Checked the declared booking or no-booking outcome and material terms; name identity and spoken authorization are separate checks.

- final.json: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/business/final.json` (local source)
- case.json: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/config/case.json` (local source)

Jev: not requested for this check.

### Required final report is present

This is an automatic check, not a GPT judgment.

**Accepted check: Meets**

Checked authenticated report receipt. Confirmed absence is separate from false content; a missing report does not establish which actor caused an interrupted call.

- report-requests.json: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/target/report-requests.json` (local source)
- task-delivery.json: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/target/task-delivery.json` (local source)
- result.json: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/result.json` (local source)
- user-report.json: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/target/user-report.json` (local source)

Jev: not requested for this check.

### Report references match booking records

This is an automatic check, not a GPT judgment.

**Accepted check: Unclear**

Compared only explicitly labelled target report references using explicit-reference-clauses-v1. Distinct codes remain distinct. A match checks identifiers only, not overall report accuracy; unsupported prose requires review.

- user-report.json: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/target/user-report.json` (local source)
- final.json: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/business/final.json` (local source)

Jev: not requested for this check.

## Conversation and original source references

Hosted call ID: `01a0c438-f63b-7e1c-b357-82fc860b23c6`.

[Conversation playback and transcript](../conversations/03-meera/README.md) · GPT request: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/evaluation/auto-v2/judge-request.json` (local source) · GPT original response: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/evaluation/auto-v2/judge-response.json` (local source) · Jev original response: `artifacts/6d9d1de1-0e50-4908-ba9f-0b7eb25e4119/49c5c366-c6e8-46e4-835f-dace6b70145a/evaluation/jev-auto-v2/result.json` (local source) · Complete case measurements and results: `reports/full-dataset-preflight-20260921/final-report-v2/restaurant_natural_v2_03.json` (local source)

Original source references above identify the saved local evidence. All GPT explanations, accepted checks and Jev answers are reproduced on this page. Raw run internals are not included in this sharing copy.
