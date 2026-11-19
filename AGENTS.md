# Maintaining Agent Engineering Kit

Read START_HERE.md for setup tasks. For AEK development, start with the
[scope and authority rules](skills/agent-engineering-kit/core/CONTRACT.md#authority-and-trust)
and [task router](skills/agent-engineering-kit/core/ROUTES.md#task-router).

For substantial work, delegate ready, independent items to subagents by
default within the current route and authority. Start implementation after
any required plan approval. After integration, review feedback, or resumption,
reassess the remaining work. Assign each newly ready independent item to a
subagent when capacity and cost allow, then verify the integrated result.
Follow the [workflow](skills/agent-engineering-kit/core/WORKFLOW.md#delegation-and-cost)
for suitable exceptions, worker scope, and the lead's integration checks.

Keep the runtime self-contained inside the single skill. Adapters contain metadata
and entry pointers only. Do not introduce copied private materials, credentials,
machine paths, hooks, telemetry, or runtime network dependencies.
Use `python3 scripts/validate.py` for the release gate. Installer and release
changes need independent review. Publish only with owner authorization and after
provenance/privacy checks. Report host runtime and catalog validation separately.
