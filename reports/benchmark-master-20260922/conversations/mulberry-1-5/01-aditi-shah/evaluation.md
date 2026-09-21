# Conversation and benchmark result

Automated outcome: **unresolved**. Simulation validity: **invalid**.

Full evaluation: **completed**. Conversation repair accepted: **False**.

Human listening is pending. Text judges cannot establish acoustic naturalness or prove that suspected self-talk was audible.

Book an indoor table for three at Neem Courtyard in Aundh on October 2, 2026 at 7:30 p.m., under Aditi Shah. We want to sit together. Please make a table reservation only, with no booking charge, deposit or cancellation fee. Let me know the booking details and reference, or tell me if it cannot be arranged. Speak naturally in Hinglish.

[Independent transcript](transcript.md) · [All metrics and raw judge answers](details.json) · [Failure evidence and uncertainty](diagnostics-v1.json) · [Timing, WER and endpointing availability](measurements-v2.json) · [Per-turn timestamps](turn-timestamps.csv)

Observed task completion: **unresolved**. Established failure owner: **unknown**. Missing required outputs remain visible even when their cause is unknown.

Left audio: restaurant employee. Right audio: received Rumik.

[Full conversation recording](conversation.mp3)

## Turn timestamps

Times below use the browser audio clock. Each row is an employee playback item, not a human-annotated semantic turn. First speech is estimated from 20 ms audio windows. First token is the arrival of Rumik's first text packet (`bot-llm-text`) at the browser after that speech ended; it includes network transit and is an upper bound on hosted generation latency.

| Turn | Employee speech end (s) | First Rumik token (s) | TTFT (ms) | First Rumik speech (s) | TTFS (ms) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 9.527 | 11.563 | 2036.000 | 12.163 | 2636.000 | answered |
| 2 | 46.547 | 47.739 | 1192.000 | 48.463 | 1916.000 | answered |
| 3 | 63.607 | 66.032 | 2425.333 | 66.763 | 3156.000 | answered |
| 4 | 94.147 | 95.632 | 1485.333 | 96.363 | 2216.000 | answered |

## Evaluation stages

| Stage | Status |
| --- | --- |
| jev | completed |
| openai | completed |
| rules | completed |

## Metrics

| Metric | Result | Explanation |
| --- | --- | --- |
| counterpart_actions | met | Found 0 forbidden counterpart action attempts. |
| task_delivery | met | The authenticated before-call response served the user's task to Rumik. This does not prove that the hosted agent used it correctly. |
| policy_actions | met | Found 0 forbidden action attempts. |
| duplicate_effects | met | Checked committed operation identities. |
| task_state | met | Checked the declared booking or no-booking outcome and material terms; name identity and spoken authorization are separate checks. |
| booking_identity | uncertain | Exact normalized names match; different spelling or script needs semantic review, not an automatic wrong-person verdict. |
| reservation_history | met | Replayed booking identity, terms, action ownership, reference and structural speech anchors. These do not prove semantic agreement. |
| user_report_references | met | Compared only explicitly labelled target report references using explicit-reference-clauses-v2. Distinct codes remain distinct. A match checks identifiers only, not overall report accuracy; unsupported prose requires review. |
| user_report_presence | met | Checked authenticated report receipt. Confirmed absence is separate from false content; a missing report does not establish which actor caused an interrupted call. |
| consent_alignment | met | The caller clearly requested confirmation of the stated reservation terms before the employee recorded it. The material terms remained unchanged. |
| constraint_behavior | not_met | The initial request communicated the required branch, time, party size, seating, name, and zero reservation charges. However, the target later produced a conflicting readback identifying the name as Courtney and leaving the time as AM/PM, rather than consistently preserving the assigned terms. |
| context_retention | not_met | The target initially retained and stated the user's core requirements, but the later target readback substituted Courtney for Aditi Shah and introduced AM/PM ambiguity. That is inconsistent with retaining the already established booking identity and time. |
| conversation_progress | met | The exchange progressed from the request, to availability and terms, to confirmation, recording, reference delivery, and closure. The target did not create an observable agreement loop or stall. |
| counterpart_validity | not_met | The employee used the supplied availability, offer, and recording tools and stated the reservation terms truthfully. However, the spoken reference was not delivered as the single issued reference SIM-097939: it was rendered as “सिम्स” and later involved a correction/readback that did not clearly preserve the issued grouping. This is a counterpart reference-delivery failure, not a target tool-action failure. |
| hinglish_quality | uncertain | This rubric requires human listening for understandability and naturalness. The supplied transcription alone cannot establish the required acoustic judgment. |
| question_relevance | met | The target's request and confirmation concern the assigned reservation. Its later reference-related statement is also part of closing and verification rather than an unrelated question. |
| target_output_integrity | uncertain | The transcript contains an anomalous target readback, but this rubric requires verifying suspected leakage or internal speech against the captured audio through human listening. Textual transcription alone is insufficient. |
| target_role_fidelity | met | The target acted as the customer's representative: it stated the reservation request, confirmed the booking under the requested name, and participated in reference closure. There was a substantive task exchange. |
| user_report_accuracy | met | The authenticated report states the booked date, time, party size, indoor regular seating, Aundh branch, restaurant, booking name, no charge, and the issued reference. The report's SIM-09-7939 formatting preserves the same issued reference digits as SIM-097939 under the supplied normalization. |

## Private report

Reservation confirmed for 2 Oct 2026 at 7:30 pm for 3 people, indoor regular table, Aundh branch Neem Courtyard, under Aditi Shah, no charge, reference SIM-09-7939.

## Business outcome

```json
[
  {
    "booking_kind": "table_only",
    "booking_name": "अदीति शाह",
    "branch": "Aundh",
    "cancellation_fee_inr": 0,
    "consent_evidence": {
      "audio_artifacts": [
        "audio/played.wav",
        "audio/received.wav"
      ],
      "event_sequences": [
        4022,
        5865,
        6113,
        6573
      ],
      "observation_boundary": "browser_render_and_received_audio",
      "observed_through_sequence": 6687,
      "readback_item_id": "item_EQgQOK9PLbG5cSix5sZ9o",
      "semantic_confirmation": "requires_human_review"
    },
    "date": "2026-10-02",
    "deposit_inr": 0,
    "inclusions": [
      "One indoor table for the whole party; meals chosen and paid for separately at the visit."
    ],
    "mandatory_extras": [],
    "menu": null,
    "offer_id": "offer-call_GYehVPb0oM6h4ECB",
    "operation_id": "call_hncAdAw8eeDLzFBm",
    "option_id": "01-aundh-1930",
    "party_size": 3,
    "pricing": {
      "currency": "INR",
      "meal_payment": "Meals are ordered and paid for separately at the visit. Their bill is not known yet; zero reservation charge does not mean free food.",
      "meal_total_inr": null,
      "reservation_charge_inr": 0,
      "total_scope": "reservation_only"
    },
    "reference": "SIM-097939",
    "remaining_due_inr": 0,
    "seating": "indoor_regular_table",
    "table_capacity": 3,
    "table_count": 1,
    "time": "19:30",
    "timezone": "Asia/Kolkata",
    "total_inr": 0,
    "without_onion_garlic_capacity": 0,
    "without_onion_garlic_guests": 0
  }
]
```

## Silence and response timing

```json
{
  "activity_is_not_semantic_turns": true,
  "algorithm": "rms-20ms-merge300ms-v2",
  "boundary": "browser_render_and_capture",
  "clock_id": "chromium-audio-context",
  "coverage_seconds": [
    1.5626666666666666,
    99.18266666666666
  ],
  "long_silence_intervals": [],
  "long_silence_threshold_seconds": 10,
  "replies": {
    "counterpart": {
      "no_response_intervals": [
        {
          "after_seconds": 15.122666666666667,
          "gap_ms": 360.0
        },
        {
          "after_seconds": 17.062666666666665,
          "gap_ms": 440.0
        },
        {
          "after_seconds": 19.442666666666668,
          "gap_ms": 520.0
        },
        {
          "after_seconds": 23.042666666666666,
          "gap_ms": 420.0
        },
        {
          "after_seconds": 24.982666666666667,
          "gap_ms": 420.0
        },
        {
          "after_seconds": 26.502666666666666,
          "gap_ms": 340.0
        },
        {
          "after_seconds": 48.782666666666664,
          "gap_ms": 300.0
        },
        {
          "after_seconds": 68.04266666666666,
          "gap_ms": 400.0
        },
        {
          "after_seconds": 70.62266666666666,
          "gap_ms": 420.0
        },
        {
          "after_seconds": 72.66266666666667,
          "gap_ms": 640.0
        },
        {
          "after_seconds": 74.02266666666667,
          "gap_ms": 340.0
        },
        {
          "after_seconds": 75.50266666666667,
          "gap_ms": 560.0
        },
        {
          "after_seconds": 78.26266666666666,
          "gap_ms": 600.0
        },
        {
          "after_seconds": 79.46266666666666,
          "gap_ms": 580.0
        },
        {
          "after_seconds": 83.00266666666667,
          "gap_ms": 800.0
        },
        {
          "after_seconds": 98.04266666666666,
          "gap_ms": 1140.0
        }
      ],
      "response_gaps": [
        {
          "after_seconds": 2.8626666666666667,
          "gap_ms": 1884.0
        },
        {
          "after_seconds": 27.502666666666666,
          "gap_ms": 4684.0
        },
        {
          "after_seconds": 52.36266666666667,
          "gap_ms": 2964.0
        },
        {
          "after_seconds": 84.42266666666667,
          "gap_ms": 1984.0
        }
      ]
    },
    "target": {
      "no_response_intervals": [
        {
          "after_seconds": 5.246666666666667,
          "gap_ms": 460.0
        },
        {
          "after_seconds": 7.306666666666667,
          "gap_ms": 500.0
        },
        {
          "after_seconds": 36.68666666666667,
          "gap_ms": 400.0
        },
        {
          "after_seconds": 39.446666666666665,
          "gap_ms": 360.0
        },
        {
          "after_seconds": 41.526666666666664,
          "gap_ms": 480.0
        },
        {
          "after_seconds": 44.026666666666664,
          "gap_ms": 600.0
        },
        {
          "after_seconds": 57.946666666666665,
          "gap_ms": 520.0
        },
        {
          "after_seconds": 61.68666666666667,
          "gap_ms": 460.0
        },
        {
          "after_seconds": 87.50666666666666,
          "gap_ms": 440.0
        },
        {
          "after_seconds": 91.14666666666666,
          "gap_ms": 340.0
        },
        {
          "after_seconds": 93.18666666666667,
          "gap_ms": 320.0
        }
      ],
      "response_gaps": [
        {
          "after_seconds": 9.526666666666667,
          "gap_ms": 2636.0
        },
        {
          "after_seconds": 46.54666666666667,
          "gap_ms": 1916.0
        },
        {
          "after_seconds": 63.60666666666667,
          "gap_ms": 3156.0
        },
        {
          "after_seconds": 94.14666666666666,
          "gap_ms": 2216.0
        }
      ]
    }
  },
  "rms_threshold": 500,
  "speaker_activity": {
    "counterpart": [
      [
        4.746666666666667,
        5.246666666666667
      ],
      [
        5.706666666666667,
        7.306666666666667
      ],
      [
        7.806666666666667,
        9.526666666666667
      ],
      [
        32.18666666666667,
        36.68666666666667
      ],
      [
        37.086666666666666,
        39.446666666666665
      ],
      [
        39.806666666666665,
        41.526666666666664
      ],
      [
        42.00666666666667,
        44.026666666666664
      ],
      [
        44.626666666666665,
        46.54666666666667
      ],
      [
        55.32666666666667,
        57.946666666666665
      ],
      [
        58.46666666666667,
        61.68666666666667
      ],
      [
        62.14666666666667,
        63.60666666666667
      ],
      [
        86.40666666666667,
        87.50666666666666
      ],
      [
        87.94666666666667,
        91.14666666666666
      ],
      [
        91.48666666666666,
        93.18666666666667
      ],
      [
        93.50666666666666,
        94.14666666666666
      ]
    ],
    "target": [
      [
        2.1226666666666665,
        2.8626666666666667
      ],
      [
        12.162666666666667,
        15.122666666666667
      ],
      [
        15.482666666666667,
        17.062666666666665
      ],
      [
        17.502666666666666,
        19.442666666666668
      ],
      [
        19.962666666666667,
        23.042666666666666
      ],
      [
        23.462666666666667,
        24.982666666666667
      ],
      [
        25.402666666666665,
        26.502666666666666
      ],
      [
        26.842666666666666,
        27.502666666666666
      ],
      [
        48.462666666666664,
        48.782666666666664
      ],
      [
        49.08266666666667,
        52.36266666666667
      ],
      [
        66.76266666666666,
        68.04266666666666
      ],
      [
        68.44266666666667,
        70.62266666666666
      ],
      [
        71.04266666666666,
        72.66266666666667
      ],
      [
        73.30266666666667,
        74.02266666666667
      ],
      [
        74.36266666666667,
        75.50266666666667
      ],
      [
        76.06266666666667,
        78.26266666666666
      ],
      [
        78.86266666666667,
        79.46266666666666
      ],
      [
        80.04266666666666,
        83.00266666666667
      ],
      [
        83.80266666666667,
        84.42266666666667
      ],
      [
        96.36266666666667,
        98.04266666666666
      ]
    ]
  },
  "status": "measured"
}
```

## Employee speech delivery

Local playback completeness is checked separately from task success. Interruptions still need conversation review; local playback does not prove remote hearing.

```json
{
  "boundary": "Local playback only; target interruptions still need semantic review.",
  "continuity": {
    "attribution": "unknown",
    "boundary": "Gaps between rendered samples of one generated item; embedded silence is excluded. Source starvation and local scheduling are not distinguished.",
    "clock_id": "chromium-audio-context",
    "items": [
      {
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "item_id": "item_EQgPw9U99p7WOioJXv3at",
        "largest_gap_ms": 0.0
      },
      {
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "item_id": "item_EQgQOK9PLbG5cSix5sZ9o",
        "largest_gap_ms": 0.0
      },
      {
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "item_id": "item_EQgQlty7xGJOht7wAyvDU",
        "largest_gap_ms": 0.0
      },
      {
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "item_id": "item_EQgRGY74pUD1MItC83nqC",
        "largest_gap_ms": 0.0
      }
    ],
    "max_bridge_delivery_delay_ms": 78.69999998807907,
    "status": "measured"
  },
  "incomplete_responses": [],
  "status": "passed",
  "target_interruptions": [],
  "unexplained_cutoffs": []
}
```

## Independent Jev assessment

```json
{
  "consent_alignment": {
    "choice": "met",
    "confidence": 0.67,
    "probabilities": {
      "met": 0.75,
      "not_applicable": 0.01,
      "not_met": 0.11,
      "uncertain": 0.13
    },
    "type": "choice"
  },
  "constraint_behavior": {
    "choice": "met",
    "confidence": 0.27,
    "probabilities": {
      "met": 0.51,
      "not_met": 0.29,
      "uncertain": 0.2
    },
    "type": "choice"
  },
  "context_retention": {
    "choice": "met",
    "confidence": 0.33,
    "probabilities": {
      "met": 0.56,
      "not_met": 0.22,
      "uncertain": 0.22
    },
    "type": "choice"
  },
  "conversation_progress": {
    "choice": "met",
    "confidence": 0.33,
    "probabilities": {
      "met": 0.55,
      "not_met": 0.27,
      "uncertain": 0.18
    },
    "type": "choice"
  },
  "counterpart_validity": {
    "choice": "met",
    "confidence": 0.3,
    "probabilities": {
      "met": 0.53,
      "not_met": 0.26,
      "uncertain": 0.21
    },
    "type": "choice"
  },
  "question_relevance": {
    "choice": "met",
    "confidence": 0.28,
    "probabilities": {
      "met": 0.51,
      "not_met": 0.26,
      "uncertain": 0.23
    },
    "type": "choice"
  },
  "target_role_fidelity": {
    "choice": "met",
    "confidence": 0.26,
    "probabilities": {
      "met": 0.51,
      "not_met": 0.29,
      "uncertain": 0.2
    },
    "type": "choice"
  },
  "user_report_accuracy": {
    "choice": "met",
    "confidence": 0.6,
    "probabilities": {
      "met": 0.7,
      "not_applicable": 0.01,
      "not_met": 0.18,
      "uncertain": 0.11
    },
    "type": "choice"
  }
}
```

Jev is an independent comparison and cannot override verified business records.
All attempts and incomplete stages remain in the batch counts.