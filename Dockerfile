FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_NO_CACHE=1

WORKDIR /app
RUN pip install --no-cache-dir uv==0.5.18
COPY pyproject.toml uv.lock README.md ./
COPY src ./src
RUN uv sync --locked --no-dev && useradd --create-home benchmark
USER benchmark

EXPOSE 8000
CMD ["/app/.venv/bin/uvicorn", "voice_bench.api.app:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]
