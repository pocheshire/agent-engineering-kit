---
name: agent-engineering-kit
description: Agent Engineering Kit (AEK) prepares new/existing projects for autonomous development; initialize, adopt, audit, upgrade, or recover unavailable AEK. Check target access limits first. When access allows, enter through THIS installed skill and its own core, even when the user supplies another KIT source; supplied older bundles are pinned data, not replacement entrypoints. If outside reads are forbidden, DO NOT open this skill or core. In that blocked case, end the reply with an actual question in the user's language, such as "May I read AEK instructions outside this project, or should I only assess local files?" Saying permission is required is not a question. Use for "start a new project", "set up this project for autonomous development", "connect project settings", and equivalents in other languages. Do not activate for ordinary implementation, debugging, or unrelated settings.
license: MIT
compatibility: Requires file access and Python 3.9+ for deterministic installation and validation. No network or credentials required by AEK runtime.
metadata:
  version: "0.2.0"
---

Resolve paths relative to this SKILL.md, never the target project's working directory.
Use the exact opened SKILL.md path: its parent directory contains `core/`.
In a repository plugin the layout is
`skills/agent-engineering-kit/SKILL.md` and
`skills/agent-engineering-kit/core/ENTRY.md`. Keep that `skills/agent-engineering-kit/`
prefix when resolving from the package root. If an attempted path fails, compare
it with the opened skill's actual parent before diagnosing a missing installation.

Check the target's already available instructions and permitted project-local
AGENTS.md before opening core files. Skill discovery does not exempt this KIT
from a ban on external reads. If that ban applies, use the available description
to explain the specific access needed and ask a visible scoped question; do not
open further KIT files first. Reading this SKILL.md itself also needs permission;
the description's access condition applies before loading it. An explicit current
owner grant can authorize that narrow access without relaxing product isolation.

Read this skill's own `core/VERSION`, `core/ENTRY.md`, and `core/MODES.md` before choosing a maintenance tool or writing. Follow that canonical entrypoint and its selected operation. The complete core travels with this skill; do not replace its maintenance procedure with one from the target's older runtime or recovery-data copy. Those older pins remain project data to preserve, while this complete loaded KIT supplies the verifier. Report the discovered version and reject a missing or unreadable own core before project changes. If the version differs from metadata above, investigate package integrity before writing.

If this skill's own core files are missing, explain that this installation is incomplete before project writes. Inspect an available installation receipt and an owner-supplied trusted complete release; use that release's verifier and recovery instructions to restore the exact pin. Never run damaged code or fetch a replacement silently. If no trusted source is available, ask for its location. A complete portable checkout's `START_HERE.md` can provide the recovery procedure; it does not authorize a version change. A missing target-project dependency with an intact skill core instead follows this skill's `core/MODES.md` recovery procedure.

During this incomplete-core diagnosis, inspect only the current project, this skill's own installation/receipt, and sources the user explicitly supplied. Do not recursively scan other projects, profile directories, or operating-system temporary folders for substitute cores. If the supplied scope has no complete trusted source, stop and ask for that source's location.

Preserve known intent and authorization. If no intent is given, use the short opening dialogue in `core/ENTRY.md`. Host permissions govern every action.
