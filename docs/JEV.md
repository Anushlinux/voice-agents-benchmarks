# Jev comparison over saved evidence

Jev is an optional TypeSafe evaluator, separate from the OpenAI audio counterpart.
It answers Choice, Score or Noul questions about text and structured evidence.
It does not listen to calls or establish whether a user received a report.

The integration uses the [official HTTP API](https://docs.typesafe.ai/api) through
the existing HTTP client. No LangChain or LangSmith installation or upload is
needed. The [LangChain experiment](https://www.langchain.com/blog/jev-agent-evals-langsmith)
used five fixed examples; it does not validate a judge on our Hinglish conversations.

## Shadow mode

Answers are recorded for comparison with human review. They cannot replace
deterministic metrics or the benchmark verdict. Batch reports and human review
reject a shadow result as their source grade. Scores retain their original
scales and probabilities; no pass threshold or accuracy claim is invented.

Inputs contain saved captured-audio transcripts from an existing model evaluation,
the user task, counterpart brief, role-specific tool grants, case criteria, and
initial/final business records and audits. A saved OpenAI evaluation currently
supplies those transcripts. Jev does not transcribe again or run OpenAI.
Received audio plus played audio are selected; submitted audio is the fallback
if played is absent. Submitted audio need not have been heard remotely. Earlier
judge answers are excluded to avoid biasing the comparison.

Raw recordings are not uploaded to TypeSafe. Saved text and selected task/business
evidence are uploaded only by `jev evaluate --live`. Preparation, planning,
imports and status remain provider-free. Keep evidence-bearing files under ignored
`artifacts/`, `reports/` or `datasets/` directories.

## Configuration and offline preparation

Add this section to an ignored local benchmark configuration:

```toml
[jev]
model = "" # Choose an explicit model; prefer a versioned ID for comparisons.
cost_ceiling_inr = "0" # Set a funded conservative ceiling before live use.
timeout_seconds = 30
max_request_bytes = 100000
```

The byte cap is an operator limit, not a token estimate. Oversized requests fail
locally without truncation. This version sends one request per attempt.

Author an independent JSON rubric with `version` and a `questions` object. Each
named question has `type` and `instructions`. `choice` requires a map of option
names to descriptions; `score` requires 2–10 ordered descriptions; `noul` may
include `criteria` with `true` and `false` descriptions. Ask atomic questions
about properties observable from text. Include an insufficient-evidence choice
where appropriate. Rubric content remains a separate workstream; no benchmark
dataset or grading thresholds are generated here.

```sh
voice-bench jev prepare "$ATTEMPT_DIRECTORY" \
  --source-version judged-v1 --rubric datasets/jev-rubric.json \
  --config configs/live.local.toml --output reports/jev-request.json
```

Preparation checks sealed artifacts and audio citation ranges. The output contains
the exact request, source-evaluation hash, raw-manifest hash, rubric and config.
It contains no API key and fails rather than overwriting an existing file.

## Explicit paid execution

For a separately authorized evaluation, export `TYPESAFE_API_KEY` and
`DATABASE_URL`, then run:

```sh
voice-bench jev evaluate "$ATTEMPT_DIRECTORY" \
  --source-version judged-v1 --rubric datasets/jev-rubric.json \
  --config configs/live.local.toml --version jev-v1 --live
```

The Jev ceiling is reserved against the original batch's funded budget before
dispatch. Errors retain the reservation; billing is not guessed. No automatic
retry occurs. Existing versions cannot be reused.

`evaluation/jev-v1/request.json` preserves inputs before network activity.
`evaluation/jev-v1/result.json` preserves the raw response, validated answers,
requested/resolved model, provider usage, elapsed time and any error type.
Timeouts and malformed/partial responses produce an error result and nonzero
CLI exit. A process crash may leave only the request and reservation; do not
silently repeat that version.

Validation checks IDs, types, finite numeric ranges, probability sums, selected
choices and consistency of scores with their rubric and probabilities. These
checks do not prove accuracy. Compare the same cases with independent human
labels, retain missing/failed judgments in denominators, and measure disagreement
before any future promotion into authoritative grading. Listening remains required
for voice quality, interruption behavior and semantic consent.
