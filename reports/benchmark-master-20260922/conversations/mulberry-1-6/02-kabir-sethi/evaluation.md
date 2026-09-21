# Conversation and benchmark result

Automated outcome: **passed**. Simulation validity: **valid**.

Full evaluation: **completed**. Conversation repair accepted: **False**.

Human listening is pending. Text judges cannot establish acoustic naturalness or prove that suspected self-talk was audible.

Please reserve one indoor table for five at Copper Leaf on October 3, 2026 at 8 p.m., under Kabir Sethi. Try Indiranagar first; Domlur is fine if Indiranagar has no table then. Keep the time and date. Make a free table reservation only, with no deposit or cancellation fee, and send me the details and reference if booked. Speak naturally in Hinglish.

[Independent transcript](transcript.md) · [All metrics and raw judge answers](details.json) · [Failure evidence and uncertainty](diagnostics-v1.json) · [Timing, WER and endpointing availability](measurements-v2.json) · [Per-turn timestamps](turn-timestamps.csv)

Observed task completion: **unresolved**. Established failure owner: **unknown**. Missing required outputs remain visible even when their cause is unknown.

Left audio: restaurant employee. Right audio: received Rumik.

[Full conversation recording](conversation.mp3)

## Turn timestamps

Times below use the browser audio clock. Each row is an employee playback item, not a human-annotated semantic turn. First speech is estimated from 20 ms audio windows. First token is the arrival of Rumik's first text packet (`bot-llm-text`) at the browser after that speech ended; it includes network transit and is an upper bound on hosted generation latency.

| Turn | Employee speech end (s) | First Rumik token (s) | TTFT (ms) | First Rumik speech (s) | TTFS (ms) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 8.501 | 9.605 | 1104.000 | 10.673 | 2172.000 | answered |
| 2 | 34.621 | 35.781 | 1160.000 | 36.973 | 2352.000 | answered |
| 3 | 59.401 | 60.635 | 1233.333 | 61.733 | 2332.000 | answered |
| 4 | 92.121 | 95.205 | 3084.000 | 96.213 | 4092.000 | answered |
| 5 | 116.341 | 117.440 | 1098.667 | 118.593 | 2252.000 | answered |

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
| booking_identity | met | Exact normalized names match; different spelling or script needs semantic review, not an automatic wrong-person verdict. |
| reservation_history | met | Replayed booking identity, terms, action ownership, reference and structural speech anchors. These do not prove semantic agreement. |
| user_report_references | met | Compared only explicitly labelled target report references using explicit-reference-clauses-v2. Distinct codes remain distinct. A match checks identifiers only, not overall report accuracy; unsupported prose requires review. |
| user_report_presence | met | Checked authenticated report receipt. Confirmed absence is separate from false content; a missing report does not establish which actor caused an interrupted call. |
| consent_alignment | met | The target explicitly requested booking the Domlur option after the employee described the date, time, party size, indoor table, and meal-payment arrangement. The request also clearly required no deposit or charges. |
| constraint_behavior | met | The target requested and accepted the authorized fallback branch Domlur while preserving the date, 20:00 time, party size of five, indoor regular table, table-only arrangement, and zero reservation charges. No payment, deposit, fee, meal purchase, or extra was authorized. |
| context_retention | met | The target retained the original party size, seating, date, and time, asked for the permitted Domlur fallback after Indiranagar was unavailable, and then gave a booking request without unnecessarily re-asking settled details. |
| conversation_progress | met | The exchange progressed from the initial request, to checking the preferred branch, to checking the authorized fallback, to booking and reporting the result. There is no unjustified repeated agreement or question loop attributable to the target. |
| counterpart_validity | met | The employee checked Indiranagar and correctly reported no matching table, checked Domlur, described the available authorized option and its meal-payment condition, and recorded the reservation only after the target's explicit booking request. The confirmed reservation and reference match the business result; the employee did not claim unsupported concessions or a nonexistent booking. |
| hinglish_quality | uncertain | This rubric requires human listening for understandability and naturalness. The supplied transcription alone cannot establish audio quality or natural delivery. |
| question_relevance | met | The target asked for the preferred-branch availability, answered the employee's fallback-branch question, and then made the booking request. These questions and answers directly advanced the reservation task. |
| target_output_integrity | uncertain | The transcript shows task-directed customer speech and no obvious internal instructions, but this diagnostic requires human listening to verify the audible output and cannot be resolved from text alone. |
| target_role_fidelity | met | The target consistently acted as the customer's representative: it stated the reservation request, selected the authorized fallback branch, and requested booking. It did not offer restaurant services or impersonate the employee. |
| user_report_accuracy | met | The delivered report accurately states one booking at Domlur for five people on 3 October 2026 at 8 pm under Kabir Sethi, with an indoor regular table and no reservation charges. It preserves the issued reference SIM-401933 and matches the committed booking record. |

## Private report

Booked indoor regular table for five at Domlur on 3 October 2026 at 8 pm under Kabir Sethi, no charges, reference SIM-401933.

## Business outcome

```json
[
  {
    "booking_kind": "table_only",
    "booking_name": "Kabir Sethi",
    "branch": "Domlur",
    "cancellation_fee_inr": 0,
    "consent_evidence": {
      "audio_artifacts": [
        "audio/played.wav",
        "audio/received.wav"
      ],
      "event_sequences": [
        5844,
        7432,
        7710,
        9601
      ],
      "observation_boundary": "browser_render_and_received_audio",
      "observed_through_sequence": 9725,
      "readback_item_id": "item_EQgcMf5rUOLQugfZy0Ocv",
      "semantic_confirmation": "requires_human_review"
    },
    "date": "2026-10-03",
    "deposit_inr": 0,
    "inclusions": [
      "One indoor table for the whole party; meals chosen and paid for separately at the visit."
    ],
    "mandatory_extras": [],
    "menu": null,
    "offer_id": "offer-call_IG6amNKBpoWdkgxX",
    "operation_id": "call_duTKzI6LnyM15zNX",
    "option_id": "02-domlur-2000",
    "party_size": 5,
    "pricing": {
      "currency": "INR",
      "meal_payment": "Meals are ordered and paid for separately at the visit. Their bill is not known yet; zero reservation charge does not mean free food.",
      "meal_total_inr": null,
      "reservation_charge_inr": 0,
      "total_scope": "reservation_only"
    },
    "reference": "SIM-401933",
    "remaining_due_inr": 0,
    "seating": "indoor_regular_table",
    "table_capacity": 5,
    "table_count": 1,
    "time": "20:00",
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
    2.2133333333333334,
    121.312
  ],
  "long_silence_intervals": [
    {
      "attribution": "unknown",
      "duration_seconds": 10.388000000000005,
      "end_seconds": 82.94133333333333,
      "start_seconds": 72.55333333333333
    }
  ],
  "long_silence_threshold_seconds": 10,
  "replies": {
    "counterpart": {
      "no_response_intervals": [
        {
          "after_seconds": 18.233333333333334,
          "gap_ms": 400.0
        },
        {
          "after_seconds": 20.833333333333332,
          "gap_ms": 460.0
        },
        {
          "after_seconds": 37.233333333333334,
          "gap_ms": 320.0
        },
        {
          "after_seconds": 66.03333333333333,
          "gap_ms": 420.0
        },
        {
          "after_seconds": 70.55333333333333,
          "gap_ms": 400.0
        },
        {
          "after_seconds": 101.97333333333333,
          "gap_ms": 420.0
        },
        {
          "after_seconds": 120.43333333333334,
          "gap_ms": 878.667
        }
      ],
      "response_gaps": [
        {
          "after_seconds": 4.113333333333333,
          "gap_ms": 1808.0
        },
        {
          "after_seconds": 23.293333333333333,
          "gap_ms": 3028.0
        },
        {
          "after_seconds": 40.81333333333333,
          "gap_ms": 6488.0
        },
        {
          "after_seconds": 72.55333333333333,
          "gap_ms": 10388.0
        },
        {
          "after_seconds": 102.83333333333333,
          "gap_ms": 2028.0
        }
      ]
    },
    "target": {
      "no_response_intervals": [
        {
          "after_seconds": 6.421333333333333,
          "gap_ms": 520.0
        },
        {
          "after_seconds": 30.221333333333334,
          "gap_ms": 620.0
        },
        {
          "after_seconds": 32.88133333333333,
          "gap_ms": 380.0
        },
        {
          "after_seconds": 48.221333333333334,
          "gap_ms": 320.0
        },
        {
          "after_seconds": 50.38133333333333,
          "gap_ms": 320.0
        },
        {
          "after_seconds": 51.641333333333336,
          "gap_ms": 340.0
        },
        {
          "after_seconds": 54.52133333333333,
          "gap_ms": 480.0
        },
        {
          "after_seconds": 57.58133333333333,
          "gap_ms": 680.0
        },
        {
          "after_seconds": 84.46133333333333,
          "gap_ms": 560.0
        },
        {
          "after_seconds": 85.90133333333333,
          "gap_ms": 320.0
        },
        {
          "after_seconds": 88.20133333333334,
          "gap_ms": 680.0
        },
        {
          "after_seconds": 90.02133333333333,
          "gap_ms": 740.0
        },
        {
          "after_seconds": 105.32133333333333,
          "gap_ms": 420.0
        },
        {
          "after_seconds": 108.56133333333334,
          "gap_ms": 480.0
        },
        {
          "after_seconds": 110.76133333333334,
          "gap_ms": 860.0
        },
        {
          "after_seconds": 112.36133333333333,
          "gap_ms": 320.0
        },
        {
          "after_seconds": 114.68133333333333,
          "gap_ms": 780.0
        }
      ],
      "response_gaps": [
        {
          "after_seconds": 8.501333333333333,
          "gap_ms": 2172.0
        },
        {
          "after_seconds": 34.62133333333333,
          "gap_ms": 2352.0
        },
        {
          "after_seconds": 59.40133333333333,
          "gap_ms": 2332.0
        },
        {
          "after_seconds": 92.12133333333334,
          "gap_ms": 4092.0
        },
        {
          "after_seconds": 116.34133333333334,
          "gap_ms": 2252.0
        }
      ]
    }
  },
  "rms_threshold": 500,
  "speaker_activity": {
    "counterpart": [
      [
        5.921333333333333,
        6.421333333333333
      ],
      [
        6.941333333333334,
        8.501333333333333
      ],
      [
        26.32133333333333,
        30.221333333333334
      ],
      [
        30.841333333333335,
        32.88133333333333
      ],
      [
        33.26133333333333,
        34.62133333333333
      ],
      [
        47.30133333333333,
        48.221333333333334
      ],
      [
        48.541333333333334,
        50.38133333333333
      ],
      [
        50.70133333333333,
        51.641333333333336
      ],
      [
        51.98133333333333,
        54.52133333333333
      ],
      [
        55.001333333333335,
        57.58133333333333
      ],
      [
        58.26133333333333,
        59.40133333333333
      ],
      [
        82.94133333333333,
        84.46133333333333
      ],
      [
        85.02133333333333,
        85.90133333333333
      ],
      [
        86.22133333333333,
        88.20133333333334
      ],
      [
        88.88133333333333,
        90.02133333333333
      ],
      [
        90.76133333333334,
        92.12133333333334
      ],
      [
        104.86133333333333,
        105.32133333333333
      ],
      [
        105.74133333333333,
        108.56133333333334
      ],
      [
        109.04133333333333,
        110.76133333333334
      ],
      [
        111.62133333333334,
        112.36133333333333
      ],
      [
        112.68133333333333,
        114.68133333333333
      ],
      [
        115.46133333333333,
        116.34133333333334
      ]
    ],
    "target": [
      [
        3.6333333333333333,
        4.113333333333333
      ],
      [
        10.673333333333334,
        18.233333333333334
      ],
      [
        18.633333333333333,
        20.833333333333332
      ],
      [
        21.293333333333333,
        23.293333333333333
      ],
      [
        36.973333333333336,
        37.233333333333334
      ],
      [
        37.553333333333335,
        40.81333333333333
      ],
      [
        61.733333333333334,
        66.03333333333333
      ],
      [
        66.45333333333333,
        70.55333333333333
      ],
      [
        70.95333333333333,
        72.55333333333333
      ],
      [
        96.21333333333334,
        101.97333333333333
      ],
      [
        102.39333333333333,
        102.83333333333333
      ],
      [
        118.59333333333333,
        120.43333333333334
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
        "item_id": "item_EQgbg9ZaqI0SO6sStjPiR",
        "largest_gap_ms": 0.0
      },
      {
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "item_id": "item_EQgc1xDKm1xz25WkC0dDm",
        "largest_gap_ms": 0.0
      },
      {
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "item_id": "item_EQgcMf5rUOLQugfZy0Ocv",
        "largest_gap_ms": 0.0
      },
      {
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "item_id": "item_EQgcvjxWyaJpEUrnLsvfg",
        "largest_gap_ms": 0.0
      },
      {
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "item_id": "item_EQgdHcCsGySBMuk8iTZIp",
        "largest_gap_ms": 0.0
      }
    ],
    "max_bridge_delivery_delay_ms": 1183.300000011921,
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
      "not_met": 0.14,
      "uncertain": 0.1
    },
    "type": "choice"
  },
  "constraint_behavior": {
    "choice": "met",
    "confidence": 0.22,
    "probabilities": {
      "met": 0.48,
      "not_met": 0.35,
      "uncertain": 0.17
    },
    "type": "choice"
  },
  "context_retention": {
    "choice": "met",
    "confidence": 0.28,
    "probabilities": {
      "met": 0.52,
      "not_met": 0.27,
      "uncertain": 0.21
    },
    "type": "choice"
  },
  "conversation_progress": {
    "choice": "met",
    "confidence": 0.34,
    "probabilities": {
      "met": 0.56,
      "not_met": 0.29,
      "uncertain": 0.15
    },
    "type": "choice"
  },
  "counterpart_validity": {
    "choice": "met",
    "confidence": 0.25,
    "probabilities": {
      "met": 0.5,
      "not_met": 0.31,
      "uncertain": 0.19
    },
    "type": "choice"
  },
  "question_relevance": {
    "choice": "met",
    "confidence": 0.23,
    "probabilities": {
      "met": 0.49,
      "not_met": 0.31,
      "uncertain": 0.2
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
    "confidence": 0.62,
    "probabilities": {
      "met": 0.72,
      "not_applicable": 0.01,
      "not_met": 0.18,
      "uncertain": 0.09
    },
    "type": "choice"
  }
}
```

Jev is an independent comparison and cannot override verified business records.
All attempts and incomplete stages remain in the batch counts.