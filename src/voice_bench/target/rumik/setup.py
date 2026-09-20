"""Dataset-independent setup plans and checks for the documented Rumik/Plivo contract."""

import json
from urllib.parse import urlsplit

from voice_bench.evidence.local import canonical, digest


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
        "secret_binding": {"tool.config.auth.token": "BENCH_TOOLS_SECRET"},
        "variable": {"name": variable, "defaultValue": "", "toolOutput": "user_task_json"},
        "variable_tool_binding": (
            "Set variable.toolId to the actual before-call tool ID returned by Rumik."
        ),
        "prompt_instruction": (
            "Act on behalf of the user whose assignment is provided below as JSON. "
            "Follow request, known_facts, constraints and permissions. "
            "Speak with the other person; "
            "do not impersonate them. If the assignment is empty, do not act.\n"
            + "{"
            + variable
            + "}"
        ),
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
