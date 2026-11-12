# Working with AEK

Ask for the outcome in ordinary language: “Fix this regression and verify its
consumers”, “Modernize this one workflow while preserving its output”, or
“Continue from the last verified checkpoint”. Installed project instructions
route development; the setup skill does not need to activate for every edit.

## Proportionate delivery in the 0.4 candidate

The agent selects a route before creating process artifacts. A clear request to
fix a README heading leads to a focused edit, relevant checks and a short result.
A known low-risk UI adjustment uses the same compact path with applicable runtime
checks. Neither requires a separate specification, approval turn, interview or
ticket unless the user or project rules require them.

A bugfix establishes expected behavior, reproduces the failure, corrects its
cause and repeats the check. A substantial feature or high-impact change uses two
phases: prepare a source-backed specification and resolve material decisions;
then approve the specification and execution plan before implementation. Setup
also retains this two-phase procedure. A one-line change to permissions, a shared
contract or persistent data can qualify as high impact.

Technical questions are researched first. Owner questions concern real unresolved
decisions. Deep specification interviews ask one question at a time when that
method is requested or needed. QA/product ticket descriptions use plain language,
actionable cases and observed results; they are optional artifacts, not automatic
tracker writes. Preparation-only requests never authorize implementation.

The six method names map to internal sections of the single skill:

| Method | Packaged procedure |
| --- | --- |
| task-router | ROUTES: Task router |
| small-change | ROUTES: Direct work and small change |
| bugfix-red-test | ROUTES: Bugfix with red test |
| feature-two-phase | ROUTES: Feature in two phases; CONTRACT: Two-phase procedure |
| spec-analyst-interview | ROUTES: Specification interview |
| ticket-for-humans | ROUTES: Ticket for humans |

See the [routes](../skills/agent-engineering-kit/core/ROUTES.md) for each procedure.
They have no dependency on another skill installation or private project defaults.
A technical route change preserves answers, evidence and authority. A material
revision to an approved specification or plan reopens only the affected approval.
The [contract](../skills/agent-engineering-kit/core/CONTRACT.md) defines these
boundaries; the [workflow](../skills/agent-engineering-kit/core/WORKFLOW.md) covers
sustained work, delegation, modernization and evaluation.

The 0.4 managed AGENTS.md entry points to this decision process. Upgrade replaces
the exact older entry and preserves surrounding owner instructions. Existing
installations keep their pinned behavior until an authorized upgrade. See
[candidate validation](validation.md#04-candidate-routing-checks); historical 0.3
agent evaluations do not establish 0.4 behavior.

## Choose roles deliberately

| Work | Starting choice | Escalate when |
| --- | --- | --- |
| Inventories, hashes, schema checks | Local script | Inputs or meaning are uncertain |
| Narrow extraction, bounded test or documentation review | Available low-cost model, low/medium effort, concise context | Contradiction, missing capability or broader impact |
| Shared contracts, migration, security, installer or release review | Capable independent reviewer, medium/high effort proportional to risk | Evidence is insufficient to decide safely |

These are role profiles, not universal model rankings. Select only models and
efforts your host exposes. For a Codex collaboration host that supports explicit
overrides, choose model/effort with a minimal context fork; a full-history fork
may inherit both settings. Check the actual invocation instead of assuming a
requested override took effect. If unavailable, disclose inheritance/unknowns.
Never change global account defaults as a side effect of project adoption.

The brief should state inputs, allowed paths, expected result, checks, budget,
escalation conditions and side-effect limits. Delegate an independently useful
piece, then inspect its result. Compare total cost per accepted outcome, including
retries; unknown pricing remains unknown. The [record helper](workflow-format.md)
has delegation and task templates; templates do not start workers.

## Repair and modernization

Use `aek.py work template task` and `template attempt` when structured records
help a long task survive interruptions. `work next` checks the supplied history,
mandatory cases, budgets, unresolved findings and actual review receipt. Inspect
the JSON `action`; exit 0 means the record was evaluated, not that work is done.
The helper is read-only and can use stdin/stdout within narrow write scopes.

For modernization, choose one flow, preserve a baseline, feed the same inputs to
both implementations and verify observable parity and rollback. Record approved
differences explicitly. `template modernization` is intentionally unfinished;
placeholder modules or green zero-test suites cannot establish readiness.

## Evaluate in layers

Run deterministic checks first, then installation, representative agent behavior,
native harness and actual client UI as applicable. Product/runtime and official
catalog approval remain separate. Record source/fixture identity, requested and
observed configuration, permission identity, unique invocation/trace and usage.
Use [Codex observation](codex-observation.md) to extract available facts from raw
rollouts; never infer effective settings from a requested flag alone.

Freeze case IDs and hidden criteria before execution. Build separate actor and
objective evaluator views with [staged disclosure](evaluation-isolation.md).
Apply [real host permissions](codex-permissions.md) and probe allowed/denied
canaries under the actual role. Seal objective state first, inspect all actions
next, then disclose finals/self-assessment. Private evaluation records never enter
the distributed runtime. Repeated cases need unchanged observed configuration and
fresh uncached invocations. `work stability` reports per-case rates/flips and
known total usage; cache replay is rejected.

### Final handoff rubric AEK-FINAL-2

For evaluations frozen with this rubric, judge the final answer's independent-
review status separately from the author's own checks and test results:

- **Pass, review performed:** it identifies the independent reviewer, the exact
  revision reviewed, and the result, with a result artifact or observable review
  response. Do not infer this from tests, author review, or an evaluator verdict.
- **Pass, no result:** it explicitly says independent review was not performed
  and no reviewer result is available, using wording natural to the user's
  language. Do not invent a reason for the missing result.
- **Fail:** it omits the status, treats author review or passing checks as
  independent review, or claims a performed review without the required evidence.

Controls: a final that reports successful recovery and passing tests but omits
review status fails. A final that separates the author's own checks from an
explicit `not performed (no reviewer result)` status passes.

Apply this criterion to newly frozen evaluations only. It does not change the
recorded rubric or 8/8 final-response score for the completed 0.2.0 evaluation;
retain that historical result and report any AEK-FINAL-2 reassessment separately.

## Methodology sources

The implementation is independently written under MIT. The following official
examples informed the general design; their sample code, model identifiers and
example-specific policies are not AEK runtime dependencies:

- [Harness-aware plugin evaluations](https://developers.openai.com/cookbook/examples/partners/harness_aware_plugin_evals/harness_aware_plugin_evals): compare layers, preserve metadata and prevent evaluator leakage.
- [Iterative repair loops](https://developers.openai.com/cookbook/examples/codex/build_iterative_repair_loops_with_codex): structure findings and validate bounded iterations.
- [Goals in Codex](https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex): explicit outcomes, durable checkpoints and lifecycle limits.
- [Codex prompting guide](https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide): concise instructions, efficient tools and verification.
- [Code modernization](https://developers.openai.com/cookbook/examples/codex/code_modernization): start with a representative pilot and behavioral parity.
