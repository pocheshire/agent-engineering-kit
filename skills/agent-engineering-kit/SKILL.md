---
name: agent-engineering-kit
description: Prepare a new or existing project for autonomous AI development; adopt, audit, or upgrade Agent Engineering Kit settings. Use for requests such as "start a new project", "set up this project for autonomous development", "connect project settings", or equivalents in other languages when the intent is engineering setup. Do not activate for ordinary feature implementation, debugging, or unrelated settings.
license: MIT
compatibility: Requires file access and Python 3.9+ for deterministic installation and validation. No network or credentials required by AEK runtime.
metadata:
  version: "0.1.0-rc.1"
---

Resolve paths relative to this SKILL.md, never the target project's working directory.

Read `core/VERSION` and `core/ENTRY.md`, then follow that canonical entrypoint. The complete core travels with this skill; do not substitute a different installed copy. Report the discovered version and reject a missing or unreadable core before project changes. If the version differs from metadata above, investigate package integrity before writing.

If files are missing, explain that this installation is incomplete. Restore the complete skill from a reviewed AEK release (including `core/`), or open `START_HERE.md` in a complete portable checkout. Do not fetch or execute a replacement silently.

Preserve known intent and authorization. If no intent is given, use the short opening dialogue in `core/ENTRY.md`. Host permissions govern every action.
