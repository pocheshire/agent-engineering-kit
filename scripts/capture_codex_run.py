#!/usr/bin/env python3
"""Produce a privacy-preserving summary of a Codex JSONL rollout."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys


class RolloutError(ValueError):
    pass


def _unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise RolloutError('duplicate JSON key')
        result[key] = value
    return result


def _reject_constant(_value):
    raise RolloutError('non-finite JSON number')


def _finite_float(value):
    number = float(value)
    if not math.isfinite(number):
        raise RolloutError('non-finite JSON number')
    return number


def _load(line):
    try:
        value = json.loads(line, object_pairs_hook=_unique, parse_constant=_reject_constant,
                           parse_float=_finite_float)
    except (ValueError, TypeError) as exc:
        raise RolloutError('malformed JSONL record') from exc
    if not isinstance(value, dict):
        raise RolloutError('JSONL records must be objects')
    return value


def _payload(record):
    value = record.get('payload')
    return value if isinstance(value, dict) else {}


def _safe_text(value):
    # These fields are metadata, but constrain them to prevent arbitrary payloads
    # from being copied into the report.
    if isinstance(value, str) and 0 < len(value) <= 160 and all(c.isprintable() for c in value):
        return value
    return None


def _nonnegative_int(value):
    return value if isinstance(value, int) and not isinstance(value, bool) and value >= 0 else None


def capture(path, requested_model=None, requested_effort=None):
    raw = Path(path).read_bytes()
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise RolloutError('rollout must be UTF-8') from exc

    contexts = []
    meta = {'session_id': set(), 'invocation_id': set(), 'cli_version': set()}
    tools, calls = set(), 0
    last_usage = None
    last_total_tokens = None
    for line in text.splitlines():
        if not line.strip():
            continue
        record = _load(line)
        kind = record.get('type')
        payload = _payload(record)
        if kind == 'session_meta':
            for key, aliases in (('session_id', ('id', 'session_id')),
                                 ('invocation_id', ('invocation_id',)),
                                 ('cli_version', ('cli_version', 'version'))):
                for alias in aliases:
                    if alias in payload:
                        safe_value = _safe_text(payload[alias])
                        if safe_value is not None:
                            meta[key].add(safe_value)
        elif kind == 'turn_context':
            contexts.append((payload.get('model'), payload.get('effort')))
        elif kind == 'response_item':
            call_type = payload.get('type')
            if call_type in ('function_call', 'custom_tool_call'):
                calls += 1
                name = _safe_text(payload.get('name'))
                if name:
                    tools.add(name)
        elif kind == 'event_msg' and payload.get('type') == 'token_count':
            info = payload.get('info')
            total = info.get('total_token_usage') if isinstance(info, dict) else None
            if isinstance(total, dict):
                last_usage = {key: _nonnegative_int(total.get(key)) for key in
                              ('input_tokens', 'cached_input_tokens', 'cache_write_input_tokens',
                               'output_tokens', 'reasoning_output_tokens')}
                last_total_tokens = _nonnegative_int(total.get('total_tokens'))

    def observed(index):
        vals = [_safe_text(row[index]) for row in contexts]
        if not vals:
            return None
        if any(v is None for v in vals) or len(set(vals)) != 1:
            return None
        return vals[0]

    model, effort = observed(0), observed(1)
    diagnostics = []
    if not contexts:
        diagnostics.append('turn_context_missing')
    elif model is None or effort is None:
        diagnostics.append('turn_context_missing_or_mixed')
    for key in ('session_id', 'invocation_id', 'cli_version'):
        if len(meta[key]) > 1:
            diagnostics.append(key + '_conflict')

    def one_meta(key):
        return next(iter(meta[key])) if len(meta[key]) == 1 else None

    return {
        'kind': 'codex_observation', 'schema': 1,
        'rollout_sha256': hashlib.sha256(raw).hexdigest(),
        'session_id': one_meta('session_id'),
        'invocation_id': one_meta('invocation_id'),
        'cli_version': one_meta('cli_version'),
        'observed': {'model': model, 'effort': effort},
        'requested': {'model': _safe_text(requested_model), 'effort': _safe_text(requested_effort)},
        'tools': sorted(tools),
        'usage': {'tokens': last_usage, 'total_tokens': last_total_tokens if last_usage is not None else None,
                  'tool_calls': calls, 'cost': None, 'seconds': None},
        'diagnostics': diagnostics,
        'limits': ['Rollout metadata may be incomplete; no messages, reasoning, environment, or credentials are emitted.',
                   'Token totals are the last cumulative snapshot present; price and elapsed time are not inferred.'],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('rollout', help='Codex rollout JSONL file')
    parser.add_argument('--requested-model')
    parser.add_argument('--requested-effort')
    args = parser.parse_args(argv)
    try:
        result = capture(args.rollout, args.requested_model, args.requested_effort)
    except (OSError, RolloutError) as exc:
        print('capture_codex_run: ' + str(exc), file=sys.stderr)
        return 2
    json.dump(result, sys.stdout, sort_keys=True, allow_nan=False)
    sys.stdout.write('\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
