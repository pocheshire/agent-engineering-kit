# Setup modes

Use the [two-phase procedure](CONTRACT.md#two-phase-procedure) for agent-led
Initialize, Adopt and Upgrade. [Recovery](#recover-an-unavailable-runtime)
defines the one direct repair case. Audit is read-only. Use the CLI beside the
currently loaded complete, trusted KIT with Python 3.9+ and `-B`.
Report the KIT version for maintenance. Product implementation and publication
require separate authority.

## Initialize

To set up a new project, follow the [Initialize procedure](MAINTENANCE.md#initialize).

## Adopt

To connect AEK to an existing project, follow the [Adopt procedure](MAINTENANCE.md#adopt).

## Adapt project rules

When adopting or upgrading, follow the [rule comparison and verification procedure](MAINTENANCE.md#adapt-project-rules).

## Audit

For a read-only audit of a trusted project installation, inspect its entry, state and
permitted runtime. Verify the complete filename and SHA-256 map against the
recorded baseline using a trusted tool before executing the pinned helper.
On a match run `python3 -IB <pinned-core>/aek.py audit TARGET`. On divergence
report the affected files and use a separately trusted complete verifier within
current access. No external setup skill is needed to check an intact, accessible
installation against its own pin. A review against another release uses the
requested complete kit. If AEK is absent, the CLI reports “AEK is not installed”; that is
not an incompatibility verdict or a completed audit of the project. Continue a
readiness review against this loaded KIT's version using accessible project rules,
architecture, CI and evidence. Report installation as not installed and installed
integrity as not applicable; do not manufacture an installed-conformance pass.
Keep incidental tool writes out of read-only audits too. Use
`git --no-optional-locks status` (and the same global flag for other Git inspection)
so status refreshes cannot rewrite the index; an inherited environment variable
may be filtered by the host. Run Python with `-B` and execute only artifact-free
checks. When a check writes, obtain authority or use an authorized isolated copy
instead of assuming caches or Git metadata are exempt.
Identify existing strengths, material workflow gaps and the actual prerequisites
for adoption, including scoped policy/access questions under ENTRY.md. Existing
rules may already satisfy a requirement; no copying is necessary to assess them.
Do not install, create .aek or modify AGENTS.md to make Audit pass. If policy blocks
a needed source, review what is accessible and report that specific limit.

For installed projects, inspect actual applicability after the integrity check.
For both readiness and installed audits, check that instructions route real
tasks through the applicable contract approvals, technical escalation preserves
valid approvals and write scope, product and publication authority is explicit,
required sources are reachable, commands exercise intended cases and evidence is
current. Sample a realistic change boundary and indirect consumer. When comparing
an older pin to this KIT, distinguish installed integrity from readiness for
the current workflow. Run only artifact-free checks during Audit. Report each
category as passed, failed, partial, unverified or not applicable with evidence. A file-presence
pass is not project conformance. Do not silently repair during Audit.

## Upgrade

To change the installed pin, follow the [Upgrade procedure](MAINTENANCE.md#upgrade).

## Recover an unavailable runtime

To restore the installed pin, follow the [Recovery procedure](MAINTENANCE.md#recover-an-unavailable-runtime) before choosing a verifier or authorizing writes.

## Runtime and adaptations

When selecting a runtime or recording local decisions, follow [runtime and adaptations](MAINTENANCE.md#runtime-and-adaptations).
