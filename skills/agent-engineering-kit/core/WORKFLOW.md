# Bounded autonomous work

Apply this procedure when work spans retries, checkpoints, delegated roles,
behavioral evaluations or modernization. A small change still uses the short
Discovery and route in CONTRACT.md/ROUTES.md. Do not create task paperwork for
every edit. Reuse an existing issue, plan or conversation checkpoint; persistent
records require the task's write authority.

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
2. Repair the supported cause within authority. Reopen Discovery when a material
   contradiction invalidates the hypothesis; do not pile on speculative patches.
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

Use deterministic scripts for mechanical inventories, hashes and format checks.
Delegate only when a bounded independent task can save time or improve quality.
Give each worker a concise brief: input locations, outcome, allowed scope,
acceptance checks, budget, model/effort, stop/escalation conditions and forbidden
side effects. Share only necessary context; do not silently inherit an expensive
parent profile. Select among capabilities the host actually exposes. Use a lower
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

Repeat critical cases with unchanged effective configuration, package and fixtures
and uncached independent invocations. Report per-case pass rates, flips and whether
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
