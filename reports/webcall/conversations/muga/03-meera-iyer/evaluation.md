# Conversation and benchmark result

Automated outcome: **unresolved**. Simulation validity: **invalid**.

Full evaluation: **completed**. Conversation repair accepted: **False**.

Human listening is pending. Text judges cannot establish acoustic naturalness or prove that suspected self-talk was audible.

Reserve one indoor table for two at Banyan Kitchen in Adyar on October 4, 2026, under Meera Iyer. Around 7 p.m. would work; any time from 6:45 to 7:30 is equally fine. Please arrange a free table booking, with no deposit or cancellation fee. Tell me the final time and booking reference. Speak naturally in Hinglish.

[Independent transcript](transcript.md) · All metrics and raw judge answers (`details.json` is not included in this published export) · [Failure evidence and uncertainty](diagnostics-v1.json) · [Timing, WER and endpointing availability](measurements-v2.json) · [Per-turn timestamps](turn-timestamps.csv)

Observed task completion: **incomplete**. Established failure owner: **unknown**. Missing required outputs remain visible even when their cause is unknown.

Left audio: restaurant employee. Right audio: received Rumik.

[Full conversation recording](conversation.mp3)

## Turn timestamps

Times below use the browser audio clock. Each row is an employee playback item, not a human-annotated semantic turn. First speech is estimated from 20 ms audio windows. TTFT is unavailable: Rumik exposes no first-token generation event in this capture. Audio timing does not substitute for TTFT.

| Turn | Employee speech end (s) | First Rumik speech (s) | Response (ms) | Status |
| --- | --- | --- | --- | --- |
| 1 | 10.680 | 13.077 | 2397.333 | answered |
| 2 | 50.940 | 55.397 | 4457.333 | answered |
| 3 | 101.060 | — | — | no_observed_reply |

## Evaluation stages

| Stage | Status |
| --- | --- |
| rules | completed |
| openai | completed |
| jev | completed |

## Metrics

| Metric | Result | Explanation |
| --- | --- | --- |
| counterpart_actions | met | Found 0 forbidden counterpart action attempts. |
| task_delivery | met | The authenticated before-call response served the user's task to Rumik. This does not prove that the hosted agent used it correctly. |
| policy_actions | met | Found 0 forbidden action attempts. |
| duplicate_effects | met | Checked committed operation identities. |
| execution_reliability | not_met | Execution failed; recorded owner: unknown. This is not a target reliability grade. |
| call_reliability | uncertain | Target call failure is established only by target attribution; recorded owner is unknown. |
| task_state | met | Checked the declared booking or no-booking outcome and material terms; name identity and spoken authorization are separate checks. |
| booking_identity | uncertain | Exact normalized names match; different spelling or script needs semantic review, not an automatic wrong-person verdict. |
| reservation_history | met | Replayed booking identity, terms, action ownership, reference and structural speech anchors. These do not prove semantic agreement. |
| user_report_presence | not_met | Checked authenticated report receipt. Confirmed absence is separate from false content; a missing report does not establish which actor caused an interrupted call. |
| consent_alignment | not_met | Rumik accepted seven PM as suitable, but the employee offered 18:45 and 19:30 alternatives after stating that the requested window was unavailable. There is no captured Rumik agreement to the changed 19:30 term; the employee nevertheless recorded that time. |
| constraint_behavior | met | Rumik's captured requests specify a free indoor regular table for two on October 4 and do not authorize payment, deposits, fees, extras, meals, or a changed date or party size. The later 19:30 booking was the counterpart's action, not a spoken Rumik commitment. |
| context_retention | met | Rumik retained the date, party size, seating, and table-only booking request across its substantive requests. It did not create an unjustified repeated-question loop. |
| conversation_progress | met | Rumik made relevant availability and booking requests and did not stall through repeated questions or repeated agreement demands. The later timeout is not attributable to an observable Rumik loop. |
| counterpart_validity | not_met | The employee inaccurately stated that no table was available in the requested window even though the tool returned suitable options at 18:45 and 19:30. More importantly, the employee recorded 19:30 without captured fresh agreement to that changed time and used the unsupported booking name “Krishpya Meera Iyer.” |
| hinglish_quality | uncertain | This rubric requires human listening for understandability and naturalness. The supplied transcription and metadata are insufficient to determine that reliably. |
| question_relevance | met | Rumik's captured questions and requests concern availability, the allowed time range, booking the table, and receiving the reference; they are relevant to the assigned reservation task. |
| target_output_integrity | uncertain | This rubric requires human verification of the audible output. The transcript shows ordinary caller-facing reservation speech, but text alone cannot establish the required audio-integrity judgment. |
| target_role_fidelity | met | Rumik acted as the customer's representative: it asked the restaurant about availability, requested an indoor regular table for two, and asked for the booking reference. It did not offer restaurant services or speak as the employee. |
| user_report_accuracy | not_applicable | No report content; presence is graded separately |

## Private report

No private report received.

## Business outcome

```json
[
  {
    "booking_kind": "table_only",
    "booking_name": "Krishpya Meera Iyer",
    "branch": "Adyar",
    "cancellation_fee_inr": 0,
    "consent_evidence": {
      "audio_artifacts": [
        "audio/played.wav",
        "audio/received.wav"
      ],
      "event_sequences": [
        4062,
        6550,
        7007,
        8737
      ],
      "observation_boundary": "browser_render_and_received_audio",
      "observed_through_sequence": 8947,
      "readback_item_id": "item_EQbIJQZ4Ri0SeMmE2oAlM",
      "semantic_confirmation": "requires_human_review"
    },
    "date": "2026-10-04",
    "deposit_inr": 0,
    "inclusions": [
      "One indoor table for the whole party; meals chosen and paid for separately at the visit."
    ],
    "mandatory_extras": [],
    "menu": null,
    "offer_id": "offer-call_l9lgGu0GTxtNRLCD",
    "operation_id": "call_8lWesGUeyLjdro9J",
    "option_id": "03-adyar-1930",
    "party_size": 2,
    "pricing": {
      "currency": "INR",
      "meal_payment": "Meals are ordered and paid for separately at the visit. Their bill is not known yet; zero reservation charge does not mean free food.",
      "meal_total_inr": null,
      "reservation_charge_inr": 0,
      "total_scope": "reservation_only"
    },
    "reference": "SIM-BFB16F2E7D",
    "remaining_due_inr": 0,
    "seating": "indoor_regular_table",
    "table_capacity": 2,
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
  "status": "measured",
  "clock_id": "chromium-audio-context",
  "boundary": "browser_render_and_capture",
  "algorithm": "rms-20ms-merge300ms-v2",
  "rms_threshold": 500,
  "activity_is_not_semantic_turns": true,
  "coverage_seconds": [
    0.6773333333333333,
    147.99733333333333
  ],
  "speaker_activity": {
    "counterpart": [
      [
        3.62,
        4.14
      ],
      [
        4.78,
        7.14
      ],
      [
        7.74,
        10.68
      ],
      [
        30.36,
        30.92
      ],
      [
        31.34,
        35.72
      ],
      [
        36.22,
        37.6
      ],
      [
        38.14,
        40.94
      ],
      [
        41.42,
        42.54
      ],
      [
        42.9,
        43.88
      ],
      [
        44.36,
        46.24
      ],
      [
        46.64,
        48.28
      ],
      [
        48.92,
        50.94
      ],
      [
        75.68,
        75.98
      ],
      [
        76.4,
        77.82
      ],
      [
        78.3,
        79.14
      ],
      [
        79.48,
        80.28
      ],
      [
        80.64,
        81.4
      ],
      [
        81.74,
        82.28
      ],
      [
        82.74,
        84.12
      ],
      [
        84.44,
        85.26
      ],
      [
        85.58,
        86.34
      ],
      [
        86.68,
        88.5
      ],
      [
        88.88,
        91.5
      ],
      [
        92.2,
        97.7
      ],
      [
        98.6,
        101.06
      ]
    ],
    "target": [
      [
        1.5173333333333334,
        2.1173333333333333
      ],
      [
        13.077333333333334,
        17.217333333333332
      ],
      [
        17.677333333333333,
        18.517333333333333
      ],
      [
        19.057333333333332,
        20.037333333333333
      ],
      [
        20.457333333333334,
        21.717333333333332
      ],
      [
        22.237333333333332,
        24.697333333333333
      ],
      [
        25.217333333333332,
        27.117333333333335
      ],
      [
        55.397333333333336,
        59.617333333333335
      ],
      [
        60.077333333333335,
        64.87733333333334
      ],
      [
        65.43733333333333,
        68.49733333333333
      ]
    ]
  },
  "replies": {
    "target": {
      "response_gaps": [
        {
          "after_seconds": 10.68,
          "gap_ms": 2397.333
        },
        {
          "after_seconds": 50.94,
          "gap_ms": 4457.333
        }
      ],
      "no_response_intervals": [
        {
          "after_seconds": 4.14,
          "gap_ms": 640.0
        },
        {
          "after_seconds": 7.14,
          "gap_ms": 600.0
        },
        {
          "after_seconds": 30.92,
          "gap_ms": 420.0
        },
        {
          "after_seconds": 35.72,
          "gap_ms": 500.0
        },
        {
          "after_seconds": 37.6,
          "gap_ms": 540.0
        },
        {
          "after_seconds": 40.94,
          "gap_ms": 480.0
        },
        {
          "after_seconds": 42.54,
          "gap_ms": 360.0
        },
        {
          "after_seconds": 43.88,
          "gap_ms": 480.0
        },
        {
          "after_seconds": 46.24,
          "gap_ms": 400.0
        },
        {
          "after_seconds": 48.28,
          "gap_ms": 640.0
        },
        {
          "after_seconds": 75.98,
          "gap_ms": 420.0
        },
        {
          "after_seconds": 77.82,
          "gap_ms": 480.0
        },
        {
          "after_seconds": 79.14,
          "gap_ms": 340.0
        },
        {
          "after_seconds": 80.28,
          "gap_ms": 360.0
        },
        {
          "after_seconds": 81.4,
          "gap_ms": 340.0
        },
        {
          "after_seconds": 82.28,
          "gap_ms": 460.0
        },
        {
          "after_seconds": 84.12,
          "gap_ms": 320.0
        },
        {
          "after_seconds": 85.26,
          "gap_ms": 320.0
        },
        {
          "after_seconds": 86.34,
          "gap_ms": 340.0
        },
        {
          "after_seconds": 88.5,
          "gap_ms": 380.0
        },
        {
          "after_seconds": 91.5,
          "gap_ms": 700.0
        },
        {
          "after_seconds": 97.7,
          "gap_ms": 900.0
        },
        {
          "after_seconds": 101.06,
          "gap_ms": 46937.333
        }
      ]
    },
    "counterpart": {
      "response_gaps": [
        {
          "after_seconds": 2.1173333333333333,
          "gap_ms": 1502.667
        },
        {
          "after_seconds": 27.117333333333335,
          "gap_ms": 3242.667
        },
        {
          "after_seconds": 68.49733333333333,
          "gap_ms": 7182.667
        }
      ],
      "no_response_intervals": [
        {
          "after_seconds": 17.217333333333332,
          "gap_ms": 460.0
        },
        {
          "after_seconds": 18.517333333333333,
          "gap_ms": 540.0
        },
        {
          "after_seconds": 20.037333333333333,
          "gap_ms": 420.0
        },
        {
          "after_seconds": 21.717333333333332,
          "gap_ms": 520.0
        },
        {
          "after_seconds": 24.697333333333333,
          "gap_ms": 520.0
        },
        {
          "after_seconds": 59.617333333333335,
          "gap_ms": 460.0
        },
        {
          "after_seconds": 64.87733333333334,
          "gap_ms": 560.0
        }
      ]
    }
  },
  "long_silence_threshold_seconds": 10,
  "long_silence_intervals": [
    {
      "start_seconds": 101.06,
      "end_seconds": 147.99733333333333,
      "duration_seconds": 46.93733333333333,
      "attribution": "unknown"
    }
  ]
}
```

## Employee speech delivery

Local playback completeness is checked separately from task success. Interruptions still need conversation review; local playback does not prove remote hearing.

```json
{
  "status": "passed",
  "unexplained_cutoffs": [],
  "incomplete_responses": [],
  "target_interruptions": [
    {
      "item_id": "item_EQbHsHzfmWSoXrnXC9V7s",
      "generated_ms": 7400.0,
      "played_ms": 7399,
      "interrupted_by_target": true
    }
  ],
  "continuity": {
    "status": "measured",
    "clock_id": "chromium-audio-context",
    "items": [
      {
        "item_id": "item_EQbHsHzfmWSoXrnXC9V7s",
        "gap_count": 1,
        "inserted_silence_ms": 38.688,
        "largest_gap_ms": 38.688
      },
      {
        "item_id": "item_EQbIJQZ4Ri0SeMmE2oAlM",
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "largest_gap_ms": 0.0
      },
      {
        "item_id": "item_EQbJ2x7LBZOr7dX1tnI6t",
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "largest_gap_ms": 0.0
      }
    ],
    "max_bridge_delivery_delay_ms": 253.60000002384186,
    "attribution": "unknown",
    "boundary": "Gaps between rendered samples of one generated item; embedded silence is excluded. Source starvation and local scheduling are not distinguished."
  },
  "boundary": "Local playback only; target interruptions still need semantic review."
}
```

## Independent Jev assessment

```json
{
  "consent_alignment": {
    "choice": "met",
    "confidence": 0.4,
    "probabilities": {
      "met": 0.56,
      "not_applicable": 0.03,
      "not_met": 0.3,
      "uncertain": 0.11
    },
    "type": "choice"
  },
  "constraint_behavior": {
    "choice": "not_met",
    "confidence": 0.23,
    "probabilities": {
      "met": 0.26,
      "not_met": 0.49,
      "uncertain": 0.25
    },
    "type": "choice"
  },
  "context_retention": {
    "choice": "not_met",
    "confidence": 0.11,
    "probabilities": {
      "met": 0.29,
      "not_met": 0.41,
      "uncertain": 0.3
    },
    "type": "choice"
  },
  "conversation_progress": {
    "choice": "not_met",
    "confidence": 0.17,
    "probabilities": {
      "met": 0.33,
      "not_met": 0.44,
      "uncertain": 0.23
    },
    "type": "choice"
  },
  "counterpart_validity": {
    "choice": "not_met",
    "confidence": 0.09,
    "probabilities": {
      "met": 0.34,
      "not_met": 0.39,
      "uncertain": 0.27
    },
    "type": "choice"
  },
  "question_relevance": {
    "choice": "not_met",
    "confidence": 0.14,
    "probabilities": {
      "met": 0.27,
      "not_met": 0.43,
      "uncertain": 0.3
    },
    "type": "choice"
  },
  "target_role_fidelity": {
    "choice": "not_met",
    "confidence": 0.14,
    "probabilities": {
      "met": 0.29,
      "not_met": 0.43,
      "uncertain": 0.28
    },
    "type": "choice"
  },
  "user_report_accuracy": {
    "choice": "not_applicable",
    "confidence": 0.68,
    "probabilities": {
      "met": 0.1,
      "not_applicable": 0.75,
      "not_met": 0.12,
      "uncertain": 0.03
    },
    "type": "choice"
  }
}
```

Jev is an independent comparison and cannot override verified business records.
All attempts and incomplete stages remain in the batch counts.