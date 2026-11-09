---
name: agent-engineering-kit
description: Prepare a new or existing project for autonomous AI development; adopt, audit, upgrade, or restore unavailable Agent Engineering Kit instructions. Use for requests such as "start a new project", "set up this project for autonomous development", "connect project settings", or equivalents in other languages when the intent is engineering setup. Do not activate for ordinary feature implementation, debugging, or unrelated settings.
license: MIT
compatibility: Requires file access and Python 3.9+ for deterministic installation and validation. No network or credentials required by AEK runtime.
metadata:
  version: "0.1.0"
---

Resolve paths relative to this SKILL.md, never the target project's working directory.

Read this skill's own `core/VERSION`, `core/ENTRY.md`, and `core/MODES.md` before choosing a maintenance tool or writing. Follow that canonical entrypoint and its selected operation. The complete core travels with this skill; do not replace its maintenance procedure with one from the target's older runtime or recovery-data copy. Those older pins remain project data to preserve, while this complete loaded KIT supplies the verifier. Report the discovered version and reject a missing or unreadable own core before project changes. If the version differs from metadata above, investigate package integrity before writing.

If this skill's own core files are missing, explain that this installation is incomplete before project writes. Inspect an available installation receipt and an owner-supplied trusted complete release; use that release's verifier and recovery instructions to restore the exact pin. Never run damaged code or fetch a replacement silently. If no trusted source is available, ask for its location. A complete portable checkout's `START_HERE.md` can provide the recovery procedure; it does not authorize a version change. A missing target-project dependency with an intact skill core instead follows this skill's `core/MODES.md` recovery procedure.

During this incomplete-core diagnosis, inspect only the current project, this skill's own installation/receipt, and sources the user explicitly supplied. Do not recursively scan other projects, profile directories, or operating-system temporary folders for substitute cores. If the supplied scope has no complete trusted source, stop and ask for that source's location.

Preserve known intent and authorization. If no intent is given, use the short opening dialogue in `core/ENTRY.md`. Host permissions govern every action.
