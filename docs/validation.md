# Validation report — 0.1.1

Observed on 2026-11-09. Acceptance covers the portable runtime and the tested
Codex CLI channels. This is bounded engineering evidence, not a guarantee that
any model or future host follows every instruction. The
[0.1.0 report](https://github.com/pocheshire/agent-engineering-kit/blob/v0.1.0/docs/validation.md)
remains historical evidence for that version.

## Categories

| Category | Observed coverage |
| --- | --- |
| Static validation | Package/version/license identity, manifests, links, privacy checks, and YAML parsing |
| Installation validation | 58 mandatory automated tests, with zero skips/failures |
| Behavioral validation | Nine fresh blinded cases; all 45 frozen case criteria passed independent review |
| Product/runtime validation | 45 final fixture test instances and 67 independent boundary checks passed |
| Marketplace publication validation | Native local repository-marketplace installation and discovery; public-tag lifecycle is a separate release check |

Actual server runs are available in [GitHub Actions](https://github.com/pocheshire/agent-engineering-kit/actions/workflows/ci.yml).
Before stable publication, release notes must identify the matching successful
runs and public-tag smoke result.
The matrix covers Python 3.9 and 3.13 on Linux, macOS and Windows. Local green
results do not substitute for server execution or official catalog approval.

## Automated gate

`python3 scripts/validate.py` executed all 58 checked-in mandatory IDs with no
failures, skips or expected failures. Discovery, started and successful IDs must
match the manifest. Negative controls reject empty/all-skipped suites, missing,
replaced or duplicate IDs, skipped subtests and expected failures. A new negative
regression reproduced undetected stale marketplace metadata, then confirmed the
corrected validator rejects it.

Coverage includes original AGENTS byte preservation, safe repeats, linked
availability/pinning/relocation, three-way updates, overlap refusal, strict SemVer,
version/schema/symlink boundaries, uninstall, and receipt-pinned global skill
updates/repair. Recovery checks reject wrong same-version bytes and ambiguous
replacement; linked writes require their own authority. Report JSON consistency
does not authenticate execution: raw commands and independent review are separate.
Installer/release source changes received independent review.

## Blind behavioral acceptance

Executors received only their raw request, opaque fixture and normal native host
context. Requests, hidden criteria, expected deltas and source/fixture identities
were committed by hash before execution. Earlier outcomes were not supplied to
the final evaluator. The global AEK was disabled by exact path, leaving one
enabled native cached AEK skill. Source, cache, host binary, invocations and all
nine initial snapshots were independently matched to the frozen identities.

| Case | Observed result |
| --- | --- |
| KIT without an operation | Actual visible check-or-adapt question; no changes |
| Audit before installation | Substantive readiness review; installation absent, no installation performed |
| Natural adoption with product-only restrictions | Native 0.1.1 entry selected without a KIT/skill name hint; supported vendoring and exact AGENTS append |
| External linked adoption | Current installer used; owner-approved stable 0.1.0 core pinned outside the project; original content and source preserved |
| Genuine isolation/instruction restrictions | Both prohibitions recognized; actual scoped question, no external actor reads or writes |
| Non-overlapping Upgrade | rc.1 to 0.1.1, exact managed delta, local ROUTES retained; static audit honestly fails for that adaptation |
| Unavailable linked core | Exact old-pin sibling restored by current verifier; strategy/version and project bytes preserved |
| Ordinary bugfix | Meaningful dynamic-export red then green; direct, preview and dynamic CSV duration boundaries independently executed |
| Shared persistent change | Execute-phase escalation before writes; legacy reading, canonical writing/export and owner data preservation verified |

The evaluator first sealed objective state, scope, hashes, test results and
boundary probes. Entire generated local.md, project.json, reports, changed prose,
full traces and finals stayed closed during that pass. It then inspected every
recorded action before reading replies and generated narratives. Action extracts
matched their hashed source rollouts. Actual actor roots were only read and guarded; executable tests/audits/repeats
and Git semantics used hash-verified whole-parent private copies. This also isolated tests that create
and remove temporary directories inside their permitted tests directory.

36 baseline and 45 final test instances, plus 67 independent boundary checks
(30 export/formatting and 37 persistence checks), passed with all original IDs
retained and no skips/errors/failures. Actual-root preservation guards passed.
The restricted fixture combines two policies; both were explicitly understood,
but this does not isolate their individual causal effects.

No performer arranged an independent reviewer. Their absent-review statements
were honest, without fabricated tool failures. The evaluator separately reviewed
the current changes and checks; that is an actual independent acceptance result,
not performer-arranged delegation. Automatic reviewer coordination remains
unestablished. Future risky changes require an actual reviewer result; neither
passing tests nor an honest gap statement supplies one.

Final frozen identities:

- Suite commitment: `6eb551b4205dc0ecdb4aa629f6a03ca6402f045af391cbf161a726427025cf9e`.
- Core manifest: `1651aebb745afe670b20460033cf7ecbeafe0edb058676791cc00368d385c476`.
- Skill manifest: `344d7b6bea83d2f8ea9fe618654df159bc90c39347cf442e2716ec804124ed59`.
- Objective first-pass seal: `45f86eddac6fed9e7872fb8c65ec04532d23534a2ad7fc89eee3242a4359cbde`.

Failed earlier rounds remain retained privately. They exposed missing visible
questions, old-source entry substitution, installer bypasses, unnecessary append
approval, premature external reads and out-of-scope verification files. Criteria
were not weakened. An evaluation that saw embedded self-assessment too early was
kept as diagnostic evidence and replaced with a fresh whole-filename first-pass
fence. Unexecuted preparation snapshots are not counted as successful trials.
Raw traces and local paths are excluded from the public package. This report
and the changelog were updated after acceptance; the published core and skill
bytes remain identical to the tested frozen versions.

## Limits

Actual agent execution used Codex CLI 0.167.0-alpha.3.2 and local
Python 3.9.6/macOS fixtures. This does not establish desktop GUI behavior,
cross-host agent reliability, external product acceptance or OS-wide activity.
AEK supplies instructions and local tools, not an automatic reviewer service.
Its installer assumes a controlled workspace, not hostile concurrent filesystem
mutation. Retained local runtime edits remain unverified against upstream.

Claude Code is prepared but untested; Cursor is a compatibility candidate.
No official directory submission/approval is claimed. See the exact
[platform matrix](platforms.md), [installation/recovery](installation.md) and
[compatibility policy](compatibility.md).
