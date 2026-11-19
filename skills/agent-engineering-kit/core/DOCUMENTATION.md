# Writing and maintaining documents

Apply these rules when a selected route or the user calls for documentation.
They govern the requested artifact; they do not create a specification, interview,
approval gate or ticket for every edit. Routing and authority remain in
[CONTRACT.md](CONTRACT.md) and [ROUTES.md](ROUTES.md).

## Reader and purpose

Identify who needs the document and what they must understand or do after reading.
Reuse an applicable existing document and the project's conventions before
creating another source of truth. Choose the appropriate kind:

| Kind | Essential content |
| --- | --- |
| Specification | Intended outcome, scope, observable behavior, constraints and acceptance |
| System reference | Verified current behavior, boundaries, dependencies and limitations |
| How-to or runbook | Preconditions, ordered actions, expected results and recovery where relevant |
| Decision record | Context, alternatives, chosen approach, reasons and consequences |
| Task description | Reader-facing change, Impact and actionable acceptance cases; see ROUTES |

A specification describes intended behavior; a reference describes observed
implementation. Keep both when they serve distinct needs, linking between them.
Do not silently replace an accepted requirement with whatever the code currently
does. Record discrepancies and resolve material changes through the existing route.

## Evidence and prose

- Start with the outcome or question the reader needs answered. Use concrete
  subjects, direct verbs and short connected explanations. Remove filler,
  unsupported evaluations and bureaucratic phrasing.
- Explain why significant choices were made, alongside their effects. Name
  relevant boundaries and interactions instead of copying classes into prose.
- Separate observed facts, accepted decisions, proposals and unknowns. Cite the
  relevant source or repository location; identify inaccessible or stale evidence.
  Do not invent behavior, measurements, examples presented as real results, or
  approval. Describe actual API responses from handlers and checks, using comments
  only as supporting evidence; distinguish desired changes from current behavior.
- Explain unfamiliar terms on first use. Match the reader's and project's
  language, preserving exact identifiers needed to find a source or run a command.
- Prefer explanations to copied implementation. Use short code, payload or command
  examples when syntax is essential; make placeholders and example status explicit.
  Link to implementation for detail that changes with the code.
- Use a table for mappings or state/trigger/result comparisons and a diagram for
  a flow or relationship when it improves understanding. Avoid duplicating a long
  narrative in a diagram. Link visual claims to the relevant design when available.
- Keep links usable in the destination. Prefer repository-relative paths for
  repository documents; avoid machine-specific paths and private material in
  distributable documentation. Never assume a particular tracker or design tool.

## Adaptable outlines

Select sections that answer real questions. Do not pad documents to a fixed
length, retain empty headings, or require a full template for a wording fix.

For a substantial specification, cover:

1. Outcome, scope and exclusions; supplied success measures and their conditions.
2. Sources, relevant current behavior, accepted decisions and unresolved choices.
3. Scenarios and observable results, including relevant empty/error/interruption
   states, access conditions and variants. Assign requirement IDs where useful
   for tracing requirements to acceptance checks.
4. Components and integration boundaries, data/error contracts and constraints;
   separate responsibilities across systems and explain significant tradeoffs.
5. Impact, dependencies, risks, preserved behavior and any compatibility change.
6. Acceptance cases and verification approach; explicit deviations only where
   agreed. Keep implementation sequencing in the execution plan.

For a system reference, explain purpose, responsibilities, interaction/data flow,
public contracts, operating constraints and known limitations, grounded in the
implementation inspected. State the inspected revision or date when freshness
matters. For a how-to, state prerequisites, steps, observable success and relevant
failure/recovery paths. Do not invent a UI or product KPI for a technical system.

## Lifecycle and consistency

Before implementation, label proposed requirements as draft or in review using
project conventions. An approved status requires an actual owner decision about
that version. During work, retain decisions and record significant deviations
with their reasons and effects. Preserve unresolved questions with an owner or
next action when known; a follow-up link does not make a blocking decision resolved.

After implementation, compare affected documents with the actual diff and check
results. Update descriptions, links and relevant metadata. Distinguish implemented
behavior from verified behavior and remaining gaps; do not mark completion merely
because the document was written. Check affected dependent documents for conflicting
contracts or instructions, within authorized access and edit scope.

Use project version/status conventions for substantive documents. Revise material
requirements and approvals under CONTRACT; routine corrections within accepted
scope need no extra approval. Preserve useful decision history without logging
every typo. Do not introduce mandatory Git tags, additional reviewers, age-based
deletion or automatic publication as documentation rituals.

Before handoff, check that the intended reader can act, claims match their sources,
terms and links are clear, acceptance is observable, and unresolved decisions and
verification limits remain visible. Report only checks actually performed.

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
