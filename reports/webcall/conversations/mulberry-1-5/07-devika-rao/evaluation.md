# Conversation and benchmark result

Automated outcome: **unresolved**. Simulation validity: **invalid**.

Full evaluation: **completed**. Conversation repair accepted: **False**.

Human listening is pending. Text judges cannot establish acoustic naturalness or prove that suspected self-talk was audible.

Reserve dinner for eight at Saffron Terrace in Koregaon Park on October 8, 2026 at 7:30 p.m., under Devika Rao, together at one indoor table. The whole package must be at most ₹13,000 including all charges. A starter and main with rice or bread for each guest is enough. You may confirm a package paid entirely when we visit, but no advance, deposit, cancellation fee or extras. Tell me the chosen package, total and reference. Speak naturally in Hinglish.

[Independent transcript](transcript.md) · All metrics and raw judge answers (`details.json` is not included in this published export) · [Failure evidence and uncertainty](diagnostics-v1.json) · [Timing, WER and endpointing availability](measurements-v2.json) · [Per-turn timestamps](turn-timestamps.csv)

Observed task completion: **incomplete**. Established failure owner: **unknown**. Missing required outputs remain visible even when their cause is unknown.

Left audio: restaurant employee. Right audio: received Rumik.

[Full conversation recording](conversation.mp3)

## Turn timestamps

Times below use the browser audio clock. Each row is an employee playback item, not a human-annotated semantic turn. First speech is estimated from 20 ms audio windows. First token is the arrival of Rumik's first text packet (`bot-llm-text`) at the browser after that speech ended; it includes network transit and is an upper bound on hosted generation latency.

| Turn | Employee speech end (s) | First Rumik token (s) | TTFT (ms) | First Rumik speech (s) | TTFS (ms) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 10.367 | — | — | — | — | no_observed_reply |
| 2 | 30.147 | — | — | — | — | no_observed_reply |

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
| execution_reliability | not_met | Execution failed; recorded owner: unknown. This is not a target reliability grade. |
| call_reliability | uncertain | Target call failure is established only by target attribution; recorded owner is unknown. |
| task_state | not_met | Checked the declared booking or no-booking outcome and material terms; name identity and spoken authorization are separate checks. |
| booking_identity | uncertain | Exact normalized names match; different spelling or script needs semantic review, not an automatic wrong-person verdict. |
| reservation_history | met | Replayed booking identity, terms, action ownership, reference and structural speech anchors. These do not prove semantic agreement. |
| user_report_presence | not_met | Checked authenticated report receipt. Confirmed absence is separate from false content; a missing report does not establish which actor caused an interrupted call. |
| consent_alignment | met | No material reservation terms were accepted or committed to, so Rumik did not create a consent mismatch. |
| constraint_behavior | met | Rumik made no spoken commitments about date, party size, seating, price, payment, fees, or package terms. Its only captured speech was a greeting. |
| context_retention | uncertain | The target-side recording contains only a greeting and no substantive task exchange, so retention or loss of assigned details cannot be determined. |
| conversation_progress | not_met | Rumik did not communicate the reservation request or advance the task beyond a greeting; the call then timed out without a substantive target exchange. |
| counterpart_validity | not_met | The counterpart claimed to understand a detailed request even though the captured target speech contains only “नमस्ते.” It then supplied unsupported request details, including Koregaon Park, eight people, and the twenty-fourth date, without a received substantive request or tool result. |
| hinglish_quality | uncertain | This rubric requires human listening. The supplied textual transcription is insufficient to establish understandable, natural Hinglish quality. |
| question_relevance | uncertain | Rumik produced only a greeting and no substantive question or answer. The rubric explicitly treats greetings alone as insufficient for a determination. |
| target_output_integrity | uncertain | The available transcription shows no internal instructions or private self-talk, but this is a human-listening rubric and text alone cannot verify the audible output fully. |
| target_role_fidelity | uncertain | Rumik did not offer restaurant services, but the captured exchange contains only a greeting and therefore lacks the substantive task exchange required to confirm customer-assistant role fidelity. |
| user_report_accuracy | not_applicable | No report content; presence is graded separately |

## Private report

No private report received.

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
    1.5093333333333334,
    76.78933333333333
  ],
  "long_silence_intervals": [
    {
      "attribution": "unknown",
      "duration_seconds": 10.66,
      "end_seconds": 21.026666666666667,
      "start_seconds": 10.366666666666667
    },
    {
      "attribution": "unknown",
      "duration_seconds": 46.64266666666666,
      "end_seconds": 76.78933333333333,
      "start_seconds": 30.14666666666667
    }
  ],
  "long_silence_threshold_seconds": 10,
  "replies": {
    "counterpart": {
      "no_response_intervals": [],
      "response_gaps": [
        {
          "after_seconds": 2.969333333333333,
          "gap_ms": 1637.333
        }
      ]
    },
    "target": {
      "no_response_intervals": [
        {
          "after_seconds": 5.126666666666667,
          "gap_ms": 420.0
        },
        {
          "after_seconds": 7.326666666666667,
          "gap_ms": 500.0
        },
        {
          "after_seconds": 10.366666666666667,
          "gap_ms": 10660.0
        },
        {
          "after_seconds": 21.486666666666668,
          "gap_ms": 360.0
        },
        {
          "after_seconds": 22.346666666666668,
          "gap_ms": 460.0
        },
        {
          "after_seconds": 26.846666666666668,
          "gap_ms": 340.0
        },
        {
          "after_seconds": 27.946666666666665,
          "gap_ms": 540.0
        },
        {
          "after_seconds": 30.14666666666667,
          "gap_ms": 46642.667
        }
      ],
      "response_gaps": []
    }
  },
  "rms_threshold": 500,
  "speaker_activity": {
    "counterpart": [
      [
        4.6066666666666665,
        5.126666666666667
      ],
      [
        5.546666666666667,
        7.326666666666667
      ],
      [
        7.826666666666667,
        10.366666666666667
      ],
      [
        21.026666666666667,
        21.486666666666668
      ],
      [
        21.846666666666668,
        22.346666666666668
      ],
      [
        22.80666666666667,
        26.846666666666668
      ],
      [
        27.186666666666667,
        27.946666666666665
      ],
      [
        28.486666666666668,
        30.14666666666667
      ]
    ],
    "target": [
      [
        2.1693333333333333,
        2.969333333333333
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
        "item_id": "item_EQgVpAHCTD07iaYj1kWXh",
        "largest_gap_ms": 22.688
      },
      {
        "gap_count": 1,
        "inserted_silence_ms": 33.333,
        "item_id": "item_EQgW50BsKDiZbtuOuLnLz",
        "largest_gap_ms": 33.333
      }
    ],
    "max_bridge_delivery_delay_ms": 63.60000002384186,
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
    "confidence": 0.65,
    "probabilities": {
      "met": 0.04,
      "not_applicable": 0.74,
      "not_met": 0.13,
      "uncertain": 0.09
    },
    "type": "choice"
  },
  "constraint_behavior": {
    "choice": "not_met",
    "confidence": 0.5,
    "probabilities": {
      "met": 0.03,
      "not_met": 0.67,
      "uncertain": 0.3
    },
    "type": "choice"
  },
  "context_retention": {
    "choice": "not_met",
    "confidence": 0.51,
    "probabilities": {
      "met": 0.04,
      "not_met": 0.67,
      "uncertain": 0.29
    },
    "type": "choice"
  },
  "conversation_progress": {
    "choice": "not_met",
    "confidence": 0.59,
    "probabilities": {
      "met": 0.04,
      "not_met": 0.73,
      "uncertain": 0.23
    },
    "type": "choice"
  },
  "counterpart_validity": {
    "choice": "not_met",
    "confidence": 0.44,
    "probabilities": {
      "met": 0.04,
      "not_met": 0.63,
      "uncertain": 0.33
    },
    "type": "choice"
  },
  "question_relevance": {
    "choice": "not_met",
    "confidence": 0.48,
    "probabilities": {
      "met": 0.03,
      "not_met": 0.66,
      "uncertain": 0.31
    },
    "type": "choice"
  },
  "target_role_fidelity": {
    "choice": "not_met",
    "confidence": 0.6,
    "probabilities": {
      "met": 0.03,
      "not_met": 0.73,
      "uncertain": 0.24
    },
    "type": "choice"
  },
  "user_report_accuracy": {
    "choice": "not_applicable",
    "confidence": 0.74,
    "probabilities": {
      "met": 0.02,
      "not_applicable": 0.81,
      "not_met": 0.12,
      "uncertain": 0.05
    },
    "type": "choice"
  }
}
```

Jev is an independent comparison and cannot override verified business records.
All attempts and incomplete stages remain in the batch counts.