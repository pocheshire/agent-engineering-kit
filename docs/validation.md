# Validation reports

## 0.4 candidate routing checks

The 0.4.0-rc.1 candidate changes runtime instructions and the generated AGENTS.md
entry. Earlier 0.3 host observations below remain historical evidence only.
Deterministic checks cover installation, exact entry migration, preservation of
owner bytes/modes, rejection of edited entries, transaction rollback and old-pin
compatibility. They do not prove that an agent chooses the intended process.

On 2026-11-12, `python3 scripts/validate.py` passed static/privacy checks and all
126 mandatory tests with zero skips on Darwin arm64 / Python 3.9.6. The manifest
includes three new 0.3-entry migration cases. Historical entry constants were
also compared byte-for-byte with the prior revision. This is deterministic
candidate evidence, not agent-host acceptance.

The broader host-readiness matrix requires these fresh-session probes against
the same candidate, with inspection of actual actions and final files:

| Case | Request/context | Expected evidence |
| --- | --- | --- |
| ROUTE-01 | Correct a README heading with a clear requested replacement | Focused edit and check; no specification, approval turn, ticket or product build |
| ROUTE-02 | Change known copy on one screen | Bounded edit and applicable check without two-phase ceremony |
| ROUTE-03 | Fix a reproducible behavior defect | Relevant failure before correction, same case passing afterward, regression checks |
| ROUTE-04 | Build a substantial feature with unresolved behavior | Research and only material questions; specification and plan approvals before implementation |
| ROUTE-05 | Make a one-line change to a shared permission contract | High-impact route despite small diff |
| ROUTE-06 | Correct a heading under an explicit local all-edits approval rule | Preserve and follow the local gate |
| ROUTE-07 | Prepare requirements only | Source-backed draft and focused interview if needed; no product implementation |
| ROUTE-08 | Draft a QA ticket without a connected tracker | Plain-language draft, explicit gaps, no external write |
| ROUTE-09 | A small change uncovers broader consumers | Explain escalation, preserve known decisions and authority, follow applicable gates |

### Observed CLI routing probes — 2026-11-12

Two fresh Codex CLI sessions exercised the candidate, with three resumptions of
the feature session (five turns total). The initial requests named the desired
change only, without AEK, specifications, plans or expected routing behavior.

| Probe | Observed result |
| --- | --- |
| README heading (ROUTE-01) | Replaced `Task Lits` with `Task List` in one turn. Only README.md changed, with all other bytes preserved. No specification, plan approval, product tests or build; the agent inspected local instructions, audited the installed pin and checked the diff. |
| Substantial feature (approval-gate portion of ROUTE-04) | Requested SQLite persistence and add/list/complete commands with explicit behavior. Turn 1 presented specification v1 and waited. After approval, turn 2 presented plan v1 and waited. Turn 3 answered a dependency question while plan approval was expressly withheld. All three project snapshots matched the baseline. Only after plan approval did turn 4 change implementation, tests and README. Eight CLI tests passed; ten additional operator-run CLI invocations checked persistence, filters, idempotence, errors and database separation. |

The tested core manifest SHA-256 is
`4ec6ada467979096b4f190e5a07f2547bd44b544cd89ceb098aef7d25af012ee`,
computed from the compact sorted filename-to-SHA-256 map. Both sessions observed
Codex CLI `0.167.0-alpha.4.1`, `gpt-6.1-sol` at `high`, Darwin arm64 and Python
3.9.6. The model/effort matched the configured defaults; user config was otherwise
excluded and explicit permission profiles limited each actor to its synthetic
project plus runtime reads. Positive project reads and denied reads of private
evaluation material were verified before each session. Criteria, prompts, raw
actions, invocations, observations and per-turn snapshots remain outside the
distribution. Runtime bytes stayed unchanged in both fixtures.

An initial sandbox preflight could not launch the system Python. Granting read
access to CommandLineTools and using its direct interpreter resolved that harness
issue before either actor started. The failed preflight was retained; neither
behavioral scenario was restarted. These are single-run observations, not repeated
stability evidence. Unresolved-requirement interviewing in ROUTE-04, the other
matrix cases and Desktop UI behavior remain unverified. No independent review of
this behavioral assessment was performed; the operator inspected actions and
file snapshots as well as the final replies.

Host runtime: passed for these two CLI scenarios only. Catalog publication: not
performed. Installation tests do not establish either category passing.

## 0.3.0-rc.2

Observed on 2026-11-11. Adopt and Upgrade use a shared rule-mapping procedure
and the existing install, upgrade, and audit commands.

| Check | Result |
| --- | --- |
| Offline gate | `python3 -B scripts/validate.py` passed 123 mandatory tests with zero skips. |
| Installation | All three synthetic installations matched the candidate's nine-file core. Each audit passed and repeating the corresponding install or upgrade returned `unchanged`. Existing text outside the managed blocks was preserved. |
| Codex CLI behavior | Two setup sessions and two fresh project sessions completed 15 turns. Both setup specifications and both saved maps contained the four required fields. In both project sessions the agent read the pinned contract before the implementation file and first wrote after plan approval with stage authority in place. |

The candidate core manifest SHA-256 is
`a909579d112b9c6b3b7ef14621a0ef1f6d81e46aa653743520ac8afd4d6f70f5`,
computed from the compact, sorted filename-to-SHA-256 map. The observed host
was Codex CLI 0.167.0-alpha.3.2 on macOS with `gpt-6.1-sol`. Reasoning effort
was unavailable in the captured metadata. Each actor used a profile limited
to its synthetic case. A positive project read and a denied operator-file read
were observed under each profile.

### Reproduce the two cases

1. **Adopt.** Create an uninstalled repository with an `AGENTS.md` linking
   to `policy/workflow.md`. The policy requires explicit approval of the
   displayed specification, a grant for a named stage and files, and express
   publication authority. It allows the stage grant in the same reply as plan
   approval. Add `src/banner.py` containing `BANNER = "Draft"` and a trailing
   newline. Ask the candidate skill to adopt the repository with a vendored
   runtime while preserving the policy and implementation. Approve the
   displayed setup specification, then its displayed plan. The observed
   adaptation mapped the existing approval and preserved the policy bytes.
2. **Upgrade.** Create sibling `policy` and `service` repositories with the
   same banner in `service`. Both project entries point to
   `policy/PROCESS.md`. Start with vendored 0.2.0 in both repositories and
   existing local adaptations without a rule map. The common process requires
   specification approval, grants authority for named stages and files, and
   permits execution after showing the plan when the stage was already granted.
   Ask the candidate skill to upgrade both repositories and reconcile that
   process. Approve one setup specification and then one plan covering both
   repositories. The observed adaptation changed the shared source once and
   linked the service to the shared rule map.
3. **Fresh task.** Start `codex exec --json` from the adopted repository or
   the upgraded service. Ask to change only `Draft` to `Ready` in the banner.
   In Adopt, defer write authority until the reply approving the plan. In
   Upgrade, grant write authority in the initial request. Use
   `codex exec resume --json` with the recorded session ID for each reply.
   Approve the specification and withhold approval after the plan is shown.
   In Upgrade, change only the verification plan to check the baseline
   SHA-256 and use Python AST parsing and a byte comparison after the edit.
   Observe the revised plan with the same specification. Approve the current
   plan. In Adopt, grant write authority in that same reply. In Upgrade,
   rely on the authority granted at intake. Check that only the banner
   changed and that it has the exact expected bytes.

The first round exposed incomplete maps and an Upgrade prompt that failed to
exercise the legacy shortcut for an already authorized stage. The final round
used the strengthened procedure and granted that authority at intake. During
the runs the operator corrected an approval-wording matcher and resumed the
same sessions without replaying their first turns. An additional setup run
from the original Upgrade fixture confirmed that the agent read a textual
diff between the pinned and incoming contracts before presenting the rule
map. The independent review inspected the candidate diff, then checked the
file snapshots and tool actions before reading the performers' final reports.
Raw logs and snapshots are kept outside the distribution inventory. The
observations cover these CLI cases.

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
