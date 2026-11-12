# Development routes

Choose the smallest sufficient process before creating specifications, plans or
interview questions. Follow authority and route-specific approvals in
[CONTRACT.md](CONTRACT.md). These methods are internal to the single AEK skill;
no separate skill installation, tracker, configuration file or network is needed.
For requested documents, apply [DOCUMENTATION.md](DOCUMENTATION.md) for writing,
adaptable outlines and maintenance. This adds no process artifacts or approvals.

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
Resolve technical facts from sources. Use the requirements interview below for
remaining owner decisions, choosing its depth to fit the gaps. Do not invent
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
Reuse earlier analysis and answers before preparing questions.

### Requirements interview

After research, identify ambiguities, contradictions, missing scenarios and gaps
that prevent acceptance. Check the purpose, relevant success measures, variants,
errors, interruptions, reused behavior, Impact and architectural choices. For
acceptance, establish how the reader reaches and completes a meaningful scenario:
screen, endpoint, command or other relevant surface; access/account/environment
conditions; action and observable result. Being part of an epic is not itself a
scope defect. Ask only about categories with a material unresolved gap.

| Priority | Consequence | Handling |
| --- | --- | --- |
| Blocking | A safe or testable requirement cannot be decided | Ask before dependent conclusions or implementation |
| Material | Changes scope, architecture or acceptance | Ask or explicitly defer with its effect and owner decision |
| Contextual | Adds background without changing the task | Optional; never delay a usable draft |

Present a short summary of consequential gaps, not the entire investigation.
In ordinary preparation, group related questions into small batches, typically
up to three; ask fewer when answers determine subsequent questions. In an
explicitly requested or necessary deep interview, ask one question at a time.
Explain the gap and consequence, propose a source-backed option when available,
and invite a choice or alternative. Do not ask for information already supplied.

Do not manufacture a metric or treat "improve" as a measured success condition.
When a metric is required, identify its measure and threshold, baseline or
comparison. Otherwise mark it not set without blocking independently testable
behavior. A bug's acceptance normally concerns the reproducer and regression;
ask for a product KPI only when the task requires one.

Record answers in the relevant specification and requested task description,
including why a significant choice was made. Preserve unanswered decisions with
their priority, consequence and owner/next action when known. Pause only dependent
work. If no material questions remain, draft without a ceremonial final
confirmation. Do not invent questions to fill a batch or populate every category.

Use source-backed requirement IDs, scenarios, relevant state tables, data/error
contracts, flags, nonfunctional constraints and acceptance checks. Include
analytics only when supplied or required; label unknown metrics honestly. Save a
requested document within authorized paths as draft/in_review; approved status
requires an actual owner decision. A document request does not authorize code.

## Ticket for humans

Use when drafting or updating a project task for its intended readers: QA,
product, operators or engineers. The method works for issues, tickets and local
task files, regardless of tracker. Use the user's or project's language. A tracker is
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
untested cases or missing designs complete. Before external publication, present
the complete reviewable draft with remaining gaps and their effects; use existing
publication authority or obtain it if missing. An authorized draft may retain
unresolved questions. Publishing it does not mark it ready or permit dependent
implementation before required decisions and approvals. Never assume a tracker
is connected.

For product/QA sections, use user-facing language and keep internal type names,
file paths and implementation details in the technical reference. A reader without
code access should understand the change and perform its product QA scenarios.
For engineering tasks, describe acceptance using the tools, access and precise
identifiers that the intended technical reader needs.

### Task description style

- Lead with why the task exists and the observable change. Organize behavior in
  the order the reader encounters it. One item describes one meaningful change;
  do not impose a minimum item count or turn this section into a coding checklist.
- Describe the relevant surface explicitly. For technical work, this may be an
  API, command, build or operating procedure rather than a screen. Technical
  identifiers are appropriate when the intended reader needs them to act; explain
  them and keep unrelated implementation detail in the engineering reference.
- Explain unfamiliar product terms on first use. Preserve established terms when
  they are more precise than a vague paraphrase. Do not use class names, JSON
  fields or log tags as substitutes for explaining product behavior.
- For visual differences, name the variant, relevant layout and exact design
  reference when available. "Large" or "compact" alone does not define behavior.
  If the design is missing, state the gap instead of inventing dimensions.
- Describe Impact through affected flows or contracts, preserved behavior and
  practical risks. A task with no user interface still has technical consumers;
  absence of UI does not make Impact automatically inapplicable.
- Make acceptance cases independently usable: preconditions, named surface,
  action and expected result. Put the main scenario in execution order, followed
  by relevant errors, variants and regressions. Keep analytics cases only when
  events are part of the requirements. Link a fuller test plan when one exists.
- Separate expected results from executed results. A checklist is not evidence
  that tests ran. An undefined error response is an open question, not permission
  to invent a notification or fallback. Record resolved analysis questions only
  when there are actual decisions; omit empty sections.
- When a specification exists or is required by the route, link it, including
  branch/revision where needed to find an unmerged document. Add a short technical
  summary when helpful; do not paste or weaken the specification to make the task
  description shorter. Task writing alone does not require a specification.

For example, replace "add retry handling" with "Export screen: after a failed
upload, Retry sends the same selected file again" only when that behavior is
established. An acceptance case adds the network/account preconditions and the
observable result. For a CLI task, identify the command, input and exit/output
contract instead. Never turn an illustrative example into a new requirement.

Before handoff, verify that readers can understand the change and perform the
cases using the description and linked sources, that supplied metrics have real
success conditions, and that claims of readiness match the evidence. Adapting
formatting or writing a draft does not authorize tracker creation or publication.

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
