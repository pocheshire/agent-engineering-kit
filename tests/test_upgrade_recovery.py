"""Pinned updates and explicit recovery, using isolated synthetic projects."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "skills/agent-engineering-kit/core"
SCRIPT = ROOT / "skills/agent-engineering-kit/core/aek.py"
spec = importlib.util.spec_from_file_location("recovery_aek", SCRIPT)
aek = importlib.util.module_from_spec(spec)
spec.loader.exec_module(aek)


class VersionTests(unittest.TestCase):
    def test_semver_precedence_numeric_prerelease_and_build_metadata(self):
        ordered = ["0.9.9", "1.0.0-alpha", "1.0.0-alpha.1", "1.0.0-alpha.beta",
                   "1.0.0-beta", "1.0.0-beta.2", "1.0.0-beta.11", "1.0.0-rc.1",
                   "1.0.0", "1.0.1", "1.1.0", "2.0.0"]
        for left, right in zip(ordered, ordered[1:]):
            with self.subTest(left=left, right=right):
                self.assertLess(aek.parse_version(left), aek.parse_version(right))
        self.assertEqual(aek.parse_version("1.0.0+build.7"), aek.parse_version("1.0.0+other.8"))
        self.assertEqual(aek.parse_version("1.0.0+build.7"), aek.parse_version("1.0.0"))
        self.assertEqual(aek.parse_version("1.0.0-rc.2+build.7"), aek.parse_version("1.0.0-rc.2"))
        aek.parse_version("1.0.0-alpha-1+build-2.003")

    def test_semver_rejects_invalid_and_non_ascii_versions(self):
        invalid = [None, True, 1, {}, [], "", "v1.0.0", "1.0", "01.0.0", "1.01.0",
                   "1.0.01", "1.0.0-01", "1.0.0-alpha..1", "1.0.0-", "1.0.0+",
                   "1.0.0+build..2", "١.0.0", "1.0.0-١", " 1.0.0", "1.0.0\n"]
        for version in invalid:
            with self.subTest(version=version), self.assertRaises(aek.Conflict):
                aek.parse_version(version)


class UpgradeRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.project = self.root / "project"
        self.project.mkdir()
        self.source = self.root / "kit-1"
        self.source.mkdir()
        required = aek.REQUIRED
        for name in required:
            (self.source / name).write_text("1.0.0\n" if name == "VERSION" else "original " + name + "\n")
        self.sequence = 0

    def install(self, strategy="vendored"):
        return aek.install(self.project, source="../kit-1", strategy=strategy)

    def incoming(self, version="1.1.0"):
        self.sequence += 1
        source = self.root / ("incoming-" + str(self.sequence))
        shutil.copytree(self.source, source)
        (source / "VERSION").write_text(version + "\n")
        return source

    def snapshot(self, root=None):
        root = root or self.project
        return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*") if p.is_file()}

    def relative(self, source):
        return "../" + source.name

    def conflict_without_writes(self, action, root=None):
        before = self.snapshot(root)
        with self.assertRaises(aek.Conflict):
            action()
        self.assertEqual(before, self.snapshot(root))

    def test_cli_upgrade_and_restore_reject_unsupported_resources_before_writes(self):
        def cli(*args):
            return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                                  capture_output=True, text=True)

        installed = cli("install", self.project, "--source", "../kit-1")
        self.assertEqual(installed.returncode, 0, installed.stdout + installed.stderr)
        incoming = self.incoming("1.1.0")
        (incoming / "schema.json").write_text("{}\n")
        before_upgrade = self.snapshot()
        result = cli("upgrade", self.project, "--source", self.relative(incoming))
        self.assertEqual(result.returncode, 2)
        self.assertIn("unsupported resource", json.loads(result.stdout)["error"])
        self.assertEqual(before_upgrade, self.snapshot())

        (self.source / "nested").mkdir()
        (self.source / "nested/schema.json").write_text("{}\n")
        before_restore = self.snapshot()
        result = cli("restore", self.project, "--source", "../kit-1")
        self.assertEqual(result.returncode, 2)
        self.assertIn("unsupported resource", json.loads(result.stdout)["error"])
        self.assertEqual(before_restore, self.snapshot())

    def test_candidate_upgrade_from_stable_020_pin(self):
        old = self.root / "stable-020"
        shutil.copytree(CORE, old, ignore=shutil.ignore_patterns("__pycache__"))
        (old / "VERSION").write_text("0.2.0\n")
        candidate = self.root / "candidate"
        shutil.copytree(CORE, candidate, ignore=shutil.ignore_patterns("__pycache__"))
        version = (candidate / "VERSION").read_text().strip()
        old_before = self.snapshot(old)
        candidate_before = self.snapshot(candidate)
        prefix = b"# Original\r\nKeep this rule."
        suffix = "\r\nRésumé\r\nOwner suffix".encode()
        for strategy in ("vendored", "linked"):
            with self.subTest(strategy=strategy):
                project = self.root / strategy
                project.mkdir()
                agents = project / "AGENTS.md"
                agents.write_bytes(prefix)
                agents.chmod(0o640)
                installed = aek.install(project, source=self.relative(old), strategy=strategy)
                self.assertEqual(installed["kit_version"], "0.2.0")
                self.assertEqual(agents.read_bytes(), prefix + aek.LEGACY_BLOCK)
                with agents.open("ab") as handle:
                    handle.write(suffix)
                adapted_before = {name: (project / ".aek" / name).read_bytes()
                                  for name in ("project.json", "local.md")}

                upgraded = aek.upgrade(project, source=self.relative(candidate))
                self.assertEqual(upgraded["kit_version"], version)
                self.assertIn("AGENTS.md", upgraded["changed"])
                self.assertEqual(agents.read_bytes(), prefix + aek.BLOCK + suffix)
                if os.name == "posix":
                    self.assertEqual(stat.S_IMODE(agents.stat().st_mode), 0o640)
                self.assertEqual(aek.audit(project)["static_validation"], "pass")
                self.assertEqual(adapted_before, {name: (project / ".aek" / name).read_bytes()
                                                  for name in adapted_before})

                before_repeat = self.snapshot(project)
                with patch.object(aek, "atomic_write", wraps=aek.atomic_write) as write:
                    repeated = aek.upgrade(project, source=self.relative(candidate))
                self.assertEqual(repeated["status"], "unchanged")
                self.assertEqual(repeated["changed"], [])
                write.assert_not_called()
                self.assertEqual(before_repeat, self.snapshot(project))
                aek.uninstall(project)
                self.assertEqual(agents.read_bytes(), prefix + suffix)
                if os.name == "posix":
                    self.assertEqual(stat.S_IMODE(agents.stat().st_mode), 0o640)
        self.assertEqual(self.snapshot(old), old_before)
        self.assertEqual(self.snapshot(candidate), candidate_before)

    def test_upgrade_rejects_edited_or_ambiguous_legacy_marker(self):
        (self.source / "VERSION").write_text("0.2.0\n")
        self.install()
        source = self.incoming("0.3.0-rc.1")
        agents = self.project / "AGENTS.md"
        for damaged in (aek.LEGACY_BLOCK.replace(b"before editing", b"before review"),
                        aek.LEGACY_BLOCK * 2, aek.LEGACY_BLOCK + aek.BLOCK, aek.BLOCK,
                        aek.LEGACY_BLOCK + aek.BEGIN):
            with self.subTest(damaged=damaged):
                agents.write_bytes(damaged)
                self.assertEqual(aek.audit(self.project)["static_validation"], "fail")
                before = self.snapshot()
                with patch.object(aek, "transact", wraps=aek.transact) as transaction:
                    with self.assertRaisesRegex(aek.Conflict, "AGENTS.md AEK block"):
                        aek.upgrade(self.project, source=self.relative(source))
                transaction.assert_not_called()
                self.assertEqual(self.snapshot(), before)

    def test_marker_migration_rolls_back_on_state_write_failure(self):
        (self.source / "VERSION").write_text("0.2.0\n")
        incoming = self.incoming("0.3.0-rc.1")
        (incoming / "CONTRACT.md").write_text("new workflow\n")
        replace = os.replace
        for strategy in ("vendored", "linked"):
            with self.subTest(strategy=strategy):
                project = self.root / strategy
                project.mkdir()
                agents = project / "AGENTS.md"
                original = b"# Owner\r\n"
                agents.write_bytes(original)
                agents.chmod(0o640)
                aek.install(project, source="../kit-1", strategy=strategy)
                before = self.snapshot(self.root)
                seen_agents = []

                def fail_state_replace(source, destination):
                    if destination == project / ".aek/state.json":
                        seen_agents.append(agents.read_bytes())
                        raise OSError("simulated state replace failure")
                    return replace(source, destination)

                with patch.object(aek.os, "replace", side_effect=fail_state_replace):
                    with self.assertRaisesRegex(OSError, "simulated state replace failure"):
                        aek.upgrade(project, source=self.relative(incoming))
                self.assertEqual(seen_agents, [original + aek.block_for("0.3.0-rc.1")])
                self.assertEqual(self.snapshot(self.root), before)
                if os.name == "posix":
                    self.assertEqual(stat.S_IMODE(agents.stat().st_mode), 0o640)
                self.assertEqual(aek.audit(project)["static_validation"], "pass")

    def test_03_pin_restore_upgrade_and_uninstall_preserve_owner_rules(self):
        for version in ("0.3.0-rc.1", "0.3.1"):
            (self.source / "VERSION").write_text(version + "\n")
            incoming = self.incoming("0.4.0-rc.1")
            for strategy in ("vendored", "linked"):
                with self.subTest(version=version, strategy=strategy):
                    project = self.root / (version + strategy)
                    project.mkdir()
                    agents = project / "AGENTS.md"
                    prefix = b"# Owner\r\nAll edits need my approval.\r\n"
                    suffix = "\nOwner suffix: Résumé\n".encode()
                    agents.write_bytes(prefix)
                    agents.chmod(0o640)
                    aek.install(project, source="../kit-1", strategy=strategy)
                    agents.write_bytes(agents.read_bytes() + suffix)
                    self.assertEqual(agents.read_bytes(), prefix + aek.SDD_BLOCK + suffix)
                    self.assertEqual(aek.audit(project)["static_validation"], "pass")
                    adaptations = {name: (project / ".aek" / name).read_bytes()
                                   for name in ("project.json", "local.md")}
                    if strategy == "vendored":
                        state = (project / ".aek/state.json").read_bytes()
                        (project / ".aek/runtime/ENTRY.md").unlink()
                        aek.restore(project, source="../kit-1")
                        self.assertEqual((project / ".aek/state.json").read_bytes(), state)
                        self.assertEqual(agents.read_bytes(), prefix + aek.SDD_BLOCK + suffix)
                        self.assertEqual(aek.audit(project)["static_validation"], "pass")

                    result = aek.upgrade(project, source=self.relative(incoming))
                    self.assertIn("AGENTS.md", result["changed"])
                    self.assertEqual(agents.read_bytes(), prefix + aek.BLOCK + suffix)
                    self.assertEqual(aek.audit(project)["static_validation"], "pass")
                    self.assertEqual(adaptations, {name: (project / ".aek" / name).read_bytes()
                                                  for name in adaptations})
                    before = self.snapshot(project)
                    with patch.object(aek, "atomic_write", wraps=aek.atomic_write) as write:
                        repeated = aek.upgrade(project, source=self.relative(incoming))
                    self.assertEqual(repeated["status"], "unchanged")
                    write.assert_not_called()
                    self.assertEqual(before, self.snapshot(project))
                    aek.uninstall(project)
                    self.assertEqual(agents.read_bytes(), prefix + suffix)
                    if os.name == "posix":
                        self.assertEqual(stat.S_IMODE(agents.stat().st_mode), 0o640)

    def test_03_entry_edits_and_ambiguity_block_upgrade_without_writes(self):
        (self.source / "VERSION").write_text("0.3.1\n")
        self.install()
        incoming = self.incoming("0.4.0-rc.1")
        agents = self.project / "AGENTS.md"
        for damaged in (aek.SDD_BLOCK.replace(b"before planning", b"before coding"),
                        aek.SDD_BLOCK * 2, aek.SDD_BLOCK + aek.BLOCK,
                        aek.BLOCK, aek.SDD_BLOCK + aek.BEGIN):
            with self.subTest(damaged=damaged):
                agents.write_bytes(damaged)
                self.assertEqual(aek.audit(self.project)["static_validation"], "fail")
                before = self.snapshot()
                with patch.object(aek, "transact", wraps=aek.transact) as transaction:
                    with self.assertRaisesRegex(aek.Conflict, "AGENTS.md AEK block"):
                        aek.upgrade(self.project, source=self.relative(incoming))
                transaction.assert_not_called()
                self.assertEqual(before, self.snapshot())

    def test_03_entry_migration_rolls_back_with_runtime_and_pin(self):
        (self.source / "VERSION").write_text("0.3.1\n")
        incoming = self.incoming("0.4.0-rc.1")
        (incoming / "CONTRACT.md").write_text("route-specific workflow\n")
        replace = os.replace
        for strategy in ("vendored", "linked"):
            with self.subTest(strategy=strategy):
                project = self.root / strategy
                project.mkdir()
                agents = project / "AGENTS.md"
                agents.write_bytes(b"# Owner\r\n")
                agents.chmod(0o640)
                aek.install(project, source="../kit-1", strategy=strategy)
                before = self.snapshot(self.root)
                seen = []

                def fail_state_replace(source, destination):
                    if destination == project / ".aek/state.json":
                        seen.append(agents.read_bytes())
                        raise OSError("simulated state replace failure")
                    return replace(source, destination)

                with patch.object(aek.os, "replace", side_effect=fail_state_replace):
                    with self.assertRaisesRegex(OSError, "simulated state replace failure"):
                        aek.upgrade(project, source=self.relative(incoming))
                self.assertEqual(seen, [b"# Owner\r\n" + aek.BLOCK])
                self.assertEqual(before, self.snapshot(self.root))
                self.assertEqual(aek.audit(project)["static_validation"], "pass")
                if os.name == "posix":
                    self.assertEqual(stat.S_IMODE(agents.stat().st_mode), 0o640)

    def test_upgrade_rejects_same_version_changed_content_without_writes(self):
        self.install()
        source = self.incoming("1.0.0")
        (source / "CONTRACT.md").write_text("changed under the same identity")
        self.conflict_without_writes(lambda: aek.upgrade(self.project, source=self.relative(source)))

    def test_upgrade_rejects_downgrade_and_stable_to_prerelease_without_writes(self):
        self.install()
        for version in ["0.9.9", "1.0.0-rc.1"]:
            source = self.incoming(version)
            with self.subTest(version=version):
                self.conflict_without_writes(lambda: aek.upgrade(self.project, source=self.relative(source)))

    def test_upgrade_rejects_same_precedence_build_change_without_writes(self):
        self.install()
        source = self.incoming("1.0.0+build.2")
        self.conflict_without_writes(lambda: aek.upgrade(self.project, source=self.relative(source)))

    def test_upgrade_same_exact_source_is_unchanged(self):
        self.install()
        before = self.snapshot()
        result = aek.upgrade(self.project, source="../kit-1")
        self.assertEqual(result["status"], "unchanged")
        self.assertEqual(before, self.snapshot())

    def test_upgrade_major_requires_explicit_migration_choice(self):
        self.install()
        source = self.incoming("2.0.0")
        self.conflict_without_writes(lambda: aek.upgrade(self.project, source=self.relative(source)))
        result = aek.upgrade(self.project, source=self.relative(source), allow_major=True)
        self.assertEqual(result["kit_version"], "2.0.0")
        self.assertEqual(aek.audit(self.project)["static_validation"], "pass")

    def test_upgrade_unknown_project_schema_is_no_write(self):
        self.install()
        path = self.project / ".aek/project.json"
        project = json.loads(path.read_text())
        project["schema_version"] = 99
        path.write_text(json.dumps(project))
        source = self.incoming()
        self.conflict_without_writes(lambda: aek.upgrade(self.project, source=self.relative(source)))

    def test_upgrade_missing_local_adaptations_is_no_write(self):
        self.install()
        (self.project / ".aek/local.md").unlink()
        source = self.incoming()
        self.conflict_without_writes(lambda: aek.upgrade(self.project, source=self.relative(source)))

    def test_upgrade_preserves_project_local_and_original_instructions(self):
        (self.project / "AGENTS.md").write_bytes(b"# Original\r\nKeep this rule.\r\n")
        self.install()
        (self.project / ".aek/local.md").write_bytes(b"An owner decision.\r\n")
        project = self.project / ".aek/project.json"
        data = json.loads(project.read_text())
        data["checks"] = [{"command": "python3 -m unittest", "scope": "project"}]
        project.write_text(json.dumps(data, indent=4) + "\n")
        names = ["AGENTS.md", ".aek/project.json", ".aek/local.md"]
        before = {name: (self.project / name).read_bytes() for name in names}
        source = self.incoming()
        aek.upgrade(self.project, source=self.relative(source))
        self.assertEqual(before, {name: (self.project / name).read_bytes() for name in names})

    def test_audit_rejects_invalid_or_mismatched_pinned_version(self):
        self.install()
        path = self.project / ".aek/state.json"
        original = json.loads(path.read_text())
        for version in ["not-semver", "01.0.0", "9.0.0"]:
            path.write_text(json.dumps(dict(original, kit_version=version)))
            before = self.snapshot()
            with self.subTest(version=version):
                try:
                    report = aek.audit(self.project)
                except aek.Conflict:
                    pass
                else:
                    self.assertEqual(report["static_validation"], "fail")
                self.assertEqual(before, self.snapshot())

    def test_restore_missing_vendored_file_preserves_all_other_project_bytes(self):
        self.install()
        for name in ["aek.py", "ENTRY.md", "VERSION", "CONTRACT.md"]:
            with self.subTest(name=name):
                relative = ".aek/runtime/" + name
                runtime = self.project / relative
                expected = runtime.read_bytes()
                runtime.unlink()
                before = self.snapshot()
                result = aek.restore(self.project, source="../kit-1")
                self.assertEqual(result["static_validation"], "pass")
                self.assertEqual(runtime.read_bytes(), expected)
                self.assertEqual(before, {key: value for key, value in self.snapshot().items() if key != relative})

    def test_restore_existing_divergence_requires_explicit_replacement(self):
        self.install()
        runtime = self.project / ".aek/runtime/aek.py"
        runtime.write_text("A legitimate local adaptation or corruption; do not guess.")
        self.conflict_without_writes(lambda: aek.restore(self.project, source="../kit-1"))
        before = self.snapshot()
        result = aek.restore(self.project, source="../kit-1", replace=["aek.py"])
        self.assertEqual(result["static_validation"], "pass")
        self.assertEqual(runtime.read_bytes(), (self.source / "aek.py").read_bytes())
        self.assertEqual({k: v for k, v in before.items() if k != ".aek/runtime/aek.py"},
                         {k: v for k, v in self.snapshot().items() if k != ".aek/runtime/aek.py"})

    def test_restore_unselected_divergence_prevents_all_writes(self):
        self.install()
        (self.project / ".aek/runtime/CONTRACT.md").write_text("local contract")
        (self.project / ".aek/runtime/ROUTES.md").write_text("local routes")
        self.conflict_without_writes(lambda: aek.restore(self.project, source="../kit-1", replace=["CONTRACT.md"]))

    def test_restore_wrong_source_version_or_same_version_bytes_is_no_write(self):
        self.install()
        (self.project / ".aek/runtime/CONTRACT.md").unlink()
        for version in ["1.0.0", "1.1.0"]:
            source = self.incoming(version)
            (source / "ROUTES.md").write_text("untrusted different bytes")
            with self.subTest(version=version):
                self.conflict_without_writes(lambda: aek.restore(self.project, source=self.relative(source)))

    def test_restore_unknown_runtime_content_and_invalid_replace_are_no_write(self):
        self.install()
        extra = self.project / ".aek/runtime/extra.txt"
        extra.write_text("untracked content")
        self.conflict_without_writes(lambda: aek.restore(self.project, source="../kit-1"))
        extra.unlink()
        self.conflict_without_writes(lambda: aek.restore(self.project, source="../kit-1", replace=["../outside"]))

    def test_restore_symlinked_runtime_or_source_is_no_write(self):
        self.install()
        runtime = self.project / ".aek/runtime/CONTRACT.md"
        runtime.unlink()
        runtime.symlink_to(self.source / "CONTRACT.md")
        self.conflict_without_writes(lambda: aek.restore(self.project, source="../kit-1"), self.root)
        runtime.unlink()
        alias = self.root / "alias"
        alias.symlink_to(self.source, target_is_directory=True)
        self.conflict_without_writes(lambda: aek.restore(self.project, source="../alias"), self.root)

    def test_restore_linked_missing_source_requires_explicit_external_write_scope(self):
        (self.source / "VERSION").write_text("0.2.0\n")
        self.install(strategy="linked")
        trusted = self.incoming("0.2.0")
        self.source.rename(self.root / "unavailable-kit")
        project_before = self.snapshot()
        self.assertEqual(project_before["AGENTS.md"], aek.LEGACY_BLOCK)
        self.conflict_without_writes(lambda: aek.restore(self.project, source=self.relative(trusted)), self.root)
        result = aek.restore(self.project, source=self.relative(trusted), allow_linked_write=True)
        self.assertEqual(result["static_validation"], "pass")
        self.assertEqual(project_before, self.snapshot())
        self.assertEqual(self.snapshot(self.source), self.snapshot(trusted))

    def test_restore_linked_corruption_requires_both_scope_and_replace(self):
        self.install(strategy="linked")
        trusted = self.incoming("1.0.0")
        (self.source / "CONTRACT.md").write_text("local linked adaptation")
        self.conflict_without_writes(lambda: aek.restore(self.project, source=self.relative(trusted),
                                                        replace=["CONTRACT.md"]), self.root)
        self.conflict_without_writes(lambda: aek.restore(self.project, source=self.relative(trusted),
                                                        allow_linked_write=True), self.root)
        project_before = self.snapshot()
        result = aek.restore(self.project, source=self.relative(trusted), replace=["CONTRACT.md"],
                             allow_linked_write=True)
        self.assertEqual(result["static_validation"], "pass")
        self.assertEqual(project_before, self.snapshot())
        self.assertEqual((self.source / "CONTRACT.md").read_bytes(), (trusted / "CONTRACT.md").read_bytes())


class GlobalBundleIntegrityTests(unittest.TestCase):
    def fixture(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name).resolve()
        self.checkout = root / "checkout"
        (self.checkout / "scripts").mkdir(parents=True)
        shutil.copy2(ROOT / "scripts/install_skill.py", self.checkout / "scripts/install_skill.py")
        self.skill = self.checkout / "skills/agent-engineering-kit"
        shutil.copytree(ROOT / "skills/agent-engineering-kit", self.skill,
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        self.base = root / "installed"
        self.target = self.base / "agent-engineering-kit"

    def run_installer(self, *extra):
        command = [sys.executable, str(self.checkout / "scripts/install_skill.py"),
                   "--skills-dir", str(self.base), *extra]
        return subprocess.run(command, capture_output=True, text=True)

    def installed_bytes(self):
        return {p.relative_to(self.target).as_posix(): p.read_bytes()
                for p in self.target.rglob("*") if p.is_file()}

    def set_source_version(self, version):
        path = self.skill / "core/VERSION"
        previous = path.read_text().strip()
        path.write_text(version + "\n")
        metadata = self.skill / "SKILL.md"
        metadata.write_text(metadata.read_text().replace('version: "' + previous + '"',
                                                         'version: "' + version + '"'))

    def test_global_repair_missing_verifier_restores_exact_receipt(self):
        self.fixture()
        result = self.run_installer()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        before = self.installed_bytes()
        (self.target / "core/aek.py").unlink()
        result = self.run_installer("--repair")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "repaired")
        self.assertEqual(before, self.installed_bytes())

    def test_global_repair_divergence_requires_explicit_replace(self):
        self.fixture()
        result = self.run_installer()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        intact = self.installed_bytes()
        entry = self.target / "core/ENTRY.md"
        entry.write_text("A local decision or corruption; preserve until explicitly selected.")
        divergent = self.installed_bytes()
        result = self.run_installer("--repair")
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertEqual(divergent, self.installed_bytes())
        result = self.run_installer("--repair", "--replace", "core/ENTRY.md")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(intact, self.installed_bytes())

    def test_global_repair_wrong_version_or_hash_preserves_installation(self):
        for kind in ["wrong_hash", "wrong_version"]:
            with self.subTest(kind=kind):
                self.fixture()
                result = self.run_installer()
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                (self.target / "core/aek.py").unlink()
                before = self.installed_bytes()
                if kind == "wrong_hash":
                    path = self.skill / "core/ROUTES.md"
                    path.write_bytes(path.read_bytes() + b"\nChanged release content.\n")
                else:
                    self.set_source_version("9.0.0")
                result = self.run_installer("--repair")
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertEqual(before, self.installed_bytes())

    def test_global_update_same_version_mutation_or_downgrade_is_no_write(self):
        for kind in ["same_version", "downgrade"]:
            with self.subTest(kind=kind):
                self.fixture()
                result = self.run_installer()
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                before = self.installed_bytes()
                if kind == "same_version":
                    path = self.skill / "core/ROUTES.md"
                    path.write_bytes(path.read_bytes() + b"\nMutated release content.\n")
                else:
                    self.set_source_version("0.0.0")
                result = self.run_installer()
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertEqual(before, self.installed_bytes())

    def test_global_installer_rejects_missing_core_license_and_mismatched_metadata(self):
        for kind in ["missing_license", "mismatched_version"]:
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as directory:
                root = Path(directory).resolve()
                checkout = root / "checkout"
                (checkout / "scripts").mkdir(parents=True)
                shutil.copy2(ROOT / "scripts/install_skill.py", checkout / "scripts/install_skill.py")
                skill = checkout / "skills/agent-engineering-kit"
                shutil.copytree(ROOT / "skills/agent-engineering-kit", skill,
                                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
                if kind == "missing_license":
                    (skill / "core/LICENSE").unlink()
                else:
                    (skill / "core/VERSION").write_text("9.0.0\n")
                base = root / "installed"
                command = [sys.executable, str(checkout / "scripts/install_skill.py"), "--skills-dir", str(base)]
                result = subprocess.run(command, capture_output=True, text=True)
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertFalse((base / "agent-engineering-kit").exists())


if __name__ == "__main__":
    unittest.main()
