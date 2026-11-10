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
        manifest_bytes = (self.output / 'manifest.json').read_bytes()
        manifest = ev.read_json(self.output / 'manifest.json')
        self.assertEqual(manifest['view_hashes']['objective'], ev.tree_hash(self.output / 'objective'))
        self.assertNotEqual(manifest['view_hashes']['objective'], ev.hash_file(self.snapshot / 'pins.json'))
        with self.assertRaises(OSError):
            ev.unlock(self.output)
        with self.assertRaises(ev.IsolationError):
            ev.tree_hash(self.output / 'actions')
        ev.record_receipt(self.output, self.receipt())
        ev.unlock(self.output)
        self.assertEqual(manifest_bytes, (self.output / 'manifest.json').read_bytes())
        self.assertEqual(manifest['view_hashes']['actions'], ev.tree_hash(self.output / 'actions'))
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

    def test_prepared_objective_and_actions_are_checked_before_and_after_receipts(self):
        self.prepare()
        (self.output / 'objective/tests/test_app.py').write_text('changed before verdict')
        with self.assertRaisesRegex(ev.IsolationError, 're-prepare from the immutable snapshot'):
            ev.record_receipt(self.output, self.receipt())

        self.output = self.root / 'output-actions'
        self.prepare()
        ev.record_receipt(self.output, self.receipt())
        ev.unlock(self.output)
        (self.output / 'actions/actions.log').write_text('changed before inspection')
        with self.assertRaisesRegex(ev.IsolationError, 're-prepare from the immutable snapshot'):
            ev.record_receipt(self.output, self.receipt(True), inspected=True)

        self.output = self.root / 'output-after-inspection'
        self.prepare()
        ev.record_receipt(self.output, self.receipt())
        ev.unlock(self.output)
        ev.record_receipt(self.output, self.receipt(True), inspected=True)
        (self.output / 'actions/actions.log').write_text('changed after inspection')
        with self.assertRaisesRegex(ev.IsolationError, 're-prepare from the immutable snapshot'):
            ev.unlock(self.output, final=True)

    def test_legacy_inflight_manifest_fails_closed_with_reprepare_guidance(self):
        self.prepare()
        path = self.output / 'manifest.json'
        manifest = ev.read_json(path)
        manifest['schema'] = 1
        manifest.pop('view_hashes')
        path.write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ev.IsolationError, 're-prepare from the immutable snapshot'):
            ev.load(self.output)

    def test_projection_hash_order_matches_nested_path_tree_order(self):
        self.add('a.py', 'print("sibling")\n', 'objective', 'code')
        self.add('a/child.py', 'print("nested")\n', 'objective', 'code')
        self.prepare()
        manifest = ev.read_json(self.output / 'manifest.json')
        self.assertEqual(manifest['view_hashes']['objective'], ev.tree_hash(self.output / 'objective'))

    def test_actor_view_remains_writable_after_prepare(self):
        ev.prepare(self.snapshot, self.config, self.output, actor=True)
        (self.output / 'public/app.py').write_text('actor work in writable view')
        self.assertEqual(ev.load(self.output)[1]['mode'], 'actor')

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

    def test_missing_initial_view_cannot_be_ready(self):
        self.prepare()
        (self.output / 'objective').rename(self.output / 'objective-missing')
        with self.assertRaises(ev.IsolationError):
            ev.readiness(self.output)


if __name__ == '__main__':
    unittest.main()
