# Running and qualifying the benchmark

## Local fixture and evidence

`voice-bench fixture --config configs/local.toml` requires `DATABASE_URL`. It initializes the schema and returns the batch and attempt directories. No provider credentials are read. The fixture deliberately includes a forbidden-action attempt: harness validation passes when that request is rejected and retained, while its target policy metric fails when the same audit is scored as a conversation. These are different claims.

Inspect and score a saved attempt using the absolute directory printed by the fixture:

```sh
voice-bench inspect "$ATTEMPT_DIRECTORY"
voice-bench evaluate "$ATTEMPT_DIRECTORY" --version rules-v1
voice-bench review export "$ATTEMPT_DIRECTORY" --version rules-v1 > review.json
voice-bench review import "$ATTEMPT_DIRECTORY" --version human-v1 --file review.json
```

Fill in reviewer identity, explanation, validity, outcome and precise evidence references before import. Review files include the evaluated result's checksum and whether the reviewer disagreed. Each version is immutable; choose a new version to rescore. Ordinary evaluation keeps validity unresolved until there is evidence-based model assessment or human review. A detected simulator/harness error remains invalid; unconfirmed termination remains unresolved.

Raw evidence uses `artifacts/<batch>/<attempt>/`. Manifest entries name the exact file, SHA-256 checksum and size; missing files and recovery integrity issues are explicit. Audio streams are `generated.wav` (customer model output), `sent.wav` (submitted to the channel), `received.wav` (target audio received), and browser `played.wav` (rendered microphone audio, including silence). A browser render proves local submission through the audio graph, not remote hearing. Telephone delivery uses carrier checkpoints and does not fabricate a played recording.

Business state and every accepted, rejected, or repeated tool operation are committed in PostgreSQL. Authenticated, correlated HTTP bodies are retained before argument validation. No model-supplied run ID is accepted. Late requests cannot mutate a closed attempt; their database audit may arrive after the raw manifest was sealed. Recovery writes supplemental versions rather than changing that manifest.

## Supply workflows and cases

`ExecutionCase` is an execution input, not the final dataset authoring format. The `--cases` file is a JSON array with:

- `case_id`, `version`, `workflow`, `workflow_version`;
- `caller`: `goal`, customer-visible `known_facts`, and `behavior_rules`;
- `initial_state`: private synthetic business records;
- `criteria`: private grading rules; and
- `harness_fixture`: true for infrastructure controls.

Implement a versioned workflow in `business/environment.py` and register it in `WORKFLOWS`. It validates/clones supplied initial state, declares allowed tools, validates arguments, applies business rules, and returns `ok` plus either a result or a stable error code. Mutations to a rejected operation's working copy are discarded. Do not load executable code from case files. The included `harness_record` workflow is the only initial fixture; it supplies no real business coverage.

Deterministic criteria currently support `state_equals` (each entry has a list-valued `path` and expected `value`), `forbidden_tools`, `state_any_of` for acceptable alternative lists of state checks, and optional `required_tool_order` as a partial ordering. `required_metrics` explicitly selects the metrics required to pass. `rubrics` supplies conversation instructions to the judge. Alternative permitted paths are accepted unless a supplied ordering rule makes order relevant. Rubric content and thresholds belong to the dataset/evaluation workstream.

Generate the synthetic execution input only for harness testing:

```sh
mkdir -p datasets
python - <<'FIXTURE'
import json
from pathlib import Path
from voice_bench.fixture import fixture_case
Path("datasets/harness.json").write_text(json.dumps([fixture_case().model_dump(mode="json")], indent=2))
FIXTURE
voice-bench batch plan --config configs/local.toml --cases datasets/harness.json --repetitions 2 --seed 7
```

The plan expands cases × channels × repetitions and records execution order and pairing. Retries receive fresh attempt IDs and business state.

## Configure a future live qualification

Copy `configs/live.example.toml` to `configs/live.local.toml` (ignored by Git). Choose all missing values explicitly. Supply positive total minutes and spend, per-component conservative ceilings for caller/target/carrier, a combined per-attempt ceiling that covers them, and a rate-card version. Ceilings must cover the setup timeout plus the maximum conversation duration. Keep maximum concurrency at one for initial qualification.

Export credentials from your secret manager: `DATABASE_URL`, `RUMIK_API_KEY`, `OPENAI_API_KEY`, `BENCH_TOOLS_SECRET`, and phone `PLIVO_AUTH_ID`/`PLIVO_AUTH_TOKEN`. The application does not automatically load `.env` files. Long-lived credentials remain in the backend. The Chromium page receives only ephemeral LiveKit room access.

Configure the Rumik agent outside this program. Its tools must call:

- `POST /tools/rumik/before-call` with the trusted Rumik `call_id`, canonical `agent_id`, and caller `phone_number` for telephone correlation;
- `POST /tools/rumik/<tool_name>` with `call_id`, a stable `operation_id`, and an `arguments` object.

Both require `Authorization: Bearer <BENCH_TOOLS_SECRET>`. Bind `call_id` and before-call fields from Rumik's authenticated call context, never from language-model arguments. Do not define account variables or model parameters that shadow `call_id`, `agent_id`, `phone_number`, or `user_id`; preflight rejects those collisions. Keep the same operation ID for a retransmission. Reusing it with different tool arguments is rejected and audited.

Make the worker's configured public HTTPS/WSS URL reach its callback server. Terminate TLS at your existing ingress. Plivo signatures are checked against that exact public URL, not an untrusted Host header. Stream connections also require an attempt-specific secret and can attach once. Protect PostgreSQL and object storage separately; only authenticated business routes and provider callbacks need external access. Health routes expose no control actions.

Phone qualification requires a Rumik-connected number and a supported voice engine. The adapter checks the deployed agent's inbound number and the provider's phone-capability metadata. Paired execution rejects browser-only engines. One caller-number/target-agent route is reserved before dialing and held until termination is confirmed.

Only after a separately authorized qualification run:

```sh
voice-bench batch run --live --config configs/live.local.toml --cases datasets/qualification.json --repetitions 1 --seed 7
```

This command starts real paid activity. It snapshots target/version/tools/variables, caller settings, cases, source and dependency hashes. Before each dispatch it rechecks target configuration. Tool secrets are write-only in provider snapshots, so their contents cannot be independently re-read; keep account administration frozen during a batch. Configure provider-side account spending controls alongside the harness's conservative reservations.

## Grading and review

Deterministic grading is offline. Model grading is a separate paid step and requires configured judge/transcription models, a rubric version, and a positive `judge.cost_ceiling_inr` within the original batch funding:

```sh
voice-bench evaluate "$ATTEMPT_DIRECTORY" --version judged-v1 --with-model --config configs/live.local.toml
```

The judge first transcribes captured audio, then receives those transcripts, private rules, state and audit evidence. A target-provided transcript never replaces captured-audio transcription. Submitted customer audio may contain unplayed speech and is labeled accordingly. Structured verdicts must cite real checksummed artifacts; event sequences and audio ranges are validated. The judge cannot replace deterministic metrics. Text does not establish audio quality: export a review and listen to the recordings.

## Recovery, reports and storage

If a worker stops unexpectedly, keep the same database and artifact volume. Recovery waits for the expired worker lease, checks known provider calls, may hang up a carrier call, closes business state, and seals remaining evidence. Torn logs are retained byte-for-byte and marked incomplete. It never redials:

```sh
voice-bench batch recover "$BATCH_ID" --remote --config configs/live.local.toml
voice-bench batch run --live --resume "$BATCH_ID" --config configs/live.local.toml --cases datasets/qualification.json --repetitions 1 --seed 7
```

Resume requires the original settings, source, dependency hashes, cases and seed. All previous attempts must have confirmed termination and sealed evidence. It skips successful execution attempts and respects the retry limit for failed/recovered attempts. An unknown start is intentionally held for authoritative reconciliation; do not guess a call ID or remove the reservation to force progress.

```sh
voice-bench batch report "$BATCH_ID" --config configs/live.local.toml --evaluation-version judged-v1 --review-version human-v1 --output reports/batch-v1
voice-bench batch finalize "$BATCH_ID" --config configs/live.local.toml --version report-v1 --evaluation-version judged-v1 --review-version human-v1
voice-bench upload "$ATTEMPT_DIRECTORY" --config configs/live.local.toml
```

Reports retain all attempts, distinguish planned items from retries, show not-run items, and state the denominator for pass rate. A reviewed valid target drop remains a failure. Version selection is explicit; missing evaluation versions remain unresolved. Report files do not overwrite earlier exports. Batch finalization requires saved worker shutdown and settled attempts. It records `finalized_with_gaps` if planned items or outcomes remain unresolved.

S3 uploads use immutable batch/attempt/version keys, SHA-256 checksums, and conditional writes. A repeated upload compares existing bytes; conflicting content is rejected. Configure a compatible endpoint, bucket, region, and normal AWS credential-chain settings. Bucket provisioning and access policy are outside this command. Back up the PostgreSQL database and batch-level config/completion files alongside uploaded attempt bundles.

Worker completion records show that this process stopped scheduling and closed its owned server/clients. They do not claim the host VM has been deallocated. Execution completion, completed grading/review, and cloud compute shutdown are separate qualification checks.
