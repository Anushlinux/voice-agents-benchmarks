import json
import socket
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from voice_bench.api.app import create_app
from voice_bench.cli import main
from voice_bench.settings import load_config

CONFIG = Path(__file__).resolve().parents[1] / "configs" / "local.toml"


def test_plan_is_offline_and_does_not_create_artifacts(tmp_path, monkeypatch, capsys):
    def reject_network(*args, **kwargs):
        raise AssertionError("Planning must not create network connections")

    monkeypatch.setattr(socket, "create_connection", reject_network)
    monkeypatch.setattr(socket.socket, "connect", reject_network)
    config = tmp_path / "local.toml"
    config.write_text(CONFIG.read_text().replace('"../artifacts"', '"results"'))
    assert main(["plan", "--config", str(config)]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["live_calls_supported"] is False
    assert output["config"]["artifact_root"] == str(tmp_path / "results")
    assert not (tmp_path / "results").exists()


@pytest.mark.parametrize(
    ("old", "new"),
    [
        ("max_concurrent_calls = 1", "max_concurrent_calls = 0"),
        ("max_call_seconds = 300", "max_call_seconds = -1"),
        ('channels = ["browser", "phone"]', 'channels = ["browser", "browser"]'),
    ],
)
def test_bad_execution_configuration_is_rejected(tmp_path, old, new):
    path = tmp_path / "bad.toml"
    path.write_text(CONFIG.read_text().replace(old, new))
    with pytest.raises(ValidationError):
        load_config(path)


def test_cli_reports_bad_config_without_success_output(tmp_path, capsys):
    path = tmp_path / "broken.toml"
    path.write_text("name = [")
    assert main(["plan", "--config", str(path)]) == 2
    output = capsys.readouterr()
    assert output.out == ""
    assert "Configuration error" in output.err


def test_api_distinguishes_process_health_from_live_readiness():
    with TestClient(create_app()) as client:
        assert client.get("/healthz").status_code == 200
        readiness = client.get("/readyz")
        assert readiness.status_code == 503
        assert readiness.json()["live_calls_supported"] is False
        assert client.post("/runs").status_code == 404
