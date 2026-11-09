"""Adversarial disclosure checks; no host sandbox claims are made here."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('eval_views', Path(__file__).resolve().parents[1] / 'scripts/eval_views.py')
ev = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ev)


class EvaluationViews(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()
        self.snapshot = self.root / 'snapshot'
        self.snapshot.mkdir()
        self.output = self.root / 'output'
        self.config = {'snapshot_id': 'snapshot-1', 'revision': 'revision-1', 'private_roots': [str(self.root / 'private')], 'files': []}
        self.add('app.py', 'print("public code")\n', 'public', 'code')
        self.add('tests/test_app.py', 'assert 2 + 2 == 4\n', 'objective', 'test')
        self.add('pins.json', json.dumps({'version': '1', 'review': 'SECRET_REVIEW', 'unexpected': 'SECRET_EXTRA'}), 'objective', 'pins', fields=['version'])
        self.add('requirements.md', 'Original trusted requirement\n', 'requirements', 'trusted-requirement')
        self.add('local.md', 'SECRET_NARRATIVE', 'opaque', 'hash-only')
        self.add('actions.log', 'raw action: command/output', 'actions', 'raw')
        self.add('final.md', 'SECRET_SELF_ASSESSMENT', 'final', 'raw')

    def tearDown(self):
        self.temp.cleanup()

    def add(self, name, content, phase, kind, **extra):
        path = self.snapshot / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        self.config['files'].append(dict(path=name, sha256=ev.hash_file(path), phase=phase, kind=kind, **extra))

    def prepare(self):
        return ev.prepare(self.snapshot, self.config, self.output)

    def receipt(self, inspected=False):
        return {'kind': 'action-inspection' if inspected else 'objective-verdict',
                'binding': ev.read_json(self.output / 'manifest.json')['binding'],
                'view_sha256': ev.tree_hash(self.output / ('actions' if inspected else 'objective')),
                'authority': 'harness', 'result': 'recorded observation'}

    def test_stages_require_bound_observations(self):
        self.prepare()
        with self.assertRaises(OSError):
            ev.unlock(self.output)
        with self.assertRaises(ev.IsolationError):
            ev.tree_hash(self.output / 'actions')
        ev.record_receipt(self.output, self.receipt())
        ev.unlock(self.output)
        self.assertEqual((self.output / 'actions/actions.log').read_text(), 'raw action: command/output')
        with self.assertRaises(OSError):
            ev.unlock(self.output, final=True)
        ev.record_receipt(self.output, self.receipt(True), inspected=True)
        ev.unlock(self.output, final=True)
        self.assertIn('SECRET_SELF', (self.output / 'final/final.md').read_text())
        with self.assertRaises(ev.IsolationError):
            ev.unlock(self.output, final=True)
        (self.output / 'objective-verdict.json').unlink()
        with self.assertRaises(ev.IsolationError):
            ev.record_receipt(self.output, self.receipt())

    def test_canaries_and_pins_do_not_leak(self):
        original = {p: p.read_bytes() for p in self.snapshot.rglob('*') if p.is_file()}
        self.prepare()
        copied = b''.join(p.read_bytes() for p in (self.output / 'objective').rglob('*') if p.is_file())
        self.assertNotIn(b'SECRET', copied)
        self.assertEqual(ev.read_json(self.output / 'objective/pins.json'), {'version': '1'})
        self.assertFalse((self.output / 'actions').exists())
        self.assertTrue(all(p.read_bytes() == data for p, data in original.items()))
        with self.assertRaises(ev.IsolationError):
            self.prepare()

    def test_new_readme_markdown_hidden_and_directory_surprises_rejected(self):
        for name in ('README.md', 'nested/new.md', '.hidden', 'app.PY'):
            path = self.snapshot / name
            path.parent.mkdir(exist_ok=True)
            path.write_text('SECRET_INJECTION')
            with self.assertRaises(ev.IsolationError):
                self.prepare()
            path.unlink()
            if name.startswith('nested/'):
                path.parent.rmdir()
        (self.snapshot / 'empty').mkdir()
        with self.assertRaises(ev.IsolationError):
            self.prepare()

    def test_unknown_json_and_narrative_extensions_rejected(self):
        for patch in ({'review': 'SECRET'}, {'path': '../escape.py'}, {'path': 'new.md'}, {'path': 'LOCAL.MD'}, {'phase': 'unexpected'}):
            config = copy.deepcopy(self.config)
            config['files'][1].update(patch)
            with self.assertRaises(ev.IsolationError):
                ev.prepare(self.snapshot, config, self.output)
        config = copy.deepcopy(self.config)
        config['review'] = 'SECRET'
        with self.assertRaises(ev.IsolationError):
            ev.prepare(self.snapshot, config, self.output)
        self.config['files'][2]['fields'] = ['review']
        with self.assertRaises(ev.IsolationError):
            self.prepare()

    def test_duplicate_hash_case_and_json_keys_rejected(self):
        for patch in ({'sha256': self.config['files'][0]['sha256']}, {'path': 'APP.PY'}):
            config = copy.deepcopy(self.config)
            config['files'][1].update(patch)
            with self.assertRaises(ev.IsolationError):
                ev.prepare(self.snapshot, config, self.output)
        p = self.root / 'duplicate.json'
        p.write_text('{"key":1,"key":2}')
        with self.assertRaises(ev.IsolationError):
            ev.read_json(p)

    def test_symlinks_hardlinks_and_source_mutations_rejected(self):
        code = self.snapshot / 'app.py'
        code.unlink()
        code.symlink_to(self.snapshot / 'local.md')
        with self.assertRaises(ev.IsolationError):
            self.prepare()
        code.unlink()
        import os
        os.link(str(self.snapshot / 'local.md'), str(code))
        with self.assertRaises(ev.IsolationError):
            self.prepare()
        code.unlink()
        code.write_text('print("public code")\n')
        self.prepare()
        (self.snapshot / 'actions.log').write_text('changed action')
        with self.assertRaises(ev.IsolationError):
            ev.record_receipt(self.output, self.receipt())

    def test_tampered_wrong_snapshot_and_wrong_view_receipts_rejected(self):
        self.prepare()
        for patch in ({'binding': 'other-snapshot'}, {'view_sha256': '0' * 64}, {'authority': 'performer'}, {'kind': 'action-inspection'}):
            receipt = self.receipt()
            receipt.update(patch)
            with self.assertRaises(ev.IsolationError):
                ev.record_receipt(self.output, receipt)
        ev.record_receipt(self.output, self.receipt())
        (self.output / 'objective/tests/test_app.py').write_text('tampered')
        with self.assertRaises(ev.IsolationError):
            ev.unlock(self.output)

    def test_actor_bundle_excludes_private_expected_criteria(self):
        ev.prepare(self.snapshot, self.config, self.output, actor=True)
        self.assertEqual([p.name for p in (self.output / 'public').iterdir()], ['app.py'])
        with self.assertRaises(ev.IsolationError):
            ev.unlock(self.output)

    def test_host_receipt_required_and_failure_unknown_not_ready(self):
        self.prepare()
        result = ev.readiness(self.output)
        self.assertTrue(result['staged_disclosure'])
        self.assertFalse(result['ready'])
        receipt = {'binding': result['binding'], 'policy_sha256': result['policy_sha256'], 'provenance': 'host-enforcement-log:fixture',
                   'enforcement': 'passed', 'negative_canary': 'denied', 'allowed_root_check': 'passed'}
        self.assertTrue(ev.readiness(self.output, receipt)['ready'])
        for patch in ({'provenance': 'unknown'}, {'provenance': 'UNKNOWN'}, {'enforcement': 'failed'}, {'negative_canary': 'readable'}, {'policy_sha256': 'other'}):
            changed = dict(receipt, **patch)
            self.assertFalse(ev.readiness(self.output, changed)['ready'])
        policy_path = self.output / 'host-policy.json'
        policy = ev.read_json(policy_path)
        policy['allowed_read_roots'].append(str(self.snapshot))
        policy_path.write_text(json.dumps(policy))
        receipt['policy_sha256'] = ev.digest(policy)
        self.assertFalse(ev.readiness(self.output, receipt)['ready'])


if __name__ == '__main__':
    unittest.main()
