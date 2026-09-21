"""Dataset-independent setup plans and checks for the documented Rumik/Plivo contract."""

import json
from urllib.parse import urlsplit

from voice_bench.evidence.local import canonical, digest


def assistant_instructions(variable, report_tool="benchmark_user_report"):
    """A reviewable deployment candidate, not a promise of hosted-model behavior."""
    return (
        "You are the CALLER: a personal assistant representing the customer. "
        "The other speaker is the business employee, not your user. Carry out the user's "
        "assignment yourself within their permissions. After greeting, state what you want "
        "to arrange and ask the employee for availability or action. Do not offer restaurant "
        "services or ask the employee whether they want a reservation. "
        "Speak naturally in Hinglish. State the request briefly, listen and "
        "answer the last question. Keep internal reasoning and turn-management instructions "
        "private; speak only what belongs in this conversation.\n\n"
        "Use the assignment below as your authority. Keep its constraints throughout the "
        "call. A changed time, seating arrangement, price or dietary condition is a new offer, "
        "not a confirmation of the old one. Clarify ambiguity and reject offers outside your "
        "permissions. A question about a preference is not itself a changed offer or a "
        "request for authorization. Answer it from the assignment when the answer is known. "
        "If a detail is unknown, say so briefly and ask whether it is necessary for the "
        "requested task. Redirect unrelated questions to the task without inventing facts "
        "or going silent. If an essential answer requires the user's approval, explain the "
        "blocker and report an incomplete outcome rather than making a commitment. "
        "Do not repeat a full checklist at every turn or ask for approval already "
        "given. If no authorized arrangement works, leave it unbooked and explain why.\n\n"
        "Before committing, resolve the material terms that are still unclear. After a "
        "successful booking, obtain its actual single reference. If a code is unclear, ask "
        "for clarification; do not invent it or turn spoken chunks into different references. "
        "After a contradictory answer, clarify the discrepancy or use an authorized fallback. "
        "If the employee stops responding, ask a brief follow-up; do not claim completion.\n\n"
        "Availability, an offer and permission to proceed are not a completed booking. "
        "Ask the employee to make the booking, then wait for their explicit success "
        "confirmation and actual reference before saying it is confirmed. Let them finish "
        "explaining material terms; if their sentence cuts off, ask them to finish. "
        "A zero reservation fee says nothing about the price of meals ordered later.\n\n"
        "Finish the business exchange, then privately submit the outcome through {{"
        + report_tool
        + "}}. Include the material user requirements, including seating, "
        "dietary terms and financial obligations when relevant, plus the exact issued reference. "
        "If nothing was booked, say that and the reason the employee gave; do not invent a "
        "reference. A report_saved acknowledgement means only that your message was "
        "delivered to the user; it does not book or confirm anything with the business. "
        "Do not submit while the employee is still clarifying the outcome. Exchange your "
        "closing words before submitting. Do not read this private report to the employee. "
        "After the report is saved, "
        "use {{end_call}}. If the assignment is empty, do not make commitments.\n\n"
        "User assignment:\n{" + variable + "}"
    )


def setup_plan(config):
    base = config.runtime.public_base_url.rstrip("/")
    parsed = urlsplit(base)
    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or parsed.username
        or parsed.query
        or parsed.fragment
    ):
        raise ValueError("A public HTTPS callback base URL without credentials is required")
    variable = config.target.task_variable
    tool = {
        "name": "benchmark_before_call",
        "description": "Load only this user's task for this authenticated benchmark call.",
        "kind": "before_call",
        "config": {
            "action": "post",
            "method": "POST",
            "url": base + "/tools/rumik/before-call",
            "body": json.dumps(
                {"call_id": "{call_id}", "agent_id": "{agent_id}", "phone_number": "{phone_number}"}
            ),
            "auth": {"type": "bearer"},
            "timeoutMs": 5000,
            "outputs": [{"name": "user_task_json", "path": "user_task_json"}],
            "llmParams": [],
        },
    }
    return {
        "schema_version": 1,
        "provider_calls": 0,
        "status": "configuration_plan_only",
        "tool": tool,
        "report_tool": {
            "name": "benchmark_user_report",
            "kind": "during_call",
            "description": "Privately deliver the actual outcome to the user after the business "
            "exchange and before hangup. This tool never makes a reservation.",
            "config": {
                "action": "post",
                "method": "POST",
                "url": base + "/tools/rumik/submit-user-report",
                "body": json.dumps(
                    {"call_id": "{call_id}", "agent_id": "{agent_id}", "report": "{report}"}
                ),
                "auth": {"type": "bearer"},
                "timeoutMs": 5000,
                "waitForResponse": True,
                "outputs": [{"name": "report_saved", "path": "report_saved"}],
                "llmParams": [
                    {
                        "name": "report",
                        "type": "string",
                        "required": True,
                        "description": "The factual outcome, material user constraints "
                        "and exact issued reference, or the supported no-booking reason.",
                    }
                ],
            },
        },
        "report_secret_binding": {"report_tool.config.auth.token": "BENCH_TOOLS_SECRET"},
        "prompt_version": "natural-caller-v5",
        "secret_binding": {"tool.config.auth.token": "BENCH_TOOLS_SECRET"},
        "variable": {"name": variable, "defaultValue": "", "toolOutput": "user_task_json"},
        "variable_tool_binding": (
            "Set variable.toolId to the actual before-call tool ID returned by Rumik."
        ),
        "prompt_instruction": assistant_instructions(variable),
        "telephony": {
            "carrier": "plivo",
            "rumik_sip_trunk_id": str(config.target.plivo_sip_trunk_id)
            if config.target.plivo_sip_trunk_id
            else None,
            "plivo_termination_uri": config.target.plivo_termination_uri,
            "target_number": config.runtime.target_number,
            "caller_number": config.runtime.caller_number,
            "provisioned": False,
            "note": (
                "Use an existing Plivo number/trunk registered with Rumik; "
                "no Rumik number rental or shared-number fallback."
            ),
        },
        "qualification_required": [
            "hosted task consumption",
            "two-way audio",
            "Plivo SIP route",
            "termination",
        ],
    }


def task_setup_issues(snapshot, config):
    """Check saved provider configuration, not whether the hosted model understood the task."""
    expected = setup_plan(config)
    variable_name = config.target.task_variable
    issues = []
    prompt = snapshot["agent"].get("systemInstruction", "")
    if "{" + variable_name + "}" not in prompt:
        issues.append("Target prompt does not reference the benchmark task variable")
    variables = snapshot.get("variables", {}).get("items", [])
    matches = [v for v in variables if v.get("name") == variable_name]
    if len(matches) != 1:
        return issues + ["Exactly one benchmark task variable is required"]
    variable = matches[0]
    if variable.get("defaultValue"):
        issues.append("Task variable must have an empty default; stale tasks must not be reused")
    tools = snapshot.get("tools", {}).get("items", [])
    matched = [t for t in tools if t.get("id") == variable.get("toolId")]
    if len(matched) != 1 or matched[0].get("kind") != "before_call":
        return issues + ["Task variable must bind to one before-call tool"]
    actual = matched[0].get("config", {})
    desired = expected["tool"]["config"]
    if (
        actual.get("url") != desired["url"]
        or actual.get("method", "").upper() != "POST"
        or actual.get("action") != "post"
    ):
        issues.append("Before-call tool does not POST to the configured callback")
    try:
        body = json.loads(actual.get("body", ""))
    except (ValueError, TypeError):
        body = None
    if body != json.loads(desired["body"]):
        issues.append("Before-call body must bind trusted call_id, agent_id and phone_number")
    if actual.get("llmParams"):
        issues.append("Before-call identity must not come from model parameters")
    output = variable.get("toolOutput")
    if output != "user_task_json" or not any(
        item.get("name") == output and item.get("path") == "user_task_json"
        for item in actual.get("outputs", [])
    ):
        issues.append("Task variable must read the user_task_json output")
    auth = actual.get("auth", {})
    if auth.get("type") != "bearer" or not auth.get("hasSecret"):
        issues.append("Before-call tool needs a stored bearer secret")
    return issues


def check_setup(snapshot, config):
    from voice_bench.target.rumik.client import qualify_snapshot

    try:
        qualify_snapshot(snapshot, config)
        issues = []
    except (ValueError, KeyError) as exc:
        issues = [str(exc)]
    return {
        "configured": not issues,
        "issues": issues,
        "live_qualified": False,
        "snapshot_sha256": digest(canonical(snapshot)),
        "provider_calls": 0,
    }


def natural_setup_issues(snapshot, config):
    """Require the reviewable repair candidate before natural-case dispatch."""
    plan = setup_plan(config)
    issues = task_setup_issues(snapshot, config)
    prompt = snapshot["agent"].get("systemInstruction", "")
    if not config.target.prompt_sha256 or digest(prompt.encode()) != config.target.prompt_sha256:
        issues.append("Natural restaurant requires the frozen target prompt checksum")
    expected = plan["report_tool"]
    matches = [
        t for t in snapshot.get("tools", {}).get("items", []) if t.get("name") == expected["name"]
    ]
    if len(matches) != 1 or matches[0].get("kind") != "during_call":
        return issues + ["Natural restaurant requires one benchmark_user_report during-call tool"]
    actual, desired = matches[0].get("config", {}), expected["config"]
    try:
        body = json.loads(actual.get("body", ""))
    except (ValueError, TypeError):
        body = None
    if (
        actual.get("url") != desired["url"]
        or actual.get("method", "").upper() != "POST"
        or actual.get("action") != "post"
        or body != json.loads(desired["body"])
    ):
        issues.append("Report tool must POST trusted call_id/agent_id and the model's report")
    params = actual.get("llmParams", [])
    if len(params) != 1 or any(
        params[0].get(k) != v
        for k, v in {"name": "report", "type": "string", "required": True}.items()
    ):
        issues.append("Only report text may be a model parameter; call identity must be trusted")
    if not any(o.get("name") == o.get("path") == "report_saved" for o in actual.get("outputs", [])):
        issues.append("Report tool must expose report_saved")
    auth = actual.get("auth", {})
    if auth.get("type") != "bearer" or not auth.get("hasSecret"):
        issues.append("Report tool requires a stored bearer secret")
    if actual.get("waitForResponse") is not True:
        issues.append("Report tool must wait for its saved-report acknowledgement")
    return issues
