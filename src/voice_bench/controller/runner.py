"""Attempt lifecycle. Cleanup and evidence sealing also run on cancellation."""

import asyncio
import time
from uuid import uuid4

from voice_bench.business.environment import WORKFLOWS, BusinessService
from voice_bench.contracts import AttemptResult
from voice_bench.controller.budget import release, reserve
from voice_bench.errors import CallerFailure, HarnessFailure, TransportFailure
from voice_bench.evidence.local import LocalEvidence
from voice_bench.models import CallRequest, FailureAttribution, RunContext, Validity
from voice_bench.scenarios import effective_counterpart


class Controller:
    def __init__(
        self,
        store,
        config,
        channel,
        counterpart,
        target=None,
        *,
        target_agent_id=None,
        target_agent_aliases=(),
    ):
        self.store, self.config = store, config
        self.target_agent_id = target_agent_id or config.target.agent_ref
        self.target_agent_aliases = tuple(target_agent_aliases)
        self.channel, self.counterpart, self.target = channel, counterpart, target

    async def execute(self, plan, case, config_digest, *, run_id=None):
        case.require_supported_execution()
        counterpart_brief = effective_counterpart(
            case.counterpart, case.counterpart_profile, case.scenario_policy
        )
        run_id = run_id or uuid4()
        initial = WORKFLOWS[(case.workflow, case.workflow_version)].initialize(case.initial_state)
        context = RunContext(
            run_id=run_id,
            case_id=case.case_id,
            case_version=case.version,
            repetition=plan.repetition,
            channel=plan.channel,
            config_digest=config_digest,
        )
        run_data = {
            "plan_id": str(plan.plan_id),
            "context": context.model_dump(mode="json"),
            "workflow": case.workflow,
            "workflow_version": case.workflow_version,
            "state": initial,
            "initial_state": case.initial_state,
            "harness_fixture": case.harness_fixture,
            "user_task": case.user_task.model_dump(mode="json"),
            "tool_access": {
                "target": list(case.target_tools),
                "counterpart": list(case.counterpart_tools),
            },
            "task_scope": case.task_scope,
            "call_initiation": case.call_initiation,
            "expected_agent_id": self.target_agent_id,
            "target_agent_aliases": list(self.target_agent_aliases),
            "counterpart_profile": case.counterpart_profile.model_dump(mode="json")
            if case.counterpart_profile
            else None,
            "case_version": case.version,
        }
        await asyncio.to_thread(self.store.create_run, plan.batch_id, run_id, run_data)
        evidence = LocalEvidence(self.config.artifact_root, plan.batch_id, run_id)
        owner = str(uuid4())
        if not await asyncio.to_thread(self.store.claim, run_id, owner):
            raise ValueError("Attempt is owned by another worker")
        result = AttemptResult(run_id=run_id)
        session = None
        dispatch = False
        task_delivered = False
        heartbeat = None
        started = time.monotonic()
        cancelled = False
        failure_stage = "preparation"
        try:
            await evidence.json("config/execution.json", self.config.model_dump(mode="json"))
            await evidence.json("config/case.json", case.model_dump(mode="json"))
            await evidence.json("config/counterpart-brief.json", counterpart_brief.model_dump())
            batch = await asyncio.to_thread(self.store.batch, plan.batch_id)
            if "frozen" in batch:
                await evidence.json("config/frozen-batch.json", batch["frozen"])
            await evidence.json("business/initial.json", case.initial_state)
            await evidence.emit("controller", "prepared")
            await asyncio.to_thread(reserve, self.store, plan.batch_id, run_id, self.config)
            await asyncio.to_thread(self.store.update_run, run_id, phase="connecting")

            async def maintain_lease():
                while True:
                    await asyncio.sleep(5)
                    if not await asyncio.to_thread(self.store.claim, run_id, owner):
                        raise RuntimeError("Worker lease lost")

            heartbeat = asyncio.create_task(maintain_lease())
            dispatch = True
            await asyncio.to_thread(self.store.update_run, run_id, dispatch_intent=True)
            async with asyncio.timeout(self.config.runtime.setup_timeout_seconds):
                failure_stage = "connection"
                session = await self.channel.connect(
                    CallRequest(
                        run=context,
                        agent_ref=self.config.target.agent_ref,
                        max_duration_seconds=self.config.limits.max_call_seconds,
                        setup_timeout_seconds=self.config.runtime.setup_timeout_seconds,
                    ),
                    evidence,
                )
                result = result.model_copy(update={"connected": True})
                failure_stage = "task_delivery"
                await asyncio.to_thread(self.store.update_run, run_id, connected=True)
                while True:
                    session.check_health()
                    delivery = await asyncio.to_thread(self.store.run, run_id)
                    if delivery.get("user_task_served"):
                        task_delivered = True
                        await evidence.json(
                            "target/task-delivery.json", delivery["user_task_delivery"]
                        )
                        break
                    await asyncio.sleep(0.05)
            await asyncio.to_thread(
                self.store.update_run, run_id, phase="in_conversation", connected=True
            )
            await evidence.emit("controller", "connected")
            conversation_options = (
                {"conversation_events": case.conversation_events}
                if case.conversation_events
                else {}
            )
            if case.scenario_policy is not None:
                conversation_options["scenario_policy"] = case.scenario_policy

            async def complete_conversation():
                speaking = asyncio.create_task(
                    self.counterpart.converse(
                        context, counterpart_brief, session, evidence, **conversation_options
                    )
                )
                report_wait = None
                try:
                    if case.completion == "counterpart":
                        return await speaking

                    async def wait_for_report():
                        while True:
                            saved = await asyncio.to_thread(self.store.run, run_id)
                            if saved.get("target_user_report"):
                                await evidence.emit("controller", "target_report_received")
                                await evidence.emit(
                                    "controller",
                                    "end_call_requested",
                                    {"reason": "final_report_received", "owner": "harness"},
                                )
                                return
                            if session.closed.is_set():
                                raise TransportFailure("Target ended without a final report")
                            session.check_health()
                            await asyncio.sleep(0.1)

                    report_wait = asyncio.create_task(wait_for_report())
                    done, _ = await asyncio.wait(
                        {speaking, report_wait}, return_when=asyncio.FIRST_COMPLETED
                    )
                    if speaking in done:
                        try:
                            speaking.result()
                        except TransportFailure:
                            saved = await asyncio.to_thread(self.store.run, run_id)
                            if session.error or not saved.get("target_user_report"):
                                raise
                    await report_wait
                    # The user's delivered final output is the completion trigger.
                    # Do not wait for a second, optional provider hangup signal.
                    speaking.cancel()
                    await asyncio.gather(speaking, return_exceptions=True)
                    if not session.closed.is_set():
                        try:
                            async with asyncio.timeout(
                                min(2, self.config.runtime.finalize_timeout_seconds / 2)
                            ):
                                await session.drain()
                        except Exception as exc:
                            await evidence.emit(
                                "controller",
                                "playback_drain_incomplete",
                                {"type": type(exc).__name__},
                            )
                    await evidence.emit("controller", "ending_after_target_report")
                finally:
                    tasks = [speaking] + ([report_wait] if report_wait else [])
                    for task in tasks:
                        task.cancel()
                    await asyncio.gather(*tasks, return_exceptions=True)

            conversation = asyncio.create_task(complete_conversation())
            failure_stage = "conversation"
            try:
                done, _ = await asyncio.wait(
                    {conversation, heartbeat},
                    timeout=self.config.limits.max_call_seconds,
                    return_when=asyncio.FIRST_COMPLETED,
                )
                if not done:
                    raise TimeoutError("Call duration limit reached")
                for task in done:
                    task.result()
            finally:
                conversation.cancel()
                await asyncio.gather(conversation, return_exceptions=True)
        except asyncio.CancelledError:
            cancelled = True
            result = result.model_copy(
                update={
                    "error": "cancelled",
                    "failure_stage": failure_stage,
                    "attribution": FailureAttribution.HARNESS,
                    "validity": Validity.INVALID,
                }
            )
        except Exception as exc:
            # Exception bodies may contain tokens/URLs; preserve type, not arbitrary provider text.
            result = result.model_copy(
                update={"error": type(exc).__name__, "failure_stage": failure_stage}
            )
            if isinstance(exc, (CallerFailure, HarnessFailure)):
                result = result.model_copy(
                    update={
                        "attribution": FailureAttribution.SIMULATOR,
                        "validity": Validity.INVALID,
                    }
                )
                if isinstance(exc, HarnessFailure):
                    result = result.model_copy(update={"attribution": FailureAttribution.HARNESS})
            if session is not None and not task_delivered:
                result = result.model_copy(
                    update={
                        "attribution": FailureAttribution.HARNESS,
                        "validity": Validity.INVALID,
                    }
                )
                await evidence.emit("controller", "user_task_not_delivered")
            await evidence.emit("controller", "failure", {"type": type(exc).__name__})
        finally:
            await asyncio.to_thread(self.store.update_run, run_id, phase="finalizing")
            confirmed = not dispatch
            if dispatch:
                try:
                    async with asyncio.timeout(self.config.runtime.finalize_timeout_seconds):
                        if session:
                            try:
                                async with asyncio.timeout(
                                    min(5, self.config.runtime.finalize_timeout_seconds / 2)
                                ):
                                    await session.close(result.error or "completed")
                            except Exception as exc:
                                await evidence.emit(
                                    "controller",
                                    "session_cleanup_failed",
                                    {"type": type(exc).__name__},
                                )
                        confirmed = await self.channel.reconcile(run_id, evidence)
                except Exception as exc:
                    await evidence.emit(
                        "controller", "termination_unconfirmed", {"type": type(exc).__name__}
                    )
            business = await asyncio.to_thread(BusinessService(self.store).seal, run_id)
            saved = await asyncio.to_thread(self.store.run, run_id)
            if saved.get("target_user_report"):
                await evidence.json("target/user-report.json", saved["target_user_report"])
            if saved.get("target_report_requests"):
                await evidence.json("target/report-requests.json", saved["target_report_requests"])
            await evidence.json("business/final.json", business["state"])
            await evidence.json("business/audit.json", business["audit"])
            await evidence.json("business/requests.json", business["incoming_requests"])
            await evidence.json("provider/callbacks.json", business["carrier_callbacks"])
            bindings = await asyncio.to_thread(self.store.bindings, run_id)
            await evidence.json("provider/bindings.json", bindings)
            result = result.model_copy(update={"termination_confirmed": confirmed})
            if not confirmed and not result.error:
                result = result.model_copy(
                    update={
                        "error": "TerminationUnconfirmed",
                        "failure_stage": "shutdown",
                        "attribution": FailureAttribution.UNKNOWN,
                    }
                )
            await evidence.json("result.json", result.model_dump(mode="json"))
            await evidence.emit(
                "controller",
                "finalized",
                {"termination_confirmed": confirmed, "elapsed_seconds": time.monotonic() - started},
            )
            await evidence.finalize(
                run_id,
                expected=("audio/received.wav", "audio/sent.wav", "provider/rumik-call.json"),
            )
            await asyncio.to_thread(
                self.store.update_run,
                run_id,
                phase="grading",
                termination_confirmed=confirmed,
                result=result.model_dump(mode="json"),
                evidence_sealed=True,
            )
            await asyncio.to_thread(release, self.store, run_id, confirmed)
            if confirmed:
                await asyncio.to_thread(self.store.release_route, run_id)
            if heartbeat:
                heartbeat.cancel()
                await asyncio.gather(heartbeat, return_exceptions=True)
            await asyncio.to_thread(self.store.expire_lease, run_id, owner)
        if cancelled:
            raise asyncio.CancelledError
        return result
