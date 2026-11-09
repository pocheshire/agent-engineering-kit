#!/usr/bin/env python3
"""Offline staged disclosure. Integrity digests are not authentication or a sandbox."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat


class IsolationError(ValueError):
    pass


PHASES = ('public', 'objective', 'requirements', 'opaque', 'actions', 'final')
PIN_FIELDS = {'version', 'runtime', 'language', 'test_command', 'entrypoint'}
CODE_SUFFIXES = {'.py', '.js', '.ts', '.tsx', '.jsx', '.swift', '.rs', '.go', '.c', '.h', '.cpp', '.java', '.sh'}
FORBIDDEN = {'local.md', 'project.json', 'verification.md', 'report.md', 'review.md'}


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def fail(message):
    raise IsolationError(message)


def keys(value, required, optional=()):
    if not isinstance(value, dict) or set(value) - set(required) - set(optional) or set(required) - set(value):
        fail('Unknown or missing fields: ' + repr(value if not isinstance(value, dict) else sorted(value)))


def read_json(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                fail('Duplicate JSON field: ' + key)
            result[key] = value
        return result
    return json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=unique)


def relative(value):
    if not isinstance(value, str) or not value or '\\' in value or '\x00' in value:
        fail('Invalid relative path')
    p = PurePosixPath(value)
    if p.is_absolute() or str(p) != value or any(x in ('', '.', '..') or x.startswith('.') for x in value.split('/')):
        fail('Unsafe or hidden path: ' + value)
    return value


def hash_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regular(path):
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        fail('Expected regular, unlinked file: ' + str(path))


def validate_config(config):
    keys(config, ('snapshot_id', 'revision', 'files', 'private_roots'))
    if not all(isinstance(config[x], str) and config[x] for x in ('snapshot_id', 'revision')):
        fail('Snapshot identity and revision required')
    if not isinstance(config['files'], list) or not isinstance(config['private_roots'], list):
        fail('files/private_roots must be lists')
    names, hashes = set(), set()
    for item in config['files']:
        keys(item, ('path', 'sha256', 'phase', 'kind'), ('fields',))
        path = relative(item['path'])
        sha = item['sha256']
        if not isinstance(sha, str) or len(sha) != 64 or any(c not in '0123456789abcdef' for c in sha):
            fail('Invalid SHA256')
        if path.casefold() in names or sha in hashes:
            fail('Duplicate path/case or hash')
        names.add(path.casefold())
        hashes.add(sha)
        if item['phase'] not in PHASES:
            fail('Unknown phase')
        phase, kind = item['phase'], item['kind']
        if phase in ('public', 'objective'):
            if kind not in ('code', 'test', 'csv', 'pins'):
                fail('Public/objective content must be code/test/csv/pins')
            if PurePosixPath(path).name.casefold() in FORBIDDEN:
                fail('Generated narrative cannot enter objective/public view')
            if kind in ('code', 'test') and PurePosixPath(path).suffix.lower() not in CODE_SUFFIXES:
                fail('Code/test extension not allowlisted')
            if kind == 'csv' and PurePosixPath(path).suffix.lower() != '.csv':
                fail('Data must be CSV')
            if kind == 'pins':
                fields = item.get('fields')
                if PurePosixPath(path).suffix.lower() != '.json' or not isinstance(fields, list) or not fields or len(set(fields)) != len(fields) or not set(fields) <= PIN_FIELDS:
                    fail('Pins require explicit known fields')
        elif phase == 'requirements' and kind != 'trusted-requirement':
            fail('Requirements require separate trusted allowlist designation')
        elif phase == 'opaque' and kind != 'hash-only':
            fail('Opaque artifacts cannot expose content')
        elif phase in ('actions', 'final') and kind != 'raw':
            fail('Actions/final require raw kind')
        if kind != 'pins' and 'fields' in item:
            fail('Only pins support fields')
    for root in config['private_roots']:
        if not isinstance(root, str) or not Path(root).is_absolute():
            fail('Private deny roots must be explicit absolute paths')
    return config


def inspect_snapshot(snapshot, config):
    """Require exact inventory, reject links, hidden paths and case collisions."""
    snapshot = Path(snapshot)
    if snapshot.is_symlink() or not snapshot.is_dir():
        fail('Snapshot must be a real directory')
    # Reject symlinked ancestors as well as leaf symlinks.
    if snapshot.absolute() != snapshot.resolve():
        fail('Snapshot ancestors must be canonical')
    expected = {x['path']: x for x in config['files']}
    parents = {str(p) for name in expected for p in PurePosixPath(name).parents if str(p) != '.'}
    found = set()
    for base, directories, files in os.walk(str(snapshot), followlinks=False):
        for name in directories:
            path = Path(base) / name
            rel = path.relative_to(snapshot).as_posix()
            relative(rel)
            if path.is_symlink() or rel not in parents:
                fail('Unexpected directory: ' + rel)
        for name in files:
            path = Path(base) / name
            rel = path.relative_to(snapshot).as_posix()
            relative(rel)
            regular(path)
            if rel not in expected or hash_file(path) != expected[rel]['sha256']:
                fail('Unexpected or changed snapshot file: ' + rel)
            found.add(rel)
    if found != set(expected):
        fail('Missing snapshot files')


def write_json(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, sort_keys=True, indent=2)
        stream.write('\n')


def publish_directory(destination, populate):
    """Build privately; exclusive mkdir reserves destination; never replace output."""
    destination = Path(destination).absolute()
    if destination.parent.resolve() != destination.parent or destination.exists() or destination.is_symlink():
        fail('Output parent must be canonical; destination must not exist')
    # Staging is explicitly inside the output directory, never elsewhere.
    destination.mkdir(mode=0o700)
    try:
        populate(destination)
    except BaseException:
        shutil.rmtree(str(destination))
        raise


def copy_phase(snapshot, destination, config, phases):
    inspect_snapshot(snapshot, config)
    for item in config['files']:
        if item['phase'] not in phases:
            continue
        source = Path(snapshot) / item['path']
        target = destination / item['path']
        target.parent.mkdir(parents=True, exist_ok=True)
        # Recheck immediately before read; callers must hold snapshot immutable.
        regular(source)
        data = source.read_bytes()
        if hashlib.sha256(data).hexdigest() != item['sha256']:
            fail('Snapshot changed during copy')
        if item['kind'] == 'pins':
            obj = read_json(source)
            if not isinstance(obj, dict) or any(field not in obj for field in item['fields']):
                fail('Missing pin fields')
            selected = {field: obj[field] for field in item['fields']}
            if any(type(value) not in (str, int, float, bool, type(None)) for value in selected.values()):
                fail('Pin values must be scalar')
            data = canonical(selected) + b'\n'
        with target.open('xb') as stream:
            stream.write(data)


def prepare(snapshot, config, output, actor=False):
    config = validate_config(config)
    snapshot = Path(snapshot).absolute()
    output = Path(output).absolute()
    if snapshot == output or snapshot in output.parents or output in snapshot.parents:
        fail('Snapshot and output must be disjoint')
    inspect_snapshot(snapshot, config)
    mode = 'actor' if actor else 'evaluator'
    binding = digest({'config': config, 'mode': mode})
    manifest = {'schema': 1, 'binding': binding, 'mode': mode, 'snapshot': str(snapshot), 'config': config,
                'forbidden_disclosures': ['hidden criteria', 'credentials', 'unlisted files', 'narratives before actions'],
                'integrity_only': True}
    policy = {'schema': 1, 'binding': binding, 'status': 'requires-host-enforcement',
              'allowed_read_roots': [str(output / ('public' if actor else 'objective'))],
              'denied_read_roots': sorted(set([str(snapshot)] + config['private_roots'])),
              'future_read_roots': [] if actor else [str(output / 'actions'), str(output / 'final')],
              'deny_precedence_required': True, 'default_read': 'deny'}
    def populate(dest):
        write_json(dest / 'manifest.json', manifest)
        write_json(dest / 'host-policy.json', policy)
        phase = 'public' if actor else 'objective'
        publish_directory(dest / phase, lambda view: copy_phase(snapshot, view, config, (phase,) if actor else ('public', 'objective', 'requirements')))
    publish_directory(output, populate)
    return manifest


def load(output):
    output = Path(output).absolute()
    if output.resolve() != output:
        fail('Output must be canonical')
    regular(output / 'manifest.json')
    manifest = read_json(output / 'manifest.json')
    keys(manifest, ('schema', 'binding', 'mode', 'snapshot', 'config', 'forbidden_disclosures', 'integrity_only'))
    validate_config(manifest['config'])
    if manifest['schema'] != 1 or manifest['mode'] not in ('actor', 'evaluator') or manifest['integrity_only'] is not True:
        fail('Invalid manifest schema or mode')
    if manifest['binding'] != digest({'config': manifest['config'], 'mode': manifest['mode']}):
        fail('Manifest binding mismatch')
    inspect_snapshot(manifest['snapshot'], manifest['config'])
    return output, manifest


def tree_hash(root):
    root = Path(root)
    if not root.is_dir() or root.is_symlink():
        fail('Required view does not exist')
    items = []
    for path in sorted(root.rglob('*')):
        if path.is_symlink():
            fail('View contains symlink')
        if path.is_file():
            regular(path)
            items.append([path.relative_to(root).as_posix(), hash_file(path)])
    return digest(items)


def record_receipt(output, receipt, inspected=False):
    """Trusted operator/harness call, never an actor/evaluator self-seal."""
    output, manifest = load(output)
    if manifest['mode'] != 'evaluator':
        fail('Actor bundle has no evaluator stages')
    kind = 'action-inspection' if inspected else 'objective-verdict'
    keys(receipt, ('kind', 'binding', 'view_sha256', 'authority', 'result'))
    if receipt['kind'] != kind or receipt['binding'] != manifest['binding'] or receipt['authority'] not in ('operator', 'harness') or not isinstance(receipt['result'], str) or not receipt['result']:
        fail('Invalid authority, result, kind or binding')
    stage = 'actions' if inspected else 'objective'
    if inspected:
        verify_receipt(output, manifest, False)
    elif (output / 'actions').exists() or (output / 'final').exists():
        fail('Verdict cannot be recorded after disclosure')
    if receipt['view_sha256'] != tree_hash(output / stage):
        fail('Receipt view mismatch')
    write_json(output / (kind + '.json'), receipt)


def verify_receipt(output, manifest, inspected):
    kind = 'action-inspection' if inspected else 'objective-verdict'
    receipt = read_json(output / (kind + '.json'))
    keys(receipt, ('kind', 'binding', 'view_sha256', 'authority', 'result'))
    if receipt['kind'] != kind or receipt['binding'] != manifest['binding'] or receipt['authority'] not in ('operator', 'harness') or not receipt['result'] or receipt['view_sha256'] != tree_hash(output / ('actions' if inspected else 'objective')):
        fail('Stored receipt mismatch')
    return receipt


def unlock(output, final=False):
    output, manifest = load(output)
    if manifest['mode'] != 'evaluator':
        fail('Actor bundle cannot unlock')
    verify_receipt(output, manifest, False)
    if final:
        verify_receipt(output, manifest, True)
    stage = 'final' if final else 'actions'
    publish_directory(output / stage, lambda view: copy_phase(manifest['snapshot'], view, manifest['config'], (stage,)))


def readiness(output, receipt=None):
    output, manifest = load(output)
    policy = read_json(output / 'host-policy.json')
    expected_allowed = [str(output / ('public' if manifest['mode'] == 'actor' else 'objective'))]
    policy_matches = (policy.get('binding') == manifest['binding'] and policy.get('schema') == 1
                      and policy.get('allowed_read_roots') == expected_allowed
                      and policy.get('denied_read_roots') == sorted(set([manifest['snapshot']] + manifest['config']['private_roots']))
                      and policy.get('default_read') == 'deny' and policy.get('deny_precedence_required') is True
                      and policy.get('future_read_roots') == ([] if manifest['mode'] == 'actor' else [str(output / 'actions'), str(output / 'final')]))
    result = {'staged_disclosure': True, 'host_isolation_verified': False, 'ready': False,
              'policy_sha256': digest(policy), 'binding': manifest['binding']}
    if receipt is not None:
        keys(receipt, ('binding', 'policy_sha256', 'provenance', 'enforcement', 'negative_canary', 'allowed_root_check'))
        verified = (policy_matches and receipt['binding'] == manifest['binding'] and receipt['policy_sha256'] == digest(policy)
                    and policy.get('status') == 'requires-host-enforcement'
                    and isinstance(receipt['provenance'], str) and receipt['provenance'].strip().lower() not in ('', 'unknown', 'failed')
                    and receipt['enforcement'] == 'passed' and receipt['negative_canary'] == 'denied'
                    and receipt['allowed_root_check'] == 'passed')
        result['host_isolation_verified'] = verified
        result['ready'] = verified
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for command in ('prepare', 'actor'):
        p = sub.add_parser(command)
        p.add_argument('--snapshot', required=True)
        p.add_argument('--config', required=True)
        p.add_argument('--output', required=True)
    for command in ('verdict', 'inspected', 'unlock-actions', 'unlock-final', 'readiness'):
        p = sub.add_parser(command)
        p.add_argument('--output', required=True)
        if command in ('verdict', 'inspected', 'readiness'):
            p.add_argument('--receipt', required=command != 'readiness')
    args = parser.parse_args(argv)
    try:
        if args.command in ('prepare', 'actor'):
            result = prepare(args.snapshot, read_json(args.config), args.output, args.command == 'actor')
        elif args.command in ('verdict', 'inspected'):
            result = record_receipt(args.output, read_json(args.receipt), args.command == 'inspected')
        elif args.command.startswith('unlock-'):
            result = unlock(args.output, args.command == 'unlock-final')
        else:
            result = readiness(args.output, read_json(args.receipt) if args.receipt else None)
        print(json.dumps(result, sort_keys=True))
    except (IsolationError, OSError, ValueError) as error:
        parser.exit(2, 'eval-views: ' + str(error) + '\n')


if __name__ == '__main__':
    main()
