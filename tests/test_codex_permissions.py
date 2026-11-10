"""Offline schema and rendering checks; these do not execute Codex."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('codex_permissions', Path(__file__).resolve().parents[1] / 'scripts/codex_permissions.py')
cp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cp)


class CodexPermissions(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()
        (self.root / 'view').mkdir()
        (self.root / 'run' / 'actions').mkdir(parents=True)
        (self.root / 'run' / 'final').mkdir(parents=True)
        self.policy = {
            'schema': 1,
            'binding': 'a' * 64,
            'allowed_read_roots': [str(self.root / 'view')],
            'denied_read_roots': sorted([str(self.root / 'snapshot'), str(self.root / 'private')]),
            'future_read_roots': [str(self.root / 'run/actions'), str(self.root / 'run/final')],
            'default_read': 'deny',
            'deny_precedence_required': True,
            'status': 'requires-host-enforcement',
        }

    def tearDown(self):
        self.temp.cleanup()

    def test_minimal_profile_emits_default_deny_and_explicit_view(self):
        text = cp.render(self.policy)
        self.assertIn('default_permissions = "aek-eval"', text)
        self.assertNotIn('extends = ":workspace"', text)
        self.assertIn('":root" = "deny"', text)
        self.assertIn('":minimal" = "read"', text)
        self.assertIn(json.dumps(str(self.root / 'view')) + ' = "read"', text)
        self.assertIn(json.dumps(str(self.root / 'snapshot')) + ' = "deny"', text)
        self.assertNotIn('sandbox_mode', text)
        self.assertNotIn('sandbox_workspace_write', text)
        self.assertIn('[permissions.aek-eval.network]\nenabled = false', text)

    def test_write_view_is_explicit(self):
        text = cp.render(self.policy, write_view=True)
        self.assertIn(json.dumps(str(self.root / 'view')) + ' = "write"', text)
        for protected in ('.git', '.agents', '.codex', '.aws'):
            self.assertIn(json.dumps(str(self.root / 'view' / protected)) + ' = "read"', text)
        self.assertIn(json.dumps(str(self.root / 'view')) + ' = "read"', cp.render(self.policy))

    def test_future_roots_not_granted_until_operator_unlock(self):
        with self.assertRaises(cp.PolicyError):
            cp.render(self.policy, stage='actions')
        actions = cp.render(self.policy, stage='actions', operator_unlocked=True)
        self.assertIn(json.dumps(str(self.root / 'run/actions')) + ' = "read"', actions)
        self.assertNotIn(json.dumps(str(self.root / 'run/final')) + ' = "read"', actions)

    def test_rejects_bad_schema_fields_and_types(self):
        for patch in (
            {'schema': 2}, {'binding': 'x'}, {'default_read': 'allow'},
            {'deny_precedence_required': False}, {'status': 'ready'},
            {'unexpected': 'field'}, {'allowed_read_roots': 'not-a-list'},
            {'future_read_roots': [str(self.root / '../escape')]},
            {'denied_read_roots': ['" = "read"\n[permissions.admin]']},
        ):
            policy = copy.deepcopy(self.policy)
            policy.update(patch)
            with self.subTest(patch=patch), self.assertRaises(cp.PolicyError):
                cp.render(policy)

    def test_rejects_allowed_denied_and_future_overlaps(self):
        for key, value in (
            ('denied_read_roots', [str(self.root), str(self.root / 'private')]),
            ('denied_read_roots', [str(self.root / 'VIEW')]),
            ('future_read_roots', [str(self.root / 'view/actions')]),
            ('future_read_roots', [str(self.root / 'snapshot/actions')]),
        ):
            policy = copy.deepcopy(self.policy)
            policy[key] = sorted(set(value))
            with self.subTest(key=key, value=value), self.assertRaises(cp.PolicyError):
                cp.render(policy)

    def test_rejects_noncanonical_and_filesystem_aliases(self):
        private = self.root / 'private'
        private.mkdir()
        policy = copy.deepcopy(self.policy)
        policy['allowed_read_roots'] = ['/' + str(private)]
        policy['denied_read_roots'] = sorted([str(private), str(self.root / 'snapshot')])
        with self.assertRaises(cp.PolicyError):
            cp.render(policy)
        # The double-leading-slash spelling is noncanonical even when a host
        # happens to resolve it to the same directory.
        policy['allowed_read_roots'] = [str(self.root / 'view')]
        policy['denied_read_roots'] = sorted(['//' + str(private).lstrip('/'), str(self.root / 'snapshot')])
        with self.assertRaises(cp.PolicyError):
            cp.render(policy)

    def test_rejects_overlapping_future_stage_roots(self):
        policy = copy.deepcopy(self.policy)
        policy['future_read_roots'] = [str(self.root / 'run'), str(self.root / 'run/final')]
        with self.assertRaises(cp.PolicyError):
            cp.render(policy)

    def test_unicode_paths_render_as_utf8_toml(self):
        unicode_view = self.root / 'view-😀'
        unicode_view.mkdir()
        policy = copy.deepcopy(self.policy)
        policy['allowed_read_roots'] = [str(unicode_view)]
        text = cp.render(policy)
        self.assertIn(json.dumps(str(unicode_view), ensure_ascii=False) + ' = "read"', text)
        self.assertNotIn('\\ud83d\\ude00', text.lower())

    def test_control_characters_in_paths_fail(self):
        policy = copy.deepcopy(self.policy)
        policy['denied_read_roots'] = sorted([str(self.root / 'private\ncorpus'), str(self.root / 'snapshot')])
        with self.assertRaises(cp.PolicyError):
            cp.render(policy)
        policy['denied_read_roots'] = sorted([str(self.root / 'private\x00corpus'), str(self.root / 'snapshot')])
        with self.assertRaises(cp.PolicyError):
            cp.render(policy)

    def test_rejects_unsorted_duplicate_and_symlinked_paths(self):
        policy = copy.deepcopy(self.policy)
        policy['denied_read_roots'] = list(reversed(policy['denied_read_roots']))
        with self.assertRaises(cp.PolicyError):
            cp.render(policy)
        policy = copy.deepcopy(self.policy)
        policy['future_read_roots'].append(policy['future_read_roots'][0])
        with self.assertRaises(cp.PolicyError):
            cp.render(policy)
        alias = self.root / 'alias'
        alias.symlink_to(self.root / 'view', target_is_directory=True)
        policy = copy.deepcopy(self.policy)
        policy['allowed_read_roots'] = [str(alias)]
        with self.assertRaises(cp.PolicyError):
            cp.render(policy)


if __name__ == '__main__':
    unittest.main()
