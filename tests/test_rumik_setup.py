import json
from pathlib import Path
from uuid import uuid4

import httpx
import pytest

from voice_bench.cli import main
from voice_bench.settings import load_config
from voice_bench.target.rumik.client import RumikClient, qualify_snapshot, snapshot_digest
from voice_bench.target.rumik.setup import check_setup, setup_plan


def configured():
    config = load_config(Path("configs/local.toml"))
    config = config.model_copy(
        update={
            "target": config.target.model_copy(
                update={
                    "agent_ref": "unit-agent",
                    "deployed_version": "1",
                    "plivo_sip_trunk_id": uuid4(),
                    "plivo_termination_uri": "unit-test.zt.plivo.com",
                }
            ),
            "runtime": config.runtime.model_copy(
                update={
                    "public_base_url": "https://benchmark.example",
                    "target_number": "+919000000001",
                }
            ),
        }
    )
    plan = setup_plan(config)
    tool = {"id": "tool-id", **plan["tool"]}
    tool["config"]["auth"]["hasSecret"] = True
    variable = {**plan["variable"], "toolId": "tool-id"}
    snapshot = {
        "agent": {
            "id": "unit-agent",
            "deployed": True,
            "systemInstruction": plan["prompt_instruction"],
            "ttsConfig": {"model": "unit-voice"},
        },
        "versions": {"items": [{"status": "active", "id": "version-id", "versionNumber": 1}]},
        "tools": {"items": [tool]},
        "variables": {"items": [variable]},
        "voices": {"models": [{"id": "unit-voice", "phoneCalls": True}]},
        "sip_trunk": {
            "id": str(config.target.plivo_sip_trunk_id),
            "phoneNumber": "+919000000001",
            "assignedAgentId": "unit-agent",
            "status": "active",
            "hasAuth": True,
            "terminationUri": "unit-test.zt.plivo.com",
        },
    }
    snapshot["versions"]["items"][0].update(
        systemInstruction=snapshot["agent"]["systemInstruction"],
        ttsConfig=dict(snapshot["agent"]["ttsConfig"]),
    )
    return config, snapshot


def test_setup_plan_contains_no_secrets_or_scenario_and_checks_plivo_route():
    config, snapshot = configured()
    plan = setup_plan(config)
    assert plan["provider_calls"] == 0
    assert plan["telephony"]["carrier"] == "plivo"
    assert "token" not in plan["tool"]["config"]["auth"]
    assert "user_task_json" in plan["tool"]["config"]["outputs"][0].values()
    assert check_setup(snapshot, config)["configured"]
    assert not check_setup(snapshot, config)["live_qualified"]
    before = snapshot_digest(snapshot)
    snapshot["sip_trunk"]["terminationUri"] = "other.example"
    assert snapshot_digest(snapshot) != before
    with pytest.raises(ValueError, match="Plivo SIP"):
        qualify_snapshot(snapshot, config)


@pytest.mark.parametrize(
    "damage", ["prompt", "variable", "secret", "identity", "output", "trunk", "agent", "default"]
)
def test_incomplete_setup_is_rejected_before_dispatch(damage):
    config, snapshot = configured()
    if damage == "prompt":
        snapshot["agent"]["systemInstruction"] = "No task"
    elif damage == "variable":
        snapshot["variables"]["items"][0]["toolId"] = "wrong"
    elif damage == "secret":
        snapshot["tools"]["items"][0]["config"]["auth"]["hasSecret"] = False
    elif damage == "identity":
        snapshot["tools"]["items"][0]["config"]["body"] = '{"call_id":"static"}'
    elif damage == "output":
        snapshot["tools"]["items"][0]["config"]["outputs"][0]["path"] = "criteria"
    elif damage == "trunk":
        del snapshot["sip_trunk"]
    elif damage == "agent":
        snapshot["sip_trunk"]["assignedAgentId"] = "another-agent"
    elif damage == "default":
        snapshot["variables"]["items"][0]["defaultValue"] = "old task"
    assert not check_setup(snapshot, config)["configured"]


@pytest.mark.asyncio
async def test_outbound_primitive_pins_plivo_trunk_and_allowlisted_destination():
    requests = []
    trunk = uuid4()

    def handler(request):
        requests.append(request)
        body = json.loads(request.content)
        assert body == {
            "agentId": "unit-agent",
            "toNumber": "+919000000002",
            "fromTrunkId": str(trunk),
        }
        return httpx.Response(
            202, json={"callId": "call-id", "status": "calling", "toNumber": body["toNumber"]}
        )

    client = RumikClient("unit-key", transport=httpx.MockTransport(handler))
    try:
        with pytest.raises(ValueError, match="allowlisted"):
            await client.start_outbound(
                "unit-agent",
                "+919000000003",
                plivo_trunk_id=trunk,
                allowed_numbers={"+919000000002"},
            )
        assert not requests
        result = await client.start_outbound(
            "unit-agent", "+919000000002", plivo_trunk_id=trunk, allowed_numbers={"+919000000002"}
        )
        assert result["callId"] == "call-id"
        assert len(requests) == 1
    finally:
        await client.close()


@pytest.mark.asyncio
async def test_outbound_timeout_never_redials():
    requests = []

    def handler(request):
        requests.append(request)
        raise httpx.ReadTimeout("Unknown whether provider accepted", request=request)

    client = RumikClient("unit-key", transport=httpx.MockTransport(handler))
    try:
        with pytest.raises(httpx.ReadTimeout):
            await client.start_outbound(
                "unit-agent",
                "+919000000002",
                plivo_trunk_id=uuid4(),
                allowed_numbers={"+919000000002"},
            )
        assert len(requests) == 1
    finally:
        await client.close()


def test_ordinary_evaluate_cli_still_routes_to_offline_evaluator(tmp_path, capsys):
    # The new Jev branch must not shadow the ordinary evaluate() function.
    assert main(["evaluate", str(tmp_path), "--version", "v1"]) == 2
    assert "FileNotFoundError" in capsys.readouterr().err


@pytest.mark.parametrize("damage", [None, "prompt", "missing", "identity", "secret", "output"])
def test_natural_setup_requires_private_report_contract_and_repaired_prompt(damage):
    from voice_bench.target.rumik.setup import natural_setup_issues

    config, snapshot = configured()
    report = setup_plan(config)["report_tool"]
    from voice_bench.evidence.local import digest

    config = config.model_copy(
        update={
            "target": config.target.model_copy(
                update={"prompt_sha256": digest(snapshot["agent"]["systemInstruction"].encode())}
            )
        }
    )
    report["config"]["auth"]["hasSecret"] = True
    snapshot["tools"]["items"].append(report)
    if damage == "prompt":
        snapshot["agent"]["systemInstruction"] += " Recite a script."
    elif damage == "missing":
        snapshot["tools"]["items"].pop()
    elif damage == "identity":
        report["config"]["llmParams"].append(
            {"name": "call_id", "type": "string", "required": True}
        )
    elif damage == "secret":
        report["config"]["auth"]["hasSecret"] = False
    elif damage == "output":
        report["config"]["outputs"] = []
    assert bool(natural_setup_issues(snapshot, config)) == bool(damage)
