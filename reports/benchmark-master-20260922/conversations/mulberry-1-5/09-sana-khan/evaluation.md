# Conversation and benchmark result

Automated outcome: **passed**. Simulation validity: **valid**.

Full evaluation: **completed**. Conversation repair accepted: **True**.

Human listening is pending. Text judges cannot establish acoustic naturalness or prove that suspected self-talk was audible.

Arrange dinner for six at Copper Mango in Greater Kailash on October 10, 2026 at 8 p.m., under Sana Khan, together at one indoor table. We need a starter and main with rice or bread each, and ₹9,000 is the absolute total limit including all charges. You can ask for a better price and agree to pay at the visit, but no deposit, cancellation fee or extras. If it cannot fit, do not book and tell me why. Speak naturally in Hinglish.

[Independent transcript](transcript.md) · [All metrics and raw judge answers](details.json) · [Failure evidence and uncertainty](diagnostics-v1.json) · [Timing, WER and endpointing availability](measurements-v2.json) · [Per-turn timestamps](turn-timestamps.csv)

Observed task completion: **completed**. Established failure owner: **unknown**. Missing required outputs remain visible even when their cause is unknown.

Left audio: restaurant employee. Right audio: received Rumik.

[Full conversation recording](conversation.mp3)

## Turn timestamps

Times below use the browser audio clock. Each row is an employee playback item, not a human-annotated semantic turn. First speech is estimated from 20 ms audio windows. First token is the arrival of Rumik's first text packet (`bot-llm-text`) at the browser after that speech ended; it includes network transit and is an upper bound on hosted generation latency.

| Turn | Employee speech end (s) | First Rumik token (s) | TTFT (ms) | First Rumik speech (s) | TTFS (ms) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 8.161 | 9.467 | 1305.333 | 10.097 | 1936.000 | answered |
| 2 | 47.121 | 49.787 | 2665.333 | 51.057 | 3936.000 | answered |

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
| constraint_behavior | met | Rumik communicated the required date, party size, Greater Kailash branch, indoor regular table, inclusions, booking name, and INR 9,000 ceiling. It made no commitment to accept the INR 9,600 offer and did not authorize payment, fees, or extras. |
| context_retention | met | Rumik stated the assignment details in the substantive request and did not unjustifiably ask for them again. Its closing followed the employee's quoted offer and confirmation question. |
| conversation_progress | uncertain | Unsupported judge claim: A speech claim does not identify a cited recording window. The original judgment is retained in judge-response.json. |
| counterpart_validity | met | The employee used the availability and offer tools, truthfully stated the available INR 9,600 concession option and its inclusions, and did not claim consent or a completed booking. The audit shows no saved reservation. |
| hinglish_quality | uncertain | This rubric requires human listening for understandability and naturalness. The supplied transcriptions alone cannot establish audio quality or natural delivery. |
| question_relevance | met | Rumik's substantive question asked whether the restaurant could confirm the requested booking, which is directly relevant to the assigned task. Its closing was also responsive to the completed exchange. |
| target_output_integrity | uncertain | The transcriptions show customer-facing content and no textual internal instructions, but this is a human-listening rubric and the text alone cannot verify whether the audible output contained leakage or private self-talk. |
| target_role_fidelity | met | Rumik acted as the customer's assistant: it presented the dinner requirements, price ceiling, seating, inclusions, and booking name, then asked for confirmation. It did not offer restaurant services or claim to be the restaurant. |
| user_report_accuracy | met | The delivered report states that no booking could be made because the INR 9,600 total exceeded the INR 9,000 limit. This matches the final business state: no booking was saved, and the offered concession total was INR 9,600. No reference was invented. |
| consent_alignment | not_applicable | Review the actual conversation and outcome |

## Private report

Cannot book: total charge INR 9,600 exceeds the allowed limit of INR 9,000.

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
    1.7973333333333332,
    53.626666666666665
  ],
  "long_silence_intervals": [],
  "long_silence_threshold_seconds": 10,
  "replies": {
    "counterpart": {
      "no_response_intervals": [
        {
          "after_seconds": 14.177333333333333,
          "gap_ms": 420.0
        },
        {
          "after_seconds": 15.257333333333333,
          "gap_ms": 880.0
        },
        {
          "after_seconds": 18.197333333333333,
          "gap_ms": 460.0
        },
        {
          "after_seconds": 20.177333333333333,
          "gap_ms": 560.0
        },
        {
          "after_seconds": 23.097333333333335,
          "gap_ms": 500.0
        },
        {
          "after_seconds": 24.957333333333334,
          "gap_ms": 400.0
        },
        {
          "after_seconds": 26.717333333333332,
          "gap_ms": 400.0
        },
        {
          "after_seconds": 51.577333333333335,
          "gap_ms": 400.0
        },
        {
          "after_seconds": 52.537333333333336,
          "gap_ms": 1089.333
        }
      ],
      "response_gaps": [
        {
          "after_seconds": 3.1573333333333333,
          "gap_ms": 1704.0
        },
        {
          "after_seconds": 28.397333333333332,
          "gap_ms": 3884.0
        }
      ]
    },
    "target": {
      "no_response_intervals": [
        {
          "after_seconds": 5.3213333333333335,
          "gap_ms": 540.0
        },
        {
          "after_seconds": 34.26133333333333,
          "gap_ms": 340.0
        },
        {
          "after_seconds": 37.58133333333333,
          "gap_ms": 440.0
        },
        {
          "after_seconds": 40.92133333333334,
          "gap_ms": 540.0
        },
        {
          "after_seconds": 44.601333333333336,
          "gap_ms": 680.0
        }
      ],
      "response_gaps": [
        {
          "after_seconds": 8.161333333333333,
          "gap_ms": 1936.0
        },
        {
          "after_seconds": 47.12133333333333,
          "gap_ms": 3936.0
        }
      ]
    }
  },
  "rms_threshold": 500,
  "speaker_activity": {
    "counterpart": [
      [
        4.8613333333333335,
        5.3213333333333335
      ],
      [
        5.8613333333333335,
        8.161333333333333
      ],
      [
        32.281333333333336,
        34.26133333333333
      ],
      [
        34.601333333333336,
        37.58133333333333
      ],
      [
        38.02133333333333,
        40.92133333333334
      ],
      [
        41.461333333333336,
        44.601333333333336
      ],
      [
        45.281333333333336,
        47.12133333333333
      ]
    ],
    "target": [
      [
        2.3973333333333335,
        3.1573333333333333
      ],
      [
        10.097333333333333,
        14.177333333333333
      ],
      [
        14.597333333333333,
        15.257333333333333
      ],
      [
        16.137333333333334,
        18.197333333333333
      ],
      [
        18.657333333333334,
        20.177333333333333
      ],
      [
        20.737333333333332,
        23.097333333333335
      ],
      [
        23.597333333333335,
        24.957333333333334
      ],
      [
        25.357333333333333,
        26.717333333333332
      ],
      [
        27.117333333333335,
        28.397333333333332
      ],
      [
        51.05733333333333,
        51.577333333333335
      ],
      [
        51.977333333333334,
        52.537333333333336
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
        "item_id": "item_EQgD81GLLo9pSgag4kqFs",
        "largest_gap_ms": 0.0
      },
      {
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "item_id": "item_EQgDZ5QS81ynPwkuD5FhW",
        "largest_gap_ms": 0.0
      }
    ],
    "max_bridge_delivery_delay_ms": 74.10000002384186,
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
    "confidence": 0.64,
    "probabilities": {
      "met": 0.25,
      "not_applicable": 0.72,
      "not_met": 0.01,
      "uncertain": 0.02
    },
    "type": "choice"
  },
  "constraint_behavior": {
    "choice": "met",
    "confidence": 0.67,
    "probabilities": {
      "met": 0.78,
      "not_met": 0.12,
      "uncertain": 0.1
    },
    "type": "choice"
  },
  "context_retention": {
    "choice": "met",
    "confidence": 0.65,
    "probabilities": {
      "met": 0.76,
      "not_met": 0.1,
      "uncertain": 0.14
    },
    "type": "choice"
  },
  "conversation_progress": {
    "choice": "met",
    "confidence": 0.66,
    "probabilities": {
      "met": 0.77,
      "not_met": 0.12,
      "uncertain": 0.11
    },
    "type": "choice"
  },
  "counterpart_validity": {
    "choice": "met",
    "confidence": 0.64,
    "probabilities": {
      "met": 0.76,
      "not_met": 0.1,
      "uncertain": 0.14
    },
    "type": "choice"
  },
  "question_relevance": {
    "choice": "met",
    "confidence": 0.57,
    "probabilities": {
      "met": 0.72,
      "not_met": 0.12,
      "uncertain": 0.16
    },
    "type": "choice"
  },
  "target_role_fidelity": {
    "choice": "met",
    "confidence": 0.48,
    "probabilities": {
      "met": 0.66,
      "not_met": 0.21,
      "uncertain": 0.13
    },
    "type": "choice"
  },
  "user_report_accuracy": {
    "choice": "met",
    "confidence": 0.86,
    "probabilities": {
      "met": 0.89,
      "not_applicable": 0.01,
      "not_met": 0.05,
      "uncertain": 0.05
    },
    "type": "choice"
  }
}
```

Jev is an independent comparison and cannot override verified business records.
All attempts and incomplete stages remain in the batch counts.