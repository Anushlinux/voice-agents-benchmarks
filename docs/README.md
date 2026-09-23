# Working on the benchmark

**Looking for results?** Open the [web-call report](../reports/webcall/README.md) or [telephony report](../reports/telephony/README.md).

| Guide | What it covers |
| --- | --- |
| [Running the benchmark](RUNNING.md) | Setup, execution, evaluation and recovery |
| [Architecture](ARCHITECTURE.md) | Audio, actors, business tools, evidence and grading |
| [Scope](SCOPE.md) | Supported tasks and role boundaries |
| [Rumik and Plivo setup](RUMIK_PLIVO_SETUP.md) | Hosted assistant configuration and phone transport |
| [Jev evaluation](JEV.md) | Independent second-opinion judgments |
| [Infrastructure](../infra/README.md) | Containers and local services |

Use Python 3.12 and uv. Provider-free development checks:

```sh
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked pytest
```

Database and browser integration checks need the local services described in the running guide. Live calls require a separately authorized, funded run.

The restaurant pilot, hard-case, critique and P0 investigation documents are historical design/debugging notes. Their run statuses do not replace the [current reports](../reports/README.md). The root `product.md` is also an earlier implementation write-up.
