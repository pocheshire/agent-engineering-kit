# Agent Engineering Kit (AEK)

AEK gives a team one way to ask coding agents for changes, review decisions
and check the result across chats. Connect it to a repository when you want
agents to use the project's own rules and tests, bring product decisions to
the owner and show what they verified before handing work back. Each project
pins its workflow version and chooses when to upgrade.

[![AEK checks](https://github.com/pocheshire/agent-engineering-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/pocheshire/agent-engineering-kit/actions/workflows/ci.yml)

**[Stable release 0.5.0](https://github.com/pocheshire/agent-engineering-kit/releases/tag/v0.5.0)** · [Previous release 0.4.5](https://github.com/pocheshire/agent-engineering-kit/releases/tag/v0.4.5) · [Changelog](CHANGELOG.md) · [MIT license](LICENSE)

## How work moves through AEK

Describe the task in ordinary language or choose a workflow skill in Codex.
The agent reads the project's pinned instructions, inspects the relevant code
and chooses checks that exercise the behavior you asked for.

| Your request | Codex skill | What comes back |
| --- | --- | --- |
| “Read the export command and prepare a specification for tab-separated output.” | `aek-spec` | A versioned specification with scope, observable requirements, acceptance checks and decisions for approval. A supplied draft goes through the same template with proposed changes shown to the owner. |
| “Implement the new export format.” | `aek-feature` | For substantial work, a specification for approval, then a plan for separate approval. Implementation follows plan approval. The lead integrates the work and reports check results. |
| “Rename this command in the help text.” | `aek-small-change` | A focused edit and a check of the affected help output. |
| “The exporter drops the last row. Fix it.” | `aek-bugfix` | A reproducer that shows the missing row, a fix and the result of rerunning the same check. |

For example, an agent preparing the export specification can inspect the
existing CSV output and the scripts that consume it. If the brief leaves the
handling of incomplete orders open, the agent brings that decision to the
owner. One possible acceptance check is that an order missing its quantity
produces a diagnostic and an empty output stream. A document-only request ends
with the specification. If you then ask to implement it, the agent reuses the
approved version, presents the plan and waits for plan approval. Substantial
plans normally get an independent review. After approval the lead delegates
independent work when the host and project permit it, then verifies the
combined result.
[Worked export specification](skills/agent-engineering-kit/core/SPEC_EXAMPLE.md) ·
[Specification template](skills/agent-engineering-kit/core/SPEC_TEMPLATE.md) ·
[Workflow and delegation](docs/workflows.md#select-a-workflow)

## Quick start with Codex

Use the repository plugin for the setup skill and all four named workflow
skills. The standalone global skill provides the setup entry. Both use the
same engineering core. AEK's local tools require Python 3.9 or later.

### Repository plugin

Install the stable tag in Codex CLI.

```sh
codex plugin marketplace add pocheshire/agent-engineering-kit --ref v0.5.0
codex plugin add agent-engineering-kit@agent-engineering-kit
codex plugin list --json
```

Next, open the repository you want to connect as the primary project in Codex.
Start a new chat and ask “Connect AEK to this repository and preserve its
existing engineering rules.” The agent inspects the repository and proposes a
setup for approval. For a read-only assessment, ask “Audit this project's
readiness for AEK.” If you already use an older marketplace tag, follow the
[tag-switch procedure](docs/platforms.md#codex-repository-plugin).

### Global skill

Install the self-contained skill from the reviewed release checkout.

```sh
git clone --branch v0.5.0 --depth 1 https://github.com/pocheshire/agent-engineering-kit.git
cd agent-engineering-kit
python3 -B scripts/install_skill.py
```

The installer uses `~/.agents/skills/agent-engineering-kit`. You can rerun it safely.
Conflicting local changes stop the operation. Remove it with
`python3 -B scripts/install_skill.py --uninstall` from the reviewed checkout.

After installation, open the target project in a new chat and make the same
setup request. You can select `$agent-engineering-kit` explicitly or ask in
your own language, for example «Подключи AEK к текущему проекту». In subsequent
chats, open the project as the primary folder so Codex can read its
`AGENTS.md` instructions.

## Portable use

Download the [0.5.0 release ZIP](https://github.com/pocheshire/agent-engineering-kit/releases/download/v0.5.0/agent-engineering-kit-0.5.0.zip)
and [SHA256SUMS](https://github.com/pocheshire/agent-engineering-kit/releases/download/v0.5.0/SHA256SUMS),
or use a reviewed tagged checkout. Give the directory to your agent and say:

> Read START_HERE.md. Help prepare /path/to/my-project for autonomous development.

After opening [START_HERE.md](START_HERE.md), the agent discovers the target and
intent. If only the KIT was supplied, it asks one short question about the missing
target or whether to audit or adapt. Clear intent needs no repeat question.
Attaching an archive alone does not guarantee activation on every platform.

## What happens in your project

The setup skill chooses an operation from your request.

| Operation | Result |
| --- | --- |
| Initialize | Discover requirements, propose architecture and prepare the engineering environment |
| Adopt | Map existing project rules to AEK, apply the approved setup and verify the adapted workflow |
| Audit | Review readiness or installed conformance without making changes |
| Upgrade | Compare old baselines and incoming files, revisit affected rules and verify the adapted workflow |
| Recovery | Restore the trusted, exact installed pin within the authorized scope |

On adoption, the installer appends a pointer to `AGENTS.md` and records
project settings in `.aek/`. Commit the managed instructions and the default
vendored runtime to give other contributors the same workflow on checkout. An audit can
also assess an existing project's readiness before you connect it.

| Integration | Dependency arrangement |
| --- | --- |
| Vendored — default | The project stores its pinned runtime and loads it directly during development |
| Linked | The project uses a pinned, reachable relative source, which may be outside the project |

Repeated installation is safe. Vendored upgrades carry forward
non-overlapping local edits and report conflicts for review. Linked upgrades
check that the new source preserves local edits in the old source. Recovery
uses the exact recorded version. [Installation and recovery guide](docs/installation.md)

## Updating AEK

1. Update the Codex entry. For the repository plugin, switch the
   marketplace to the new tag and reinstall the plugin. For the standalone
   skill, rerun its installer from the new tagged checkout. [Tag-switch commands](docs/platforms.md#codex-repository-plugin)
2. Open the target project in a new chat and ask “Upgrade this project's AEK
   pin to 0.5.0 and verify its setup.” The project keeps its previous workflow
   until this upgrade. For a linked installation, review the shared source
   before changing it. [Compatibility policy](docs/compatibility.md)

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
| Portable KIT | Offline release checks cover installation, upgrade, conflict handling and recovery. |
| Codex repository plugin | On 0.5.0-rc.1, Codex CLI and the Desktop backend exposed the setup entry and all four workflow skills. A fresh Desktop chat selected the specification skill from an ordinary request and produced a document for approval. |
| Codex global skill | The standalone setup skill has installation, update and recovery checks and historical Desktop setup trials. |
| Claude Code | Adapter available. Runtime verification is pending. |
| Cursor and other clients | Runtime compatibility is unverified. |

GitHub hosts the release and repository marketplace. Official directory listing
has a separate submission and review process. [Validation reports](docs/validation.md)
· [Platforms and installation](docs/platforms.md)

## Documentation and contributing

- [Agent entry](START_HERE.md) and [canonical engineering contract](skills/agent-engineering-kit/core/CONTRACT.md)
- [Installation and recovery](docs/installation.md), [platforms](docs/platforms.md), [compatibility](docs/compatibility.md)
- [Development workflows](docs/workflows.md) and [workflow record format](docs/workflow-format.md)
- [Evaluator isolation](docs/evaluation-isolation.md), [Codex permissions](docs/codex-permissions.md), [rollout observation](docs/codex-observation.md)
- [Contributing](CONTRIBUTING.md), [adapter development](docs/adapters.md), [security](SECURITY.md), [provenance](docs/provenance.md)

Licensed under [MIT](LICENSE).
