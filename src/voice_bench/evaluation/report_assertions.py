"""Conservative extraction of explicitly labelled reference assertions, without answer leakage."""

import re

from voice_bench.models import MetricResult

LABEL = re.compile(
    r"(?:^|(?<=[.;\n]))[ \t]*(?:[-*] )?reference(?:\s+(?:numbers?|codes?))?"
    r"(?:\s+provided)?\s*:\s*",
    re.I,
)
CODE = r"[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*"
LIST = re.compile(rf"{CODE}(?:\s*(?:,\s*(?:and\s+)?|\band\b|&)\s*{CODE})*", re.I)


def reference_assertions(text):
    """Recognize a small declared English grammar; unfamiliar prose stays unresolved.

    Extraction receives ONLY target text, never issued identifiers. Spans refer to the
    unchanged text. Hyphens and case are harmless; distinct assertions never get joined.
    """
    clauses = []
    for label in LABEL.finditer(text):
        end = re.search(r"[.;\n]", text[label.end() :])
        stop = label.end() + end.start() if end else len(text)
        raw = text[label.end() : stop].strip()
        matches = list(re.finditer(CODE, raw))
        supported = bool(LIST.fullmatch(raw)) and all(
            any(c.isdigit() for c in m.group()) for m in matches if m.group().lower() != "and"
        )
        clauses.append(
            {
                "text": text[label.start() : stop],
                "start": label.start(),
                "end": stop,
                "supported": supported,
                "assertions": [m.group() for m in matches if m.group().lower() != "and"]
                if supported
                else [],
            }
        )
    return {
        "version": "explicit-reference-clauses-v1",
        "normalization": "ASCII case and hyphens only; never join separate assertions",
        "status": "extracted" if len(clauses) == 1 and clauses[0]["supported"] else "uncertain",
        "clauses": clauses,
    }


def compare_references(text, bookings):
    extracted = reference_assertions(text)
    expected = [b.get("reference") for b in bookings]
    status = "uncertain"
    if extracted["status"] == "extracted" and all(isinstance(r, str) and r for r in expected):
        actual = extracted["clauses"][0]["assertions"]

        def normalize(value):
            return value.replace("-", "").upper()

        # Compare a multiset, retaining multiplicity rather than silently deduplicating.
        status = (
            "met"
            if sorted(map(normalize, actual)) == sorted(map(normalize, expected))
            else "not_met"
        )
    return {**extracted, "comparison": status, "issued_references": expected}


def reference_metric(report, final, refs):
    files = ("target/user-report.json", "business/final.json")
    comparison = compare_references(report.get("text", ""), final.get("bookings", []))
    status = comparison["comparison"] if all(f in refs for f in files) else "uncertain"
    return MetricResult(
        name="user_report_references",
        status=status,
        explanation=(
            "Compared only explicitly labelled target report references using "
            "explicit-reference-clauses-v1. Distinct codes remain distinct. "
            "A match checks identifiers only, not overall report accuracy; unsupported prose "
            "requires review."
        ),
        evidence=tuple(refs[f] for f in files if f in refs),
    )
