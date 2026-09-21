import json

import pytest

from voice_bench.evaluation.playback import playback_integrity


@pytest.mark.parametrize(
    "played,interrupted,status",
    [(6760, False, "failed"), (17350, False, "passed"), (6760, True, "passed")],
)
def test_cutoff_cannot_pass_as_delivered_speech(tmp_path, played, interrupted, status):
    event = {
        "kind": "counterpart_playback_summary",
        "payload": {
            "items": [
                {
                    "item_id": "closing",
                    "generated_ms": 17350,
                    "played_ms": played,
                    "interrupted_by_target": interrupted,
                }
            ]
        },
    }
    (tmp_path / "events.jsonl").write_text(json.dumps(event))
    result = playback_integrity(tmp_path)
    assert result["status"] == status
    assert bool(result["target_interruptions"]) == interrupted


def test_missing_evidence_and_incomplete_generation_cannot_pass(tmp_path):
    path = tmp_path / "events.jsonl"
    path.write_text("")
    assert playback_integrity(tmp_path)["status"] == "unresolved"
    path.write_text(
        "\n".join(
            json.dumps(e)
            for e in [
                {
                    "kind": "counterpart_playback_summary",
                    "payload": {
                        "items": [
                            {
                                "item_id": "cutoff",
                                "generated_ms": 1000,
                                "played_ms": 1000,
                                "interrupted_by_target": False,
                            }
                        ]
                    },
                },
                {"kind": "response_done", "payload": {"status": "incomplete"}},
            ]
        )
    )
    assert playback_integrity(tmp_path)["status"] == "failed"
