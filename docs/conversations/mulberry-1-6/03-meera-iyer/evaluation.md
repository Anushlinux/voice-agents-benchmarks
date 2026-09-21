# Conversation and benchmark result

Automated outcome: **unresolved**. Simulation validity: **invalid**.

Full evaluation: **incomplete**. Conversation repair accepted: **False**.

Human listening is pending. Text judges cannot establish acoustic naturalness or prove that suspected self-talk was audible.

Reserve one indoor table for two at Banyan Kitchen in Adyar on October 4, 2026, under Meera Iyer. Around 7 p.m. would work; any time from 6:45 to 7:30 is equally fine. Please arrange a free table booking, with no deposit or cancellation fee. Tell me the final time and booking reference. Speak naturally in Hinglish.

[Independent transcript](transcript.md) · [All metrics and raw judge answers](details.json) · [Failure evidence and uncertainty](diagnostics-v1.json) · [Timing, WER and endpointing availability](measurements-v2.json) · [Per-turn timestamps](turn-timestamps.csv)

Observed task completion: **unresolved**. Established failure owner: **unknown**. Missing required outputs remain visible even when their cause is unknown.

Left audio: restaurant employee. Right audio: received Rumik.

[Full conversation recording](conversation.mp3)

## Turn timestamps

Times below use the browser audio clock. Each row is an employee playback item, not a human-annotated semantic turn. First speech is estimated from 20 ms audio windows. First token is the arrival of Rumik's first text packet (`bot-llm-text`) at the browser after that speech ended; it includes network transit and is an upper bound on hosted generation latency.

| Turn | Employee speech end (s) | First Rumik token (s) | TTFT (ms) | First Rumik speech (s) | TTFS (ms) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 7.861 | 9.264 | 1402.667 | 10.164 | 2302.667 | answered |
| 2 | 28.981 | 30.053 | 1072.000 | 31.064 | 2082.667 | answered |
| 3 | 40.829 | — | — | — | — | no_observed_reply |
| 4 | 51.721 | 52.907 | 1185.333 | 54.044 | 2322.667 | answered |
| 5 | 71.161 | 73.803 | 2641.333 | 74.964 | 3802.667 | answered |
| 6 | 89.481 | 90.987 | 1505.333 | 92.104 | 2622.667 | answered |

## Evaluation stages

| Stage | Status |
| --- | --- |
| jev | error |
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
| consent_alignment | met | The counterpart presented the available 19:30 option and its reservation terms, including no reservation charge and separately paid meals. Rumik then explicitly requested booking at 7:30 p.m., which is clear agreement to the unchanged material terms. |
| constraint_behavior | met | Rumik requested the assigned restaurant, date, Adyar branch, indoor seating and table reservation, then selected 19:30, which is within the permitted time window. The committed reservation is for two, one indoor regular table, table-only, with zero reservation charge and no deposit, cancellation fee or mandatory extras. |
| context_retention | met | After the initial request and the employee's availability/terms explanation, Rumik selected 19:30 and asked to book it without unnecessarily repeating settled requirements or asking an irrelevant confirmation question. |
| conversation_progress | met | The exchange progresses from the request, to availability, to selection of 19:30, to booking and closure. Rumik's substantive utterances are task-directed and do not create a repeated agreement or question loop. |
| counterpart_validity | not_met | The employee used the availability, offer and recording tools and described the reservation terms, but announced that the booking was confirmed before the successful record result and delivered a reference inconsistent with the issued reference. The business record issued SIM-143712, while the employee's speech states 14712 and later repeats that form. |
| hinglish_quality | uncertain | This rubric requires human listening for understandability and natural Hinglish quality. The supplied transcription is insufficient to establish that judgment. |
| question_relevance | met | Rumik's request to check the time and its later instruction to book at 7:30 p.m. directly address the reservation task and the employee's offered time options. |
| target_output_integrity | uncertain | This is a human-listening rubric requiring confirmation from the captured audio that no internal instructions or private self-talk were audible. The transcription alone cannot establish that conclusively. |
| target_role_fidelity | met | Rumik acts as the customer's assistant: it states the reservation request and then selects a time and asks the restaurant to book it. It does not offer restaurant services or speak as the restaurant employee. |
| user_report_accuracy | not_met | The report correctly states the date, time, party size, seating, branch, booking name and zero charge, but it reports reference 14712. The committed business record issued the single reference SIM-143712, so the reference identity is materially inaccurate. |

## Private report

Booked indoor regular table for 2 at Banyan Kitchen Adyar on 2026-10-04 at 19:30 under Meera Iyer, no charge, reference 14712.

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
        5146,
        6894,
        7185,
        7997
      ],
      "observation_boundary": "browser_render_and_received_audio",
      "observed_through_sequence": 8114,
      "readback_item_id": "item_EQgkTP7zshcesumVNQ3sI",
      "semantic_confirmation": "requires_human_review"
    },
    "date": "2026-10-04",
    "deposit_inr": 0,
    "inclusions": [
      "One indoor table for the whole party; meals chosen and paid for separately at the visit."
    ],
    "mandatory_extras": [],
    "menu": null,
    "offer_id": "offer-call_1rJYPSyE3YxnAsYv",
    "operation_id": "call_uyS0irI10tVEDiU9",
    "option_id": "03-adyar-1930",
    "party_size": 2,
    "pricing": {
      "currency": "INR",
      "meal_payment": "Meals are ordered and paid for separately at the visit. Their bill is not known yet; zero reservation charge does not mean free food.",
      "meal_total_inr": null,
      "reservation_charge_inr": 0,
      "total_scope": "reservation_only"
    },
    "reference": "SIM-143712",
    "remaining_due_inr": 0,
    "seating": "indoor_regular_table",
    "table_capacity": 2,
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
    1.504,
    94.264
  ],
  "long_silence_intervals": [],
  "long_silence_threshold_seconds": 10,
  "replies": {
    "counterpart": {
      "no_response_intervals": [
        {
          "after_seconds": 14.264,
          "gap_ms": 440.0
        },
        {
          "after_seconds": 32.744,
          "gap_ms": 440.0
        },
        {
          "after_seconds": 76.544,
          "gap_ms": 400.0
        },
        {
          "after_seconds": 79.404,
          "gap_ms": 500.0
        },
        {
          "after_seconds": 93.384,
          "gap_ms": 880.0
        }
      ],
      "response_gaps": [
        {
          "after_seconds": 2.984,
          "gap_ms": 1597.333
        },
        {
          "after_seconds": 17.624,
          "gap_ms": 2837.333
        },
        {
          "after_seconds": 34.884,
          "gap_ms": 1797.333
        },
        {
          "after_seconds": 56.444,
          "gap_ms": 7897.333
        },
        {
          "after_seconds": 80.844,
          "gap_ms": 1777.333
        }
      ]
    },
    "target": {
      "no_response_intervals": [
        {
          "after_seconds": 5.061333333333334,
          "gap_ms": 580.0
        },
        {
          "after_seconds": 23.301333333333332,
          "gap_ms": 520.0
        },
        {
          "after_seconds": 26.981333333333332,
          "gap_ms": 460.0
        },
        {
          "after_seconds": 38.601333333333336,
          "gap_ms": 440.0
        },
        {
          "after_seconds": 42.74133333333333,
          "gap_ms": 440.0
        },
        {
          "after_seconds": 45.641333333333336,
          "gap_ms": 420.0
        },
        {
          "after_seconds": 47.70133333333333,
          "gap_ms": 460.0
        },
        {
          "after_seconds": 50.221333333333334,
          "gap_ms": 660.0
        },
        {
          "after_seconds": 65.84133333333334,
          "gap_ms": 400.0
        },
        {
          "after_seconds": 69.30133333333333,
          "gap_ms": 680.0
        },
        {
          "after_seconds": 85.84133333333334,
          "gap_ms": 500.0
        },
        {
          "after_seconds": 87.50133333333333,
          "gap_ms": 560.0
        }
      ],
      "response_gaps": [
        {
          "after_seconds": 7.8613333333333335,
          "gap_ms": 2302.667
        },
        {
          "after_seconds": 28.981333333333332,
          "gap_ms": 2082.667
        },
        {
          "after_seconds": 51.721333333333334,
          "gap_ms": 2322.667
        },
        {
          "after_seconds": 71.16133333333333,
          "gap_ms": 3802.667
        },
        {
          "after_seconds": 89.48133333333334,
          "gap_ms": 2622.667
        }
      ]
    }
  },
  "rms_threshold": 500,
  "speaker_activity": {
    "counterpart": [
      [
        4.581333333333333,
        5.061333333333334
      ],
      [
        5.641333333333334,
        7.8613333333333335
      ],
      [
        20.461333333333332,
        23.301333333333332
      ],
      [
        23.82133333333333,
        26.981333333333332
      ],
      [
        27.441333333333333,
        28.981333333333332
      ],
      [
        36.681333333333335,
        38.601333333333336
      ],
      [
        39.041333333333334,
        42.74133333333333
      ],
      [
        43.181333333333335,
        45.641333333333336
      ],
      [
        46.06133333333333,
        47.70133333333333
      ],
      [
        48.16133333333333,
        50.221333333333334
      ],
      [
        50.88133333333333,
        51.721333333333334
      ],
      [
        64.34133333333334,
        65.84133333333334
      ],
      [
        66.24133333333333,
        69.30133333333333
      ],
      [
        69.98133333333334,
        71.16133333333333
      ],
      [
        82.62133333333334,
        85.84133333333334
      ],
      [
        86.34133333333334,
        87.50133333333333
      ],
      [
        88.06133333333334,
        89.48133333333334
      ]
    ],
    "target": [
      [
        2.404,
        2.984
      ],
      [
        10.164,
        14.264
      ],
      [
        14.704,
        17.624
      ],
      [
        31.064,
        32.744
      ],
      [
        33.184,
        34.884
      ],
      [
        54.044,
        56.444
      ],
      [
        74.964,
        76.544
      ],
      [
        76.944,
        79.404
      ],
      [
        79.904,
        80.844
      ],
      [
        92.104,
        93.384
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
        "inserted_silence_ms": 44.021,
        "item_id": "item_EQgjvUSNYRs5JFdpvIPgd",
        "largest_gap_ms": 44.021
      },
      {
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "item_id": "item_EQgkBXuxGhk3hn8q0Nn46",
        "largest_gap_ms": 0.0
      },
      {
        "gap_count": 1,
        "inserted_silence_ms": 22.667,
        "item_id": "item_EQgkRysXJlKhZ16skdlS2",
        "largest_gap_ms": 22.667
      },
      {
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "item_id": "item_EQgkTP7zshcesumVNQ3sI",
        "largest_gap_ms": 0.0
      },
      {
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "item_id": "item_EQgktKQXEFnOuIxRc0coV",
        "largest_gap_ms": 0.0
      },
      {
        "gap_count": 1,
        "inserted_silence_ms": 6.667,
        "item_id": "item_EQglBmVIky8O645r4FoZm",
        "largest_gap_ms": 6.667
      }
    ],
    "max_bridge_delivery_delay_ms": 187.80000001192093,
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
  "error_type": "ValueError",
  "status": "error"
}
```

Jev is an independent comparison and cannot override verified business records.
All attempts and incomplete stages remain in the batch counts.