# Planning and bounded autonomous work

Use the execution plan for the two-phase routes under [CONTRACT.md](CONTRACT.md).
Direct work and small changes need only a brief action/check summary when useful.
Read the section for the event in the [Discovery contract](CONTRACT.md#discovery-contract).
Reuse the conversation or existing project artifacts for checkpoints. Persistent
records need write authority and applicable approval.

## Execution plan

Use a compact table or similarly scannable layout. Refer to the approved
specification version. Show work items, owners, dependencies, what can run in
parallel, and how each result will be checked. Add a small diagram if it helps
explain dependencies. For each proposed worker, show their task, allowed scope,
expected result, model, and reasoning effort. Where model or effort is inherited,
host-selected, or unknown, report that accurately.

For substantial tasks, launch a read-only subagent by default after drafting
the plan and before presenting it for approval. Provide the draft, the approved
specification, and the review scope. Ask the reviewer to check for missing work,
dependency and ownership conflicts, risks, and gaps in verification. Get the
review result and resolve material findings before presenting the plan.
Use a solo review for small tasks or when host limits, project rules, or the
expected benefit relative to cost make delegation a poor fit. For a substantial
task, state the reason when presenting a plan reviewed by the lead alone.

If the contract requires independent review of the implemented result, show who
will review it or identify the obstacle to arranging that review. Final
acceptance depends on the evidence required by the contract.

## Outcome and checkpoints

Before a long task, record the outcome, authoritative requirements, invariants,
mandatory check IDs, environment/commands, read/write/publication scopes, review
requirement and bounded attempt/time budget. Use a token cap only when usage is
observable. Unknown usage cannot establish compliance with a token cap. Budgets
bound delegated work too; they do not grant resources or extend authority.
Keep a short durable checkpoint: current revision, verified results, unresolved
findings, remaining delta and next discriminating action. Preserve failures and
cost across retries; changing a contract requires an explicit recorded revision,
not resetting history to erase an exhausted budget.

Native Goals are an optional host facility. Create one only on an explicit user
request supported by the host. Goals do not replace project rules or evidence,
and their budget exhaustion is not task completion. Follow the host's lifecycle
and stop rules; never emulate an unlimited background service.

## Review → Repair → Validate

1. Review actual state and actions, identify findings with stable IDs, severity,
   violated invariant, evidence and the smallest remaining delta.
2. Reassess ownership of the remaining work under [Delegation and cost](#delegation-and-cost)
   before starting repairs. Repair the supported cause within authority.
   Reopen Discovery when a material contradiction invalidates the hypothesis.
3. Validate mandatory cases and indirect consumers at the current revision.
   Bind evidence and any independent reviewer result to that revision. Update the
   checkpoint with actual failed and successful usage.

Stop when the accepted outcome and every mandatory check are verified with no
unresolved material finding and required independent review is present. Stop
without declaring completion on budget exhaustion, unchanged failure fingerprints
without progress, missing authority or an unresolved owner choice. Report the
remaining delta and specific next decision. A structural record validator cannot
authenticate a command, a reviewer or a model's claim; inspect raw observations.
The offline `aek.py work` helper emits templates, validates records, derives a
conservative next action and aggregates repeated runs. It never executes commands
or starts agents. `work template task` is a synthetic example, not a grant or a
successful result. Its `--help` explains the interface.

## Delegation and cost

Choose roles to improve quality and shorten time to an accepted result while
minimizing total cost. Account for context transfer, coordination, verification
and likely retries. Use deterministic scripts for mechanical inventories, hashes
and format checks.

For substantial tasks, delegate ready, independent items to subagents by
default when the host supports it and their scope and checks are clear.
Respect the current route and obtain any required plan approval before
assigning implementation. After each integration, on review feedback, and
when resuming, check which remaining items or repairs are now ready. When
several can proceed independently and worker capacity and cost allow,
give each its own subagent assignment before starting local edits. Reuse an
available worker when its context helps. The lead checks the combined result.
Continue under the existing approval while the work stays within scope.
Keep dependent or overlapping edits with the lead when they need a single
owner. Host limits and disproportionate coordination costs can also justify
solo work. When keeping a ready item for local implementation, briefly record
the specific dependency, limit, or cost that motivated that decision.

The lead owns the technical decisions, integration, and quality of the final
result. Give each subagent a precise brief covering the specific review or edits,
input locations, authorized read/write scope, expected result, acceptance checks,
budget, model and effort, and when to stop or escalate. For implementation,
include the approved specification and plan versions when the route requires
them. The lead inspects the actual changes, resolves conflicts, and verifies the
integrated result against the specification.

Provide the project root and resolved paths to the applicable AEK entry and
contract, using the pinned runtime for installed project work. Instruct the
subagent to use its first tool call to read only the pinned entry and CONTRACT's
Authority and trust section. Before product sources, apply scoped project rules
and local adaptations and read the applicable route and any required gates.
Provide the applicable decisions, approvals and checking scope in the brief.

Share only necessary context; do not silently inherit an expensive parent profile.
Select among capabilities the host actually exposes. Use a lower
cost model with low/medium effort for narrow extraction and routine checks; use
a stronger reviewer proportionate to shared contracts, security or release risk.
Do not use a weaker review merely to meet a price target. If the host cannot
select a model/effort, report the inherited/unknown setting rather than claiming
a cheap profile. Keep roles independent of the implementation author where
independent review is required. An actual reviewer result is mandatory evidence.

Compare total tokens, elapsed time, tool calls, known price and cost per accepted
outcome, including failures and retries. A smaller model can cost more overall.
Do not estimate unknown usage/prices or promote one provider/model as universal.

## Layered behavioral evaluation

Before starting test chats, tell the user which acceptance question needs fresh
evidence. Estimate the number of runs and total input and output tokens, including
child agents. Use a range based on comparable runs when usage is uncertain.
Reuse applicable evidence and start with the smallest sample that can answer the
question. Stop when it does. If more cases, hosts, repeats or retries are needed,
or the work would exceed the estimate, show the remaining gap, the additional
runs and their estimated tokens. Wait for the user's explicit approval to expand.

Separate deterministic checks, installation, standalone behavior, native agent
harness, representative client UI, product runtime and catalog publication.
Use the same frozen case IDs/inputs/graders across relevant layers; record where
the environment requires differences. Native CLI success does not prove desktop
UI activation. Capture requested and actually observed model/effort, harness and
version, entrypoint, available tools, permission identity, source/fixture/trace
hashes, invocation ID, cache mode and usage. Requested settings alone are not
observations. Unknown or mixed settings cannot establish comparable repeats.

Freeze hidden criteria outside actor-readable roots. Do not pass criteria or
earlier scores to the performer. An independent evaluator first inspects objective
code/state/tests and trusted original requirements without any generated narrator
files (including local.md, project.json, reports, changed Markdown or finals).
Seal that verdict, then disclose all actions, then author assessment/final replies.
Use explicit file allowlists, immutable hashes, separate host-enforced read roots
and an actual negative read canary. Prompt instructions or staged copies alone
do not prove isolation. Trusted harness receipts bind stages; digests are integrity
checks, not authenticated provenance. Keep private evidence outside distributions.

For stability claims, repeat critical cases within the agreed sample. Use unchanged effective
configuration, package and fixtures and uncached independent invocations. Report per-case pass rates, flips and whether
every repeat passed, plus total known cost. A cached replay, duplicate trace or
different configuration is not a stability repeat. Preserve failed rounds and
do not weaken frozen criteria after observing results.

## Bounded modernization

Start with one representative business flow, not a repository-wide rewrite.
Inventory its consumers, data/API contracts, environment and rollback path.
Capture a working baseline and characterization checks, then define the target
contract. Feed identical frozen inputs to baseline/candidate and compare output,
errors, persistence and relevant performance boundaries. Existing defects are
not silently normalized: record owner-approved differences separately. Check
parity with executed assertions; draft modules, placeholder tests and checklists
do not establish runtime readiness. Review the pilot and verify rollback before
expanding the pattern. Use existing feature/diagnosis routes and project planning
artifacts; no extra skill or compulsory orchestrator is needed.

## Feature in two phases

**Prepare:** apply Discovery, compare requirements with current code and designs,
and identify conflicts, missing states, errors and unfinished user journeys.
Resolve technical facts from sources. Use the [requirements interview](DOCUMENTATION.md#requirements-interview) for
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
2. Trace the symptom to a causal hypothesis. Use [systematic diagnosis](ROUTES.md#escalation-and-diagnosis) when cause,
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
