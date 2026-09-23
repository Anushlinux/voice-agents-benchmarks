# Conversation and benchmark result

Automated outcome: **passed**. Simulation validity: **valid**.

Full evaluation: **completed**. Conversation repair accepted: **True**.

Human listening is pending. Text judges cannot establish acoustic naturalness or prove that suspected self-talk was audible.

Book an indoor table for three at Neem Courtyard in Aundh on October 2, 2026 at 7:30 p.m., under Aditi Shah. We want to sit together. Please make a table reservation only, with no booking charge, deposit or cancellation fee. Let me know the booking details and reference, or tell me if it cannot be arranged. Speak naturally in Hinglish.

[Independent transcript](transcript.md) · All metrics and raw judge answers (`details.json` is not included in this published export) · [Failure evidence and uncertainty](diagnostics-v1.json) · [Timing, WER and endpointing availability](measurements-v2.json) · [Per-turn timestamps](turn-timestamps.csv)

Observed task completion: **completed**. Established failure owner: **unknown**. Missing required outputs remain visible even when their cause is unknown.

Left audio: restaurant employee. Right audio: received Rumik.

[Full conversation recording](conversation.mp3)

## Turn timestamps

Times below use the browser audio clock. Each row is an employee playback item, not a human-annotated semantic turn. First speech is estimated from 20 ms audio windows. First token is the arrival of Rumik's first text packet (`bot-llm-text`) at the browser after that speech ended; it includes network transit and is an upper bound on hosted generation latency.

| Turn | Employee speech end (s) | First Rumik token (s) | TTFT (ms) | First Rumik speech (s) | TTFS (ms) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 9.652 | 11.024 | 1372.000 | 11.869 | 2217.333 | answered |
| 2 | 25.092 | 26.261 | 1169.333 | 27.309 | 2217.333 | answered |
| 3 | 55.732 | 56.784 | 1052.000 | 58.069 | 2337.333 | answered |
| 4 | 65.272 | 66.613 | 1341.333 | 67.809 | 2537.333 | answered |
| 5 | 79.932 | 82.795 | 2862.667 | 83.949 | 4017.333 | answered |
| 6 | 99.172 | 101.275 | 2102.667 | 102.329 | 3157.333 | answered |
| 7 | 118.932 | — | — | 121.229 | 2297.333 | answered |
| 8 | 135.492 | — | — | 138.189 | 2697.333 | answered |

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
| consent_alignment | met | The caller gives affirmative booking consent in context after discussing the requested reservation terms, and the employee records the matching reservation. |
| constraint_behavior | met | Rumik communicates the requested date, time, party size, indoor regular table and table-only/no-charge terms, and does not agree to a deposit, fee, meal purchase or other unauthorized extra. |
| context_retention | met | Rumik supplies the requested party size, date/time and seating information, then provides the booking name without an unjustified repetition loop. The later reference correction attempts are responsive to the reference discussion. |
| conversation_progress | met | The exchange progresses from the reservation request to availability, consent, booking name, reservation completion and reference handling. The reference clarification does not constitute an unjustified agreement or question loop. |
| counterpart_validity | met | The employee gives the available matching option, states that the reservation is free and meals are separately ordered and paid for, seeks booking confirmation, records the reservation only after the exchange, and provides the issued reference. The tool results confirm one valid booking with no deposit, cancellation fee or mandatory extras. |
| hinglish_quality | uncertain | This rubric requires human listening for intelligibility and naturalness; the supplied transcription alone cannot establish that standard. |
| question_relevance | met | Rumik asks for availability of the requested table and supplies the booking name; its substantive questions and answers are relevant to completing the reservation. |
| target_output_integrity | uncertain | The transcript shows task-directed conversation and no clear internal self-talk, but this diagnostic explicitly requires verification against the captured audio rather than transcription alone. |
| target_role_fidelity | met | Rumik acts as the caller's booking assistant: it requests the table, supplies the party and seating details, gives the booking name, and participates in the reservation exchange rather than offering restaurant services. |
| user_report_accuracy | met | The latest accepted private report accurately states the booked date, time, party size, indoor regular table, booking name, zero reservation charge and the issued reference. Its reference formatting preserves the single issued identifier SIM-985180 under the supplied normalization, and the booking record matches it. |

## Private report

Booked indoor regular table for 3 on 2026-10-02 at 19:30 under name Aditi Shah, no reservation charge, reference SIM-98-5180.

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
        8103,
        8456,
        8733,
        9059
      ],
      "observation_boundary": "browser_render_and_received_audio",
      "observed_through_sequence": 9165,
      "readback_item_id": "item_EQgnAHMaCxReJFwI2hJNP",
      "semantic_confirmation": "requires_human_review"
    },
    "date": "2026-10-02",
    "deposit_inr": 0,
    "inclusions": [
      "One indoor table for the whole party; meals chosen and paid for separately at the visit."
    ],
    "mandatory_extras": [],
    "menu": null,
    "offer_id": "offer-call_guuwYw134Xxgdajs",
    "operation_id": "call_dv3sHoZPGScVACBc",
    "option_id": "01-aundh-1930",
    "party_size": 3,
    "pricing": {
      "currency": "INR",
      "meal_payment": "Meals are ordered and paid for separately at the visit. Their bill is not known yet; zero reservation charge does not mean free food.",
      "meal_total_inr": null,
      "reservation_charge_inr": 0,
      "total_scope": "reservation_only"
    },
    "reference": "SIM-985180",
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
    1.7493333333333334,
    139.84933333333333
  ],
  "long_silence_intervals": [],
  "long_silence_threshold_seconds": 10,
  "replies": {
    "counterpart": {
      "no_response_intervals": [
        {
          "after_seconds": 30.269333333333332,
          "gap_ms": 560.0
        },
        {
          "after_seconds": 32.409333333333336,
          "gap_ms": 400.0
        },
        {
          "after_seconds": 89.06933333333333,
          "gap_ms": 500.0
        },
        {
          "after_seconds": 107.50933333333333,
          "gap_ms": 420.0
        },
        {
          "after_seconds": 138.62933333333334,
          "gap_ms": 1220.0
        }
      ],
      "response_gaps": [
        {
          "after_seconds": 3.1493333333333333,
          "gap_ms": 2302.667
        },
        {
          "after_seconds": 13.549333333333333,
          "gap_ms": 5382.667
        },
        {
          "after_seconds": 36.06933333333333,
          "gap_ms": 3962.667
        },
        {
          "after_seconds": 60.989333333333335,
          "gap_ms": 1922.667
        },
        {
          "after_seconds": 70.32933333333334,
          "gap_ms": 2822.667
        },
        {
          "after_seconds": 90.68933333333334,
          "gap_ms": 2422.667
        },
        {
          "after_seconds": 109.16933333333333,
          "gap_ms": 2362.667
        },
        {
          "after_seconds": 126.54933333333334,
          "gap_ms": 2102.667
        }
      ]
    },
    "target": {
      "no_response_intervals": [
        {
          "after_seconds": 5.992,
          "gap_ms": 440.0
        },
        {
          "after_seconds": 8.592,
          "gap_ms": 400.0
        },
        {
          "after_seconds": 20.152,
          "gap_ms": 500.0
        },
        {
          "after_seconds": 23.132,
          "gap_ms": 360.0
        },
        {
          "after_seconds": 41.312,
          "gap_ms": 380.0
        },
        {
          "after_seconds": 44.392,
          "gap_ms": 400.0
        },
        {
          "after_seconds": 45.992,
          "gap_ms": 380.0
        },
        {
          "after_seconds": 47.752,
          "gap_ms": 440.0
        },
        {
          "after_seconds": 48.892,
          "gap_ms": 520.0
        },
        {
          "after_seconds": 53.392,
          "gap_ms": 660.0
        },
        {
          "after_seconds": 63.312,
          "gap_ms": 480.0
        },
        {
          "after_seconds": 74.772,
          "gap_ms": 480.0
        },
        {
          "after_seconds": 78.132,
          "gap_ms": 500.0
        },
        {
          "after_seconds": 94.192,
          "gap_ms": 440.0
        },
        {
          "after_seconds": 97.392,
          "gap_ms": 480.0
        },
        {
          "after_seconds": 112.952,
          "gap_ms": 560.0
        },
        {
          "after_seconds": 116.412,
          "gap_ms": 700.0
        },
        {
          "after_seconds": 131.432,
          "gap_ms": 480.0
        },
        {
          "after_seconds": 133.492,
          "gap_ms": 520.0
        }
      ],
      "response_gaps": [
        {
          "after_seconds": 9.652,
          "gap_ms": 2217.333
        },
        {
          "after_seconds": 25.092,
          "gap_ms": 2217.333
        },
        {
          "after_seconds": 55.732,
          "gap_ms": 2337.333
        },
        {
          "after_seconds": 65.272,
          "gap_ms": 2537.333
        },
        {
          "after_seconds": 79.932,
          "gap_ms": 4017.333
        },
        {
          "after_seconds": 99.172,
          "gap_ms": 3157.333
        },
        {
          "after_seconds": 118.932,
          "gap_ms": 2297.333
        },
        {
          "after_seconds": 135.492,
          "gap_ms": 2697.333
        }
      ]
    }
  },
  "rms_threshold": 500,
  "speaker_activity": {
    "counterpart": [
      [
        5.452,
        5.992
      ],
      [
        6.432,
        8.592
      ],
      [
        8.992,
        9.652
      ],
      [
        18.932,
        20.152
      ],
      [
        20.652,
        23.132
      ],
      [
        23.492,
        25.092
      ],
      [
        40.032,
        41.312
      ],
      [
        41.692,
        44.392
      ],
      [
        44.792,
        45.992
      ],
      [
        46.372,
        47.752
      ],
      [
        48.192,
        48.892
      ],
      [
        49.412,
        53.392
      ],
      [
        54.052,
        55.732
      ],
      [
        62.912,
        63.312
      ],
      [
        63.792,
        65.272
      ],
      [
        73.152,
        74.772
      ],
      [
        75.252,
        78.132
      ],
      [
        78.632,
        79.932
      ],
      [
        93.112,
        94.192
      ],
      [
        94.632,
        97.392
      ],
      [
        97.872,
        99.172
      ],
      [
        111.532,
        112.952
      ],
      [
        113.512,
        116.412
      ],
      [
        117.112,
        118.932
      ],
      [
        128.652,
        131.432
      ],
      [
        131.912,
        133.492
      ],
      [
        134.012,
        135.492
      ]
    ],
    "target": [
      [
        2.6893333333333334,
        3.1493333333333333
      ],
      [
        11.869333333333334,
        13.549333333333333
      ],
      [
        27.309333333333335,
        30.269333333333332
      ],
      [
        30.829333333333334,
        32.409333333333336
      ],
      [
        32.809333333333335,
        36.06933333333333
      ],
      [
        58.06933333333333,
        60.989333333333335
      ],
      [
        67.80933333333333,
        70.32933333333334
      ],
      [
        83.94933333333333,
        89.06933333333333
      ],
      [
        89.56933333333333,
        90.68933333333334
      ],
      [
        102.32933333333334,
        107.50933333333333
      ],
      [
        107.92933333333333,
        109.16933333333333
      ],
      [
        121.22933333333333,
        126.54933333333334
      ],
      [
        138.18933333333334,
        138.62933333333334
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
        "inserted_silence_ms": 28.021,
        "item_id": "item_EQgmEfg1sukOq9heNce7k",
        "largest_gap_ms": 28.021
      },
      {
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "item_id": "item_EQgmSU32OEsKGlo1PgDq2",
        "largest_gap_ms": 0.0
      },
      {
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "item_id": "item_EQgmoUZcyNtkHpuPgPwc8",
        "largest_gap_ms": 0.0
      },
      {
        "gap_count": 1,
        "inserted_silence_ms": 28.0,
        "item_id": "item_EQgnAHMaCxReJFwI2hJNP",
        "largest_gap_ms": 28.0
      },
      {
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "item_id": "item_EQgnL9RpoPshXKoyc40nJ",
        "largest_gap_ms": 0.0
      },
      {
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "item_id": "item_EQgneXI99XoDByAjbC6Cg",
        "largest_gap_ms": 0.0
      },
      {
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "item_id": "item_EQgnxegtyUfjT2CBSMLfJ",
        "largest_gap_ms": 0.0
      },
      {
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "item_id": "item_EQgoElX0TmIqitLBWJv2F",
        "largest_gap_ms": 0.0
      }
    ],
    "max_bridge_delivery_delay_ms": 128,
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
    "confidence": 0.66,
    "probabilities": {
      "met": 0.74,
      "not_applicable": 0.01,
      "not_met": 0.12,
      "uncertain": 0.13
    },
    "type": "choice"
  },
  "constraint_behavior": {
    "choice": "met",
    "confidence": 0.21,
    "probabilities": {
      "met": 0.47,
      "not_met": 0.32,
      "uncertain": 0.21
    },
    "type": "choice"
  },
  "context_retention": {
    "choice": "met",
    "confidence": 0.31,
    "probabilities": {
      "met": 0.54,
      "not_met": 0.23,
      "uncertain": 0.23
    },
    "type": "choice"
  },
  "conversation_progress": {
    "choice": "met",
    "confidence": 0.26,
    "probabilities": {
      "met": 0.51,
      "not_met": 0.29,
      "uncertain": 0.2
    },
    "type": "choice"
  },
  "counterpart_validity": {
    "choice": "met",
    "confidence": 0.26,
    "probabilities": {
      "met": 0.51,
      "not_met": 0.24,
      "uncertain": 0.25
    },
    "type": "choice"
  },
  "question_relevance": {
    "choice": "met",
    "confidence": 0.23,
    "probabilities": {
      "met": 0.49,
      "not_met": 0.26,
      "uncertain": 0.25
    },
    "type": "choice"
  },
  "target_role_fidelity": {
    "choice": "met",
    "confidence": 0.25,
    "probabilities": {
      "met": 0.5,
      "not_met": 0.27,
      "uncertain": 0.23
    },
    "type": "choice"
  },
  "user_report_accuracy": {
    "choice": "met",
    "confidence": 0.59,
    "probabilities": {
      "met": 0.69,
      "not_applicable": 0.01,
      "not_met": 0.18,
      "uncertain": 0.12
    },
    "type": "choice"
  }
}
```

Jev is an independent comparison and cannot override verified business records.
All attempts and incomplete stages remain in the batch counts.