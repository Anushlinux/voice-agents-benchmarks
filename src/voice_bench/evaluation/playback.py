"""Check speech delivery separately from whether the task was accomplished."""

import json


def playback_continuity(events):
    items, delays = {}, []
    for event in events:
        payload = event["payload"]
        if event["kind"] in {"received_block", "rendered_block"}:
            delay = payload.get("bridge_delay_ms")
            if delay is not None:
                delays.append(delay)
        if event["kind"] != "playback_progress" or "sample" not in payload:
            continue
        if event.get("clock_id") != "chromium-audio-context":
            continue
        item = items.setdefault(
            payload["item_id"],
            {
                "rate": payload["rate"],
                "end": None,
                "gap_samples": 0,
                "largest_gap_samples": 0,
                "gaps": 0,
            },
        )
        if item["rate"] != payload["rate"]:
            return {"status": "uncertain", "reason": "Playback sample rate changed"}
        if item["end"] is not None:
            gap = payload["sample"] - item["end"]
            if gap < 0:
                return {"status": "uncertain", "reason": "Playback intervals overlap"}
            if gap:
                item["gap_samples"] += gap
                item["largest_gap_samples"] = max(item["largest_gap_samples"], gap)
                item["gaps"] += 1
        item["end"] = payload["sample"] + payload["samples"]
    return {
        "status": "measured" if items else "unavailable",
        "clock_id": "chromium-audio-context",
        "items": [
            {
                "item_id": name,
                "gap_count": item["gaps"],
                "inserted_silence_ms": round(item["gap_samples"] * 1000 / item["rate"], 3),
                "largest_gap_ms": round(item["largest_gap_samples"] * 1000 / item["rate"], 3),
            }
            for name, item in items.items()
        ],
        "max_bridge_delivery_delay_ms": max(delays, default=None),
        "attribution": "unknown",
        "boundary": "Gaps between rendered samples of one generated item; embedded silence "
        "is excluded. Source starvation and local scheduling are not distinguished.",
    }


def playback_integrity(directory):
    events = [json.loads(line) for line in (directory / "events.jsonl").read_text().splitlines()]
    summaries = [e["payload"] for e in events if e["kind"] == "counterpart_playback_summary"]
    if not summaries or not summaries[-1]["items"]:
        return {"status": "unresolved", "reason": "No final per-item playback evidence"}
    items = summaries[-1]["items"]
    # One millisecond covers integer playback checkpoint rounding, not missing words.
    cutoffs = [
        item
        for item in items
        if item["generated_ms"] - item["played_ms"] > 1 and not item["interrupted_by_target"]
    ]
    incomplete = [
        e["payload"]
        for e in events
        if e["kind"] == "response_done" and e["payload"].get("status") in {"incomplete", "failed"}
    ]
    return {
        "status": "failed" if cutoffs or incomplete else "passed",
        "unexplained_cutoffs": cutoffs,
        "incomplete_responses": incomplete,
        "target_interruptions": [i for i in items if i["interrupted_by_target"]],
        "continuity": playback_continuity(events),
        "boundary": "Local playback only; target interruptions still need semantic review.",
    }
