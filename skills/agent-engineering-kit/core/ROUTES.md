# Development routes

## Task router

Before opening project sources, apply the pinned [authority rules](CONTRACT.md#authority-and-trust)
and scoped project instructions. Select one row. Read its named section and the relevant project
evidence. Stop when the minimum outcome and checks on affected paths are satisfied.
Extend the search along a concrete dependency, conflict or unresolved decision.

| Task | Route | Minimum outcome | Read now | Expand when |
| --- | --- | --- | --- | --- |
| Question, analysis or review | Read-only | Grounded answer or findings | Named object, definition and source of observed behavior | Value originates elsewhere or sources disagree: trace the relevant boundary |
| Editorial documentation, bounded maintenance or disposable prototype | Direct work | Requested result, check and author review | [Direct work](#direct-work-and-small-change) and target fragment | Anchor, command or instruction meaning changes: inspect references or callers |
| Known low-risk change in one screen, flow or local mechanism | Small change | Focused edit and proportionate check | [Small change](#direct-work-and-small-change), local mechanism and nearest check | Shared consumer, permission or persistent format appears: trace [Impact](CONTRACT.md#discovery-contract) and reassess route |
| Known behavior with an observed defect | Bugfix with red test | Same relevant check before and after, plus regression evidence | [Bugfix](WORKFLOW.md#bugfix-with-red-test), expected behavior and reproducer | Unexpected green or different symptom: open [diagnosis](#escalation-and-diagnosis) |
| Uncertain cause or boundary | Systematic diagnosis | Discriminating observation and applicable fix route | [Diagnosis](#escalation-and-diagnosis), closest working and failing cases | First divergence crosses a boundary: inspect its producer or consumer |
| Substantial feature, unresolved product behavior or high-impact contract | Feature, prepare | Grounded specification and blocking decisions resolved | [Feature](WORKFLOW.md#feature-in-two-phases), [Discovery](CONTRACT.md#discovery-contract), governing requirements and [approval gates](CONTRACT.md#two-phase-procedure) | Shared contract: trace consumers. Material owner choice: use the [interview](DOCUMENTATION.md#requirements-interview) |
| Substantial work with accepted specification and implementation request | Feature, execute | Approved plan, checked implementation and review | Accepted specification, [plan](WORKFLOW.md#execution-plan) and [approval gates](CONTRACT.md#two-phase-procedure) | Independent work becomes ready: [delegate](WORKFLOW.md#delegation-and-cost). Material revision: reopen affected approval |
| Standalone requirements document or deep interview | Specification interview | Source-backed requirements and owner decisions | [Specification interview](DOCUMENTATION.md#specification-interview) and supplied sources | After research, a choice changes acceptance: ask the owner |
| Product or QA ticket | Ticket for humans | Reader-ready draft and actionable cases | [Ticket](DOCUMENTATION.md#ticket-for-humans), original request and intended audience | Describing completed work: inspect actual diff and case results |
| Review feedback | Review feedback | Verified finding and authorized response | Finding, reviewed revision, governing rule and observed result | Confirmed correction: follow the affected change route and check analogous consumers |

When drafting a substantive document, consult the relevant [writing guidance](DOCUMENTATION.md#reader-and-purpose).
Setup follows MODES.md. Honor an explicitly selected process, then check its
applicability before writing. Do not use a file count or the word “documentation”
as proof of low risk: a one-line permission rule or public API contract is a
high-impact change. A spelling correction in a README is direct work, even when
this repository contains a large product.

If a material decision is missing, ask only about that decision and continue
independent work. Otherwise briefly state the route when useful and proceed.
Never require a formal confirmation of the routing choice. A handoff carries
known requirements, answers, evidence, scope, approvals and verification context;
it does not restart intake.

## Direct work and small change

Use when expected behavior is clear, impact is bounded and no material product
choice or high-impact contract change is hidden in the edit. A local copy,
spacing, color or condition adjustment may fit; a change to access control,
payment behavior, persistence or navigation semantics needs deeper analysis.

1. Locate the relevant files and consumers. Check local instructions and pending
   changes; preserve unrelated work. Reuse the current task context and branch.
2. State the intended edit and check briefly if helpful. Proceed under the clear
   request; no standalone specification, approval turn or durable plan is needed
   unless the user or applicable project rules require one.
3. Make the smallest coherent edit. Recheck route boundaries before expanding it.
4. Check the result in proportion to impact: prose diff and affected links for a
   README edit; relevant existing tests or runtime/UI cases for behavior. Do not
   build the whole product or create a test just to verify an ordinary wording
   correction. Required project checks still apply.
5. Review the diff and report the result and limits. For QA delivery, give one to
   three self-contained cases with observed results where available. Use the
   ticket method only when a ticket is actually requested or part of the task.

No automatic branch creation, commit, PR, tracker write or background QA agent is
part of this route. Perform those actions only within existing task authority.

## Escalation and diagnosis

Reassess when consumers expand, a shared contract or persistence boundary changes,
a new product decision is needed, or permissions, payment, migrations or
cross-component invariants are involved. Announce the reason and switch to the
appropriate existing route before dependent implementation. Carry forward valid
answers, approvals, branch, changes and evidence. A purely technical transition
within authorized scope does not itself require new permission. Material changes
to an approved specification or plan follow the contract's revision rules.

For diagnosis, state a hypothesis and an observation that distinguishes it from
alternatives. Trace the first divergence and compare working/failing cases. At a
material contradiction, verify the observation, revise the hypothesis and Impact,
and inspect analogous paths before another patch. For review feedback, validate
the finding against raw evidence, actual callers and the governing contract;
separate defects, suggestions and owner decisions.

## Feature in two phases

See [feature preparation and execution](WORKFLOW.md#feature-in-two-phases).

## Bugfix with red test

See the [bugfix procedure](WORKFLOW.md#bugfix-with-red-test).

## Specification interview

See the [specification interview](DOCUMENTATION.md#specification-interview).

### Requirements interview

See [requirements questions](DOCUMENTATION.md#requirements-interview).

## Ticket for humans

See [ticket preparation](DOCUMENTATION.md#ticket-for-humans).

### Task description style

See [task description style](DOCUMENTATION.md#task-description-style).
