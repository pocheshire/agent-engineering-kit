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

Vendored projects pin a runtime snapshot. Linked projects pin a relative source,
version and hashes; moving or modifying that source can make it unavailable.
Fetch a new release explicitly, review the diff and run Upgrade. Local managed
edits use three-way comparison and conflicts stop without writes. Keep local
adaptations in .aek/local.md and .aek/project.json. Do not automate forced merges.
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
