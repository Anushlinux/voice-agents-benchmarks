# Working in this repository

Explain changes in clear, plain English. Start with the intended behavior, then
explain technical details and verification. Separate facts, proposals, and gaps.

## Scope

This repository benchmarks Rumik's hosted voice agents through browser and real
telephone audio. Follow README.md and docs/ARCHITECTURE.md. Dataset design is a
parallel workstream; do not invent workflows or claim coverage from scaffold data.

## Architecture rules

- Keep the caller, target, transport, business environment, evidence and grading
  separate. The target is hosted Rumik, not a custom agent using Rumik TTS.
- The caller hears received audio. Never feed it Rumik's internal transcript,
  hidden business state, or expected answers to make a test work.
- Preserve simultaneous send/receive audio; alternating turns cannot prove
  interruption handling.
- Give each attempt independent state. Correlate provider IDs before executing
  business mutations; never guess which run owns an incoming tool request.
- Verify actions and final state. A spoken success claim is not evidence of a
  successful mutation. Retain blocked forbidden attempts as evidence too.
- Keep raw evidence immutable and write rescoring to a separate result version.
- Label timing clocks and observation boundaries. Do not combine browser,
  carrier, or provider timestamps as if they shared a clock.
- Report planned, attempted, valid, invalid, unresolved, passed and failed counts.
  A valid target-side drop remains a failure; it is not automatically excluded.
- Freeze caller settings, target configuration, tools, variables and grading
  versions for a reported batch. Account-wide tools may change independently.

## Execution and credentials

- Imports, status, planning, unit tests and health routes must be provider-free.
- Live calls require an explicitly requested run, funded limits, and a real
  implementation. Never treat dependency installation or validation as permission
  to dial numbers, deploy an agent, rent a number or run paid evaluations.
- Keep credentials, call audio, transcripts, datasets and generated evidence out
  of Git. Use synthetic business data and intended benchmark phone endpoints.
- Do not call Cekura MCP tools or execute Cekura skills unless explicitly asked.
- Do not replace unavailable integrations with fake successful results.
- Do not add a dashboard, provider SDK, or extra service until the next feature
  actually needs it. Vercel is optional; the live worker is a separate concern.

## Development

Python 3.12 with uv; update uv.lock when changing dependencies. Keep interfaces
provider-independent and functions small. Run ruff check, ruff format --check,
and relevant pytest checks before reporting code changes complete. Distinguish
unit validation, container validation and live provider proof in your report.
