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
