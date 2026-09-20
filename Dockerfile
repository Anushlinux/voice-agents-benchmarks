FROM node:22-alpine@sha256:b6f26b36c8ff49624cfdac716b8ea1138d606df02586a77d364bb5536a634f85 AS browser-build
WORKDIR /build/browser
COPY browser/package.json browser/package-lock.json ./
RUN npm ci --ignore-scripts
COPY browser/ ./
RUN npm run build

FROM python:3.12-slim@sha256:2f17fc044b579bab302c2e8054d3a686e2cb9a83de48e70534b94cd8ebbe06a9 AS api
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_NO_CACHE=1 \
    PLAYWRIGHT_BROWSERS_PATH=/opt/playwright
WORKDIR /app
RUN pip install --no-cache-dir uv==0.5.18
COPY pyproject.toml uv.lock README.md ./
COPY src ./src
COPY --from=browser-build /build/src/voice_bench/channels/browser/static/ ./src/voice_bench/channels/browser/static/
COPY browser/package-lock.json ./browser/package-lock.json
RUN uv sync --locked --no-dev && useradd --create-home benchmark && mkdir /app/artifacts && chown benchmark /app/artifacts
USER benchmark
EXPOSE 8000
CMD ["/app/.venv/bin/uvicorn", "voice_bench.api.app:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]

FROM api AS worker
USER root
RUN /app/.venv/bin/playwright install --with-deps --only-shell chromium \
    && rm -rf /var/lib/apt/lists/* \
    && chmod -R a+rX /opt/playwright
USER benchmark
ENTRYPOINT ["/app/.venv/bin/voice-bench"]
CMD ["status"]
