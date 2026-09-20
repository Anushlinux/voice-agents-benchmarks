import io
import json
import wave
from uuid import uuid4

import pytest
from botocore.exceptions import ClientError

from voice_bench.evaluation.timing import browser_timing
from voice_bench.evidence.local import LocalEvidence
from voice_bench.evidence.s3 import S3Artifacts


class Objects:
    def __init__(self):
        self.values = {}

    def put_object(self, **args):
        assert args["IfNoneMatch"] == "*"
        if args["Key"] in self.values:
            raise ClientError({"Error": {"Code": "PreconditionFailed"}}, "PutObject")
        self.values[args["Key"]] = args["Body"]

    def get_object(self, **args):
        return {"Body": io.BytesIO(self.values[args["Key"]])}


@pytest.mark.asyncio
async def test_s3_retry_compares_bytes_and_never_overwrites(tmp_path):
    evidence = LocalEvidence(tmp_path, uuid4(), uuid4())
    await evidence.json("business/final.json", {"value": 1})
    await evidence.finalize(evidence.run_id)
    objects = Objects()
    storage = S3Artifacts("test-only", client=objects)
    first = storage.upload(evidence.directory)
    assert storage.upload(evidence.directory) == first
    assert list(objects.values)[-1].endswith("manifest.json")
    key = next(iter(objects.values))
    objects.values[key] = b"different"
    with pytest.raises(ValueError, match="different evidence"):
        storage.upload(evidence.directory)
    assert objects.values[key] == b"different"


def test_timing_uses_browser_sample_positions_and_excludes_overlap(tmp_path):
    (tmp_path / "audio").mkdir()
    events = []
    for name, kind, segments in (
        ("played", "rendered_block", [(0, 800), (2400, 3200), (4800, 5600)]),
        ("received", "received_block", [(1600, 2240), (2800, 3600)]),
    ):
        samples = bytearray(8000 * 2)
        for a, b in segments:
            samples[a * 2 : b * 2] = b"\x00\x10" * (b - a)
        with wave.open(str(tmp_path / f"audio/{name}.wav"), "wb") as audio:
            audio.setparams((1, 2, 8000, 0, "NONE", "none"))
            audio.writeframes(samples)
        events.append(
            {
                "kind": kind,
                "clock_id": "chromium-audio-context",
                "payload": {"sample": 10000, "samples": 8000, "recording_offset": 0, "rate": 8000},
            }
        )
    (tmp_path / "events.jsonl").write_text("\n".join(json.dumps(e) for e in events))
    result = browser_timing(tmp_path)
    assert result["response_gaps_ms"] == [100]
    assert result["overlap_segments"] == 1
    assert result["no_response_segments"] == 1
    events[1]["clock_id"] = "plivo-media"
    (tmp_path / "events.jsonl").write_text("\n".join(json.dumps(e) for e in events))
    assert browser_timing(tmp_path)["status"] == "uncertain"


def test_timing_does_not_bridge_missing_clock_blocks(tmp_path):
    (tmp_path / "audio").mkdir()
    events = []
    for name, kind in (("played", "rendered_block"), ("received", "received_block")):
        with wave.open(str(tmp_path / f"audio/{name}.wav"), "wb") as audio:
            audio.setparams((1, 2, 8000, 0, "NONE", "none"))
            audio.writeframes(b"\x00\x10" * 8000)
        # Both endpoints map; the missing middle must still invalidate the interval.
        for offset in (0, 6000):
            events.append(
                {
                    "kind": kind,
                    "clock_id": "chromium-audio-context",
                    "payload": {
                        "sample": 10000 + offset,
                        "recording_offset": offset,
                        "samples": 2000,
                        "rate": 8000,
                    },
                }
            )
    (tmp_path / "events.jsonl").write_text("\n".join(json.dumps(e) for e in events))
    assert browser_timing(tmp_path)["status"] == "uncertain"
