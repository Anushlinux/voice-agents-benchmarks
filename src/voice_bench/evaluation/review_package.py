"""Provider-free listening package from an explicitly selected saved evaluation."""

import json

from voice_bench.evaluation.report_assertions import compare_references
from voice_bench.evaluation.scoring import load_bundle, review_template
from voice_bench.evaluation.timeline import build_timeline
from voice_bench.evidence.local import canonical, digest, publish, safe_path


def prepare_review_package(directory, version, destination):
    manifest, refs = load_bundle(directory)
    path = safe_path(directory, f"evaluation/{version}/result.json")
    evaluation = json.loads(path.read_text())
    transcripts = (evaluation.get("judge") or {}).get("transcripts", [])
    timeline, sources = build_timeline(directory, transcripts, refs)
    report = (
        json.loads((directory / "target/user-report.json").read_text())
        if "target/user-report.json" in refs
        else {}
    )
    final = (
        json.loads((directory / "business/final.json").read_text())
        if "business/final.json" in refs
        else {}
    )
    package = {
        "version": "listening-package-v1",
        "mode": "review_preparation_not_a_grade",
        "evaluation_version": version,
        "evaluation_sha256": digest(path.read_bytes()),
        "evidence_directory": str(directory.resolve()),
        "portable": False,
        "missing_evidence": manifest["missing"],
        "timeline": timeline,
        "sources": {name: ref.model_dump(mode="json") for name, ref in sources.items()},
        "report_reference_comparison": compare_references(
            report.get("text", ""), final.get("bookings", [])
        ),
        "review_template": review_template(directory, version),
        "listening_instructions": [
            "Listen to original played and received audio before consulting model verdicts.",
            "Record exact audio ranges for disputed reference delivery and consent.",
            "Record transcript corrections as new annotations; never overwrite raw transcripts.",
            "Check semantic agreement separately from compliance with the original readback rules.",
            "Keep insufficient evidence uncertain. This package is not a completed human review.",
        ],
    }
    # The listening worksheet starts blind to the model verdict.
    package["review_template"].update(validity="unresolved", outcome="unresolved")
    publish(destination, canonical(package))
    return {"review_package": str(destination.resolve()), "human_review_imported": False}
