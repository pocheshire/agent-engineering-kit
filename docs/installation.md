# Installation, upgrade and recovery

Let your agent open START_HERE.md and supply the target project. The installer is
an implementation detail; users can request setup in ordinary language.

## Vendored

```sh
python3 skills/agent-engineering-kit/core/aek.py install /path/to/project --mode adopt --strategy vendored
```

Use `--mode initialize` for an empty/new project. This installs instructions only.
It appends a managed block to AGENTS.md, stores a pinned runtime and baseline
hashes in .aek, and creates user-owned .aek/project.json and .aek/local.md. Inspect
the diff. The agent must fill discovered facts and review semantic conflicts;
a successful copy is not a completed architecture or product audit.

Repeat the same command safely. It must stop if it encounters conflicting managed
content. The original prose in AGENTS.md and local adaptations are retained.

## Linked

Keep the KIT in a stable relative layout, for example sibling directories:

```sh
python3 agent-engineering-kit/skills/agent-engineering-kit/core/aek.py install project --mode adopt --strategy linked --source ../agent-engineering-kit/skills/agent-engineering-kit/core
```

The source is relative to the target project, not to the shell working directory.
Absolute machine paths are rejected. Hashes and version pin the source. Moving the
project alone or editing the shared source can invalidate it. Use vendored when
the layout cannot be guaranteed. Review dependency availability before adoption.

## Audit and upgrade

```sh
python3 skills/agent-engineering-kit/core/aek.py audit /path/to/project
python3 skills/agent-engineering-kit/core/aek.py upgrade /path/to/project
```

First explicitly obtain a trusted newer KIT. Run Upgrade from its core. For linked
installs pass `--source` with the intended new relative source if it moved. Upgrade
compares old baseline, current runtime and incoming runtime. If both changed the
same managed file differently, it fails without writing. Resolve the actual diff
manually; never delete state or force-install to conceal adaptations.

If the KIT is unavailable, a vendored project still has .aek/runtime. For linked
projects restore the pinned layout/version from your trusted release, or analyze
an intentional migration. Never silently use an unrelated installation.

`aek.py uninstall TARGET` removes unchanged managed files and its AGENTS marker.
User-owned adaptations remain. Removal refuses modified managed content.

## Verification categories

Static audit checks integrity and availability. The agent separately reviews real
commands, authority, routes, consumers and evidence. Product tests remain project
specific. Evidence supplied to `check-evidence` is a consistency check of a report,
not proof that a command executed; preserve the raw logs and revision too.

For global skills and native plugin mechanisms, see [platforms](platforms.md).
