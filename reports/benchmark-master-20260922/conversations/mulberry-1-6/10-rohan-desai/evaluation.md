# Conversation and benchmark result

Automated outcome: **failed**. Simulation validity: **valid**.

Full evaluation: **completed**. Conversation repair accepted: **False**.

Human listening is pending. Text judges cannot establish acoustic naturalness or prove that suspected self-talk was audible.

Please book one indoor table for five at Clay Bowl in Alkapuri on October 11, 2026 at 7:15 p.m., under Rohan Desai. Two guests need food containing neither onion nor garlic; it is a food preference, not an allergy. Book only if the kitchen can meet both exclusions for both people. We will order meals there, and there must be no booking charge, deposit or cancellation fee. Otherwise leave it unbooked and explain why. Speak naturally in Hinglish.

[Independent transcript](transcript.md) · [All metrics and raw judge answers](details.json) · [Failure evidence and uncertainty](diagnostics-v1.json) · [Timing, WER and endpointing availability](measurements-v2.json) · [Per-turn timestamps](turn-timestamps.csv)

Observed task completion: **unresolved**. Established failure owner: **unknown**. Missing required outputs remain visible even when their cause is unknown.

Left audio: restaurant employee. Right audio: received Rumik.

[Full conversation recording](conversation.mp3)

## Turn timestamps

Times below use the browser audio clock. Each row is an employee playback item, not a human-annotated semantic turn. First speech is estimated from 20 ms audio windows. First token is the arrival of Rumik's first text packet (`bot-llm-text`) at the browser after that speech ended; it includes network transit and is an upper bound on hosted generation latency.

| Turn | Employee speech end (s) | First Rumik token (s) | TTFT (ms) | First Rumik speech (s) | TTFS (ms) | Status |
| --- | --- | --- | --- | --- | --- | --- |

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
| constraint_behavior | met | Rumik stated the requested date, party size, branch, indoor table, booking name, and dietary requirement, then declined to book after the restaurant explained that the required onion-and-garlic-free food was unavailable. It did not agree to a charge, deposit, fee, extra, or unauthorized alternative. |
| context_retention | met | Rumik did not unnecessarily repeat already stated requirements. After receiving the dietary limitation and booking question, it made the appropriate no-booking decision. |
| conversation_progress | met | The exchange progressed from the request to the restaurant's limitation and then to an appropriate refusal to book. There was no repeated agreement or question loop. |
| counterpart_validity | met | The employee answered the request consistently with the restaurant facts, reported that the required dietary accommodation was unavailable, offered only the available table as an unaccepted alternative, and did not claim a booking or invent a reference. The failed dietary-capacity check supports the stated limitation. |
| hinglish_quality | uncertain | The supplied transcription shows a plausible Hinglish exchange, but this rubric requires human listening. Text and transcription alone cannot establish naturalness or understandability. |
| question_relevance | met | Rumik's substantive response accepted the restaurant's dietary limitation and declined the booking. Its closing offer to help further was relevant to ending the call; no unrelated question or answer appears. |
| target_output_integrity | uncertain | The transcription contains only caller-facing conversation and no apparent internal instructions, but this diagnostic requires verification from the captured audio. Text alone cannot establish the audible output's integrity. |
| target_role_fidelity | met | Rumik acted as the customer's assistant: it presented the user's reservation request, included the dietary condition, and responded as the caller by declining the unsuitable booking. It did not offer restaurant services or impersonate the employee. |
| user_report_accuracy | not_met | The report correctly states that no reservation was booked and identifies the dietary blocker, but it omits material requirements that were relevant to the attempted booking, including the specified seating and reservation details. The final business state confirms that no booking existed and that the dietary capacity was zero. |
| consent_alignment | not_applicable | Review the actual conversation and outcome |

## Private report

Reservation not booked because onion‑garlic free meals are not available.

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
    1.504,
    63.704
  ],
  "long_silence_intervals": [],
  "long_silence_threshold_seconds": 10,
  "replies": {
    "counterpart": {
      "no_response_intervals": [
        {
          "after_seconds": 13.364,
          "gap_ms": 480.0
        },
        {
          "after_seconds": 17.504,
          "gap_ms": 360.0
        },
        {
          "after_seconds": 19.924,
          "gap_ms": 480.0
        },
        {
          "after_seconds": 23.004,
          "gap_ms": 440.0
        },
        {
          "after_seconds": 60.584,
          "gap_ms": 3120.0
        }
      ],
      "response_gaps": [
        {
          "after_seconds": 3.144,
          "gap_ms": 1622.667
        },
        {
          "after_seconds": 24.684,
          "gap_ms": 6702.667
        },
        {
          "after_seconds": 50.724,
          "gap_ms": 1842.667
        }
      ]
    },
    "target": {
      "no_response_intervals": [
        {
          "after_seconds": 31.966666666666665,
          "gap_ms": 380.0
        },
        {
          "after_seconds": 35.96666666666667,
          "gap_ms": 540.0
        },
        {
          "after_seconds": 40.126666666666665,
          "gap_ms": 500.0
        },
        {
          "after_seconds": 43.166666666666664,
          "gap_ms": 560.0
        },
        {
          "after_seconds": 53.06666666666667,
          "gap_ms": 340.0
        },
        {
          "after_seconds": 55.10666666666667,
          "gap_ms": 480.0
        }
      ],
      "response_gaps": [
        {
          "after_seconds": 6.886666666666667,
          "gap_ms": 2137.333
        },
        {
          "after_seconds": 45.406666666666666,
          "gap_ms": 3697.333
        },
        {
          "after_seconds": 56.846666666666664,
          "gap_ms": 2497.333
        }
      ]
    }
  },
  "rms_threshold": 500,
  "speaker_activity": {
    "counterpart": [
      [
        4.766666666666667,
        6.886666666666667
      ],
      [
        31.386666666666667,
        31.966666666666665
      ],
      [
        32.346666666666664,
        35.96666666666667
      ],
      [
        36.50666666666667,
        40.126666666666665
      ],
      [
        40.626666666666665,
        43.166666666666664
      ],
      [
        43.72666666666667,
        45.406666666666666
      ],
      [
        52.56666666666667,
        53.06666666666667
      ],
      [
        53.406666666666666,
        55.10666666666667
      ],
      [
        55.586666666666666,
        56.846666666666664
      ]
    ],
    "target": [
      [
        2.524,
        3.144
      ],
      [
        9.024,
        13.364
      ],
      [
        13.844,
        17.504
      ],
      [
        17.864,
        19.924
      ],
      [
        20.404,
        23.004
      ],
      [
        23.444,
        24.684
      ],
      [
        49.104,
        50.724
      ],
      [
        59.344,
        60.584
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
  "reason": "No final per-item playback evidence",
  "status": "unresolved"
}
```

## Independent Jev assessment

```json
{
  "consent_alignment": {
    "choice": "not_applicable",
    "confidence": 0.67,
    "probabilities": {
      "met": 0.23,
      "not_applicable": 0.75,
      "not_met": 0.01,
      "uncertain": 0.01
    },
    "type": "choice"
  },
  "constraint_behavior": {
    "choice": "met",
    "confidence": 0.75,
    "probabilities": {
      "met": 0.83,
      "not_met": 0.1,
      "uncertain": 0.07
    },
    "type": "choice"
  },
  "context_retention": {
    "choice": "met",
    "confidence": 0.68,
    "probabilities": {
      "met": 0.79,
      "not_met": 0.08,
      "uncertain": 0.13
    },
    "type": "choice"
  },
  "conversation_progress": {
    "choice": "met",
    "confidence": 0.74,
    "probabilities": {
      "met": 0.83,
      "not_met": 0.1,
      "uncertain": 0.07
    },
    "type": "choice"
  },
  "counterpart_validity": {
    "choice": "met",
    "confidence": 0.75,
    "probabilities": {
      "met": 0.83,
      "not_met": 0.08,
      "uncertain": 0.09
    },
    "type": "choice"
  },
  "question_relevance": {
    "choice": "met",
    "confidence": 0.71,
    "probabilities": {
      "met": 0.81,
      "not_met": 0.09,
      "uncertain": 0.1
    },
    "type": "choice"
  },
  "target_role_fidelity": {
    "choice": "met",
    "confidence": 0.62,
    "probabilities": {
      "met": 0.74,
      "not_met": 0.16,
      "uncertain": 0.1
    },
    "type": "choice"
  },
  "user_report_accuracy": {
    "choice": "met",
    "confidence": 0.73,
    "probabilities": {
      "met": 0.8,
      "not_applicable": 0,
      "not_met": 0.15,
      "uncertain": 0.05
    },
    "type": "choice"
  }
}
```

Jev is an independent comparison and cannot override verified business records.
All attempts and incomplete stages remain in the batch counts.