# Conversation and benchmark result

Automated outcome: **unresolved**. Simulation validity: **unresolved**.

Full evaluation: **completed**. Conversation repair accepted: **False**.

Human listening is pending. Text judges cannot establish acoustic naturalness or prove that suspected self-talk was audible.

Reserve one indoor table for two at Banyan Kitchen in Adyar on October 4, 2026, under Meera Iyer. Around 7 p.m. would work; any time from 6:45 to 7:30 is equally fine. Please arrange a free table booking, with no deposit or cancellation fee. Tell me the final time and booking reference. Speak naturally in Hinglish.

[Independent transcript](transcript.md) · All metrics and raw judge answers (`details.json` is not included in this published export) · [Failure evidence and uncertainty](diagnostics-v1.json) · [Timing, WER and endpointing availability](measurements-v2.json) · [Per-turn timestamps](turn-timestamps.csv)

Observed task completion: **unresolved**. Established failure owner: **unknown**. Missing required outputs remain visible even when their cause is unknown.

Left audio: restaurant employee. Right audio: received Rumik.

[Full conversation recording](conversation.mp3)

## Turn timestamps

Times below use the browser audio clock. Each row is an employee playback item, not a human-annotated semantic turn. First speech is estimated from 20 ms audio windows. First token is the arrival of Rumik's first text packet (`bot-llm-text`) at the browser after that speech ended; it includes network transit and is an upper bound on hosted generation latency.

| Turn | Employee speech end (s) | First Rumik token (s) | TTFT (ms) | First Rumik speech (s) | TTFS (ms) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 8.447 | 9.803 | 1356.000 | 10.403 | 1956.000 | answered |
| 2 | 40.067 | 41.205 | 1138.667 | 41.903 | 1836.000 | answered |
| 3 | 59.347 | 60.384 | 1037.333 | 61.263 | 1916.000 | answered |
| 4 | 81.147 | 83.429 | 2282.667 | 84.343 | 3196.000 | answered |

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
| user_report_references | not_met | Compared only explicitly labelled target report references using explicit-reference-clauses-v2. Distinct codes remain distinct. A match checks identifiers only, not overall report accuracy; unsupported prose requires review. |
| user_report_presence | met | Checked authenticated report receipt. Confirmed absence is separate from false content; a missing report does not establish which actor caused an interrupted call. |
| consent_alignment | uncertain | Unsupported judge claim: A claimed quotation does not occur in its cited transcription window. The original judgment is retained in judge-response.json. |
| constraint_behavior | met | The caller stated the required branch, date, party size, indoor regular table, flexible 18:45–19:30 window, table-only booking, and no charge or deposit. Nothing in the caller's captured commitments authorizes payment, extras, a different date, party size, or seating. |
| context_retention | met | The caller consistently used the previously supplied booking name, seating requirement, party size, and flexible time window, and did not unnecessarily re-ask settled user requirements. The later time discussion reflected the availability issue rather than a needless repetition of the original assignment. |
| conversation_progress | met | The exchange progressed from the request, through availability alternatives, to a booking and reference delivery without an observable repeated-question loop by the caller. The caller also closed the conversation after the reference exchange. |
| counterpart_validity | uncertain | Unsupported judge claim: A claimed quotation does not occur in its cited transcription window. The original judgment is retained in judge-response.json. |
| hinglish_quality | uncertain | This rubric requires human listening for understandability and naturalness. The supplied transcription alone cannot establish those properties. |
| question_relevance | met | The caller's questions concern availability, time selection, confirmation, and the booking reference, all of which are relevant to the assigned reservation task. The employee's questions likewise seek a time choice and reference acknowledgement. |
| target_output_integrity | uncertain | This is a human-listening rubric requiring verification that the audible output contains no internal instructions or private self-talk. The supplied text does not establish that acoustically. |
| target_role_fidelity | met | The caller acts as a customer assistant requesting a reservation, states the user's booking requirements, responds within the reservation exchange, and closes the call. It does not offer restaurant services or impersonate the employee. |
| user_report_accuracy | not_met | The report correctly states the booking time, seating, party size, date, name, and no charge. However, it reports the reference as SIM-92-691, while the committed reservation issued SIM-929661. The reference identity and grouping were not preserved. |

## Private report

Booked indoor regular table for 2 on 2026-10-04 at 6:45 PM under Meera Iyer, no charge, reference SIM-92-691.

## Business outcome

```json
[
  {
    "booking_kind": "table_only",
    "booking_name": "Meera Iyer",
    "branch": "Adyar",
    "cancellation_fee_inr": 0,
    "consent_evidence": {
      "audio_artifacts": [
        "audio/played.wav",
        "audio/received.wav"
      ],
      "event_sequences": [
        6117,
        7357,
        7617,
        8579
      ],
      "observation_boundary": "browser_render_and_received_audio",
      "observed_through_sequence": 8842,
      "readback_item_id": "item_EQgOFkFZUC3q2daGOvn3w",
      "semantic_confirmation": "requires_human_review"
    },
    "date": "2026-10-04",
    "deposit_inr": 0,
    "inclusions": [
      "One indoor table for the whole party; meals chosen and paid for separately at the visit."
    ],
    "mandatory_extras": [],
    "menu": null,
    "offer_id": "offer-call_tOYmCiP28ApAxIkk",
    "operation_id": "call_Ba914NAp4LJ41EY1",
    "option_id": "03-adyar-1845",
    "party_size": 2,
    "pricing": {
      "currency": "INR",
      "meal_payment": "Meals are ordered and paid for separately at the visit. Their bill is not known yet; zero reservation charge does not mean free food.",
      "meal_total_inr": null,
      "reservation_charge_inr": 0,
      "total_scope": "reservation_only"
    },
    "reference": "SIM-929661",
    "remaining_due_inr": 0,
    "seating": "indoor_regular_table",
    "table_capacity": 2,
    "table_count": 1,
    "time": "18:45",
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
    1.9626666666666666,
    91.14266666666667
  ],
  "long_silence_intervals": [],
  "long_silence_threshold_seconds": 10,
  "replies": {
    "counterpart": {
      "no_response_intervals": [
        {
          "after_seconds": 13.442666666666666,
          "gap_ms": 380.0
        },
        {
          "after_seconds": 15.562666666666667,
          "gap_ms": 420.0
        },
        {
          "after_seconds": 18.24266666666667,
          "gap_ms": 460.0
        },
        {
          "after_seconds": 19.902666666666665,
          "gap_ms": 340.0
        },
        {
          "after_seconds": 23.102666666666668,
          "gap_ms": 320.0
        },
        {
          "after_seconds": 24.102666666666668,
          "gap_ms": 340.0
        },
        {
          "after_seconds": 26.562666666666665,
          "gap_ms": 380.0
        },
        {
          "after_seconds": 43.80266666666667,
          "gap_ms": 440.0
        },
        {
          "after_seconds": 64.48266666666666,
          "gap_ms": 400.0
        },
        {
          "after_seconds": 86.12266666666666,
          "gap_ms": 5020.0
        }
      ],
      "response_gaps": [
        {
          "after_seconds": 3.502666666666667,
          "gap_ms": 1724.0
        },
        {
          "after_seconds": 27.982666666666667,
          "gap_ms": 3044.0
        },
        {
          "after_seconds": 47.72266666666667,
          "gap_ms": 2044.0
        },
        {
          "after_seconds": 70.20266666666667,
          "gap_ms": 4604.0
        }
      ]
    },
    "target": {
      "no_response_intervals": [
        {
          "after_seconds": 5.6866666666666665,
          "gap_ms": 540.0
        },
        {
          "after_seconds": 33.04666666666667,
          "gap_ms": 580.0
        },
        {
          "after_seconds": 38.06666666666667,
          "gap_ms": 540.0
        },
        {
          "after_seconds": 52.906666666666666,
          "gap_ms": 520.0
        },
        {
          "after_seconds": 55.06666666666667,
          "gap_ms": 320.0
        },
        {
          "after_seconds": 57.50666666666667,
          "gap_ms": 600.0
        },
        {
          "after_seconds": 76.54666666666667,
          "gap_ms": 440.0
        },
        {
          "after_seconds": 79.60666666666667,
          "gap_ms": 580.0
        }
      ],
      "response_gaps": [
        {
          "after_seconds": 8.446666666666667,
          "gap_ms": 1956.0
        },
        {
          "after_seconds": 40.06666666666667,
          "gap_ms": 1836.0
        },
        {
          "after_seconds": 59.346666666666664,
          "gap_ms": 1916.0
        },
        {
          "after_seconds": 81.14666666666666,
          "gap_ms": 3196.0
        }
      ]
    }
  },
  "rms_threshold": 500,
  "speaker_activity": {
    "counterpart": [
      [
        5.226666666666667,
        5.6866666666666665
      ],
      [
        6.226666666666667,
        8.446666666666667
      ],
      [
        31.026666666666667,
        33.04666666666667
      ],
      [
        33.626666666666665,
        38.06666666666667
      ],
      [
        38.60666666666667,
        40.06666666666667
      ],
      [
        49.766666666666666,
        52.906666666666666
      ],
      [
        53.42666666666667,
        55.06666666666667
      ],
      [
        55.38666666666666,
        57.50666666666667
      ],
      [
        58.10666666666667,
        59.346666666666664
      ],
      [
        74.80666666666667,
        76.54666666666667
      ],
      [
        76.98666666666666,
        79.60666666666667
      ],
      [
        80.18666666666667,
        81.14666666666666
      ]
    ],
    "target": [
      [
        2.6826666666666665,
        3.502666666666667
      ],
      [
        10.402666666666667,
        13.442666666666666
      ],
      [
        13.822666666666667,
        15.562666666666667
      ],
      [
        15.982666666666667,
        18.24266666666667
      ],
      [
        18.702666666666666,
        19.902666666666665
      ],
      [
        20.24266666666667,
        23.102666666666668
      ],
      [
        23.422666666666668,
        24.102666666666668
      ],
      [
        24.442666666666668,
        26.562666666666665
      ],
      [
        26.942666666666668,
        27.982666666666667
      ],
      [
        41.90266666666667,
        43.80266666666667
      ],
      [
        44.242666666666665,
        47.72266666666667
      ],
      [
        61.26266666666667,
        64.48266666666666
      ],
      [
        64.88266666666667,
        70.20266666666667
      ],
      [
        84.34266666666667,
        86.12266666666666
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
        "item_id": "item_EQgNXgAdX74WglG7Ukf8h",
        "largest_gap_ms": 0.0
      },
      {
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "item_id": "item_EQgNxq1z3ZrAMPdPanmuD",
        "largest_gap_ms": 0.0
      },
      {
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "item_id": "item_EQgOFkFZUC3q2daGOvn3w",
        "largest_gap_ms": 0.0
      },
      {
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "item_id": "item_EQgOfznkky2MfFeKABxLg",
        "largest_gap_ms": 0.0
      }
    ],
    "max_bridge_delivery_delay_ms": 107.19999998807907,
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
    "confidence": 0.38,
    "probabilities": {
      "met": 0.54,
      "not_applicable": 0.02,
      "not_met": 0.29,
      "uncertain": 0.15
    },
    "type": "choice"
  },
  "constraint_behavior": {
    "choice": "not_met",
    "confidence": 0.36,
    "probabilities": {
      "met": 0.24,
      "not_met": 0.57,
      "uncertain": 0.19
    },
    "type": "choice"
  },
  "context_retention": {
    "choice": "not_met",
    "confidence": 0.26,
    "probabilities": {
      "met": 0.26,
      "not_met": 0.51,
      "uncertain": 0.23
    },
    "type": "choice"
  },
  "conversation_progress": {
    "choice": "not_met",
    "confidence": 0.22,
    "probabilities": {
      "met": 0.33,
      "not_met": 0.48,
      "uncertain": 0.19
    },
    "type": "choice"
  },
  "counterpart_validity": {
    "choice": "not_met",
    "confidence": 0.19,
    "probabilities": {
      "met": 0.31,
      "not_met": 0.46,
      "uncertain": 0.23
    },
    "type": "choice"
  },
  "question_relevance": {
    "choice": "not_met",
    "confidence": 0.23,
    "probabilities": {
      "met": 0.26,
      "not_met": 0.49,
      "uncertain": 0.25
    },
    "type": "choice"
  },
  "target_role_fidelity": {
    "choice": "not_met",
    "confidence": 0.2,
    "probabilities": {
      "met": 0.29,
      "not_met": 0.47,
      "uncertain": 0.24
    },
    "type": "choice"
  },
  "user_report_accuracy": {
    "choice": "not_met",
    "confidence": 0.64,
    "probabilities": {
      "met": 0.19,
      "not_applicable": 0.01,
      "not_met": 0.72,
      "uncertain": 0.08
    },
    "type": "choice"
  }
}
```

Jev is an independent comparison and cannot override verified business records.
All attempts and incomplete stages remain in the batch counts.