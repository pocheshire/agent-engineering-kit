# Installation and recovery procedures

Apply the [shared setup rules](MODES.md#setup-modes) and the section for the selected operation.

## Initialize

Use the opening interview to establish the idea, users, intended outcome, and
material constraints. Inspect the target and context during analysis. Use the
follow-up interview for remaining material choices, including stack tradeoffs.
Propose a suitable minimal architecture, commands, and acceptance checks. During
approved execution with setup authority, choose the [runtime strategy](#runtime-and-adaptations),
install AEK and record discovered commands, tool versions and outstanding
dependencies in `.aek/project.json`. Inspect the diff and run the static audit.
A blank project with no tests remains unverified for product runtime.

## Adopt

Read existing and scoped instructions, architecture, dependency manifests, tests,
CI and working tree before writing. [Check interacting rules](#adapt-project-rules)
and choose the [runtime strategy](#runtime-and-adaptations). Preserve local decisions and pending changes.
Use the installer to append the managed pointer to AGENTS.md. Apply approved
adaptations at the source of each rule and verify behavior after setup.

Identify what each local restriction covers: product code, dependencies, copied
instructions or filesystem access. Vendoring copies MIT engineering instructions
and a Python helper into the project. Linking still writes project metadata and
requires access to the shared source. If a rule blocks the intended action,
explain the exact conflict and ask the narrow question that would resolve it.
If the owner keeps that restriction, offer a read-only readiness review.

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

Compare the applicable rules for specification and plan approval, first writes,
revised approvals, publication, and other behavior affected by setup. Keep
host/profile instructions at their original scope. Persist a project decision
only when it changes this project's workflow. Leave unrelated personal routines,
profile text and private machine paths out of project files. If these
sources yield no interacting project rule, record the sources checked and that
finding in the setup specification. This completes the comparison for that project.

For each interaction, record the decision and its affected consumers. Use the
four-field map below for conflicts and shared policies, both in the specification
and in the saved local or shared decision record.

| AEK rule | Project rule | Decision | Consumers and verification |
| --- | --- | --- | --- |
| Contract version and section | Authoritative path and section | How both rules apply or what must be resolved | Affected repositories and routes, expected behavior, and how to exercise an affected consumer |

Match equivalent decisions once. An explicitly approved, applicable
specification version can satisfy the first approval. The plan still receives
its own approval. If project prerequisites for a stage are met, the same reply
can approve the shown plan and explicitly authorize that stage. Keep an existing
authorization that still applies. Apply publication and other side effects only
within the granted scope. A map entry records the governing rule and decision;
the current request and actual approvals establish authority for each task.

Show the comparison and any material decisions in the setup specification. Resolve
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

Audit each installation, inspect the diff and repeat the same CLI operation
to verify it leaves files unchanged. With no interacting rules and no changed
behavior or previous conflict to exercise, these checks complete verification
of the installation. Report the scope of the checks.

Exercise behavior where an interaction or change warrants it. For a shared rule,
name its consumers and test through an affected consumer. For an Upgrade, test
changed behavior and repeat the trigger of any known previous conflict. Use an
ordinary task in a fresh, authorized isolated session. For example, under a
local all-edits approval rule, request a small wording edit and check that the
agent waits before its first write. A stage authorized at intake must still
respect a separate local plan approval. Inspect actual actions and changed files.
If the host is unavailable, report the unverified behavior. The full route matrix
belongs to [core release evaluation](WORKFLOW.md#layered-behavioral-evaluation).

## Upgrade

Inspect installed state, current adaptations, new release and changelog. The CLI
inventory must include every incoming runtime file, including additions that have
no old baseline. Verify the complete incoming version/hash map against the
owner-trusted release before writing; comparing only old baseline names misses
new rules/helpers. Inspect the incoming changelog and relevant added contract or
procedure files to understand their effect. When the incoming source is meant
to be the currently loaded release, explicitly compare its full map with that
loaded core; otherwise preserve and report the separately trusted source identity.
Revisit the affected [project rules](#adapt-project-rules) against the
incoming contract and the current project sources. Carry forward decisions that
still apply. If the installation predates the comparison, use those sources.
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

When the incoming version selects a different managed entry, include the
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

Recovery preserves the installed version and connection strategy. First inspect
the installed state or global-skill receipt, applicable local instructions, the
missing dependency and the owner's trusted local release within current read
authority.

**Direct recovery.** An owner's explicit request to restore missing files
authorizes a direct repair when the installation is vendored, every missing
managed runtime file falls within the requested write scope, and local rules
permit that write without further approval. The trusted source must match the
installed version and complete baseline hash map. Check the list of missing
files and all surviving runtime bytes before writing: the CLI restores *all*
missing runtime files in one transaction. Existing divergent content or an
unexpected runtime file requires reconciliation. With these checks satisfied,
run the default restore immediately, without separate specification and plan
approvals.

Use the [two-phase procedure](CONTRACT.md#two-phase-procedure) for other
recovery, including linked or global installations and replacement of existing
bytes. Respect any project-specific approval before writing. A source mismatch
or unavailable trusted source blocks recovery until a matching source is available.

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
silently switch to another KIT. Verify the static audit, the restored paths,
preservation of all other project bytes and any applicable project checks.
Report restored files, verification and material limits. For formal acceptance,
release or required independent review, use the
[contract's evidence requirements](CONTRACT.md#verification-review-and-evidence).

## Runtime and adaptations

Vendored is the default: .aek/runtime is sufficient for ordinary development
without the original KIT. Select linked for a requested shared installation
with a stable source path; verify availability, pinning and permission to read
it. Creating or changing an external shared source needs its own write authority.
Linked stores a project-relative source, pinned version
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
