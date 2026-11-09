# Agent Engineering Kit (AEK)

Prepare new and existing projects for autonomous AI development with explicit
authority, risk-based discovery, safe updates and verifiable evidence.

AEK is an installable, versioned engineering workflow. One shared core powers
its portable entry, Codex skill and plugin adapters. It works with your project's
architecture, tests and local rules.

[![AEK checks](https://github.com/pocheshire/agent-engineering-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/pocheshire/agent-engineering-kit/actions/workflows/ci.yml)

**Stable release: [0.2.0](https://github.com/pocheshire/agent-engineering-kit/releases/tag/v0.2.0)** · [Changelog](CHANGELOG.md) · [MIT license](LICENSE)

## What you get

- Project discovery and setup that preserve existing instructions and adaptations.
- Read-only readiness audits, including projects where AEK is not installed.
- Version-pinned installation, three-way upgrades and exact-pin recovery.
- Risk-based development routes, indirect-consumer checks and independent review.
- Bounded Review → Repair → Validate loops, checkpoints and explicit budgets.
- Cost-aware delegation guidance, pilot-first modernization and layered evaluations.

The agent investigates available context first and asks only for missing product
decisions or authority. Setup follows the paths and actions you authorize;
product implementation and publication need their own authorization.

## Quick start with Codex

Choose a repository plugin or a global skill as your Codex entry. Both use the
same engineering core. Python 3.9+ is required for AEK's local tools.

### Repository plugin

With a Codex CLI that supports repository marketplaces:

```sh
codex plugin marketplace add pocheshire/agent-engineering-kit --ref v0.2.0
codex plugin add agent-engineering-kit@agent-engineering-kit
codex plugin list --json
```

This installs from the public repository marketplace. It is separate from an
official directory listing. The documented lifecycle was tested with Codex CLI
0.167.0-alpha.3.2; check your CLI's `--help` for available commands.

### Global skill

Obtain and review the tagged checkout, then install its self-contained skill:

```sh
git clone --branch v0.2.0 --depth 1 https://github.com/pocheshire/agent-engineering-kit.git
cd agent-engineering-kit
python3 -B scripts/install_skill.py
```

The installer uses `~/.agents/skills/agent-engineering-kit`. A repeat is safe;
conflicting local changes stop the operation. Remove it with
`python3 -B scripts/install_skill.py --uninstall` from the reviewed checkout.

### Start a conversation

Open your target project in Codex and start a new chat. Ask, for example:

> Help prepare this project for autonomous development.

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

Download the [0.2.0 release ZIP](https://github.com/pocheshire/agent-engineering-kit/releases/download/v0.2.0/agent-engineering-kit-0.2.0.zip)
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

Repeated installation is safe. Upgrade preserves non-overlapping adaptations;
conflicts stop before writes. Recovery verifies the complete original pin and
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
| Portable KIT | Self-contained runtime and installation checks validated |
| Codex global skill | Installation/update/recovery checks; natural activation in an actual desktop app task |
| Codex repository plugin | Native CLI discovery, natural activation, maintenance and public-tag lifecycle validated |
| Claude Code plugin | Adapter prepared; host runtime untested |
| Cursor / other clients | Compatibility candidates; no runtime support claim |

No official directory submission or approval is claimed. See
[platforms](docs/platforms.md) for installation, activation, update, removal and
smoke tests for each entry.

Release 0.2.0 verification:

| Evidence | Result |
| --- | --- |
| Automated checks | 97 mandatory tests per CI job; six OS/Python configurations; zero skips |
| Independent behavior review | Four critical scenarios repeated twice; 8/8 passed objective → actions → final review |
| Fixture product checks | 32 independent test executions passed |
| Public-tag plugin lifecycle | Install, refresh, list and removal passed; all 55 package files matched |

[Release CI](https://github.com/pocheshire/agent-engineering-kit/actions/runs/42684485769)
and the [validation report](docs/validation.md) give the evidence and its limits.
Visual desktop UI inspection, certified uncached stability and universal agent
adherence are not established. Static integrity and valid JSON do not prove
product correctness or authentic execution. Zero or entirely skipped test suites
cannot establish successful mandatory coverage.

## Documentation and contributing

- [Agent entry](START_HERE.md) and [canonical engineering contract](skills/agent-engineering-kit/core/CONTRACT.md)
- [Installation and recovery](docs/installation.md), [platforms](docs/platforms.md), [compatibility](docs/compatibility.md)
- [Development workflows](docs/workflows.md) and [workflow record format](docs/workflow-format.md)
- [Evaluator isolation](docs/evaluation-isolation.md), [Codex permissions](docs/codex-permissions.md), [rollout observation](docs/codex-observation.md)
- [Contributing](CONTRIBUTING.md), [adapter development](docs/adapters.md), [security](SECURITY.md), [provenance](docs/provenance.md)

Licensed under [MIT](LICENSE).
