# Local and India worker packaging

The Dockerfile has `api` and `worker` targets. Both use Python 3.12 and locked Python dependencies. Base images are pinned by digest. A Node build stage bundles LiveKit and the audio worklet locally. The worker adds Chromium headless shell and its Linux libraries, runs as a non-root user, and defaults to provider-free `status`.

```sh
docker compose --profile database up -d postgres
docker build --target worker -t voice-bench-worker .
docker run --rm voice-bench-worker status
docker compose --profile worker --profile database run --rm worker fixture --config /app/configs/local.toml
```

The named PostgreSQL volume persists across `docker compose down`. The development credentials are `voice_bench` / `local_only`; never use them for a cloud database. Mount a writable artifact volume owned by the worker user (UID 1000). Local Compose publishes only loopback ports. The API and live worker use the same port, so do not publish both simultaneously.

`docker compose up --build api` starts only the provider-free health API. The `run --live` command inside a worker owns its authenticated callback server. Model credentials and tool secrets are injected at runtime, never baked into the image.

## Fixed India deployment configuration

`india-worker.compose.yaml` supplies an explicit Linux amd64 worker environment, India timezone/region declaration, shared memory and resource limits. Apply it on an already provisioned India host:

```sh
docker compose -f compose.yaml -f infra/india-worker.compose.yaml --profile worker config
```

The default command is still `status`. Choose an explicit funded live command only for an authorized run. Configure your existing HTTPS/WSS ingress, private PostgreSQL, persistent artifacts, secrets, and S3-compatible bucket outside this repository. The region declaration does not move a host into India; verify the VM and media route independently during qualification. Freeze the built image digest for each reported batch.

No VM, numbers, buckets, DNS, TLS certificates, or hosted target agents are provisioned here. A worker completion file proves that its scheduling and owned connections stopped. Confirm infrastructure shutdown separately if the qualification requires stopped compute.

## Validation boundary

The implementation was tested with local PostgreSQL and Chromium. An intermediate Linux arm64 worker image built locally. Container startup then exhausted available host disk, so integrated container validation and a final-source image rebuild remain pending. CI builds the worker and runs its provider-free smoke command. `tests/container_smoke.py` additionally exercises PostgreSQL, real Chromium audio and an S3 endpoint together when those services are available. Follow the full container and live qualification checklist in `docs/IMPLEMENTATION.md` before reporting benchmark results.


To run the integrated provider-free acceptance test on a machine with adequate free disk:

```sh
docker compose -f infra/validation.compose.yaml up --build --abort-on-container-exit --exit-code-from worker
docker compose -f infra/validation.compose.yaml down --volumes
```

This isolated network has temporary PostgreSQL and MinIO stores, no published ports, and no provider credentials. The worker exercises the business fixture, Chromium audio and immutable uploads. MinIO is a disposable compatibility test service, not a production deployment recommendation. On the implementation machine, roughly 7 GB free before the build was insufficient for Docker's images and cache.

After that disk-space failure, the worker was reduced to Chromium headless shell and removes package-manager indexes. This final packaging change still needs an image rebuild and integrated acceptance run.
