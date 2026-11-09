#!/usr/bin/env python3
"""Install or explicitly repair the complete AEK skill. No network operations."""
import argparse
import hashlib
import importlib.util
import json
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


def source_identity():
    # This is the verifier from the reviewed source being run, never the damaged target.
    spec = importlib.util.spec_from_file_location("aek_source_validator", SOURCE / "core" / "aek.py")
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except (ImportError, SyntaxError, AttributeError) as exc:
        raise ValueError("Incomplete or inconsistent source bundle: " + str(exc)) from exc
    try:
        version, unused = module.validate_skill_bundle(SOURCE)
    except module.Conflict as exc:
        raise ValueError("Incomplete or inconsistent source bundle: " + str(exc)) from exc
    return version, module


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-dir", type=Path, default=Path.home() / ".agents" / "skills")
    operation = parser.add_mutually_exclusive_group()
    operation.add_argument("--uninstall", action="store_true")
    operation.add_argument("--repair", action="store_true", help="Restore the exact installed receipt from this trusted release")
    parser.add_argument("--replace", action="append", default=[], help="With --repair, explicitly replace a confirmed damaged relative file")
    parser.add_argument("--allow-major", action="store_true", help="Only after reviewing an authorized major migration")
    args = parser.parse_args()
    base = args.skills_dir.expanduser().absolute()
    target = base / "agent-engineering-kit"
    try:
        for p in [target, *target.parents]:
            if p.is_symlink():
                raise ValueError("Refusing symlinked installation path: " + str(p))
        if args.replace and not args.repair:
            raise ValueError("--replace is only accepted with --repair")
        state, receipt_bytes = None, None
        current = hashes(target) if target.exists() else {}
        if target.exists():
            receipt = target / RECEIPT
            if not receipt.is_file():
                raise ValueError("Existing skill has no AEK receipt; preserve it and choose another directory")
            receipt_bytes = receipt.read_bytes()
            state = json.loads(receipt_bytes)
            if (not isinstance(state, dict) or type(state.get("schema")) is not int or state["schema"] != 1
                    or not isinstance(state.get("files"), dict) or not isinstance(state.get("version"), str)):
                raise ValueError("Unsupported skill receipt; inspect it before update or removal")
            if not args.repair and state["files"] != current:
                raise ValueError("Installed skill changed; inspect local edits or repair the exact pin before updating")
        if args.uninstall:
            if target.exists():
                shutil.rmtree(target)
            print(json.dumps({"removed": str(target), "project_installations": "unchanged"}))
            return 0
        incoming = hashes(SOURCE)
        required = {"LICENSE", "SKILL.md", "core/LICENSE", "core/ENTRY.md", "core/CONTRACT.md", "core/MODES.md", "core/ROUTES.md", "core/VERSION", "core/aek.py"}
        if not required.issubset(incoming):
            raise ValueError("Incomplete source bundle; restore this release from its trusted source")
        version, validator = source_identity()
        selected = set(args.replace)
        if args.repair:
            if state is None or state["version"] != version or state["files"] != incoming:
                raise ValueError("Repair requires the exact installed version and complete receipt hashes")
            if not selected.issubset(incoming) or set(current) - set(incoming):
                raise ValueError("Unknown replacement or untracked installed content; review before repair")
            divergent = [name for name, digest in current.items() if digest != incoming[name] and name not in selected]
            if divergent:
                raise ValueError("Existing divergence may be a local adaptation; explicit --replace required: " + ", ".join(sorted(divergent)))
        elif state is not None:
            installed_version, unused = validator.validate_skill_bundle(target)
            if installed_version != state["version"]:
                raise ValueError("Installed version differs from its receipt")
            old_order, new_order = validator.parse_version(installed_version), validator.parse_version(version)
            if new_order < old_order:
                raise ValueError("Downgrade requires a separate rollback plan")
            if new_order == old_order and incoming != state["files"]:
                raise ValueError("Same version precedence has different content; use a newer release")
            if old_order[0] != new_order[0] and not args.allow_major:
                raise ValueError("Major update requires a reviewed migration and explicit --allow-major")
        if target.exists() and current == incoming:
            print(json.dumps({"status": "unchanged", "version": version, "path": str(target)}))
            return 0
        base.mkdir(parents=True, exist_ok=True)
        staging = Path(tempfile.mkdtemp(prefix=".aek-skill-", dir=base))
        backup, keep_backup = staging / "previous", False
        try:
            staged = staging / "bundle"
            shutil.copytree(SOURCE, staged, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            if hashes(staged) != incoming:
                raise ValueError("Source changed while staging; installation was not modified")
            data = receipt_bytes if args.repair else (json.dumps({"schema": 1, "version": version, "files": incoming}, indent=2) + "\n").encode()
            (staged / RECEIPT).write_bytes(data)
            if target.exists():
                target.rename(backup)
            try:
                staged.rename(target)
            except OSError:
                if backup.exists():
                    try:
                        backup.rename(target)
                    except OSError as exc:
                        keep_backup = True
                        raise ValueError("Rollback could not complete; original installation preserved at " + str(backup)) from exc
                raise
        finally:
            if not keep_backup:
                shutil.rmtree(staging)
        print(json.dumps({"status": "repaired" if args.repair else "installed", "version": version, "path": str(target)}))
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2
    except Exception as exc:
        # A malformed trusted source's validator still fails closed with a recovery diagnostic.
        print(json.dumps({"error": "Source validation failed: " + str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
