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
The managed block is appended after the original bytes; an untracked AGENTS.md
need not be committed. An explicit whole-file immutability rule needs a scoped
owner decision. Do not patch the installer, omit its entry block or substitute a
README link to bypass that rule; such a result is not a valid installation.

## Linked

Keep the KIT in a stable relative layout, for example sibling directories:

```sh
python3 agent-engineering-kit/skills/agent-engineering-kit/core/aek.py install project --mode adopt --strategy linked --source ../agent-engineering-kit/skills/agent-engineering-kit/core
```

The source is relative to the target project, not to the shell working directory.
Absolute machine paths are rejected. Hashes and version pin the source. Moving the
project alone or editing the shared source can invalidate it. Use vendored when
the layout cannot be guaranteed. Review dependency availability before adoption.
The source may be outside the project; relative does not mean contained. Local
filesystem isolation still applies. Linking adds project metadata and pointers,
so it cannot bypass a ban on all external reads or imported instructions.

Before calling a clean-room rule a conflict, distinguish product code and
dependencies from engineering tooling and filesystem access. Vendoring includes
MIT instructions and a Python helper. An explicit broad ban still applies; the
agent must describe the exact restricted action and ask only for a needed scoped
exception. It must preserve the project's product-source isolation.

## Audit and upgrade

```sh
python3 skills/agent-engineering-kit/core/aek.py audit /path/to/project
python3 skills/agent-engineering-kit/core/aek.py upgrade /path/to/project
```

Audit works as an agent review even before installation. The CLI's integrity
check reports “AEK is not installed”; the agent then assesses existing workflows
against the loaded KIT and reports strengths, gaps and adoption prerequisites.
No installation is performed. “Not installed” alone does not mean incompatible;
file-based findings also do not prove that product tests ran.

First explicitly obtain a trusted newer KIT. Run Upgrade from its core. For linked
installs pass `--source` with the intended new relative source if it moved. Upgrade
compares old baseline, current runtime and incoming runtime. Vendored installs
keep a non-overlapping project-local runtime edit while applying the new snapshot.
Linked installs share a relative source: before switching sources, Upgrade stops
without writes if the old source has a local edit that the incoming source does
not contain, even when the release changed only VERSION. This protects a shared
checkout and its users. Keep the old pin until the change is resolved. Review the
old-to-new diff, then represent an intended project-specific change as an explicit
project adaptation, or carry it into an owner-controlled copy of the new release;
verify that copy and retry with its relative path as `--source`. Do not edit a
shared source or state just to bypass the conflict.
Upgrade also rejects downgrades, changed bytes under equal version precedence,
and unsupported adaptation schemas.

When an older installation upgrades to 0.3.0-rc.1 or later, Upgrade replaces
the exact legacy AEK block in AGENTS.md as part of the same transaction as the
pin update. The new block tells the agent to open the AEK workflow before
inspecting the implementation. The surrounding owner text and ordinary file
permissions are preserved. An edited or ambiguous block stops the upgrade
before any writes.

A major version transition additionally needs an authorized reviewed migration
and explicit `--allow-major`; the flag does not grant permission. Resolve the actual diff
manually; never delete state or force-install to conceal adaptations.

A preserved local runtime edit can make the static baseline audit fail after a
successful non-overlapping update. That result is intentional: the edit remains
local and unverified against upstream. Do not rewrite its hash to manufacture a
pass. Review/reconcile the adaptation separately.

## Recover unavailable instructions

Tell the agent what stopped working and where your trusted local copy is. No new
product decisions or version change are implied. If no verified source is
available, the agent asks for its location and leaves the project untouched.

Run the verifier from the current complete reviewed KIT, never a damaged runtime's aek.py.
An older pinned release is recovery data for `--source`; do not substitute its older
maintenance procedure for the currently loaded KIT's verifier.
The recovery source is relative to the target project:

```sh
python3 skills/agent-engineering-kit/core/aek.py restore /path/to/project --source ../trusted-aek/skills/agent-engineering-kit/core
```

Its version and entire file/hash manifest must match the installed pin. Missing
runtime files are restored; user-owned project.json/local.md, AGENTS.md, state and
connection strategy remain unchanged. Existing different bytes might be local
adaptations: recovery stops before any writes until their meaning is established.
For confirmed damage that the user authorized replacing, name each file explicitly
with `--replace aek.py` (or another pinned filename). The operation never executes
the damaged file to verify itself.

Linked recovery restores the original relative source. If writing that dependency
is authorized, add `--allow-linked-write`; otherwise the agent asks for that scope.
A matching source/version alone grants no external write permission. For global
skills with an installation receipt, run `python3 scripts/install_skill.py --repair`
from the exact reviewed release. Its source must match every receipt hash;
confirmed damaged files need, for example, `--replace core/ENTRY.md`.
A different or newer release cannot repair an old pin merely by sharing a name.
Do not delete state/receipts, force reinstall, fetch remote code silently or switch
installation strategy to conceal an unavailable dependency.

Verify audit, preservation and applicable project checks after recovery. Audit is
still read-only; a repair request separately authorizes its bounded writes.

`aek.py uninstall TARGET` removes unchanged managed files and its AGENTS marker.
User-owned adaptations remain. Removal refuses modified managed content.

## Verification categories

Static audit checks integrity and availability. The agent separately reviews real
commands, authority, routes, consumers and evidence. Product tests remain project
specific. Evidence supplied to `check-evidence` is a consistency check of a report,
not proof that a command executed; preserve the raw logs and revision too.

For global skills and native plugin mechanisms, see [platforms](platforms.md).
