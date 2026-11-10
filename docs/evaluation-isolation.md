# Staged evaluator disclosure

`scripts/eval_views.py` is an offline Python 3.9+ helper with no dependencies.
It constructs physical views from a separately prepared immutable snapshot. It
never runs a performer, starts a server, modifies inputs, installs a host policy,
or authenticates a receipt. Copying files is **not OS isolation**.

The trusted operator/harness owns the snapshot, configuration, output control
files and receipt commands. The performer must not be able to call those commands
or write those files. Evaluators get only the permitted view directory, never the
output parent, source snapshot, receipts or private evaluation material. These
boundaries require actual host enforcement. A digest detects inconsistent bytes;
it does not prove who supplied them. A writable control directory lets an attacker
replace receipts, rewrite the configuration or delete history. This helper cannot
prevent a privileged owner from doing that.

The current manifest schema stores trusted hashes for the actual projected
`objective` view and the derived `actions` and `final` views. These hashes are
computed from immutable snapshot bytes during preparation, using the same pin
filtering and serialization as copying. The control manifest stays unchanged as
stages are disclosed. Legacy in-flight schema-1 outputs have no prepared-view
anchors and fail closed with instructions to re-prepare from the immutable
snapshot; do not add hashes to an old view after it may have been modified.

## Input contract

Construct a narrow snapshot independently from the performer. Do not pass the
whole project directory. Inventory is exact: every file must occur once in the
configuration; unexpected files, empty/unlisted directories, hidden paths,
case-colliding paths, traversal, symlinks and multiply linked files fail closed.
All snapshot ancestors must be canonical. The harness must prevent concurrent
snapshot changes; hash checks before stages detect changes but are not a defense
against a hostile process racing file reads. Snapshot identity and source revision
are explicit pinned assertions from the trusted harness, not inferred Git facts.

An example configuration follows. Replace placeholders with SHA256 of source
bytes. Each hash must be unique; identical artifacts require deduplication before
snapshot construction. Unknown configuration/item fields are rejected. JSON input
with duplicate keys is rejected.

```json
{
  "snapshot_id": "run-001-immutable",
  "revision": "source-commit-id",
  "private_roots": ["/absolute/evaluator-private"],
  "files": [
    {"path": "src/app.py", "sha256": "<64 lowercase hex>", "phase": "public", "kind": "code"},
    {"path": "tests/test_app.py", "sha256": "<64 lowercase hex>", "phase": "objective", "kind": "test"},
    {"path": "pins.json", "sha256": "<64 lowercase hex>", "phase": "objective", "kind": "pins", "fields": ["version", "runtime"]},
    {"path": "original-requirements.md", "sha256": "<64 lowercase hex>", "phase": "requirements", "kind": "trusted-requirement"},
    {"path": "local.md", "sha256": "<64 lowercase hex>", "phase": "opaque", "kind": "hash-only"},
    {"path": "actions.log", "sha256": "<64 lowercase hex>", "phase": "actions", "kind": "raw"},
    {"path": "final.md", "sha256": "<64 lowercase hex>", "phase": "final", "kind": "raw"}
  ]
}
```

`public` is the explicit actor input allowlist. Hidden expected criteria, rubrics
and credentials must never be public inputs or appear in their code/data. They
belong outside the snapshot in `private_roots`; this helper cannot classify secrets
inside intentionally allowlisted source code. An actor bundle exposes only its
`public/` child. Its parent manifest is trusted control material, not actor input.
Actor bundles cannot unlock evaluator stages.

The evaluator objective view includes `public`, `objective` and separately trusted
`requirements` files. `objective` permits actual code/tests (fixed extension allowlist), CSV data, and
selected scalar JSON pins. Known pin names are `version`, `runtime`, `language`,
`test_command`, `entrypoint`; unknown source JSON fields are excluded from copied
pins, and unsupported selected fields are rejected. Full `project.json` is
forbidden in public/objective views. Markdown, README prose and generated
`local.md`, verification/review/report narratives cannot enter those views.
Extensions do not prove provenance: the harness must verify that allowlisted code,
tests and data are actual artifacts rather than disguised narrator instructions.

`requirements` is a separate explicit trusted allowlist. Use it only for original
authoritative requirements whose provenance and exact hashes were independently
checked. It deliberately permits original prose and therefore must never be
populated from a performer's rewritten requirements. `opaque` records source
hashes but never copies content at any stage. Actions and final materials require
explicit complete allowlists; the harness checks completeness and separates raw
commands/tool results from self-assessment. The helper cannot reconstruct missing
raw action records or establish completeness from a performer's assertions.

## Operator sequence

All output paths must be new, disjoint from the snapshot, with a canonical existing
parent. Exclusive directory/file creation refuses existing destinations. Failed
construction removes its own partial output. No source files, hidden files or
extra reports are copied implicitly. All writes occur inside the explicit output
directory. Publish access to a phase only after its command has completed; creation
is exclusive, not a transaction safe for concurrent readers.

```sh
python3 -B scripts/eval_views.py actor --snapshot /snapshot --config /control/config.json --output /control/actor-run
python3 -B scripts/eval_views.py prepare --snapshot /snapshot --config /control/config.json --output /control/evaluator-run
python3 -B scripts/eval_views.py verdict --output /control/evaluator-run --receipt /control/verdict.json
python3 -B scripts/eval_views.py unlock-actions --output /control/evaluator-run
python3 -B scripts/eval_views.py inspected --output /control/evaluator-run --receipt /control/inspection.json
python3 -B scripts/eval_views.py unlock-final --output /control/evaluator-run
```

The objective evaluator must record its verdict before seeing raw actions. An
operator/harness stores that verdict using the explicit `verdict` command. Only
then can `unlock-actions` copy the complete permitted raw action set. The evaluator
inspects those actions before the harness stores an inspection receipt, after
which `unlock-final` copies permitted final answers and self-assessment. Neither
later phase exists at preparation time. Repeated stage creation is rejected;
removing a verdict after actions exist cannot authorize a fresh early verdict.
Input hashes and stored receipts are rechecked at each transition. Tampered views,
wrong snapshot bindings and missing receipts prevent unlocking. The actual
objective projection is checked before the verdict receipt and again before
actions can be unlocked. The actions projection is checked before its inspection
receipt and again before final disclosure. New stage directories are created
exclusively and checked against their precomputed projection hash before the
command completes; a failed copy removes only the directory created by that
command. A changed view requires a fresh run from the immutable snapshot.

Verdict receipt schema (inspection uses `action-inspection` and the actions view
hash):

```json
{
  "kind": "objective-verdict",
  "binding": "<manifest binding>",
  "view_sha256": "<tree_hash(objective directory)>",
  "authority": "harness",
  "result": "Recorded objective observations and verdict"
}
```

`authority` is `operator` or `harness`. This declaration is not proof of authority:
the host must enforce who can invoke receipt creation and who can mutate its
output. `tree_hash()` and the importable `prepare()`, `record_receipt()`, `unlock()`
and `readiness()` functions use the same logic as the CLI. A performer must never
self-issue an early verdict or an inspection receipt.

## Host enforcement and readiness

`host-policy.json` is a **portable policy description**, not native Codex settings.
It contains an initial allowed read root, explicit denied snapshot/private roots,
future evaluator stage roots, default-deny intent, required deny precedence, and
binding. It invents no platform configuration keys. The host adapter must use its
official supported controls, preserve required runtime access separately, and
check that the effective policy excludes all private/source/control paths. Future
roots are not current permissions: activate them in order only after successful
stage transitions, then repeat enforcement probes for the changed permission set.
Never expose the policy/control parent just to make it convenient to read the
manifest.

Before claiming isolation, execute a real negative canary attempt using the exact
actor/evaluator host identity and a positive allowed-root read. A canary secret in
a denied private file must be unreadable through the available host tools. Record
the actual enforcement mechanism and observable attempt/output reference. A host
adapter must produce this receipt only from those observations:

```json
{
  "binding": "<manifest binding>",
  "policy_sha256": "<canonical JSON policy digest>",
  "provenance": "<actual host configuration and probe evidence reference>",
  "enforcement": "passed",
  "negative_canary": "denied",
  "allowed_root_check": "passed"
}
```

```sh
python3 -B scripts/eval_views.py readiness --output /control/evaluator-run --receipt /control/host-receipt.json
```

Readiness always distinguishes `staged_disclosure` from
`host_isolation_verified`. Missing receipt, mismatched digest/binding, unknown
provenance or failed probes leave `ready` false. A matching trusted receipt is
necessary for the latter claim; the helper does not execute or independently
validate the referenced host evidence. A fabricated receipt is not verification.
Tests exercise receipt validation with synthetic fixtures and **do not establish
host isolation**. A native adapter and actual host negative-smoke evidence must be
reported separately from these tests and static catalog validation.

Run local behavioral checks with:

```sh
python3 -B -m unittest discover -s tests -p test_eval_views.py -v
```
