# Conversation and benchmark result

Automated outcome: **failed**. Simulation validity: **valid**.

Full evaluation: **completed**. Conversation repair accepted: **False**.

Human listening is pending. Text judges cannot establish acoustic naturalness or prove that suspected self-talk was audible.

Arrange dinner for seven at Cedar Dining in Powai on October 7, 2026 at 8 p.m., under Priya Nair, at one indoor table. Keep the total within ₹10,500 including every charge. A smaller menu is fine if everyone gets a starter, a main and rice or bread; dessert is optional. You can agree to pay at the restaurant, but no deposit, cancellation fee or extras. Tell me the menu, total and booking reference. Speak naturally in Hinglish.

[Independent transcript](transcript.md) · All metrics and raw judge answers (`details.json` is not included in this published export) · [Failure evidence and uncertainty](diagnostics-v1.json) · [Timing, WER and endpointing availability](measurements-v2.json) · [Per-turn timestamps](turn-timestamps.csv)

Observed task completion: **unresolved**. Established failure owner: **unknown**. Missing required outputs remain visible even when their cause is unknown.

Left audio: restaurant employee. Right audio: received Rumik.

[Full conversation recording](conversation.mp3)

## Turn timestamps

Times below use the browser audio clock. Each row is an employee playback item, not a human-annotated semantic turn. First speech is estimated from 20 ms audio windows. First token is the arrival of Rumik's first text packet (`bot-llm-text`) at the browser after that speech ended; it includes network transit and is an upper bound on hosted generation latency.

| Turn | Employee speech end (s) | First Rumik token (s) | TTFT (ms) | First Rumik speech (s) | TTFS (ms) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 10.187 | 12.160 | 1973.333 | 12.781 | 2594.667 | answered |
| 2 | 61.367 | 62.459 | 1092.000 | 63.161 | 1794.667 | answered |
| 3 | 78.167 | 80.443 | 2276.000 | 81.241 | 3074.667 | answered |
| 4 | 95.667 | 97.035 | 1368.000 | 97.801 | 2134.667 | answered |
| 5 | 108.967 | 110.160 | 1193.333 | 110.961 | 1994.667 | answered |
| 6 | 127.667 | 129.595 | 1928.000 | 130.301 | 2634.667 | answered |

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
| user_report_references | uncertain | Compared only explicitly labelled target report references using explicit-reference-clauses-v2. Distinct codes remain distinct. A match checks identifiers only, not overall report accuracy; unsupported prose requires review. |
| user_report_presence | met | Checked authenticated report receipt. Confirmed absence is separate from false content; a missing report does not establish which actor caused an interrupted call. |
| consent_alignment | met | Rumik clearly agreed to the offered compact-menu terms and explicitly requested booking. The terms had already been stated by the counterpart, so a full recital was unnecessary. |
| constraint_behavior | met | Rumik communicated and accepted the requested date, party size, Powai branch, indoor table, dining-package inclusions, and INR 10,500 ceiling. The committed booking terms stayed within the authorized constraints; no deposit, cancellation fee, payment, or extras were agreed to. |
| context_retention | met | Rumik retained the core request and gave affirmative booking consent after the compact-menu terms were provided. The later reference correction reflects an attempted correction rather than failure to retain the reservation details. |
| conversation_progress | met | The exchange progressed from the request to availability, terms, consent, booking, and reference correction. There is no clear repeated-agreement loop; the reference correction was responsive to a misunderstanding. |
| counterpart_validity | met | The employee used the availability, offer, and reservation tools, presented the available compact option at INR 9,800 with the required inclusions, obtained the caller's booking request, and recorded the reservation under Priya Nair. The employee corrected the misunderstood reference rather than inventing a second identifier. |
| hinglish_quality | uncertain | This rubric requires human listening for understandability and natural Hinglish quality. The supplied transcripts alone cannot establish that. |
| question_relevance | not_met | Rumik's initial availability/menu/reference request was relevant, but it later asked the restaurant-side question, “क्या आप preferences बदलना चाहेंगे?”, which did not help complete the assigned customer task and reflects a role-inappropriate turn. |
| target_output_integrity | uncertain | This is a human-listening rubric requiring verification of audible leakage or private self-talk. The transcripts do not establish whether any output was internal turn-management speech. |
| target_role_fidelity | not_met | Rumik initially acted as the customer assistant, but later adopted the employee's role by asking whether the caller wanted to change preferences and by presenting itself as handling reservation confirmation/reference communication rather than consistently responding as the caller. |
| user_report_accuracy | not_met | The report omits the menu and required package inclusions, despite the report rubric requiring material dining terms when relevant. It also reports the reference as Hindi text “सिम 385061” rather than preserving the issued reference identity in its supported form, and it does not state that no deposit, cancellation fee, or mandatory extras apply. The booking itself is otherwise consistent with the committed record. |

## Private report

Reservation for 7 people on 2026-10-07 at 20:00 under Priya Nair, indoor regular table, dining package total INR 9,800, reference सिम 385061.

## Business outcome

```json
[
  {
    "booking_kind": "dining_package",
    "booking_name": "Priya Nair",
    "branch": "Powai",
    "cancellation_fee_inr": 0,
    "consent_evidence": {
      "audio_artifacts": [
        "audio/played.wav",
        "audio/received.wav"
      ],
      "event_sequences": [
        5496,
        7415,
        7604,
        8006
      ],
      "observation_boundary": "browser_render_and_received_audio",
      "observed_through_sequence": 8230,
      "readback_item_id": "item_EQgH8BqpF8SnD3ZBCk5Nk",
      "semantic_confirmation": "requires_human_review"
    },
    "date": "2026-10-07",
    "deposit_inr": 0,
    "inclusions": [
      "starter_each",
      "main_each",
      "rice_or_bread_each"
    ],
    "mandatory_extras": [],
    "menu": "Compact menu",
    "offer_id": "offer-call_ZRKYwlg1P8B0WeMQ",
    "operation_id": "call_jjoNSrXd3Q70dS39",
    "option_id": "06-compact",
    "party_size": 7,
    "pricing": {
      "currency": "INR",
      "meal_payment": "The total is for the listed dining package and inclusions only.",
      "meal_total_inr": 9800,
      "reservation_charge_inr": null,
      "total_scope": "dining_package"
    },
    "reference": "SIM-385061",
    "remaining_due_inr": 9800,
    "seating": "indoor_regular_table",
    "table_capacity": 7,
    "table_count": 1,
    "time": "20:00",
    "timezone": "Asia/Kolkata",
    "total_inr": 9800,
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
    1.7013333333333334,
    133.44133333333335
  ],
  "long_silence_intervals": [
    {
      "attribution": "unknown",
      "duration_seconds": 11.345333333333336,
      "end_seconds": 47.406666666666666,
      "start_seconds": 36.06133333333333
    }
  ],
  "long_silence_threshold_seconds": 10,
  "replies": {
    "counterpart": {
      "no_response_intervals": [
        {
          "after_seconds": 13.581333333333333,
          "gap_ms": 420.0
        },
        {
          "after_seconds": 19.941333333333333,
          "gap_ms": 440.0
        },
        {
          "after_seconds": 23.281333333333333,
          "gap_ms": 500.0
        },
        {
          "after_seconds": 28.941333333333333,
          "gap_ms": 520.0
        },
        {
          "after_seconds": 31.861333333333334,
          "gap_ms": 540.0
        },
        {
          "after_seconds": 34.48133333333333,
          "gap_ms": 400.0
        },
        {
          "after_seconds": 63.681333333333335,
          "gap_ms": 400.0
        },
        {
          "after_seconds": 64.94133333333333,
          "gap_ms": 460.0
        },
        {
          "after_seconds": 82.58133333333333,
          "gap_ms": 440.0
        },
        {
          "after_seconds": 86.46133333333333,
          "gap_ms": 620.0
        },
        {
          "after_seconds": 87.58133333333333,
          "gap_ms": 500.0
        },
        {
          "after_seconds": 111.28133333333334,
          "gap_ms": 520.0
        },
        {
          "after_seconds": 131.18133333333333,
          "gap_ms": 440.0
        },
        {
          "after_seconds": 132.22133333333332,
          "gap_ms": 1220.0
        }
      ],
      "response_gaps": [
        {
          "after_seconds": 3.1613333333333333,
          "gap_ms": 1765.333
        },
        {
          "after_seconds": 36.06133333333333,
          "gap_ms": 11345.333
        },
        {
          "after_seconds": 66.48133333333334,
          "gap_ms": 4205.333
        },
        {
          "after_seconds": 88.52133333333333,
          "gap_ms": 1945.333
        },
        {
          "after_seconds": 99.72133333333333,
          "gap_ms": 1925.333
        },
        {
          "after_seconds": 116.92133333333334,
          "gap_ms": 1965.333
        }
      ]
    },
    "target": {
      "no_response_intervals": [
        {
          "after_seconds": 5.386666666666667,
          "gap_ms": 400.0
        },
        {
          "after_seconds": 7.546666666666667,
          "gap_ms": 500.0
        },
        {
          "after_seconds": 51.04666666666667,
          "gap_ms": 540.0
        },
        {
          "after_seconds": 54.72666666666667,
          "gap_ms": 400.0
        },
        {
          "after_seconds": 56.74666666666667,
          "gap_ms": 380.0
        },
        {
          "after_seconds": 59.46666666666667,
          "gap_ms": 640.0
        },
        {
          "after_seconds": 72.08666666666667,
          "gap_ms": 480.0
        },
        {
          "after_seconds": 73.42666666666666,
          "gap_ms": 300.0
        },
        {
          "after_seconds": 74.58666666666667,
          "gap_ms": 320.0
        },
        {
          "after_seconds": 76.08666666666667,
          "gap_ms": 480.0
        },
        {
          "after_seconds": 91.72666666666667,
          "gap_ms": 420.0
        },
        {
          "after_seconds": 93.00666666666666,
          "gap_ms": 320.0
        },
        {
          "after_seconds": 103.34666666666666,
          "gap_ms": 340.0
        },
        {
          "after_seconds": 105.16666666666667,
          "gap_ms": 400.0
        },
        {
          "after_seconds": 107.60666666666667,
          "gap_ms": 420.0
        },
        {
          "after_seconds": 120.94666666666667,
          "gap_ms": 320.0
        },
        {
          "after_seconds": 121.90666666666667,
          "gap_ms": 480.0
        },
        {
          "after_seconds": 124.46666666666667,
          "gap_ms": 320.0
        },
        {
          "after_seconds": 125.80666666666667,
          "gap_ms": 620.0
        }
      ],
      "response_gaps": [
        {
          "after_seconds": 10.186666666666667,
          "gap_ms": 2594.667
        },
        {
          "after_seconds": 61.36666666666667,
          "gap_ms": 1794.667
        },
        {
          "after_seconds": 78.16666666666667,
          "gap_ms": 3074.667
        },
        {
          "after_seconds": 95.66666666666667,
          "gap_ms": 2134.667
        },
        {
          "after_seconds": 108.96666666666667,
          "gap_ms": 1994.667
        },
        {
          "after_seconds": 127.66666666666667,
          "gap_ms": 2634.667
        }
      ]
    }
  },
  "rms_threshold": 500,
  "speaker_activity": {
    "counterpart": [
      [
        4.926666666666667,
        5.386666666666667
      ],
      [
        5.786666666666667,
        7.546666666666667
      ],
      [
        8.046666666666667,
        10.186666666666667
      ],
      [
        47.406666666666666,
        51.04666666666667
      ],
      [
        51.586666666666666,
        54.72666666666667
      ],
      [
        55.126666666666665,
        56.74666666666667
      ],
      [
        57.126666666666665,
        59.46666666666667
      ],
      [
        60.10666666666667,
        61.36666666666667
      ],
      [
        70.68666666666667,
        72.08666666666667
      ],
      [
        72.56666666666666,
        73.42666666666666
      ],
      [
        73.72666666666667,
        74.58666666666667
      ],
      [
        74.90666666666667,
        76.08666666666667
      ],
      [
        76.56666666666666,
        78.16666666666667
      ],
      [
        90.46666666666667,
        91.72666666666667
      ],
      [
        92.14666666666666,
        93.00666666666666
      ],
      [
        93.32666666666667,
        95.66666666666667
      ],
      [
        101.64666666666666,
        103.34666666666666
      ],
      [
        103.68666666666667,
        105.16666666666667
      ],
      [
        105.56666666666666,
        107.60666666666667
      ],
      [
        108.02666666666667,
        108.96666666666667
      ],
      [
        118.88666666666667,
        120.94666666666667
      ],
      [
        121.26666666666667,
        121.90666666666667
      ],
      [
        122.38666666666667,
        124.46666666666667
      ],
      [
        124.78666666666666,
        125.80666666666667
      ],
      [
        126.42666666666666,
        127.66666666666667
      ]
    ],
    "target": [
      [
        2.4013333333333335,
        3.1613333333333333
      ],
      [
        12.781333333333333,
        13.581333333333333
      ],
      [
        14.001333333333333,
        19.941333333333333
      ],
      [
        20.381333333333334,
        23.281333333333333
      ],
      [
        23.781333333333333,
        28.941333333333333
      ],
      [
        29.461333333333332,
        31.861333333333334
      ],
      [
        32.40133333333333,
        34.48133333333333
      ],
      [
        34.88133333333333,
        36.06133333333333
      ],
      [
        63.16133333333333,
        63.681333333333335
      ],
      [
        64.08133333333333,
        64.94133333333333
      ],
      [
        65.40133333333333,
        66.48133333333334
      ],
      [
        81.24133333333333,
        82.58133333333333
      ],
      [
        83.02133333333333,
        86.46133333333333
      ],
      [
        87.08133333333333,
        87.58133333333333
      ],
      [
        88.08133333333333,
        88.52133333333333
      ],
      [
        97.80133333333333,
        99.72133333333333
      ],
      [
        110.96133333333333,
        111.28133333333334
      ],
      [
        111.80133333333333,
        116.92133333333334
      ],
      [
        130.30133333333333,
        131.18133333333333
      ],
      [
        131.62133333333333,
        132.22133333333332
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
        "item_id": "item_EQgGSo4qMxxmOrc7j7I7M",
        "largest_gap_ms": 0.0
      },
      {
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "item_id": "item_EQgH8BqpF8SnD3ZBCk5Nk",
        "largest_gap_ms": 0.0
      },
      {
        "gap_count": 1,
        "inserted_silence_ms": 12.0,
        "item_id": "item_EQgHV2spKDKNoS1XSLObL",
        "largest_gap_ms": 12.0
      },
      {
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "item_id": "item_EQgHpxkmmNI778rYGkrbV",
        "largest_gap_ms": 0.0
      },
      {
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "item_id": "item_EQgI0PbhikH7A6WoeTs3B",
        "largest_gap_ms": 0.0
      },
      {
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "item_id": "item_EQgIIRtrci8V3xFs8LmJY",
        "largest_gap_ms": 0.0
      }
    ],
    "max_bridge_delivery_delay_ms": 118.39999997615814,
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
      "not_applicable": 0.02,
      "not_met": 0.15,
      "uncertain": 0.09
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
    "confidence": 0.31,
    "probabilities": {
      "met": 0.54,
      "not_met": 0.25,
      "uncertain": 0.21
    },
    "type": "choice"
  },
  "conversation_progress": {
    "choice": "met",
    "confidence": 0.28,
    "probabilities": {
      "met": 0.52,
      "not_met": 0.32,
      "uncertain": 0.16
    },
    "type": "choice"
  },
  "counterpart_validity": {
    "choice": "met",
    "confidence": 0.24,
    "probabilities": {
      "met": 0.49,
      "not_met": 0.29,
      "uncertain": 0.22
    },
    "type": "choice"
  },
  "question_relevance": {
    "choice": "met",
    "confidence": 0.23,
    "probabilities": {
      "met": 0.49,
      "not_met": 0.3,
      "uncertain": 0.21
    },
    "type": "choice"
  },
  "target_role_fidelity": {
    "choice": "met",
    "confidence": 0.23,
    "probabilities": {
      "met": 0.49,
      "not_met": 0.3,
      "uncertain": 0.21
    },
    "type": "choice"
  },
  "user_report_accuracy": {
    "choice": "met",
    "confidence": 0.66,
    "probabilities": {
      "met": 0.74,
      "not_applicable": 0.01,
      "not_met": 0.16,
      "uncertain": 0.09
    },
    "type": "choice"
  }
}
```

Jev is an independent comparison and cannot override verified business records.
All attempts and incomplete stages remain in the batch counts.