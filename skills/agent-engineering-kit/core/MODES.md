# Setup modes

For agent-led Initialize, Adopt, Upgrade and Recovery, follow the two-phase procedure in
[CONTRACT.md](CONTRACT.md) before installation or managed-state writes. Audit is read-only. Direct use of
the offline CLI follows its own deterministic operations and integrity checks.
Setup authority covers engineering setup. Product implementation and publication
require their own authority.

## Initialize

Use the opening interview to establish the idea, users, intended outcome, and
material constraints. Inspect the target and context during analysis. Use the
follow-up interview for remaining material choices, including stack tradeoffs.
Propose a suitable minimal architecture, commands, and acceptance checks. During
approved execution with setup authority, install AEK and record known project
facts. A blank project with no tests remains unverified for product runtime.

## Adopt

Read existing and scoped instructions, architecture, dependency manifests, tests,
CI and working tree before writing. Build the [rule map](#adapt-project-rules)
from current project sources. Preserve local decisions and pending changes.
Use the installer to append the managed pointer to AGENTS.md. Apply approved
adaptations at the source of each rule and verify behavior after setup.

Use the unmodified CLI from the currently loaded complete KIT for installation,
including linked installation: `python3 -B <loaded-core>/aek.py install TARGET
--mode adopt --strategy linked --source RELATIVE_CORE`. The explicitly selected
linked source supplies pinned runtime data; it does not replace the active
installer. Do not import/patch its functions, filter the transaction, manufacture
state, or move the agent pointer to README to work around a perceived restriction.
Those changes can produce an undiscoverable installation that fails audit.

Preserving existing AGENTS.md means retaining every original byte as an exact
prefix and appending the small managed block. Include the append in the proposed
scope when the task authorizes engineering adaptation and local rules allow
AGENTS.md changes. Use the CLI after plan approval. A generic “preserve AGENTS.md”,
“preserve its existing bytes”, “keep my rules” or “keep my uncommitted changes”
does not forbid that append. Do not paraphrase those requests as “the entire file
must remain byte-identical”. Untracked status is not immutability; do not stage
or commit the file without task authority.

Ask for append permission only when an applicable instruction expressly forbids
editing/appending to AGENTS.md, requires the entire file to stay byte-identical,
or the required write scope is actually absent. Identify that exact prohibiting
instruction; do not invent one from a generic preservation request where the
engineering change is already allowed. Do not bypass the helper to manufacture a partial
installation. Limit the installer to its supported paths and other edits to
the approved adaptation scope. A missing entry block fails installation
verification. Put run findings in the reply by default.

## Adapt project rules

Use this procedure for agent-led Adopt and Upgrade. Before any writes, identify
the target repositories, their applicable instructions and authoritative shared
sources, and the routes that consume them. Read the active and incoming AEK
contracts as applicable. For Upgrade, inspect the applicable clauses in both
versions or their textual diff and identify what changes for the project.
Use one setup specification and then one execution plan for the agreed set of
repositories under [CONTRACT.md](CONTRACT.md).

Build a compact rule map from rules that interact with the project workflow.
Cover specification and plan approvals, authority before the first write,
revision of approvals, and publication. Include other rules when the setup
changes their behavior.

| AEK rule | Project rule | Decision | Consumers and verification |
| --- | --- | --- | --- |
| Contract version and section | Authoritative path and section, or the result of checking that no local rule applies | How the rules work together, the source edit required, or the decision still needed | Affected repositories and routes, expected behavior, and the action or state that will verify it |

Keep all four fields in every row of the map shown in the setup specification
and of the saved map. A short row can cite a section and name one observable
check. When a rule is shared, name its consumers and which consumer will be
exercised.

Match equivalent decisions once. An explicitly approved, applicable
specification version can satisfy the first approval. The plan still receives
its own approval. If project prerequisites for a stage are met, the same reply
can approve the shown plan and explicitly authorize that stage. Keep an existing
authorization that still applies. Apply publication and other side effects only
within the granted scope. A map entry records the governing rule and decision;
the current request and actual approvals establish authority for each task.

Show the map and any material decisions in the setup specification. Resolve
conflicts from authoritative sources or with the owner. After specification
approval, list the affected files, expected edits, and verification in the plan.
Before applying it, recheck the relevant source revisions or bytes. If a source
has changed, inspect the affected rule and reopen the applicable approval under
the contract when the change is material. Pause dependent edits while a required
source or decision is unavailable.

Use the existing CLI for the managed installation or upgrade. Make authorized
rule edits at their authoritative source. Save applicable decisions and their
sources in `.aek/local.md`. When several repositories share rules, put the
full map in one approved shared location and link to it from their local
adaptations. Verify references from each affected repository. Record discovered
commands and environment facts in `.aek/project.json`, preserving existing
unrelated entries.

Audit each installation, inspect the diff, and repeat the same CLI operation
to check that it leaves files unchanged. Run behavioral probes in fresh sessions
from authorized isolated copies. Give ordinary requests without naming AEK or
prescribing approval steps. Observe that the agent reads the pinned contract
before implementation and follows the applicable route:

- A README heading correction proceeds with a focused edit and check, without
  a specification, plan approval or ticket, unless a project rule requires them.
- A substantial feature follows specification and plan approval before writing.
- A local policy requiring approval for all edits still applies to small changes.
- A technical escalation preserves known answers and authorization while applying
  the new route's required checks and approvals.

Exercise affected consumers for shared rules. For Upgrade, exercise changed
behavior and the trigger that caused the original conflict. If a local route
requires plan approval independently of stage authority, grant that authority at
intake and verify that the agent waits only for the still-required approval.
Use actions and file snapshots as evidence. If the host or evidence is unavailable,
report behavior as unverified and the installation checks actually completed.
See [WORKFLOW.md](WORKFLOW.md#layered-behavioral-evaluation).

## Audit

Read-only: inspect installation state and run `aek.py audit TARGET` for its bounded
integrity check. If AEK is absent, the CLI reports “AEK is not installed”; that is
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

Inspect installed state, current adaptations, new release and changelog. The CLI
inventory must include every incoming runtime file, including additions that have
no old baseline. Verify the complete incoming version/hash map against the
owner-trusted release before writing; comparing only old baseline names misses
new rules/helpers. Inspect the incoming changelog and relevant added contract or
procedure files to understand their effect. When the incoming source is meant
to be the currently loaded release, explicitly compare its full map with that
loaded core; otherwise preserve and report the separately trusted source identity.
Revisit the affected rows of the [rule map](#adapt-project-rules) against the
incoming contract and the current project sources. Carry forward decisions that
still apply. If the installation predates the map, build it from those sources.
The CLI compares baseline hashes, current managed content and incoming content.
For vendored installs it keeps non-overlapping project-local runtime edits while
applying the incoming snapshot. Linked installs switch a shared relative source;
if an old-source edit is absent from the incoming source, Upgrade stops without
writes even when upstream changed only VERSION. Keep the old pin until the change
is resolved. Review the diff, then represent an intended project-specific change
as an explicit project adaptation or carry it into an owner-controlled copy of
the new release, verify that copy and retry with its relative path. Do not modify
a shared source or state to bypass the conflict. Review a manual three-way
resolution with the owner when policy choices are involved. The CLI retains
user-owned project.json/local.md. Include any authorized updates to them in the
adaptation plan.

When crossing a managed-entry boundary (0.3.0-rc.1 or 0.4.0-rc.1), include the
AGENTS.md block replacement in the plan and check its write scope. The installer
replaces the exact block belonging to the old pin in the same transaction as the
runtime update, preserving surrounding owner text and ordinary file permissions.
An edited or ambiguous block requires reconciliation before Upgrade can write.
The 0.4 entry delegates process selection to the pinned routes; preserve any
stricter owner policy outside that block and reconcile it in the rule map.

Do not overwrite state to hide a conflict. Snapshot the project in version control
before an authorized upgrade when appropriate and within the approved plan.
Afterward check the diff, static audit and relevant behavioral checks. Minor
releases before 1.0 may change the contract. From 1.0 onward, breaking contract
changes require a major version. Review incompatible changes and their explicit
migration in the proposed upgrade. A version string alone is not provenance.
The installer rejects downgrades, changed content with equal version precedence,
and unsupported adaptation schemas before writes. A major transition additionally
requires `--allow-major` after an authorized migration has been reviewed; the flag
itself does not grant that authority. Build metadata does not increase precedence.
By default, put the upgrade findings and verification record in the final reply.
Use the helper's bounded upgrade transaction for managed files. Limit adaptation
edits and any persisted evidence to the approved scope.

## Recover an unavailable runtime

Recovery preserves the installed version and connection strategy. During read-only
analysis, inspect the installed state or global-skill receipt, the missing
dependency, and available trusted local release. Verify the source before any
dependent write. Use a verifier from a complete reviewed bundle.

For a project, use the aek.py colocated with these instructions in the currently
loaded complete KIT as the verifier: `aek.py restore TARGET --source RELATIVE_CORE`.
Pass the owner's exact-pinned older release as recovery data with `--source`;
it may predate the restore command and is not the verifier to execute. The current
helper can restore an older pin without changing its version. Do not reimplement
runtime copying while this canonical helper is available. If the loaded helper
is unavailable too, locate a complete reviewed verifier within the supplied
sources, or ask for its location before writing. Do not search unrelated projects
or temporary/profile directories for a lookalike KIT.
The recovery data must match the installed version and complete baseline hash map.
Default recovery restores missing runtime files. Existing divergent bytes may be
local decisions: preserve them unless the user has authorized replacing confirmed
damage, then name only those files with `--replace FILENAME`. All conflicts are
checked before writing. Do not delete state, regenerate baselines or force Upgrade
to conceal damage. AGENTS.md and user-owned adaptations stay byte-identical.

For linked projects, restoration writes the original relative source, which may
be outside the project. Use `--allow-linked-write` only when the current task
authorizes that destination; otherwise ask for the missing write authority.
For a global skill with its receipt, run `scripts/install_skill.py --repair` from
the exact trusted release. Explicit damaged-file replacement uses, for example,
`--replace core/ENTRY.md`. The receipt remains unchanged. A different version or
hash set cannot repair the pin. If the trusted release is unavailable, report that
specific dependency and ask where to obtain it; do not fetch a replacement or
silently switch to another KIT. Verify audit, byte preservation and applicable
project checks after recovery, and report their categories separately. State the
independent-review status for the current revision: say `performed` only with
reviewer identity, reviewed revision and result; otherwise say
`not performed (no reviewer result)`.

## Runtime and adaptations

Vendored is the default: .aek/runtime is sufficient for ordinary development
without the original KIT. Linked stores a project-relative source, pinned version
and content hashes. The source may be outside the project via `..`; reading it
must be allowed by local policy and the host. Linking does not grant external
write permission or bypass isolation. Audit must fail when unavailable or changed. Relocation works
only when that relative layout is preserved. An intentional source change requires
an analyzed upgrade, never automatic trust of the new bytes.

Keep each rule in one canonical file. .aek/local.md records local decisions and
scope without copying the whole contract. project.json records commands and facts;
empty checks or unknown authority are pending discovery, not verification.
AGENTS.md is a small pointer alongside the project's own instructions. The installer
cannot infer semantic contradictions in arbitrary prose; the agent must review them.
