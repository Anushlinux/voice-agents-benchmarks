import json
from uuid import uuid4

import pytest

from voice_bench.channels.browser.adapter import BrowserSession
from voice_bench.evaluation.diagnostics import conversation_diagnostics
from voice_bench.evidence.local import LocalEvidence


def saved(tmp_path, events, *, owner="unknown"):
    documents = {
        "result.json": {"attribution": owner, "termination_confirmed": True},
        "config/case.json": {"completion": "target_report_then_conversation_end"},
        "business/final.json": {"bookings": [{"reference": "SIM-TEST"}]},
        "evaluation/auto-v2/result.json": {"validity": "valid", "outcome": "unresolved"},
    }
    for name, value in documents.items():
        path = tmp_path / name
        path.parent.mkdir(exist_ok=True, parents=True)
        path.write_text(json.dumps(value))
    (tmp_path / "events.jsonl").write_text(
        "\n".join(
            json.dumps(
                dict(sequence=i, clock_id="worker-test", observed_at="2026-09-21T00:00:00Z") | event
            )
            for i, event in enumerate(events)
        )
    )
    return conversation_diagnostics(tmp_path, {"playback_integrity": {"status": "passed"}})


def test_silent_packets_do_not_assign_blame_or_hide_missing_report(tmp_path):
    events = [
        {"kind": "playback_progress", "payload": {"played_ms": 2000}},
        *[
            {
                "kind": "transport_observation",
                "payload": {
                    "name": "audio_transport_stats",
                    "direction": "incoming",
                    "track_id": "a",
                    "status": "available",
                    "rows": [{"packetsReceived": 300, "totalAudioEnergy": 0}],
                },
            }
        ]
        * 2,
        {"kind": "conversation_idle_timeout", "payload": {"seconds": 15}},
    ]
    result = saved(tmp_path, events)
    assert result["simulation_validity"] == "valid"
    assert result["observed_task_completion"] == "incomplete"
    assert result["recorded_bookings"] == 1
    assert result["automated_target_outcome"] == "unresolved"
    assert result["established_failure_owner"] == "unknown"
    assert result["last_completed_step"]["sequence"] == 0
    assert result["transport"]["tracks"][0]["available"] == 2


def test_old_evidence_remains_unavailable_and_rejected_tools_are_not_progress(tmp_path):
    result = saved(
        tmp_path,
        [{"kind": "business_tool_result", "payload": {"result": {"ok": False}}}],
        owner="simulator",
    )
    assert result["transport"]["status"] == "unavailable"
    assert result["last_completed_step"] is None
    assert result["established_failure_owner"] == "simulator"
    assert len(result["event_anchors"]) == 1


@pytest.mark.asyncio
async def test_transport_event_keeps_worker_clock_and_browser_clock_separate(tmp_path):
    evidence = LocalEvidence(tmp_path, uuid4(), uuid4())
    session = BrowserSession(evidence)
    try:
        await session.event(
            None,
            {
                "type": "transport_observation",
                "name": "audio_transport_stats",
                "performance_ms": 123.4,
                "audio_context_seconds": 0.2,
                "status": "unavailable",
                "rows": [],
            },
        )
        await session.flush_evidence()
        event = (await evidence.event_snapshot())[-1]
        assert event["clock_id"] == evidence.clock_id
        assert event["payload"]["performance_clock"] == "browser-performance"
        assert event["payload"]["audio_clock"] == "chromium-audio-context"
        assert event["payload"]["performance_ms"] == 123.4
        assert not session.error
    finally:
        await session.close("test")
