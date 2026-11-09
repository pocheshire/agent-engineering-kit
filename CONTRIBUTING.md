# Contributing

Open an issue describing the concrete failure and expected behavior. Keep private
project content and credentials out of reports. Contributions use the MIT license.

Use Python 3.9+ and run `python3 scripts/validate.py`. Add meaningful regression
cases for installer or verification changes. No third-party runtime dependencies
are needed. Keep the shared rules under skills/agent-engineering-kit/core;
adapters must not fork the engineering contract. See docs/adapters.md.

Installer, authority, upgrade and release changes require an independent reviewer.
For behavioral tests, keep hidden criteria away from the executor and review raw
actions before self-assessment. State host/version and limitations. Update the
changelog for user-visible changes. Do not claim host or marketplace support on
manifest validation alone. Follow docs/compatibility.md for version changes.
