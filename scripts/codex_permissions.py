#!/usr/bin/env python3
"""Render an eval_views host-policy as an offline Codex permission profile."""
import argparse
import json
import ntpath
import os
from pathlib import Path, PureWindowsPath
import re
import sys
import unicodedata


class PolicyError(ValueError):
    pass


def fail(message):
    raise PolicyError(message)


def _keys(obj, expected, label):
    if not isinstance(obj, dict) or set(obj) != set(expected):
        fail('Invalid {} fields'.format(label))


def _path(value, label, must_exist=False):
    if not isinstance(value, str) or not value:
        fail('{} must be an absolute path'.format(label))
    if any(unicodedata.category(char) == 'Cc' for char in value):
        fail('{} contains a control character'.format(label))
    windows = PureWindowsPath(value)
    is_windows = os.name == 'nt' and bool(windows.drive or value.startswith('\\\\'))
    path = Path(value)
    if not path.is_absolute():
        fail('{} must be an absolute path'.format(label))
    normalized = ntpath.normpath(value) if is_windows else os.path.normpath(value)
    canonical = normalized == value and (is_windows or os.path.abspath(value) == value)
    if not is_windows and os.name != 'nt' and value.startswith('//'):
        canonical = False
    parts = windows.parts if is_windows else path.parts
    if any(part in ('.', '..') for part in parts) or not canonical:
        fail('{} must be canonical and contain no dot segments'.format(label))
    for probe in reversed(path.parents):
        if probe.is_symlink():
            fail('{} traverses a symlink'.format(label))
    if path.is_symlink():
        fail('{} traverses a symlink'.format(label))
    if must_exist and (not path.is_dir() or path.is_symlink()):
        fail('{} must be an existing directory'.format(label))
    return value


def _overlap(a, b):
    # Reject case-only aliases even on case-sensitive hosts: the same policy
    # may later be consumed by a case-insensitive filesystem.
    left = os.path.normpath(a).casefold()
    right = os.path.normpath(b).casefold()
    windows = os.name == 'nt' and bool(PureWindowsPath(left).drive or PureWindowsPath(right).drive)
    path_type = PureWindowsPath if windows else Path
    left_path, right_path = path_type(left), path_type(right)
    if left_path == right_path or left_path in right_path.parents or right_path in left_path.parents:
        return True
    # Resolve existing components while preserving missing suffixes. This
    # covers symlink/junction aliases and future roots whose leaf is absent.
    real_left, real_right = os.path.realpath(a), os.path.realpath(b)
    real_left, real_right = os.path.normcase(real_left), os.path.normcase(real_right)
    left_real_path, right_real_path = Path(real_left), Path(real_right)
    if (left_real_path == right_real_path or left_real_path in right_real_path.parents
            or right_real_path in left_real_path.parents):
        return True

    # Also compare existing directory identities for aliases such as mount
    # points. Relative tails distinguish overlapping roots from sibling paths.
    identities = []
    for value in (a, b):
        path = Path(value)
        entries = []
        for ancestor in (path, *path.parents):
            try:
                stat = ancestor.stat()
            except OSError:
                continue
            if os.path.isdir(ancestor):
                tail = tuple(os.path.normcase(part) for part in path.relative_to(ancestor).parts)
                entries.append(((stat.st_dev, stat.st_ino), tail))
        identities.append(entries)
    for left_id, left_tail in identities[0]:
        for right_id, right_tail in identities[1]:
            if left_id == right_id and (left_tail[:len(right_tail)] == right_tail
                                        or right_tail[:len(left_tail)] == left_tail):
                return True
    return False


def validate(policy):
    fields = ('schema', 'binding', 'allowed_read_roots', 'denied_read_roots',
              'future_read_roots', 'default_read', 'deny_precedence_required', 'status')
    _keys(policy, fields, 'policy')
    if type(policy['schema']) is not int or policy['schema'] != 1:
        fail('Unsupported policy schema')
    if not isinstance(policy['binding'], str) or not re.fullmatch(r'[0-9a-f]{64}', policy['binding']):
        fail('Invalid binding')
    if policy['default_read'] != 'deny' or policy['deny_precedence_required'] is not True:
        fail('Policy must require default deny and deny precedence')
    if policy['status'] != 'requires-host-enforcement':
        fail('Policy is not awaiting host enforcement')
    for key in ('allowed_read_roots', 'denied_read_roots', 'future_read_roots'):
        roots = policy[key]
        if not isinstance(roots, list) or (key != 'future_read_roots' and not roots) or any(not isinstance(root, str) for root in roots):
            fail('{} must be a path list'.format(key))
        normalized = [_path(root, key, must_exist=(key == 'allowed_read_roots')) for root in roots]
        if normalized != sorted(set(normalized)):
            fail('{} must be sorted and unique'.format(key))
        policy[key] = normalized
    if not policy['denied_read_roots']:
        fail('At least one denied root is required')
    for allowed in policy['allowed_read_roots']:
        if any(_overlap(allowed, denied) for denied in policy['denied_read_roots']):
            fail('Allowed root overlaps a denied root')
        if any(_overlap(allowed, future) for future in policy['future_read_roots']):
            fail('Allowed root overlaps a future root')
    for future in policy['future_read_roots']:
        if any(_overlap(future, denied) for denied in policy['denied_read_roots']):
            fail('Future root overlaps a denied root')
    for index, future in enumerate(policy['future_read_roots']):
        if any(_overlap(future, other) for other in policy['future_read_roots'][index + 1:]):
            fail('Future roots overlap')
    return policy


def render(policy, stage='initial', write_view=False, operator_unlocked=False):
    policy = validate(dict(policy))
    if stage not in ('initial', 'actions', 'final'):
        fail('Unsupported stage')
    if stage != 'initial' and not operator_unlocked:
        fail('Later-stage permissions require an explicit operator unlock')
    roots = list(policy['allowed_read_roots'])
    if stage != 'initial':
        selected = [p for p in policy['future_read_roots'] if Path(p).name == stage]
        if len(selected) != 1:
            fail('Policy does not identify exactly one {} stage root'.format(stage))
        _path(selected[0], 'selected future root', must_exist=True)
        roots.append(selected[0])
    permission = 'write' if write_view else 'read'
    lines = [
        'default_permissions = "aek-eval"',
        '',
        '[permissions.aek-eval]',
        '[permissions.aek-eval.filesystem]',
        '":root" = "deny"',
        '":minimal" = "read"',
        '":tmpdir" = "deny"',
        '":slash_tmp" = "deny"',
    ]
    for path in sorted(set(policy['denied_read_roots'])):
        lines.append('{} = "deny"'.format(json.dumps(path, ensure_ascii=False)))
    for path in sorted(set(roots)):
        lines.append('{} = "{}"'.format(json.dumps(path, ensure_ascii=False), permission))
        if write_view:
            for protected in ('.git', '.agents', '.codex', '.aws'):
                child = str(Path(path) / protected)
                lines.append('{} = "read"'.format(json.dumps(child, ensure_ascii=False)))
    lines.extend(['', '[permissions.aek-eval.network]', 'enabled = false'])
    return '\n'.join(lines) + '\n'


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            fail('Duplicate JSON key')
        result[key] = value
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--policy', required=True, help='host-policy.json produced by eval_views.py')
    parser.add_argument('--stage', choices=('initial', 'actions', 'final'), default='initial')
    parser.add_argument('--write-view', action='store_true', help='grant write access to allowed view roots')
    parser.add_argument('--operator-unlocked', action='store_true', help='operator assertion required for actions/final stages')
    args = parser.parse_args(argv)
    try:
        path = Path(args.policy)
        if path.is_symlink() or not path.is_file():
            fail('Policy file must be a regular non-symlink file')
        with path.open('r', encoding='utf-8') as stream:
            policy = json.load(stream, object_pairs_hook=_unique_object)
        sys.stdout.write(render(policy, args.stage, args.write_view, args.operator_unlocked))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print('codex_permissions: {}'.format(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
