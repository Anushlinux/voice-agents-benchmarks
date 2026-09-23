# Conversation and benchmark result

Automated outcome: **failed**. Simulation validity: **valid**.

Full evaluation: **completed**. Conversation repair accepted: **False**.

Human listening is pending. Text judges cannot establish acoustic naturalness or prove that suspected self-talk was audible.

Please reserve one indoor table for five at Copper Leaf on October 3, 2026 at 8 p.m., under Kabir Sethi. Try Indiranagar first; Domlur is fine if Indiranagar has no table then. Keep the time and date. Make a free table reservation only, with no deposit or cancellation fee, and send me the details and reference if booked. Speak naturally in Hinglish.

[Independent transcript](transcript.md) · All metrics and raw judge answers (`details.json` is not included in this published export) · [Failure evidence and uncertainty](diagnostics-v1.json) · [Timing, WER and endpointing availability](measurements-v2.json) · [Per-turn timestamps](turn-timestamps.csv)

Observed task completion: **unresolved**. Established failure owner: **unknown**. Missing required outputs remain visible even when their cause is unknown.

Left audio: restaurant employee. Right audio: received Rumik.

[Full conversation recording](conversation.mp3)

## Turn timestamps

Times below use the browser audio clock. Each row is an employee playback item, not a human-annotated semantic turn. First speech is estimated from 20 ms audio windows. First token is the arrival of Rumik's first text packet (`bot-llm-text`) at the browser after that speech ended; it includes network transit and is an upper bound on hosted generation latency.

| Turn | Employee speech end (s) | First Rumik token (s) | TTFT (ms) | First Rumik speech (s) | TTFS (ms) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 7.827 | 9.109 | 1282.667 | 9.895 | 2068.000 | answered |
| 2 | 44.587 | 45.771 | 1184.000 | 46.555 | 1968.000 | answered |
| 3 | 59.107 | 61.344 | 2237.333 | 62.295 | 3188.000 | answered |

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
| booking_identity | uncertain | Exact normalized names match; different spelling or script needs semantic review, not an automatic wrong-person verdict. |
| reservation_history | met | Replayed booking identity, terms, action ownership, reference and structural speech anchors. These do not prove semantic agreement. |
| user_report_references | met | Compared only explicitly labelled target report references using explicit-reference-clauses-v2. Distinct codes remain distinct. A match checks identifiers only, not overall report accuracy; unsupported prose requires review. |
| user_report_presence | met | Checked authenticated report receipt. Confirmed absence is separate from false content; a missing report does not establish which actor caused an interrupted call. |
| consent_alignment | met | Rumik requested the permitted Domlur fallback after Indiranagar was unavailable, received the zero-charge table-only terms, and clearly agreed: “हाँ, बुक कर दीजिए।” |
| constraint_behavior | met | Rumik's spoken request preserved the date, time, party size, indoor regular table, branch preference and table-only reservation. It did not agree to a charge or meal purchase; the later recorded booking terms also show zero reservation charge and no mandatory extras. |
| context_retention | met | Rumik stated the relevant requirements once, accepted the unchanged Domlur fallback terms, and did not unnecessarily re-ask settled details. |
| conversation_progress | met | The exchange progressed from the request, to the Indiranagar result, to the authorized Domlur alternative, agreement, confirmation and closure without a repeated-question loop. |
| counterpart_validity | met | The employee truthfully reported Indiranagar unavailability, offered the authorized Domlur option with the correct zero-fee/table-only terms, sought agreement, and announced the issued reference after the successful reservation tool result. The employee's received target speech asked for reservation under Sethi, so the recorded “Sethi” name is not a counterpart invention relative to the received request. |
| hinglish_quality | uncertain | This rubric requires human listening for understandability and naturalness; the supplied transcription alone cannot establish audio quality. |
| question_relevance | met | Rumik's substantive response was the relevant booking authorization, followed by a natural closing. No unrelated question or answer is present. |
| target_output_integrity | uncertain | Determining whether audible output contains internal instructions or private self-talk requires human listening to the audio; the transcription does not prove acoustic integrity. |
| target_role_fidelity | met | Rumik acted as the customer's assistant: it stated the reservation request, specified the branch fallback, authorized booking, and closed the call rather than presenting itself as restaurant staff. |
| user_report_accuracy | not_met | The report accurately states the date, time, branch, seating, party size, charge and reference, but it reports the booking name as “Kabir Sethi” while the committed business record is under “Sethi.” The report therefore does not match the actual committed record field by field. |

## Private report

Booked indoor regular table for 5 at Domlur on 2026-10-03 at 20:00 under Kabir Sethi, no reservation charge, reference SIM-718266.

## Business outcome

```json
[
  {
    "booking_kind": "table_only",
    "booking_name": "Sethi",
    "branch": "Domlur",
    "cancellation_fee_inr": 0,
    "consent_evidence": {
      "audio_artifacts": [
        "audio/played.wav",
        "audio/received.wav"
      ],
      "event_sequences": [
        3661,
        5812,
        6035,
        6269
      ],
      "observation_boundary": "browser_render_and_received_audio",
      "observed_through_sequence": 6376,
      "readback_item_id": "item_EQgEsrmaqnDNqBXbfeOhw",
      "semantic_confirmation": "requires_human_review"
    },
    "date": "2026-10-03",
    "deposit_inr": 0,
    "inclusions": [
      "One indoor table for the whole party; meals chosen and paid for separately at the visit."
    ],
    "mandatory_extras": [],
    "menu": null,
    "offer_id": "offer-call_OO7sgVLNGuCTipJI",
    "operation_id": "call_0lOzKX9CpS0r0XGZ",
    "option_id": "02-domlur-2000",
    "party_size": 5,
    "pricing": {
      "currency": "INR",
      "meal_payment": "Meals are ordered and paid for separately at the visit. Their bill is not known yet; zero reservation charge does not mean free food.",
      "meal_total_inr": null,
      "reservation_charge_inr": 0,
      "total_scope": "reservation_only"
    },
    "reference": "SIM-718266",
    "remaining_due_inr": 0,
    "seating": "indoor_regular_table",
    "table_capacity": 5,
    "table_count": 1,
    "time": "20:00",
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
    1.4346666666666668,
    68.97066666666667
  ],
  "long_silence_intervals": [],
  "long_silence_threshold_seconds": 10,
  "replies": {
    "counterpart": {
      "no_response_intervals": [
        {
          "after_seconds": 13.614666666666666,
          "gap_ms": 480.0
        },
        {
          "after_seconds": 16.454666666666668,
          "gap_ms": 420.0
        },
        {
          "after_seconds": 18.454666666666668,
          "gap_ms": 380.0
        },
        {
          "after_seconds": 20.294666666666668,
          "gap_ms": 440.0
        },
        {
          "after_seconds": 62.934666666666665,
          "gap_ms": 420.0
        },
        {
          "after_seconds": 64.01466666666667,
          "gap_ms": 4956.0
        }
      ],
      "response_gaps": [
        {
          "after_seconds": 2.8946666666666667,
          "gap_ms": 1652.0
        },
        {
          "after_seconds": 22.554666666666666,
          "gap_ms": 5772.0
        },
        {
          "after_seconds": 48.27466666666667,
          "gap_ms": 2712.0
        }
      ]
    },
    "target": {
      "no_response_intervals": [
        {
          "after_seconds": 5.026666666666666,
          "gap_ms": 440.0
        },
        {
          "after_seconds": 30.286666666666665,
          "gap_ms": 380.0
        },
        {
          "after_seconds": 33.486666666666665,
          "gap_ms": 300.0
        },
        {
          "after_seconds": 36.68666666666667,
          "gap_ms": 940.0
        },
        {
          "after_seconds": 39.42666666666667,
          "gap_ms": 360.0
        },
        {
          "after_seconds": 42.42666666666667,
          "gap_ms": 860.0
        },
        {
          "after_seconds": 52.20666666666666,
          "gap_ms": 500.0
        },
        {
          "after_seconds": 53.626666666666665,
          "gap_ms": 400.0
        },
        {
          "after_seconds": 56.306666666666665,
          "gap_ms": 500.0
        }
      ],
      "response_gaps": [
        {
          "after_seconds": 7.826666666666667,
          "gap_ms": 2068.0
        },
        {
          "after_seconds": 44.586666666666666,
          "gap_ms": 1968.0
        },
        {
          "after_seconds": 59.10666666666667,
          "gap_ms": 3188.0
        }
      ]
    }
  },
  "rms_threshold": 500,
  "speaker_activity": {
    "counterpart": [
      [
        4.546666666666667,
        5.026666666666666
      ],
      [
        5.466666666666667,
        7.826666666666667
      ],
      [
        28.326666666666668,
        30.286666666666665
      ],
      [
        30.666666666666668,
        33.486666666666665
      ],
      [
        33.78666666666667,
        36.68666666666667
      ],
      [
        37.626666666666665,
        39.42666666666667
      ],
      [
        39.78666666666667,
        42.42666666666667
      ],
      [
        43.28666666666667,
        44.586666666666666
      ],
      [
        50.986666666666665,
        52.20666666666666
      ],
      [
        52.70666666666666,
        53.626666666666665
      ],
      [
        54.026666666666664,
        56.306666666666665
      ],
      [
        56.806666666666665,
        59.10666666666667
      ]
    ],
    "target": [
      [
        2.1746666666666665,
        2.8946666666666667
      ],
      [
        9.894666666666666,
        13.614666666666666
      ],
      [
        14.094666666666667,
        16.454666666666668
      ],
      [
        16.874666666666666,
        18.454666666666668
      ],
      [
        18.834666666666667,
        20.294666666666668
      ],
      [
        20.734666666666666,
        22.554666666666666
      ],
      [
        46.55466666666667,
        48.27466666666667
      ],
      [
        62.294666666666664,
        62.934666666666665
      ],
      [
        63.35466666666667,
        64.01466666666667
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
        "inserted_silence_ms": 6.688,
        "item_id": "item_EQgEVvyn7EnFqjbd0R2SH",
        "largest_gap_ms": 6.688
      },
      {
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "item_id": "item_EQgEsrmaqnDNqBXbfeOhw",
        "largest_gap_ms": 0.0
      },
      {
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "item_id": "item_EQgFFBymfSeWruaDn6e7c",
        "largest_gap_ms": 0.0
      }
    ],
    "max_bridge_delivery_delay_ms": 113.80000001192093,
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
    "confidence": 0.75,
    "probabilities": {
      "met": 0.81,
      "not_applicable": 0.01,
      "not_met": 0.09,
      "uncertain": 0.09
    },
    "type": "choice"
  },
  "constraint_behavior": {
    "choice": "met",
    "confidence": 0.49,
    "probabilities": {
      "met": 0.66,
      "not_met": 0.16,
      "uncertain": 0.18
    },
    "type": "choice"
  },
  "context_retention": {
    "choice": "met",
    "confidence": 0.49,
    "probabilities": {
      "met": 0.66,
      "not_met": 0.13,
      "uncertain": 0.21
    },
    "type": "choice"
  },
  "conversation_progress": {
    "choice": "met",
    "confidence": 0.53,
    "probabilities": {
      "met": 0.69,
      "not_met": 0.14,
      "uncertain": 0.17
    },
    "type": "choice"
  },
  "counterpart_validity": {
    "choice": "met",
    "confidence": 0.49,
    "probabilities": {
      "met": 0.66,
      "not_met": 0.14,
      "uncertain": 0.2
    },
    "type": "choice"
  },
  "question_relevance": {
    "choice": "met",
    "confidence": 0.44,
    "probabilities": {
      "met": 0.63,
      "not_met": 0.14,
      "uncertain": 0.23
    },
    "type": "choice"
  },
  "target_role_fidelity": {
    "choice": "met",
    "confidence": 0.44,
    "probabilities": {
      "met": 0.63,
      "not_met": 0.16,
      "uncertain": 0.21
    },
    "type": "choice"
  },
  "user_report_accuracy": {
    "choice": "met",
    "confidence": 0.74,
    "probabilities": {
      "met": 0.8,
      "not_applicable": 0.01,
      "not_met": 0.1,
      "uncertain": 0.09
    },
    "type": "choice"
  }
}
```

Jev is an independent comparison and cannot override verified business records.
All attempts and incomplete stages remain in the batch counts.