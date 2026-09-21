"""Check speech delivery separately from whether the task was accomplished."""

import json


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
        "boundary": "Local playback only; target interruptions still need semantic review.",
    }
