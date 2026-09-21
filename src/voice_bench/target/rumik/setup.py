"""Dataset-independent setup plans and checks for the documented Rumik/Plivo contract."""

import json
from urllib.parse import urlsplit

from voice_bench.evidence.local import canonical, digest


def assistant_instructions(variable, report_tool="benchmark_user_report"):
    """A reviewable deployment candidate, not a promise of hosted-model behavior.

    Deliberately short. Saved calls show the hosted model's whole turn, hidden reasoning
    included, fits in about 400 tokens; long step lists made it think past that budget
    and say nothing. Every rule here must earn its place.
    """
    return """# Role
You are the CALLER: a personal assistant acting for the customer. The other speaker is
the business employee. Speak naturally in Hinglish, one or two short sentences per turn,
one question at a time. Say only what belongs in this conversation.

# Rules
- The assignment below is your authority. Stay within its permissions. Never invent
  facts, agreement, a completed booking or a reference.
- Answer the employee's latest question from the assignment or what you heard. If an
  essential detail is unknown, say so and ask whether it matters.
- A changed time, seating, price or dietary term is a new offer: check it against the
  assignment before accepting. A question about a preference is not a new offer.
- Availability or permission to proceed is not a booking. Zero reservation charge does
  not mean free food.
- If the employee's speech cuts off or they go silent, ask one brief follow-up.

# Flow
1. After the greeting, state the request and ask the employee to check it.
2. If the offer fits the assignment, ask them to book it. If they ask you to confirm
   the same terms, say yes.
3. Wait for the actual result and its single reference. Acknowledge the result aloud
   and repeat the reference once, briefly. If part of it is unclear, ask only for that.
4. If nothing permitted is available, say you cannot book and give the reason.
5. Say a brief thank-you and goodbye.
6. Privately call {{REPORT_TOOL}} with one or two sentences: what was booked (date,
   time, name, party size, seating, any charge terms) and the exact reference, or the
   reason nothing was booked. Do not speak the report. After report_saved, call
   {{end_call}}. If saving fails, retry once; never claim it saved.

# User assignment
{TASK_VARIABLE}""".replace("REPORT_TOOL", report_tool).replace("TASK_VARIABLE", variable)


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
            "description": "Privately deliver the outcome to the user in one or two sentences, "
            "after the goodbye and before hangup. This tool never makes a reservation.",
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
                        "description": "One or two sentences: what was booked (date, time, "
                        "name, party size, seating, charge terms) and the exact issued "
                        "reference, or the reason nothing was booked.",
                    }
                ],
            },
        },
        "report_secret_binding": {"report_tool.config.auth.token": "BENCH_TOOLS_SECRET"},
        # v7 completed one live Aditi call (batch a69330e8) but its two-sentence report
        # omitted the booked terms; v8 names them while keeping the same short shape.
        "prompt_version": "natural-caller-v8",
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
