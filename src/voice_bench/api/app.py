"""Import-safe API shell. Starting it never initializes provider clients."""

import asyncio
import hmac
import json
from urllib.parse import parse_qsl
from uuid import UUID

from fastapi import FastAPI, Header, HTTPException, Request, WebSocket
from fastapi.responses import JSONResponse, Response
from pydantic import Field, ValidationError

from voice_bench import __version__
from voice_bench.business.environment import BusinessService
from voice_bench.contracts import ToolRequest
from voice_bench.evidence.local import canonical, digest
from voice_bench.models import Contract
from voice_bench.readiness import scaffold_status


class BeforeCall(Contract):
    call_id: str = Field(min_length=1)
    agent_id: str = Field(min_length=1)
    phone_number: str = ""


def create_app(store=None, tools_secret=None, phone_hub=None) -> FastAPI:
    app = FastAPI(
        title="Voice Agent Benchmark",
        version=__version__,
        description="Benchmark health, authenticated business tools, and carrier callbacks.",
    )

    @app.get("/healthz")
    def health() -> dict[str, str]:
        return {"status": "ok", "stage": "implemented_unqualified"}

    @app.get("/readyz", status_code=503)
    def readiness() -> JSONResponse:
        return JSONResponse(status_code=503, content=scaffold_status())

    if store is not None and tools_secret:
        business = BusinessService(store)

        def authorize(authorization):
            if not authorization or not hmac.compare_digest(
                authorization, f"Bearer {tools_secret}"
            ):
                raise HTTPException(401, "Invalid tool authentication")

        @app.post("/tools/rumik/before-call")
        def before_call(body: BeforeCall, authorization: str | None = Header(default=None)):
            authorize(authorization)
            try:
                try:
                    run_id = store.resolve("rumik", body.call_id)
                except KeyError:
                    run_id = store.bind_phone(body.phone_number, body.agent_id, body.call_id)
                run = store.run(run_id)
                if not run["accept_tools"]:
                    raise ValueError("Attempt closed")
                return {"benchmark_ready": True}
            except (ValueError, KeyError) as exc:
                raise HTTPException(409, "Uncorrelated or closed call") from exc

        @app.post("/tools/rumik/{tool_name}")
        async def execute_tool(
            tool_name: str, request: Request, authorization: str | None = Header(default=None)
        ):
            authorize(authorization)
            try:
                raw = await request.body()
                if len(raw) > 65536:
                    raise HTTPException(413, "Tool request too large")
                payload = json.loads(raw)
                if not isinstance(payload, dict) or not isinstance(payload.get("call_id"), str):
                    raise HTTPException(422, "A provider call ID is required")
                await asyncio.to_thread(
                    business.record_request, payload["call_id"], tool_name, raw.decode()
                )
                body = ToolRequest.model_validate(payload)
                return await asyncio.to_thread(
                    business.execute_call,
                    body.call_id,
                    tool_name,
                    body.arguments,
                    body.operation_id,
                )
            except (ValidationError, json.JSONDecodeError, UnicodeError) as exc:
                raise HTTPException(422, "Malformed tool request") from exc
            except (KeyError, ValueError) as exc:
                raise HTTPException(409, "Uncorrelated or invalid tool request") from exc

    if phone_hub is not None:
        from plivo.utils import validate_v3_signature

        def signature(headers, method, path, params=None, query="", websocket=False):
            base = phone_hub.config.runtime.public_base_url.rstrip("/")
            if websocket:
                base = base.replace("https://", "wss://", 1)
            url = base + path + ("?" + query if query else "")
            try:
                return validate_v3_signature(
                    method,
                    url,
                    headers.get("x-plivo-signature-v3-nonce", ""),
                    phone_hub.client.token,
                    headers.get("x-plivo-signature-v3", ""),
                    params or {},
                )
            except Exception:
                return False

        async def signed_form(request):
            body = await request.body()
            if len(body) > 65536:
                raise HTTPException(413, "Callback too large")
            pairs = parse_qsl(body.decode(), keep_blank_values=True)
            params = dict(pairs)
            if len(pairs) != len(params) or not signature(
                request.headers, "POST", request.url.path, params, request.url.query
            ):
                raise HTTPException(401, "Invalid carrier signature")
            return params

        @app.post("/callbacks/plivo/answer/{run_id}")
        async def answer(run_id: UUID, request: Request):
            params = await signed_form(request)
            try:
                xml = await asyncio.to_thread(phone_hub.answer, run_id, params)
            except (KeyError, ValueError) as exc:
                raise HTTPException(409, "Unknown call or mismatched route") from exc
            return Response(xml, media_type="application/xml")

        @app.post("/callbacks/plivo/status/{run_id}")
        async def carrier_status(run_id: UUID, request: Request):
            params = await signed_form(request)

            def save():
                phone_hub.correlate(run_id, params)
                with store.locked_run(run_id) as run:
                    callbacks = run.setdefault("carrier_callbacks", {})
                    callbacks.setdefault(digest(canonical(params)), params)

            try:
                await asyncio.to_thread(save)
            except (KeyError, ValueError) as exc:
                raise HTTPException(409, "Unknown carrier call") from exc
            session = phone_hub.sessions.get(run_id)
            if session and (
                params.get("CallStatus") == "completed" or params.get("Event") == "failed"
            ):
                session.closed.set()
            return {"ok": True}

        @app.websocket("/callbacks/plivo/media/{run_id}/{token}")
        async def carrier_media(run_id: UUID, token: str, websocket: WebSocket):
            session = phone_hub.sessions.get(run_id)
            if (
                not session
                or not hmac.compare_digest(session.token, token)
                or session.socket is not None
                or not signature(
                    websocket.headers,
                    "GET",
                    websocket.url.path,
                    query=websocket.url.query,
                    websocket=True,
                )
            ):
                await websocket.close(code=1008)
                return
            await websocket.accept()
            await session.attach(websocket)

    return app
