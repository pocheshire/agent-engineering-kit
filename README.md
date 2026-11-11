# Agent Engineering Kit (AEK)

Prepare new and existing projects for autonomous AI development with explicit
authority, risk-based discovery, safe updates and verifiable evidence.

AEK is an installable, versioned engineering workflow. One shared core powers
its portable entry, Codex skill and plugin adapters. It works with your project's
architecture, tests and local rules.

[![AEK checks](https://github.com/pocheshire/agent-engineering-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/pocheshire/agent-engineering-kit/actions/workflows/ci.yml)

**Current release: [0.3.0-rc.1](https://github.com/pocheshire/agent-engineering-kit/releases/tag/v0.3.0-rc.1)** · [Previous release: 0.2.0](https://github.com/pocheshire/agent-engineering-kit/releases/tag/v0.2.0) · [Changelog](CHANGELOG.md) · [MIT license](LICENSE)

## What you get

- Project discovery and setup that preserve existing instructions and adaptations.
- Read-only readiness audits, including projects where AEK is not installed.
- Version-pinned installation, three-way upgrades and exact-pin recovery.
- Spec-Driven Development with separate approvals for the specification and plan.
- Risk-based development routes, indirect-consumer checks and independent review.
- Bounded Review → Repair → Validate loops, checkpoints and explicit budgets.
- Cost-aware delegation guidance, pilot-first modernization and layered evaluations.

In the 0.3 workflow, the agent asks about material requirements before and
after read-only project discovery. It then presents the specification and waits
for approval, presents a compact plan and waits again before editing or
delegating. Small changes use the same steps in a short format. Setup, product
implementation and publication each follow the scope you authorize. See the
[development workflow](docs/workflows.md).

## Quick start with Codex

Choose a repository plugin or a global skill as your Codex entry. Both use the
same engineering core. Python 3.9+ is required for AEK's local tools.
The examples pin the current release.

### Repository plugin

With a Codex CLI that supports repository marketplaces:

```sh
codex plugin marketplace add pocheshire/agent-engineering-kit --ref v0.3.0-rc.1
codex plugin add agent-engineering-kit@agent-engineering-kit
codex plugin list --json
```

This installs from the public repository marketplace. It is separate from an
official directory listing. The documented lifecycle was tested with Codex CLI
0.167.0-alpha.3.2; check your CLI's `--help` for available commands.

### Global skill

Obtain and review the tagged checkout, then install its self-contained skill:

```sh
git clone --branch v0.3.0-rc.1 --depth 1 https://github.com/pocheshire/agent-engineering-kit.git
cd agent-engineering-kit
python3 -B scripts/install_skill.py
```

The installer uses `~/.agents/skills/agent-engineering-kit`. A repeat is safe;
conflicting local changes stop the operation. Remove it with
`python3 -B scripts/install_skill.py --uninstall` from the reviewed checkout.

### Start a conversation

Open your target project in Codex and start a new chat. Ask, for example:

> Help prepare this project for autonomous development.

For a project with AEK 0.3 installed, open its folder as the primary local
project in Codex Desktop before starting a development chat. This lets Codex
load the managed `AGENTS.md` block at startup.

Other natural requests work too:

- “Start a new project.”
- “Connect these engineering settings to the current project.”
- “Check this project's setup without changing anything.”
- “Update this project's AEK settings.”
- “Restore the unavailable AEK instructions from my trusted local copy.”

Russian equivalents such as «Подключи настройки к текущему проекту» are supported.
Explicit skill fallback: `$agent-engineering-kit`. The setup skill handles
preparation and maintenance; installed project instructions guide ordinary coding.

## Portable use

Download the [0.3.0-rc.1 release ZIP](https://github.com/pocheshire/agent-engineering-kit/releases/download/v0.3.0-rc.1/agent-engineering-kit-0.3.0-rc.1.zip)
or use a reviewed tagged checkout. Give the directory to your agent and say:

> Read START_HERE.md. Help prepare /path/to/my-project for autonomous development.

After opening [START_HERE.md](START_HERE.md), the agent discovers the target and
intent. If only the KIT was supplied, it asks one short question about the missing
target or whether to audit or adapt. Clear intent needs no repeat question.
Attaching an archive alone does not guarantee activation on every platform.

## What happens in your project

The agent chooses the operation from your request:

| Operation | Result |
| --- | --- |
| Initialize | Discover requirements, propose architecture and prepare the engineering environment |
| Adopt | Inspect the existing project and adapt AEK while preserving local rules |
| Audit | Review readiness or installed conformance without making changes |
| Upgrade | Compare old baselines, all incoming files and local adaptations; stop on conflicts |

An audit continues with a substantive readiness assessment when AEK is absent.
“Not installed” describes installation status; it does not establish incompatibility.
An existing AGENTS.md also does not decide whether you want an audit or adoption.

Installation appends a small managed pointer to AGENTS.md and records project
facts and local decisions under `.aek/`. Existing AGENTS.md bytes remain the exact
prefix. The agent checks applicable restrictions before writing.

| Integration | Dependency arrangement |
| --- | --- |
| Vendored — default | The project keeps its pinned runtime; ordinary development needs no original KIT checkout |
| Linked | The project uses a pinned, reachable relative source, which may be outside the project |

Repeated installation is safe. Vendored Upgrade carries non-overlapping edits
in that project's runtime snapshot forward. Linked Upgrade switches a shared
relative source only when it preserves edits in the old source; it stops before
writes if the incoming source lacks a changed file, even when that release only
changed VERSION. Keep the old pin until the diff is resolved. Represent an
intended project-specific change as an explicit project adaptation, or carry it
into an owner-controlled copy of the new release, verify the copy, and retry
with that reviewed source. Recovery verifies the complete original pin and
preserves its version and connection strategy. Read the
[installation and recovery guide](docs/installation.md) for CLI automation and
authority boundaries.

## Updating AEK

Host installation and project installation have independent versions:

- **Global skill:** obtain a newer reviewed release and rerun its installer.
- **Repository plugin:** follow the [tag-switch procedure](docs/platforms.md#codex-repository-plugin).
  Refreshing a tag-pinned marketplace keeps that tag.
- **Project:** ask the agent to update its AEK setup after the new KIT is available.
  Updating the host entry does not upgrade existing vendored project runtimes.

Start a new chat after updating the host entry and verify the loaded version.
Read the [compatibility policy](docs/compatibility.md) and changelog before migration.
Local modifications are retained or reported as conflicts.
For linked projects, moving or updating the shared source can invalidate the pin;
review that dependency before changing it.

## Sustained development and evaluation

AEK's [workflow](docs/workflows.md) guides agents through bounded repair loops,
current-revision checks, durable checkpoints and actual reviewer results. It
calls for explicit model/effort choices when the host supports them, narrower
briefs for delegated work and scripts for mechanical checks. Native Goals are
optional and require an explicit user request. Modernization starts with one
pilot, shared-input parity checks and a verified rollback path.

The offline `aek.py work` helper validates task, attempt, delegation and
modernization records and evaluates repeated-run evidence. Repository tools
prepare staged evaluator views, render Codex permission profiles and capture
observed model/effort/usage. These tools do not start workers, execute project
checks or authenticate claims. AEK adds no background orchestrator, hooks,
telemetry or runtime network dependency.

## Platforms and verified results

| Entry | Status |
| --- | --- |
| Portable KIT | Self-contained runtime, installation and candidate marker migration validated |
| Codex Desktop | Two candidate project chats verified real delegation after plan approval, worker model and effort, instruction read order and lead acceptance |
| Codex global skill | Installation/update/recovery checks; natural activation in an actual desktop app task |
| Codex repository plugin | Native CLI discovery, natural activation, maintenance and public-tag lifecycle validated |
| Claude Code plugin | Adapter prepared; host runtime untested |
| Cursor / other clients | Compatibility candidates; no runtime support claim |

No official directory submission or approval is claimed. See
[platforms](docs/platforms.md) for installation, activation, update, removal and
smoke tests for each entry.

The [validation reports](docs/validation.md) record the candidate's 123 local
checks, the Desktop rollout evidence and the historical 0.2.0 results. The
[0.3.0-rc.1 release](https://github.com/pocheshire/agent-engineering-kit/releases/tag/v0.3.0-rc.1)
links to the matching CI and downloadable artifacts.

## Documentation and contributing

- [Agent entry](START_HERE.md) and [canonical engineering contract](skills/agent-engineering-kit/core/CONTRACT.md)
- [Installation and recovery](docs/installation.md), [platforms](docs/platforms.md), [compatibility](docs/compatibility.md)
- [Development workflows](docs/workflows.md) and [workflow record format](docs/workflow-format.md)
- [Evaluator isolation](docs/evaluation-isolation.md), [Codex permissions](docs/codex-permissions.md), [rollout observation](docs/codex-observation.md)
- [Contributing](CONTRIBUTING.md), [adapter development](docs/adapters.md), [security](SECURITY.md), [provenance](docs/provenance.md)

Licensed under [MIT](LICENSE).
