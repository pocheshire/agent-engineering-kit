# Agent entry

This is AEK's canonical entry for setup and installed project work. Read VERSION
here and report it when the work completes. For ordinary development requests,
follow [CONTRACT.md](CONTRACT.md) and [ROUTES.md](ROUTES.md) directly. For setup
and recovery, use the selected operation in [MODES.md](MODES.md) with the same
contract. Users can request work in their own words.
For KIT maintenance, resolve these procedure files beside this currently loaded
entry, including when the project pins an older runtime. An older release supplied
for restoration is pinned data; it does not replace the active maintenance route.
Read the colocated MODES.md before choosing a verifier or making maintenance writes.
Project-specific constraints and current user authority still apply.

## Recognize intent

Respond in the user's language. Natural requests such as “Start a new project”,
“Connect the settings to this project”, “Check the setup against the template”,
“Update the project settings”, and “Help prepare this project for autonomous
work” are sufficient. Russian equivalents are equally valid.

Identify the target, task intent, and access limits from the request and the
minimum context needed, such as the current directory, repository root, and
applicable ancestor and scoped instructions. If several targets remain
plausible, ask which one the user intends. The KIT checkout is the target only
for a request to maintain AEK itself. Search only relevant authorized locations.

For a change, use the opening interview in CONTRACT.md before analyzing the
project. During read-only analysis, inspect the applicable project rules,
architecture, manifests, test commands, CI, pending changes, installed
`.aek/state.json`, and authoritative docs as relevant to the task. For Audit,
begin the read-only inspection once target, intent, and access are clear.

| Intent | Mode |
| --- | --- |
| A new product or empty project | Initialize |
| Add AEK to an existing project | Adopt |
| Check setup, rules, or installed conformance | Audit (read-only) |
| Update an existing AEK installation | Upgrade |

Opening the KIT or selecting its plugin establishes context, not permission to
install. If the target is known but the operation is unclear, ask one short
question: “Should I check this project's current setup without changes, or adapt
it for autonomous development?” If the target is unknown, ask which project to
prepare (new or existing). Ask the missing question only; an existing AGENTS.md
does not establish the owner's intent or mean the project needs no adaptation.
“Connect these settings” already means Adopt; “check this project” means Audit.
Do not ask that clear intent again or present an internal command menu.

Make a needed question visible in the user-facing reply, using the host's question
UI when available. If a question tool is unavailable, fails, or its delivery is
unconfirmed, ask directly in the reply. Do not finish with “I sent a question”
without displaying the unresolved question. Wait for an answer before dependent
writes; continue only independent authorized investigation. If “update settings”
could mean product configuration without AEK context, clarify the object.

If installed instructions are unavailable, investigate the recorded dependency
and follow the recovery procedure in MODES.md within the current write authority.
Preserve the version and connection strategy; do not interpret recovery as Upgrade.

## Setup decisions and local constraints

For Initialize, use the opening interview to establish the intended outcome and
material constraints. Use analysis to compare viable architectures, then discuss
unresolved tradeoffs in the follow-up interview. Product implementation needs
its own authority. Installation defaults to vendored for portability. Choose
linked when the user wants a shared installation and a stable relative source
is available. A project-relative linked path can point outside the project (for
example `../shared-kit/skills/agent-engineering-kit/core`). Check availability,
pinning and permission to read that destination. Creating, moving or modifying
an external source requires authority. Check that a proposed host cache offers
the stability the installation needs. Explain the arrangement in user terms.

During analysis, inspect applicable local instructions and their scope. A
restriction on product implementation, product dependencies, copied instructions,
or filesystem access has a different effect. AEK includes MIT engineering prose
and a Python maintenance helper; vendoring copies them into .aek, not product
modules. This distinction does not exempt AEK from an applicable blanket ban.
Do not infer a tooling ban merely from “clean-room”, or assume tooling is exempt
when the rule is broad. Identify the exact rule, the proposed action it restricts,
and check whether an authorized alternative exists before calling it a conflict.
Linked avoids copying the core into the project but still adds local metadata/pointers and needs access
to the source; it cannot bypass filesystem or instruction-copy restrictions.
If a real conflict remains, ask one concrete scoped question in plain language
(for example permission to read a named engineering-tool directory while keeping
product-source isolation). Preserve local rules; do not resolve a contradiction
merely by appending AEK, silently narrowing it, or broadening the exception.
End a blocked adoption with the actual narrow question needed to proceed, rather
than only declaring incompatibility. If the owner requires every restriction to
remain, offer a read-only readiness review within those restrictions and ask
whether that is the desired next step. Explain why the requested installation is
blocked; do not present already-clear intent as though it were unknown.
Determine project-specific verification commands and actual consumers. During
approved execution, record facts and unknowns in .aek/project.json and
.aek/local.md after installation.
Do not mark readiness while commands, scopes, or authority are unresolved.
Keep the project entry small. Record executable build/test/lint commands, required
tool versions and unavailable dependencies as facts, not generic recommendations.
Identify which checks are deterministic, behavioral and product/runtime; use
WORKFLOW.md for long-task budgets, optional host Goals and delegated roles only
when applicable. Never install an always-running orchestrator or create native
Goals merely because AEK was selected.

Use the colocated aek.py with Python 3.9+ for deterministic file operations.
`python3 <core>/aek.py --help` lists the interface. Review the source before first
execution if it is untrusted. Resolve <core> relative to this loaded file; never
guess a developer machine path. If VERSION or core files are missing, stop the
dependent installation, explain which dependency is missing, and use a complete
owner-trusted bundle to restore the exact pin under MODES.md. Never run damaged
runtime code, silently fetch code, or substitute a different installed copy.

## Verification and handoff

Run the static audit, then conduct the agent review defined in MODES.md. A static
pass only proves the checks it reports. Record executed commands, revision,
mandatory cases, counts, raw artifact location, and limits. Do not invent a passing
product check. Explain what changed, installed version/strategy, local decisions,
verification category and outstanding gaps. Leave the user's normal development
request routed through CONTRACT.md and ROUTES.md, without requiring skill names.
