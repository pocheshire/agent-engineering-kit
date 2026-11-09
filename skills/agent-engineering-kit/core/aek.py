#!/usr/bin/env python3
"""Offline AEK instruction installer; never executes project or remote code."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile

CORE = Path(__file__).resolve().parent
REQUIRED = {"LICENSE", "ENTRY.md", "CONTRACT.md", "MODES.md", "ROUTES.md", "VERSION", "aek.py"}
BEGIN, END = b"<!-- AEK:BEGIN -->", b"<!-- AEK:END -->"
BLOCK = (b"\n<!-- AEK:BEGIN -->\n"
         b"For autonomous engineering work, read `.aek/ENTRY.md` before editing.\n"
         b"Local adaptations: `.aek/local.md` and `.aek/project.json`.\n"
         b"<!-- AEK:END -->\n")
ENTRY = b"# Installed AEK\n\nRead `state.json` to resolve the pinned runtime.\nFor vendored installs, read `runtime/ENTRY.md`.\nFor linked installs, resolve `source` relative to the project root and read its `ENTRY.md`.\nRun the kit's `aek.py audit PROJECT` to verify availability and integrity.\nIf unavailable or changed, report the dependency problem; do not silently substitute another kit.\n"

class Conflict(Exception):
    pass

def digest(data):
    return hashlib.sha256(data).hexdigest()

def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()

def project_root(value):
    path = Path(value).expanduser().absolute()
    if path.is_symlink() or not path.is_dir():
        raise Conflict("Target must be an existing, non-symlink project directory")
    return path.resolve()

def safe(root, relative):
    rel = Path(relative)
    if rel.is_absolute() or ".." in rel.parts:
        raise Conflict("Invalid managed path: " + str(relative))
    current = root
    for part in rel.parts:
        current = current / part
        if current.is_symlink():
            raise Conflict("Symlink in managed path: " + str(relative))
    return current

def read(root, relative):
    path = safe(root, relative)
    if path.exists() and not path.is_file():
        raise Conflict("Expected a regular file: " + str(relative))
    return path.read_bytes() if path.exists() else None

def load_json(data, label):
    try:
        value = json.loads(data)
    except (ValueError, TypeError, UnicodeError) as exc:
        raise Conflict("Invalid JSON in " + label) from exc
    if not isinstance(value, dict):
        raise Conflict("Expected JSON object in " + label)
    return value

def source_path(root, source):
    if source is None:
        return CORE
    rel = Path(source)
    if rel.is_absolute():
        raise Conflict("Source must be relative to the target project")
    current = root
    for part in rel.parts:
        current = current / part
        if current.is_symlink():
            raise Conflict("Symlink in source path")
    return current.resolve()

def bundle(directory):
    if not directory.is_dir() or directory.is_symlink():
        raise Conflict("KIT source is unavailable; restore the pinned checkout or provide --source")
    files = {}
    for path in sorted(directory.iterdir()):
        if path.name == "__pycache__":
            continue
        if path.is_symlink():
            raise Conflict("KIT source contains a symlink")
        if path.is_file() and (path.suffix in {".md", ".py"} or path.name in {"VERSION", "LICENSE"}):
            files[path.name] = path.read_bytes()
    if not REQUIRED.issubset(files):
        raise Conflict("KIT source is incomplete")
    version = files["VERSION"].decode().strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?", version):
        raise Conflict("KIT VERSION must be a semantic version")
    return version, files

def state_for(root):
    raw = read(root, ".aek/state.json")
    if raw is None:
        raise Conflict("AEK is not installed")
    state = load_json(raw, "state.json")
    if (type(state.get("schema_version")) is not int or state.get("schema_version") != 1 or not isinstance(state.get("strategy"), str) or state.get("strategy") not in {"vendored", "linked"}
            or not isinstance(state.get("kit_version"), str)):
        raise Conflict("Unsupported installation state; use a compatible KIT version")
    hashes = state.get("baselines")
    if not isinstance(hashes, dict) or not REQUIRED.issubset(hashes):
        raise Conflict("Invalid installation baselines")
    for name, value in hashes.items():
        if Path(name).name != name or not re.fullmatch(r"[0-9a-f]{64}", str(value)):
            raise Conflict("Invalid managed file baseline")
    if state["strategy"] == "linked":
        if not isinstance(state.get("source"), str) or Path(state["source"]).is_absolute():
            raise Conflict("Invalid linked source")
    return state

def transact(root, changes):
    """Preflight every destination; roll back file contents after an I/O failure."""
    before = {name: read(root, name) for name in changes}
    written = []
    try:
        for name, data in changes.items():
            path = safe(root, name)
            if data == before[name]:
                continue
            if data is None:
                if path.exists():
                    path.unlink()
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                with tempfile.NamedTemporaryFile(dir=str(path.parent), delete=False) as temporary:
                    temporary.write(data)
                    temporary_name = temporary.name
                try:
                    os.replace(temporary_name, path)
                finally:
                    if os.path.exists(temporary_name):
                        os.unlink(temporary_name)
            written.append(name)
    except OSError:
        for name in reversed(written):
            path = safe(root, name)
            if before[name] is None:
                path.unlink(missing_ok=True)
            else:
                path.write_bytes(before[name])
        raise
    return written

def marker_check(data):
    if data is None or data.count(BEGIN) != 1 or data.count(END) != 1 or data.count(BLOCK) != 1:
        raise Conflict("AGENTS.md AEK block was changed or is ambiguous; reconcile it manually")

def install(target, mode="adopt", strategy="vendored", source=None):
    root = project_root(target)
    if strategy == "linked" and source is None:
        raise Conflict("Linked installation requires an explicit project-relative --source")
    directory = source_path(root, source)
    version, files = bundle(directory)
    raw_state = read(root, ".aek/state.json")
    if raw_state is not None:
        state = state_for(root)
        expected_source = Path(os.path.relpath(directory, root)).as_posix() if strategy == "linked" else None
        if (state["kit_version"] != version or state["strategy"] != strategy
                or state.get("source") != expected_source
                or state["baselines"] != {name: digest(data) for name, data in files.items()}):
            raise Conflict("Different installation already exists; use upgrade after reviewing the plan")
        result = audit(root)
        if result["static_validation"] != "pass":
            raise Conflict("Existing installation needs reconciliation; rerun did not modify it")
        return {"status": "unchanged", "kit_version": version, "needs_agent_review": True}
    agents = read(root, "AGENTS.md")
    if agents is not None and (BEGIN in agents or END in agents):
        raise Conflict("Unmanaged AEK marker already exists")
    aek = safe(root, ".aek")
    if aek.exists() and any(aek.iterdir()):
        raise Conflict("Unmanaged .aek directory already exists; review before adoption")
    state = {"schema_version": 1, "kit_version": version, "strategy": strategy,
             "source": Path(os.path.relpath(directory, root)).as_posix() if strategy == "linked" else None,
             "baselines": {name: digest(data) for name, data in files.items()},
             "agents_created": agents is None, "mode": mode}
    project = {"schema_version": 1, "project": {"summary": None, "architecture": None},
               "authority": {"execution": "task-scoped", "write_scope": [], "publication": False},
               "checks": [], "review": {"status": "pending", "evidence": []}}
    changes = {"AGENTS.md": (agents or b"") + BLOCK, ".aek/ENTRY.md": ENTRY,
               ".aek/project.json": encoded(project),
               ".aek/local.md": b"# Local adaptations\n\nRecord project decisions, scope, checks, and justified deviations here.\nUnresolved product decisions remain questions for the owner.\n",
               ".aek/state.json": encoded(state)}
    if strategy == "vendored":
        changes.update({".aek/runtime/" + name: data for name, data in files.items()})
    written = transact(root, changes)
    return {"status": "installed", "kit_version": version, "changed": written,
            "needs_agent_review": True, "note": "Installation is not project or behavioral validation"}

def audit(target):
    root = project_root(target)
    state = state_for(root)
    errors, local_changes = [], []
    try:
        marker_check(read(root, "AGENTS.md"))
    except Conflict as exc:
        errors.append(str(exc))
    if read(root, ".aek/ENTRY.md") != ENTRY:
        errors.append("Installed entrypoint is missing or changed")
    project = load_json(read(root, ".aek/project.json"), "project.json")
    authority = project.get("authority")
    if (type(project.get("schema_version")) is not int or project.get("schema_version") != 1 or not isinstance(authority, dict)
            or not isinstance(authority.get("publication"), bool)
            or not isinstance(authority.get("write_scope"), list)
            or not all(isinstance(x, str) for x in authority.get("write_scope", []))
            or not isinstance(project.get("checks"), list)):
        errors.append("Project adaptation schema is incomplete")
    if read(root, ".aek/local.md") is None:
        errors.append("Local adaptation file is missing")
    if state["strategy"] == "linked":
        try:
            version, files = bundle(source_path(root, state["source"]))
            if version != state["kit_version"]:
                errors.append("Linked KIT version differs from pin")
        except Conflict as exc:
            files = {}
            errors.append(str(exc))
    else:
        files = {}
        for name in state["baselines"]:
            value = read(root, ".aek/runtime/" + name)
            if value is not None:
                files[name] = value
    for name, expected in state["baselines"].items():
        if name not in files:
            errors.append("Runtime dependency missing: " + name)
        elif digest(files[name]) != expected:
            local_changes.append(name)
    if state["strategy"] == "linked" and set(files) != set(state["baselines"]):
        errors.append("Linked KIT file set differs from pin")
    if state["strategy"] == "vendored":
        runtime = safe(root, ".aek/runtime")
        if runtime.is_dir():
            extras = [p.name for p in runtime.iterdir() if p.name != "__pycache__" and p.name not in state["baselines"]]
            if extras:
                errors.append("Untracked runtime content: " + ", ".join(sorted(extras)))
    if local_changes:
        errors.append("Runtime differs from upstream baseline; review local adaptations")
    return {"static_validation": "fail" if errors else "pass", "errors": errors,
            "local_runtime_changes": local_changes, "kit_version": state["kit_version"],
            "needs_agent_review": True, "behavioral_validation": "not_performed",
            "product_runtime_validation": "not_performed",
            "review_required": ["instruction conflicts and applicability", "direct and indirect consumers",
                                "authority and routing", "actual checks and evidence", "risk-based independent review"]}

def upgrade(target, source=None):
    root = project_root(target)
    state = state_for(root)
    marker_check(read(root, "AGENTS.md"))
    if read(root, ".aek/ENTRY.md") != ENTRY:
        raise Conflict("Installed entrypoint changed; reconcile it before upgrading")
    if state["strategy"] == "linked":
        directory = source_path(root, source if source is not None else state["source"])
        if source is None and audit(root)["static_validation"] != "pass":
            raise Conflict("Linked source changed or unavailable; provide a separate pinned --source")
        version, files = bundle(directory)
        old_directory = source_path(root, state["source"])
        try:
            old_version, old_files = bundle(old_directory)
        except Conflict as exc:
            raise Conflict("Restore the previous linked source before a three-way upgrade") from exc
        incoming_hashes = {name: digest(data) for name, data in files.items()}
        current_hashes = {name: digest(data) for name, data in old_files.items()}
        if old_directory == directory and current_hashes != state["baselines"]:
            raise Conflict("Changed linked source must be restored; use a separate pinned new source")
        diverged = [name for name in set(state["baselines"]) | set(current_hashes)
                    if current_hashes.get(name) != state["baselines"].get(name)
                    and current_hashes.get(name) != incoming_hashes.get(name)]
        if diverged:
            raise Conflict("Linked local adaptations would be lost (nothing changed): " + ", ".join(sorted(diverged)))
        changes = {}
    else:
        version, files = bundle(source_path(root, source))
        changes, conflicts = {}, []
        for name in sorted(set(state["baselines"]) | set(files)):
            old = state["baselines"].get(name)
            current = read(root, ".aek/runtime/" + name)
            current_hash = digest(current) if current is not None else None
            new = files.get(name)
            new_hash = digest(new) if new is not None else None
            if current_hash == old:
                changes[".aek/runtime/" + name] = new
            elif new_hash == old or current_hash == new_hash:
                pass
            else:
                conflicts.append(name)
        if conflicts:
            raise Conflict("Three-way upgrade conflict (nothing changed): " + ", ".join(conflicts))
    next_state = dict(state, kit_version=version,
                      baselines={name: digest(data) for name, data in files.items()})
    if state["strategy"] == "linked":
        next_state["source"] = Path(os.path.relpath(directory, root)).as_posix()
    changes[".aek/state.json"] = encoded(next_state)
    written = transact(root, changes)
    return {"status": "upgraded" if written else "unchanged", "kit_version": version,
            "changed": written, "needs_agent_review": True}

def uninstall(target):
    root = project_root(target)
    state = state_for(root)
    agents = read(root, "AGENTS.md")
    marker_check(agents)
    changes = {}
    if state["strategy"] == "vendored":
        for name, expected in state["baselines"].items():
            current = read(root, ".aek/runtime/" + name)
            if current is not None and digest(current) != expected:
                raise Conflict("Runtime has local edits; preserve/reconcile before uninstalling")
            changes[".aek/runtime/" + name] = None
    if read(root, ".aek/ENTRY.md") != ENTRY:
        raise Conflict("Installed entrypoint changed; reconcile it before uninstalling")
    remaining = agents.replace(BLOCK, b"", 1)
    changes["AGENTS.md"] = None if state.get("agents_created") and remaining == b"" else remaining
    changes[".aek/ENTRY.md"] = None
    changes[".aek/state.json"] = None
    written = transact(root, changes)
    return {"status": "uninstalled", "changed": written,
            "preserved": [".aek/project.json", ".aek/local.md", "unmanaged files"]}

def check_evidence(path, required):
    value = load_json(Path(path).read_bytes(), "evidence")
    expected = json.loads(Path(required).read_text())
    if isinstance(expected, dict):
        expected = expected.get("required_ids")
    def ids(items):
        return (isinstance(items, list) and all(isinstance(x, str) and x for x in items)
                and len(set(items)) == len(items))
    if not ids(expected) or not expected:
        raise Conflict("Required manifest must contain distinct nonempty case IDs")
    for key in ("command", "environment", "revision"):
        if not isinstance(value.get(key), str) or not value[key].strip():
            raise Conflict("Evidence requires a nonempty " + key)
    tests = value.get("tests")
    if not isinstance(tests, dict):
        raise Conflict("Evidence requires test counts and IDs")
    names = ("total", "passed", "failed", "skipped")
    if any(type(tests.get(name)) is not int or tests[name] < 0 for name in names):
        raise Conflict("Test counts must be nonnegative integers")
    completed = tests.get("completed_ids")
    if not ids(completed) or set(completed) != set(expected):
        raise Conflict("Completed cases differ from mandatory IDs, or contain duplicates")
    for key in ("skipped_ids", "expected_failure_ids", "unexpected_success_ids"):
        if tests.get(key) != []:
            raise Conflict("Mandatory evidence cannot contain skips or expected/unexpected failures")
    if (tests["total"] != tests["passed"] + tests["failed"] + tests["skipped"]
            or tests["passed"] != len(completed) or tests["passed"] < 1
            or tests["failed"] != 0 or tests["skipped"] != 0 or value.get("result") != "passed"):
        raise Conflict("Evidence is not passing: require executed mandatory cases and zero failures/skips")
    return {"evidence_structure": "accepted", "executed": tests["passed"],
            "authenticity": "requires_independent_verification", "behavioral_validation": "not_performed"}

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    ins = sub.add_parser("install", help="Install instructions after agent discovery")
    ins.add_argument("target")
    ins.add_argument("--mode", choices=["initialize", "adopt"], default="adopt")
    ins.add_argument("--strategy", choices=["vendored", "linked"], default="vendored")
    ins.add_argument("--source", help="Core directory, relative to target")
    for command in ("audit", "upgrade", "uninstall"):
        item = sub.add_parser(command)
        item.add_argument("target")
        if command == "upgrade":
            item.add_argument("--source", help="New core directory, relative to target")
    item = sub.add_parser("check-evidence")
    item.add_argument("path")
    item.add_argument("--required", required=True, help="Independent mandatory case manifest")
    args = vars(parser.parse_args(argv))
    command = args.pop("command")
    try:
        result = globals()[command.replace("-", "_")](**args)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 2 if result.get("static_validation") == "fail" else 0
    except (Conflict, OSError, UnicodeError, ValueError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}))
        return 2

if __name__ == "__main__":
    sys.exit(main())
