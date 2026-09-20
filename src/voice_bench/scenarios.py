"""Provider-free behavior profiles and bounded counterpart conversation policy."""

from typing import Literal

from pydantic import Field

from voice_bench.models import Contract


class CounterpartProfile(Contract):
    profile_id: Literal["straightforward", "concise", "clarification_seeking"]
    version: Literal["1"] = "1"


class ScenarioPolicy(Contract):
    version: Literal["1"] = "1"
    event_conflicts: Literal["reject", "priority_order"] = "reject"
    max_pending_events: int = Field(default=4, ge=1, le=20)


PROFILE_RULES = {
    "straightforward": "Answer directly and cooperatively in ordinary complete sentences.",
    "concise": "Give brief answers, but disclose required availability, prices, restrictions "
    "and confirmation terms completely. Brevity must not hide material business facts.",
    "clarification_seeking": "Ask a focused clarification when received speech leaves a "
    "material detail ambiguous. Do not repeatedly ask about facts already made clear.",
}

BOUNDED_RULES = (
    "Your assigned facts, business rules, tool permissions and explicit scenario actions "
    "take precedence over conversational style. Never change them to help the caller pass.",
    "For an ordinary question without a dedicated scenario action, answer using only "
    "your brief, received audio and permitted tool results. If information is unavailable, "
    "say so or ask for clarification; do not invent an answer or a new task.",
    "Preserve corrections and refusals across repeated questions. Rephrase consistent facts "
    "when asked to repeat. A correction or an unrelated answer is not consent.",
    "After a challenge, resume the unresolved business request using accurate current terms. "
    "Changed terms require fresh confirmation. Do not repeat a one-time challenge yourself.",
    "Close only after an evidenced outcome, an appropriate refusal, or an explicit request "
    "to end. Finish closing speech before ending the call; do not fabricate completion.",
)


def effective_counterpart(brief, profile=None, policy=None):
    """Accept only counterpart inputs, so private task/grading data cannot be copied here."""
    rules = list(brief.behavior_rules)
    if profile is not None or policy is not None:
        rules.extend(BOUNDED_RULES)
    if profile is not None:
        rules.append(PROFILE_RULES[profile.profile_id])
    return brief.model_copy(update={"behavior_rules": tuple(rules)})
