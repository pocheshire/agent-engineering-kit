# Setup modes

These modes use CONTRACT.md and the same installer. They do not implement a
product or choose its business requirements implicitly.

## Initialize

Inspect the target and context; do not assume a chosen stack. Establish the idea,
users, intended outcome and material constraints from available sources, then ask
only for missing decisions. Propose a suitable minimal architecture, commands and
acceptance checks. With setup authority, install AEK and record known project
facts. Create product implementation only when requirements and execution are
authorized. A blank project with no tests remains unverified for product runtime.

## Adopt

Read existing and scoped instructions, architecture, dependency manifests, tests,
CI and working tree before writing. Identify contradictions with the contract.
Preserve local decisions and pending changes. Use the installer to append a small
managed pointer to AGENTS.md; do not rewrite existing prose. Resolve substantive
policy conflicts with the owner or existing authoritative rule before claiming
adoption complete. Populate user-owned project.json/local.md with discovered
commands, authority, architecture and consumer boundaries. Inspect the produced
diff and verify a safe repeat run.

Use the unmodified CLI from the currently loaded complete KIT for installation,
including linked installation: `python3 -B <loaded-core>/aek.py install TARGET
--mode adopt --strategy linked --source RELATIVE_CORE`. The explicitly selected
linked source supplies pinned runtime data; it does not replace the active
installer. Do not import/patch its functions, filter the transaction, manufacture
state, or move the agent pointer to README to work around a perceived restriction.
Those changes can produce an undiscoverable installation that fails audit.

Preserving existing AGENTS.md means retaining every original byte as an exact
prefix and appending the small managed block. When the task authorizes engineering
adaptation and local rules allow AGENTS.md changes, this is Proceed: use the CLI
without asking again for append permission. A generic “preserve AGENTS.md”,
“preserve its existing bytes”, “keep my rules” or “keep my uncommitted changes”
does not forbid that append. Do not paraphrase those requests as “the entire file
must remain byte-identical”. Untracked status is not immutability; do not stage
or commit the file without task authority.

Ask for append permission only when an applicable instruction expressly forbids
editing/appending to AGENTS.md, requires the entire file to stay byte-identical,
or the required write scope is actually absent. Identify that exact prohibiting
instruction; do not invent one from a generic preservation request where the
engineering change is already allowed. Do not bypass the helper to manufacture a partial
installation. Use only the supported managed paths, then audit and repeat the
same installer command. A missing entry block is a failed installation boundary,
not an accepted local adaptation. Put run findings in the reply by default;
additional report files or unrelated documentation edits need task scope.

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
For both readiness and installed audits, check that
instructions route real tasks, technical escalation preserves phase and write
scope, product/publication authority is explicit, required sources are reachable,
commands exercise intended cases and evidence is current. Sample a realistic
change boundary and indirect consumer. Do not execute project commands that write
artifacts without authority; a static audit itself writes nothing. Report each
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
The CLI compares baseline hashes, current managed content and incoming content.
For vendored installs it keeps non-overlapping project-local runtime edits while
applying the incoming snapshot. Linked installs switch a shared relative source;
if an old-source edit is absent from the incoming source, Upgrade stops without
writes even when upstream changed only VERSION. Keep the old pin until the change
is resolved. Review the diff, then represent an intended project-specific change
as an explicit project adaptation or carry it into an owner-controlled copy of
the new release, verify that copy and retry with its relative path. Do not modify
a shared source or state to bypass the conflict. Review a manual three-way
resolution with the owner when policy choices are involved. User-owned
project.json/local.md are retained.
Do not overwrite state to hide a conflict. Snapshot the project in version control
before an authorized upgrade when appropriate. Afterward check the diff, static
audit and relevant behavioral checks. Breaking contract changes require a major
version and an explicit migration. A version string alone is not provenance.
The installer rejects downgrades, changed content with equal version precedence,
and unsupported adaptation schemas before writes. A major transition additionally
requires `--allow-major` after an authorized migration has been reviewed; the flag
itself does not grant that authority. Build metadata does not increase precedence.
By default, put the upgrade findings and verification record in the final reply.
Use the helper's bounded runtime/state transaction; do not create separate
per-run report files or rewrite user-owned adaptation documents unless the task
explicitly asks for those additional artifacts or edits. Existing adaptations
can be analyzed without changing them.

## Recover an unavailable runtime

Recovery preserves the installed version and connection strategy; it is not an
upgrade or a new setup mode. Inspect the installed state or global-skill receipt,
the missing dependency, and available trusted local release first. Stop dependent
project writes until the source can be verified. Do not execute a damaged aek.py
to verify or repair itself. Use a verifier from a complete reviewed bundle.

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
