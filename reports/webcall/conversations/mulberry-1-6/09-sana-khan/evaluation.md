# Conversation and benchmark result

Automated outcome: **passed**. Simulation validity: **valid**.

Full evaluation: **completed**. Conversation repair accepted: **True**.

Human listening is pending. Text judges cannot establish acoustic naturalness or prove that suspected self-talk was audible.

Arrange dinner for six at Copper Mango in Greater Kailash on October 10, 2026 at 8 p.m., under Sana Khan, together at one indoor table. We need a starter and main with rice or bread each, and ₹9,000 is the absolute total limit including all charges. You can ask for a better price and agree to pay at the visit, but no deposit, cancellation fee or extras. If it cannot fit, do not book and tell me why. Speak naturally in Hinglish.

[Independent transcript](transcript.md) · All metrics and raw judge answers (`details.json` is not included in this published export) · [Failure evidence and uncertainty](diagnostics-v1.json) · [Timing, WER and endpointing availability](measurements-v2.json) · [Per-turn timestamps](turn-timestamps.csv)

Observed task completion: **completed**. Established failure owner: **unknown**. Missing required outputs remain visible even when their cause is unknown.

Left audio: restaurant employee. Right audio: received Rumik.

[Full conversation recording](conversation.mp3)

## Turn timestamps

Times below use the browser audio clock. Each row is an employee playback item, not a human-annotated semantic turn. First speech is estimated from 20 ms audio windows. First token is the arrival of Rumik's first text packet (`bot-llm-text`) at the browser after that speech ended; it includes network transit and is an upper bound on hosted generation latency.

| Turn | Employee speech end (s) | First Rumik token (s) | TTFT (ms) | First Rumik speech (s) | TTFS (ms) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 8.307 | 12.779 | 4472.000 | 13.740 | 5433.333 | answered |
| 2 | 50.587 | 53.627 | 3040.000 | 54.680 | 4093.333 | answered |

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
| constraint_behavior | met | Rumik stated the requested date, party size, branch, indoor table, inclusions, booking name, and INR 9,000 limit, and made no unauthorized booking or financial commitment. The final report correctly declined the INR 9,600 option. |
| context_retention | met | Rumik communicated the relevant assignment details in one request and did not repeat already-established questions or terms before ending the call. |
| conversation_progress | met | The exchange progressed from the request to an availability response and a confirmation question. Rumik then ended without committing to an option that exceeded the user's limit. |
| counterpart_validity | met | The employee used an availability lookup, described an indoor table for six with the requested inclusions, and asked for confirmation rather than claiming a booking. The tool records show the offered total was INR 9,600 and no reservation was saved. |
| hinglish_quality | uncertain | This rubric requires human listening for understandability and naturalness; the supplied transcription alone cannot establish it. |
| question_relevance | met | Rumik's request asks the employee to check the relevant reservation, and the employee's confirmation question is directly related to the requested booking. Rumik's closing is not an unrelated question or answer. |
| target_output_integrity | uncertain | This is a human-listening-only rubric. The transcription shows customer-facing speech, but text alone cannot verify whether the audible output contained internal instructions or private self-talk. |
| target_role_fidelity | met | Rumik acted as the customer's assistant by requesting a reservation and asking the restaurant to check availability; it did not present itself as restaurant staff or offer restaurant services. |
| user_report_accuracy | met | The authenticated report accurately states that no booking was made because the available INR 9,600 total exceeded the INR 9,000 limit. This matches the final business record, which contains no booking. |
| consent_alignment | not_applicable | Review the actual conversation and outcome |

## Private report

Cannot book because the total charge of INR 9,600 exceeds the allowed limit of INR 9,000.

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
    1.76,
    56.730666666666664
  ],
  "long_silence_intervals": [],
  "long_silence_threshold_seconds": 10,
  "replies": {
    "counterpart": {
      "no_response_intervals": [
        {
          "after_seconds": 19.96,
          "gap_ms": 460.0
        },
        {
          "after_seconds": 22.68,
          "gap_ms": 440.0
        },
        {
          "after_seconds": 26.1,
          "gap_ms": 540.0
        },
        {
          "after_seconds": 28.08,
          "gap_ms": 480.0
        },
        {
          "after_seconds": 29.82,
          "gap_ms": 500.0
        },
        {
          "after_seconds": 55.9,
          "gap_ms": 830.667
        }
      ],
      "response_gaps": [
        {
          "after_seconds": 3.14,
          "gap_ms": 1986.667
        },
        {
          "after_seconds": 31.6,
          "gap_ms": 4006.667
        }
      ]
    },
    "target": {
      "no_response_intervals": [
        {
          "after_seconds": 5.6466666666666665,
          "gap_ms": 460.0
        },
        {
          "after_seconds": 40.56666666666667,
          "gap_ms": 380.0
        },
        {
          "after_seconds": 43.986666666666665,
          "gap_ms": 460.0
        },
        {
          "after_seconds": 46.526666666666664,
          "gap_ms": 680.0
        }
      ],
      "response_gaps": [
        {
          "after_seconds": 8.306666666666667,
          "gap_ms": 5433.333
        },
        {
          "after_seconds": 50.586666666666666,
          "gap_ms": 4093.333
        }
      ]
    }
  },
  "rms_threshold": 500,
  "speaker_activity": {
    "counterpart": [
      [
        5.126666666666667,
        5.6466666666666665
      ],
      [
        6.1066666666666665,
        8.306666666666667
      ],
      [
        35.60666666666667,
        40.56666666666667
      ],
      [
        40.946666666666665,
        43.986666666666665
      ],
      [
        44.446666666666665,
        46.526666666666664
      ],
      [
        47.20666666666666,
        50.586666666666666
      ]
    ],
    "target": [
      [
        2.62,
        3.14
      ],
      [
        13.74,
        19.96
      ],
      [
        20.42,
        22.68
      ],
      [
        23.12,
        26.1
      ],
      [
        26.64,
        28.08
      ],
      [
        28.56,
        29.82
      ],
      [
        30.32,
        31.6
      ],
      [
        54.68,
        55.9
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
        "item_id": "item_EQgaBOJbXHFHgmrgfMBvU",
        "largest_gap_ms": 33.354
      },
      {
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "item_id": "item_EQgafhQjjUIqdSy4ttPtX",
        "largest_gap_ms": 0.0
      }
    ],
    "max_bridge_delivery_delay_ms": 77.5,
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
    "confidence": 0.62,
    "probabilities": {
      "met": 0.21,
      "not_applicable": 0.71,
      "not_met": 0.04,
      "uncertain": 0.04
    },
    "type": "choice"
  },
  "constraint_behavior": {
    "choice": "met",
    "confidence": 0.42,
    "probabilities": {
      "met": 0.62,
      "not_met": 0.26,
      "uncertain": 0.12
    },
    "type": "choice"
  },
  "context_retention": {
    "choice": "met",
    "confidence": 0.36,
    "probabilities": {
      "met": 0.57,
      "not_met": 0.25,
      "uncertain": 0.18
    },
    "type": "choice"
  },
  "conversation_progress": {
    "choice": "met",
    "confidence": 0.37,
    "probabilities": {
      "met": 0.58,
      "not_met": 0.28,
      "uncertain": 0.14
    },
    "type": "choice"
  },
  "counterpart_validity": {
    "choice": "met",
    "confidence": 0.25,
    "probabilities": {
      "met": 0.5,
      "not_met": 0.34,
      "uncertain": 0.16
    },
    "type": "choice"
  },
  "question_relevance": {
    "choice": "met",
    "confidence": 0.24,
    "probabilities": {
      "met": 0.5,
      "not_met": 0.31,
      "uncertain": 0.19
    },
    "type": "choice"
  },
  "target_role_fidelity": {
    "choice": "met",
    "confidence": 0.23,
    "probabilities": {
      "met": 0.48,
      "not_met": 0.35,
      "uncertain": 0.17
    },
    "type": "choice"
  },
  "user_report_accuracy": {
    "choice": "met",
    "confidence": 0.76,
    "probabilities": {
      "met": 0.8099999999999999,
      "not_applicable": 0.01,
      "not_met": 0.11,
      "uncertain": 0.07
    },
    "type": "choice"
  }
}
```

Jev is an independent comparison and cannot override verified business records.
All attempts and incomplete stages remain in the batch counts.