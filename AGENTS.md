# Maintaining Agent Engineering Kit

Read START_HERE.md for setup tasks. For AEK development, read the canonical
[contract](skills/agent-engineering-kit/core/CONTRACT.md) and
[routes](skills/agent-engineering-kit/core/ROUTES.md).

Keep the runtime self-contained inside the single skill. Adapters contain metadata
and entry pointers only. Do not introduce copied private materials, credentials,
machine paths, hooks, telemetry, or runtime network dependencies.
Use `python3 scripts/validate.py` for the release gate. Installer and release
changes need independent review. Publish only with owner authorization and after
provenance/privacy checks. Report host runtime and catalog validation separately.
