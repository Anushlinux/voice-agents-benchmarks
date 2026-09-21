# Conversation and benchmark result

Automated outcome: **failed**. Simulation validity: **valid**.

Full evaluation: **completed**. Conversation repair accepted: **False**.

Human listening is pending. Text judges cannot establish acoustic naturalness or prove that suspected self-talk was audible.

Book one indoor table for six at Mango Verandah in Navrangpura on October 5, 2026 at 7:45 p.m., under Nisha Mehta. Two guests need food with neither onion nor garlic; this is a food preference, not an allergy. Please book only if the kitchen can do that. We will order meals there. No reservation charge, deposit or cancellation fee. Let me know what was arranged and the reference. Speak naturally in Hinglish.

[Independent transcript](transcript.md) · [All metrics and raw judge answers](details.json) · [Failure evidence and uncertainty](diagnostics-v1.json) · [Timing, WER and endpointing availability](measurements-v2.json) · [Per-turn timestamps](turn-timestamps.csv)

Observed task completion: **unresolved**. Established failure owner: **unknown**. Missing required outputs remain visible even when their cause is unknown.

Left audio: restaurant employee. Right audio: received Rumik.

[Full conversation recording](conversation.mp3)

## Turn timestamps

Times below use the browser audio clock. Each row is an employee playback item, not a human-annotated semantic turn. First speech is estimated from 20 ms audio windows. First token is the arrival of Rumik's first text packet (`bot-llm-text`) at the browser after that speech ended; it includes network transit and is an upper bound on hosted generation latency.

| Turn | Employee speech end (s) | First Rumik token (s) | TTFT (ms) | First Rumik speech (s) | TTFS (ms) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 11.787 | 13.803 | 2016.000 | 14.412 | 2625.333 | answered |
| 2 | 57.267 | 58.459 | 1192.000 | 59.212 | 1945.333 | answered |
| 3 | 73.067 | 75.349 | 2282.667 | 76.192 | 3125.333 | answered |

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
| consent_alignment | met | The counterpart disclosed that meals would be ordered and paid for separately, then asked for confirmation. Rumik answered affirmatively and requested finalization, which is clear consent to the stated booking terms. |
| constraint_behavior | not_met | Rumik communicated that two guests wanted “अनियन गार्लिक फ्री फूड,” which changes the user's food preference into a request for free meals. The user authorized only a table reservation, with meals independently ordered and paid for at the visit. Although the final booking did not include a meal charge, the spoken commitment did not accurately respect the task constraint. |
| context_retention | met | Rumik provided the requested date, time, party size, branch, seating, booking name, reservation-charge limit, and dietary count without repeatedly asking for already supplied information. It also asked for the availability check and later accepted finalization. |
| conversation_progress | met | The exchange progressed from stating the request, to checking feasibility, to confirming the booking, and finally requesting the reference. There was no unjustified agreement loop or repeated question from Rumik. |
| counterpart_validity | met | The employee used the supplied availability and reservation tools, accurately stated the available indoor table, zero reservation charge, separate meal payment, and two-guest dietary accommodation, then recorded the reservation only after Rumik's affirmative confirmation. The issued reference was delivered without inventing a booking or unsupported concession. |
| hinglish_quality | uncertain | This rubric requires human listening for understandability and natural Hinglish quality. The supplied transcriptions show a substantive Hindi-English exchange, but text evidence alone cannot establish audio quality or naturalness. |
| question_relevance | met | Rumik's substantive request asked the employee to check whether the requested booking and dietary accommodation were possible, then asked for the reference after confirmation. These questions and answers were relevant to the assigned task. |
| target_output_integrity | uncertain | The transcriptions contain ordinary customer-assistant conversation and no explicit internal turn-management instructions or private self-talk. However, this is a human-listening rubric, and text alone cannot verify the complete audible output. |
| target_role_fidelity | met | Rumik acted as the caller's customer assistant: it stated the user's reservation request, asked the restaurant to check feasibility, consented to finalization, and requested the reference. It did not offer restaurant services or impersonate the restaurant employee. |
| user_report_accuracy | not_met | The report correctly states the booked date, time, party size, seating, booking name, zero reservation charge, and the issued reference in a hyphenated form accepted by the narrow reference comparison. However, it omits the material dietary accommodation for two guests, which the rubric requires when relevant. It also does not state that meals are separate and independently paid for, though the primary failure is the missing dietary term. |

## Private report

Booked indoor regular table for 6 on 2026-10-05 at 19:45 under Nisha Mehta, no reservation charge, reference SIM-27-1196.

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
        4709,
        7406,
        7639,
        8104
      ],
      "observation_boundary": "browser_render_and_received_audio",
      "observed_through_sequence": 8217,
      "readback_item_id": "item_EQgJyk3qRGyFcwe3FtMgO",
      "semantic_confirmation": "requires_human_review"
    },
    "date": "2026-10-05",
    "deposit_inr": 0,
    "inclusions": [
      "One indoor table for the whole party; meals chosen and paid for separately at the visit."
    ],
    "mandatory_extras": [],
    "menu": null,
    "offer_id": "offer-call_lPKtpZ6MYwUwz311",
    "operation_id": "call_qaKD2K7Q2SsMTP2s",
    "option_id": "04-navrangpura-1945",
    "party_size": 6,
    "pricing": {
      "currency": "INR",
      "meal_payment": "Meals are ordered and paid for separately at the visit. Their bill is not known yet; zero reservation charge does not mean free food.",
      "meal_total_inr": null,
      "reservation_charge_inr": 0,
      "total_scope": "reservation_only"
    },
    "reference": "SIM-271196",
    "remaining_due_inr": 0,
    "seating": "indoor_regular_table",
    "table_capacity": 6,
    "table_count": 1,
    "time": "19:45",
    "timezone": "Asia/Kolkata",
    "total_inr": 0,
    "without_onion_garlic_capacity": 4,
    "without_onion_garlic_guests": 2
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
    1.552,
    82.26666666666667
  ],
  "long_silence_intervals": [],
  "long_silence_threshold_seconds": 10,
  "replies": {
    "counterpart": {
      "no_response_intervals": [
        {
          "after_seconds": 16.472,
          "gap_ms": 440.0
        },
        {
          "after_seconds": 19.072,
          "gap_ms": 340.0
        },
        {
          "after_seconds": 21.092,
          "gap_ms": 340.0
        },
        {
          "after_seconds": 23.772,
          "gap_ms": 360.0
        },
        {
          "after_seconds": 25.532,
          "gap_ms": 360.0
        },
        {
          "after_seconds": 27.212,
          "gap_ms": 380.0
        },
        {
          "after_seconds": 30.172,
          "gap_ms": 420.0
        },
        {
          "after_seconds": 77.392,
          "gap_ms": 4874.667
        }
      ],
      "response_gaps": [
        {
          "after_seconds": 2.932,
          "gap_ms": 3174.667
        },
        {
          "after_seconds": 32.472,
          "gap_ms": 3954.667
        },
        {
          "after_seconds": 63.272,
          "gap_ms": 2754.667
        }
      ]
    },
    "target": {
      "no_response_intervals": [
        {
          "after_seconds": 6.6066666666666665,
          "gap_ms": 480.0
        },
        {
          "after_seconds": 9.466666666666667,
          "gap_ms": 480.0
        },
        {
          "after_seconds": 37.406666666666666,
          "gap_ms": 320.0
        },
        {
          "after_seconds": 39.446666666666665,
          "gap_ms": 400.0
        },
        {
          "after_seconds": 41.266666666666666,
          "gap_ms": 400.0
        },
        {
          "after_seconds": 45.24666666666667,
          "gap_ms": 520.0
        },
        {
          "after_seconds": 46.846666666666664,
          "gap_ms": 300.0
        },
        {
          "after_seconds": 49.20666666666666,
          "gap_ms": 640.0
        },
        {
          "after_seconds": 51.20666666666666,
          "gap_ms": 400.0
        },
        {
          "after_seconds": 53.42666666666667,
          "gap_ms": 380.0
        },
        {
          "after_seconds": 54.82666666666667,
          "gap_ms": 700.0
        },
        {
          "after_seconds": 67.44666666666667,
          "gap_ms": 580.0
        },
        {
          "after_seconds": 71.48666666666666,
          "gap_ms": 380.0
        }
      ],
      "response_gaps": [
        {
          "after_seconds": 11.786666666666667,
          "gap_ms": 2625.333
        },
        {
          "after_seconds": 57.266666666666666,
          "gap_ms": 1945.333
        },
        {
          "after_seconds": 73.06666666666666,
          "gap_ms": 3125.333
        }
      ]
    }
  },
  "rms_threshold": 500,
  "speaker_activity": {
    "counterpart": [
      [
        6.1066666666666665,
        6.6066666666666665
      ],
      [
        7.086666666666667,
        9.466666666666667
      ],
      [
        9.946666666666667,
        11.786666666666667
      ],
      [
        36.42666666666667,
        37.406666666666666
      ],
      [
        37.72666666666667,
        39.446666666666665
      ],
      [
        39.846666666666664,
        41.266666666666666
      ],
      [
        41.666666666666664,
        45.24666666666667
      ],
      [
        45.766666666666666,
        46.846666666666664
      ],
      [
        47.14666666666667,
        49.20666666666666
      ],
      [
        49.846666666666664,
        51.20666666666666
      ],
      [
        51.60666666666667,
        53.42666666666667
      ],
      [
        53.806666666666665,
        54.82666666666667
      ],
      [
        55.526666666666664,
        57.266666666666666
      ],
      [
        66.02666666666667,
        67.44666666666667
      ],
      [
        68.02666666666667,
        71.48666666666666
      ],
      [
        71.86666666666666,
        73.06666666666666
      ]
    ],
    "target": [
      [
        2.192,
        2.932
      ],
      [
        14.412,
        16.472
      ],
      [
        16.912,
        19.072
      ],
      [
        19.412,
        21.092
      ],
      [
        21.432,
        23.772
      ],
      [
        24.132,
        25.532
      ],
      [
        25.892,
        27.212
      ],
      [
        27.592,
        30.172
      ],
      [
        30.592,
        32.472
      ],
      [
        59.212,
        63.272
      ],
      [
        76.192,
        77.392
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
        "inserted_silence_ms": 22.688,
        "item_id": "item_EQgJUslL6wqbAxBXsScyW",
        "largest_gap_ms": 22.688
      },
      {
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "item_id": "item_EQgJyk3qRGyFcwe3FtMgO",
        "largest_gap_ms": 0.0
      },
      {
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "item_id": "item_EQgKR7bIGurCbQeqgadmF",
        "largest_gap_ms": 0.0
      }
    ],
    "max_bridge_delivery_delay_ms": 53.200000047683716,
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
    "confidence": 0.68,
    "probabilities": {
      "met": 0.76,
      "not_applicable": 0.01,
      "not_met": 0.12,
      "uncertain": 0.11
    },
    "type": "choice"
  },
  "constraint_behavior": {
    "choice": "met",
    "confidence": 0.35,
    "probabilities": {
      "met": 0.56,
      "not_met": 0.24,
      "uncertain": 0.2
    },
    "type": "choice"
  },
  "context_retention": {
    "choice": "met",
    "confidence": 0.33,
    "probabilities": {
      "met": 0.56,
      "not_met": 0.2,
      "uncertain": 0.24
    },
    "type": "choice"
  },
  "conversation_progress": {
    "choice": "met",
    "confidence": 0.37,
    "probabilities": {
      "met": 0.58,
      "not_met": 0.23,
      "uncertain": 0.19
    },
    "type": "choice"
  },
  "counterpart_validity": {
    "choice": "met",
    "confidence": 0.3,
    "probabilities": {
      "met": 0.53,
      "not_met": 0.22,
      "uncertain": 0.25
    },
    "type": "choice"
  },
  "question_relevance": {
    "choice": "met",
    "confidence": 0.28,
    "probabilities": {
      "met": 0.52,
      "not_met": 0.22,
      "uncertain": 0.26
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
    "confidence": 0.29,
    "probabilities": {
      "met": 0.47,
      "not_applicable": 0.01,
      "not_met": 0.44,
      "uncertain": 0.08
    },
    "type": "choice"
  }
}
```

Jev is an independent comparison and cannot override verified business records.
All attempts and incomplete stages remain in the batch counts.