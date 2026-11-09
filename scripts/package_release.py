#!/usr/bin/env python3
"""Build a deterministic release ZIP from tracked files, without local evidence."""
import hashlib
from pathlib import Path
import subprocess
import zipfile

root = Path(__file__).resolve().parents[1]
version = (root / "VERSION").read_text().strip()
if subprocess.check_output(["git", "status", "--porcelain"], cwd=root):
    raise SystemExit("Commit all publication changes before packaging")
files = subprocess.check_output(["git", "ls-files", "-z"], cwd=root).decode().split("\0")
out = root / "dist"
out.mkdir(exist_ok=True)
archive = out / ("agent-engineering-kit-" + version + ".zip")
with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
    for name in sorted(filter(None, files)):
        path = root / name
        if path.is_symlink():
            raise SystemExit("Refusing publication symlink: " + name)
        item = zipfile.ZipInfo("agent-engineering-kit/" + name, (2026, 1, 1, 0, 0, 0))
        item.compress_type = zipfile.ZIP_DEFLATED
        item.external_attr = 0o644 << 16
        bundle.writestr(item, path.read_bytes())
checksum = hashlib.sha256(archive.read_bytes()).hexdigest()
(out / "SHA256SUMS").write_text(checksum + "  " + archive.name + "\n")
print(archive.name + " SHA256 " + checksum)
