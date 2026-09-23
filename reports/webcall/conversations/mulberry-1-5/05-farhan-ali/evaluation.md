# Conversation and benchmark result

Automated outcome: **failed**. Simulation validity: **valid**.

Full evaluation: **completed**. Conversation repair accepted: **False**.

Human listening is pending. Text judges cannot establish acoustic naturalness or prove that suspected self-talk was audible.

Book one indoor table for four at Tamarind Room on October 6, 2026, under Farhan Ali. Any time from 7 to 8 p.m. at Jubilee Hills or Banjara Hills is fine. Choose the earliest available time; Jubilee Hills is my preference only if the times are the same. Make a free table reservation with no deposit or cancellation fee. Tell me the final details and reference. Speak naturally in Hinglish.

[Independent transcript](transcript.md) · All metrics and raw judge answers (`details.json` is not included in this published export) · [Failure evidence and uncertainty](diagnostics-v1.json) · [Timing, WER and endpointing availability](measurements-v2.json) · [Per-turn timestamps](turn-timestamps.csv)

Observed task completion: **unresolved**. Established failure owner: **unknown**. Missing required outputs remain visible even when their cause is unknown.

Left audio: restaurant employee. Right audio: received Rumik.

[Full conversation recording](conversation.mp3)

## Turn timestamps

Times below use the browser audio clock. Each row is an employee playback item, not a human-annotated semantic turn. First speech is estimated from 20 ms audio windows. First token is the arrival of Rumik's first text packet (`bot-llm-text`) at the browser after that speech ended; it includes network transit and is an upper bound on hosted generation latency.

| Turn | Employee speech end (s) | First Rumik token (s) | TTFT (ms) | First Rumik speech (s) | TTFS (ms) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 8.867 | 10.869 | 2002.667 | 11.451 | 2584.000 | answered |
| 2 | 43.867 | 45.045 | 1178.667 | 45.891 | 2024.000 | answered |
| 3 | 58.807 | 61.280 | 2473.333 | 61.911 | 3104.000 | answered |

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
| task_state | not_met | Checked the declared booking or no-booking outcome and material terms; name identity and spoken authorization are separate checks. |
| booking_identity | met | Exact normalized names match; different spelling or script needs semantic review, not an automatic wrong-person verdict. |
| reservation_history | met | Replayed booking identity, terms, action ownership, reference and structural speech anchors. These do not prove semantic agreement. |
| user_report_references | met | Compared only explicitly labelled target report references using explicit-reference-clauses-v2. Distinct codes remain distinct. A match checks identifiers only, not overall report accuracy; unsupported prose requires review. |
| user_report_presence | met | Checked authenticated report receipt. Confirmed absence is separate from false content; a missing report does not establish which actor caused an interrupted call. |
| consent_alignment | met | The employee disclosed the material terms: indoor regular table for four, 6 October, 7:30 pm, no deposit or charge, and meals ordered separately. Rumik then clearly agreed to book those terms. |
| constraint_behavior | not_met | Rumik did not preserve the requested search order. It asked for the earliest slot at Jubilee Hills only, although the assignment required the earliest qualifying time across both allowed branches, with Jubilee Hills only as a tie-breaker. The qualifying 19:00 Banjara Hills option was therefore missed, and the booked 19:30 Jubilee Hills option was not the required earliest outcome. |
| context_retention | not_met | Rumik retained the seating, party size, name, date range, and no-charge requirements, but it did not retain the branch preference rule correctly. It treated Jubilee Hills as the search location rather than using it only to break an equal-time tie, causing the earlier Banjara Hills option to be overlooked. |
| conversation_progress | met | The exchange progressed from the request, to availability, to disclosure of terms, to a booking decision, confirmation, and closure. There was no unjustified repeated-agreement or question loop. |
| counterpart_validity | met | The employee answered the received Jubilee Hills request using the availability tool, disclosed the applicable reservation and meal terms, obtained agreement, and recorded a reservation only after agreement. The confirmation and reference match the committed business result; no unsupported concession or invented booking is evident. |
| hinglish_quality | uncertain | This rubric requires human listening for understandability and naturalness. The supplied transcript alone cannot establish audio quality, pronunciation, or conversational naturalness. |
| question_relevance | met | Rumik's substantive request asked the employee to check and book the requested table, and its later affirmative answer responded to the booking question. The employee's questions were also directly related to availability and booking. |
| target_output_integrity | uncertain | The transcript contains ordinary customer-facing conversation and no explicit internal turn-management or private self-talk. However, this diagnostic requires verification from the captured audio, and transcript text alone is insufficient to establish audible output integrity. |
| target_role_fidelity | met | Rumik acted as the customer's assistant: it requested a table reservation, supplied the booking name and constraints, answered the employee's booking question, and did not offer restaurant services. The exchange was substantive. |
| user_report_accuracy | met | The authenticated report accurately states the committed booking: 6 October 2026 at 19:30, indoor regular table for four, under Farhan Ali, with no reservation charge, and reference SIM-641022. These fields match the final business record, including the single reference identity. |

## Private report

Booked 6 Oct 2026 at 7:30pm indoor regular table for 4 under Farhan Ali, no charge, reference SIM-641022

## Business outcome

```json
[
  {
    "booking_kind": "table_only",
    "booking_name": "Farhan Ali",
    "branch": "Jubilee Hills",
    "cancellation_fee_inr": 0,
    "consent_evidence": {
      "audio_artifacts": [
        "audio/played.wav",
        "audio/received.wav"
      ],
      "event_sequences": [
        3903,
        5501,
        5756,
        6021
      ],
      "observation_boundary": "browser_render_and_received_audio",
      "observed_through_sequence": 6132,
      "readback_item_id": "item_EQgM0zmNflCKzPQAOAPfv",
      "semantic_confirmation": "requires_human_review"
    },
    "date": "2026-10-06",
    "deposit_inr": 0,
    "inclusions": [
      "One indoor table for the whole party; meals chosen and paid for separately at the visit."
    ],
    "mandatory_extras": [],
    "menu": null,
    "offer_id": "offer-call_K762mDylzzwJN9pR",
    "operation_id": "call_a4xY0HrDqT04YuhA",
    "option_id": "05-jubilee-1930",
    "party_size": 4,
    "pricing": {
      "currency": "INR",
      "meal_payment": "Meals are ordered and paid for separately at the visit. Their bill is not known yet; zero reservation charge does not mean free food.",
      "meal_total_inr": null,
      "reservation_charge_inr": 0,
      "total_scope": "reservation_only"
    },
    "reference": "SIM-641022",
    "remaining_due_inr": 0,
    "seating": "indoor_regular_table",
    "table_capacity": 4,
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
    1.0506666666666666,
    70.18666666666667
  ],
  "long_silence_intervals": [],
  "long_silence_threshold_seconds": 10,
  "replies": {
    "counterpart": {
      "no_response_intervals": [
        {
          "after_seconds": 16.030666666666665,
          "gap_ms": 700.0
        },
        {
          "after_seconds": 20.310666666666666,
          "gap_ms": 480.0
        },
        {
          "after_seconds": 21.950666666666667,
          "gap_ms": 420.0
        },
        {
          "after_seconds": 23.950666666666667,
          "gap_ms": 500.0
        },
        {
          "after_seconds": 26.110666666666667,
          "gap_ms": 540.0
        },
        {
          "after_seconds": 46.230666666666664,
          "gap_ms": 300.0
        },
        {
          "after_seconds": 63.25066666666667,
          "gap_ms": 340.0
        },
        {
          "after_seconds": 64.21066666666667,
          "gap_ms": 360.0
        },
        {
          "after_seconds": 65.03066666666666,
          "gap_ms": 5156.0
        }
      ],
      "response_gaps": [
        {
          "after_seconds": 2.3706666666666667,
          "gap_ms": 1856.0
        },
        {
          "after_seconds": 27.630666666666666,
          "gap_ms": 3836.0
        },
        {
          "after_seconds": 47.830666666666666,
          "gap_ms": 2776.0
        }
      ]
    },
    "target": {
      "no_response_intervals": [
        {
          "after_seconds": 6.206666666666667,
          "gap_ms": 640.0
        },
        {
          "after_seconds": 35.986666666666665,
          "gap_ms": 340.0
        },
        {
          "after_seconds": 37.82666666666667,
          "gap_ms": 580.0
        },
        {
          "after_seconds": 39.906666666666666,
          "gap_ms": 400.0
        },
        {
          "after_seconds": 42.50666666666667,
          "gap_ms": 480.0
        },
        {
          "after_seconds": 52.026666666666664,
          "gap_ms": 440.0
        },
        {
          "after_seconds": 53.24666666666667,
          "gap_ms": 320.0
        },
        {
          "after_seconds": 55.526666666666664,
          "gap_ms": 520.0
        },
        {
          "after_seconds": 56.906666666666666,
          "gap_ms": 660.0
        }
      ],
      "response_gaps": [
        {
          "after_seconds": 8.866666666666667,
          "gap_ms": 2584.0
        },
        {
          "after_seconds": 43.86666666666667,
          "gap_ms": 2024.0
        },
        {
          "after_seconds": 58.806666666666665,
          "gap_ms": 3104.0
        }
      ]
    }
  },
  "rms_threshold": 500,
  "speaker_activity": {
    "counterpart": [
      [
        4.226666666666667,
        6.206666666666667
      ],
      [
        6.846666666666667,
        8.866666666666667
      ],
      [
        31.466666666666665,
        35.986666666666665
      ],
      [
        36.32666666666667,
        37.82666666666667
      ],
      [
        38.406666666666666,
        39.906666666666666
      ],
      [
        40.306666666666665,
        42.50666666666667
      ],
      [
        42.986666666666665,
        43.86666666666667
      ],
      [
        50.60666666666667,
        52.026666666666664
      ],
      [
        52.46666666666667,
        53.24666666666667
      ],
      [
        53.56666666666667,
        55.526666666666664
      ],
      [
        56.04666666666667,
        56.906666666666666
      ],
      [
        57.56666666666667,
        58.806666666666665
      ]
    ],
    "target": [
      [
        1.6506666666666667,
        2.3706666666666667
      ],
      [
        11.450666666666667,
        16.030666666666665
      ],
      [
        16.730666666666668,
        20.310666666666666
      ],
      [
        20.790666666666667,
        21.950666666666667
      ],
      [
        22.370666666666665,
        23.950666666666667
      ],
      [
        24.450666666666667,
        26.110666666666667
      ],
      [
        26.650666666666666,
        27.630666666666666
      ],
      [
        45.89066666666667,
        46.230666666666664
      ],
      [
        46.53066666666667,
        47.830666666666666
      ],
      [
        61.910666666666664,
        63.25066666666667
      ],
      [
        63.590666666666664,
        64.21066666666667
      ],
      [
        64.57066666666667,
        65.03066666666666
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
        "item_id": "item_EQgLZkLH05vDPlO2xDA2j",
        "largest_gap_ms": 0.0
      },
      {
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "item_id": "item_EQgM0zmNflCKzPQAOAPfv",
        "largest_gap_ms": 0.0
      },
      {
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "item_id": "item_EQgMKEPjNrgJgL6ZQjYne",
        "largest_gap_ms": 0.0
      }
    ],
    "max_bridge_delivery_delay_ms": 69.60000002384186,
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
    "confidence": 0.35,
    "probabilities": {
      "met": 0.52,
      "not_applicable": 0.02,
      "not_met": 0.37,
      "uncertain": 0.09
    },
    "type": "choice"
  },
  "constraint_behavior": {
    "choice": "not_met",
    "confidence": 0.42,
    "probabilities": {
      "met": 0.25,
      "not_met": 0.62,
      "uncertain": 0.13
    },
    "type": "choice"
  },
  "context_retention": {
    "choice": "not_met",
    "confidence": 0.32,
    "probabilities": {
      "met": 0.28,
      "not_met": 0.55,
      "uncertain": 0.17
    },
    "type": "choice"
  },
  "conversation_progress": {
    "choice": "not_met",
    "confidence": 0.22,
    "probabilities": {
      "met": 0.39,
      "not_met": 0.49,
      "uncertain": 0.12
    },
    "type": "choice"
  },
  "counterpart_validity": {
    "choice": "not_met",
    "confidence": 0.24,
    "probabilities": {
      "met": 0.34,
      "not_met": 0.49,
      "uncertain": 0.17
    },
    "type": "choice"
  },
  "question_relevance": {
    "choice": "not_met",
    "confidence": 0.35,
    "probabilities": {
      "met": 0.27,
      "not_met": 0.5599999999999999,
      "uncertain": 0.17
    },
    "type": "choice"
  },
  "target_role_fidelity": {
    "choice": "not_met",
    "confidence": 0.26,
    "probabilities": {
      "met": 0.31,
      "not_met": 0.51,
      "uncertain": 0.18
    },
    "type": "choice"
  },
  "user_report_accuracy": {
    "choice": "met",
    "confidence": 0.37,
    "probabilities": {
      "met": 0.52,
      "not_applicable": 0.01,
      "not_met": 0.37,
      "uncertain": 0.1
    },
    "type": "choice"
  }
}
```

Jev is an independent comparison and cannot override verified business records.
All attempts and incomplete stages remain in the batch counts.