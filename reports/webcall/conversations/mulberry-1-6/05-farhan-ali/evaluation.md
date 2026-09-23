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
| 1 | 7.621 | 8.944 | 1322.667 | 9.905 | 2284.000 | answered |
| 2 | 37.661 | 39.008 | 1346.667 | 40.045 | 2384.000 | answered |
| 3 | 54.881 | 57.093 | 2212.000 | 58.165 | 3284.000 | answered |

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
| consent_alignment | met | The counterpart offered a 19:30 Jubilee Hills table, and Rumik clearly accepted that current offer by asking to confirm it. The subsequent reservation was recorded for those terms. |
| constraint_behavior | not_met | Rumik's initial spoken request states a 17:00–18:00 window, which conflicts with the user's permitted 19:00–20:00 window. It later accepts 19:30, which is within the allowed window, but the initial commitment does not respect the assigned time constraint. |
| context_retention | met | Rumik supplied the date, party size, seating, branch preference, booking name and free table-only requirement, then responded to the offered time without an unjustified repetition loop. |
| conversation_progress | met | The exchange progresses from the request, to an availability alternative, to acceptance and confirmation, without an observable repeated-question loop. |
| counterpart_validity | met | The employee states that the requested Jubilee Hills interval has no matching availability, offers a supplied 19:30 alternative, obtains acceptance, records the reservation under Farhan Ali, and provides the issued reference. The tool records support the offered and completed reservation; no unsupported concession or invented reference is shown. |
| hinglish_quality | uncertain | This rubric requires human listening for understandability and naturalness. The supplied transcription alone cannot establish audio quality or natural delivery. |
| question_relevance | met | Rumik's request asks for the assigned reservation and asks the employee to check availability; its later response accepts the offered time and requests confirmation. These are relevant to the task. |
| target_output_integrity | uncertain | The transcript contains ordinary customer-facing conversation and no obvious internal turn-management instructions, but this is a human-listening rubric and the text alone cannot verify the audible output fully. |
| target_role_fidelity | met | Rumik acts as the customer's caller: it states the reservation request, supplies the booking name and preferences, responds to the employee's offer, and asks for confirmation. It does not present itself as restaurant staff. |
| user_report_accuracy | met | The authenticated report states a 6 October 2026 19:30 indoor regular table for four under Farhan Ali at Jubilee Hills with INR 0 charge. Those fields match the committed reservation in business/final.json, and the reported reference preserves the issued identifier under the permitted hyphen normalization. |

## Private report

Booked 6 Oct 2026 19:30 indoor regular table for 4 under Farhan Ali at Jubilee Hills, charge INR 0, reference SIM-84-6468.

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
        3328,
        4653,
        4917,
        5469
      ],
      "observation_boundary": "browser_render_and_received_audio",
      "observed_through_sequence": 5669,
      "readback_item_id": "item_EQgiGZGMoo6luUnxTWyqi",
      "semantic_confirmation": "requires_human_review"
    },
    "date": "2026-10-06",
    "deposit_inr": 0,
    "inclusions": [
      "One indoor table for the whole party; meals chosen and paid for separately at the visit."
    ],
    "mandatory_extras": [],
    "menu": null,
    "offer_id": "offer-call_sZccMXtNA5Ue0wq4",
    "operation_id": "call_6FKNmSzHI8dFIUC4",
    "option_id": "05-jubilee-1930",
    "party_size": 4,
    "pricing": {
      "currency": "INR",
      "meal_payment": "Meals are ordered and paid for separately at the visit. Their bill is not known yet; zero reservation charge does not mean free food.",
      "meal_total_inr": null,
      "reservation_charge_inr": 0,
      "total_scope": "reservation_only"
    },
    "reference": "SIM-846468",
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
    1.5253333333333334,
    64.42533333333333
  ],
  "long_silence_intervals": [],
  "long_silence_threshold_seconds": 10,
  "replies": {
    "counterpart": {
      "no_response_intervals": [
        {
          "after_seconds": 15.605333333333334,
          "gap_ms": 520.0
        },
        {
          "after_seconds": 17.945333333333334,
          "gap_ms": 480.0
        },
        {
          "after_seconds": 19.765333333333334,
          "gap_ms": 420.0
        },
        {
          "after_seconds": 22.805333333333333,
          "gap_ms": 440.0
        },
        {
          "after_seconds": 42.44533333333333,
          "gap_ms": 440.0
        },
        {
          "after_seconds": 59.425333333333334,
          "gap_ms": 5000.0
        }
      ],
      "response_gaps": [
        {
          "after_seconds": 2.8853333333333335,
          "gap_ms": 1776.0
        },
        {
          "after_seconds": 24.505333333333333,
          "gap_ms": 3016.0
        },
        {
          "after_seconds": 44.885333333333335,
          "gap_ms": 3616.0
        }
      ]
    },
    "target": {
      "no_response_intervals": [
        {
          "after_seconds": 5.101333333333334,
          "gap_ms": 420.0
        },
        {
          "after_seconds": 31.861333333333334,
          "gap_ms": 500.0
        },
        {
          "after_seconds": 35.74133333333333,
          "gap_ms": 500.0
        },
        {
          "after_seconds": 50.041333333333334,
          "gap_ms": 400.0
        },
        {
          "after_seconds": 53.141333333333336,
          "gap_ms": 520.0
        }
      ],
      "response_gaps": [
        {
          "after_seconds": 7.621333333333333,
          "gap_ms": 2284.0
        },
        {
          "after_seconds": 37.66133333333333,
          "gap_ms": 2384.0
        },
        {
          "after_seconds": 54.88133333333333,
          "gap_ms": 3284.0
        }
      ]
    }
  },
  "rms_threshold": 500,
  "speaker_activity": {
    "counterpart": [
      [
        4.661333333333333,
        5.101333333333334
      ],
      [
        5.521333333333334,
        7.621333333333333
      ],
      [
        27.521333333333335,
        31.861333333333334
      ],
      [
        32.361333333333334,
        35.74133333333333
      ],
      [
        36.24133333333333,
        37.66133333333333
      ],
      [
        48.501333333333335,
        50.041333333333334
      ],
      [
        50.44133333333333,
        53.141333333333336
      ],
      [
        53.66133333333333,
        54.88133333333333
      ]
    ],
    "target": [
      [
        2.3853333333333335,
        2.8853333333333335
      ],
      [
        9.905333333333333,
        15.605333333333334
      ],
      [
        16.125333333333334,
        17.945333333333334
      ],
      [
        18.425333333333334,
        19.765333333333334
      ],
      [
        20.185333333333332,
        22.805333333333333
      ],
      [
        23.245333333333335,
        24.505333333333333
      ],
      [
        40.04533333333333,
        42.44533333333333
      ],
      [
        42.885333333333335,
        44.885333333333335
      ],
      [
        58.165333333333336,
        59.425333333333334
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
        "item_id": "item_EQghtjYIzHOPMxdUkOA4m",
        "largest_gap_ms": 0.0
      },
      {
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "item_id": "item_EQgiGZGMoo6luUnxTWyqi",
        "largest_gap_ms": 0.0
      },
      {
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "item_id": "item_EQgib8kjuBfVSU1frhGE7",
        "largest_gap_ms": 0.0
      }
    ],
    "max_bridge_delivery_delay_ms": 63.39999997615814,
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
    "confidence": 0.3,
    "probabilities": {
      "met": 0.48,
      "not_applicable": 0.03,
      "not_met": 0.41,
      "uncertain": 0.08
    },
    "type": "choice"
  },
  "constraint_behavior": {
    "choice": "not_met",
    "confidence": 0.53,
    "probabilities": {
      "met": 0.2,
      "not_met": 0.6799999999999999,
      "uncertain": 0.12
    },
    "type": "choice"
  },
  "context_retention": {
    "choice": "not_met",
    "confidence": 0.43,
    "probabilities": {
      "met": 0.24,
      "not_met": 0.62,
      "uncertain": 0.14
    },
    "type": "choice"
  },
  "conversation_progress": {
    "choice": "not_met",
    "confidence": 0.36,
    "probabilities": {
      "met": 0.32,
      "not_met": 0.57,
      "uncertain": 0.11
    },
    "type": "choice"
  },
  "counterpart_validity": {
    "choice": "not_met",
    "confidence": 0.37,
    "probabilities": {
      "met": 0.27,
      "not_met": 0.59,
      "uncertain": 0.14
    },
    "type": "choice"
  },
  "question_relevance": {
    "choice": "not_met",
    "confidence": 0.47,
    "probabilities": {
      "met": 0.2,
      "not_met": 0.65,
      "uncertain": 0.15
    },
    "type": "choice"
  },
  "target_role_fidelity": {
    "choice": "not_met",
    "confidence": 0.4,
    "probabilities": {
      "met": 0.23,
      "not_met": 0.6,
      "uncertain": 0.17
    },
    "type": "choice"
  },
  "user_report_accuracy": {
    "choice": "not_met",
    "confidence": 0.32,
    "probabilities": {
      "met": 0.41,
      "not_applicable": 0.01,
      "not_met": 0.49,
      "uncertain": 0.09
    },
    "type": "choice"
  }
}
```

Jev is an independent comparison and cannot override verified business records.
All attempts and incomplete stages remain in the batch counts.