# Development routes

Use one applicable route plus the real platform's existing checks. For changes,
follow the interviews, analysis, and two approvals in [CONTRACT.md](CONTRACT.md).
Choose the route during analysis and check it again before writing. Do not
create new skills merely to mirror this table.

| Route | Applies when | Work and exit evidence |
| --- | --- | --- |
| Small change | Behavior and scope are known and impact is bounded | Short specification and plan, minimal edit, relevant checks and author review |
| Feature, prepare phase | A new capability has material unresolved requirements | Inspect context, resolve material decisions in the interviews, propose design, acceptance criteria and verification |
| Feature, execute phase | Specification and plan are approved and implementation is authorized | Preserve accepted decisions, implement by risk, verify affected consumers and review |
| Bugfix with red test | Correct behavior is known and current behavior diverges | Reproduce the relevant failure, establish meaningful red evidence, correct cause, show green and regression checks. Run reproductions that write files during approved execution |
| Systematic diagnosis | Cause or affected boundary is uncertain | Form a discriminating hypothesis, trace the first divergence, experiment, revise at contradiction, then route to a fix when requested |
| Review feedback | A finding or proposed patch needs evaluation | Verify raw evidence against the actual contract and callers. For requested fixes, follow the workflow for changes or repair within the existing approved scope |

A change that alters a shared contract, permission, persistent format, or
cross-component invariant, or uncovers broader material consumers needs a route
with deeper analysis. Move to feature execution if the approved specification
and plan still cover the work. Otherwise diagnose or prepare the missing
decision and follow the contract's revision rules. Carry forward known answers
and approvals that still apply.

For a bug, a test that never reaches the failing path is not a reproducer. If a
reproducer cannot be run, state why and use the strongest available observation;
never report red/green that did not happen. Platform constraints may require
manual/device checks alongside automated tests. Avoid arbitrary coverage targets.
