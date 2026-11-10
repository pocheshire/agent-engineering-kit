#!/usr/bin/env python3
"""Offline AEK instruction installer; never executes project or remote code."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
from types import ModuleType

CORE = Path(__file__).resolve().parent
LEGACY_REQUIRED = {"LICENSE", "ENTRY.md", "CONTRACT.md", "MODES.md", "ROUTES.md", "VERSION", "aek.py"}
REQUIRED = LEGACY_REQUIRED | {"WORKFLOW.md", "workflow.py"}
BEGIN, END = b"<!-- AEK:BEGIN -->", b"<!-- AEK:END -->"
BLOCK = (b"\n<!-- AEK:BEGIN -->\n"
         b"For autonomous engineering work, read `.aek/ENTRY.md` before editing.\n"
         b"Local adaptations: `.aek/local.md` and `.aek/project.json`.\n"
         b"<!-- AEK:END -->\n")
ENTRY = b"# Installed AEK\n\nRead `state.json` to resolve the pinned runtime.\nFor vendored installs, read `runtime/ENTRY.md`.\nFor linked installs, resolve `source` relative to the project root and read its `ENTRY.md`.\nRun the kit's `aek.py audit PROJECT` to verify availability and integrity.\nIf unavailable or changed, report the dependency problem; do not silently substitute another kit.\n"

class Conflict(Exception):
    pass

def parse_version(value):
    """Strict SemVer precedence; build metadata never changes ordering."""
    if not isinstance(value, str):
        raise Conflict("Version must be a semantic version string")
    match = re.fullmatch(
        r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
        r"(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
        r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?", value)
    if not match:
        raise Conflict("Invalid semantic version: " + repr(value))
    prerelease = match.group(4)
    identifiers = []
    if prerelease is not None:
        for part in prerelease.split("."):
            numeric = part.isascii() and part.isdigit()
            if numeric and len(part) > 1 and part.startswith("0"):
                raise Conflict("Numeric prerelease identifiers cannot have leading zeroes")
            identifiers.append((0, int(part)) if numeric else (1, part))
    return (*map(int, match.group(1, 2, 3)), prerelease is None, tuple(identifiers))

def digest(data):
    return hashlib.sha256(data).hexdigest()

def required_for(version):
    return REQUIRED if parse_version(version)[:3] >= (0, 2, 0) else LEGACY_REQUIRED

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
        if path.name == "__pycache__" and path.is_dir() and not path.is_symlink():
            continue
        if path.is_symlink():
            raise Conflict("KIT source contains a symlink")
        if not path.is_file() or not (path.suffix in {".md", ".py"} or path.name in {"VERSION", "LICENSE"}):
            raise Conflict("KIT source contains an unsupported resource: " + path.name)
        files[path.name] = path.read_bytes()
    if "VERSION" not in files:
        raise Conflict("KIT source is incomplete")
    version = files["VERSION"].decode().strip()
    if not required_for(version).issubset(files):
        raise Conflict("KIT source is incomplete")
    return version, files

def validate_skill_bundle(directory):
    """Validate AEK's shipped metadata and both standalone license notices."""
    version, files = bundle(directory / "core")
    skill = (directory / "SKILL.md").read_text(encoding="utf-8")
    header = skill.split("---", 2)
    if len(header) != 3 or header[0].strip():
        raise Conflict("Skill frontmatter is missing")
    if re.findall(r"(?m)^name: ([^\n]+)$", header[1]) != ["agent-engineering-kit"]:
        raise Conflict("Skill name differs from package identity")
    if len(re.findall(r"(?m)^description: [^\n]+$", header[1])) != 1:
        raise Conflict("Skill description is missing")
    metadata = re.findall(r"(?m)^metadata:\s*\n((?:[ \t]+[^\n]*\n?)*)", header[1])
    declared = re.findall(r"(?m)^  version: [\"']?([^\s\"']+)[\"']?\s*$", metadata[0] if len(metadata) == 1 else "")
    if declared != [version]:
        raise Conflict("Skill metadata version differs from core VERSION")
    if (directory / "LICENSE").read_bytes() != files["LICENSE"]:
        raise Conflict("Standalone skill and core license notices differ")
    return version, files

def state_for(root):
    raw = read(root, ".aek/state.json")
    if raw is None:
        raise Conflict("AEK is not installed")
    state = load_json(raw, "state.json")
    if (type(state.get("schema_version")) is not int or state.get("schema_version") != 1 or not isinstance(state.get("strategy"), str) or state.get("strategy") not in {"vendored", "linked"}
            or not isinstance(state.get("kit_version"), str)):
        raise Conflict("Unsupported installation state; use a compatible KIT version")
    parse_version(state["kit_version"])
    hashes = state.get("baselines")
    if not isinstance(hashes, dict) or not required_for(state["kit_version"]).issubset(hashes):
        raise Conflict("Invalid installation baselines")
    for name, value in hashes.items():
        if (not name or Path(name).name != name or "/" in name or "\\" in name
                or not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value)):
            raise Conflict("Invalid managed file baseline")
    if state["strategy"] == "linked":
        if not isinstance(state.get("source"), str) or Path(state["source"]).is_absolute():
            raise Conflict("Invalid linked source")
    return state

def project_for(root):
    project = load_json(read(root, ".aek/project.json"), "project.json")
    authority = project.get("authority")
    if (type(project.get("schema_version")) is not int or project["schema_version"] != 1
            or not isinstance(authority, dict) or not isinstance(authority.get("publication"), bool)
            or not isinstance(authority.get("write_scope"), list)
            or not all(isinstance(x, str) for x in authority["write_scope"])
            or not isinstance(project.get("checks"), list)):
        raise Conflict("Unsupported or incomplete project adaptation schema")
    if read(root, ".aek/local.md") is None:
        raise Conflict("Local adaptation file is missing")
    return project

def atomic_write(path, data, mode=None):
    """Replace a file atomically, preserving selected mode and cleaning failed temps."""
    temporary_name = None
    try:
        with tempfile.NamedTemporaryFile(dir=str(path.parent), delete=False) as temporary:
            temporary_name = temporary.name
            temporary.write(data)
        if mode is not None:
            os.chmod(temporary_name, mode)
        os.replace(temporary_name, path)
    finally:
        if temporary_name is not None and os.path.exists(temporary_name):
            os.unlink(temporary_name)

def transact(root, changes):
    """Preflight every destination; roll back file contents and ordinary POSIX modes."""
    before = {name: read(root, name) for name in changes}
    modes = {}
    if os.name == "posix":
        for name, data in before.items():
            if data is not None:
                path = safe(root, name)
                file_stat = path.lstat()
                if stat.S_ISREG(file_stat.st_mode):
                    # Preserve rwx permissions, but never copy setuid/setgid/sticky bits.
                    modes[name] = stat.S_IMODE(file_stat.st_mode) & 0o777
    written = []
    created_dirs = []
    try:
        for name, data in changes.items():
            path = safe(root, name)
            if data == before[name]:
                continue
            if data is None:
                if path.exists():
                    path.unlink()
            else:
                missing = []
                parent = path.parent
                while not parent.exists():
                    missing.append(parent)
                    parent = parent.parent
                path.parent.mkdir(parents=True, exist_ok=True)
                created_dirs.extend(reversed(missing))
                atomic_write(path, data, modes.get(name))
            written.append(name)
    except OSError:
        for name in reversed(written):
            path = safe(root, name)
            if before[name] is None:
                path.unlink(missing_ok=True)
            else:
                atomic_write(path, before[name], modes.get(name))
        for directory in reversed(created_dirs):
            try:
                directory.rmdir()
            except OSError:
                pass
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
    try:
        project_for(root)
    except Conflict as exc:
        errors.append(str(exc))
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
    if "VERSION" in files:
        try:
            actual_version = files["VERSION"].decode().strip()
            parse_version(actual_version)
            if actual_version != state["kit_version"]:
                errors.append("Runtime VERSION differs from installed pin")
        except (Conflict, UnicodeError) as exc:
            errors.append("Invalid runtime VERSION: " + str(exc))
    return {"static_validation": "fail" if errors else "pass", "errors": errors,
            "local_runtime_changes": local_changes, "kit_version": state["kit_version"],
            "needs_agent_review": True, "behavioral_validation": "not_performed",
            "product_runtime_validation": "not_performed",
            "review_required": ["instruction conflicts and applicability", "direct and indirect consumers",
                                "authority and routing", "actual checks and evidence", "risk-based independent review"]}

def upgrade(target, source=None, allow_major=False):
    root = project_root(target)
    state = state_for(root)
    marker_check(read(root, "AGENTS.md"))
    if read(root, ".aek/ENTRY.md") != ENTRY:
        raise Conflict("Installed entrypoint changed; reconcile it before upgrading")
    project_for(root)
    old_directory = source_path(root, state["source"]) if state["strategy"] == "linked" else safe(root, ".aek/runtime")
    installed_version = read(old_directory, "VERSION")
    if (installed_version is None or digest(installed_version) != state["baselines"]["VERSION"]
            or installed_version.decode().strip() != state["kit_version"]):
        raise Conflict("Installed version identity is unavailable or inconsistent; restore the exact pin first")
    directory = source_path(root, source if source is not None else state["source"]) if state["strategy"] == "linked" else source_path(root, source)
    version, files = bundle(directory)
    old_order, new_order = parse_version(state["kit_version"]), parse_version(version)
    incoming_hashes = {name: digest(data) for name, data in files.items()}
    if new_order < old_order:
        raise Conflict("Downgrade is not an upgrade; review a separate rollback plan")
    if new_order == old_order and incoming_hashes != state["baselines"]:
        raise Conflict("Same version precedence has different content; publish a newer version")
    if new_order[0] != old_order[0] and not allow_major:
        raise Conflict("Major upgrade requires a reviewed migration and explicit --allow-major")
    if state["strategy"] == "linked":
        if source is None and audit(root)["static_validation"] != "pass":
            raise Conflict("Linked source changed or unavailable; provide a separate pinned --source")
        try:
            old_version, old_files = bundle(old_directory)
        except Conflict as exc:
            raise Conflict("Restore the previous linked source before a three-way upgrade") from exc
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

def restore(target, source, replace=None, allow_linked_write=False):
    """Restore an exact pin, never infer that a local edit is corruption."""
    if source is None:
        raise Conflict("Recovery requires an explicit trusted source")
    root = project_root(target)
    state = state_for(root)
    marker_check(read(root, "AGENTS.md"))
    if read(root, ".aek/ENTRY.md") != ENTRY:
        raise Conflict("Installed entrypoint changed; reconcile it before restoring runtime")
    project_for(root)
    version, files = bundle(source_path(root, source))
    if (version != state["kit_version"]
            or {name: digest(data) for name, data in files.items()} != state["baselines"]):
        raise Conflict("Recovery source does not match the pinned version and complete hash manifest")
    selected = set(replace or [])
    if not selected.issubset(state["baselines"]):
        raise Conflict("Replacement names must be pinned runtime filenames")
    linked = state["strategy"] == "linked"
    if linked and not allow_linked_write:
        raise Conflict("Restoring a linked dependency requires explicit --allow-linked-write within authorized scope")
    destination = source_path(root, state["source"]) if linked else safe(root, ".aek/runtime")
    if destination.exists():
        extras = [p.name for p in destination.iterdir() if p.name != "__pycache__" and p.name not in files]
        if extras:
            raise Conflict("Untracked runtime content must be reviewed before recovery: " + ", ".join(sorted(extras)))
    changes = {}
    for name, data in files.items():
        current = read(destination, name)
        if current is None:
            changes[name] = data
        elif digest(current) != state["baselines"][name]:
            if name not in selected:
                raise Conflict("Existing divergence may be a local adaptation; explicit --replace required: " + name)
            changes[name] = data
    written = transact(destination, changes)
    report = audit(root)
    return {"status": "restored" if written else "unchanged", "kit_version": version,
            "changed": written, "destination": "linked_source" if linked else ".aek/runtime",
            "static_validation": report["static_validation"], "errors": report["errors"],
            "needs_agent_review": True, "note": "Pin and project adaptations were not changed"}

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
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] == "work":
        # Resolve our own reviewed sibling, never a CWD/PYTHONPATH lookalike.
        try:
            source = CORE / "workflow.py"
            module = ModuleType("aek_workflow")
            module.__file__ = str(source)
            # Compile the verified sibling source bytes directly; do not allow a
            # stale or unchecked __pycache__ entry to select different code.
            exec(compile(source.read_bytes(), str(source), "exec"), module.__dict__)
            return module.main(argv[1:])
        except (OSError, ImportError, SyntaxError) as exc:
            print(json.dumps({"status": "error", "error": "Workflow runtime unavailable: " + str(exc)}))
            return 2
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("work", help="Offline task, repair, delegation and stability records; work --help")
    ins = sub.add_parser("install", help="Install instructions after agent discovery")
    ins.add_argument("target")
    ins.add_argument("--mode", choices=["initialize", "adopt"], default="adopt")
    ins.add_argument("--strategy", choices=["vendored", "linked"], default="vendored")
    ins.add_argument("--source", help="Core directory relative to target; ../ may point outside it (read access required)")
    for command in ("audit", "upgrade", "uninstall"):
        item = sub.add_parser(command)
        item.add_argument("target")
        if command == "upgrade":
            item.add_argument("--source", help="New core directory, relative to target")
            item.add_argument("--allow-major", action="store_true", help="Only after reviewing an authorized migration")
    item = sub.add_parser("restore", help="Restore unavailable runtime from an exact trusted pin")
    item.add_argument("target")
    item.add_argument("--source", required=True, help="Trusted exact-pinned core, relative to target")
    item.add_argument("--replace", action="append", default=[], help="Explicitly replace a confirmed damaged runtime filename")
    item.add_argument("--allow-linked-write", action="store_true", help="Only when writing the original linked source is authorized")
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
