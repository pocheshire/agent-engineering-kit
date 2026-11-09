# Development routes

Use one applicable route plus the real platform's existing checks. Do not create
new skills merely to mirror this table. The pre-write applicability rule and
engineering authority are defined in CONTRACT.md.

| Route | Applies when | Work and exit evidence |
| --- | --- | --- |
| Small change | Behavior and scope are known; impact is bounded | Brief intended behavior and boundary, minimal edit, relevant checks and author review |
| Feature, prepare phase | A new capability has material unresolved requirements | Inspect context, clarify only necessary product choices, propose design/acceptance criteria and verification |
| Feature, execute phase | Requirements and implementation are authorized | Preserve accepted decisions, implement by risk, verify affected consumers and review |
| Bugfix with red test | Correct behavior is known but current behavior diverges | Reproduce the relevant failure, establish meaningful red evidence, correct cause, show green and regression checks |
| Systematic diagnosis | Cause or affected boundary is uncertain | Discriminating hypothesis, trace first divergence, experiment, revise at contradiction, then route to fix |
| Review feedback | A finding or proposed patch needs evaluation | Verify raw evidence against actual contract/callers; implement authorized defects and check regressions |

A small change is no longer applicable when it alters a shared contract,
permission, persistent format, cross-component invariant, or uncovers broader
material consumers. Move to feature execution if implementation is already
approved and requirements remain settled; otherwise diagnose or prepare the
missing decision. Do not reset authorized work to an interview.

For a bug, a test that never reaches the failing path is not a reproducer. If a
reproducer cannot be run, state why and use the strongest available observation;
never report red/green that did not happen. Platform constraints may require
manual/device checks alongside automated tests. Avoid arbitrary coverage targets.
