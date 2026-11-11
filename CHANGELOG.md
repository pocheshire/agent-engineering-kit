# Changelog

## 0.3.0-rc.2 — 2026-11-11 (candidate)

- Map AEK rules to existing project approvals, authorities, and shared routes
  during Adopt and Upgrade. Verify the reconciled workflow in a fresh session.

## 0.3.0-rc.1 — 2026-11-11 (candidate)

- Introduce Spec-Driven Development for project changes. Ask material questions
  before and after read-only discovery, then obtain separate approval of the
  specification and the execution plan before edits or delegation.
- Show a compact plan with dependencies, owners, available model and effort
  choices, and verification. Keep both approvals for small changes and allow a
  single executor where the task and review requirements permit it.
- Keep approval bound to the presented revision. Reopen the affected stage when
  requirements or the execution plan materially change.
- Load the development workflow through the managed AGENTS.md block before
  implementation reads. Upgrade migrates the exact legacy block with the runtime
  pin and preserves owner text and file permissions.
- Have delegated workers read the AEK entry and full pinned contract in their
  first tool call. Verify the read order, approved model profiles and lead
  acceptance in two local Codex Desktop project chats.

## 0.2.1-rc.1 — 2026-11-10 (candidate; validation pending)

This candidate starts remediation of findings F1–F8 from the 0.2.0 audit. It is
not a stable release or a replacement for the historical 0.2.0 acceptance record.

- F1: prevent stale cached runtime bytecode from executing after exact restore.
- F2: reject aliased and overlapping filesystem scopes in generated permissions.
- F3: validate newly referenced runtime resources before Upgrade writes.
- F4: preserve existing instruction-file bytes and permissions through install and
  uninstall.
- F5: bind evaluation receipts to the exact prepared view and reject mutations.
- F6: use one tracked publication inventory for the release gate and ZIP, reject
  reserved tracked paths, and retain Git-free validation.
- F7: clarify the different adaptation outcomes for vendored and linked upgrades.
- F8: require the final handoff to state independent-review status accurately.

Candidate implementation and acceptance evidence remain in progress; the 0.2.0
validation report and its historical result are unchanged.

## 0.2.0 — 2026-11-09

- Add bounded Review → Repair → Validate, durable checkpoints, cost-aware roles,
  optional native Goals and pilot-first modernization to the canonical core.
- Add offline task/attempt/delegation/modernization validation and live repeat
  aggregation, including current-revision checks, cumulative budgets, unresolved
  findings and required independent review receipts.
- Add staged actor/evaluator views, explicit Codex permission-profile generation
  and privacy-preserving capture of observed rollout configuration and usage.
- Preserve exact recovery of original seven-file 0.1 pins; Upgrade adds the new
  self-contained runtime without overwriting non-overlapping adaptations.
- Keep static, installation, behavioral, native client, runtime and catalog
  evidence separate. See the versioned validation report for actual coverage.

## 0.1.1 — 2026-11-09

- Show an actual short check-or-adapt question when a known project's setup intent
  is missing; retain explicit intent without another interview.
- Continue read-only readiness review when AEK is not installed, separating it
  from installed integrity and product test evidence.
- Scope clean-room conflicts to concrete actions and authority. Explain external
  relative linked sources without bypassing filesystem or imported-content bans.
- Diagnose old-version reports by the loaded source; distinguish global skills,
  native plugins, portable checkouts and project pins.
- Preserve existing AGENTS bytes with the supported append; prohibit installer
  bypasses and substitute entrypoints. Keep verification scratch within task
  authority and show a concrete next-step question when adoption is blocked.
- Check target read limits before loading external KIT files. Recognize the
  installed AEK entry even when the user supplies an older pinned source.

## 0.1.0 — 2026-11-09

First stable release for the validated portable and Codex CLI channels.

- Enforce strict SemVer ordering, pinned version identity, no same-version content
  replacement, and adaptation-schema preflight before Upgrade.
- Restore unavailable/corrupt runtime from exact trusted pins without repinning;
  require explicit replacement for confirmed damage and explicit linked-source
  write scope.
- Validate complete global skill identity and license notices; add receipt-pinned
  repair and preserve backups if an I/O rollback cannot complete.
- Clarify recovery intent and evidence reporting. See the current
  [validation report](docs/validation.md) for execution and review boundaries.

## 0.1.0-rc.1 — 2026-11-09

Initial public release candidate: portable entry, four setup modes, shared
engineering contract, vendored/linked installation, conflict-aware upgrades,
Codex global skill and plugin adapters. This prerelease's original
[validation boundary](https://github.com/pocheshire/agent-engineering-kit/blob/v0.1.0-rc.1/docs/validation.md)
remains available with its tag; it did not claim stable acceptance.
