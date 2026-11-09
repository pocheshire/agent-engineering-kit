# Platforms and distribution

Official documentation checked on 2026-11-09. AEK packages local instructions and
resources. It has no MCP server, hooks, telemetry, credentials or runtime network
calls. Downloads/updates are explicit operations. Host trust, tools, sandbox and
approval policies govern every action.

| Entry | Package | Validation status | Catalog |
| --- | --- | --- | --- |
| Portable | START_HERE.md | See [validation](validation.md) | GitHub release, not a native plugin |
| Codex global skill | Complete self-contained skill | See [validation](validation.md) | Local user installation |
| Codex plugin | plugin.json and repository marketplace | CLI native discovery/natural activation and maintenance trials passed (see validation) | No universal directory listing |
| Claude Code plugin | .claude-plugin manifests | Documented adapter; host unavailable | No submission |
| Cursor / other clients | Standard skill/package | Compatibility candidate; untested | No support/listing claim |

Manifest validity, installation, activation and project behavior are separate.

## Portable

Open START_HERE.md in a reviewed release and ask “Help prepare this project for
autonomous development.” Attaching an archive alone cannot guarantee activation.
Update by obtaining a reviewed release and requesting Upgrade. Remove the KIT
checkout only when linked projects no longer depend on it. Project removal is
separate; see [installation](installation.md).

## Codex global skill

```sh
python3 scripts/install_skill.py
```

Installs the whole skill into `~/.agents/skills/agent-engineering-kit`. Start a new
chat and say “Connect project settings to this project” or “Audit this project's
AEK setup.” Explicit fallback: `$agent-engineering-kit`. Repeat the installer from
a newer reviewed release to update; modified installations stop for analysis.
Use `python3 scripts/install_skill.py --uninstall` to remove. A receipt-pinned
unavailable installation can be restored from the exact trusted release with
`--repair`; confirmed existing damage requires explicit `--replace RELATIVE_FILE`.
Version/metadata or license mismatches and ambiguous local edits fail before writes.
Existing vendored
project installations do not change when the global skill changes.

Current Codex discovery uses `~/.agents/skills` for the user and `.agents/skills`
for projects. Name/description drives natural selection. Skills grant no extra
execution permission. [Official skill documentation](https://learn.chatgpt.com/docs/build-skills)

Smoke: install with `--skills-dir /path/to/test-skills`, check core/VERSION and
ENTRY.md, repeat to observe unchanged, then uninstall using the same directory.
That tests installation. To test activation, use a fresh chat with discovery
enabled and observe canonical entry reads after the natural request. Ordinary
feature work should not activate the setup skill.

## Codex repository plugin

The portable root plugin.json and compatibility .codex-plugin/plugin.json use
the same skill. Install a reviewed version:

```sh
codex plugin marketplace add pocheshire/agent-engineering-kit --ref v0.2.0
codex plugin add agent-engineering-kit@agent-engineering-kit
codex plugin list --json
```

For a local release, use `codex plugin marketplace add /path/to/agent-engineering-kit`.
Start a new chat and ask the natural setup question. Inspect/refresh with:

```sh
codex plugin marketplace list
codex plugin marketplace upgrade agent-engineering-kit
```

A source pinned to a tag stays on that tag. To change release, remove the source
and re-add the reviewed new tag, then refresh/install AEK. Check the skill version.
Remove with:

```sh
codex plugin remove agent-engineering-kit@agent-engineering-kit
codex plugin marketplace remove agent-engineering-kit
```

Commands are present in host 0.167.0-alpha.3.2; inspect your host's `--help`.
A repository marketplace differs from official directory publication.
[Official plugin packaging](https://developers.openai.com/plugins/build/plugins)

Smoke in isolated CODEX_HOME: add local marketplace, install, inspect cached
skill/core, list, remove and verify removal. A separate natural setup task proves
activation; package installation alone does not. For an isolated check, disable
the standalone global AEK by its exact SKILL.md path (not by name), then verify
that the sole enabled AEK skill comes from the installed native cache. Use a
separate test profile; do not modify your normal profile just to prove discovery.
The test report records the actual host/version and cache provenance.

## Claude Code: prepared adapter, runtime unverified

```sh
claude plugin marketplace add pocheshire/agent-engineering-kit
claude plugin install agent-engineering-kit@agent-engineering-kit
claude plugin list
```

Start a new session and ask “Set up this project for autonomous development.”
Explicit fallback: `/agent-engineering-kit:agent-engineering-kit`. Update with
`claude plugin update agent-engineering-kit@agent-engineering-kit`. Remove with
`claude plugin uninstall agent-engineering-kit@agent-engineering-kit`, then
`claude plugin marketplace remove agent-engineering-kit`. Third-party auto-update
is off by default; review the intended version before updating.
[Official management](https://code.claude.com/docs/en/discover-plugins)

When a host is available, smoke with `claude plugin validate . --strict`, local
installation, inventory, natural setup in a disposable project, then removal.
The adapter uses root skills, with no independent rule copy.
[Manifest](https://code.claude.com/docs/en/plugins-reference),
[marketplace](https://code.claude.com/docs/en/plugin-marketplaces)

## Compatibility candidates and directory publication

Shared metadata follows the [Agent Skills format](https://agentskills.io/specification).
Format compatibility does not prove host support. Cursor documents
[skills](https://cursor.com/docs/skills) and [plugins](https://cursor.com/docs/plugins),
but AEK has no Cursor runtime test or listing.

No official directory submission has occurred. OpenAI requires owner identity,
package upload and review; Anthropic has a separate eligible-account portal/review.
These remain manual owner steps after package and runtime checks; a public GitHub
repository does not imply completion. Prepare required catalog artwork and review
cases when submitting. [OpenAI submission](https://developers.openai.com/plugins/deploy/submission),
[Anthropic publication](https://code.claude.com/docs/en/plugins/publish)

## Troubleshooting

For missing activation, inspect discovery path, duplicate names and description;
restart the session. Missing VERSION/ENTRY means an incomplete installation:
restore the exact trusted pin under [recovery](installation.md#recover-unavailable-instructions), never silently fetch executable code.
For linked dependencies restore the pinned layout or analyze vendored migration.
Retain local rules when semantic conflicts arise; reinstall is not a resolution.

If an agent reports an old version, identify the actual loaded SKILL.md and its
colocated core/VERSION first. A global skill, native plugin cache, project pin and
portable checkout can have different versions; updating one does not update the
others. Do not silently substitute another source or assume a cache caused it.
Check that installation's receipt or marketplace ref. A tag-pinned RC marketplace
needs a deliberate new reviewed tag; refresh alone stays pinned. After updating,
start a new chat and verify the loaded version. Existing chat instructions are
not evidence that the on-disk update was reloaded. Project Upgrade is separate.
