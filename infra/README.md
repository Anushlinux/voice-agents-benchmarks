# Local infrastructure

The Dockerfile runs the API shell using locked production dependencies. It does
not run a benchmark. PostgreSQL is an optional Compose profile, prepared for
future persistence work and not wired into application startup.

```sh
docker compose up --build api
docker compose --profile database up -d postgres
docker compose --profile database down
```

Local PostgreSQL: database/user `voice_bench`, password `local_only`, port 5432.
These are development-only values. Both published ports bind to 127.0.0.1.
The named database volume survives `down`; add `--volumes` only when you intend
to delete the local database.

The scaffold API has health and readiness routes only. It has no authentication
because it has no business/control endpoints and is for local use. Implement
authentication and callback validation before adding publicly reachable tools.

## Later cloud deployment

- One fixed India worker for caller/audio/browser processing.
- Stable HTTPS/WSS endpoints for business tools and carrier callbacks.
- PostgreSQL for run/state persistence; object storage for raw evidence.
- Secrets injected at runtime, never copied into the container image.
- Independent audio send/receive; asynchronous evidence writes off the audio loop.
- Runtime budget enforcement, cleanup, finalization and stopped-compute proof.

The API image is not yet a media-worker deployment. Add Pipecat dependencies and
Chromium system libraries when those adapters are implemented and qualified.
There is no Vercel config, cloud resource creation or production deployment here.
