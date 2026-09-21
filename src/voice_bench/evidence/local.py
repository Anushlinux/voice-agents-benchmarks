"""Single-writer, append-only local evidence with atomic, no-clobber publication."""

import asyncio
import fcntl
import hashlib
import json
import os
import re
import tempfile
import time
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from uuid import UUID

from voice_bench.models import EvidenceEvent, EvidenceRef


def canonical(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode()


def digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def safe_path(root: Path, name: str) -> Path:
    parts = PurePosixPath(name).parts
    if not parts or name.startswith("/") or "\\" in name or any(p in {".", ".."} for p in parts):
        raise ValueError("Invalid artifact path")
    path = root.joinpath(*parts)
    if root.is_symlink() or any(p.is_symlink() for p in (path, *path.parents)):
        raise ValueError("Symlinks are not permitted in evidence paths")
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError("Artifact path escapes its root")
    return path


def publish(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(dir=path.parent, prefix=".pending-")
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.link(temporary, path)  # Atomic, fails if the destination already exists.
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        os.unlink(temporary)


class LocalEvidence:
    def __init__(self, root: Path, batch_id: UUID, run_id: UUID, *, recovering=False):
        safe_path(root.absolute(), f"{batch_id}/{run_id}")
        self.root = root.resolve()
        self.run_id = run_id
        self.prefix = f"{batch_id}/{run_id}"
        self.directory = safe_path(self.root, self.prefix)
        self.lock = asyncio.Lock()
        self.sequence = 0
        self.integrity_issues = []
        self.recovering = recovering
        self.clock_id = f"worker-{os.getpid()}-{time.monotonic_ns()}"
        self.directory.mkdir(parents=True, exist_ok=True)
        if (self.directory / "events.jsonl").exists():
            try:
                events = (self.directory / "events.jsonl").read_text().splitlines()
                self.sequence = len(events)
                for n, line in enumerate(events):
                    event = json.loads(line)
                    if event["sequence"] != n or event["run_id"] != str(run_id):
                        raise ValueError("Invalid event identity or sequence")
            except (ValueError, KeyError, UnicodeError) as exc:
                if not recovering:
                    raise ValueError("Corrupt evidence event log; use recovery") from exc
                self.integrity_issues.append("event_log_incomplete_or_invalid")
        self.writer_lock = safe_path(self.directory, ".writer.lock").open("ab")
        try:
            fcntl.flock(self.writer_lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            self.writer_lock.close()
            raise ValueError("Another evidence writer is still active") from exc

    def close_writer(self):
        self.writer_lock.close()

    def _open(self):
        if (self.directory / "manifest.json").exists():
            raise ValueError("Raw evidence is sealed")

    async def append(self, event: EvidenceEvent) -> None:
        async with self.lock:
            self._open()
            if self.recovering:
                raise ValueError("Recovery cannot append to the original event log")
            if event.run_id != self.run_id or event.sequence != self.sequence:
                raise ValueError("Wrong run or nonconsecutive event sequence")
            data = event.model_dump_json().encode() + b"\n"
            await asyncio.to_thread(self._append_bytes, data)
            self.sequence += 1

    def _append_bytes(self, data):
        with safe_path(self.directory, "events.jsonl").open("ab") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())

    async def emit(self, source, kind, payload=None, *, clock_id=None, observed_ns=None):
        await self.emit_many(
            [
                {
                    "source": source,
                    "kind": kind,
                    "payload": payload or {},
                    "clock_id": clock_id,
                    "observed_ns": observed_ns,
                }
            ]
        )

    async def emit_many(self, observations):
        """Durably append one bounded observation batch with one disk synchronization.

        The lock covers allocation and publication; snapshots cannot observe half a batch.
        This does not defer durability beyond the call or change the append-only contract.
        """
        if not observations or len(observations) > 100:
            raise ValueError("Evidence batches must contain 1 to 100 observations")
        async with self.lock:
            self._open()
            if self.recovering:
                raise ValueError("Recovery cannot append to the original event log")
            events = [
                EvidenceEvent(
                    run_id=self.run_id,
                    source=item["source"],
                    kind=item["kind"],
                    sequence=self.sequence + index,
                    clock_id=item.get("clock_id") or self.clock_id,
                    observed_monotonic_ns=item["observed_ns"]
                    if item.get("observed_ns") is not None
                    else time.monotonic_ns(),
                    observed_at=datetime.now(UTC),
                    payload=item.get("payload", {}),
                )
                for index, item in enumerate(observations)
            ]
            await asyncio.to_thread(
                self._append_bytes,
                b"".join(event.model_dump_json().encode() + b"\n" for event in events),
            )
            self.sequence += len(events)

    async def event_snapshot(self):
        """Read complete local events under the writer lock, including before sealing."""
        async with self.lock:
            path = self.directory / "events.jsonl"
            if not path.exists():
                return []
            content = await asyncio.to_thread(path.read_text)
            return [json.loads(line) for line in content.splitlines()]

    async def store_artifact(self, run_id, name, content, media_type="application/octet-stream"):
        async with self.lock:
            self._open()
            if run_id != self.run_id or name.split("/")[0] in {"evaluation", "review"}:
                raise ValueError("Wrong run or reserved artifact namespace")
            if name in {"manifest.json", "events.jsonl"}:
                raise ValueError("Reserved artifact name")
            await asyncio.to_thread(publish, safe_path(self.directory, name), content)
            return EvidenceRef(artifact_key=f"{self.prefix}/{name}", sha256=digest(content))

    async def json(self, name, value):
        return await self.store_artifact(self.run_id, name, canonical(value), "application/json")

    async def finalize(self, run_id, expected=()):
        async with self.lock:
            if run_id != self.run_id:
                raise ValueError("Wrong run")
            self._open()
            items = []
            for path in sorted(self.directory.rglob("*")):
                if path.is_symlink():
                    raise ValueError("Symlink in evidence bundle")
                if path.is_file():
                    name = path.relative_to(self.directory).as_posix()
                    if any(p.startswith(".pending-") for p in path.parts):
                        if not self.recovering:
                            raise ValueError("Unfinished artifact write")
                        self.integrity_issues.append(f"unfinished_artifact:{name}")
                    content = await asyncio.to_thread(path.read_bytes)
                    items.append(
                        {
                            "artifact_key": f"{self.prefix}/{name}",
                            "sha256": digest(content),
                            "size": len(content),
                        }
                    )
            present = {item["artifact_key"][len(self.prefix) + 1 :] for item in items}
            manifest = {
                "schema_version": 1,
                "run_id": str(run_id),
                "artifacts": items,
                "missing": sorted(set(expected) - present),
                "integrity_issues": self.integrity_issues,
                "sealed_at": datetime.now(UTC),
            }
            await asyncio.to_thread(publish, self.directory / "manifest.json", canonical(manifest))
            self.close_writer()
            return tuple(
                EvidenceRef.model_validate({k: x[k] for k in ("artifact_key", "sha256")})
                for x in items
            )


def verify_bundle(directory: Path) -> dict:
    manifest = json.loads((directory / "manifest.json").read_bytes())
    prefix = f"{directory.parent.name}/{directory.name}/"
    for item in manifest["artifacts"]:
        if not item["artifact_key"].startswith(prefix):
            raise ValueError("Manifest references another run")
        path = safe_path(directory, item["artifact_key"][len(prefix) :])
        content = path.read_bytes()
        if digest(content) != item["sha256"] or len(content) != item["size"]:
            raise ValueError(f"Evidence checksum mismatch: {path.name}")
    return manifest


def write_derived(directory: Path, category: str, version: str, value) -> Path:
    if category not in {"evaluation", "review"} or not re.fullmatch(r"[A-Za-z0-9_-]+", version):
        raise ValueError("Invalid derived result version")
    verify_bundle(directory)
    path = safe_path(directory, f"{category}/{version}/result.json")
    publish(path, canonical(value))
    return path
