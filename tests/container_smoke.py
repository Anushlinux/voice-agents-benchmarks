"""Provider-free container acceptance: persistent state, Chromium and an S3 endpoint."""

import asyncio
import json
import os
import platform
import tempfile
from pathlib import Path
from uuid import uuid4

import boto3
import httpx

from voice_bench.channels.browser.adapter import BrowserSession
from voice_bench.evidence.local import LocalEvidence, verify_bundle
from voice_bench.evidence.s3 import S3Artifacts
from voice_bench.fixture import execute_fixture
from voice_bench.models import AudioFrame
from voice_bench.storage import PostgresStore


async def main():
    async with httpx.AsyncClient() as client, asyncio.timeout(45):
        while True:
            try:
                response = await client.get(os.environ["S3_TEST_ENDPOINT"] + "/minio/health/live")
                response.raise_for_status()
                break
            except httpx.HTTPError:
                await asyncio.sleep(0.5)
    root = Path(tempfile.mkdtemp(prefix="voice-bench-acceptance-"))
    fixture = await execute_fixture(PostgresStore(os.environ["DATABASE_URL"]), root)
    evidence = LocalEvidence(root, uuid4(), uuid4())
    session = BrowserSession(evidence)
    try:
        await session.start({}, test=True)
        await session.page.evaluate("bridge.testInput()")
        await session.send_audio(
            AudioFrame(
                pcm_s16le=b"\x00\x10" * 24000,
                sample_rate_hz=24000,
                sample_offset=0,
                clock_id="fixture",
                observed_monotonic_ns=0,
                item_id="smoke",
            )
        )
        async with asyncio.timeout(10):
            while session.played.get("smoke", 0) < 100:
                await asyncio.sleep(0.02)
            while not any((await session.incoming.get()).pcm_s16le):
                pass
        played = await session.cancel_playback()
        assert 0 < played["smoke"] < 1000
    finally:
        await session.close("container fixture complete")
    await evidence.finalize(evidence.run_id)
    verify_bundle(evidence.directory)
    client = boto3.client(
        "s3",
        endpoint_url=os.environ["S3_TEST_ENDPOINT"],
        region_name="us-east-1",
        aws_access_key_id="fixture-access",
        aws_secret_access_key="fixture-secret-only",
    )
    bucket = "voice-bench-" + uuid4().hex
    client.create_bucket(Bucket=bucket)
    storage = S3Artifacts(bucket, client=client)
    for directory in (evidence.directory, root / fixture["batch_id"] / fixture["run_ids"][0]):
        uploaded = storage.upload(directory)
        assert storage.upload(directory) == uploaded
    print(
        json.dumps(
            {
                "provider_calls": 0,
                "fixture": fixture["harness_validation"],
                "browser": "passed",
                "s3": "passed",
                "architecture": platform.machine(),
            }
        )
    )


if __name__ == "__main__":
    asyncio.run(main())
