# Compatibility and updates

AEK uses semantic versions. Before 1.0, minor releases may change the contract;
read the changelog. A release candidate is a prerelease, not stable acceptance.
State files have an explicit schema. Unsupported schema versions must fail closed.

Vendored projects pin a runtime snapshot. Linked projects pin a relative source,
version and hashes; moving or modifying that source can make it unavailable.
Fetch a new release explicitly, review the diff and run Upgrade. Local managed
edits use three-way comparison and conflicts stop without writes. Keep local
adaptations in .aek/local.md and .aek/project.json. Do not automate forced merges.
Global skill updates affect future setup sessions, not already vendored projects.

Uninstall removes only unchanged managed content and the AEK marker; user-owned
adaptations are preserved. Inspect the output for any retained files. Removing a
host plugin or skill does not uninstall AEK from projects.
