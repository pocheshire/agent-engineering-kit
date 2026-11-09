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

## Audit

Read-only: run `aek.py audit TARGET`, then inspect actual applicability. Check that
instructions route real tasks, technical escalation preserves phase and write
scope, product/publication authority is explicit, required sources are reachable,
commands exercise intended cases and evidence is current. Sample a realistic
change boundary and indirect consumer. Do not execute project commands that write
artifacts without authority; a static audit itself writes nothing. Report each
category as passed, failed, partial or unverified with evidence. A file-presence
pass is not project conformance. Do not silently repair during Audit.

## Upgrade

Inspect installed state, current adaptations, new release and changelog. The CLI
compares baseline hashes, current managed content and incoming content. It keeps
non-overlapping changes; if both sides changed a managed file differently, it
stops without writes. Review a manual three-way resolution with the owner when
policy choices are involved. User-owned project.json/local.md are retained.
Do not overwrite state to hide a conflict. Snapshot the project in version control
before an authorized upgrade when appropriate. Afterward check the diff, static
audit and relevant behavioral checks. Breaking contract changes require a major
version and an explicit migration. A version string alone is not provenance.

## Runtime and adaptations

Vendored is the default: .aek/runtime is sufficient for ordinary development
without the original KIT. Linked stores a project-relative source, pinned version
and content hashes; audit must fail when unavailable or changed. Relocation works
only when that relative layout is preserved. An intentional source change requires
an analyzed upgrade, never automatic trust of the new bytes.

Keep each rule in one canonical file. .aek/local.md records local decisions and
scope without copying the whole contract. project.json records commands and facts;
empty checks or unknown authority are pending discovery, not verification.
AGENTS.md is a small pointer alongside the project's own instructions. The installer
cannot infer semantic contradictions in arbitrary prose; the agent must review them.
