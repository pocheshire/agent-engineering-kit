"""Backward-compatible runtime packaging and actual installed workflow entry."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

CORE = Path(__file__).resolve().parents[1] / 'skills/agent-engineering-kit/core'
spec = importlib.util.spec_from_file_location('workflow_install_aek', CORE / 'aek.py')
aek = importlib.util.module_from_spec(spec)
spec.loader.exec_module(aek)


class WorkflowInstallation(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.project = self.root / 'project'
        self.project.mkdir()
        self.old = self.root / 'old'
        self.old.mkdir()
        for name in aek.LEGACY_REQUIRED:
            shutil.copyfile(CORE / name, self.old / name)
        (self.old / 'VERSION').write_text('0.1.1\n')

    def test_legacy_upgrade_adds_workflow_and_preserves_local_decisions(self):
        aek.install(self.project, source='../old')
        local = self.project / '.aek/local.md'
        local.write_text('Owner decisions retained\n')
        routes = self.project / '.aek/runtime/ROUTES.md'
        routes.write_bytes(routes.read_bytes() + b'\nOwner route adaptation\n')
        expected = routes.read_bytes()
        # ROUTES upstream has no change; the local edit is non-overlapping.
        incoming = self.root / 'new'
        shutil.copytree(CORE, incoming, ignore=shutil.ignore_patterns('__pycache__'))
        result = aek.upgrade(self.project, source='../new')
        self.assertEqual(result['kit_version'], (CORE / 'VERSION').read_text().strip())
        self.assertEqual(routes.read_bytes(), expected)
        self.assertEqual(local.read_text(), 'Owner decisions retained\n')
        self.assertTrue((self.project / '.aek/runtime/workflow.py').is_file())
        self.assertEqual(aek.audit(self.project)['static_validation'], 'fail')
        run = subprocess.run([sys.executable, '-B', str(self.project / '.aek/runtime/aek.py'),
                              'work', 'template', 'task'], capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(json.loads(run.stdout)['kind'], 'task')

    def test_current_verifier_restores_exact_seven_file_legacy_pin(self):
        aek.install(self.project, source='../old')
        state = (self.project / '.aek/state.json').read_bytes()
        (self.project / '.aek/runtime/ENTRY.md').unlink()
        aek.restore(self.project, source='../old')
        self.assertEqual((self.project / '.aek/state.json').read_bytes(), state)
        self.assertEqual(aek.audit(self.project)['static_validation'], 'pass')
        self.assertFalse((self.project / '.aek/runtime/workflow.py').exists())

    def test_dispatch_uses_installed_sibling_and_missing_helper_is_error(self):
        aek.install(self.project)
        runtime = self.project / '.aek/runtime'
        (self.project / 'workflow.py').write_text('raise RuntimeError("CWD shadow")\n')
        command = [sys.executable, '-B', str(runtime / 'aek.py'), 'work', 'template', 'run']
        run = subprocess.run(command, cwd=self.project, capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertFalse(json.loads(run.stdout)['live'])
        (runtime / 'workflow.py').unlink()
        run = subprocess.run(command, cwd=self.project, capture_output=True, text=True)
        self.assertEqual(run.returncode, 2)
        self.assertEqual(json.loads(run.stdout)['status'], 'error')

    def test_new_version_requires_both_workflow_resources(self):
        incoming = self.root / 'new'
        shutil.copytree(CORE, incoming, ignore=shutil.ignore_patterns('__pycache__'))
        for name in ('workflow.py', 'WORKFLOW.md'):
            data = (incoming / name).read_bytes()
            (incoming / name).unlink()
            with self.assertRaises(aek.Conflict):
                aek.bundle(incoming)
            (incoming / name).write_bytes(data)


if __name__ == '__main__':
    unittest.main()
