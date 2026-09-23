# Conversation and benchmark result

Automated outcome: **passed**. Simulation validity: **valid**.

Full evaluation: **completed**. Conversation repair accepted: **False**.

Human listening is pending. Text judges cannot establish acoustic naturalness or prove that suspected self-talk was audible.

Please book one indoor table for five at Clay Bowl in Alkapuri on October 11, 2026 at 7:15 p.m., under Rohan Desai. Two guests need food containing neither onion nor garlic; it is a food preference, not an allergy. Book only if the kitchen can meet both exclusions for both people. We will order meals there, and there must be no booking charge, deposit or cancellation fee. Otherwise leave it unbooked and explain why. Speak naturally in Hinglish.

[Independent transcript](transcript.md) · All metrics and raw judge answers (`details.json` is not included in this published export) · [Failure evidence and uncertainty](diagnostics-v1.json) · [Timing, WER and endpointing availability](measurements-v2.json) · [Per-turn timestamps](turn-timestamps.csv)

Observed task completion: **unresolved**. Established failure owner: **unknown**. Missing required outputs remain visible even when their cause is unknown.

Left audio: restaurant employee. Right audio: received Rumik.

[Full conversation recording](conversation.mp3)

## Turn timestamps

Times below use the browser audio clock. Each row is an employee playback item, not a human-annotated semantic turn. First speech is estimated from 20 ms audio windows. First token is the arrival of Rumik's first text packet (`bot-llm-text`) at the browser after that speech ended; it includes network transit and is an upper bound on hosted generation latency.

| Turn | Employee speech end (s) | First Rumik token (s) | TTFT (ms) | First Rumik speech (s) | TTFS (ms) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 7.027 | — | — | — | — | no_observed_reply |
| 2 | 21.867 | 23.435 | 1568.000 | 24.089 | 2222.667 | answered |
| 3 | 57.187 | 59.605 | 2418.667 | 60.349 | 3162.667 | answered |

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
| booking_identity | not_applicable | Required outcome proof |
| reservation_history | met | Replayed booking identity, terms, action ownership, reference and structural speech anchors. These do not prove semantic agreement. |
| user_report_references | uncertain | Compared only explicitly labelled target report references using explicit-reference-clauses-v2. Distinct codes remain distinct. A match checks identifiers only, not overall report accuracy; unsupported prose requires review. |
| user_report_presence | met | Checked authenticated report receipt. Confirmed absence is separate from false content; a missing report does not establish which actor caused an interrupted call. |
| constraint_behavior | met | Rumik stated the requested date, party size, branch, indoor table, booking name, and onion-and-garlic-free requirement, without agreeing to any unauthorized charge, meal purchase, deposit, or alternative. It appropriately ended the exchange after the dietary limitation was disclosed. |
| context_retention | met | Rumik used the assigned requirements in its substantive request and did not unnecessarily repeat them or ask the employee to restate settled terms. Its closing after the employee reported the dietary blocker was consistent with the instruction not to book if no authorized option existed. |
| conversation_progress | met | The exchange progressed from the request, through the employee's clarification, to disclosure of the dietary limitation and a natural customer close. There is no repeated agreement or question loop attributable to Rumik. |
| counterpart_validity | met | The employee's dietary limitation statement matches the failed dietary-capacity offer result, and the employee did not claim a booking or invent a reference. The employee's question about a table-only booking or alternative was relevant; the absence of a booking is consistent with the no-suitable-option outcome. |
| hinglish_quality | uncertain | This rubric requires human listening for understandability and naturalness. The supplied transcription shows a substantive Hinglish exchange, but text evidence alone cannot establish audio quality or natural delivery. |
| question_relevance | met | Rumik's substantive utterance asked the employee to check the exact requested reservation and dietary accommodation. Its closing was relevant after the employee disclosed that the dietary requirement could not be met; there is no unrelated target question or answer. |
| target_output_integrity | uncertain | The available transcript contains only customer-facing conversation and no evident internal turn-management instructions, but this diagnostic requires verification from captured audio and cannot be conclusively passed from text alone. |
| target_role_fidelity | met | Rumik acted as the customer's assistant: it communicated the reservation request and dietary condition, asked the restaurant to check feasibility, and did not offer restaurant services or claim a booking. |
| user_report_accuracy | met | The authenticated report states that no booking was made because the kitchen could not meet the onion-and-garlic-free requirement for two guests. This matches the final business state of zero bookings and the failed dietary-capacity result; it invents no reference or unsupported booking detail. |
| consent_alignment | not_applicable | Review the actual conversation and outcome |

## Private report

No booking was made because the kitchen cannot meet the onion‑ and garlic‑free requirement for the two guests.

## Business outcome

```json
[]
```

## Silence and response timing

```json
{
  "activity_is_not_semantic_turns": true,
  "algorithm": "rms-20ms-merge300ms-v2",
  "boundary": "browser_render_and_capture",
  "clock_id": "chromium-audio-context",
  "coverage_seconds": [
    1.5093333333333334,
    67.18933333333334
  ],
  "long_silence_intervals": [
    {
      "attribution": "unknown",
      "duration_seconds": 11.259999999999998,
      "end_seconds": 18.286666666666665,
      "start_seconds": 7.026666666666666
    }
  ],
  "long_silence_threshold_seconds": 10,
  "replies": {
    "counterpart": {
      "no_response_intervals": [
        {
          "after_seconds": 24.749333333333333,
          "gap_ms": 920.0
        },
        {
          "after_seconds": 28.229333333333333,
          "gap_ms": 560.0
        },
        {
          "after_seconds": 29.269333333333332,
          "gap_ms": 440.0
        },
        {
          "after_seconds": 31.729333333333333,
          "gap_ms": 720.0
        },
        {
          "after_seconds": 35.04933333333334,
          "gap_ms": 600.0
        },
        {
          "after_seconds": 36.449333333333335,
          "gap_ms": 540.0
        },
        {
          "after_seconds": 38.129333333333335,
          "gap_ms": 600.0
        },
        {
          "after_seconds": 42.60933333333333,
          "gap_ms": 680.0
        },
        {
          "after_seconds": 61.989333333333335,
          "gap_ms": 5200.0
        }
      ],
      "response_gaps": [
        {
          "after_seconds": 3.029333333333333,
          "gap_ms": 1697.333
        },
        {
          "after_seconds": 44.50933333333333,
          "gap_ms": 4077.333
        }
      ]
    },
    "target": {
      "no_response_intervals": [
        {
          "after_seconds": 5.046666666666667,
          "gap_ms": 600.0
        },
        {
          "after_seconds": 7.026666666666666,
          "gap_ms": 11260.0
        },
        {
          "after_seconds": 18.526666666666667,
          "gap_ms": 440.0
        },
        {
          "after_seconds": 49.22666666666667,
          "gap_ms": 360.0
        },
        {
          "after_seconds": 53.22666666666667,
          "gap_ms": 520.0
        },
        {
          "after_seconds": 55.166666666666664,
          "gap_ms": 320.0
        }
      ],
      "response_gaps": [
        {
          "after_seconds": 21.866666666666667,
          "gap_ms": 2222.667
        },
        {
          "after_seconds": 57.18666666666667,
          "gap_ms": 3162.667
        }
      ]
    }
  },
  "rms_threshold": 500,
  "speaker_activity": {
    "counterpart": [
      [
        4.726666666666667,
        5.046666666666667
      ],
      [
        5.6466666666666665,
        7.026666666666666
      ],
      [
        18.286666666666665,
        18.526666666666667
      ],
      [
        18.966666666666665,
        21.866666666666667
      ],
      [
        48.586666666666666,
        49.22666666666667
      ],
      [
        49.586666666666666,
        53.22666666666667
      ],
      [
        53.74666666666667,
        55.166666666666664
      ],
      [
        55.486666666666665,
        57.18666666666667
      ]
    ],
    "target": [
      [
        2.2293333333333334,
        3.029333333333333
      ],
      [
        24.089333333333332,
        24.749333333333333
      ],
      [
        25.669333333333334,
        28.229333333333333
      ],
      [
        28.78933333333333,
        29.269333333333332
      ],
      [
        29.709333333333333,
        31.729333333333333
      ],
      [
        32.449333333333335,
        35.04933333333334
      ],
      [
        35.64933333333333,
        36.449333333333335
      ],
      [
        36.989333333333335,
        38.129333333333335
      ],
      [
        38.72933333333334,
        42.60933333333333
      ],
      [
        43.28933333333333,
        44.50933333333333
      ],
      [
        60.349333333333334,
        61.989333333333335
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
        "item_id": "item_EQgSKU8AzjBdsR30K2peS",
        "largest_gap_ms": 0.0
      },
      {
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "item_id": "item_EQgSX0V3HKl5wxR9ECQEf",
        "largest_gap_ms": 0.0
      },
      {
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "item_id": "item_EQgT22Dp5L7jxvYkl4UzI",
        "largest_gap_ms": 0.0
      }
    ],
    "max_bridge_delivery_delay_ms": 89.19999998807907,
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
    "choice": "not_applicable",
    "confidence": 0.61,
    "probabilities": {
      "met": 0.27,
      "not_applicable": 0.71,
      "not_met": 0.01,
      "uncertain": 0.01
    },
    "type": "choice"
  },
  "constraint_behavior": {
    "choice": "met",
    "confidence": 0.58,
    "probabilities": {
      "met": 0.72,
      "not_met": 0.14,
      "uncertain": 0.14
    },
    "type": "choice"
  },
  "context_retention": {
    "choice": "met",
    "confidence": 0.57,
    "probabilities": {
      "met": 0.72,
      "not_met": 0.11,
      "uncertain": 0.17
    },
    "type": "choice"
  },
  "conversation_progress": {
    "choice": "met",
    "confidence": 0.6,
    "probabilities": {
      "met": 0.74,
      "not_met": 0.14,
      "uncertain": 0.12
    },
    "type": "choice"
  },
  "counterpart_validity": {
    "choice": "met",
    "confidence": 0.64,
    "probabilities": {
      "met": 0.76,
      "not_met": 0.11,
      "uncertain": 0.13
    },
    "type": "choice"
  },
  "question_relevance": {
    "choice": "met",
    "confidence": 0.55,
    "probabilities": {
      "met": 0.7,
      "not_met": 0.12,
      "uncertain": 0.18
    },
    "type": "choice"
  },
  "target_role_fidelity": {
    "choice": "met",
    "confidence": 0.52,
    "probabilities": {
      "met": 0.68,
      "not_met": 0.14,
      "uncertain": 0.18
    },
    "type": "choice"
  },
  "user_report_accuracy": {
    "choice": "met",
    "confidence": 0.84,
    "probabilities": {
      "met": 0.89,
      "not_applicable": 0,
      "not_met": 0.06,
      "uncertain": 0.05
    },
    "type": "choice"
  }
}
```

Jev is an independent comparison and cannot override verified business records.
All attempts and incomplete stages remain in the batch counts.