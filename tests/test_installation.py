"""Installation boundary tests use only synthetic temporary projects."""
import importlib.util
import json
import os
from pathlib import Path
import stat
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "skills/agent-engineering-kit/core/aek.py"
spec = importlib.util.spec_from_file_location("aek", SCRIPT)
aek = importlib.util.module_from_spec(spec)
spec.loader.exec_module(aek)

class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.project = self.root / "project"
        self.project.mkdir()
        self.source = self.root / "kit-1"
        self.source.mkdir()
        for name in aek.REQUIRED:
            (self.source / name).write_text("1.0.0\n" if name == "VERSION" else "original " + name + "\n")

    def install(self, **kwargs):
        return aek.install(self.project, source="../kit-1", **kwargs)

    def snapshot(self):
        return {str(p.relative_to(self.project)): p.read_bytes() for p in self.project.rglob("*") if p.is_file()}

    def next_source(self, version="1.1.0"):
        source = self.root / "kit-2"
        source.mkdir()
        for p in self.source.iterdir():
            (source / p.name).write_bytes(p.read_bytes())
        (source / "VERSION").write_text(version + "\n")
        return source

    def test_empty_and_audit_is_read_only(self):
        self.assertEqual(self.install(mode="initialize")["status"], "installed")
        before = self.snapshot()
        report = aek.audit(self.project)
        self.assertEqual(report["static_validation"], "pass")
        self.assertTrue(report["needs_agent_review"])
        self.assertEqual(report["behavioral_validation"], "not_performed")
        self.assertEqual(before, self.snapshot())
        project = json.loads((self.project / ".aek/project.json").read_text())
        self.assertFalse(project["authority"]["publication"])
        self.assertEqual(project["checks"], [])

    def test_existing_agents_preserved_byte_for_byte(self):
        original = b"# Local\r\nNever publish without permission.\r\n"
        (self.project / "AGENTS.md").write_bytes(original)
        self.install()
        self.assertEqual((self.project / "AGENTS.md").read_bytes(), original + aek.BLOCK)
        aek.uninstall(self.project)
        self.assertEqual((self.project / "AGENTS.md").read_bytes(), original)

    def test_generated_marker_follows_source_version(self):
        legacy = "4c87ee649fa18d4433736d7290f65d0d0e0b9e2ca8dc0392bbaecaeb22f688d2"
        current = "ee5af2b6fb4b70af5538c4850925110799a813ecb14bc23ff03388018ae8466c"
        cases = [("0.2.0", legacy), ("0.3.0-rc.0+build.9", legacy),
                 ("0.3.0-rc.1", current), ("0.3.0-rc.1+build.9", current),
                 ("0.3.0", current)]
        for index, (version, expected) in enumerate(cases):
            with self.subTest(version=version):
                target = self.root / ("project-" + str(index))
                target.mkdir()
                (self.source / "VERSION").write_text(version + "\n")
                aek.install(target, source="../kit-1", mode="initialize")
                self.assertEqual(aek.digest((target / "AGENTS.md").read_bytes()), expected)
                self.assertEqual(aek.audit(target)["static_validation"], "pass")

    def test_install_and_uninstall_preserve_existing_agents_permissions(self):
        original = b"# Owner instructions\n"
        for mode in (0o644, 0o600):
            with self.subTest(mode=oct(mode)):
                target = self.root / ("project-" + oct(mode))
                target.mkdir()
                path = target / "AGENTS.md"
                path.write_bytes(original)
                path.chmod(mode)
                aek.install(target, source="../kit-1")
                if os.name == "posix":
                    self.assertEqual(stat.S_IMODE(path.stat().st_mode), mode)
                aek.uninstall(target)
                self.assertEqual(path.read_bytes(), original)
                if os.name == "posix":
                    self.assertEqual(stat.S_IMODE(path.stat().st_mode), mode)
                path.unlink()

    def test_transaction_failure_cleans_temp_and_rolls_back_bytes_and_mode(self):
        modes = (0o751, 0o444) if os.name == "posix" else (0o751,)
        for mode in modes:
            with self.subTest(mode=oct(mode)):
                target = self.root / ("transaction-" + oct(mode))
                target.mkdir()
                path = target / "AGENTS.md"
                path.write_bytes(b"before\n")
                path.chmod(mode)
                replace = os.replace
                calls = 0

                def fail_second_replace(source, destination):
                    nonlocal calls
                    calls += 1
                    if calls == 2:
                        raise OSError("simulated replace failure")
                    return replace(source, destination)

                with patch.object(aek.os, "replace", side_effect=fail_second_replace):
                    with self.assertRaisesRegex(OSError, "simulated"):
                        aek.transact(target, {"AGENTS.md": b"after\n", "new/file.txt": b"new\n"})
                self.assertEqual(path.read_bytes(), b"before\n")
                if os.name == "posix":
                    self.assertEqual(stat.S_IMODE(path.stat().st_mode), mode)
                self.assertFalse((target / "new/file.txt").exists())
                self.assertEqual(list(target.iterdir()), [path])

    def test_repeated_install_is_idempotent(self):
        self.install()
        before = self.snapshot()
        self.assertEqual(self.install()["status"], "unchanged")
        self.assertEqual(before, self.snapshot())

    def test_unmanaged_markers_and_directory_conflict_without_mutation(self):
        (self.project / "AGENTS.md").write_bytes(aek.BEGIN)
        before = self.snapshot()
        with self.assertRaises(aek.Conflict):
            self.install()
        self.assertEqual(before, self.snapshot())
        (self.project / "AGENTS.md").unlink()
        (self.project / ".aek").mkdir()
        (self.project / ".aek/private").write_text("local")
        before = self.snapshot()
        with self.assertRaises(aek.Conflict):
            self.install()
        self.assertEqual(before, self.snapshot())

    def test_upgrade_preserves_local_only_edits_and_user_files(self):
        self.install()
        runtime = self.project / ".aek/runtime/CONTRACT.md"
        runtime.write_text("local contract")
        local = self.project / ".aek/local.md"
        local.write_text("local decisions")
        source = self.next_source()
        (source / "ROUTES.md").write_text("new routes")
        aek.upgrade(self.project, source="../kit-2")
        self.assertEqual(runtime.read_text(), "local contract")
        self.assertEqual(local.read_text(), "local decisions")
        self.assertEqual((self.project / ".aek/runtime/ROUTES.md").read_text(), "new routes")
        self.assertEqual(aek.audit(self.project)["static_validation"], "fail")

    def test_upgrade_conflict_is_no_write(self):
        (self.source / "VERSION").write_text("0.2.0\n")
        self.install()
        (self.project / ".aek/runtime/CONTRACT.md").write_text("local")
        source = self.next_source("0.3.0-rc.1")
        (source / "CONTRACT.md").write_text("upstream")
        before = self.snapshot()
        with self.assertRaisesRegex(aek.Conflict, "CONTRACT"):
            aek.upgrade(self.project, source="../kit-2")
        self.assertEqual(before, self.snapshot())

    def test_upgrade_handles_added_deleted_and_locally_deleted_files(self):
        (self.source / "OLD.md").write_text("old")
        (self.source / "LOCAL.md").write_text("local")
        self.install()
        (self.project / ".aek/runtime/LOCAL.md").unlink()
        source = self.next_source()
        (source / "OLD.md").unlink()
        (source / "NEW.md").write_text("new")
        aek.upgrade(self.project, source="../kit-2")
        self.assertFalse((self.project / ".aek/runtime/OLD.md").exists())
        self.assertFalse((self.project / ".aek/runtime/LOCAL.md").exists())
        self.assertEqual((self.project / ".aek/runtime/NEW.md").read_text(), "new")

    def test_missing_linked_source_is_honest(self):
        self.install(strategy="linked")
        self.source.rename(self.root / "hidden")
        before = self.snapshot()
        self.assertEqual(aek.audit(self.project)["static_validation"], "fail")
        self.assertEqual(before, self.snapshot())

    def test_linked_install_relocates_and_is_pinned(self):
        self.install(strategy="linked")
        state = json.loads((self.project / ".aek/state.json").read_text())
        self.assertEqual(state["source"], "../kit-1")
        self.assertNotIn(str(self.root), json.dumps(state))
        moved = self.root / "moved"
        moved.mkdir()
        self.project.rename(moved / "project")
        self.source.rename(moved / "kit-1")
        self.assertEqual(aek.audit(moved / "project")["static_validation"], "pass")
        (moved / "kit-1/CONTRACT.md").write_text("mutated")
        self.assertEqual(aek.audit(moved / "project")["static_validation"], "fail")

    def test_linked_upgrade_requires_usable_explicit_new_source(self):
        self.install(strategy="linked")
        self.next_source()
        aek.upgrade(self.project, source="../kit-2")
        self.assertEqual(aek.audit(self.project)["static_validation"], "pass")
        (self.root / "kit-2/CONTRACT.md").write_text("unreviewed")
        before = self.snapshot()
        with self.assertRaises(aek.Conflict):
            aek.upgrade(self.project)
        self.assertEqual(before, self.snapshot())

    def test_absolute_source_rejected(self):
        with self.assertRaises(aek.Conflict):
            aek.install(self.project, source=str(self.source))

    def test_symlink_managed_ancestors_and_leaf_rejected(self):
        outside = self.root / "outside"
        outside.mkdir()
        (self.project / ".aek").symlink_to(outside, target_is_directory=True)
        with self.assertRaises(aek.Conflict):
            self.install()
        self.assertEqual(list(outside.iterdir()), [])
        (self.project / ".aek").unlink()
        (self.project / "AGENTS.md").symlink_to(outside / "victim")
        with self.assertRaises(aek.Conflict):
            self.install()
        self.assertFalse((outside / "victim").exists())

    def test_symlink_runtime_ancestor_blocks_upgrade_before_writing(self):
        self.install()
        runtime = self.project / ".aek/runtime"
        runtime.rename(self.root / "runtime")
        runtime.symlink_to(self.root / "runtime", target_is_directory=True)
        self.next_source()
        state = (self.project / ".aek/state.json").read_bytes()
        with self.assertRaises(aek.Conflict):
            aek.upgrade(self.project, source="../kit-2")
        self.assertEqual(state, (self.project / ".aek/state.json").read_bytes())

    def test_changed_entrypoint_blocks_mutations(self):
        self.install()
        (self.project / ".aek/ENTRY.md").write_text("local")
        before = self.snapshot()
        with self.assertRaises(aek.Conflict):
            aek.uninstall(self.project)
        self.assertEqual(before, self.snapshot())

    def test_uninstall_retains_adaptations(self):
        self.install()
        (self.project / ".aek/local.md").write_text("important decision")
        aek.uninstall(self.project)
        self.assertFalse((self.project / "AGENTS.md").exists())
        self.assertFalse((self.project / ".aek/state.json").exists())
        self.assertEqual((self.project / ".aek/local.md").read_text(), "important decision")

    def test_linked_upgrade_preserves_active_adaptation_by_conflicting(self):
        self.install(strategy="linked")
        new = self.next_source()
        (self.source / "CONTRACT.md").write_text("local adaptation")
        (new / "CONTRACT.md").write_text("upstream change")
        before = self.snapshot()
        with self.assertRaisesRegex(aek.Conflict, "adaptations"):
            aek.upgrade(self.project, source="../kit-2")
        self.assertEqual(before, self.snapshot())

    def test_linked_upgrade_rejects_nonoverlap_without_changing_shared_sources(self):
        (self.source / "VERSION").write_text("0.2.0\n")
        self.install(strategy="linked")
        incoming = self.next_source("0.3.0-rc.1")
        # The incoming release changes VERSION only; the old linked source has a
        # project-specific ROUTES edit that is absent from the new source.
        (self.source / "ROUTES.md").write_bytes(
            (self.source / "ROUTES.md").read_bytes() + b"\nOwner route adaptation\n")
        project_before = self.snapshot()

        def source_snapshot(source):
            return {p.relative_to(source).as_posix(): p.read_bytes()
                    for p in source.rglob("*") if p.is_file()}

        old_before = source_snapshot(self.source)
        incoming_before = source_snapshot(incoming)
        with self.assertRaisesRegex(aek.Conflict, "ROUTES.md"):
            aek.upgrade(self.project, source="../kit-2")
        self.assertEqual(project_before, self.snapshot())
        self.assertEqual(old_before, source_snapshot(self.source))
        self.assertEqual(incoming_before, source_snapshot(incoming))

    def test_same_version_changed_source_is_not_unchanged(self):
        self.install()
        (self.source / "CONTRACT.md").write_text("changed without new version")
        before = self.snapshot()
        with self.assertRaises(aek.Conflict):
            self.install()
        self.assertEqual(before, self.snapshot())

    def test_untracked_runtime_is_not_silently_valid(self):
        self.install()
        (self.project / ".aek/runtime/UNTRACKED.md").write_text("extra instructions")
        self.assertEqual(aek.audit(self.project)["static_validation"], "fail")

    def evidence(self):
        self.evidence_path = self.root / "evidence.json"
        self.required_path = self.root / "required.json"
        self.required_path.write_text(json.dumps(["one", "two"]))
        return {"command": "test", "environment": "synthetic fixture", "revision": "abc", "result": "passed",
                "tests": {"total": 2, "passed": 2, "failed": 0, "skipped": 0,
                          "completed_ids": ["one", "two"], "skipped_ids": [],
                          "expected_failure_ids": [], "unexpected_success_ids": []}}

    def verify(self, value):
        self.evidence_path.write_text(json.dumps(value))
        return aek.check_evidence(self.evidence_path, self.required_path)

    def test_evidence_accepts_only_exact_executed_cases(self):
        value = self.evidence()
        self.assertEqual(self.verify(value)["executed"], 2)
        for ids in (["one"], ["one", "replacement"], ["one", "one", "two"], []):
            value = self.evidence()
            value["tests"]["completed_ids"] = ids
            with self.subTest(ids=ids), self.assertRaises(aek.Conflict):
                self.verify(value)

    def test_evidence_rejects_zero_skipped_false_counts_and_failures(self):
        for counts in ({"total": 0, "passed": 0, "failed": 0, "skipped": 0},
                       {"total": 2, "passed": 0, "failed": 0, "skipped": 2},
                       {"total": 2, "passed": 1, "failed": 1, "skipped": 0},
                       {"total": 9, "passed": 2, "failed": 0, "skipped": 0},
                       {"total": 2, "passed": True, "failed": 0, "skipped": 0}):
            value = self.evidence()
            value["tests"].update(counts)
            with self.subTest(counts=counts), self.assertRaises(aek.Conflict):
                self.verify(value)

    def test_evidence_rejects_expected_failures_skipped_cases_and_missing_context(self):
        for key in ("skipped_ids", "expected_failure_ids", "unexpected_success_ids"):
            value = self.evidence()
            value["tests"][key] = ["one"]
            with self.subTest(key=key), self.assertRaises(aek.Conflict):
                self.verify(value)
        value = self.evidence()
        del value["environment"]
        with self.assertRaises(aek.Conflict):
            self.verify(value)

if __name__ == "__main__":
    unittest.main()
