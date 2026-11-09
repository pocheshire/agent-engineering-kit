# Agent entry

This is AEK's canonical setup interface. Read VERSION here and report it when the
work completes. Read CONTRACT.md for engineering decisions and MODES.md for the
selected setup operation. ROUTES.md applies to subsequent development.

## Recognize intent

Respond in the user's language. Natural requests such as “Start a new project”,
“Connect the settings to this project”, “Check the setup against the template”,
“Update the project settings”, and “Help prepare this project for autonomous
work” are sufficient. Russian equivalents are equally valid.

Inspect context first: explicit target, current directory, repository root,
existing AGENTS.md and scoped instructions, architecture, manifests, test commands,
CI, pending changes, installed .aek/state.json, and available authoritative docs.
Read applicable ancestor instructions without treating all nearby directories as
writable. Do not search unrelated private directories. This distribution's own
root is not the target unless the user explicitly asks to maintain AEK itself.
If several projects remain plausible, ask one target question before writing.

| Intent | Mode |
| --- | --- |
| A new product or empty project | Initialize |
| Add AEK to an existing project | Adopt |
| Check setup, rules, or installed conformance | Audit (read-only) |
| Update an existing AEK installation | Upgrade |

If no intent is supplied, ask one short question: “What project should we prepare:
a new one, or an existing project?” Do not present an internal command menu.
If intent is clear, do not ask it again. If “update settings” could mean product
configuration and no AEK context exists, clarify the object of the update.

## Proceed without a questionnaire

Research available facts before asking. For Initialize, establish the intended
user outcome and material constraints, propose an architecture with tradeoffs,
and obtain only the product decisions still missing. Setup authorization alone
permits engineering setup, not product implementation. Preserve existing approval
when moving between technical routes. Installation strategy defaults to vendored
for portability; choose linked when the user wants a shared installation and a
stable relative source is available. Explain that choice briefly.

Before installing, inspect and report conflicting local instructions. Preserve
local rules; do not resolve a policy contradiction merely by appending AEK.
Determine project-specific verification commands and actual consumers; record
facts and unknowns in .aek/project.json and .aek/local.md after installation.
Do not mark readiness while commands, scopes, or authority are unresolved.

Use the colocated aek.py with Python 3.9+ for deterministic file operations.
`python3 <core>/aek.py --help` lists the interface. Review the source before first
execution if it is untrusted. Resolve <core> relative to this loaded file; never
guess a developer machine path. If VERSION or core files are missing, stop the
installation, explain which dependency is missing, and restore the same version
from the owner's trusted checkout or release; never silently fetch or execute code.

## Verification and handoff

Run the static audit, then conduct the agent review defined in MODES.md. A static
pass only proves the checks it reports. Record executed commands, revision,
mandatory cases, counts, raw artifact location, and limits. Do not invent a passing
product check. Explain what changed, installed version/strategy, local decisions,
verification category and outstanding gaps. Leave the user's normal development
request routed through CONTRACT.md and ROUTES.md, without requiring skill names.
