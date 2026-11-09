# Changelog

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
