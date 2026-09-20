"""Explicit HTTP operations on the hosted target. No provisioning side effects."""

from copy import deepcopy

import httpx

from voice_bench.evidence.local import canonical, digest


class RumikClient:
    def __init__(self, key: str, *, transport=None, base_url="https://silk-api.rumik.ai"):
        self.client = httpx.AsyncClient(
            base_url=base_url,
            timeout=20,
            transport=transport,
            headers={"Authorization": f"Bearer {key}"},
        )

    async def close(self):
        await self.client.aclose()

    async def get(self, path):
        response = await self.client.get(path)
        response.raise_for_status()
        return response.json()

    async def snapshot(self, agent_ref):
        agent = await self.get(f"/v1/agents/{agent_ref}")
        versions = await self.get(f"/v1/agents/{agent_ref}/versions")
        tools = await self.get("/v1/tools")
        variables = await self.get("/v1/variables")
        voices = await self.get("/v1/voices")
        reserved = {"call_id", "agent_id", "phone_number", "user_id"}
        for variable in variables.get("items", []):
            if variable["name"].lower() in reserved:
                raise ValueError("Account variable shadows a trusted call-context field")
        for tool in tools.get("items", []):
            params = tool.get("config", {}).get("llmParams", [])
            if any(p["name"].lower() in reserved for p in params):
                raise ValueError("Tool argument shadows a trusted call-context field")
        result = {
            "agent": agent,
            "versions": versions,
            "tools": tools,
            "variables": variables,
            "voices": voices,
        }
        return result

    async def register(self, agent_ref):
        response = await self.client.post("/v1/register-call", json={"agent_id": agent_ref})
        response.raise_for_status()
        return response.json()

    async def start_browser(self, token):
        request = self.client.build_request("POST", "/v1/webcall", json={"accessToken": token})
        del request.headers["Authorization"]
        response = await self.client.send(request)
        response.raise_for_status()
        return response.json()

    async def call(self, call_id):
        return await self.get(f"/v1/calls/{call_id}")

    async def recording(self, url):
        # Signed recording URLs are credentials; never send the Rumik API key with them.
        if not url.startswith("https://"):
            raise ValueError("Recording URL must use HTTPS")
        async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.content


def snapshot_digest(snapshot):
    value = deepcopy(snapshot)
    # Hash only stable configuration, not unrelated usage or polling timestamps.
    agent_fields = (
        "id",
        "handle",
        "systemInstruction",
        "greeting",
        "ttsConfig",
        "language",
        "callSettings",
        "deployed",
        "inboundPhoneNumber",
    )
    value["agent"] = {k: value["agent"].get(k) for k in agent_fields}
    return digest(canonical(value))


def qualify_snapshot(snapshot, config):
    agent = snapshot["agent"]
    if not agent.get("deployed"):
        raise ValueError("Target is not deployed")
    versions = snapshot["versions"]
    versions = versions.get("items", []) if isinstance(versions, dict) else versions
    active = [v for v in versions if v.get("status") == "active"]
    if len(active) != 1 or config.target.deployed_version not in {
        str(active[0].get("id")),
        str(active[0].get("versionNumber")),
    }:
        raise ValueError("Deployed version does not match the requested frozen version")
    if "phone" in config.channels:
        engine = agent.get("ttsConfig", {}).get("model")
        supported = any(
            v["id"] == engine and v.get("phoneCalls") for v in snapshot["voices"].get("models", [])
        )
        if not supported:
            raise ValueError("Target engine does not support paired telephone calls")
        if agent.get("inboundPhoneNumber") != config.runtime.target_number:
            raise ValueError("Telephone target does not match the agent's inbound number")
