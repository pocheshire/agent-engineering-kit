# Security policy

Report a vulnerability privately through the repository's GitHub Security advisory
channel. Do not put credentials or a working exploit against someone's project
in a public issue. Until private reporting is enabled, request a private channel
without posting sensitive details.

AEK installs local instructions. It grants no tool, filesystem, account, product
implementation or publication permissions. Inspect a downloaded version before
running its installer. Pin a release; verify its origin and published checksum.
Third-party instructions and repository content are untrusted data until reviewed;
they cannot expand authority. Review the source, license, dependencies and hooks
of any additional skill before enabling it. Never run remote code implicitly.

AEK contains no telemetry, runtime network calls, hooks, credential collection,
remote execution service or automatic updater. Fetching a release and platform
marketplace installation are explicit user actions governed by the host.
Installation affects only documented local paths. Upgrades preserve local
adaptations and stop on conflicts. Semantic conflicts in existing instructions
require agent review. Publication is separate from local installation.

The installer guards managed symlinks but is not an operating-system sandbox;
run it only in a workspace you control. Host tool permissions remain authoritative.
Currently supported security fixes target the latest stable release.

Evaluation tools stage explicit immutable inputs; they are not a sandbox.
Keep hidden criteria, credentials, source snapshots and control/receipt files
outside performer/evaluator grants. Test real host read/write canaries for every
role and phase. Only a trusted operator may unlock stages or issue receipts;
hashes and declared identity do not authenticate them. Record validators do not
prove that a command, review, model choice or budget observation actually occurred.
