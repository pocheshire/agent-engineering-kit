"""Backward-compatible runtime packaging and actual installed workflow entry."""
import importlib.util
import json
import os
from pathlib import Path
import py_compile
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
        self.core_source = self.root / 'core-source'
        shutil.copytree(CORE, self.core_source, ignore=shutil.ignore_patterns('__pycache__'))
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

    def test_cli_restore_executes_source_despite_stale_unchecked_bytecode(self):
        aek.install(self.project)
        runtime = self.project / '.aek/runtime'
        workflow = runtime / 'workflow.py'
        cache_prefix = self.root / 'pycache-prefix'
        env = dict(os.environ, PYTHONPYCACHEPREFIX=str(cache_prefix))
        cache_path = subprocess.run(
            [sys.executable, '-c',
             'import importlib.util, sys; print(importlib.util.cache_from_source(sys.argv[1]))',
             str(workflow)], capture_output=True, text=True, env=env)
        self.assertEqual(cache_path.returncode, 0, cache_path.stderr)
        cache = Path(cache_path.stdout.strip())
        cache.parent.mkdir(parents=True, exist_ok=True)
        evil = self.root / 'evil.py'
        evil.write_text('def main(argv=None):\n print("CACHED-AUDIT-CANARY")\n return 0\n')
        py_compile.compile(str(evil), cfile=str(cache), dfile=str(workflow),
                           invalidation_mode=py_compile.PycInvalidationMode.UNCHECKED_HASH)
        cached_canary = cache.read_bytes()
        workflow.write_text('# divergent bytes to be repaired\n')
        source = os.path.relpath(self.core_source, self.project)
        command = [sys.executable, '-B', str(runtime / 'aek.py'), 'restore', str(self.project),
                   '--source', source, '--replace', 'workflow.py']
        restored = subprocess.run(command, capture_output=True, text=True, env=env)
        self.assertEqual(restored.returncode, 0, restored.stdout + restored.stderr)
        self.assertEqual(json.loads(restored.stdout)['static_validation'], 'pass')
        self.assertEqual(cache.read_bytes(), cached_canary)
        run = subprocess.run([sys.executable, '-B', str(runtime / 'aek.py'), 'work', 'template', 'task'],
                             cwd=self.project, capture_output=True, text=True, env=env)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertNotIn('CACHED-AUDIT-CANARY', run.stdout)
        self.assertEqual(cache.read_bytes(), cached_canary)
        self.assertEqual(json.loads(run.stdout)['kind'], 'task')

    def test_cli_install_rejects_unsupported_nested_source_without_writes(self):
        (self.old / 'assets').mkdir()
        (self.old / 'assets/schema.json').write_text('{}\n')
        command = [sys.executable, str(CORE / 'aek.py'), 'install', str(self.project),
                   '--source', '../old']
        run = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(run.returncode, 2)
        self.assertIn('unsupported resource', json.loads(run.stdout)['error'])
        self.assertEqual(list(self.project.iterdir()), [])

    def test_new_version_requires_both_workflow_resources(self):
        incoming = self.root / 'new'
        shutil.copytree(CORE, incoming, ignore=shutil.ignore_patterns('__pycache__'))
        cache = incoming / '__pycache__' / 'workflow.pyc'
        cache.parent.mkdir()
        cache.write_bytes(b'ignored interpreter cache')
        self.assertIn('workflow.py', aek.bundle(incoming)[1])
        for name in ('workflow.py', 'WORKFLOW.md'):
            data = (incoming / name).read_bytes()
            (incoming / name).unlink()
            with self.assertRaises(aek.Conflict):
                aek.bundle(incoming)
            (incoming / name).write_bytes(data)


if __name__ == '__main__':
    unittest.main()
