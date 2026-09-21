"""Capture the executed source, including dirty files and built browser assets."""

import io
import tarfile
from pathlib import Path

from voice_bench.evidence.local import digest


def source_snapshot(root=None):
    root = root or Path(__file__).resolve().parents[3]
    paths = {
        *root.glob("src/voice_bench/**/*.py"),
        *root.glob("browser/*.js"),
        *root.glob("src/voice_bench/channels/browser/static/*.js"),
    }
    paths.update(root / name for name in ("pyproject.toml", "uv.lock", "browser/package-lock.json"))
    inventory = {}
    output = io.BytesIO()
    with tarfile.open(fileobj=output, mode="w:gz") as archive:
        for path in sorted(paths):
            if not path.is_file() or path.is_symlink():
                continue
            content = path.read_bytes()
            name = path.relative_to(root).as_posix()
            inventory[name] = digest(content)
            info = tarfile.TarInfo(name)
            info.size = len(content)
            info.mode = 0o644
            archive.addfile(info, io.BytesIO(content))
    return inventory, output.getvalue()
