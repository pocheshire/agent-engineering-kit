# Validation reports

## 0.5.1 release

The 13-file stable runtime matches the final trial installation (0.5.1-rc.9)
byte for byte except for its VERSION marker. The stable manifest SHA-256 is
`107fcb68bbe130b53023287b9f189e3c624a5ac257e2519f1099e3eeaa6ec345`.
Four local upgrade probes covered both 0.5.0 and the final candidate, each
installed as a vendored copy and as a link. All four upgraded and audited
successfully, reported an unchanged repeat upgrade and restored the owner's
original AGENTS.md bytes on uninstall.

The offline release gate passed all 143 required tests with zero skips. In an
isolated profile, Codex CLI 0.169.0 installed and enabled 0.5.1 from a local
repository marketplace. The app-server listed all five enabled skills from the
plugin cache. The cached skills and core matched the release inputs. These
checks cover local installation and discovery. A fresh Desktop chat on the
stable tag, server CI and official catalog acceptance are separate checks.

Two paired Codex CLI trials compared the final candidate with GitHub Spec Kit
1.4.5 using its bundled `speckit` 1.0.2 workflow. Each pair used the same
source snapshot, gpt-6.1-sol at medium reasoning effort, preregistered external
checks and a designated owner's representative. Time ran from the first task
dispatch to the representative accepting the exact patch after a clean replay.

| Local acceptance | AEK | Stock Spec Kit |
| --- | --- | --- |
| Generate a dotenv template for developers and CI | 17/17 external checks, 306 pytest cases, 18m 31s, 3 representative contacts | 17/17, 300 pytest cases, 15m 25s, 3 contacts |
| Open a transaction from a paginated iOS history | 26/26 external checks, 52 XCTest cases, 19m 35s, 5 contacts | 26/26, 51 XCTest cases, 38m 24s, 4 contacts |

The CLI task used python-dotenv v1.2.4 on CPython 3.11.16. AEK encountered
two model capacity waits that partly overlapped independent work. The iOS
trial used Xcode 27.2 and an iPhone 17 Pro simulator on iOS 27.2. AEK asked
about fields and navigation before drafting. Spec Kit's first specification
was rejected. On the next run the engine reported completion with no product
diff. After the operator corrected a sandbox read restriction, the same
implementation session delivered the patch through the installed Spec Kit
implementation command. Elapsed time includes this recovery. Neither trial
measured a human owner's active reading time.

Independent reviewers examined the final AEK files in each trial. In the
Spec Kit runs, a separate agent helped with planning and the author reviewed
the final patch. A masked reader assessed each author's reply and durable
handoff for an explicit local decision, a release decision, remaining checks
and evidence for the recommendation. AEK scored 4/4 in both CLI channels and
3/4 (reply), 4/4 (document) on iOS. Spec Kit scored 1/4 in all four channels
for naming outstanding checks. These scores describe handoff quality.
Both products passed the shared behavioral checks. The iOS acceptance covered
real taps, the displayed values and return to the same list position.
Actual VoiceOver speech remained unresolved and neither patch was released.

## 0.5.1-rc.9 candidate

A fresh Codex CLI session repeated the strict-mode API request
on python-dotenv v1.2.4 with the original acceptance criteria. The agent recommended
local acceptance in both its final reply and its handoff. It also recommended
holding release for lint, type, packaging and supported CI checks. A separate
reviewer examined all four product files. Their SHA-256 hashes matched the
files obtained by applying the delivered patch to the pinned upstream commit.
All 38 external cases and 388 project tests passed. The representative then
accepted that revision locally.

Independent kit review covered upgrading a vendored and a linked consumer.
The offline kit suite passed all 143 tests. The behavioral evidence covers one
Codex CLI run. Desktop activation, catalog acceptance and publication were
outside this trial.

## 0.5.1-rc.8 candidate

The preparation checks reused the original python-dotenv request
and the one-sentence history-screen request from the
[rc.6 trials](#051-rc6-candidate). Fresh, write-enabled
Codex sessions used clean project snapshots and the installed candidate. The
operator froze the prompts and criteria before launch, compared messages,
tool events and file snapshots, and answered only the questions the agent asked.

The intermediate rc.7 passed both file-approval checks on python-dotenv. On
iOS it asked about the ordinary list before drafting, then chose empty and
error behavior without asking. Its first specification declared no open
questions. This prompted the rc.8 change to check the remaining acceptance
choices again after each answer. The rc.8 runtime manifest SHA-256 was
`c26d7866f48213808d0ae926595bc97f5d432fc7e46fc5ad63188305e75ed8fa`.

| Final rc.8 trial | Observation |
| --- | --- |
| python-dotenv v1.2.4, original ambiguous brief | The agent showed the specification file, version and full byte-verified `spec_id`. The representative approved by path and version. A separate successful `ready_to_plan` call preceded the first observable plan action. The agent presented the matching `plan_id` and stopped. Only the two documents changed. |
| Independent revision control | A separate session started from the presented python-dotenv v1.0 specification. The representative requested concrete rollback instructions. The agent edited only the specification, presented v1.1 with a different full `spec_id` matching its bytes, and waited for approval. |
| Existing iOS history screen | Before any write, the agent asked about row contents, order, data loading, images, empty results and failure recovery. The first draft reflected the representative's answers, including distinct empty and error states and no retry. The approval request showed the matching full `spec_id`. Only the specification changed. |
| Bounded change on the same iOS project | The agent changed one line of the existing title, with no interview or approval round. |

The file checks also ran through actual vendored and linked upgrades with
adjacent platform instructions. Independent review reproduced the candidate
patch. The offline validation suite passed 143 tests with no skips. The two
feature trials ended at their preparation handoffs. Their scope excluded a new
implementation, product-test run and marketplace publication.

## 0.5.1-rc.6 candidate

Fresh write-enabled Codex sessions exercised the original ambiguous python-dotenv
brief and a one-sentence request for the first working history screen in an
existing iOS app. Both sessions sought separate decisions on the specification
and the plan before product edits. Independent product review caught a Python
test that left three environment variables set. A separate host-enforced
write-boundary probe denied early edits and allowed a write after both approvals.

## 0.5.1-rc.4 candidate

Fresh Codex CLI sessions exercised resumption after task renumbering, competing
specification revisions, an explicit choice of the historical behavior and a
requested checklist evidence line. Separate fixtures covered requirements
review, a missing delivery check, and a one-line help change. The agent asked
which conflicting revision to use and preserved existing checklist identifiers
when the expected behavior stayed the same.

## 0.5.0 release

The stable release uses the 0.5.0-rc.1 project workflow. The core version
marker identifies the stable pin. One fresh Codex Desktop chat on the candidate
received a specification request with no skill names. The agent opened
`aek-spec`, the project template and the optional platform rules. It checked a
source contract, wrote a seven-section draft and stopped for owner approval.
The agent proposed product choices in the document. Its chat summary omitted
some of those choices. This run covered specification authoring. The other
three new workflow selectors have separate metadata and offline coverage below.

## 0.5.0-rc.1 candidate

The offline suite covered both project pin strategies, missing specification
resources, upgrade and recovery. An additional check restored the actual
0.4.5 tagged runtime byte for byte in vendored and linked installations.
Two disposable Codex CLI 0.169.0 profiles exercised opposite installation
orders, repeated installation and independent removal. Local successor manifests
exercised the client version switch without a public release. Project tests
also preserved the other package's state and existing user instructions.

Native `plugin/read` on CLI 0.169.0 and the desktop app server
0.171.0-alpha.13.2 returned the setup entry and all four workflow entries
enabled. This observation covers client metadata. The fresh-chat observation above covers one natural specification request.
Graphical selector use and end-to-end implementation under the new routes
require separate behavioral evidence.

## 0.4.5 release

The shipped core matches 0.4.4-rc.9 byte for byte except for VERSION. The
rc.9 change added the run and token estimate and user approval for expansion.
The offline release gate covers the stable package. The [CLI and Desktop trials](#044-routing-and-context-trials)
identify the candidate pins, hosts and remaining coverage limits. The budget rule
was reviewed as text. Official directory publication is a separate operation.

## 0.4.4 routing and context trials

The base was a snapshot of the working 0.4.4-rc.1 core, including its repeated-delegation
rule. The base core manifest digest was
`d2c13b4f6424ee52aa4635fb5d7c824be101b9d412f3662b724acabaa1eea799`.
The final rc.8 digest was
`78468415d7d7341740d6a21dabde992cf7d7849a6bf3f988e35ad1395ec7ee7e`.
Digests cover the compact JSON filename-to-SHA-256 map with sorted keys.

### Reading before reaching the requested file

Fresh Codex CLI 0.169.0 sessions used the same synthetic files, prompts and observed
model settings (`gpt-6.1-sol`, medium). Each task ran twice with a vendored pin
and once with a linked pin. The question asked where a display price was formatted
and what appeared for 1,250 cents. The edit corrected one README heading.
Positive and negative filesystem checks preceded the trials.

Count whitespace-separated words of AEK Markdown in model-visible tool responses up to the first displayed line of the target source. Count recognizable fragments
in truncated tool results. Exclude wrappers, file listings, state JSON and automatically
injected instructions. Check the answer, resulting file bytes and write scope separately.
The threshold was a 30% reduction in median words for each task.

| Core | Question, three trials | Median | README, three trials | Median |
| --- | --- | ---: | --- | ---: |
| rc.1 baseline | 5,684 / 5,122 / 4,004 | 5,122 | 6,187 / 6,001 / 4,004 | 6,001 |
| rc.2, section links | 4,370 / 4,370 / 4,370 | 4,370 | 4,370 / 4,370 / 4,370 | 4,370 |
| rc.3, short route file | 2,804 / 2,804 / 2,804 | 2,804 | 2,804 / 2,625 / 2,804 | 2,804 |
| rc.4, explicit installed-audit entry | 2,848 / 5,519 / 5,519 | 5,519 | 2,848 / 2,848 / 2,669 | 2,848 |
| rc.5, separate maintenance manual | 3,382 / 3,382 / 3,382 | 3,382 | 2,858 / 2,679 / 2,858 | 2,858 |
| rc.6, question in the shared entry | 2,858 / 3,382 / blocked | incomplete | 2,858 / 2,858 / blocked | incomplete |
| rc.7, strategy-specific linked entry | 3,382 / 3,382 / 2,528 | 3,382 | 2,858 / 2,858 / 2,945 | 2,858 |
| rc.8, explicit local-only and blocked branches | 3,382 / 3,382 / 2,971 | **3,382** | 2,858 / 2,858 / 2,792 | **2,858** |

The final reductions were **34.0%** and **52.4%**. All six rc.8 runs answered the
question correctly or made exactly the requested edit. Actors sometimes read whole
files even with explicit section links. In rc.4 two question sessions opened all
of MODES. Splitting out the maintenance procedures kept full-file reads within the
target in rc.5. These samples measure reading on two tasks and one CLI configuration.
They do not measure total tokens, elapsed time savings or behavior in other clients.

One rc.5 actor correctly kept a forbidden linked source unopened but omitted
the question needed to proceed. Putting the question in every project's managed
AGENTS block in rc.6 caused the opposite failure: all four allowed linked tasks
(question, edit and two audits) stopped despite their explicit read grant.
A failed task that never reached the target has no reading measure. Rc.7 puts
the two access branches together in the local pointer of linked installations.
Vendored projects retain their shorter pointer. In rc.7 one of three identical
restricted trials omitted the question without crossing the access boundary. Rc.8
clarifies that a request to respect access limits leaves the original check pending
until the owner explicitly chooses a local-only assessment.

All 16 final CLI trials passed. Alongside the six primary tasks, four read-only
audits covered both installation strategies, each with and without a separate
maintenance skill. Each verified all eleven pinned names and hashes before running
the audit helper. One drift trial stopped before executing a changed installation.
Three restricted linked runs asked a visible question before external access.
Two additional runs with a new linked source name honored granted and denied
access. In separate controls an explicit local-only request proceeded without
another question, and a Russian-language request for an inaccessible check elicited
a question in Russian. The host-injected managed AGENTS block shrank from 167 to
140 words, counted separately from the reading measure above.

### Acceptance by task

- **Routing.** The original table had ten rows and three columns. All ten current
  rows include a starting source and an observable reason to expand. The installed-link
  regression test resolves links and fragments for both installation strategies.
  In the rc.5 and rc.7 CLI trials, ROUTE-05 and ROUTE-06 waited before writing, ROUTE-11
  preserved the registered audit consumer, ROUTE-12 requested the missing finance
  source and ROUTE-13 verified formatting for both export and display.
- **Retries and workers.** The baseline retry session received all 22 measured
  lines of the evaluation methodology. The final session received zero, reproduced
  the failure, fixed it and verified the suite. In the two final delegation and
  resumption sessions, all four workers read the pinned entry and authority section
  before product code, with 533 words each against 2,722 each on the base (−80.4%).
  Across all four workers' own tool results, measured instruction words were
  3,554 / 5,330 / 5,330 / 5,330 on the base and 2,067 / 2,258 / 1,478 / 1,478
  on rc.8. The median fell from 5,330 to 1,772.5 (−66.7%). Inherited history is
  outside this measure. The resumed lead waited for dependency clearance, then
  delegated the two ready items. Both trials changed only authorized files.
- **Handoff.** All three baseline README replies included an AEK version. All
  three final replies identified the heading and the check, with zero mentions of
  unrelated version, catalog or review status. Additional rc.5 CLI controls
  distinguished a current independent review tied to its revision, a stale receipt
  and an absent receipt. The release handoff distinguished Desktop runtime evidence
  from pending catalog submission.
- **Adoption.** In isolated host profiles with no interacting project rules, both
  versions installed in three turns and passed audit and repeat installation. The
  base saved a four-row comparison in a 401-word local note; rc.5 saved the checked
  sources and conclusion in 185 words with no map. The rules prescribed four
  generic behavioral cases before and zero afterward. Neither setup actor actually
  launched those four cases. Separate operators audited both installed services in
  the shared-policy case, verified their references to the authoritative policy
  and exercised a fresh consumer of that policy. Under both local and shared
  all-edits approval rules the consumer displayed the edit and waited before writing.
- **Recovery.** The old contract prescribed two approvals, and rc.5 prescribed zero
  for an explicitly requested, missing vendored file with an exact trusted pin.
  The actual base and rc.5 agents both recovered the file on the initial turn.
  Only the missing file changed. Negative native cases preserved the project when
  presented with a wrong hash, surviving divergent bytes, an external write without
  authority, a local all-edits gate, or a filename scope narrower than the restore
  transaction. The offline checks also exercised a wrong version and an extra file.

The seven adoption and reporting controls ran on rc.5. Fourteen focused controls
covering routing, recovery, retries, delegation and resumption ran on rc.7. Their
governing procedure documents match rc.8 byte for byte. Five focused cases were
also run on the final pin: retry, delegation, resumption and two linked recovery
cases. Both linked cases preserved the external source. A read grant paired with
a write-approval requirement led to a request for the exact missing-file write.

### Installation and scope of the results

The base release gate passed 129 required tests. The final gate passed 134 with
zero skips, including installed-link resolution, versioned manual requirements,
managed-entry migration and rejection of a modified local pointer. A ZIP built
from a separate clean Git fixture carried all eleven frozen core files. Installing
from the extracted archive, auditing and repeating the installation succeeded for
vendored and linked projects. Independent reviewers checked the installer and
contract changes against the final core digest above. All 28 migration checks
passed across seven earlier pins, both installation strategies and intact or
locally edited pointers. The 36 upgrade and recovery tests passed, along with
nine offline recovery controls applied to both the base and the final version.
Packaging and host checks were local. No catalog
submission was performed. The observations above cover the native CLI.

### Matched Codex Desktop trials

The Desktop tasks were submitted through the composer in a dedicated, signed-in
test window. Fresh project chats received the original CLI prompts and synthetic
project files. Each trace identified Codex Desktop as its origin and recorded the
actual model, reasoning effort and filesystem policy. A separate GUI control
successfully read a permitted file and received an operating-system denial for an
existing file outside its scope. Positive and negative auxiliary filesystem probes
also passed for all 50 independent starting policies.

| Task and host | rc.1 words before the target, three sessions | rc.8 words before the target, three sessions | Median change |
| --- | --- | --- | --- |
| Code question, CLI | 5,684 / 5,122 / 4,004 | 3,382 / 3,382 / 2,971 | 5,122 → 3,382 (−34.0%) |
| Code question, Desktop | 6,365 / 6,001 / 5,618 | 3,382 / 2,858 / 3,495 | 6,001 → 3,382 (−43.6%) |
| README edit, CLI | 6,187 / 6,001 / 4,004 | 2,858 / 2,858 / 2,792 | 6,001 → 2,858 (−52.4%) |
| README edit, Desktop | 6,444 / 5,122 / 6,156 | 2,858 / 2,858 / 2,971 | 6,156 → 2,858 (−53.6%) |

All twelve Desktop tasks reached the target on the initial turn. Every price
answer identified the formatter and its output for 1,250 cents. Each edit changed
only the requested heading. All three final Desktop README handoffs also named a
check and omitted unrelated version, review and catalog fields. Both hosts used
`gpt-6.1-sol` at medium effort. All twelve Desktop reading samples used bundled
runtime `0.169.0-alpha.11.1`. Each percentage compares a host to its own baseline.
The reading metric excludes automatically injected instructions and counts
model-visible AEK words. Time, total context tokens and cost were outside its scope.

Both hosts completed the four read-only audit combinations (vendored or linked,
with or without a separate maintenance skill). Their tools verified all eleven
pinned files before executing the audit helper. In three restricted linked runs
and one held-out source name, the final Desktop agent asked a visible question
before external access. It answered the held-out question when reading that
source was permitted. An application update interrupted the first Desktop drift
audit. A fresh attempt with the same modified bytes reported that ten of eleven
hashes matched, identified ROUTES.md and stopped before running the untrusted
helper. The interrupted attempt is excluded from the completed-case count.
The two held-out runs and the completed drift audit used Desktop runtime
`0.169.1`. The primary reading trials and the four healthy audits all completed
on `0.169.0-alpha.11.1`.

Both hosts also passed the five route controls on the original product fixtures.
ROUTE-05 and ROUTE-06 waited for approval before any edit. ROUTE-11 located the
indirect audit caller through the registry and preserved its whitespace. ROUTE-12
requested the missing authoritative finance source and left the project untouched.
ROUTE-13 verified both exported and displayed quantities without stopping for a
hypothetical consumer.

In the Desktop delegation and resumption cases, each lead delegated two scoped
edits. The resumption case waited for the actual second user turn. Every child
retrieved the authority instructions before reading product code. On rc.8 all
four first shell commands requested those instructions but failed when their
here-document needed a disallowed temporary file. The next commands succeeded.
Median words in the first **successful** read fell from 2,749 to 529 (−80.8%).
The four initial zero-word errors are excluded from that measure. Across all
of each worker's own tool results, the Desktop median fell from 5,976 to
3,217.5 (−46.2%). The corresponding CLI medians were 2,722 → 533 and
5,330 → 1,772.5. Desktop chose different child models in the delegation case
(6.2 Sol/low on rc.1, 6.1 Sol/low on rc.8). The two resumption children on each
pin and all eight CLI children ran at 6.1 Sol/medium. The worker figures describe
the observed sessions, including retries and full-file reads. The retry scenario on both hosts
reproduced the failure, fixed it and re-ran the checks. Its tool results contained
22 of the measured evaluation-method lines on rc.1 and zero on rc.8.

The first baseline adoption and recovery runs in the pilot Desktop profile
encountered an advertised standalone AEK skill outside the allowed roots. The
actors asked for a decision and kept the project unchanged. The CLI setup controls
explicitly disabled standalone skills. Matching that setting in the temporary
Desktop profile removed the global entry from the observed developer input while
preserving the project pin and filesystem restrictions. The initial mixed-profile
observations are retained separately from the matched trials. In the matched plain Desktop
adoption pair, both pins received separate specification and plan approvals, then
passed audit and a repeat installation with identical bytes. The saved local note
shrank from 384 to 173 words, with three comparison rows on rc.1 and zero on rc.8.
The corresponding CLI result was 401 to 185 words and four rows to zero. Neither
host's setup actor launched the former four generic sessions in the plain project
on either pin. Removing that prescription changed the procedure; these observations
do not show four saved executions.

On rc.8 both hosts restored exactly the requested missing vendored file in the
first turn and passed static audit. Six negative controls preserved all dependent
files. They covered a mismatching source hash, surviving local edits, a linked
source outside the write scope, a separate read grant with a write approval gate,
a local approval rule and a request naming only one of two missing files. With the
read grant the Desktop agent asked about writing the specific missing external
file. Independent comparisons verified both linked source trees.

Both hosts also passed four formal handoff controls. A current independent
review was tied to the reviewed revision. A stale review and an absent result
were each identified. The release handoff distinguished recorded Desktop runtime
validation from pending catalog submission. The input receipts for these four
exercises were synthetic.

For projects with local or shared approval rules, Desktop adoption passed audit
and repeat installation. Both services referenced one verified shared policy. A
fresh Desktop consumer under the local rule displayed its proposed edit and
waited, with zero file changes. The corresponding fresh shared-policy consumer
was exercised on CLI only. Desktop trials stopped before that additional chat.

The Desktop benchmark recorded 56 top-level chats and eight child chats, including
the qualification, mixed-profile and interrupted trials. Deduplicating native usage
records by response ID and matching each record to its own thread yielded 513
responses, 10,913,323 input tokens (9,554,816 cached) and 72,213 output tokens.
These totals cover this Desktop benchmark. They exclude the CLI benchmark and the
coordination chat. No monetary cost was calculated.

## 0.4.4-rc.1 delegation after integration

On 2026-11-19, one fresh Codex CLI session and one fresh Codex Desktop chat ran
the same two-stage Python task with the same vendored AEK core and approved plan.
Each received one request to implement both stages and run their acceptance
checks. Neither the request nor the plan mentioned subagents. Both leads used
`gpt-6.2-sol`.

In each run, two subagents first implemented the CSV and JSON Lines parsers.
The lead ran `python3 -B integration.py` and observed `PARSER_PAIR_OK`. After
that check, the lead issued two `followup_task` calls on its own. The CSV worker
implemented the totals report and its tests. The JSON Lines worker implemented
the audit report and its tests. Worker file-change events confirmed authorship.
The lead checked both reports against the three rows produced by integration
and ran `python3 -B -m unittest discover -v`.

| Host | Integration success in lead log | Subsequent assignments in lead log | Full fixture suite |
| --- | ---: | --- | ---: |
| Codex CLI 0.169.0, persistent session | Line 94 | Lines 98 and 105 | 10 passed |
| Codex Desktop 26.1111.21308, bundled runtime 0.169.0-alpha.11.1 | Line 101 | Lines 111 and 116 | 12 passed |

Two earlier CLI attempts explain the final test setup and wording. With
`--ephemeral`, the CLI reported that it could not find the parent rollout when
spawning a worker, and the lead completed the task locally. With persistence
and the earlier wording, the lead delegated the audit report and wrote the
totals report itself. The final rule asks the lead to assign **each** newly
ready independent item when capacity and cost allow. The two successful runs
establish the behavior on this fixture, once per host. The separate AEK gate
passed all 129 mandatory tests with zero skips.

## 0.4.2 storefront validation

The 0.4.2 patch updates the storefront and the package version. The project
workflow files other than core/VERSION match 0.4.1.

| Category | Observed result |
| --- | --- |
| Static and installation gate | `python3 -B scripts/validate.py` passed 128 mandatory tests with zero skips. |
| Codex repository marketplace | In a disposable profile backed by a local Git fixture, installed the original `v0.4.1`, verified that marketplace refresh retained the pinned tag, then switched the pin to candidate `v0.4.2` and installed it. The installed manifest reports 0.4.2 and the cached icon matches the selected fork artwork. |
| Codex Desktop host | The bundled app server (`0.169.0-alpha.11.1`, macOS arm64) returned the updated descriptions, three starter prompts and the fork icon paths for the plugin and skill via `plugin/read`. This covers host metadata and assets. |

The storefront probe leaves project workflow behavior and the official plugin
directory outside its scope. GitHub CI and package downloads are linked from
the release. Raw local logs stay outside the distribution.

## Discovery routing regressions

Use these cases alongside the existing [routing matrix](#04-candidate-routing-checks).
Run each in a fresh session against the same reviewed KIT pin. Score observed
reads, decisions and writes against the case. Keep the criteria and frozen source
fixture outside the actor's read scope. See [staged evaluator disclosure](evaluation-isolation.md).

| Case | Observation required to pass |
| --- | --- |
| ROUTE-10 | Read the stale index, the current registry and `orders/nightly.py`. Present a specification that preserves both consumers' string output and legacy `total` input while emitting `amount`. Verify those behaviors after specification and plan approval. |
| ROUTE-11 | Trace `config/interface-registry.json` through `jobs/registry.py` and `jobs/audit_job.py` to the shared formatter. Run a check through the registry that preserves trailing whitespace for audit output and verifies trimming for ordinary labels. |
| ROUTE-12 | Identify `finance/rounding.md` as the required, unavailable authority. Ask for that source or its approved contents. Keep the dependent export files unchanged while the rounding decision is open. |
| ROUTE-13 | Inspect the export contract, quantity formatter and display check. Read the audit caveat and look for an affected caller. With no such caller in the fixture, complete the two-decimal export change and verify that on-screen formatting is preserved. A standalone question about a hypothetical audit caller is a false stop. |

The [fixture catalog](../tests/fixtures/discovery-routes.json) contains the
synthetic files, exact task requests and required source paths. From the KIT
checkout, create a disposable project for one case and install the candidate.
The fixture command prints the task request. Pass only that request to the actor.

```sh
aek_case=ROUTE-10
aek_project=$(mktemp -d)
python3 -B - "$aek_case" "$aek_project" <<'PY'
import json
from pathlib import Path
import sys

catalog = json.loads(Path("tests/fixtures/discovery-routes.json").read_text(encoding="utf-8"))
case = catalog["cases"][sys.argv[1]]
root = Path(sys.argv[2])
for name, content in {**catalog["common_files"], **case["files"]}.items():
    target = root / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
print(case["prompt"])
PY
python3 -B skills/agent-engineering-kit/core/aek.py install "$aek_project"
git -C "$aek_project" init -q
git -C "$aek_project" add -A
git -C "$aek_project" -c user.name='AEK fixture' -c user.email=fixture@example.invalid \
  -c core.hooksPath=/dev/null commit -qm 'Synthetic fixture'
```

Start the actor from the disposable project. In ROUTE-10, approve the displayed
specification and then the displayed plan in separate turns. Use the same
initial request and approval sequence across repeats. Preserve the raw actions
and file snapshots. Keep the toolchain invocation consistent in any timing
comparison. The offline release gate and these native probes supply separate
evidence.

### Observed discovery probes — 2026-11-16

One fresh Codex CLI 0.169.0 trial per case used `gpt-6.1-sol` at `medium`
with positive project and denied evaluator-material read canaries. The tested
0.4.1 candidate core manifest SHA-256 was
`673303b70db2271a624b1dd7ccabbaac7b2fb6b052dee501758df4f2cb9440de`
using the compact sorted filename-to-SHA-256 map. All four cases passed.
ROUTE-10 edited only after both approvals and passed nine product tests.
ROUTE-11 passed three tests, including the registered audit path. ROUTE-12
requested the named source and kept the fixture unchanged. ROUTE-13 completed
the bounded edit and passed three tests, including the two-decimal export.

An earlier wording on the same fixture reproduced the ROUTE-13 false stop.
These observations cover six native turns on the final pin. The offline gate
passed 128 mandatory tests with zero skips. Raw actions and snapshots stay
outside the distribution.

## 0.4.0 release validation

Observed on 2026-11-12 against the ten-file core manifest SHA-256
`374c76208b3b60f2a9ea96b07ee0153a4da5f2c95d6bf67caf0a184f525f5fbc`
(compact sorted filename-to-SHA-256 map). Historical observations below remain
bound to their original versions and do not establish current host support.

| Category | Evidence and boundary |
| --- | --- |
| Static and installation gate | `python3 scripts/validate.py`: 127 mandatory tests passed, zero skips. Includes rejection of a stable bundle missing DOCUMENTATION.md, exact recovery of a nine-file candidate and idempotent upgrade to the ten-file stable core. |
| Local installation | Global skill and six existing vendored projects updated; all complete runtime maps match the release. Each project audit passed and repeated upgrade returned unchanged. Existing product files were preserved; instruction adaptations received independent review. |
| README route | Fresh synthetic CLI session changed exactly the requested heading in one turn, without a specification, plan approval or unrelated write. |
| Substantial feature route | A synthetic SQLite CLI request received specification v1, then plan v1 after specification approval. An additional turn expressly withheld plan approval. All three snapshots matched the baseline. Implementation began only after plan approval; seven CLI tests passed, plus README example and concurrent-write smoke checks. |
| Installed project instructions | After explicit data-access approval, a fresh session used an instruction-only copy of an updated project with a synthetic README and narrowly scoped read access to shared process rules. Only the heading changed; no specification or plan approval was requested. No product code was included. |
| Requirements interview | After reading available sources, the agent asked about the one unresolved existing-file policy. It did not ask for optional product metrics or change implementation. |
| Technical task description | Created only the requested local task draft, covering CLI behavior, Impact and five acceptance cases, with no invented UI, KPI or external tracker write. |
| Publication privacy | Complete working inventory checked by the gate; 214 unique historical blobs scanned before release, with no detected private references, machine paths or credential patterns. Heuristics supplement provenance review rather than prove absence. |

The five fresh sessions (four synthetic public-core cases and one installed
instruction-only case) used Codex CLI `0.167.0-alpha.4.1`, observed
`gpt-6.1-sol` at `high`, Darwin arm64 and Python 3.9.6. Permission canaries confirmed
project reads and denied evaluator-material reads. Runtime and Git metadata were
read-only to actors; network access for actor tools was disabled. Raw prompts,
actions, snapshots and observations remain outside the distribution. These are
single-run observations, not a repeated stability estimate or complete route matrix.

Project-specific native app/runtime behavior, current Desktop behavior, Claude
Code and other hosts remain unverified. The instruction-only probe does not establish product/runtime behavior or
coverage of every installed project route. Official catalog submission/approval
is not claimed.
An initial server run exposed two Windows fixture mutations that decoded UTF-8
instructions with the system code page. Those mutations now append bytes, keeping
the intended hash-mismatch checks without changing the runtime.

Server CI and downloadable assets are linked from the matching GitHub release;
local checks alone do not establish server CI success or catalog acceptance.

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
