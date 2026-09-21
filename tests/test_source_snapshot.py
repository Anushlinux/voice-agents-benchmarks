import io
import tarfile

from voice_bench.evidence.source import source_snapshot


def test_source_snapshot_covers_executed_browser_and_python_without_private_data(tmp_path):
    paths = {
        "src/voice_bench/runtime.py": "# dirty Python\n",
        "src/voice_bench/channels/browser/static/bridge.js": "// actual built JavaScript\n",
        "browser/bridge.js": "// dirty browser source\n",
        "uv.lock": "version = 1\n",
        ".env": "SECRET=private\n",
        "artifacts/private.json": "private",
        "browser/node_modules/private.js": "private",
    }
    for name, content in paths.items():
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    first, archive = source_snapshot(tmp_path)
    assert set(first) == set(list(paths)[:4])
    with tarfile.open(fileobj=io.BytesIO(archive)) as bundle:
        assert set(bundle.getnames()) == set(first)
        assert bundle.extractfile("browser/bridge.js").read() == b"// dirty browser source\n"
    path = tmp_path / "src/voice_bench/channels/browser/static/bridge.js"
    path.write_text("// another build\n")
    changed, _ = source_snapshot(tmp_path)
    assert (
        first[path.relative_to(tmp_path).as_posix()]
        != changed[path.relative_to(tmp_path).as_posix()]
    )
