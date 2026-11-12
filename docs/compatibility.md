# Compatibility and updates

AEK uses semantic versions. Before 1.0, minor releases may change the contract;
read the changelog. Prerelease tags remain historical candidates; 0.1.0 is the first stable release for the validated channels.
Version 0.2 adds WORKFLOW.md and workflow.py to the self-contained core and a
separate version-1 workflow record format. The current verifier accepts original
seven-file 0.1 pins for exact recovery and three-way Upgrade. It never adds the
new files during recovery. Upgrade adds them only with the new version, while
retaining non-overlapping local changes and stopping on shared-file conflicts.
Project state/adaptation schema remains 1; optional records are not required for
ordinary development and are not rewritten by the installer.
State files have an explicit schema. Unsupported schema versions must fail closed.

Stable 0.4.0 additionally requires DOCUMENTATION.md in its ten-file core. The
nine-file 0.4.0-rc.1 candidate remains valid for exact recovery; Upgrade to 0.4.0
adds the writing rules and revises routes. Historical recovery does not add files
from a newer release. No project-state schema migration is needed.

Vendored projects pin a runtime snapshot. Linked projects pin a relative source,
version and hashes; moving or modifying that source can make it unavailable.
Fetch a new release explicitly, review the diff and run Upgrade. Vendored three-way
comparison can retain a non-overlapping project-local runtime edit while
applying the incoming snapshot. Linked Upgrade must also switch the shared source
pointer. It stops without writes if an old-source edit is absent from the incoming
source, even when only VERSION changed upstream. Review the change and either
keep the old pin until resolved, represent an intended project-specific change
as an explicit project adaptation, or copy the new release into an owner-controlled
source, carry the adaptation there, verify it, and retry with that source. Do not
alter a shared checkout or force the pointer past the conflict.
Keep project adaptations in `.aek/local.md` and `.aek/project.json`. Do not
automate forced merges.
Global skill updates affect future setup sessions, not already vendored projects.

Upgrade compares strict SemVer precedence (numeric prerelease components, build
metadata excluded). It refuses downgrades and different content at the same
precedence. Unsupported state/adaptation schemas fail before writes. Major
transitions require an explicitly reviewed migration. These checks do not replace
semantic review of contract changes.

Recovery restores exact pinned bytes from a trusted complete release and does
not change versions. Missing files may be restored; existing divergence requires
an explicit confirmed-damage replacement. A linked source outside the project
requires its own write authority. Do not use Upgrade or altered receipts as repair.

Uninstall removes only unchanged managed content and the AEK marker; user-owned
adaptations are preserved. Inspect the output for any retained files. Removing a
host plugin or skill does not uninstall AEK from projects.
