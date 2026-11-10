#!/usr/bin/env python3
"""Offline static, privacy and mandatory test gate. Does not claim behavioral QA."""
import importlib.util
import json
import re
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tests"))
sys.path.insert(0, str(ROOT / "scripts"))
import distribution


def static_checks():
    errors = []
    version = (ROOT / "VERSION").read_text().strip()
    core = ROOT / "skills" / "agent-engineering-kit" / "core"
    if (core / "VERSION").read_text().strip() != version:
        errors.append("Runtime version mismatch")
    manifests = ["plugin.json", ".codex-plugin/plugin.json", ".claude-plugin/plugin.json"]
    for name in manifests:
        data = json.loads((ROOT / name).read_text())
        if data.get("version") != version or data.get("name") != "agent-engineering-kit":
            errors.append("Manifest identity/version mismatch: " + name)
    skill = ROOT / "skills" / "agent-engineering-kit"
    spec = importlib.util.spec_from_file_location("aek_package_identity", core / "aek.py")
    identity = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(identity)
    try:
        packaged_version, unused = identity.validate_skill_bundle(skill)
        if packaged_version != version:
            errors.append("Skill/core release version mismatch")
    except (identity.Conflict, OSError, UnicodeError) as exc:
        errors.append("Skill bundle identity: " + str(exc))
    for notice in (skill / "LICENSE", core / "LICENSE"):
        if notice.read_bytes() != (ROOT / "LICENSE").read_bytes():
            errors.append("Standalone bundle license notice mismatch")
    for marketplace in (".agents/plugins/marketplace.json", ".claude-plugin/marketplace.json"):
        data = json.loads((ROOT / marketplace).read_text())
        entries = data.get("plugins", [])
        if data.get("name") != "agent-engineering-kit" or len(entries) != 1 or entries[0].get("name") != "agent-engineering-kit":
            errors.append("Invalid marketplace identity: " + marketplace)
        elif entries[0].get("source") not in ("./", {"source": "local", "path": "./"}):
            errors.append("Marketplace source must be this package root: " + marketplace)
        if len(entries) == 1 and ("version" in entries[0] or marketplace.startswith(".claude-plugin/")):
            if entries[0].get("version") != version:
                errors.append("Marketplace version mismatch: " + marketplace)
    required = ["README.md", "LICENSE", "START_HERE.md", "AGENTS.md", "CONTRIBUTING.md", "SECURITY.md", "CHANGELOG.md", "docs/platforms.md", "docs/installation.md", "docs/validation.md"]
    for name in required:
        if not (ROOT / name).is_file():
            errors.append("Missing " + name)
    # Scan the release inventory and eligible untracked files. The inventory
    # itself includes forbidden tracked paths so they cannot disappear silently.
    patterns = {
        "private machine path": re.compile(r"/(?:Users|home)/[A-Za-z0-9_.-]+/"),
        "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        "GitHub token": re.compile(r"(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{50,})"),
        "provider secret": re.compile(r"sk-[A-Za-z0-9_-]{30,}"),
        "private source reference": re.compile(r"CampIn|AGENTS-WORKFLOW-03|iCloud~md~obsidian"),
    }
    try:
        files = distribution.inventory(ROOT)
    except RuntimeError as exc:
        errors.append("Publication inventory: " + str(exc))
        return errors
    for name in files.release_files:
        if distribution.is_reserved(name):
            errors.append("Reserved publication path: " + name)
    for name in files.scan_files:
        path = ROOT / name
        if distribution.path_is_symlink(ROOT, name, files.symlink_files):
            errors.append("Publication symlink: " + name)
            continue
        if not path.is_file():
            if name in files.release_files:
                errors.append("Missing publication file: " + name)
            continue
        try:
            raw = path.read_bytes()
            if b"\x00" in raw or path.suffix in {".pyc", ".pyo"}:
                errors.append("Review binary publication artifact: " + name)
                continue
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            errors.append("Review binary publication artifact: " + name)
            continue
        except OSError as exc:
            errors.append("Cannot read publication file " + name + ": " + str(exc))
            continue
        for label, pattern in patterns.items():
            # The scanner's own detection patterns are not leaked source material.
            if name == "scripts/validate.py":
                continue
            if pattern.search(text):
                errors.append(label + " in " + name)
        if path.suffix == ".md":
            for destination in re.findall(r"\]\(([^)]+)\)", text):
                if "://" in destination or destination.startswith("#"):
                    continue
                dest = destination.split("#", 1)[0]
                if dest and not (path.parent / dest).exists():
                    errors.append("Broken relative link " + name + ": " + dest)
    return errors


def flatten(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from flatten(item)
        else:
            yield item


class StrictResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.started_ids = []
        self.successful_ids = []
    def startTest(self, test):
        self.started_ids.append(test.id())
        super().startTest(test)
    def addSuccess(self, test):
        self.successful_ids.append(test.id())
        super().addSuccess(test)


def result_ok(result, mandatory):
    return (result.wasSuccessful() and result.testsRun > 0 and not result.skipped and not result.expectedFailures
            and len(set(mandatory)) == len(mandatory)
            and len(result.started_ids) == len(mandatory) and set(result.started_ids) == set(mandatory)
            and len(result.successful_ids) == len(mandatory) and set(result.successful_ids) == set(mandatory))


def run():
    errors = static_checks()
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), pattern="test_*.py")
    discovered = [t.id() for t in flatten(suite)]
    mandatory = json.loads((ROOT / "tests" / "required-tests.json").read_text())
    if not mandatory or len(set(mandatory)) != len(mandatory):
        errors.append("Mandatory manifest is empty or contains duplicate IDs")
    if len(set(discovered)) != len(discovered) or set(discovered) != set(mandatory):
        errors.append("Discovered IDs differ from checked-in mandatory manifest: " + repr(sorted(set(discovered) ^ set(mandatory))))
    if errors:
        print(json.dumps({"static_validation": "failed", "errors": errors}, indent=2))
        return 1
    result = unittest.TextTestRunner(verbosity=2, resultclass=StrictResult).run(suite)
    passed = result_ok(result, mandatory)
    print(json.dumps({"static_validation": "passed", "installation_tests": "passed" if passed else "failed",
                      "tests_run": result.testsRun, "skipped": len(result.skipped),
                      "behavioral_validation": "separate", "product_runtime": "separate", "marketplace_publication": "separate"}, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(run())
