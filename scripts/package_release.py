#!/usr/bin/env python3
"""Build a deterministic release ZIP from tracked files, without local evidence."""
import hashlib
from pathlib import Path
import sys
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parent))
import distribution

root = Path(__file__).resolve().parents[1]
version = (root / "VERSION").read_text().strip()
try:
    files = distribution.inventory(root)
except RuntimeError as exc:
    raise SystemExit(str(exc))
if not files.is_git:
    raise SystemExit("Release packaging requires a Git checkout")
reserved = [name for name in files.release_files if distribution.is_reserved(name)]
if reserved:
    raise SystemExit("Refusing reserved publication path: " + ", ".join(reserved))
try:
    changed = distribution.working_tree_changes(root)
except RuntimeError as exc:
    raise SystemExit(str(exc))
if changed:
    raise SystemExit("Commit all publication changes before packaging")
content = {}
for name in files.release_files:
    if distribution.path_is_symlink(root, name):
        raise SystemExit("Refusing publication symlink: " + name)
    try:
        content[name] = (root / name).read_bytes()
    except OSError as exc:
        raise SystemExit("Cannot read publication file " + name + ": " + str(exc))
out = root / "dist"
out.mkdir(exist_ok=True)
archive = out / ("agent-engineering-kit-" + version + ".zip")
with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
    for name in sorted(content):
        item = zipfile.ZipInfo("agent-engineering-kit/" + name, (2026, 1, 1, 0, 0, 0))
        item.compress_type = zipfile.ZIP_DEFLATED
        item.external_attr = 0o644 << 16
        bundle.writestr(item, content[name])
checksum = hashlib.sha256(archive.read_bytes()).hexdigest()
(out / "SHA256SUMS").write_text(checksum + "  " + archive.name + "\n")
print(archive.name + " SHA256 " + checksum)
