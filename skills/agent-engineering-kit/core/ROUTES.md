# Development routes

Choose the smallest sufficient process before creating specifications, plans or
interview questions. Follow authority and route-specific approvals in
[CONTRACT.md](CONTRACT.md). These methods are internal to the single AEK skill;
no separate skill installation, tracker, configuration file or network is needed.

## Task router

Start from the request, supplied materials, existing project decisions and
focused inspection. Discover technical facts before asking the owner. For
user-visible delivery, classify a known defect before considering a feature.
Documentation, refactors, CI, tests and prototypes do not automatically enter
product delivery. Their impact still determines analysis and verification.

| Task | Route | Minimum outcome |
| --- | --- | --- |
| Question, analysis or review | Read-only | Grounded answer or findings; no implementation |
| Editorial documentation, bounded maintenance or disposable prototype | Direct work | Requested result, relevant checks and author review |
| Known low-risk change in one screen, flow or local mechanism | Small change | Minimal edit and proportionate acceptance evidence |
| Known correct behavior with an observed defect | Bugfix with red test | Relevant failure before the fix, same check after, regression evidence |
| Uncertain cause or boundary | Systematic diagnosis | Discriminating hypothesis and observation; then the applicable fix route |
| Substantial capability, unresolved product behavior or high-impact contract | Feature, prepare phase | Grounded specification and resolved blocking decisions |
| Substantial work with an accepted specification and requested implementation | Feature, execute phase | Approved plan, bounded implementation, verification and review |
| Standalone requirements document or explicitly requested deep interview | Specification interview | Source-backed requirements and recorded owner decisions |
| Ticket description for product or QA | Ticket for humans | Clear draft with user-visible behavior and actionable cases |
| Review feedback | Review feedback | Verified findings; authorized repairs use the appropriate route |

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

## Feature in two phases

**Prepare:** apply Discovery, compare requirements with current code and designs,
and identify conflicts, missing states, errors and unfinished user journeys.
Resolve technical facts from sources. Batch remaining owner questions; use the
specification interview below when deeper discussion is needed. Do not invent
success metrics or block work on absent optional metrics. Keep an architectural
decision record only when a significant choice warrants one; it complements the
specification rather than replacing it.

Present an engineering specification with outcome, scope, sources, behavior and
states, architecture/integration boundaries, data and errors, Impact, acceptance
checks, risks and unresolved decisions as relevant. Keep implementation details
here; a product ticket has a different audience. Preparation alone ends with a
draft or accepted specification, not product implementation or publication.

**Execute:** confirm the accepted specification, necessary design decisions,
verification approach and requested implementation scope. Reuse existing
approvals. Follow the contract's plan approval, then implement in coherent steps
with dependencies and checks. Review each result, preserve prior decisions and
report acceptance against the specification. Commits and PRs depend on task
authority; stages do not create an extra commit approval ritual.

## Bugfix with red test

1. Establish expected behavior from authoritative requirements and inspect
   existing fixes or triage evidence. Reuse a valid reproducer when available.
2. Trace the symptom to a causal hypothesis. Use systematic diagnosis when cause,
   timing or affected boundaries remain uncertain.
3. Before changing product behavior, run the smallest reproducer asserting the
   correct outcome. A compilation error, unrelated crash or test that never
   reaches the affected path is not red evidence. For an unexpectedly green test,
   inspect the executed ID, fixture, environment, reached path and assertion.
4. If an automated test is unsuitable, record the reason and an observed runtime
   scenario using the real platform (browser, API, isolated database, simulator
   or device). Do not restructure production code solely to manufacture a test.
   If reproduction is unavailable, state the gap and strongest observation;
   do not claim a confirmed cause or red/green that was not observed.
5. Make the minimal supported correction. A bounded known fix needs no separate
   specification or plan approval. High-impact fixes use the contract's two-phase
   procedure before implementation; reproduction and diagnosis may proceed within
   existing authority. Product ambiguity returns to preparation.
6. Repeat the same reproducer, relevant regression cases and applicable build or
   type checks. Distinguish pre-existing unrelated failures. Review the diff and
   record passed, failed and unverified cases. Keep unrelated fixes separate.

## Specification interview

Use for a requested standalone specification or when requirements need focused
owner discussion, not as an obligatory opening for every task.

Research supplied documents, designs and affected code first. For a relevant UI
flow, inspect nested states and trace data through its service to the actual
endpoint/method where accessible. For other platforms, trace the corresponding
boundary. Record inaccessible sources as limits rather than inventing details.

Sort unresolved owner decisions by consequence. In deep-interview mode ask one
question at a time: explain the gap, propose a grounded option, and let the owner
choose. Record each decision before moving on. Name contradictions explicitly.
Pause only dependent conclusions; skip questions already answered by sources.
When no material questions remain, draft the document without a ceremonial final
confirmation. Deferred decisions stay explicit.

Use source-backed requirement IDs, scenarios, relevant state tables, data/error
contracts, flags, nonfunctional constraints and acceptance checks. Include
analytics only when supplied or required; label unknown metrics honestly. Save a
requested document within authorized paths as draft/in_review; approved status
requires an actual owner decision. A document request does not authorize code.

## Ticket for humans

Use when drafting or updating a ticket for QA/product readers. A tracker is
optional: return a draft in chat or an authorized local file when no external
write is requested. Do not create a ticket for every engineering change.

For preparation, use requirements and recorded decisions. After implementation,
use the original ticket, owner answers, actual diff and executed case results.
Preserve product intent; separate observed implementation details in an update.
Do not simplify the engineering specification to make the ticket shorter.

Cover these sections in proportion to the task:

- Outcome and user-visible changes, with supplied success metrics or “not set”.
- Experiment/flag, analytics and design links when relevant.
- Technical reference: specification link and a short architecture note.
- Decisions resolved during analysis, when there are any.
- Impact: affected screens/flows, preserved behavior and user-visible risks.
- QA cases: preconditions, action and expected result, one surface per case;
  include relevant happy path, empty/error states, variants and regression.
- Readiness/completion checklist based on actual evidence.

Give each applicable section a disposition: supported content, an unresolved
question, confirmed not applicable, or a linked follow-up task. Missing behavior
is an explicit gap, not a guessed QA expectation. Do not mark absent metrics,
untested cases or missing designs complete. Before external publication, resolve
material gaps and present the complete reviewable draft; use existing publication
authority or obtain it if missing. Never assume a tracker is connected.

Use user-facing language. Keep type names, file paths and implementation details
in the technical reference. A reader without code access should understand the
change and perform each QA scenario.

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
