# Codex permission profile adapter

`scripts/codex_permissions.py` is an offline Python 3.9+ adapter from the
portable `host-policy.json` emitted by `eval_views.py` to a TOML permission
profile. It prints TOML to stdout only. It does not install or modify Codex
configuration, launch a process, access a network, or establish isolation.

The input policy is treated as untrusted data. The adapter requires the exact
schema-1 host-policy fields, `requires-host-enforcement` status, a SHA256 binding,
default deny, and required deny precedence. Roots must be absolute canonical
paths with no dot segments or symlinked existing path components. The allowed
view root must exist as a directory. At least one allowed and denied root is
required. Allowed roots may not overlap a denied or future root; future roots
may not overlap denied roots. Overlap checks fold path case on all platforms,
so case-only aliases are conservatively rejected even on case-sensitive hosts.
Control characters in paths are rejected. Keep all private material outside allowed trees.
Avoid broad denied roots such as `/usr` because Codex needs runtime files there.

Generate the initial actor profile (read-only by default):

```sh
python3 -B scripts/codex_permissions.py --policy /control/actor-run/host-policy.json
```

For an explicitly writable actor view, add `--write-view`; only the listed
allowed view root changes from `read` to `write`. Denied roots remain denied.
This narrow profile is built without inheriting `:workspace`: that built-in can
grant the current workspace write access and defeat an exclusive-view boundary.
It denies `:root`, restores only `:minimal` runtime reads, denies temporary
directories, and grants only explicit view roots. Network access is disabled.
In write mode, `.git`, `.agents`, `.codex`, and `.aws` beneath each allowed root
remain read-only.
Use a separate Codex home/config stack for this profile so the ordinary user
profile and unrelated projects are unaffected. Merge the emitted TOML into that
isolated config; do not combine it with legacy `sandbox_mode`,
`sandbox_workspace_write`, or a `codex exec --sandbox` setting. Permission profiles
are selected by `default_permissions`; `codex sandbox -P aek-eval -C VIEW
--log-denials -- COMMAND` is the native command form shown by local CLI help.
CLI/config support can vary by version; check the installed CLI help and verify
effective behavior before use.

Evaluator policies list future `actions` and `final` paths, but the initial
profile grants neither. After the trusted operator completes the required stage
transition and explicitly unlocks that phase, render only that stage:

```sh
python3 -B scripts/codex_permissions.py --policy /control/evaluator-run/host-policy.json --stage actions --operator-unlocked
python3 -B scripts/codex_permissions.py --policy /control/evaluator-run/host-policy.json --stage final --operator-unlocked
```

`--operator-unlocked` is an operator assertion, not cryptographic proof or an
authorization mechanism. The adapter has no receipt integration and does not
validate stage receipts. Only the trusted harness/operator may invoke it for a
later phase, after checking the corresponding receipt independently. Re-run the
host negative and positive canaries after every profile change. Do not use an
agent self-claim as evidence that a denied read was blocked. See the official
[Codex permission profile documentation](https://learn.chatgpt.com/docs/permissions)
for path rules, precedence, and runtime limitations. A selected future root must
exist as a canonical directory before the adapter grants it.
