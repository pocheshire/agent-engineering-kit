#!/usr/bin/env python3
"""Install the complete, self-contained AEK skill. No network operations."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile

SOURCE = Path(__file__).resolve().parents[1] / "skills" / "agent-engineering-kit"
RECEIPT = ".aek-skill-receipt.json"


def hashes(root):
    result = {}
    for p in sorted(root.rglob("*")):
        if p.is_symlink():
            raise ValueError("Symlinks are not accepted in skill bundles")
        if p.is_file() and p.name != RECEIPT and "__pycache__" not in p.parts and p.suffix != ".pyc":
            result[p.relative_to(root).as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-dir", type=Path, default=Path.home() / ".agents" / "skills")
    parser.add_argument("--uninstall", action="store_true")
    args = parser.parse_args()
    base = args.skills_dir.expanduser().absolute()
    target = base / "agent-engineering-kit"
    try:
        for p in [target, *target.parents]:
            if p.is_symlink():
                raise ValueError("Refusing symlinked installation path: " + str(p))
        if target.exists():
            receipt = target / RECEIPT
            if not receipt.is_file():
                raise ValueError("Existing skill has no AEK receipt; preserve it and choose another directory")
            state = json.loads(receipt.read_text())
            if not isinstance(state, dict) or state.get("schema") != 1 or state.get("files") != hashes(target):
                raise ValueError("Installed skill changed; inspect local edits before update or removal")
        if args.uninstall:
            if target.exists():
                shutil.rmtree(target)
            print(json.dumps({"removed": str(target), "project_installations": "unchanged"}))
            return 0
        incoming = hashes(SOURCE)
        required = {"LICENSE", "SKILL.md", "core/ENTRY.md", "core/CONTRACT.md", "core/MODES.md", "core/ROUTES.md", "core/VERSION", "core/aek.py"}
        if not required.issubset(incoming):
            raise ValueError("Incomplete source bundle; restore this release from its trusted source")
        version = (SOURCE / "core" / "VERSION").read_text().strip()
        if target.exists() and hashes(target) == incoming:
            print(json.dumps({"status": "unchanged", "version": version, "path": str(target)}))
            return 0
        base.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix=".aek-skill-", dir=base) as temporary:
            staged = Path(temporary) / "bundle"
            shutil.copytree(SOURCE, staged, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            (staged / RECEIPT).write_text(json.dumps({"schema": 1, "version": version, "files": incoming}, indent=2) + "\n")
            backup = Path(temporary) / "previous"
            if target.exists():
                target.rename(backup)
            try:
                staged.rename(target)
            except OSError:
                if backup.exists():
                    backup.rename(target)
                raise
        print(json.dumps({"status": "installed", "version": version, "path": str(target)}))
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
