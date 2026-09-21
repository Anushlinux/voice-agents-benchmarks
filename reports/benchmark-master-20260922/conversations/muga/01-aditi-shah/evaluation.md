# Conversation and benchmark result

Automated outcome: **unresolved**. Simulation validity: **invalid**.

Full evaluation: **completed**. Conversation repair accepted: **False**.

Human listening is pending. Text judges cannot establish acoustic naturalness or prove that suspected self-talk was audible.

Book an indoor table for three at Neem Courtyard in Aundh on October 2, 2026 at 7:30 p.m., under Aditi Shah. We want to sit together. Please make a table reservation only, with no booking charge, deposit or cancellation fee. Let me know the booking details and reference, or tell me if it cannot be arranged. Speak naturally in Hinglish.

[Independent transcript](transcript.md) · [All metrics and raw judge answers](details.json) · [Failure evidence and uncertainty](diagnostics-v1.json) · [Timing, WER and endpointing availability](measurements-v2.json) · [Per-turn timestamps](turn-timestamps.csv)

Observed task completion: **incomplete**. Established failure owner: **unknown**. Missing required outputs remain visible even when their cause is unknown.

Left audio: restaurant employee. Right audio: received Rumik.

[Full conversation recording](conversation.mp3)

## Turn timestamps

Times below use the browser audio clock. Each row is an employee playback item, not a human-annotated semantic turn. First speech is estimated from 20 ms audio windows. TTFT is unavailable: Rumik exposes no first-token generation event in this capture. Audio timing does not substitute for TTFT.

| Turn | Employee speech end (s) | First Rumik speech (s) | Response (ms) | Status |
| --- | --- | --- | --- | --- |
| 1 | 9.980 | 14.799 | 4818.667 | answered |
| 2 | 47.060 | 49.979 | 2918.667 | answered |
| 3 | 86.140 | 88.759 | 2618.667 | answered |

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
| booking_identity | met | Exact normalized names match; different spelling or script needs semantic review, not an automatic wrong-person verdict. |
| reservation_history | met | Replayed booking identity, terms, action ownership, reference and structural speech anchors. These do not prove semantic agreement. |
| user_report_presence | not_met | Checked authenticated report receipt. Confirmed absence is separate from false content; a missing report does not establish which actor caused an interrupted call. |
| consent_alignment | met | The target initially requested the specified table reservation without charge or deposit and then explicitly asked the employee to confirm the table and share the reference. The employee's disclosed terms remained unchanged, so fresh wording was not required. |
| constraint_behavior | met | The target communicated the required date, time, branch, party size, indoor table, booking name, table-only/no-charge terms, and no deposit. It did not authorize meals, deposits, fees, or other extras. |
| context_retention | met | The target stated the core booking requirements and subsequently asked for confirmation and the exact reference rather than re-asking settled requirements or introducing changed terms. |
| conversation_progress | met | The target made a relevant booking request, sought confirmation, and asked for the exact reference. The exchange progressed to a completed reservation rather than an observable repeated-question loop attributable to the target. |
| counterpart_validity | not_met | The employee announced that the booking was confirmed before the successful reservation tool result, and attempted to record it before fresh conversation evidence was accepted. The first recording attempt was rejected, so the premature confirmation was not truthful at that point. |
| hinglish_quality | uncertain | This rubric requires human listening for understandability and naturalness. The supplied transcription alone cannot establish the required audio-quality judgment. |
| question_relevance | met | The target's questions concerned availability, confirmation, and obtaining the exact reservation reference, all of which directly supported the assigned booking task. |
| target_output_integrity | uncertain | The transcript contains customer-facing booking speech and no clear internal instructions, but this diagnostic requires verification by human listening to the captured audio; text alone is insufficient. |
| target_role_fidelity | met | The target acted as the customer's assistant: it requested a reservation from the restaurant, stated the customer's constraints, sought confirmation, and requested the issued reference. It did not offer restaurant services. |
| user_report_accuracy | not_applicable | No report content; presence is graded separately |

## Private report

No private report received.

## Business outcome

```json
[
  {
    "booking_kind": "table_only",
    "booking_name": "Aditi Shah",
    "branch": "Aundh",
    "cancellation_fee_inr": 0,
    "consent_evidence": {
      "audio_artifacts": [
        "audio/played.wav",
        "audio/received.wav"
      ],
      "event_sequences": [
        3960,
        5810,
        6120,
        6752
      ],
      "observation_boundary": "browser_render_and_received_audio",
      "observed_through_sequence": 6854,
      "readback_item_id": "item_EQbLpXHmdayQcBOsZxxMt",
      "semantic_confirmation": "requires_human_review"
    },
    "date": "2026-10-02",
    "deposit_inr": 0,
    "inclusions": [
      "One indoor table for the whole party; meals chosen and paid for separately at the visit."
    ],
    "mandatory_extras": [],
    "menu": null,
    "offer_id": "offer-call_oZgcA0KmudXVBPcn",
    "operation_id": "call_uXOwj1GBnn0NBsPt",
    "option_id": "01-aundh-1930",
    "party_size": 3,
    "pricing": {
      "currency": "INR",
      "meal_payment": "Meals are ordered and paid for separately at the visit. Their bill is not known yet; zero reservation charge does not mean free food.",
      "meal_total_inr": null,
      "reservation_charge_inr": 0,
      "total_scope": "reservation_only"
    },
    "reference": "SIM-8DC273D126",
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
  "status": "measured",
  "clock_id": "chromium-audio-context",
  "boundary": "browser_render_and_capture",
  "algorithm": "rms-20ms-merge300ms-v2",
  "rms_threshold": 500,
  "activity_is_not_semantic_turns": true,
  "coverage_seconds": [
    1.0186666666666666,
    138.23866666666666
  ],
  "speaker_activity": {
    "counterpart": [
      [
        3.98,
        4.5
      ],
      [
        5.08,
        6.54
      ],
      [
        7.46,
        9.98
      ],
      [
        31.88,
        31.98
      ],
      [
        32.72,
        35.12
      ],
      [
        35.44,
        39.32
      ],
      [
        39.84,
        41.32
      ],
      [
        41.7,
        44.2
      ],
      [
        44.9,
        47.06
      ],
      [
        58.3,
        59.86
      ],
      [
        60.58,
        61.82
      ],
      [
        62.32,
        63.14
      ],
      [
        63.52,
        65.14
      ],
      [
        65.68,
        66.22
      ],
      [
        66.66,
        66.84
      ],
      [
        67.22,
        68.0
      ],
      [
        68.32,
        69.1
      ],
      [
        69.5,
        70.34
      ],
      [
        70.7,
        71.5
      ],
      [
        71.82,
        73.22
      ],
      [
        74.26,
        79.72
      ],
      [
        80.38,
        82.74
      ],
      [
        83.42,
        83.88
      ],
      [
        84.36,
        86.14
      ]
    ],
    "target": [
      [
        1.7586666666666666,
        2.2786666666666666
      ],
      [
        14.798666666666668,
        20.918666666666667
      ],
      [
        21.358666666666668,
        23.278666666666666
      ],
      [
        23.878666666666668,
        25.598666666666666
      ],
      [
        26.078666666666667,
        26.938666666666666
      ],
      [
        49.97866666666667,
        50.23866666666667
      ],
      [
        50.65866666666667,
        55.638666666666666
      ],
      [
        88.75866666666667,
        92.95866666666667
      ]
    ]
  },
  "replies": {
    "target": {
      "response_gaps": [
        {
          "after_seconds": 9.98,
          "gap_ms": 4818.667
        },
        {
          "after_seconds": 47.06,
          "gap_ms": 2918.667
        },
        {
          "after_seconds": 86.14,
          "gap_ms": 2618.667
        }
      ],
      "no_response_intervals": [
        {
          "after_seconds": 4.5,
          "gap_ms": 580.0
        },
        {
          "after_seconds": 6.54,
          "gap_ms": 920.0
        },
        {
          "after_seconds": 31.98,
          "gap_ms": 740.0
        },
        {
          "after_seconds": 35.12,
          "gap_ms": 320.0
        },
        {
          "after_seconds": 39.32,
          "gap_ms": 520.0
        },
        {
          "after_seconds": 41.32,
          "gap_ms": 380.0
        },
        {
          "after_seconds": 44.2,
          "gap_ms": 700.0
        },
        {
          "after_seconds": 59.86,
          "gap_ms": 720.0
        },
        {
          "after_seconds": 61.82,
          "gap_ms": 500.0
        },
        {
          "after_seconds": 63.14,
          "gap_ms": 380.0
        },
        {
          "after_seconds": 65.14,
          "gap_ms": 540.0
        },
        {
          "after_seconds": 66.22,
          "gap_ms": 440.0
        },
        {
          "after_seconds": 66.84,
          "gap_ms": 380.0
        },
        {
          "after_seconds": 68.0,
          "gap_ms": 320.0
        },
        {
          "after_seconds": 69.1,
          "gap_ms": 400.0
        },
        {
          "after_seconds": 70.34,
          "gap_ms": 360.0
        },
        {
          "after_seconds": 71.5,
          "gap_ms": 320.0
        },
        {
          "after_seconds": 73.22,
          "gap_ms": 1040.0
        },
        {
          "after_seconds": 79.72,
          "gap_ms": 660.0
        },
        {
          "after_seconds": 82.74,
          "gap_ms": 680.0
        },
        {
          "after_seconds": 83.88,
          "gap_ms": 480.0
        }
      ]
    },
    "counterpart": {
      "response_gaps": [
        {
          "after_seconds": 2.2786666666666666,
          "gap_ms": 1701.333
        },
        {
          "after_seconds": 26.938666666666666,
          "gap_ms": 4941.333
        },
        {
          "after_seconds": 55.638666666666666,
          "gap_ms": 2661.333
        }
      ],
      "no_response_intervals": [
        {
          "after_seconds": 20.918666666666667,
          "gap_ms": 440.0
        },
        {
          "after_seconds": 23.278666666666666,
          "gap_ms": 600.0
        },
        {
          "after_seconds": 25.598666666666666,
          "gap_ms": 480.0
        },
        {
          "after_seconds": 50.23866666666667,
          "gap_ms": 420.0
        },
        {
          "after_seconds": 92.95866666666667,
          "gap_ms": 45280.0
        }
      ]
    }
  },
  "long_silence_threshold_seconds": 10,
  "long_silence_intervals": [
    {
      "start_seconds": 92.95866666666667,
      "end_seconds": 138.23866666666666,
      "duration_seconds": 45.27999999999999,
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
      "item_id": "item_EQbLN8LRprykxzccQeg0K",
      "generated_ms": 6200.0,
      "played_ms": 6199,
      "interrupted_by_target": true
    }
  ],
  "continuity": {
    "status": "measured",
    "clock_id": "chromium-audio-context",
    "items": [
      {
        "item_id": "item_EQbLN8LRprykxzccQeg0K",
        "gap_count": 1,
        "inserted_silence_ms": 33.354,
        "largest_gap_ms": 33.354
      },
      {
        "item_id": "item_EQbLpXHmdayQcBOsZxxMt",
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "largest_gap_ms": 0.0
      },
      {
        "item_id": "item_EQbMFqr1hlohKFXYvpwlC",
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "largest_gap_ms": 0.0
      }
    ],
    "max_bridge_delivery_delay_ms": 1358.699999988079,
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
    "confidence": 0.62,
    "probabilities": {
      "met": 0.72,
      "not_applicable": 0.03,
      "not_met": 0.14,
      "uncertain": 0.11
    },
    "type": "choice"
  },
  "constraint_behavior": {
    "choice": "met",
    "confidence": 0.16,
    "probabilities": {
      "met": 0.44,
      "not_met": 0.28,
      "uncertain": 0.28
    },
    "type": "choice"
  },
  "context_retention": {
    "choice": "met",
    "confidence": 0.17,
    "probabilities": {
      "met": 0.45,
      "not_met": 0.25,
      "uncertain": 0.3
    },
    "type": "choice"
  },
  "conversation_progress": {
    "choice": "met",
    "confidence": 0.2,
    "probabilities": {
      "met": 0.46,
      "not_met": 0.28,
      "uncertain": 0.26
    },
    "type": "choice"
  },
  "counterpart_validity": {
    "choice": "met",
    "confidence": 0.19,
    "probabilities": {
      "met": 0.46,
      "not_met": 0.28,
      "uncertain": 0.26
    },
    "type": "choice"
  },
  "question_relevance": {
    "choice": "met",
    "confidence": 0.17,
    "probabilities": {
      "met": 0.45,
      "not_met": 0.24,
      "uncertain": 0.31
    },
    "type": "choice"
  },
  "target_role_fidelity": {
    "choice": "met",
    "confidence": 0.14,
    "probabilities": {
      "met": 0.42,
      "not_met": 0.32,
      "uncertain": 0.26
    },
    "type": "choice"
  },
  "user_report_accuracy": {
    "choice": "not_applicable",
    "confidence": 0.64,
    "probabilities": {
      "met": 0.18,
      "not_applicable": 0.74,
      "not_met": 0.05,
      "uncertain": 0.03
    },
    "type": "choice"
  }
}
```

Jev is an independent comparison and cannot override verified business records.
All attempts and incomplete stages remain in the batch counts.