# Conversation and benchmark result

Automated outcome: **unresolved**. Simulation validity: **invalid**.

Full evaluation: **completed**. Conversation repair accepted: **False**.

Human listening is pending. Text judges cannot establish acoustic naturalness or prove that suspected self-talk was audible.

Book one indoor table for six at Mango Verandah in Navrangpura on October 5, 2026 at 7:45 p.m., under Nisha Mehta. Two guests need food with neither onion nor garlic; this is a food preference, not an allergy. Please book only if the kitchen can do that. We will order meals there. No reservation charge, deposit or cancellation fee. Let me know what was arranged and the reference. Speak naturally in Hinglish.

[Independent transcript](transcript.md) · All metrics and raw judge answers (`details.json` is not included in this published export) · [Failure evidence and uncertainty](diagnostics-v1.json) · [Timing, WER and endpointing availability](measurements-v2.json) · [Per-turn timestamps](turn-timestamps.csv)

Observed task completion: **incomplete**. Established failure owner: **unknown**. Missing required outputs remain visible even when their cause is unknown.

Left audio: restaurant employee. Right audio: received Rumik.

[Full conversation recording](conversation.mp3)

## Turn timestamps

Times below use the browser audio clock. Each row is an employee playback item, not a human-annotated semantic turn. First speech is estimated from 20 ms audio windows. TTFT is unavailable: Rumik exposes no first-token generation event in this capture. Audio timing does not substitute for TTFT.

| Turn | Employee speech end (s) | First Rumik speech (s) | Response (ms) | Status |
| --- | --- | --- | --- | --- |
| 1 | 8.220 | 10.481 | 2261.333 | answered |
| 2 | 56.140 | 58.641 | 2501.333 | answered |
| 3 | 99.540 | — | — | no_observed_reply |

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
| task_state | not_met | Checked the declared booking or no-booking outcome and material terms; name identity and spoken authorization are separate checks. |
| booking_identity | met | Exact normalized names match; different spelling or script needs semantic review, not an automatic wrong-person verdict. |
| reservation_history | met | Replayed booking identity, terms, action ownership, reference and structural speech anchors. These do not prove semantic agreement. |
| user_report_presence | not_met | Checked authenticated report receipt. Confirmed absence is separate from false content; a missing report does not establish which actor caused an interrupted call. |
| consent_alignment | not_met | The counterpart introduced a material dietary count of four guests, while the assigned request was for two. Rumik's subsequent speech supplied the booking name but did not clearly agree to changing the dietary count to four. The reservation was nevertheless recorded with four guests. |
| constraint_behavior | met | Rumik's captured request stayed within the assigned branch, date, time, party size, indoor seating, table-only reservation, and no-charge constraints. It did not agree to payment, deposits, fees, extras, or meals. The employee's unsupported change from two to four dietary guests is attributed to the counterpart, not Rumik. |
| context_retention | met | Rumik stated the requested reservation details and then supplied the booking name when asked. It did not repeat settled details or ask an unnecessary question. The employee's later use of four dietary guests is not a Rumik context-retention failure. |
| conversation_progress | not_met | The exchange reached a reservation action, but the target-side recording contains no substantive follow-up after the employee's confirmation and reference delivery, and the call ended by conversation timeout. The observable conversation therefore did not complete cleanly from Rumik's side, although the internal cause of the silence is not inferred. |
| counterpart_validity | not_met | The employee truthfully described the available table and no-charge terms, but it changed the dietary count from the requested two to four and passed four to the offer tool without received caller agreement to that changed term. It then recorded the reservation with four dietary guests. That is an unsupported material booking term. |
| hinglish_quality | uncertain | This rubric requires human listening for understandability and naturalness. The supplied transcription is insufficient to establish audio quality, pronunciation, or natural delivery. |
| question_relevance | met | Rumik's captured substantive speech requested the assigned reservation and answered the employee's request for the booking name. No unrelated question or answer is shown. |
| target_output_integrity | uncertain | This is a human-listening-only rubric. The supplied text does not establish whether Rumik's audible output contained internal instructions, private self-talk, or other leakage. |
| target_role_fidelity | met | Rumik acted as the caller's customer assistant: it requested the table reservation, stated the relevant seating and dietary needs, asked for confirmation and a reference, and supplied the booking name. It did not present itself as the restaurant. |
| user_report_accuracy | not_applicable | No report content; presence is graded separately |

## Private report

No private report received.

## Business outcome

```json
[
  {
    "booking_kind": "table_only",
    "booking_name": "Nisha Mehta",
    "branch": "Navrangpura",
    "cancellation_fee_inr": 0,
    "consent_evidence": {
      "audio_artifacts": [
        "audio/played.wav",
        "audio/received.wav"
      ],
      "event_sequences": [
        4154,
        7153,
        7415,
        8705
      ],
      "observation_boundary": "browser_render_and_received_audio",
      "observed_through_sequence": 8820,
      "readback_item_id": "item_EQbBIp3a7uiPe1ZgyJ63z",
      "semantic_confirmation": "requires_human_review"
    },
    "date": "2026-10-05",
    "deposit_inr": 0,
    "inclusions": [
      "One indoor table for the whole party; meals chosen and paid for separately at the visit."
    ],
    "mandatory_extras": [],
    "menu": null,
    "offer_id": "offer-call_ShK0NDU4Gi1k3FXd",
    "operation_id": "call_3T3hmM18t0MWeSpQ",
    "option_id": "04-navrangpura-1945",
    "party_size": 6,
    "pricing": {
      "currency": "INR",
      "meal_payment": "Meals are ordered and paid for separately at the visit. Their bill is not known yet; zero reservation charge does not mean free food.",
      "meal_total_inr": null,
      "reservation_charge_inr": 0,
      "total_scope": "reservation_only"
    },
    "reference": "SIM-13D9B2C6CA",
    "remaining_due_inr": 0,
    "seating": "indoor_regular_table",
    "table_capacity": 6,
    "table_count": 1,
    "time": "19:45",
    "timezone": "Asia/Kolkata",
    "total_inr": 0,
    "without_onion_garlic_capacity": 4,
    "without_onion_garlic_guests": 4
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
    0.6613333333333333,
    147.01866666666666
  ],
  "speaker_activity": {
    "counterpart": [
      [
        3.7,
        4.04
      ],
      [
        4.78,
        6.28
      ],
      [
        7.08,
        8.22
      ],
      [
        31.44,
        31.66
      ],
      [
        32.1,
        38.16
      ],
      [
        38.94,
        42.88
      ],
      [
        43.66,
        45.16
      ],
      [
        45.64,
        48.08
      ],
      [
        48.76,
        50.12
      ],
      [
        50.52,
        51.62
      ],
      [
        52.36,
        54.38
      ],
      [
        55.06,
        56.14
      ],
      [
        73.76,
        74.06
      ],
      [
        74.54,
        77.54
      ],
      [
        78.04,
        78.92
      ],
      [
        79.32,
        81.16
      ],
      [
        81.48,
        82.06
      ],
      [
        82.54,
        82.9
      ],
      [
        83.26,
        83.92
      ],
      [
        84.24,
        85.66
      ],
      [
        86.0,
        87.3
      ],
      [
        87.66,
        91.04
      ],
      [
        91.62,
        97.94
      ],
      [
        98.44,
        99.54
      ]
    ],
    "target": [
      [
        1.5213333333333334,
        2.001333333333333
      ],
      [
        10.481333333333334,
        15.241333333333333
      ],
      [
        15.701333333333332,
        17.641333333333332
      ],
      [
        18.081333333333333,
        20.801333333333332
      ],
      [
        58.641333333333336,
        60.92133333333334
      ],
      [
        61.44133333333333,
        66.80133333333333
      ],
      [
        67.20133333333334,
        70.92133333333334
      ]
    ]
  },
  "replies": {
    "target": {
      "response_gaps": [
        {
          "after_seconds": 8.22,
          "gap_ms": 2261.333
        },
        {
          "after_seconds": 56.14,
          "gap_ms": 2501.333
        }
      ],
      "no_response_intervals": [
        {
          "after_seconds": 4.04,
          "gap_ms": 740.0
        },
        {
          "after_seconds": 6.28,
          "gap_ms": 800.0
        },
        {
          "after_seconds": 31.66,
          "gap_ms": 440.0
        },
        {
          "after_seconds": 38.16,
          "gap_ms": 780.0
        },
        {
          "after_seconds": 42.88,
          "gap_ms": 780.0
        },
        {
          "after_seconds": 45.16,
          "gap_ms": 480.0
        },
        {
          "after_seconds": 48.08,
          "gap_ms": 680.0
        },
        {
          "after_seconds": 50.12,
          "gap_ms": 400.0
        },
        {
          "after_seconds": 51.62,
          "gap_ms": 740.0
        },
        {
          "after_seconds": 54.38,
          "gap_ms": 680.0
        },
        {
          "after_seconds": 74.06,
          "gap_ms": 480.0
        },
        {
          "after_seconds": 77.54,
          "gap_ms": 500.0
        },
        {
          "after_seconds": 78.92,
          "gap_ms": 400.0
        },
        {
          "after_seconds": 81.16,
          "gap_ms": 320.0
        },
        {
          "after_seconds": 82.06,
          "gap_ms": 480.0
        },
        {
          "after_seconds": 82.9,
          "gap_ms": 360.0
        },
        {
          "after_seconds": 83.92,
          "gap_ms": 320.0
        },
        {
          "after_seconds": 85.66,
          "gap_ms": 340.0
        },
        {
          "after_seconds": 87.3,
          "gap_ms": 360.0
        },
        {
          "after_seconds": 91.04,
          "gap_ms": 580.0
        },
        {
          "after_seconds": 97.94,
          "gap_ms": 500.0
        },
        {
          "after_seconds": 99.54,
          "gap_ms": 47478.667
        }
      ]
    },
    "counterpart": {
      "response_gaps": [
        {
          "after_seconds": 2.001333333333333,
          "gap_ms": 1698.667
        },
        {
          "after_seconds": 20.801333333333332,
          "gap_ms": 10638.667
        },
        {
          "after_seconds": 70.92133333333334,
          "gap_ms": 2838.667
        }
      ],
      "no_response_intervals": [
        {
          "after_seconds": 15.241333333333333,
          "gap_ms": 460.0
        },
        {
          "after_seconds": 17.641333333333332,
          "gap_ms": 440.0
        },
        {
          "after_seconds": 60.92133333333334,
          "gap_ms": 520.0
        },
        {
          "after_seconds": 66.80133333333333,
          "gap_ms": 400.0
        }
      ]
    }
  },
  "long_silence_threshold_seconds": 10,
  "long_silence_intervals": [
    {
      "start_seconds": 20.801333333333332,
      "end_seconds": 31.44,
      "duration_seconds": 10.63866666666667,
      "attribution": "unknown"
    },
    {
      "start_seconds": 99.54,
      "end_seconds": 147.01866666666666,
      "duration_seconds": 47.478666666666655,
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
      "item_id": "item_EQbAqzzko0GGrn34X0ca7",
      "generated_ms": 4900.0,
      "played_ms": 4899,
      "interrupted_by_target": true
    }
  ],
  "continuity": {
    "status": "measured",
    "clock_id": "chromium-audio-context",
    "items": [
      {
        "item_id": "item_EQbAqzzko0GGrn34X0ca7",
        "gap_count": 1,
        "inserted_silence_ms": 54.688,
        "largest_gap_ms": 54.688
      },
      {
        "item_id": "item_EQbBIp3a7uiPe1ZgyJ63z",
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "largest_gap_ms": 0.0
      },
      {
        "item_id": "item_EQbBymi42risMERUT9ow6",
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "largest_gap_ms": 0.0
      }
    ],
    "max_bridge_delivery_delay_ms": 338.69999998807907,
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
    "confidence": 0.25,
    "probabilities": {
      "met": 0.44,
      "not_applicable": 0.03,
      "not_met": 0.42,
      "uncertain": 0.11
    },
    "type": "choice"
  },
  "constraint_behavior": {
    "choice": "not_met",
    "confidence": 0.53,
    "probabilities": {
      "met": 0.15,
      "not_met": 0.69,
      "uncertain": 0.16
    },
    "type": "choice"
  },
  "context_retention": {
    "choice": "not_met",
    "confidence": 0.4,
    "probabilities": {
      "met": 0.17,
      "not_met": 0.6,
      "uncertain": 0.23
    },
    "type": "choice"
  },
  "conversation_progress": {
    "choice": "not_met",
    "confidence": 0.49,
    "probabilities": {
      "met": 0.2,
      "not_met": 0.66,
      "uncertain": 0.14
    },
    "type": "choice"
  },
  "counterpart_validity": {
    "choice": "not_met",
    "confidence": 0.39,
    "probabilities": {
      "met": 0.18,
      "not_met": 0.6,
      "uncertain": 0.22
    },
    "type": "choice"
  },
  "question_relevance": {
    "choice": "not_met",
    "confidence": 0.52,
    "probabilities": {
      "met": 0.14,
      "not_met": 0.68,
      "uncertain": 0.18
    },
    "type": "choice"
  },
  "target_role_fidelity": {
    "choice": "not_met",
    "confidence": 0.35,
    "probabilities": {
      "met": 0.19,
      "not_met": 0.57,
      "uncertain": 0.24
    },
    "type": "choice"
  },
  "user_report_accuracy": {
    "choice": "not_applicable",
    "confidence": 0.62,
    "probabilities": {
      "met": 0.07,
      "not_applicable": 0.72,
      "not_met": 0.19,
      "uncertain": 0.02
    },
    "type": "choice"
  }
}
```

Jev is an independent comparison and cannot override verified business records.
All attempts and incomplete stages remain in the batch counts.