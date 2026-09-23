# Rumik voice-agent benchmarks

Start with the latest reports below. Both cover **Muga, Mulberry 1.5 and Mulberry 1.6**, with ten restaurant cases per model.

| Benchmark | Latest report | Conversations and audio |
| --- | --- | --- |
| **Web calls** — browser audio | [Read the web-call report](reports/webcall/README.md) | [Browse all 30 conversations](reports/webcall/conversations/README.md) |
| **Telephony** — phone calls through Plivo | [Read the telephony report](reports/telephony/README.md) | [Browse all 30 attempts](reports/telephony/conversations/README.md) |

Reports cover **21–22 September 2026**. Each case has its recording when a call connected, transcripts, the private report sent by Rumik, and evaluation evidence. Open an audio link to play or download the MP3; GitHub may require **View raw** or **Download**.

**Telephony coverage:** Muga and Mulberry 1.5 each connected all ten calls. Mulberry 1.6 connected none: all ten were rejected with `USER_BUSY`. Its rejection evidence is included; there are no recordings for those attempts.

**Web-call comparison:** Muga is the latest available ten-case baseline for that model, recorded on an earlier harness. The web-call report explains why it is not directly comparable with the two Mulberry cohorts. Failed and unresolved results remain included.

Rumik is the assistant being tested. It acts for a customer and talks to an OpenAI-simulated restaurant employee. These are single, harness-connected conversations; they do not test Rumik choosing and dialing a restaurant or completing a task across several calls.

## Repository guide

| Folder | Purpose |
| --- | --- |
| [reports](reports/README.md) | Current web-call and telephony reports, with all model results and proof |
| [reports/archive](reports/archive/README.md) | Older published results, clearly separated from the current reports |
| [docs](docs/README.md) | Setup, architecture and development instructions |
| [datasets](datasets/README.md) | Case definitions, source attribution and dataset notes |
| `src/`, `browser/`, `tests/` | Benchmark implementation and checks |
| `artifacts/` | Local raw evidence, excluded from Git |

To work on the harness, start with the [running guide](docs/RUNNING.md) and [architecture](docs/ARCHITECTURE.md). Reading these reports makes no provider calls.
