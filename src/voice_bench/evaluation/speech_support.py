"""Check attribution and quotation, without pretending to verify semantic judgment."""

import unicodedata
from typing import Literal

from voice_bench.models import Contract

ACTOR_KNOWLEDGE_GUIDANCE = (
    "The counterpart never receives the private user_task or outcome_criteria. "
    "Assess it against its own brief, received target speech and permitted tool results. "
    "If Rumik misstates the user's requirements, an employee responding truthfully to "
    "that spoken request is not invalid merely because the request differs from the "
    "private assignment. Attribute the misstatement to Rumik. Do not require the "
    "employee to know or correct undisclosed private instructions. Read the actual "
    "audited tool name and result: an availability lookup or proposed offer is not a "
    "committed reservation. "
)


class SpeechClaim(Contract):
    source_id: str
    speaker: Literal["target", "counterpart"]
    quote: str


def normalized(text):
    text = unicodedata.normalize("NFKC", text).casefold()
    # ASR punctuation is not spoken. Hindi danda vs period, or an excerpt ending
    # in a question mark instead of a comma, must not discard the same words.
    return " ".join(
        "".join(" " if unicodedata.category(c).startswith("P") else c for c in text).split()
    )


def support_issue(metric, claims, windows):
    if metric.status not in {"met", "not_met"} or metric.name == "user_report_accuracy":
        return None
    if not claims:
        return "No quoted speech supports this resolved conversational judgment."
    sources = {w["source_id"]: w for w in windows}
    expected_actor = (
        "counterpart" if metric.name in {"counterpart_validity", "caller_validity"} else "target"
    )
    for claim in claims:
        source = sources.get(claim.source_id)
        if source is None or claim.source_id not in metric.evidence:
            return "A speech claim does not identify a cited recording window."
        if claim.speaker != source["speaker"]:
            return "A speech claim attributes the quoted window to the wrong speaker."
        if not normalized(claim.quote) or normalized(claim.quote) not in normalized(source["text"]):
            return "A claimed quotation does not occur in its cited transcription window."
    if not any(claim.speaker == expected_actor for claim in claims):
        return f"The judgment lacks a quoted observation from the assessed {expected_actor}."
    return None
