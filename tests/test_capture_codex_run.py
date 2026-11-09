import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/capture_codex_run.py'
spec = importlib.util.spec_from_file_location('capture_codex_run', SCRIPT)
capture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(capture)


class CaptureCodexRun(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / 'rollout.jsonl'

    def tearDown(self):
        self.temp.cleanup()

    def write(self, rows):
        self.path.write_text('\n'.join(json.dumps(row) for row in rows) + '\n', encoding='utf-8')

    def test_allowlist_omits_secret_payloads_and_counts_unique_tools_and_calls(self):
        self.write([
            {'type': 'session_meta', 'payload': {'id': 's1', 'invocation_id': 'i1', 'cli_version': '1.2', 'secret': 'SECRET_META'}},
            {'type': 'turn_context', 'payload': {'model': 'gpt-x', 'effort': 'high', 'api_key': 'SECRET_CONTEXT'}},
            {'type': 'response_item', 'payload': {'type': 'function_call', 'name': 'exec_command', 'arguments': 'SECRET_ARGUMENT'}},
            {'type': 'response_item', 'payload': {'type': 'custom_tool_call', 'name': 'exec_command', 'input': 'SECRET_INPUT'}},
            {'type': 'response_item', 'payload': {'type': 'function_call_output', 'output': 'SECRET_RESULT'}},
            {'type': 'event_msg', 'payload': {'type': 'agent_message', 'message': 'SECRET_MESSAGE'}},
        ])
        result = capture.capture(self.path, 'gpt-x', 'high')
        encoded = json.dumps(result)
        self.assertNotIn('SECRET', encoded)
        self.assertEqual(result['tools'], ['exec_command'])
        self.assertEqual(result['usage']['tool_calls'], 2)
        self.assertEqual(result['requested'], {'model': 'gpt-x', 'effort': 'high'})
        self.assertEqual(result['observed'], {'model': 'gpt-x', 'effort': 'high'})
        self.assertEqual(result['session_id'], 's1')
        self.assertEqual(result['invocation_id'], 'i1')

    def test_missing_and_mixed_context_are_null_with_diagnostic(self):
        self.write([{'type': 'session_meta', 'payload': {'id': 's'}},
                    {'type': 'turn_context', 'payload': {'model': 'a', 'effort': 'low'}},
                    {'type': 'turn_context', 'payload': {'model': 'b', 'effort': 'low'}}])
        result = capture.capture(self.path)
        self.assertEqual(result['observed'], {'model': None, 'effort': 'low'})
        self.assertIn('turn_context_missing_or_mixed', result['diagnostics'])
        self.write([{'type': 'session_meta', 'payload': {'id': 's'}}])
        result = capture.capture(self.path)
        self.assertEqual(result['observed'], {'model': None, 'effort': None})
        self.assertIn('turn_context_missing', result['diagnostics'])

    def test_token_usage_uses_last_cumulative_snapshot_not_sum(self):
        self.write([
            {'type': 'event_msg', 'payload': {'type': 'token_count', 'info': {'total_token_usage': {'input_tokens': 10, 'output_tokens': 2, 'total_tokens': 12}}}},
            {'type': 'event_msg', 'payload': {'type': 'token_count', 'info': {'total_token_usage': {'input_tokens': 15, 'cached_input_tokens': 3, 'cache_write_input_tokens': 2, 'output_tokens': 4, 'total_tokens': 19}}}},
        ])
        result = capture.capture(self.path)
        self.assertEqual(result['usage']['tokens'], {'input_tokens': 15, 'cached_input_tokens': 3,
                                                      'cache_write_input_tokens': 2, 'output_tokens': 4,
                                                      'reasoning_output_tokens': None})
        self.assertEqual(result['usage']['total_tokens'], 19)
        self.assertIsNone(result['usage']['cost'])
        self.assertIsNone(result['usage']['seconds'])

    def test_duplicate_keys_malformed_and_nonfinite_rejected(self):
        for content in ('{"type":"x","type":"y"}', '{bad}', '{"x":NaN}', '{"x":1e999}'):
            self.path.write_text(content + '\n', encoding='utf-8')
            with self.assertRaises(capture.RolloutError):
                capture.capture(self.path)

    def test_conflicting_session_metadata_is_null_and_diagnostic(self):
        self.write([{'type': 'session_meta', 'payload': {'id': 's1', 'cli_version': '1.0'}},
                    {'type': 'session_meta', 'payload': {'id': 's2', 'cli_version': '2.0'}}])
        result = capture.capture(self.path)
        self.assertIsNone(result['session_id'])
        self.assertIsNone(result['cli_version'])
        self.assertIn('session_id_conflict', result['diagnostics'])
        self.assertIn('cli_version_conflict', result['diagnostics'])


if __name__ == '__main__':
    unittest.main()
