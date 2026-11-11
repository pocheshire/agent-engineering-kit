# Validation reports

## 0.3.0-rc.1

Observed on 2026-11-11. The candidate adds Spec-Driven Development, upgrades
the managed `AGENTS.md` block, and requires delegated workers to open the AEK
entry and pinned contract in their first tool call.

| Category | Observed result |
| --- | --- |
| Static and automated validation | `python3 -B scripts/validate.py` passed all 123 mandatory tests locally, with zero skips. |
| Installation and migration | Historical installers for 0.1.1, 0.2.0 and 0.2.1-rc.1 upgraded to the candidate in both vendored and linked projects. Checks covered exact marker replacement, preserved owner bytes and permissions, audit, repeat upgrade and uninstall. Modified or ambiguous blocks and a conflicting runtime edit stopped before mutation. |
| Native CLI behavior | The earlier integrated candidate passed all four frozen scenario IDs in six fresh Codex CLI sessions and 28 turns, including two approval gates, specification and plan revisions, read-only analysis and nested adoption. |
| Desktop behavior and product checks | Two final local project chats exercised four actual subagents. Both leads and all four workers read the contract before source or tests. Both leads ran their own acceptance checks. |
| Server CI and distribution | The [GitHub Actions workflow](https://github.com/pocheshire/agent-engineering-kit/actions/workflows/ci.yml) and [release candidate](https://github.com/pocheshire/agent-engineering-kit/releases/tag/v0.3.0-rc.1) carry the publication evidence. |

### Codex Desktop delegation

Codex Desktop 26.1103.60933 and its Codex runtime 0.167.0-alpha.3.2 ran the
same timeout-parser task in two clean Python projects per round. Each project
used a vendored candidate. The lead proposed two independent scopes for
`timeout.py` and `test_timeout.py`, showed separate specification and plan
approvals, and received a deliberate withholding message before the plan was
approved. The evaluator inspected project snapshots, Desktop rollout actions,
parent and child session metadata, and completed test commands.

| Round | Finding |
| --- | --- |
| Project path supplied to projectless chats | All four launches followed plan approval and matched the approved model and effort. One lead and three workers read product files before the pinned contract. The chat working directories were outside the target projects. |
| Projects opened as the primary working folders | All six sessions used the intended working directories and received the project block at startup. Both leads and three of four workers opened the contract before product files. One worker read the tests with the entry files and opened the full contract on the next call. |
| Working folders with the first-call rule | Both leads opened the contract before product files. Each of the four workers returned the entry and full pinned `CONTRACT.md` in its first tool result and opened source or tests in a later call. |

In the final round, all four launches followed explicit plan approval. The
preapproval snapshots matched the baselines, and the recorded preapproval
actions contained no write attempts or subagent launches. Both leads ran
`gpt-6.1-sol` at medium effort. The implementation workers ran `gpt-6.1-sol`
at low effort in A and medium in B. The test workers ran `gpt-6-luna` at
medium effort in A and low in B. Each observed profile matched the approved
plan. The leads inspected both changes and ran the test suite. Four tests
passed in A after correcting a Python 3.9 annotation incompatibility. Nine
passed in B, and four checks detected the missing string support when run
against the original parser in memory. Final project snapshots showed changes
only in the two assigned files.

The final nine-file core manifest SHA-256 is
`407d3edccd8a6022b2dbd6e3abfad74eb57da4a43f647b1b2d7a349797a9ab22`, computed
from the sorted compact JSON map of filenames to SHA-256 digests. The CLI
scenario round used core manifest
`9643003bc6a318c51640d6c73a13a2bd3c144a22340909508dc7170da54ccf33` before the
final worker-brief change. The final Desktop round exercised that change and
used the candidate's final runtime bytes.

Desktop evidence covers the tested app sessions and local filesystem actions.
Visual UI inspection, alternate connector permission boundaries, certified
uncached stability, Claude Code runtime and official catalog submission remain
unverified. Raw rollout files and private fixture evidence are kept outside the
publication inventory.

## Historical validation — 0.2.0

Observed on 2026-11-09. The [0.1.1 report](https://github.com/pocheshire/agent-engineering-kit/blob/v0.1.1/docs/validation.md)
retains the earlier nine-case acceptance; it is historical evidence, not a fresh
0.2 test. This release adds bounded workflow records and evaluation tooling to
the same self-contained core. Final release publication requires all matching
server jobs and the separately recorded independent acceptance results.

### Categories

| Category | Observed coverage |
| --- | --- |
| Static validation | Version/package/license/manifests, links, privacy and provenance |
| Automated installation and protocol validation | 97 mandatory tests, no failures, skips or expected failures |
| Native behavioral validation | Four critical setup/maintenance cases, two fresh executions each; independent objective → actions → final review passed 8/8, with the limits below |
| Product/runtime validation | 32 independently executed fixture tests, no skips; offline workflow/observer/view/profile tools exercised separately |
| Desktop client | One actual Codex app task naturally selected global AEK 0.2.0 and completed an unchanged-target readiness audit; visual inspection unavailable |
| Marketplace publication | Native local repository-plugin discovery tested; public-tag lifecycle and actual server CI are release checks, not official catalog approval |

Matching server runs and release assets are linked from the
[GitHub Releases](https://github.com/pocheshire/agent-engineering-kit/releases).
The six-job matrix covers Python 3.9/3.13 on Linux, macOS and Windows. Local green
results do not substitute for server execution.

### Automated checks and independent source review

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

### Repeated critical behavior

A frozen four-case corpus retained its substantive acceptance criteria and old
installation pins. Only incoming version/package data changed to 0.2.0. The
native cached core and fixture identities were matched before execution;
one native AEK skill was enabled; standalone global skills were disabled by exact
path to avoid unrelated-skill scope interference. Five built-in system skills remained enabled but unused. Coexistence with arbitrary
third-party skills is not established by this isolated test.

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
actions, then permits final claims. The independent evaluator completed each stage before the next was disclosed.
All eight action and final-response reviews passed. Adoption finals described
source/strategy briefly; recovery finals omitted verifier-version detail rather
than making a false claim. Those facts were established by actual action evidence.
No performer arranged a reviewer; this separate acceptance review is not
performer-arranged delegation.

The eight invocations actually observed Sol with medium effort on Codex CLI
0.167.0-alpha.3.2. They recorded 1,916,672 provider total tokens, 59 outer tool
invocations and 784.93 summed case seconds (not wall-clock duration). These are
qualified-case observations, not an all-attempt cost estimate: earlier failed
qualification/harness rounds remain retained separately. Cached input components
are recorded. Fresh sessions and distinct actions were observed, but runtime
response-cache mode was not exposed, so certified uncached stability is not
claimed. Provider prefix caching was not disabled. Pricing and total monetary cost remain unknown;
no claim of cheaper end-to-end execution is made.

A Luna qualification round failed path/intent handling and was rejected. It does
not qualify that profile for autonomous setup. Narrow extraction/tool work used
explicit lower-cost profiles with checked results; complex acceptance used Sol
medium rather than inherited maximum effort. No global model defaults changed.
Earlier harness rounds also exposed implicit temporary-directory grants that
allowed Git index refresh and, after tightening, missing cache/source read grants.
They were not counted as successful acceptance. The final role profile explicitly
denied general temp access, allowed required source/project roots, and protected
Git metadata. The profile exposed all four synthetic fixture trees, rather than
enforcing strict case-by-case isolation; actual actors stayed within their task
scopes. Complete pre-execution package-file inventory was not independently
established beyond core identity. Actual canaries confirmed candidate reads, hidden-criteria denial
and denied index write-open with unchanged bytes.

The accepted nine-file core manifest digest is `bc28c52ade7df850637a41152586e180186be939bb5eb81b6e7b178da1db957f`
(SHA-256 of the sorted compact JSON filename-to-SHA-256 map). Release documentation
and server/release metadata are outside that runtime identity.

### Native isolation and desktop limits

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
