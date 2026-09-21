from voice_bench.caller.instructions import counterpart_instructions
from voice_bench.models import CounterpartBrief
from voice_bench.target.rumik.setup import assistant_instructions


def test_restaurant_playbook_uses_only_granted_tools_and_counterpart_brief():
    brief = CounterpartBrief(role="Restaurant employee", goal="Handle requests", known_facts={})
    tools = [
        {"name": "business_" + name}
        for name in ("check_availability", "offer_reservation", "record_reservation")
    ]
    prompt = counterpart_instructions("Keep facts fixed.", brief, tools)
    assert "# Restaurant booking playbook" in prompt
    assert "then WAIT for their reply" in prompt
    assert "# Assigned brief" in prompt
    assert "benchmark_user_task" not in prompt
    assert "benchmark_user_report" not in prompt
    generic = counterpart_instructions("Keep facts fixed.", brief, tools[:1])
    assert "business_record_reservation" not in generic
    assert "# Restaurant booking playbook" not in generic


def test_target_prompt_keeps_binding_and_report_after_acknowledgement():
    prompt = assistant_instructions("private_task", "private_report")
    assert "{private_task}" in prompt
    assert "{{private_report}}" in prompt
    assert "{{end_call}}" in prompt
    assert prompt.index("Acknowledge the result aloud") < prompt.index("Privately call")
    assert "business_record_reservation" not in prompt
    assert len(prompt) < 8000
