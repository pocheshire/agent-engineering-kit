# Agent Engineering Kit (AEK)

Prepare a new or existing project for autonomous AI development, with explicit
authority, risk-based discovery, task routing and verifiable evidence.

AEK is a versioned local tool and agent interface. One shared contract powers its
portable entry, global skill and plugin adapters. It does not require a particular
product, stack, AI provider or private knowledge base.

[![AEK checks](https://github.com/pocheshire/agent-engineering-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/pocheshire/agent-engineering-kit/actions/workflows/ci.yml)

**Current version: 0.1.0-rc.1 (release candidate).** See
[validation](docs/validation.md) for tested behavior and remaining limitations.

## Quick start

Download a [release](https://github.com/pocheshire/agent-engineering-kit/releases)
or clone this repository at a version tag. Give your agent this directory and say:

> Read START_HERE.md. Help prepare this project for autonomous development.

Specify the target project if it is outside the agent's current workspace. After
the entry is opened, AEK discovers context and asks only for missing decisions.
Simply attaching an archive does not guarantee activation on every platform.

You can also say “Start a new project”, “Connect these settings to the current
project”, “Check the setup against the template”, or “Update the project settings”.
Russian requests such as «Подключи настройки к текущему проекту» work too.

## Install for Codex

With Python 3.9+ and a reviewed checkout, run:

```sh
python3 scripts/install_skill.py
```

This installs the complete skill into `~/.agents/skills/agent-engineering-kit`.
Start a new Codex session and ask “Help set up this project for autonomous
development”. Explicit fallback: `$agent-engineering-kit`.
The skill applies to setup/adoption/audit/upgrade requests, not ordinary coding.
Run the installer again to update an unchanged installation; local edits stop it.
Use `python3 scripts/install_skill.py --uninstall` to remove it.

For native repository plugins, update/removal commands, smoke tests and the exact
support matrix, see [platforms](docs/platforms.md). Official directory submission
and repository marketplace installation have separate statuses.

## Four modes

| Mode | Result |
| --- | --- |
| Initialize | Discover requirements, propose architecture, install engineering setup within authority |
| Adopt | Inspect an existing project and preserve local rules while adding AEK |
| Audit | Read-only review of installation integrity and real workflow applicability |
| Upgrade | Compare the old baseline, incoming runtime and local adaptations; stop on conflicts |

The agent chooses the mode from your request. Product implementation requires
agreed requirements and execution authority. Local setup never permits deployment
or public publication by itself.

## Project installation

Vendored installation is the portable default: the project keeps its own runtime
and ordinary development needs no KIT checkout. Linked installation uses a pinned
project-relative source and fails when that source is unavailable or changed.
Both preserve existing AGENTS.md and local adaptations. The deterministic CLI is
available for automation; most users can let the agent handle it.

```sh
python3 skills/agent-engineering-kit/core/aek.py install /path/to/project --mode adopt --strategy vendored
python3 skills/agent-engineering-kit/core/aek.py audit /path/to/project
python3 skills/agent-engineering-kit/core/aek.py upgrade /path/to/project
```

Read [installation](docs/installation.md) for linked paths, conflicts and recovery.

## What AEK checks

The installer validates files, versions, integrity and safe repeated operations.
The agent separately examines decisions, write/publication authority, direct and
indirect consumers, routing, meaningful tests and evidence. Zero or entirely
skipped suites never establish successful mandatory coverage.

AEK cannot guarantee that a model follows instructions. Static checks do not prove
runtime behavior, product correctness, host activation or official marketplace
publication. An unavailable environment stays unverified. Semantic conflicts with
existing project instructions need agent review.

## Documentation

- [Agent entry](START_HERE.md) and [engineering contract](skills/agent-engineering-kit/core/CONTRACT.md)
- [Installation and recovery](docs/installation.md)
- [Platform support and distribution](docs/platforms.md)
- [Validation results](docs/validation.md)
- [Compatibility](docs/compatibility.md), [adapter contributions](docs/adapters.md)
- [Security](SECURITY.md), [provenance](docs/provenance.md), [contributing](CONTRIBUTING.md)

Licensed under [MIT](LICENSE).
