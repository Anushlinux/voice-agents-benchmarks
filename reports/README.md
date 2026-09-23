# Benchmark reports

These are the current published results. Choose a channel, then a model and case to read the conversation or listen to its recording.

| Channel | Report | Audio, transcripts and case evidence | Models |
| --- | --- | --- | --- |
| Web calls | [Results and metrics](webcall/README.md) | [All conversations](webcall/conversations/README.md) | Muga, Mulberry 1.5, Mulberry 1.6 |
| Telephony | [Results and metrics](telephony/README.md) | [All attempts](telephony/conversations/README.md) | Muga, Mulberry 1.5, Mulberry 1.6 |

Latest published cohorts: **21–22 September 2026**. There are 30 attempted cases per channel. Web calls have 30 recordings; telephony has 20 recordings and ten Mulberry 1.6 rejection records.

[Older published reports](archive/README.md) are retained for history. Their results are not additional cases in the latest comparison.

## For maintainers

Keep one current report per channel in `webcall/` and `telephony/`. Keep each case's audio, transcripts, private report and measurements together under `conversations/<model>/<case>/`. When a new batch supersedes a report, archive the previous publication and update this index and the repository README. A rejected or unresolved attempt must remain visible.

Other dated folders visible in a local checkout are ignored run workspaces: deployment receipts, diagnostics, earlier report versions and generation inputs. They are not the reader-facing reports. Their original paths are retained because saved evidence and local scripts refer to them. Raw `artifacts/` bundles and historical manifests must not be renamed or rewritten to tidy the presentation.

The historical web-call export script is at [scripts/build_webcall_report.py](../scripts/build_webcall_report.py). It needs local evidence and a local helper from the original run workspace. It writes a separate ignored draft; it does not overwrite the published reports.

[Repository home](../README.md)
