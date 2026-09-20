"""Upload sealed bundles under immutable object keys; never overwrite a different object."""

import base64
import hashlib

from voice_bench.evidence.local import canonical, digest, safe_path, verify_bundle


class S3Artifacts:
    def __init__(self, bucket, *, client=None, endpoint_url=None, region="ap-south-1"):
        if client is None:
            import boto3

            client = boto3.client("s3", endpoint_url=endpoint_url, region_name=region)
        self.client, self.bucket = client, bucket

    def upload(self, directory):
        manifest = verify_bundle(directory)
        prefix = f"{directory.parent.name}/{directory.name}"
        objects = [
            (item["artifact_key"], directory / item["artifact_key"][len(prefix) + 1 :])
            for item in manifest["artifacts"]
        ]
        for category in ("evaluation", "review"):
            for path in sorted((directory / category).glob("*/result.json")):
                name = path.relative_to(directory).as_posix()
                objects.append((f"{prefix}/{name}", safe_path(directory, name)))
        objects.append((f"{prefix}/manifest.json", directory / "manifest.json"))
        for key, path in objects:
            body = path.read_bytes()
            checksum = base64.b64encode(hashlib.sha256(body).digest()).decode()
            try:
                self.client.put_object(
                    Bucket=self.bucket,
                    Key=key,
                    Body=body,
                    IfNoneMatch="*",
                    ChecksumSHA256=checksum,
                    Metadata={"sha256": digest(body)},
                )
            except Exception as exc:
                code = getattr(exc, "response", {}).get("Error", {}).get("Code")
                if code not in {"PreconditionFailed", "412"}:
                    raise
                saved = self.client.get_object(Bucket=self.bucket, Key=key)["Body"].read()
                if digest(saved) != digest(body):
                    raise ValueError("S3 object key already contains different evidence") from exc
        return {
            "bucket": self.bucket,
            "prefix": prefix,
            "manifest_sha256": digest(canonical(manifest)),
        }
