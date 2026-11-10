import importlib.util
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import zipfile
import runpy

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("gate", ROOT / "scripts" / "validate.py")
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)
import distribution


class DistributionTests(unittest.TestCase):
    def test_stale_marketplace_release_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory).resolve() / "release"
            shutil.copytree(ROOT, fixture, ignore=shutil.ignore_patterns(
                ".git", ".scratch", "dist", "__pycache__", ".venv", "validate.py"))
            path = fixture / ".claude-plugin/marketplace.json"
            data = json.loads(path.read_text())
            data["plugins"][0]["version"] = "0.0.0"
            path.write_text(json.dumps(data))
            with mock.patch.object(gate, "ROOT", fixture):
                self.assertIn("Marketplace version mismatch: .claude-plugin/marketplace.json", gate.static_checks())

    def test_global_skill_repeat_and_remove(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory).resolve() / "skills"
            command = [sys.executable, str(ROOT / "scripts" / "install_skill.py"), "--skills-dir", str(base)]
            first = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            target = base / "agent-engineering-kit"
            self.assertTrue((target / "core" / "aek.py").is_file())
            second = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(json.loads(second.stdout)["status"], "unchanged")
            removed = subprocess.run(command + ["--uninstall"], capture_output=True, text=True)
            self.assertEqual(removed.returncode, 0, removed.stderr)
            self.assertFalse(target.exists())

    def test_global_skill_preserves_local_edits(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory).resolve() / "skills"
            command = [sys.executable, str(ROOT / "scripts" / "install_skill.py"), "--skills-dir", str(base)]
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 0)
            entry = base / "agent-engineering-kit" / "SKILL.md"
            entry.write_text(entry.read_text() + "\nLocal adaptation\n")
            original = entry.read_bytes()
            for extra in [[], ["--uninstall"]]:
                result = subprocess.run(command + extra, capture_output=True)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(entry.read_bytes(), original)

    def test_global_skill_refuses_foreign_installation(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory).resolve()
            target = base / "agent-engineering-kit"
            target.mkdir()
            (target / "SKILL.md").write_text("User skill")
            result = subprocess.run([sys.executable, str(ROOT / "scripts" / "install_skill.py"), "--skills-dir", str(base)], capture_output=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual((target / "SKILL.md").read_text(), "User skill")


    def test_global_upgrade_and_malformed_receipt(self):
        import shutil
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory).resolve()
            source = base / "source"
            (source / "scripts").mkdir(parents=True)
            shutil.copy2(ROOT / "scripts/install_skill.py", source / "scripts/install_skill.py")
            shutil.copytree(ROOT / "skills", source / "skills")
            target_base = base / "installed"
            command = [sys.executable, str(source / "scripts/install_skill.py"), "--skills-dir", str(target_base)]
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 0)
            skill = source / "skills/agent-engineering-kit"
            original_version = (skill / "core/VERSION").read_text().strip()
            (skill / "core/VERSION").write_text("0.3.0\n")
            metadata = skill / "SKILL.md"
            metadata.write_text(metadata.read_text().replace('version: "' + original_version + '"', 'version: "0.3.0"'))
            updated = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(updated.returncode, 0, updated.stderr)
            installed = target_base / "agent-engineering-kit"
            self.assertEqual((installed / "core/VERSION").read_text(), "0.3.0\n")
            self.assertTrue((installed / "LICENSE").is_file())
            (installed / ".aek-skill-receipt.json").write_text("[]")
            failed = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(failed.returncode, 2)
            self.assertNotIn("Traceback", failed.stderr)


class GateTests(unittest.TestCase):
    def result(self, kind):
        class Sample(unittest.TestCase):
            def runTest(self):
                if kind == "skip":
                    self.skipTest("unavailable")
                if kind == "subskip":
                    with self.subTest(value=1):
                        self.skipTest("unavailable")
                if kind == "failure":
                    self.fail("broken")
        if kind == "expected":
            Sample.runTest = unittest.expectedFailure(lambda self: self.fail("known"))
        case = Sample()
        suite = unittest.TestSuite([] if kind == "zero" else [case])
        result = unittest.TextTestRunner(stream=io.StringIO(), resultclass=gate.StrictResult).run(suite)
        return result, [case.id()]

    def test_positive(self):
        result, ids = self.result("pass")
        self.assertTrue(gate.result_ok(result, ids))

    def test_zero_not_green(self):
        result, ids = self.result("zero")
        self.assertFalse(gate.result_ok(result, ids))

    def test_all_skipped_not_green(self):
        result, ids = self.result("skip")
        self.assertFalse(gate.result_ok(result, ids))

    def test_subtest_skipped_not_green(self):
        result, ids = self.result("subskip")
        self.assertFalse(gate.result_ok(result, ids))

    def test_expected_failure_not_green(self):
        result, ids = self.result("expected")
        self.assertFalse(gate.result_ok(result, ids))

    def test_failure_not_green(self):
        result, ids = self.result("failure")
        self.assertFalse(gate.result_ok(result, ids))

    def test_missing_replaced_duplicate_ids_not_green(self):
        result, ids = self.result("pass")
        for required in [[], ["unrelated"], ids + ["missing"], ids + ids]:
            self.assertFalse(gate.result_ok(result, required))

    def test_gate_cli_negative_controls(self):
        cases = {
            "zero": ("", []),
            "skipped": ("@unittest.skip('missing environment')\n", ["test_probe_unique.Probe.test_case"]),
            "expected": ("@unittest.expectedFailure\n", ["test_probe_unique.Probe.test_case"]),
            "missing": ("", ["test_probe_unique.Probe.test_case", "required.missing"]),
        }
        for kind, (decorator, expected) in cases.items():
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as directory:
                fixture = Path(directory).resolve()
                tests = fixture / "tests"
                tests.mkdir()
                body = "import unittest\n"
                if kind != "zero":
                    body += "class Probe(unittest.TestCase):\n"
                    body += "    " + decorator if decorator else ""
                    body += "    def test_case(self):\n        " + ("self.fail('known')" if kind == "expected" else "self.assertTrue(True)") + "\n"
                (tests / "test_probe_unique.py").write_text(body)
                (tests / "required-tests.json").write_text(json.dumps(expected))
                code = ("import importlib.util,pathlib,sys; "
                        "s=importlib.util.spec_from_file_location('isolated_gate',sys.argv[1]); "
                        "g=importlib.util.module_from_spec(s);s.loader.exec_module(g); "
                        "g.ROOT=pathlib.Path(sys.argv[2]);g.static_checks=lambda:[];sys.exit(g.run())")
                result = subprocess.run([sys.executable, "-c", code, str(ROOT / "scripts" / "validate.py"), str(fixture)], capture_output=True, text=True)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)


class ReleaseInventoryTests(unittest.TestCase):
    def fixture(self, directory):
        repo = Path(directory).resolve() / "release-fixture"
        shutil.copytree(ROOT, repo, ignore=shutil.ignore_patterns(
            ".git", ".scratch", "dist", "__pycache__", ".venv"))
        subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
        subprocess.run(["git", "config", "core.autocrlf", "false"], cwd=repo, check=True)
        subprocess.run(["git", "config", "user.name", "Fixture"], cwd=repo, check=True)
        subprocess.run(["git", "config", "user.email", "fixture@example.invalid"], cwd=repo, check=True)
        subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
        subprocess.run(["git", "commit", "-qm", "fixture"], cwd=repo, check=True)
        return repo

    def test_git_inventory_builds_exact_zip(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = self.fixture(directory)
            command = [sys.executable, str(repo / "scripts/package_release.py")]
            result = subprocess.run(command, cwd=repo, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            files = subprocess.check_output(["git", "ls-files", "-z"], cwd=repo).decode().split("\0")
            version = (repo / "VERSION").read_text().strip()
            archive = repo / "dist" / ("agent-engineering-kit-" + version + ".zip")
            with zipfile.ZipFile(archive) as bundle:
                self.assertEqual(set(bundle.namelist()), {"agent-engineering-kit/" + name for name in files if name})
                self.assertNotIn("agent-engineering-kit/.scratch/canary.txt", bundle.namelist())

    def test_forced_tracked_reserved_paths_fail_gate_and_packaging(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = self.fixture(directory)
            for name in (".scratch/canary.txt", "dist/old.zip", ".env.production"):
                path = repo / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("synthetic canary\n")
            subprocess.run(["git", "add", "-f", ".scratch/canary.txt", "dist/old.zip", ".env.production"], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-qm", "reserved-path controls"], cwd=repo, check=True)
            with mock.patch.object(gate, "ROOT", repo):
                errors = gate.static_checks()
            for name in (".scratch/canary.txt", "dist/old.zip", ".env.production"):
                self.assertIn("Reserved publication path: " + name, errors)
            result = subprocess.run([sys.executable, str(repo / "scripts/package_release.py")],
                                    cwd=repo, capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertIn("Refusing reserved publication path:", result.stderr)
            self.assertFalse((repo / "dist" / ("agent-engineering-kit-" + (repo / "VERSION").read_text().strip() + ".zip")).exists())

    def test_unpacked_inventory_does_not_borrow_parent_git(self):
        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory).resolve()
            subprocess.run(["git", "init", "-q"], cwd=parent, check=True)
            extracted = parent / "extracted-kit"
            shutil.copytree(ROOT, extracted, ignore=shutil.ignore_patterns(
                ".git", ".scratch", "dist", "__pycache__", ".venv"))
            (extracted / "probe.txt").write_text("/" + "Users/" + "synthetic-owner/review.txt\n")
            with mock.patch.object(gate, "ROOT", extracted):
                errors = gate.static_checks()
            self.assertTrue(any("private machine path in probe.txt" in error for error in errors), errors)

    def test_eligible_untracked_file_remains_in_privacy_scan(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = self.fixture(directory)
            (repo / "local-review.txt").write_text("/" + "Users/" + "synthetic-owner/private.txt\n")
            with mock.patch.object(gate, "ROOT", repo):
                errors = gate.static_checks()
            self.assertTrue(any("private machine path in local-review.txt" in error for error in errors), errors)

    def test_tracked_symlink_and_bytecode_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = self.fixture(directory)
            # Mock symlink metadata so this regression also runs on Windows
            # accounts that cannot create filesystem symlinks.
            (repo / "linked-license").write_text("LICENSE\n")
            (repo / "opaque.pyc").write_bytes(b"\x00\x01synthetic bytecode")
            (repo / "opaque.pyo").write_bytes(b"\x00\x01synthetic bytecode")
            subprocess.run(["git", "add", "linked-license"], cwd=repo, check=True)
            subprocess.run(["git", "add", "-f", "opaque.pyc", "opaque.pyo"], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-qm", "binary and symlink controls"], cwd=repo, check=True)
            actual_symlink = distribution.path_is_symlink
            def symlink_probe(root, name):
                return name == "linked-license" or actual_symlink(root, name)
            with mock.patch.object(gate, "ROOT", repo), mock.patch.object(distribution, "path_is_symlink", symlink_probe):
                errors = gate.static_checks()
            self.assertIn("Publication symlink: linked-license", errors)
            self.assertIn("Reserved publication path: opaque.pyc", errors)
            self.assertIn("Reserved publication path: opaque.pyo", errors)
            with mock.patch.object(distribution, "path_is_symlink", symlink_probe):
                with self.assertRaises(SystemExit) as raised:
                    runpy.run_path(str(repo / "scripts/package_release.py"), run_name="__main__")
            self.assertIn("Refusing reserved publication path: opaque.pyc, opaque.pyo", str(raised.exception))

    def test_package_rejects_symlink_before_creating_archive(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = self.fixture(directory)
            (repo / "linked-license").write_text("LICENSE\n")
            subprocess.run(["git", "add", "linked-license"], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-qm", "symlink fixture"], cwd=repo, check=True)
            actual_symlink = distribution.path_is_symlink
            def symlink_probe(root, name):
                return name == "linked-license" or actual_symlink(root, name)
            with mock.patch.object(distribution, "path_is_symlink", symlink_probe):
                with self.assertRaises(SystemExit) as raised:
                    runpy.run_path(str(repo / "scripts/package_release.py"), run_name="__main__")
            self.assertIn("Refusing publication symlink: linked-license", str(raised.exception))
            self.assertFalse((repo / "dist").exists())

    def test_env_example_is_permitted_but_scanned(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = self.fixture(directory)
            example = repo / ".env.example"
            example.write_text("SAMPLE=" + "/" + "Users/" + "synthetic-owner/example\n")
            subprocess.run(["git", "add", ".env.example"], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-qm", "example environment template"], cwd=repo, check=True)
            with mock.patch.object(gate, "ROOT", repo):
                errors = gate.static_checks()
            self.assertIn("private machine path in .env.example", errors)
            self.assertNotIn("Reserved publication path: .env.example", errors)

    def test_git_index_inventory_failure_does_not_fall_back(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = self.fixture(directory)
            original = distribution._git
            for failed_args, expected in [
                (("ls-files", "-z"), "Cannot read Git index"),
                (("ls-files", "--others", "-z"), "Cannot read Git untracked file list"),
            ]:
                def fail_inventory(root, *args):
                    if args == failed_args:
                        return subprocess.CompletedProcess(["git"], 1, b"", b"synthetic index error")
                    return original(root, *args)
                with self.subTest(args=failed_args), mock.patch.object(distribution, "_git", fail_inventory):
                    with self.assertRaisesRegex(RuntimeError, expected + ": synthetic index error"):
                        distribution.inventory(repo)

    def test_missing_tracked_path_fails_gate(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = self.fixture(directory)
            (repo / "docs/platforms.md").unlink()
            with mock.patch.object(gate, "ROOT", repo):
                errors = gate.static_checks()
            self.assertIn("Missing publication file: docs/platforms.md", errors)
