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

Times below use the browser audio clock. Each row is an employee playback item, not a human-annotated semantic turn. First speech is estimated from 20 ms audio windows. TTFT is unavailable: Rumik exposes no first-token generation event in this capture. Audio timing does not substitute for TTFT.

| Turn | Employee speech end (s) | First Rumik speech (s) | Response (ms) | Status |
| --- | --- | --- | --- | --- |
| 1 | 9.800 | 12.275 | 2474.667 | answered |
| 2 | 50.640 | 53.035 | 2394.667 | answered |
| 3 | 77.480 | 80.255 | 2774.667 | answered |
| 4 | 110.040 | 113.695 | 3654.667 | answered |

## Evaluation stages

| Stage | Status |
| --- | --- |
| rules | completed |
| openai | completed |
| jev | completed |

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
| user_report_references | uncertain | Compared only explicitly labelled target report references using explicit-reference-clauses-v1. Distinct codes remain distinct. A match checks identifiers only, not overall report accuracy; unsupported prose requires review. |
| user_report_presence | met | Checked authenticated report receipt. Confirmed absence is separate from false content; a missing report does not establish which actor caused an interrupted call. |
| consent_alignment | met | No booking or other material agreement was made. The target stated the requested terms and, after the employee's response, did not agree to a changed time, price, deposit, or other alternative. |
| constraint_behavior | met | The target's captured request respected the known date, party size, indoor seating, single-table/package request, time, and INR 13,000 ceiling. It made no spoken commitment to a deposit, fee, payment, extra, changed date, or changed party size. |
| context_retention | not_met | The target repeated substantially the same date, time, seating, party-size, package, and budget request after its initial request, without a clearly changed term. The transcript shows the repeated request but cannot establish the internal reason for it. |
| conversation_progress | met | The target made a substantive request, received an answer, and ended without making an unauthorized booking or entering a repeated agreement loop. The employee's unsupported availability conclusion is attributed to the counterpart, not the target. |
| counterpart_validity | not_met | The employee's lookup used the wrong year, 2023 instead of the requested 2026, and returned no matching options. The employee then stated that no package under INR 13,000 was available, but the supplied business state includes the suitable 07-simple package at INR 12,400 with no deposit. This was an unsupported business explanation and caused the test to be invalid. |
| hinglish_quality | uncertain | This rubric requires human listening for understandability and natural Hinglish. The supplied transcription and audio metadata are insufficient to establish that judgment. |
| question_relevance | met | The target's questions concerned the requested date, time, party size, seating, dining package, and budget. No unrelated target question or answer is shown. |
| target_output_integrity | uncertain | This is a human-listening rubric. The transcripts show customer-facing reservation speech and no explicit internal instructions, but text alone cannot verify the audible output or rule out leakage acoustically. |
| target_role_fidelity | met | The target acted as the customer assistant: it presented the user's reservation request, asked the restaurant about availability, and closed the call. It did not offer restaurant services or claim to be the restaurant. |
| user_report_accuracy | not_met | The report was present, but it inaccurately stated that no package under INR 13,000 was available. The committed business state lists the suitable 07-simple package at INR 12,400 for the requested date, time, party size, branch, indoor table, and inclusions. No booking was saved, but the stated blocker was false. |

## Private report

No reservation could be made because on 2026-10-08 at 19:30 indoor regular table for 8 guests with a package under INR 13000 was not available at Saffron Terrace, Koregaon Park.

## Business outcome

```json
[]
```

## Silence and response timing

```json
{
  "status": "measured",
  "clock_id": "chromium-audio-context",
  "boundary": "browser_render_and_capture",
  "algorithm": "rms-20ms-merge300ms-v2",
  "rms_threshold": 500,
  "activity_is_not_semantic_turns": true,
  "coverage_seconds": [
    0.6346666666666667,
    120.13333333333334
  ],
  "speaker_activity": {
    "counterpart": [
      [
        3.9,
        4.4
      ],
      [
        4.92,
        6.62
      ],
      [
        7.42,
        9.8
      ],
      [
        32.08,
        32.82
      ],
      [
        33.4,
        36.0
      ],
      [
        36.4,
        39.2
      ],
      [
        39.78,
        43.6
      ],
      [
        44.52,
        45.8
      ],
      [
        46.24,
        48.3
      ],
      [
        48.72,
        50.64
      ],
      [
        64.16,
        64.88
      ],
      [
        65.58,
        67.98
      ],
      [
        68.34,
        71.42
      ],
      [
        72.3,
        74.64
      ],
      [
        75.08,
        77.48
      ],
      [
        95.42,
        95.8
      ],
      [
        96.32,
        97.66
      ],
      [
        98.28,
        100.8
      ],
      [
        101.22,
        104.0
      ],
      [
        104.88,
        107.9
      ],
      [
        108.3,
        110.04
      ]
    ],
    "target": [
      [
        1.6346666666666667,
        2.1746666666666665
      ],
      [
        12.274666666666667,
        18.414666666666665
      ],
      [
        18.814666666666668,
        20.674666666666667
      ],
      [
        21.074666666666666,
        22.974666666666668
      ],
      [
        23.434666666666665,
        25.414666666666665
      ],
      [
        25.834666666666667,
        28.574666666666666
      ],
      [
        53.034666666666666,
        58.294666666666664
      ],
      [
        58.69466666666667,
        62.09466666666667
      ],
      [
        80.25466666666667,
        85.77466666666666
      ],
      [
        86.29466666666667,
        89.63466666666666
      ],
      [
        90.05466666666666,
        92.21466666666667
      ],
      [
        113.69466666666666,
        115.07466666666667
      ]
    ]
  },
  "replies": {
    "target": {
      "response_gaps": [
        {
          "after_seconds": 9.8,
          "gap_ms": 2474.667
        },
        {
          "after_seconds": 50.64,
          "gap_ms": 2394.667
        },
        {
          "after_seconds": 77.48,
          "gap_ms": 2774.667
        },
        {
          "after_seconds": 110.04,
          "gap_ms": 3654.667
        }
      ],
      "no_response_intervals": [
        {
          "after_seconds": 4.4,
          "gap_ms": 520.0
        },
        {
          "after_seconds": 6.62,
          "gap_ms": 800.0
        },
        {
          "after_seconds": 32.82,
          "gap_ms": 580.0
        },
        {
          "after_seconds": 36.0,
          "gap_ms": 400.0
        },
        {
          "after_seconds": 39.2,
          "gap_ms": 580.0
        },
        {
          "after_seconds": 43.6,
          "gap_ms": 920.0
        },
        {
          "after_seconds": 45.8,
          "gap_ms": 440.0
        },
        {
          "after_seconds": 48.3,
          "gap_ms": 420.0
        },
        {
          "after_seconds": 64.88,
          "gap_ms": 700.0
        },
        {
          "after_seconds": 67.98,
          "gap_ms": 360.0
        },
        {
          "after_seconds": 71.42,
          "gap_ms": 880.0
        },
        {
          "after_seconds": 74.64,
          "gap_ms": 440.0
        },
        {
          "after_seconds": 95.8,
          "gap_ms": 520.0
        },
        {
          "after_seconds": 97.66,
          "gap_ms": 620.0
        },
        {
          "after_seconds": 100.8,
          "gap_ms": 420.0
        },
        {
          "after_seconds": 104.0,
          "gap_ms": 880.0
        },
        {
          "after_seconds": 107.9,
          "gap_ms": 400.0
        }
      ]
    },
    "counterpart": {
      "response_gaps": [
        {
          "after_seconds": 2.1746666666666665,
          "gap_ms": 1725.333
        },
        {
          "after_seconds": 28.574666666666666,
          "gap_ms": 3505.333
        },
        {
          "after_seconds": 62.09466666666667,
          "gap_ms": 2065.333
        },
        {
          "after_seconds": 92.21466666666667,
          "gap_ms": 3205.333
        }
      ],
      "no_response_intervals": [
        {
          "after_seconds": 18.414666666666665,
          "gap_ms": 400.0
        },
        {
          "after_seconds": 20.674666666666667,
          "gap_ms": 400.0
        },
        {
          "after_seconds": 22.974666666666668,
          "gap_ms": 460.0
        },
        {
          "after_seconds": 25.414666666666665,
          "gap_ms": 420.0
        },
        {
          "after_seconds": 58.294666666666664,
          "gap_ms": 400.0
        },
        {
          "after_seconds": 85.77466666666666,
          "gap_ms": 520.0
        },
        {
          "after_seconds": 89.63466666666666,
          "gap_ms": 420.0
        },
        {
          "after_seconds": 115.07466666666667,
          "gap_ms": 5058.667
        }
      ]
    }
  },
  "long_silence_threshold_seconds": 10,
  "long_silence_intervals": []
}
```

## Employee speech delivery

Local playback completeness is checked separately from task success. Interruptions still need conversation review; local playback does not prove remote hearing.

```json
{
  "status": "passed",
  "unexplained_cutoffs": [],
  "incomplete_responses": [],
  "target_interruptions": [
    {
      "item_id": "item_EQbQHdK9kzbddIPFbfHpW",
      "generated_ms": 6050.0,
      "played_ms": 6049,
      "interrupted_by_target": true
    }
  ],
  "continuity": {
    "status": "measured",
    "clock_id": "chromium-audio-context",
    "items": [
      {
        "item_id": "item_EQbQHdK9kzbddIPFbfHpW",
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "largest_gap_ms": 0.0
      },
      {
        "item_id": "item_EQbQk1t6T40121cfbEunJ",
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "largest_gap_ms": 0.0
      },
      {
        "item_id": "item_EQbRFehwe2kfgLgcAnegh",
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "largest_gap_ms": 0.0
      },
      {
        "item_id": "item_EQbRlCrxth87oSHEjQAEd",
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "largest_gap_ms": 0.0
      }
    ],
    "max_bridge_delivery_delay_ms": 74.59999996423721,
    "attribution": "unknown",
    "boundary": "Gaps between rendered samples of one generated item; embedded silence is excluded. Source starvation and local scheduling are not distinguished."
  },
  "boundary": "Local playback only; target interruptions still need semantic review."
}
```

## Independent Jev assessment

```json
{
  "consent_alignment": {
    "choice": "not_applicable",
    "confidence": 0.6,
    "probabilities": {
      "met": 0.16,
      "not_applicable": 0.7,
      "not_met": 0.11,
      "uncertain": 0.03
    },
    "type": "choice"
  },
  "constraint_behavior": {
    "choice": "not_met",
    "confidence": 0.41,
    "probabilities": {
      "met": 0.3,
      "not_met": 0.61,
      "uncertain": 0.09
    },
    "type": "choice"
  },
  "context_retention": {
    "choice": "not_met",
    "confidence": 0.4,
    "probabilities": {
      "met": 0.31,
      "not_met": 0.59,
      "uncertain": 0.1
    },
    "type": "choice"
  },
  "conversation_progress": {
    "choice": "not_met",
    "confidence": 0.33,
    "probabilities": {
      "met": 0.37,
      "not_met": 0.55,
      "uncertain": 0.08
    },
    "type": "choice"
  },
  "counterpart_validity": {
    "choice": "not_met",
    "confidence": 0.37,
    "probabilities": {
      "met": 0.32,
      "not_met": 0.58,
      "uncertain": 0.1
    },
    "type": "choice"
  },
  "question_relevance": {
    "choice": "not_met",
    "confidence": 0.45,
    "probabilities": {
      "met": 0.25,
      "not_met": 0.64,
      "uncertain": 0.11
    },
    "type": "choice"
  },
  "target_role_fidelity": {
    "choice": "not_met",
    "confidence": 0.33,
    "probabilities": {
      "met": 0.33,
      "not_met": 0.55,
      "uncertain": 0.12
    },
    "type": "choice"
  },
  "user_report_accuracy": {
    "choice": "met",
    "confidence": 0.39,
    "probabilities": {
      "met": 0.54,
      "not_applicable": 0.01,
      "not_met": 0.38,
      "uncertain": 0.07
    },
    "type": "choice"
  }
}
```

Jev is an independent comparison and cannot override verified business records.
All attempts and incomplete stages remain in the batch counts.