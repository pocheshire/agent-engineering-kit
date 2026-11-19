# Agent entry

Use the current request and applicable project instructions to identify the target,
scope and allowed paths. Before inspecting project implementation, read the pinned
[authority and trust section](CONTRACT.md#authority-and-trust) and applicable local
adaptations. In an installed project the local entry resolves the runtime through
the project's state. A linked source may be outside the project. Follow the recorded
path when the current request, host permissions and project rules allow the read.
Ask before opening it when a specific restriction applies.

**Project work.** Start with the [task router](ROUTES.md#task-router). Read the table
and the section for your task. With shell tools, a range such as
`sed -n '/^## Task router$/,/^## /p' ROUTES.md` from the pinned core returns that
section. Leave setup and maintenance procedures closed during ordinary project
work. Follow further references when the trigger in your row occurs.

**Audit this installation.** Use the [Audit section](MODES.md#audit) of the
permitted installed pin. A request to check this project already authorizes a
read-only inspection within its access boundaries. A named external kit or an
explicit comparison with a newer version follows that source's access rules.

**AEK setup or maintenance.** From this complete loaded kit, read VERSION and
the [shared setup rules](MODES.md#setup-modes) and the section for the requested
operation before choosing a tool or writing.
Use its verifier even when an owner supplies an older release as pinned data.
Report the version and checks for the operation.

| Request | Read now |
| --- | --- |
| Prepare a new project | [Initialize](MODES.md#initialize) |
| Connect AEK to an existing project | [Adopt](MODES.md#adopt) |
| Check setup or readiness | [Audit](MODES.md#audit) |
| Update an installed project | [Upgrade](MODES.md#upgrade) |
| Restore the installed pin | [Recover an unavailable runtime](MODES.md#recover-an-unavailable-runtime) |

If intent or target is missing, ask one visible question in the user's language.
For a known project with unclear intent, ask whether to check its setup or adapt it.
If the question UI cannot confirm delivery, put the question directly in the reply.
Opening the kit alone supplies context. Wait for a needed decision before dependent writes.
