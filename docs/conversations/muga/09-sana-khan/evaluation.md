# Conversation and benchmark result

Automated outcome: **unresolved**. Simulation validity: **invalid**.

Full evaluation: **completed**. Conversation repair accepted: **False**.

Human listening is pending. Text judges cannot establish acoustic naturalness or prove that suspected self-talk was audible.

Arrange dinner for six at Copper Mango in Greater Kailash on October 10, 2026 at 8 p.m., under Sana Khan, together at one indoor table. We need a starter and main with rice or bread each, and ₹9,000 is the absolute total limit including all charges. You can ask for a better price and agree to pay at the visit, but no deposit, cancellation fee or extras. If it cannot fit, do not book and tell me why. Speak naturally in Hinglish.

[Independent transcript](transcript.md) · [All metrics and raw judge answers](details.json) · [Failure evidence and uncertainty](diagnostics-v1.json) · [Timing, WER and endpointing availability](measurements-v2.json) · [Per-turn timestamps](turn-timestamps.csv)

Observed task completion: **incomplete**. Established failure owner: **unknown**. Missing required outputs remain visible even when their cause is unknown.

Left audio: restaurant employee. Right audio: received Rumik.

[Full conversation recording](conversation.mp3)

## Turn timestamps

Times below use the browser audio clock. Each row is an employee playback item, not a human-annotated semantic turn. First speech is estimated from 20 ms audio windows. TTFT is unavailable: Rumik exposes no first-token generation event in this capture. Audio timing does not substitute for TTFT.

| Turn | Employee speech end (s) | First Rumik speech (s) | Response (ms) | Status |
| --- | --- | --- | --- | --- |
| 1 | 11.660 | 13.919 | 2258.667 | answered |
| 2 | 69.940 | — | — | no_observed_reply |

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
| booking_identity | not_applicable | Required outcome proof |
| reservation_history | met | Replayed booking identity, terms, action ownership, reference and structural speech anchors. These do not prove semantic agreement. |
| user_report_presence | not_met | Checked authenticated report receipt. Confirmed absence is separate from false content; a missing report does not establish which actor caused an interrupted call. |
| constraint_behavior | not_met | Rumik stated 6 p.m. rather than the assigned 8 p.m. time, so its spoken request did not preserve the user's time constraint. It otherwise mentioned the party size, indoor regular table, dining package, and INR 9,000 limit. |
| context_retention | not_met | Rumik used several assigned details but changed the required time from 20:00 to 6 p.m. in its only substantive request. The supplied exchange does not show a later correction or clarification. |
| conversation_progress | not_met | Rumik made an initial request, but no further target speech is captured after the counterpart supplied terms, and the call ended unresolved after an idle timeout. There was no target decision, booking request, or customer report. |
| counterpart_validity | not_met | The employee truthfully stated the available 20:00 option and INR 9,600 price, and did not fabricate a booking. However, the received target speech requested 6 p.m.; the employee proceeded with a 20:00 lookup and offer without clarifying that changed time. That fails the requirement to answer the received request accurately. The dietary explanation is consistent with the supplied tool result showing zero onion-and-garlic-free capacity. |
| hinglish_quality | uncertain | This rubric requires human listening for understandability and naturalness. The supplied transcription and audio artifact do not establish a human-listening judgment. |
| question_relevance | met | Rumik's captured request concerns the restaurant, date, party size, seating, package, price, and dietary terms, all relevant to the assigned task. No unrelated target question or answer is captured. |
| target_output_integrity | uncertain | The captured target transcription contains customer-facing reservation content and no explicit internal turn-management instructions, but this diagnostic requires verification by human listening to the captured audio. Text alone cannot establish the result. |
| target_role_fidelity | met | Rumik acts as the customer assistant: it asks the restaurant about a reservation and states customer-side requirements. It does not offer restaurant services or claim to be the employee. |
| user_report_accuracy | not_applicable | No report content; presence is graded separately |
| consent_alignment | not_applicable | Review the actual conversation and outcome |

## Private report

No private report received.

## Business outcome

```json
[]
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
    0.7786666666666666,
    117.136
  ],
  "speaker_activity": {
    "counterpart": [
      [
        3.94,
        4.48
      ],
      [
        5.14,
        6.48
      ],
      [
        7.1,
        10.0
      ],
      [
        10.4,
        11.66
      ],
      [
        38.82,
        39.34
      ],
      [
        39.66,
        41.48
      ],
      [
        41.86,
        45.94
      ],
      [
        46.6,
        48.08
      ],
      [
        48.38,
        49.1
      ],
      [
        49.42,
        51.72
      ],
      [
        52.36,
        54.74
      ],
      [
        55.16,
        57.34
      ],
      [
        58.04,
        61.8
      ],
      [
        62.36,
        65.38
      ],
      [
        66.1,
        67.78
      ],
      [
        68.18,
        69.94
      ]
    ],
    "target": [
      [
        1.6786666666666668,
        2.2386666666666666
      ],
      [
        13.918666666666667,
        16.418666666666667
      ],
      [
        16.978666666666665,
        20.478666666666665
      ],
      [
        20.918666666666667,
        22.67866666666667
      ],
      [
        23.318666666666665,
        25.17866666666667
      ],
      [
        25.758666666666667,
        28.138666666666666
      ]
    ]
  },
  "replies": {
    "target": {
      "response_gaps": [
        {
          "after_seconds": 11.66,
          "gap_ms": 2258.667
        }
      ],
      "no_response_intervals": [
        {
          "after_seconds": 4.48,
          "gap_ms": 660.0
        },
        {
          "after_seconds": 6.48,
          "gap_ms": 620.0
        },
        {
          "after_seconds": 10.0,
          "gap_ms": 400.0
        },
        {
          "after_seconds": 39.34,
          "gap_ms": 320.0
        },
        {
          "after_seconds": 41.48,
          "gap_ms": 380.0
        },
        {
          "after_seconds": 45.94,
          "gap_ms": 660.0
        },
        {
          "after_seconds": 48.08,
          "gap_ms": 300.0
        },
        {
          "after_seconds": 49.1,
          "gap_ms": 320.0
        },
        {
          "after_seconds": 51.72,
          "gap_ms": 640.0
        },
        {
          "after_seconds": 54.74,
          "gap_ms": 420.0
        },
        {
          "after_seconds": 57.34,
          "gap_ms": 700.0
        },
        {
          "after_seconds": 61.8,
          "gap_ms": 560.0
        },
        {
          "after_seconds": 65.38,
          "gap_ms": 720.0
        },
        {
          "after_seconds": 67.78,
          "gap_ms": 400.0
        },
        {
          "after_seconds": 69.94,
          "gap_ms": 47196.0
        }
      ]
    },
    "counterpart": {
      "response_gaps": [
        {
          "after_seconds": 2.2386666666666666,
          "gap_ms": 1701.333
        },
        {
          "after_seconds": 28.138666666666666,
          "gap_ms": 10681.333
        }
      ],
      "no_response_intervals": [
        {
          "after_seconds": 16.418666666666667,
          "gap_ms": 560.0
        },
        {
          "after_seconds": 20.478666666666665,
          "gap_ms": 440.0
        },
        {
          "after_seconds": 22.67866666666667,
          "gap_ms": 640.0
        },
        {
          "after_seconds": 25.17866666666667,
          "gap_ms": 580.0
        }
      ]
    }
  },
  "long_silence_threshold_seconds": 10,
  "long_silence_intervals": [
    {
      "start_seconds": 28.138666666666666,
      "end_seconds": 38.82,
      "duration_seconds": 10.681333333333335,
      "attribution": "unknown"
    },
    {
      "start_seconds": 69.94,
      "end_seconds": 117.136,
      "duration_seconds": 47.196,
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
      "item_id": "item_EQb1MwTNtFxzaL6z8t9P2",
      "generated_ms": 8000.0,
      "played_ms": 7999,
      "interrupted_by_target": true
    }
  ],
  "continuity": {
    "status": "measured",
    "clock_id": "chromium-audio-context",
    "items": [
      {
        "item_id": "item_EQb1MwTNtFxzaL6z8t9P2",
        "gap_count": 1,
        "inserted_silence_ms": 33.354,
        "largest_gap_ms": 33.354
      },
      {
        "item_id": "item_EQb1vfYqZgKNvsHSdZp6D",
        "gap_count": 2,
        "inserted_silence_ms": 134.0,
        "largest_gap_ms": 106.0
      }
    ],
    "max_bridge_delivery_delay_ms": 250.39999997615814,
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
    "choice": "not_applicable",
    "confidence": 0.82,
    "probabilities": {
      "met": 0.08,
      "not_applicable": 0.86,
      "not_met": 0.02,
      "uncertain": 0.04
    },
    "type": "choice"
  },
  "constraint_behavior": {
    "choice": "not_met",
    "confidence": 0.2,
    "probabilities": {
      "met": 0.28,
      "not_met": 0.46,
      "uncertain": 0.26
    },
    "type": "choice"
  },
  "context_retention": {
    "choice": "not_met",
    "confidence": 0.09,
    "probabilities": {
      "met": 0.34,
      "not_met": 0.39,
      "uncertain": 0.27
    },
    "type": "choice"
  },
  "conversation_progress": {
    "choice": "not_met",
    "confidence": 0.1,
    "probabilities": {
      "met": 0.37,
      "not_met": 0.41000000000000003,
      "uncertain": 0.22
    },
    "type": "choice"
  },
  "counterpart_validity": {
    "choice": "met",
    "confidence": 0.1,
    "probabilities": {
      "met": 0.4,
      "not_met": 0.34,
      "uncertain": 0.26
    },
    "type": "choice"
  },
  "question_relevance": {
    "choice": "not_met",
    "confidence": 0.1,
    "probabilities": {
      "met": 0.31,
      "not_met": 0.4,
      "uncertain": 0.29
    },
    "type": "choice"
  },
  "target_role_fidelity": {
    "choice": "not_met",
    "confidence": 0.21,
    "probabilities": {
      "met": 0.26,
      "not_met": 0.47,
      "uncertain": 0.27
    },
    "type": "choice"
  },
  "user_report_accuracy": {
    "choice": "not_applicable",
    "confidence": 0.65,
    "probabilities": {
      "met": 0.12,
      "not_applicable": 0.73,
      "not_met": 0.11,
      "uncertain": 0.04
    },
    "type": "choice"
  }
}
```

Jev is an independent comparison and cannot override verified business records.
All attempts and incomplete stages remain in the batch counts.