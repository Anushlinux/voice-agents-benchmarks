# Scope and decisions

This summarizes the supplied RUMIK_VOICE_BENCHMARK_SCOPE.md handoff and the
architecture discussion of 2026-09-20. It is project context, not an instruction
to provision services or execute evaluations.

## Confirmed

- Evaluate Rumik's hosted voice-agent product on difficult Hinglish conversations.
- Support browser/API audio and actual phone-number calls, reported separately.
- Use an interactive controlled customer and synthetic business tools where needed.
- Verify task outcomes, policy/action correctness, conversation behavior, audio,
  latency and call reliability using inspectable evidence.
- Preserve configuration identity and repeat runs under comparable conditions.
- Include human validation of passing and failing grades.

## Architecture accepted for this scaffold

Start test → simulated customer → browser or phone → hosted Rumik → mock business
system → evidence → evaluation and review. Develop locally; use an India cloud
worker for reported conversations. Vercel controls/review are optional.

Python is the shared runtime. Pipecat, Chromium/LiveKit and Plivo are proposed
integration choices, not working integrations. Rumik stays the target; a separate
caller is infrastructure, not another ranked agent.

## Still open

Dataset domains, scenario contents, counts and repetitions are being considered
in a separate workstream. This repository does not choose them. Caller/judge
models, target account access, numbers, route, funded budgets, review volume and
grading thresholds also need qualification or agreement.

## Outside the first benchmark

Competitor ranking, a public leaderboard, a polished management dashboard,
production customer integrations, model training, and automatic agent tuning.

## Reference reading

- [Rumik hosted agents](https://docs.rumik.ai/voice-agents)
- [Rumik business tools](https://docs.rumik.ai/variables-and-tools)
- [Plivo audio streaming](https://docs.plivo.com/docs/voice-agents/audio-streaming/overview)
- [Cekura tool-call evaluation](https://docs.cekura.ai/documentation/guides/testing-agents/tool-call-testing)
- [Tau-Voice](https://arxiv.org/html/2603.13686v1)
- [Full-Duplex-Bench](https://arxiv.org/abs/2503.04721)

Borrow verifiable outcomes and full-duplex interaction from related benchmarks.
Do not inherit transcript-fed caller perception or simulated timing where those
would bypass the actual browser/telephone audio path required here.
