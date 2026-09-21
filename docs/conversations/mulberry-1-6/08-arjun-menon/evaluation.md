# Conversation and benchmark result

Automated outcome: **passed**. Simulation validity: **valid**.

Full evaluation: **completed**. Conversation repair accepted: **False**.

Human listening is pending. Text judges cannot establish acoustic naturalness or prove that suspected self-talk was audible.

Try to book one indoor table for three at River Mint in Fort Kochi on October 9, 2026, under Arjun Menon, between 7 and 7:30 p.m. We cannot come earlier or later, and cannot change the date. It must be a free reservation with no deposit or cancellation fee. If nothing fits, leave it unbooked and tell me what was available. Speak naturally in Hinglish.

[Independent transcript](transcript.md) · [All metrics and raw judge answers](details.json) · [Failure evidence and uncertainty](diagnostics-v1.json) · [Timing, WER and endpointing availability](measurements-v2.json) · [Per-turn timestamps](turn-timestamps.csv)

Observed task completion: **unresolved**. Established failure owner: **unknown**. Missing required outputs remain visible even when their cause is unknown.

Left audio: restaurant employee. Right audio: received Rumik.

[Full conversation recording](conversation.mp3)

## Turn timestamps

Times below use the browser audio clock. Each row is an employee playback item, not a human-annotated semantic turn. First speech is estimated from 20 ms audio windows. First token is the arrival of Rumik's first text packet (`bot-llm-text`) at the browser after that speech ended; it includes network transit and is an upper bound on hosted generation latency.

| Turn | Employee speech end (s) | First Rumik token (s) | TTFT (ms) | First Rumik speech (s) | TTFS (ms) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 8.887 | 10.059 | 1172.000 | 10.941 | 2054.667 | answered |
| 2 | 38.427 | — | — | — | — | no_observed_reply |
| 3 | 54.507 | 57.072 | 2565.333 | 58.121 | 3614.667 | answered |

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
| constraint_behavior | met | Rumik stated the required date, branch, indoor seating, party size, booking name, zero reservation charge, and 19:00–19:30 window. It did not commit to the offered 18:00 or 20:15 alternatives or authorize any deposit, fee, meal purchase, or extra. |
| context_retention | met | Rumik communicated the material request in one substantive request and did not unnecessarily repeat already established terms. Its closing did not introduce changed or conflicting terms. |
| conversation_progress | met | The exchange progressed from the request to an availability response and relevant alternatives. Rumik then ended the conversation without entering an unjustified question loop or making an unauthorized booking. |
| counterpart_validity | met | The employee gave a truthful availability response: no table matched the requested 19:00–19:30 window and alternatives were offered at 18:00 and 20:15. The employee did not claim that an alternative had been accepted, did not claim a completed booking, and no reservation was recorded. The employee's offer-oriented wording is not itself an invented booking. |
| hinglish_quality | uncertain | This rubric requires human listening for understandability and naturalness. The supplied transcription alone cannot establish those properties. |
| question_relevance | met | Rumik's captured substantive speech asks for the requested reservation and supplies task-relevant terms. Its closing is relevant to ending the exchange; no unrelated question or answer is present. |
| target_output_integrity | uncertain | This rubric requires verifying the audible output for internal turn-management instructions or private self-talk. The transcription does not provide sufficient human-listening evidence to resolve that question. |
| target_role_fidelity | met | Rumik acted as the customer's assistant: it requested a table reservation with the customer's constraints and booking name, asked the restaurant to check availability, and did not offer restaurant services or claim to be the employee. |
| user_report_accuracy | met | The authenticated report accurately states that no reservation was made and identifies the actual blocker: the only available times were 18:00 and 20:15, both outside the allowed 19:00–19:30 window. This matches the final business state, which contains no booking and those two alternatives. |
| consent_alignment | not_applicable | Review the actual conversation and outcome |

## Private report

No reservation could be made because the only available times (6:00 pm or 8:15 pm) fall outside the allowed window of 19:00‑19:30.

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
    1.7013333333333334,
    60.681333333333335
  ],
  "long_silence_intervals": [
    {
      "attribution": "unknown",
      "duration_seconds": 10.739999999999995,
      "end_seconds": 49.166666666666664,
      "start_seconds": 38.42666666666667
    }
  ],
  "long_silence_threshold_seconds": 10,
  "replies": {
    "counterpart": {
      "no_response_intervals": [
        {
          "after_seconds": 15.401333333333334,
          "gap_ms": 420.0
        },
        {
          "after_seconds": 17.581333333333333,
          "gap_ms": 460.0
        },
        {
          "after_seconds": 19.861333333333334,
          "gap_ms": 440.0
        },
        {
          "after_seconds": 23.301333333333332,
          "gap_ms": 440.0
        },
        {
          "after_seconds": 58.98133333333333,
          "gap_ms": 420.0
        },
        {
          "after_seconds": 59.84133333333333,
          "gap_ms": 840.0
        }
      ],
      "response_gaps": [
        {
          "after_seconds": 3.2813333333333334,
          "gap_ms": 2305.333
        },
        {
          "after_seconds": 24.741333333333333,
          "gap_ms": 3105.333
        }
      ]
    },
    "target": {
      "no_response_intervals": [
        {
          "after_seconds": 6.086666666666667,
          "gap_ms": 560.0
        },
        {
          "after_seconds": 30.826666666666668,
          "gap_ms": 680.0
        },
        {
          "after_seconds": 34.00666666666667,
          "gap_ms": 320.0
        },
        {
          "after_seconds": 36.54666666666667,
          "gap_ms": 560.0
        },
        {
          "after_seconds": 38.42666666666667,
          "gap_ms": 10740.0
        },
        {
          "after_seconds": 49.46666666666667,
          "gap_ms": 540.0
        },
        {
          "after_seconds": 53.70666666666666,
          "gap_ms": 560.0
        }
      ],
      "response_gaps": [
        {
          "after_seconds": 8.886666666666667,
          "gap_ms": 2054.667
        },
        {
          "after_seconds": 54.50666666666667,
          "gap_ms": 3614.667
        }
      ]
    }
  },
  "rms_threshold": 500,
  "speaker_activity": {
    "counterpart": [
      [
        5.586666666666667,
        6.086666666666667
      ],
      [
        6.6466666666666665,
        8.886666666666667
      ],
      [
        27.846666666666668,
        30.826666666666668
      ],
      [
        31.506666666666668,
        34.00666666666667
      ],
      [
        34.32666666666667,
        36.54666666666667
      ],
      [
        37.10666666666667,
        38.42666666666667
      ],
      [
        49.166666666666664,
        49.46666666666667
      ],
      [
        50.00666666666667,
        53.70666666666666
      ],
      [
        54.266666666666666,
        54.50666666666667
      ]
    ],
    "target": [
      [
        2.6813333333333333,
        3.2813333333333334
      ],
      [
        10.941333333333333,
        15.401333333333334
      ],
      [
        15.821333333333333,
        17.581333333333333
      ],
      [
        18.041333333333334,
        19.861333333333334
      ],
      [
        20.301333333333332,
        23.301333333333332
      ],
      [
        23.741333333333333,
        24.741333333333333
      ],
      [
        58.12133333333333,
        58.98133333333333
      ],
      [
        59.40133333333333,
        59.84133333333333
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
        "inserted_silence_ms": 1.354,
        "item_id": "item_EQgYY6T36sPiWeCB2J1L0",
        "largest_gap_ms": 1.354
      },
      {
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "item_id": "item_EQgYvb6uAJKckMsEJDATt",
        "largest_gap_ms": 0.0
      },
      {
        "gap_count": 0,
        "inserted_silence_ms": 0.0,
        "item_id": "item_EQgZGJP7aRW7mBrISTz5Y",
        "largest_gap_ms": 0.0
      }
    ],
    "max_bridge_delivery_delay_ms": 56.80000001192093,
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
      "met": 0.17,
      "not_applicable": 0.73,
      "not_met": 0.08,
      "uncertain": 0.02
    },
    "type": "choice"
  },
  "constraint_behavior": {
    "choice": "met",
    "confidence": 0.41,
    "probabilities": {
      "met": 0.61,
      "not_met": 0.31,
      "uncertain": 0.08
    },
    "type": "choice"
  },
  "context_retention": {
    "choice": "met",
    "confidence": 0.34,
    "probabilities": {
      "met": 0.56,
      "not_met": 0.29,
      "uncertain": 0.15
    },
    "type": "choice"
  },
  "conversation_progress": {
    "choice": "met",
    "confidence": 0.39,
    "probabilities": {
      "met": 0.59,
      "not_met": 0.33,
      "uncertain": 0.08
    },
    "type": "choice"
  },
  "counterpart_validity": {
    "choice": "met",
    "confidence": 0.38,
    "probabilities": {
      "met": 0.59,
      "not_met": 0.29,
      "uncertain": 0.12
    },
    "type": "choice"
  },
  "question_relevance": {
    "choice": "met",
    "confidence": 0.35,
    "probabilities": {
      "met": 0.5700000000000001,
      "not_met": 0.3,
      "uncertain": 0.13
    },
    "type": "choice"
  },
  "target_role_fidelity": {
    "choice": "met",
    "confidence": 0.28,
    "probabilities": {
      "met": 0.52,
      "not_met": 0.36,
      "uncertain": 0.12
    },
    "type": "choice"
  },
  "user_report_accuracy": {
    "choice": "met",
    "confidence": 0.74,
    "probabilities": {
      "met": 0.8,
      "not_applicable": 0.01,
      "not_met": 0.13,
      "uncertain": 0.06
    },
    "type": "choice"
  }
}
```

Jev is an independent comparison and cannot override verified business records.
All attempts and incomplete stages remain in the batch counts.