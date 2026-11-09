# Validation report — 0.2.0

Observed on 2026-11-09. The [0.1.1 report](https://github.com/pocheshire/agent-engineering-kit/blob/v0.1.1/docs/validation.md)
retains the earlier nine-case acceptance; it is historical evidence, not a fresh
0.2 test. This release adds bounded workflow records and evaluation tooling to
the same self-contained core. Final release publication requires all matching
server jobs and the separately recorded independent acceptance results.

## Categories

| Category | Observed coverage |
| --- | --- |
| Static validation | Version/package/license/manifests, links, privacy and provenance |
| Automated installation and protocol validation | 97 mandatory tests, no failures, skips or expected failures |
| Native behavioral validation | Four critical setup/maintenance cases, two fresh executions each; objective state passed 8/8; independent action/final review is a separate release gate |
| Product/runtime validation | 32 independently executed fixture tests, no skips; offline workflow/observer/view/profile tools exercised separately |
| Desktop client | One actual Codex app task naturally selected global AEK 0.2.0 and completed an unchanged-target readiness audit; visual inspection unavailable |
| Marketplace publication | Native local repository-plugin discovery tested; public-tag lifecycle and actual server CI are release checks, not official catalog approval |

Matching server runs and release assets are linked from the
[GitHub Releases](https://github.com/pocheshire/agent-engineering-kit/releases).
The six-job matrix covers Python 3.9/3.13 on Linux, macOS and Windows. Local green
results do not substitute for server execution.

## Automated checks and independent source review

The mandatory gate checks exact discovered, started and successful IDs. It
rejects zero/all-skipped suites, missing/replaced/duplicate IDs, skipped subtests
and expected failures. New negative controls cover missing nullable fields,
nonfinite values, stale revisions, dropped/downgraded unresolved findings,
cumulative failed-attempt usage, unknown budget usage, missing actual review,
replayed traces, incomparable configurations, incomplete modernization receipts,
view leakage and tampering, path aliases, Unicode TOML and permission boundaries.

Independent source review found and corrected three record-gate defects and two
path-rendering defects before release. The reviewer separately tested actual
original 0.1.1 seven-file bytes from Git: exact recovery preserved state and pin;
Upgrade added the new resources and audited successfully. New current-version
packages require all nine runtime files. Installed sibling dispatch was exercised
from a hostile working directory, including unavailable-helper failure.

The rollout observer was checked against real native metadata. Requested and
observed model/effort remain separate, conflicting/missing values stay unknown,
and provider cumulative usage is not summed across snapshots. Conversation text,
reasoning, tool arguments/results, environment and credentials are excluded.
Record validation and hashes establish consistency, not authenticated provenance.

## Repeated critical behavior

A frozen four-case corpus retained its substantive acceptance criteria and old
installation pins. Only incoming version/package data changed to 0.2.0. The
native cached candidate and fixture identities were matched before execution;
one native AEK skill was enabled and the global AEK disabled by exact path.

| Case | Two-repeat objective result |
| --- | --- |
| Audit before installation | 2/2: substantive readiness path, no installation or file/index changes |
| Natural existing-project adoption | 2/2: managed AGENTS append, exact candidate runtime, owner/product bytes retained |
| Non-overlapping Upgrade | 2/2: new files/version installed, local ROUTES retained, integrity audit honestly reports that adaptation |
| Unavailable linked runtime | 2/2: exact original seven-file pin restored by current verifier; all project bytes unchanged |

A separate independent mechanical grader checked full parent-file/directory
expectations and preserved actual roots. Tests/audits ran on hash-verified private
copies. Entire generated local.md/project.json and changed prose remained opaque
in the first evaluator view; hashes and machine observations were available.
The physical disclosure tool seals objective verdict, then permits complete raw
actions, then permits final claims. Independent reviewer receipts are required
before treating action/final acceptance as complete.

The eight invocations actually observed Sol with medium effort on Codex CLI
0.167.0-alpha.3.2. They recorded 2,027,610 provider total tokens, 62 outer tool
invocations and 707.38 summed case seconds (not wall-clock duration). These are
qualified-case observations, not an all-attempt cost estimate: earlier failed
qualification/harness rounds remain retained separately. Cached input components
are recorded; fresh invocations did not reuse saved answers or verdicts. Provider
prefix caching was not disabled. Pricing and total monetary cost remain unknown;
no claim of cheaper end-to-end execution is made.

A Luna qualification round failed path/intent handling and was rejected. It does
not qualify that profile for autonomous setup. Narrow extraction/tool work used
explicit lower-cost profiles with checked results; complex acceptance used Sol
medium rather than inherited maximum effort. No global model defaults changed.
Earlier harness rounds also exposed implicit temporary-directory grants that
allowed Git index refresh and, after tightening, missing cache/source read grants.
They were not counted as successful acceptance. The final role profile explicitly
denied general temp access, allowed required source/project roots, and protected
Git metadata. Actual canaries confirmed candidate reads, hidden-criteria denial
and denied index write-open with unchanged bytes.

## Native isolation and desktop limits

Real Codex sandbox probes exercised all three evaluator phases. The permitted
phase file was readable; private snapshot, narrator-final/control data and view
writes were denied until their appropriate transition. The initial, actions and
final profiles were each tested. A separate four-profile native matrix confirmed
read/deny behavior beneath a writable root with general temp access disabled.
This is evidence for the tested filesystem/shell surface on macOS, not proof that
all possible connected tools, operating systems or privileged processes are isolated.
Receipts belong to a trusted operator; they are not authentication mechanisms.

An owner-authorized new Codex desktop task used an ordinary readiness request
without a skill name. Its command log confirms the global 0.2 entry, bounded audit
and accurate uninstalled/runtime limits. The two target files remained exact.
This tests the app task channel with the global skill, not native-plugin desktop
UI discovery. Computer Use refused access to the Codex app, so no screenshot or
visual control verification is claimed. Native repository-plugin behavior was
validated separately in the CLI. New bounded-workflow/model-coordination advice
is not a guarantee of universal agent adherence or an automatic reviewer service.

Claude Code remains a prepared, untested adapter. Other clients and official
catalog submission/approval remain unverified. See [platforms](platforms.md),
[workflow records](workflow-format.md), [isolation](evaluation-isolation.md),
[permissions](codex-permissions.md) and [compatibility](compatibility.md).
