# Conversation and benchmark result

Automated outcome: **unresolved**. Simulation validity: **invalid**.

Full evaluation: **completed**. Conversation repair accepted: **False**.

Human listening is pending. Text judges cannot establish acoustic naturalness or prove that suspected self-talk was audible.

Reserve dinner for eight at Saffron Terrace in Koregaon Park on October 8, 2026 at 7:30 p.m., under Devika Rao, together at one indoor table. The whole package must be at most ₹13,000 including all charges. A starter and main with rice or bread for each guest is enough. You may confirm a package paid entirely when we visit, but no advance, deposit, cancellation fee or extras. Tell me the chosen package, total and reference. Speak naturally in Hinglish.

[Independent transcript](transcript.md) · [All metrics and raw judge answers](details.json) · [Failure evidence and uncertainty](diagnostics-v1.json) · [Timing, WER and endpointing availability](measurements-v2.json) · [Per-turn timestamps](turn-timestamps.csv)

Observed task completion: **unresolved**. Established failure owner: **unknown**. Missing required outputs remain visible even when their cause is unknown.

Left audio: restaurant employee. Right audio: received Rumik.

[Full conversation recording](conversation.mp3)

## Turn timestamps

Times below use the browser audio clock. Each row is an employee playback item, not a human-annotated semantic turn. First speech is estimated from 20 ms audio windows. First token is the arrival of Rumik's first text packet (`bot-llm-text`) at the browser after that speech ended; it includes network transit and is an upper bound on hosted generation latency.

| Turn | Employee speech end (s) | First Rumik token (s) | TTFT (ms) | First Rumik speech (s) | TTFS (ms) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 8.207 | 9.483 | 1276.000 | 10.391 | 2184.000 | answered |
| 2 | 50.647 | — | — | — | — | no_observed_reply |
| 3 | 67.427 | 70.597 | 3170.667 | 71.811 | 4384.000 | answered |
| 4 | 87.467 | 88.752 | 1285.333 | 89.811 | 2344.000 | answered |
| 5 | 104.087 | 107.392 | 3305.333 | 108.511 | 4424.000 | answered |
| 6 | 122.467 | — | — | — | — | no_observed_reply |
| 7 | 137.467 | 139.440 | 1973.333 | 140.531 | 3064.000 | answered |

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
| consent_alignment | not_met | The simple menu was presented with its material terms, but Rumik never clearly agreed to that option. Its subsequent statement gave or acknowledged a reference rather than consenting to the changed package. |
| constraint_behavior | met | Rumik stated the required date, party size, branch, indoor table, package inclusions, budget and booking name, and explicitly rejected the ₹2,000 advance as unauthorized. It did not verbally authorize a deposit, fee or extra. |
| context_retention | met | Rumik retained and communicated the core reservation facts and the prohibition on advance payment. There is no clear unjustified repetition of settled requirements. |
| conversation_progress | not_met | After the employee offered the no-deposit simple menu, Rumik did not provide a clear decision about that offer; its captured response instead referred to a reference. The employee nevertheless proceeded to booking, so the target-side exchange did not establish a valid decision path. |
| counterpart_validity | not_met | The employee correctly disclosed that the promotional option required a ₹2,000 advance and correctly described the simple menu as ₹12,400 with no advance. However, after asking whether the caller wanted the simple menu, the employee recorded the reservation without clear caller consent; the target's captured response was a reference statement, not agreement to book. |
| hinglish_quality | uncertain | The supplied transcript shows Hindi-English code-switching, but this rubric requires human listening for understandability and naturalness; text and transcription alone cannot establish it. |
| question_relevance | met | Rumik's captured request was relevant to making the reservation, and its reference-related statement is relevant to the reservation exchange. No unrelated target question or answer is shown. |
| target_output_integrity | uncertain | The transcript contains customer-facing reservation speech and does not show internal turn-management instructions, but this diagnostic requires verification against captured audio rather than transcription alone. |
| target_role_fidelity | met | Rumik acted as the customer's assistant: it presented the reservation request, communicated the user's restrictions, challenged the unauthorized advance, and discussed the reference. It did not offer restaurant services as the employee. |
| user_report_accuracy | met | The latest authenticated report accurately states the committed booking's date, time, name, party size, indoor regular table, INR 12,400 total, required inclusions, and the issued reference SIM-673238. The earlier no-booking report was superseded and is not the delivered outcome. |

## Private report

Booked: 8 Oct 2026 19:30, Devika Rao, 8 persons, indoor regular table, total INR 12400, includes starter, main, rice/bread each, reference SIM-673238.

## Business outcome

```json
[
  {
    "booking_kind": "dining_package",
    "booking_name": "Devika Rao",
    "branch": "Koregaon Park",
    "cancellation_fee_inr": 0,
    "consent_evidence": {
      "audio_artifacts": [
        "audio/played.wav",
        "audio/received.wav"
      ],
      "event_sequences": [
        9799,
        10803,
        11065,
        11460
      ],
      "observation_boundary": "browser_render_and_received_audio",
      "observed_through_sequence": 11682,
      "readback_item_id": "item_EQgtngRZLZzMH6PKVkZfp",
      "semantic_confirmation": "requires_human_review"
    },
    "date": "2026-10-08",
    "deposit_inr": 0,
    "inclusions": [
      "starter_each",
      "main_each",
      "rice_or_bread_each"
    ],
    "mandatory_extras": [],
    "menu": "Simple menu",
    "offer_id": "offer-call_9uPjAK75n6PXpw5a",
    "operation_id": "call_cJ4pShsBQSbnsGr2",
    "option_id": "07-simple",
    "party_size": 8,
    "pricing": {
      "currency": "INR",
      "meal_payment": "The total is for the listed dining package and inclusions only.",
      "meal_total_inr": 12400,
      "reservation_charge_inr": null,
      "total_scope": "dining_package"
    },
    "reference": "SIM-673238",
    "remaining_due_inr": 12400,
    "seating": "indoor_regular_table",
    "table_capacity": 8,
    "table_count": 1,
    "time": "19:30",
    "timezone": "Asia/Kolkata",
    "total_inr": 12400,
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
    1.6906666666666668,
    143.01066666666668
  ],
  "long_silence_intervals": [
    {
      "attribution": "unknown",
      "duration_seconds": 10.879999999999995,
      "end_seconds": 61.526666666666664,
      "start_seconds": 50.64666666666667
    },
    {
      "attribution": "unknown",
      "duration_seconds": 11.159999999999997,
      "end_seconds": 133.62666666666667,
      "start_seconds": 122.46666666666667
    }
  ],
  "long_silence_threshold_seconds": 10,
  "replies": {
    "counterpart": {
      "no_response_intervals": [
        {
          "after_seconds": 16.930666666666667,
          "gap_ms": 620.0
        },
        {
          "after_seconds": 21.110666666666667,
          "gap_ms": 460.0
        },
        {
          "after_seconds": 23.110666666666667,
          "gap_ms": 540.0
        },
        {
          "after_seconds": 25.750666666666667,
          "gap_ms": 460.0
        },
        {
          "after_seconds": 75.61066666666666,
          "gap_ms": 420.0
        },
        {
          "after_seconds": 108.83066666666667,
          "gap_ms": 460.0
        },
        {
          "after_seconds": 113.33066666666667,
          "gap_ms": 380.0
        },
        {
          "after_seconds": 142.19066666666666,
          "gap_ms": 820.0
        }
      ],
      "response_gaps": [
        {
          "after_seconds": 3.3106666666666666,
          "gap_ms": 1756.0
        },
        {
          "after_seconds": 27.410666666666668,
          "gap_ms": 8756.0
        },
        {
          "after_seconds": 78.25066666666666,
          "gap_ms": 1876.0
        },
        {
          "after_seconds": 92.95066666666666,
          "gap_ms": 4056.0
        },
        {
          "after_seconds": 114.35066666666667,
          "gap_ms": 2036.0
        }
      ]
    },
    "target": {
      "no_response_intervals": [
        {
          "after_seconds": 5.506666666666667,
          "gap_ms": 680.0
        },
        {
          "after_seconds": 36.846666666666664,
          "gap_ms": 480.0
        },
        {
          "after_seconds": 39.166666666666664,
          "gap_ms": 360.0
        },
        {
          "after_seconds": 40.586666666666666,
          "gap_ms": 320.0
        },
        {
          "after_seconds": 43.666666666666664,
          "gap_ms": 500.0
        },
        {
          "after_seconds": 45.82666666666667,
          "gap_ms": 420.0
        },
        {
          "after_seconds": 48.42666666666667,
          "gap_ms": 700.0
        },
        {
          "after_seconds": 50.64666666666667,
          "gap_ms": 10880.0
        },
        {
          "after_seconds": 61.88666666666666,
          "gap_ms": 500.0
        },
        {
          "after_seconds": 63.96666666666667,
          "gap_ms": 560.0
        },
        {
          "after_seconds": 80.58666666666667,
          "gap_ms": 540.0
        },
        {
          "after_seconds": 83.48666666666666,
          "gap_ms": 340.0
        },
        {
          "after_seconds": 85.64666666666666,
          "gap_ms": 300.0
        },
        {
          "after_seconds": 98.50666666666666,
          "gap_ms": 440.0
        },
        {
          "after_seconds": 101.76666666666667,
          "gap_ms": 640.0
        },
        {
          "after_seconds": 117.08666666666667,
          "gap_ms": 640.0
        },
        {
          "after_seconds": 119.92666666666666,
          "gap_ms": 300.0
        },
        {
          "after_seconds": 121.22666666666667,
          "gap_ms": 620.0
        },
        {
          "after_seconds": 122.46666666666667,
          "gap_ms": 11160.0
        },
        {
          "after_seconds": 133.90666666666667,
          "gap_ms": 480.0
        },
        {
          "after_seconds": 135.98666666666668,
          "gap_ms": 400.0
        }
      ],
      "response_gaps": [
        {
          "after_seconds": 8.206666666666667,
          "gap_ms": 2184.0
        },
        {
          "after_seconds": 67.42666666666666,
          "gap_ms": 4384.0
        },
        {
          "after_seconds": 87.46666666666667,
          "gap_ms": 2344.0
        },
        {
          "after_seconds": 104.08666666666667,
          "gap_ms": 4424.0
        },
        {
          "after_seconds": 137.46666666666667,
          "gap_ms": 3064.0
        }
      ]
    }
  },
  "rms_threshold": 500,
  "speaker_activity": {
    "counterpart": [
      [
        5.066666666666666,
        5.506666666666667
      ],
      [
        6.1866666666666665,
        8.206666666666667
      ],
      [
        36.166666666666664,
        36.846666666666664
      ],
      [
        37.32666666666667,
        39.166666666666664
      ],
      [
        39.526666666666664,
        40.586666666666666
      ],
      [
        40.906666666666666,
        43.666666666666664
      ],
      [
        44.166666666666664,
        45.82666666666667
      ],
      [
        46.24666666666667,
        48.42666666666667
      ],
      [
        49.126666666666665,
        50.64666666666667
      ],
      [
        61.526666666666664,
        61.88666666666666
      ],
      [
        62.38666666666666,
        63.96666666666667
      ],
      [
        64.52666666666667,
        67.42666666666666
      ],
      [
        80.12666666666667,
        80.58666666666667
      ],
      [
        81.12666666666667,
        83.48666666666666
      ],
      [
        83.82666666666667,
        85.64666666666666
      ],
      [
        85.94666666666667,
        87.46666666666667
      ],
      [
        97.00666666666666,
        98.50666666666666
      ],
      [
        98.94666666666667,
        101.76666666666667
      ],
      [
        102.40666666666667,
        104.08666666666667
      ],
      [
        116.38666666666667,
        117.08666666666667
      ],
      [
        117.72666666666667,
        119.92666666666666
      ],
      [
        120.22666666666667,
        121.22666666666667
      ],
      [
        121.84666666666666,
        122.46666666666667
      ],
      [
        133.62666666666667,
        133.90666666666667
      ],
      [
        134.38666666666666,
        135.98666666666668
      ],
      [
        136.38666666666666,
        137.46666666666667
      ]
    ],
    "target": [
      [
        2.6906666666666665,
        3.3106666666666666
      ],
      [
        10.390666666666666,
        16.930666666666667
      ],
      [
        17.550666666666668,
        21.110666666666667
      ],
      [
        21.570666666666668,
        23.110666666666667
      ],
      [
        23.650666666666666,
        25.750666666666667
      ],
      [
        26.21066666666667,
        27.410666666666668
      ],
      [
        71.81066666666666,
        75.61066666666666
      ],
      [
        76.03066666666666,
        78.25066666666666
      ],
      [
        89.81066666666666,
        92.95066666666666
      ],
      [
        108.51066666666667,
        108.83066666666667
      ],
      [
        109.29066666666667,
        113.33066666666667
      ],
      [
        113.71066666666667,
        114.35066666666667
      ],
      [
        140.53066666666666,
        142.19066666666666
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
        "gap_count": 1,
        "inserted_silence_ms": 1.354,
        "item_id": "item_EQgsa4RFBIEYD778RVXrx",
        "largest_gap_ms": 1.354
      },
      {
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "item_id": "item_EQgt581fyeM7TTgNiEzO7",
        "largest_gap_ms": 0.0
      },
      {
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "item_id": "item_EQgtVCQy9RBf6vza8eqPd",
        "largest_gap_ms": 0.0
      },
      {
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "item_id": "item_EQgtngRZLZzMH6PKVkZfp",
        "largest_gap_ms": 0.0
      },
      {
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "item_id": "item_EQgu4aNQPZbXeps7vJe4X",
        "largest_gap_ms": 0.0
      },
      {
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "item_id": "item_EQguONKGBFZkrERdBmgEk",
        "largest_gap_ms": 0.0
      },
      {
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "item_id": "item_EQgufLSEOaQhLC4oPRWP6",
        "largest_gap_ms": 0.0
      }
    ],
    "max_bridge_delivery_delay_ms": 68.39999997615814,
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
    "confidence": 0.64,
    "probabilities": {
      "met": 0.73,
      "not_applicable": 0.03,
      "not_met": 0.15,
      "uncertain": 0.09
    },
    "type": "choice"
  },
  "constraint_behavior": {
    "choice": "met",
    "confidence": 0.26,
    "probabilities": {
      "met": 0.51,
      "not_met": 0.3,
      "uncertain": 0.19
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
    "confidence": 0.26,
    "probabilities": {
      "met": 0.51,
      "not_met": 0.3,
      "uncertain": 0.19
    },
    "type": "choice"
  },
  "counterpart_validity": {
    "choice": "met",
    "confidence": 0.22,
    "probabilities": {
      "met": 0.48,
      "not_met": 0.32,
      "uncertain": 0.2
    },
    "type": "choice"
  },
  "question_relevance": {
    "choice": "met",
    "confidence": 0.19,
    "probabilities": {
      "met": 0.46,
      "not_met": 0.31,
      "uncertain": 0.23
    },
    "type": "choice"
  },
  "target_role_fidelity": {
    "choice": "met",
    "confidence": 0.25,
    "probabilities": {
      "met": 0.5,
      "not_met": 0.28,
      "uncertain": 0.22
    },
    "type": "choice"
  },
  "user_report_accuracy": {
    "choice": "met",
    "confidence": 0.61,
    "probabilities": {
      "met": 0.7,
      "not_applicable": 0.01,
      "not_met": 0.19,
      "uncertain": 0.1
    },
    "type": "choice"
  }
}
```

Jev is an independent comparison and cannot override verified business records.
All attempts and incomplete stages remain in the batch counts.