import json
from uuid import uuid4

import pytest

from voice_bench.evidence.local import LocalEvidence, verify_bundle, write_derived


@pytest.mark.asyncio
async def test_sealing_integrity_missing_evidence_and_rescoring(tmp_path):
    run_id = uuid4()
    sink = LocalEvidence(tmp_path, uuid4(), run_id)
    await sink.emit("controller", "start")
    await sink.json("business/final.json", {"note": "done"})
    with pytest.raises(FileExistsError):
        await sink.json("business/final.json", {"note": "replaced"})
    await sink.finalize(run_id, expected=["audio/received.wav"])
    manifest = verify_bundle(sink.directory)
    assert manifest["missing"] == ["audio/received.wav"]
    before = (sink.directory / "manifest.json").read_bytes()
    with pytest.raises(ValueError, match="sealed"):
        await sink.emit("controller", "late")
    write_derived(sink.directory, "evaluation", "v1", {"outcome": "uncertain"})
    write_derived(sink.directory, "evaluation", "v2", {"outcome": "failed"})
    with pytest.raises(FileExistsError):
        write_derived(sink.directory, "evaluation", "v1", {})
    assert (sink.directory / "manifest.json").read_bytes() == before
    (sink.directory / "business/final.json").write_text("corruption")
    with pytest.raises(ValueError, match="checksum"):
        verify_bundle(sink.directory)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "name", ["../escape", "/tmp/escape", "a/../../escape", "a\\b", "manifest.json", "events.jsonl"]
)
async def test_unsafe_and_reserved_artifact_names(tmp_path, name):
    run_id = uuid4()
    sink = LocalEvidence(tmp_path, uuid4(), run_id)
    with pytest.raises(ValueError):
        await sink.store_artifact(run_id, name, b"bad")


@pytest.mark.asyncio
async def test_symlink_and_corrupt_event_log_rejected(tmp_path):
    run_id, batch_id = uuid4(), uuid4()
    sink = LocalEvidence(tmp_path, batch_id, run_id)
    (sink.directory / "escape").symlink_to(tmp_path)
    with pytest.raises(ValueError):
        await sink.json("escape/bad.json", {})
    (sink.directory / "events.jsonl").write_text('{"sequence": 4}\n')
    with pytest.raises(ValueError, match="Corrupt"):
        LocalEvidence(tmp_path, batch_id, run_id)


@pytest.mark.asyncio
async def test_parallel_event_producers_have_one_sequence(tmp_path):
    import asyncio

    sink = LocalEvidence(tmp_path, uuid4(), uuid4())
    await asyncio.gather(*(sink.emit("caller", "event", {"n": i}) for i in range(30)))
    events = [json.loads(x) for x in (sink.directory / "events.jsonl").read_text().splitlines()]
    assert [e["sequence"] for e in events] == list(range(30))


def test_second_writer_cannot_take_an_active_bundle(tmp_path):
    run_id, batch_id = uuid4(), uuid4()
    first = LocalEvidence(tmp_path, batch_id, run_id)
    with pytest.raises(ValueError, match="writer"):
        LocalEvidence(tmp_path, batch_id, run_id)
    first.close_writer()
    second = LocalEvidence(tmp_path, batch_id, run_id)
    second.close_writer()
