# ruff: noqa: E501
"""Assemble one GitHub-ready master report with per-case transcripts, audio and evaluations.

Historical exporter; requires the original local run workspace and its helper module.
Writes reports/generated-webcall-draft, never the current published reports.

Reads immutable artifacts only. Copies each attempt's independent transcript, Rumik's own
hosted transcript, the evaluation summary, private report, measurements and a compressed
mp3 of the synchronized conversation into conversations/<model>/<case>/.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports" / "generated-webcall-draft"
sys.path.insert(0, str(ROOT / "reports/p0-cohort-mulberry-20260922"))
from build_report import LLM_QUESTIONS, attempt_row, cohort_summary  # noqa: E402

FFMPEG = "/opt/homebrew/bin/ffmpeg"
MODELS = {
    "muga": {
        "label": "Muga",
        "batches": ["9e75406e-6e55-4eda-aaf2-9864a630ae05"],
        "note": "Pre-repair harness: target prompt A (3,041 characters), workflow 5, phonetically spelled hex reference, no silence follow-up. Run on 21 September 2026 as the historical baseline.",
    },
    "mulberry-1-5": {
        "label": "Mulberry 1.5",
        "batches": ["f65d8b78-d09a-4eb7-af40-f98efd8803ce"],
        "note": "Repaired harness: prompt natural-caller-v8, workflow 6 with the compact numeric reference, one ten-second silence follow-up. Run on 22 September 2026.",
    },
    "mulberry-1-6": {
        "label": "Mulberry 1.6",
        "batches": ["ed8bb1e2-4d90-49c2-b581-491987cb498f", "8c9f849c-c24c-416c-8b41-8d8a4cddd92e"],
        "note": "Same repaired harness and settings as Mulberry 1.5; the second batch holds the two cases a conservative drift stop skipped. Run on 22 September 2026.",
    },
}
SLUG = {
    "restaurant_natural_v2_01": "01-aditi-shah",
    "restaurant_natural_v2_02": "02-kabir-sethi",
    "restaurant_natural_v2_03": "03-meera-iyer",
    "restaurant_natural_v2_04": "04-nisha-mehta",
    "restaurant_natural_v2_05": "05-farhan-ali",
    "restaurant_natural_v2_06": "06-priya-nair",
    "restaurant_natural_v2_07": "07-devika-rao",
    "restaurant_natural_v2_08": "08-arjun-menon",
    "restaurant_natural_v2_09": "09-sana-khan",
    "restaurant_natural_v2_10": "10-rohan-desai",
}


def read(path, default=None):
    return json.loads(path.read_text()) if path.exists() else ({} if default is None else default)


def fmt(value, digits=0):
    if value is None:
        return "—"
    return f"{value:,.{digits}f}" if isinstance(value, float) else f"{value:,}"


def dist(d):
    if not d or not d.get("n"):
        return "— (n=0)"
    return " / ".join(fmt(d[k]) for k in ("mean", "p50", "p90", "p95")) + f" (n={d['n']})"


def export_case(model, row, batch):
    run = batch / row["run_id"]
    report_dir = batch / "full-report-v2" / row["run_id"]
    if not report_dir.exists():
        report_dir = batch / "full-report" / row["run_id"]
    dest = OUT / "conversations" / model / SLUG[row["case_id"]]
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "transcript.md").write_text((report_dir / "transcript.md").read_text())
    provider = read(run / "provider/rumik-call.json")
    lines = [
        f"# Rumik's own call transcript — {row['name']} ({MODELS[model]['label']})",
        "",
        "This is the transcript Rumik's service saved for the call: `assistant` is Rumik, `user` is what Rumik's speech recognition heard from the restaurant employee. Recognition errors are preserved. Compare with `transcript.md`, the independent transcription of the actual audio.",
        "",
        f"Provider status: `{provider.get('status')}`, end reason `{provider.get('endReason')}`, duration {provider.get('durationSeconds')} s.",
        "",
    ]
    for turn in provider.get("transcript") or []:
        who = "Rumik" if turn.get("role") == "assistant" else "Employee (as heard by Rumik)"
        lines.append(f"- **{who}:** {turn.get('content', '')}")
    (dest / "hosted-transcript.md").write_text("\n".join(lines) + "\n")
    evaluation = (report_dir / "README.md").read_text()
    evaluation = re.sub(
        r"\]\(/Users/[^)]*?/(conversation\.wav)\)", "](conversation.mp3)", evaluation
    )
    evaluation = re.sub(
        r"\]\(/Users/[^)]*?/(details\.json|measurements-v2\.json|turn-timestamps\.csv|transcript\.md|diagnostics-v1\.json|audio-provenance\.json)\)",
        r"](\1)",
        evaluation,
    )
    evaluation = evaluation.replace(
        "![Full conversation](conversation.mp3)", "[Full conversation recording](conversation.mp3)"
    )
    evaluation = re.sub(r"/Users/[^\s)]*artifacts/", "artifacts/", evaluation)
    (dest / "evaluation.md").write_text(evaluation)
    for name in ("measurements-v2.json", "turn-timestamps.csv", "diagnostics-v1.json"):
        src = report_dir / name
        if src.exists():
            (dest / name).write_bytes(src.read_bytes())
    report = read(run / "target/user-report.json")
    (dest / "private-report.txt").write_text(
        (report.get("text") or "(no private report was received)") + "\n"
    )
    mp3 = dest / "conversation.mp3"
    if not mp3.exists():
        subprocess.run(
            [
                FFMPEG,
                "-loglevel",
                "error",
                "-y",
                "-i",
                str(report_dir / "conversation.wav"),
                "-ac",
                "2",
                "-ar",
                "24000",
                "-b:a",
                "64k",
                str(mp3),
            ],
            check=True,
        )
    luna_bad = [q for q in LLM_QUESTIONS if row["luna"].get(q) in ("not_met", "uncertain")]
    jev_bad = [q for q in LLM_QUESTIONS if row["jev"].get(q) in ("not_met", "uncertain")]
    ttfs, ttft = row["ttfs_ms"] or {}, (row["ttft_item_ms"] or row["ttft_ms"] or {})
    wer = row["wer"]
    case_readme = [
        f"# {row['case_id'][-2:]} {row['name']} — {MODELS[model]['label']}",
        "",
        f"Expected outcome: **{row['expected'].replace('_', ' ')}**. Recorded business outcome: **{row['actual_business_outcome'].replace('_', ' ')}** ({'matches' if row['business_outcome_matches'] else 'does not match'}).",
        f"Simulation validity: **{row['validity']}**. Formal outcome: **{row['outcome']}**. Deterministic checks: {'all met' if row['deterministic_solved'] else 'not all met'}. Private report: {'received' if row['report_received'] else 'missing'}. Ending: {row['conversation_end'] or row['execution_error']}.",
        "",
        "| Metric | Value |",
        "| --- | --- |",
        f"| Call duration | {fmt(row['duration_seconds'])} s |",
        f"| TTFS ms mean / p50 / p90 / p95 | {dist(ttfs)} |",
        f"| TTFT per employee turn ms | {dist(ttft)} |",
        f"| Provider LLM first byte ms | {dist(row['provider_llm_ttfb_ms'])} |",
        f"| WER (ASR-to-ASR) | {fmt(wer['wer'] * 100, 1) + '%' if wer else '—'} |",
        f"| Highest completion tokens in a turn | {fmt(row['max_completion'])}{' (' + str(row['turns_at_400']) + ' turn(s) at the 400 ceiling)' if row['turns_at_400'] else ''} |",
        f"| Luna not met / uncertain | {', '.join(luna_bad) or 'none'} |",
        f"| Jev not met / uncertain | {', '.join(jev_bad) or 'none'} |",
        f"| Luna = Jev | {row['luna_jev_agreement']} |",
        "",
        "## Files",
        "",
        "- [conversation.mp3](conversation.mp3) — synchronized recording; left channel restaurant employee, right channel Rumik.",
        "- [transcript.md](transcript.md) — independent transcription of the recording (gpt-4o-mini-transcribe).",
        "- [hosted-transcript.md](hosted-transcript.md) — Rumik's own saved transcript, including what its speech recognition heard.",
        "- [evaluation.md](evaluation.md) — every metric with the judge's explanation, timing table and pipeline status.",
        "- [private-report.txt](private-report.txt) — the exact report Rumik sent to its user through the authenticated tool.",
        "- [measurements-v2.json](measurements-v2.json), [turn-timestamps.csv](turn-timestamps.csv), [diagnostics-v1.json](diagnostics-v1.json) — raw measurements.",
        "",
        "## Private report",
        "",
        "> " + (report.get("text") or "(no private report was received)"),
        "",
        f"Raw evidence: `artifacts/{batch.name}/{row['run_id']}/`.",
        "",
    ]
    (dest / "README.md").write_text("\n".join(case_readme))
    return f"conversations/{model}/{SLUG[row['case_id']]}"


def build():
    models = {}
    for model, spec in MODELS.items():
        rows = []
        for batch_id in spec["batches"]:
            batch = ROOT / "artifacts" / batch_id
            report = read(batch / "full-report/report.json")
            for attempt in report.get("attempts", []):
                row = attempt_row(batch, attempt)
                row["folder"] = export_case(model, row, batch)
                rows.append(row)
        rows.sort(key=lambda r: r["case_id"])
        models[model] = {"rows": rows, "summary": cohort_summary(rows)}
    return models


def markdown(models):
    s = {m: models[m]["summary"] for m in MODELS}
    L = ["# Rumik voice-agent benchmark — Muga, Mulberry 1.5 and Mulberry 1.6", ""]
    L += [
        "Hosted [Rumik](https://rumik.ai) acts as a customer's personal assistant and phones a restaurant to book a table. The restaurant employee is simulated by OpenAI `gpt-realtime`, which hears Rumik's actual audio and can only use the restaurant's own availability, offer and booking tools. Every call is a real full-duplex browser call to the hosted Rumik agent; nothing is scripted and no call is retried.",
        "",
        "Ten authored Hinglish restaurant cases are used. Seven expect a booking under the customer's constraints; three expect Rumik to decline correctly because no permitted option exists. Each model ran every case once.",
        "",
        "**Read the proof, not just the table.** Every case links to the recording, the independent transcript, Rumik's own transcript, the exact private report Rumik sent its user, and the full evaluation with the judge's reasoning.",
        "",
        "## Headline",
        "",
        "| Measure | Muga | Mulberry 1.5 | Mulberry 1.6 |",
        "| --- | --- | --- | --- |",
    ]

    def row(label, f):
        L.append(f"| {label} | " + " | ".join(f(s[m]) for m in MODELS) + " |")

    row("Attempted / connected", lambda x: f"{x['attempted']} / {x['connected']}")
    row("Conversations completed with a private report", lambda x: str(x["reports_received"]))
    row("Business outcome matches the case", lambda x: str(x["business_outcome_matches"]))
    row("All deterministic checks met", lambda x: str(x["deterministic_solved"]))
    row(
        "Simulation valid / invalid / unresolved",
        lambda x: f"{x['valid']} / {x['invalid']} / {x['validity_unresolved']}",
    )
    row(
        "Formal outcome passed / failed / unresolved",
        lambda x: f"{x['passed']} / {x['failed']} / {x['outcome_unresolved']}",
    )
    row(
        "Ended by Rumik hangup / employee finish / inactivity timeout",
        lambda x: (
            f"{x['ended_by_rumik_hangup']} / {x['ended_by_employee_finish']} / {x['idle_timeouts']}"
        ),
    )
    row(
        "Rumik generations at the 400-token ceiling",
        lambda x: (
            str(x["turns_at_400"]) if x["ttft_ms"]["n"] or x["turns_at_400"] else "not captured"
        ),
    )
    row("TTFS ms mean / p50 / p90 / p95", lambda x: dist(x["ttfs_ms"]))
    row(
        "TTFT per employee turn ms mean / p50 / p90 / p95",
        lambda x: dist(x["ttft_item_ms"]) if x["ttft_item_ms"]["n"] else "not captured (see notes)",
    )
    row(
        "TTFT per Rumik generation ms",
        lambda x: dist(x["ttft_ms"]) if x["ttft_ms"]["n"] else "not captured (see notes)",
    )
    row(
        "Provider LLM first byte ms",
        lambda x: (
            dist(x["provider_llm_ttfb_ms"])
            if x["provider_llm_ttfb_ms"]["n"]
            else "not captured (see notes)"
        ),
    )
    row(
        "WER pooled, ASR-to-ASR",
        lambda x: (
            f"{x['wer_pooled'] * 100:.1f}% over {x['wer_words']} words"
            if x["wer_pooled"] is not None
            else "—"
        ),
    )
    row("Call duration s mean / p50 / p90 / p95", lambda x: dist(x["duration_seconds"]))
    L += [
        "",
        "**Important comparability note.** Muga ran on 21 September on the pre-repair harness (long prompt A, spelled hex references, no silence follow-up), which is where most of its inactivity timeouts come from. Mulberry 1.5 and 1.6 ran on 22 September on the repaired harness with prompt v8 and the compact numeric reference. The two Mulberry cohorts are directly comparable with each other; Muga is the historical baseline and its lower completion rate is mostly the harness, not the voice. Muga's calls also predate the capture of Rumik's lifecycle packets, so TTFT is not available for it.",
        "",
        "## How the benchmark works",
        "",
        "1. **Case.** A private user task (request, constraints, permissions) is delivered to Rumik through an authenticated before-call tool. The employee gets only its own brief and restaurant policies. Neither side sees the grading rules.",
        "2. **Call.** The harness joins Rumik's browser call, records both directions and plays the employee's speech into the room. Audio is simultaneous, so interruptions are real.",
        "3. **Business tools.** The employee must look up availability, prepare an offer, and only then record a reservation; the recorder demands that the offer was actually played and that the caller spoke afterwards. Every request is audited and rejected requests are kept.",
        "4. **Private report.** Rumik must send the outcome to its user through an authenticated tool before hanging up. The report is the user-facing deliverable.",
        "5. **Evaluation.** Deterministic checks on the sealed business state and event log, then two independent LLM judges, then this report. Grades are frozen per batch and never edited.",
        "",
        "## What the metrics mean",
        "",
        "- **Business outcome** — did the restaurant record what the case expected (a booking with the right terms, or deliberately no booking)? Read from sealed business state, never from speech.",
        "- **Deterministic checks** — task state, booking identity, immutable reservation history, no forbidden actions, no duplicates, authenticated task delivery, authenticated report receipt.",
        "- **Luna** — `gpt-5.6-luna` reads the independent transcript, business record and report against the frozen rubric and answers eight questions: counterpart validity, constraint behaviour, consent alignment, report accuracy, role fidelity, question relevance, context retention, conversation progress. Its explanations are in each case's `evaluation.md`.",
        "- **Jev** — `typesafe/jev-1.13` answers the same eight questions independently with a probability per choice. It is a second opinion and does not change grades. Luna = Jev counts agreements out of comparable questions.",
        "- **Formal outcome** — passed only when every required deterministic and Luna requirement is met on a valid simulation; failed when any requirement is not met; unresolved when the simulation is invalid (an employee fault) or a requirement stays uncertain.",
        "- **TTFS** (time to first speech) — end of the employee's rendered speech to the first Rumik speech captured, on the browser audio clock, per employee turn.",
        "- **TTFT** (time to first token) — from the lifecycle packets Rumik publishes into the call. *Per employee turn*: end of employee speech to Rumik's first text token, same clock as TTFS. *Per Rumik generation*: Rumik's own end-of-speech decision to its first token. *Provider LLM first byte*: Rumik's self-reported LLM latency. All include network transit and are upper bounds.",
        "- **WER** — word error rate between an independent transcription of the employee's played audio and Rumik's own recognition transcript. Two machine transcripts, so provisional; it is not a human-scored recognition accuracy.",
        "- Distributions are mean / p50 / p90 / p95 in milliseconds over individual observations, nearest-rank quantiles.",
        "",
    ]
    for model, spec in MODELS.items():
        rows = models[model]["rows"]
        L += [
            f"## {spec['label']}",
            "",
            spec["note"],
            "",
            f"Batches: {', '.join('`' + b + '`' for b in spec['batches'])}.",
            "",
        ]
        L += [
            "| Case | Expected | Business outcome | Simulation | Formal | Deterministic | Luna not met / uncertain | Jev not met / uncertain | Luna = Jev | Report | Ending | Dur s | TTFS p50 (n) | TTFT p50 (n) | Max tokens | WER | Proof |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
        for r in rows:
            luna_bad = [
                q.replace("_", " ")
                for q in LLM_QUESTIONS
                if r["luna"].get(q) in ("not_met", "uncertain")
            ]
            jev_bad = [
                q.replace("_", " ")
                for q in LLM_QUESTIONS
                if r["jev"].get(q) in ("not_met", "uncertain")
            ]
            ttfs, ttft = r["ttfs_ms"] or {}, (r["ttft_item_ms"] or r["ttft_ms"] or {})
            wer = r["wer"]
            f = r["folder"]
            end = {
                "target_hangup": "Rumik hung up",
                "counterpart_finish": "employee finished",
                "ConversationTimeout": "inactivity timeout",
            }.get(
                r["conversation_end"] or r["execution_error"] or "",
                r["conversation_end"] or r["execution_error"] or "—",
            )
            proof = f"[audio]({f}/conversation.mp3) · [transcript]({f}/transcript.md) · [Rumik transcript]({f}/hosted-transcript.md) · [evaluation]({f}/evaluation.md) · [report]({f}/private-report.txt)"
            L.append(
                f"| [{r['case_id'][-2:]} {r['name']}]({f}/README.md) | {r['expected'].replace('_', ' ')} | {'✓' if r['business_outcome_matches'] else '✗'} {r['actual_business_outcome'].replace('_', ' ')} | {r['validity']} | {r['outcome']} | {'all met' if r['deterministic_solved'] else 'not met'} | {', '.join(luna_bad) or 'none'} | {', '.join(jev_bad) or 'none'} | {r['luna_jev_agreement']} | {'yes' if r['report_received'] else 'no'} | {end} | {fmt(r['duration_seconds'])} | {fmt(ttfs.get('p50'))} ({ttfs.get('n', 0)}) | {fmt(ttft.get('p50'))} ({ttft.get('n', 0)}) | {fmt(r['max_completion'])}{' ⚠' + str(r['turns_at_400']) if r['turns_at_400'] else ''} | {fmt(wer['wer'] * 100, 1) + '%' if wer else '—'} | {proof} |"
            )
        L += ["", "Private reports Rumik sent its user:", ""]
        for r in rows:
            L.append(
                f"- **{r['case_id'][-2:]} {r['name']}:** {(r['report_text'] or '(no report received)').replace(chr(10), ' ')}"
            )
        L.append("")
    L += [
        "## Judge verdicts per question",
        "",
        "Count of cases per verdict. `n/a` means the question did not apply (for example consent on a no-booking case); `no answer` means Jev's response was rejected by the frozen validator.",
        "",
        "| Question | Luna Muga | Jev Muga | Luna 1.5 | Jev 1.5 | Luna 1.6 | Jev 1.6 |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]

    def cell(c):
        names = {
            "met": "met",
            "not_met": "not met",
            "uncertain": "uncertain",
            "not_applicable": "n/a",
            None: "no answer",
            "None": "no answer",
        }
        return ", ".join(
            f"{names.get(k, k)} {v}" for k, v in sorted(c.items(), key=lambda kv: str(kv[0]))
        )

    for q in LLM_QUESTIONS:
        L.append(
            f"| {q.replace('_', ' ')} | "
            + " | ".join(
                f"{cell(s[m]['luna_verdicts'][q])} | {cell(s[m]['jev_verdicts'][q])}"
                for m in MODELS
            )
            + " |"
        )
    L += [
        "",
        "## Findings",
        "",
        "1. **The repaired harness moved the failure from silence to content.** Muga on the old harness completed 3 of 10 conversations with a report and timed out 7 times. Mulberry 1.5 and 1.6 on the repaired harness completed 19 of 20. The remaining stall (Mulberry 1.5, Devika Rao) carries the known signature: Rumik's hosted LLM spends its whole 400-token completion budget on hidden reasoning and produces nothing. That limit is hosted configuration and still bit fifteen turns across the twenty Mulberry calls; fourteen recovered.",
        "2. **Employee slips now cause most invalid simulations**: a mispronounced reference, an invented request during a silence follow-up, a confirmation announced before the tool result, an unrelated phrase, a missed budget-fitting menu, a booking recorded without clear consent. These are `gpt-realtime` faults and make the simulation invalid rather than grading Rumik.",
        "3. **Rumik's own errors are about content**: an ignored branch-preference rule, an initial wrong time window, a role slip into the employee's position, a wrong readback of the customer's name, an invented time mismatch, and 'without onion and garlic' turned into 'free food'.",
        "4. **Report accuracy is the most frequent failed requirement** in the Mulberry cohorts (9 of 19 reports): omitted booked terms, dropped reference digits, a reference written in Devanagari, a surname-only booking name recorded by the employee.",
        "5. **Latency.** Rumik's self-reported LLM first byte is about 0.32 s. The caller waits about 1.4 to 1.6 s (p50) for the first token and 2.2 to 2.4 s (p50) for the first speech, so endpointing plus reasoning and then speech synthesis account for most of the perceived delay. Muga's TTFS is in the same range on the calls that did reply.",
        "6. **WER** is 21 to 23 percent for both Mulberry cohorts and higher for Muga on this ASR-to-ASR comparison. Hinglish script differences inflate all three numbers; treat them as relative, not absolute recognition accuracy.",
        "7. **Judges.** Luna and Jev agree on roughly six of eight questions per case; Jev leans toward 'met' with low confidence. Two Luna verdicts were downgraded to uncertain because the judge's quoted evidence did not match the transcript window; one Jev answer was rejected by the validator.",
        "",
        "## Limits",
        "",
        "One attempt per case per model; differences of one or two cases are not statistically meaningful. Muga is not on the same harness as the Mulberry cohorts. TTFT and TTFS are observed at the browser and include network transit. WER compares two machine transcripts. Human listening for Hinglish quality and output integrity is pending for every case. Formal grades come from the frozen rubric and can fail a call that completed the business task, for example on report completeness.",
        "",
        "## Provenance",
        "",
        "Recordings here are 64 kbps mp3 transcodes of the synchronized `conversation.wav` in each attempt's frozen report; raw evidence, frozen configuration, source snapshot and database ledgers are under `artifacts/<batch>/`. Per-attempt evaluations for the Mulberry cohorts are the regenerated `full-report-v2` (adds TTFT; grades unchanged). Investigation write-ups: `docs/CONVERSATION_REPAIR.md`, `docs/P0_DEBUG_PLAN.md`, `reports/p0-cohort-mulberry-20260922/`.",
        "",
    ]
    return "\n".join(L)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    models = build()
    (OUT / "README.md").write_text(markdown(models))
    summary = {
        m: {
            "summary": models[m]["summary"],
            "cases": [
                {k: v for k, v in r.items() if not k.startswith("_")} for r in models[m]["rows"]
            ],
        }
        for m in MODELS
    }
    (OUT / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    print("master report written:", OUT / "README.md")
