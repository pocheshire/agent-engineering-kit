# Validation report — 0.1.0

Observed on 2026-11-09. Stable acceptance covers the portable runtime and the tested
Codex CLI entry points. It is a bounded engineering acceptance, not a guarantee
that every agent or host follows instructions. The original
[0.1.0-rc.1 report](https://github.com/pocheshire/agent-engineering-kit/blob/v0.1.0-rc.1/docs/validation.md)
remains historical evidence for that prerelease.

## Categories

| Category | Observed coverage |
| --- | --- |
| Static validation | Shared package/version/metadata identity, standalone license notices, links and privacy heuristics |
| Installation validation | 57 checked-in mandatory tests; deterministic install, update, repair and refusal boundaries |
| Behavioral validation | Eight fresh, blinded cases passed final independent action-and-artifact review |
| Product/runtime validation | Real local helper/host execution and synthetic product fixtures; 41 independently executed tests plus 70 boundary/signature checks |
| Marketplace publication validation | Native repository-marketplace lifecycle; official directory submission is a separate unperformed action |

Server results are visible in [GitHub Actions](https://github.com/pocheshire/agent-engineering-kit/actions/workflows/ci.yml).
Release notes record the exact successful server run and remote-tag smoke results.
The matrix covers Python 3.9 and 3.13 on Linux, macOS and Windows; minimum-version
jobs use compatible explicit runners. No cancelled/skipped job is counted as pass.

## Automated checks

`python3 scripts/validate.py` executed all 57 mandatory test IDs with zero failures,
skips or expected failures. Discovery, started and successful IDs must match the
checked-in manifest. Empty suites, missing/replaced/duplicate IDs, skipped subtests
and expected failures are rejected. Separate negative subprocess controls exercise
the gate itself. Report JSON validation does not authenticate the underlying run;
raw execution and independent review remain necessary.

Coverage includes original AGENTS byte preservation, safe repeats, linked pinning,
relocation and missing sources; vendored three-way additions/deletions/local edits;
overlap refusal without writes; source/version/schema mismatches; strict SemVer
precedence; explicit major-migration admission; symlink boundaries; read-only audit;
uninstall preservation; global installation/update/repair and receipt integrity.
Recovery tests include missing or corrupt aek.py/ENTRY/VERSION/CONTRACT, wrong
same-version bytes, replacement ambiguity, and linked external-write scope. The
verifier runs from a complete trusted source rather than executing damaged code.
Counterfactual tests against the immutable prerelease reproduced the defects that
were fixed. Independent source review separately examined the implementation.

## Blind behavioral acceptance

Each executor received only its raw user request and fixture, without the hidden
rubric, expected deltas, prior outcomes or implementation solution. Requests,
rubrics, source identity and fixture baselines were hash-committed before execution.
Copies ran outside the KIT checkout, preserving sibling layouts and pending edits.

| Case | Final observed result |
| --- | --- |
| Natural native plugin Adopt | Loaded the cached native skill/core without a skill-name/path hint; complete vendoring, project commands and original rules/data preserved |
| Non-overlapping Upgrade | Advanced from the prerelease to 0.1.0, preserved local ROUTES and owner adaptations, changed exactly the intended six managed paths; audit honestly retained the local-baseline failure |
| Conflicting Upgrade | Identified the overlapping contract edit and stopped with zero project changes |
| Unavailable linked core | Used the complete current verifier and exact trusted old-pin data; restored the original seven files, preserved linked strategy/version and project bytes |
| Corrupt vendored core | Restored only the authorized damaged aek.py and missing CONTRACT, with unchanged pin and other project bytes |
| Missing plugin core | Reported incomplete own installation, scoped its lookup, requested the trusted exact source and made zero project changes |
| Ordinary bugfix | Demonstrated meaningful red then green, checked the dynamically routed export consumer and changed only the permitted formatter/tests |
| Shared persistent change | Transitioned from small-change to already-authorized feature execution before writing, preserved legacy compatibility/data, and established actual matching-revision independent review |

The final evaluator was context-free and did not receive prior failed outcomes or
fixes. It first verified identities, whole measured state, scope, pins, tests and
command ledgers. All performer local/review/report prose and raw dialogue stayed
closed until its first-pass verdict was written. It then reconciled complete
public traces, filtered persisted tool-call/error records and final claims.
No reasoning/message payloads were extracted into the supplemental tool evidence.
The actual reviewer spawn, reviewed hashes, diff and test actions were established
for the persistent-contract case. Process exit zero alone was not acceptance.

Final frozen commitments:

- Six maintenance cases: `5f0ab31cb604480e338bfa6b1ae59599658ed047b94be651ad6d0d027a92e0ee`.
- Two development cases: `1453724c7f6fcd986564c99e9c1fcea691a10000efe7d1ffb32f2232134336be`.
- Core manifest: `209e49c34627971a301b10c2a26c011e596b32724e8bc1ab9ecac0b14a2f5697`.

Earlier failed/ineligible rounds remain retained locally. They exposed invalid
host override quoting, old-verifier/manual recovery, overly broad source search,
an extra update report and an unsupported reviewer-failure claim. The package or
harness was corrected and fresh trials repeated; criteria/requests were not
weakened after observing outcomes. An evaluator-ordering problem was replaced
with a fresh restricted first pass, rather than counted as independent acceptance.
Private traces contain local host details and are not part of the public package.

## Host and scope limits

Codex CLI `0.167.0-alpha.3.2` was actually executed. Before every final corpus the
host inventory showed exactly one enabled cached native AEK and the ordinary
global AEK disabled by exact path. The binary/version, complete argv, fresh thread
IDs, package/core hashes and immutable context were recorded. Test profiles reused
existing CLI authentication by reference; no credential bytes were copied into
the package or logs. Normal user configuration was not changed for the trials.
This establishes discovery isolation, not an operating-system security boundary.

Two ordinary fixture `.git/index` byte hashes differed at evaluator readback;
the cause was not established. HEAD, all staged path/mode/object entries, empty
cached diffs and all non-.git measured bytes were independently verified. Three
performer verification scratch files outside the measured roots lack committed
prior-state coverage. Those limits prevent any whole-machine preservation claim;
they do not hide or relabel a product-scope failure.

The installer assumes a controlled workspace; hostile concurrent filesystem
mutation is outside its transaction model. A retained local runtime adaptation
remains unverified against upstream until reconciled. AEK does not prove external
product acceptance, GUI/device behavior, cross-host agent reliability or future
Codex compatibility. Claude Code is prepared but untested here; Cursor remains a
compatibility candidate. No official directory approval or listing is claimed.
See the exact [platform matrix](platforms.md) and [recovery policy](installation.md).
