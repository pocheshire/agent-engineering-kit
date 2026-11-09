# Validation report — 0.1.0-rc.1

Observed on 2026-11-09. This is a release candidate, not stable acceptance.
No private source project or private research evidence is distributed.

## Automated verification

`python3 scripts/validate.py` passed 33 checked-in mandatory test IDs, with zero
skips, expected failures or failures. The gate rejects discovery/started/successful
ID mismatches, duplicate/replaced/missing cases, empty suites and skipped subtests.
Separate negative subprocess controls exercise empty, skipped, expected-failure
and incomplete suites. Evidence JSON verification checks an independent mandatory
manifest and explicitly does not authenticate the underlying execution.

Installation coverage includes empty Initialize, existing AGENTS byte preservation,
unmanaged conflicts, safe repeats, linked relocation/pinning/missing source,
vendored three-way local changes/conflicts/additions/deletions, linked adaptation
loss prevention, symlink boundaries, read-only audit, uninstall preservation,
global skill installation/update/removal and malformed receipt recovery.

The static gate checks required files, versions, standalone MIT notices, relative
links, skill/marketplace identity and privacy heuristics. Native manifests also
need actual host validation. A bundled external skill-authoring helper could not
run because its Python environment lacks PyYAML; this is not counted as a pass.
AEK itself has no third-party runtime dependency.

## Independent behavioral probes

The executor received natural requests and raw synthetic project artifacts, not
the hidden rubric. Rubric/request/baseline hashes were fixed before execution.
A fresh reviewer graded actions and independently inspected files/results before
each corresponding final self-assessment. An earlier reviewer package exposed
embedded self-assessment, so that initial reviewer was not used for the clean
first verdict. The fresh review deferred the affected commands and evaluated raw
state first, then reconciled those commands and final claims.

| Probe | Observed result |
| --- | --- |
| Portable Adopt | Passed: canonical entry loaded, versioned self-contained runtime, original instructions/product bytes preserved |
| Setup → ordinary bugfix | Passed: bounded red/green regression, direct and indirect seconds consumer preserved, exact write scope respected |
| No-intent portable entry | Passed: one short target/intent question, no writes |
| Audit with conflicting publication rule | Passed: static integrity separated from policy failure and missing project evidence, no repairs |
| Global skill natural Initialize | Passed: unhinted natural request discovered installed skill/core, grounded product questions, no writes |
| Small-change technical escalation | Passed route/scope/compatibility: transitions before writes, preserves approved execution, finds dynamic cache consumer; reporting caveat below |

The bug session executed five named test methods with no failures/skips; the
reviewer independently reran them and sampled player/exporter behavior. The
indirect exporter was discovered during Adopt and handed to subsequent development.
Do not infer that the second session alone rediscovered an unknown consumer.
Repeat installation byte identity and relocation within the same host were checked;
a different machine/OS behavior is a separate claim.

A separate fresh ordinary-development probe started with a small-change request
and discovered a shared persistent-key contract through dynamic routing. It moved
to authorized feature execution before writing, kept legacy/new round trips and
changed only the permitted source/tests. Seven test methods passed and were
independently rerun. Its actor reported an unavailable review with an unsupported
“tool failure” explanation: no attempted review call appears in the trace. No
independent review was falsely claimed, and the external fresh reviewer supplied
that review, but the explanation remains unverified. This reporting limitation is
one reason the release is a candidate. The first probe's rubric/request/baseline
were hash-pinned; the separate route probe hash-pinned its rubric, while request
and baseline ordering is established by the driver trace.

## Host and distribution validation

Codex CLI 0.167.0-alpha.3.2 installed the native repository plugin in an isolated
profile from a clean local package. Inventory reported the expected version,
enabled state and cached canonical entry. Plugin and marketplace removal succeeded.
An initial harness put its cache inside the source and recursively copied it;
that failed attempt is excluded from the passing clean-package smoke.

The complete global skill was installed at the current official user discovery
location. Claude Code is unavailable here: its official adapter is prepared but
not runtime validated. Cursor is a documented compatibility candidate only.
No official OpenAI/Anthropic/Cursor directory submission or review has occurred.

## Limits and release boundary

These are bounded synthetic tests and one available host, not a guarantee that
any model follows the workflow. Static integrity is not semantic project readiness.
Installer/host execution is not external product acceptance. Product/runtime checks
must be adapted to each project. Concurrent hostile filesystem mutation is outside
the installer transaction model. Local runtime adaptations remain preserved but
make baseline audit fail until reconciled. Linked upgrades require the previous
source to be available for comparison.

The initial server run stopped at environment setup: Python 3.9 has no setup-python
artifact for Ubuntu 26.04. The gate itself passed on the Python 3.13 Linux job;
other cancelled jobs were not counted. The corrected matrix uses compatible
explicit runners for Python 3.9 and current runners for Python 3.13, with
fail-fast disabled so each platform reports its result. Runner selection was
checked against the [official versions manifest](https://github.com/actions/python-versions/blob/main/versions-manifest.json).

Server checks are visible in [GitHub Actions](https://github.com/pocheshire/agent-engineering-kit/actions/workflows/ci.yml).
Release notes record the observed server run and remote marketplace smoke result.
Stable status is withheld pending broader host/platform validation and release
experience. See [platforms](platforms.md) for exact channels.
