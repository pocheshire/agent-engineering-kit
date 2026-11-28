"""Backward-compatible runtime packaging and actual installed workflow entry."""
import importlib.util
import json
import os
from pathlib import Path
import py_compile
import re
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

    def test_routing_links_resolve_within_the_installed_pin(self):
        for strategy in ("vendored", "linked"):
            with self.subTest(strategy=strategy):
                project = self.root / strategy
                project.mkdir()
                aek.install(project, source="../core-source", strategy=strategy)
                state = json.loads((project / ".aek/state.json").read_text(encoding="utf-8"))
                runtime = (project / state["source"]).resolve() if state["source"] else project / ".aek/runtime"
                for document in runtime.glob("*.md"):
                    for link in re.findall(r"\]\(([^)]+)\)", document.read_text(encoding="utf-8")):
                        filename, _, fragment = link.partition("#")
                        target = (runtime / filename).resolve() if filename else document
                        self.assertEqual(target.parent, runtime, link)
                        self.assertTrue(target.is_file(), link)
                        if fragment:
                            headings = re.findall(r"^#+ (.+)$", target.read_text(encoding="utf-8"), re.MULTILINE)
                            anchors = [re.sub(r"[^\w -]", "", h.lower()).replace(" ", "-") for h in headings]
                            self.assertIn(fragment, anchors, link)

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
        agents = self.project / 'AGENTS.md'
        owner = b'# Original rules\r\n'
        agents.write_bytes(owner)
        aek.install(self.project, source='../old')
        installed_agents = owner + aek.LEGACY_BLOCK
        self.assertEqual(agents.read_bytes(), installed_agents)
        state = (self.project / '.aek/state.json').read_bytes()
        (self.project / '.aek/runtime/ENTRY.md').unlink()
        result = aek.restore(self.project, source='../old')
        self.assertEqual(result['changed'], ['ENTRY.md'])
        self.assertEqual(agents.read_bytes(), installed_agents)
        self.assertEqual((self.project / '.aek/state.json').read_bytes(), state)
        self.assertEqual(aek.audit(self.project)['static_validation'], 'pass')
        self.assertFalse((self.project / '.aek/runtime/workflow.py').exists())
        aek.uninstall(self.project)
        self.assertEqual(agents.read_bytes(), owner)

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

    def test_installed_feature_gate_and_small_change_route(self):
        aek.install(self.project)
        runtime = self.project / '.aek/runtime'
        document = self.project / 'spec.md'
        document.write_text('# Approved outcome\n', encoding='utf-8')
        command = [sys.executable, '-B', str(runtime / 'aek.py'), 'work', 'gate', 'plan', '--spec', document.name]
        run = subprocess.run(command, cwd=self.project, capture_output=True, text=True)
        blocked = json.loads(run.stdout)
        self.assertEqual((run.returncode, blocked['status']), (1, 'awaiting_spec_approval'))
        run = subprocess.run(command + ['--approved-spec', blocked['spec_id']], cwd=self.project,
                             capture_output=True, text=True)
        self.assertEqual((run.returncode, json.loads(run.stdout)['status']), (0, 'ready_to_plan'))

        routes = (runtime / 'ROUTES.md').read_text(encoding='utf-8')
        self.assertRegex(routes, r'\x60aek-feature\x60.*\(#feature-in-two-phases\)')
        feature = routes.split('## Feature in two phases\n', 1)[1].split('\n## ', 1)[0]
        self.assertIn('(WORKFLOW.md#feature-in-two-phases)', feature)
        workflow = (runtime / 'WORKFLOW.md').read_text(encoding='utf-8')
        self.assertIn('(CONTRACT.md#two-phase-procedure)', workflow)
        contract = (runtime / 'CONTRACT.md').read_text(encoding='utf-8')
        self.assertIn('(WORKFLOW.md#feature-approval-check)', contract)
        gate = workflow.split('## Feature approval check\n', 1)[1].split('\n## ', 1)[0]
        self.assertIn('work gate', gate)
        small = routes.split('## Direct work and small change\n', 1)[1].split('\n## ', 1)[0]
        self.assertIn('no standalone specification', small)
        self.assertNotIn('work gate', small)

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

    def test_maintenance_manual_required_only_from_its_introduction(self):
        manual = self.core_source / 'MAINTENANCE.md'
        original = manual.read_bytes()
        manual.unlink()
        version = self.core_source / 'VERSION'
        version.write_text('0.4.4-rc.5\n')
        with self.assertRaises(aek.Conflict):
            aek.install(self.project, source='../core-source')
        self.assertEqual(list(self.project.iterdir()), [])
        version.write_text('0.4.4-rc.4\n')
        aek.install(self.project, source='../core-source')
        self.assertEqual(aek.audit(self.project)['static_validation'], 'pass')
        manual.write_bytes(original)
        version.write_text('0.4.4-rc.5\n')
        aek.upgrade(self.project, source='../core-source')
        self.assertEqual((self.project / '.aek/runtime/MAINTENANCE.md').read_bytes(), original)
        self.assertEqual(aek.audit(self.project)['static_validation'], 'pass')

    def test_spec_resources_across_pin_lifecycle(self):
        resources = ('SPEC_TEMPLATE.md', 'SPEC_EXAMPLE.md')
        old = self.root / 'stable-core'
        shutil.copytree(self.core_source, old)
        (old / 'VERSION').write_text('0.4.5\n')
        for name in resources:
            (old / name).unlink()
        for strategy in ('vendored', 'linked'):
            for name in resources:
                with self.subTest(strategy=strategy, resource=name):
                    project = self.root / (strategy + name)
                    project.mkdir()
                    resource = self.core_source / name
                    saved = resource.read_bytes()
                    resource.unlink()
                    with self.assertRaises(aek.Conflict):
                        aek.install(project, source='../core-source', strategy=strategy)
                    self.assertEqual(list(project.iterdir()), [])
                    aek.install(project, source='../stable-core', strategy=strategy)
                    with self.assertRaises(aek.Conflict):
                        aek.upgrade(project, source='../core-source')
                    self.assertEqual(aek.audit(project)['static_validation'], 'pass')
                    resource.write_bytes(saved)
                    aek.upgrade(project, source='../core-source')
                    incomplete = self.root / ('incomplete-' + strategy + name)
                    shutil.copytree(self.core_source, incomplete)
                    (incomplete / name).unlink()
                    with self.assertRaises(aek.Conflict):
                        aek.restore(project, source='../' + incomplete.name,
                                    allow_linked_write=(strategy == 'linked'))
                    runtime = project / '.aek/runtime' if strategy == 'vendored' else self.core_source
                    (runtime / name).unlink()
                    self.assertEqual(aek.audit(project)['static_validation'], 'fail')
                    if strategy == 'vendored':
                        aek.restore(project, source='../core-source')
                    else:
                        (incomplete / name).write_bytes(saved)
                        aek.restore(project, source='../' + incomplete.name, allow_linked_write=True)
                    self.assertEqual((runtime / name).read_bytes(), saved)
                    self.assertEqual(aek.audit(project)['static_validation'], 'pass')

    def test_stable_requires_documentation_and_upgrades_nine_file_candidate(self):
        incoming = self.core_source
        (incoming / 'VERSION').write_text('0.4.0\n')
        documentation = (incoming / 'DOCUMENTATION.md').read_bytes()
        (incoming / 'DOCUMENTATION.md').unlink()
        with self.assertRaises(aek.Conflict):
            aek.install(self.project, source='../core-source')
        self.assertEqual(list(self.project.iterdir()), [])

        # Historical candidate pins had nine files and must remain usable.
        (incoming / 'VERSION').write_text('0.4.0-rc.1\n')
        aek.install(self.project, source='../core-source')
        self.assertEqual(aek.audit(self.project)['static_validation'], 'pass')
        self.assertFalse((self.project / '.aek/runtime/DOCUMENTATION.md').exists())
        (self.project / '.aek/runtime/ROUTES.md').unlink()
        aek.restore(self.project, source='../core-source')
        self.assertFalse((self.project / '.aek/runtime/DOCUMENTATION.md').exists())

        (incoming / 'VERSION').write_text('0.4.0\n')
        (incoming / 'DOCUMENTATION.md').write_bytes(documentation)
        aek.upgrade(self.project, source='../core-source')
        self.assertEqual((self.project / '.aek/runtime/DOCUMENTATION.md').read_bytes(), documentation)
        self.assertEqual(aek.audit(self.project)['static_validation'], 'pass')
        self.assertEqual(aek.upgrade(self.project, source='../core-source')['status'], 'unchanged')


if __name__ == '__main__':
    unittest.main()
