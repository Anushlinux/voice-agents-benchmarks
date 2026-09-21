# Conversation and benchmark result

Automated outcome: **unresolved**. Simulation validity: **invalid**.

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
| 1 | 7.927 | 9.952 | 2025.333 | 10.896 | 2969.333 | answered |
| 2 | 47.767 | 51.493 | 3726.667 | 52.576 | 4809.333 | answered |

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
| booking_identity | uncertain | Exact normalized names match; different spelling or script needs semantic review, not an automatic wrong-person verdict. |
| reservation_history | met | Replayed booking identity, terms, action ownership, reference and structural speech anchors. These do not prove semantic agreement. |
| user_report_references | uncertain | Compared only explicitly labelled target report references using explicit-reference-clauses-v2. Distinct codes remain distinct. A match checks identifiers only, not overall report accuracy; unsupported prose requires review. |
| user_report_presence | met | Checked authenticated report receipt. Confirmed absence is separate from false content; a missing report does not establish which actor caused an interrupted call. |
| consent_alignment | met | The employee asked whether to confirm the reservation, but Rumik did not clearly agree to the offered terms or authorize a booking. No reservation was therefore made without clear consent. |
| constraint_behavior | met | Rumik's captured request communicated the permitted branch, party size, indoor table, booking name, requested time, and dietary requirement, and it made no unauthorized payment, deposit, fee, meal-package, or booking commitment. The later time misunderstanding is assessed under context retention and progress rather than as an unauthorized commitment. |
| context_retention | not_met | The employee's offer described the requested 19:45 indoor table for six and stated that the reservation had no charge. Rumik nevertheless treated the requested time as outside the allowed slot instead of retaining and using the already stated 19:45 requirement. |
| conversation_progress | not_met | The exchange reached a suitable offer and a confirmation question, but Rumik did not answer the confirmation question or proceed. It instead stopped with an incorrect time-mismatch explanation, leaving the task unresolved. |
| counterpart_validity | not_met | The employee used the availability and offer flow and stated several supported terms, but the captured utterance “Table milk” is unrelated to the caller's request and is not a truthful, useful answer. The employee did not invent a booking or unsupported concession, but the irrelevant response prevents full validity. |
| hinglish_quality | uncertain | This rubric requires human listening for intelligibility and naturalness. The supplied transcript alone cannot establish audio quality or natural delivery. |
| question_relevance | not_met | Rumik's initial request and dietary question were relevant, but after the employee's confirmation question, Rumik did not answer it and instead gave an unrelated time-mismatch explanation. The employee's “Table milk” utterance is attributed to the counterpart, not Rumik. |
| target_output_integrity | uncertain | Determining whether the audible output contains internal turn-management instructions or private self-talk requires human audio verification. The transcript does not establish such leakage, but text alone cannot pass this listening-based rubric. |
| target_role_fidelity | met | Rumik acted as the customer's booking assistant: it requested a table reservation, supplied the booking name and constraints, asked about the dietary accommodation, and responded to the employee as the caller. It did not offer restaurant services. |
| user_report_accuracy | not_met | The delivered report says the requested time was 7:50 pm and that it mismatched the allowed 19:45 slot. The actual request and business record concern 19:45, and the business record shows a matching suitable option with no booking saved. The report therefore gives the wrong time and blocker and omits the actual unresolved reason supported by the exchange. |

## Private report

Could not book: requested time 7:50 pm does not match allowed reservation time 19:45 for 5 October 2026.

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
    1.536,
    59.256
  ],
  "long_silence_intervals": [],
  "long_silence_threshold_seconds": 10,
  "replies": {
    "counterpart": {
      "no_response_intervals": [
        {
          "after_seconds": 16.716,
          "gap_ms": 460.0
        },
        {
          "after_seconds": 19.076,
          "gap_ms": 320.0
        },
        {
          "after_seconds": 20.496,
          "gap_ms": 420.0
        },
        {
          "after_seconds": 22.816,
          "gap_ms": 440.0
        },
        {
          "after_seconds": 55.696,
          "gap_ms": 420.0
        },
        {
          "after_seconds": 58.356,
          "gap_ms": 900.0
        }
      ],
      "response_gaps": [
        {
          "after_seconds": 3.036,
          "gap_ms": 1570.667
        },
        {
          "after_seconds": 25.576,
          "gap_ms": 3790.667
        }
      ]
    },
    "target": {
      "no_response_intervals": [
        {
          "after_seconds": 5.1466666666666665,
          "gap_ms": 580.0
        },
        {
          "after_seconds": 32.766666666666666,
          "gap_ms": 380.0
        },
        {
          "after_seconds": 34.446666666666665,
          "gap_ms": 420.0
        },
        {
          "after_seconds": 37.04666666666667,
          "gap_ms": 640.0
        },
        {
          "after_seconds": 39.306666666666665,
          "gap_ms": 400.0
        },
        {
          "after_seconds": 41.14666666666667,
          "gap_ms": 680.0
        },
        {
          "after_seconds": 44.846666666666664,
          "gap_ms": 640.0
        }
      ],
      "response_gaps": [
        {
          "after_seconds": 7.926666666666667,
          "gap_ms": 2969.333
        },
        {
          "after_seconds": 47.766666666666666,
          "gap_ms": 4809.333
        }
      ]
    }
  },
  "rms_threshold": 500,
  "speaker_activity": {
    "counterpart": [
      [
        4.6066666666666665,
        5.1466666666666665
      ],
      [
        5.726666666666667,
        7.926666666666667
      ],
      [
        29.366666666666667,
        32.766666666666666
      ],
      [
        33.14666666666667,
        34.446666666666665
      ],
      [
        34.86666666666667,
        37.04666666666667
      ],
      [
        37.68666666666667,
        39.306666666666665
      ],
      [
        39.70666666666666,
        41.14666666666667
      ],
      [
        41.82666666666667,
        44.846666666666664
      ],
      [
        45.486666666666665,
        47.766666666666666
      ]
    ],
    "target": [
      [
        2.416,
        3.036
      ],
      [
        10.896,
        16.716
      ],
      [
        17.176,
        19.076
      ],
      [
        19.396,
        20.496
      ],
      [
        20.916,
        22.816
      ],
      [
        23.256,
        25.576
      ],
      [
        52.576,
        55.696
      ],
      [
        56.116,
        58.356
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
        "inserted_silence_ms": 33.354,
        "item_id": "item_EQggF1HLEYNXQ0umGHwak",
        "largest_gap_ms": 33.354
      },
      {
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "item_id": "item_EQggd7GMOQ9x7ZMfTSNvt",
        "largest_gap_ms": 0.0
      }
    ],
    "max_bridge_delivery_delay_ms": 70.5,
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
    "confidence": 0.63,
    "probabilities": {
      "met": 0.11,
      "not_applicable": 0.73,
      "not_met": 0.13,
      "uncertain": 0.03
    },
    "type": "choice"
  },
  "constraint_behavior": {
    "choice": "not_met",
    "confidence": 0.6,
    "probabilities": {
      "met": 0.14,
      "not_met": 0.73,
      "uncertain": 0.13
    },
    "type": "choice"
  },
  "context_retention": {
    "choice": "not_met",
    "confidence": 0.58,
    "probabilities": {
      "met": 0.15,
      "not_met": 0.72,
      "uncertain": 0.13
    },
    "type": "choice"
  },
  "conversation_progress": {
    "choice": "not_met",
    "confidence": 0.52,
    "probabilities": {
      "met": 0.2,
      "not_met": 0.68,
      "uncertain": 0.12
    },
    "type": "choice"
  },
  "counterpart_validity": {
    "choice": "not_met",
    "confidence": 0.51,
    "probabilities": {
      "met": 0.18,
      "not_met": 0.68,
      "uncertain": 0.14
    },
    "type": "choice"
  },
  "question_relevance": {
    "choice": "not_met",
    "confidence": 0.57,
    "probabilities": {
      "met": 0.14,
      "not_met": 0.71,
      "uncertain": 0.15
    },
    "type": "choice"
  },
  "target_role_fidelity": {
    "choice": "not_met",
    "confidence": 0.57,
    "probabilities": {
      "met": 0.14,
      "not_met": 0.71,
      "uncertain": 0.15
    },
    "type": "choice"
  },
  "user_report_accuracy": {
    "choice": "not_met",
    "confidence": 0.64,
    "probabilities": {
      "met": 0.18,
      "not_applicable": 0.01,
      "not_met": 0.73,
      "uncertain": 0.08
    },
    "type": "choice"
  }
}
```

Jev is an independent comparison and cannot override verified business records.
All attempts and incomplete stages remain in the batch counts.