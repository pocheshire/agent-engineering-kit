# Portable workflow records

AEK's offline workflow helper reads JSON and prints JSON. It does not execute
project checks, start models, delegate to agents, activate native goals, write
records, or grant permissions. Run it with Python 3.9 or newer:

```sh
python3 -B skills/agent-engineering-kit/core/aek.py work template task
python3 -B skills/agent-engineering-kit/core/aek.py work template attempt
python3 -B skills/agent-engineering-kit/core/aek.py work validate task.json
python3 -B skills/agent-engineering-kit/core/aek.py work validate - < attempt.json
python3 -B skills/agent-engineering-kit/core/aek.py work next --task task.json --history attempts.json
python3 -B skills/agent-engineering-kit/core/aek.py work stability --required cases.json --min-repeats 3 run-1.json run-2.json run-3.json
```

`template` also accepts `run`, `delegation`, and `modernization`. Its output is the
canonical small synthetic example of each record shape. Examples deliberately
contain unknown observations, pending checks, missing capabilities, or unfinished
migration receipts. They establish structure, never actual execution or readiness.
Capture stdout in a file only when that write is within your authorized scope.
The module can also run directly as `python3 -B .../core/workflow.py ...`; importing
it exposes `main(argv)`, `validate`, `assessment`, `task_digest`, `next_action`,
`stability`, and `template`. Helpers return dictionaries; `main` emits JSON and
returns an exit code.

Every record has integer `version: 1`, a `kind`, and a nonempty `id`. Versions and
counts reject booleans; counts are nonnegative integers; numbers must be finite.
IDs in each collection must be unique. Unknown usage is explicit `null`, never
zero. Duplicate JSON object keys, invalid input, missing required fields, or
unsupported kinds produce a JSON error on stdout and exit 2. Valid evaluations
exit 0: inspect `action`, `ready`, or `status` to distinguish continuation,
readiness, and stability. Additional metadata fields are allowed, remain part of
the record digest, and cannot contain nonfinite numbers. Help text follows the
normal command-line help convention.

## Tasks and attempts

A task states the outcome and nonempty check catalog. Each check has an ID,
invariant, and explicit `mandatory` boolean; at least one is mandatory. Authority
lists granted `read_scope` and `write_scope`, the corresponding required scopes,
and granted/required publication booleans. Scope membership is exact symbolic
membership: the helper does not infer filesystem containment or host permissions.
The host and human must verify that the recorded grants are real.

Budgets contain positive attempt and elapsed-second caps and an optional positive
token cap (`null` or omitted means no explicit token cap). `checkpoints` are named
planning checkpoints; they do not stand in for checks or review receipts.
`independent_review_required` is explicit. Optional `nativeGoals` is host metadata;
the helper always reports `native_goals_activated: false`. A recorded request is
not a host activation.

History is a JSON array in chronological order, including every failed attempt.
Each attempt carries the task ID, canonical `task_digest`, sequential number
starting at 1, and `previous_attempt_digest` (null for the first attempt). Obtain
the digest through `validate`'s output or the importable digest helpers. Canonical
hashing uses sorted JSON keys, compact separators, and SHA-256. Editing a task
invalidates its old history binding; it does not authorize dropping prior usage
or creating a fresh budget for the same continuing work. Do not omit retries:
the chain detects gaps within supplied history, but cannot discover a concealed
history or authenticate the start of a task.

Attempts record revision, author, actual check outcomes, structured findings,
remaining delta, failure fingerprints, usage, and optional independent review.
The `review` key is mandatory, with null when no receipt exists. The
`previous_attempt_digest` key is mandatory, including null for sequence 1.
Check outcomes have ID, status (`pass`, `fail`, `skip`, `unknown`), executed count,
evidence references, and revision. A pass needs positive executed count and
nonempty evidence. Missing, skipped, failed, stale, or unknown mandatory checks
cannot complete a task. IDs not declared in the task are rejected. Finding IDs
persist across history; a finding stays open until a later record explicitly
resolves that ID with evidence. An open finding retains its highest unresolved
severity across retries; reissuing it as low severity is not a resolution. Open
critical, high, or medium findings block completion; low findings remain visible for disposition.

A review receipt names the reviewer, explicit independence boolean, reviewed
revision, `pass` or `changes_requested`, and nonempty evidence. Required review
must be independent, by someone other than the attempt author, passing, and bound
to the latest attempt revision. This is a receipt requirement, not a mechanism
for proving reviewer identity or independence.

`next` derives `continue`, `complete`, or `stop`. Completion requires all mandatory
checks passing on the latest revision, no open material findings, empty remaining
delta, and the required review receipt. Missing authority stops immediately.
All attempts contribute tokens, seconds, tool calls, and cost, including failures.
An unknown value makes that metric's total unknown; unknown seconds stop budget
assessment, and unknown tokens under an explicit token cap stop assessment.
Reaching an attempt, time, or token cap stops even if the latest attempt claims
success; exhaustion never produces false completion. Repeated unchanged nonempty
failure fingerprints stop when neither remaining delta shrinks nor passing check
IDs increase. A changed revision alone is not evidence of progress.

## Run manifests and stability

A run separates `requested` configuration from `observed` configuration. Both
name model, effort, harness, version, entry, tools, and permission. Requested
values are explicit strings (tools is a list); each observed value may be null
when the host did not expose it. A requested model or effort is never silently
copied into observations. Record host observations from raw execution evidence.

Run identity includes invocation ID, trace hash, live boolean, cache-enabled
boolean, source revision and hash, fixtures hash, artifact-name to SHA-256 mapping, case
outcomes, and usage. Here `cache_enabled` concerns answer/verdict replay or reuse
by the evaluation harness. Provider prefix/KV cache usage is a separate observed
metric and must not be described as disabled without host evidence. Fresh model
invocations may still use provider prefix caching. Artifact hashes identify the declared bytes; the helper does
not read or authenticate those artifacts. Usage always includes tokens, seconds,
tool calls, and cost; unknown fields stay null. Define currency and pricing basis
in accompanying evidence before comparing costs.

The required catalog is either a nonempty JSON array of unique case IDs or an
object with `required_ids`. Each run must contain exactly that set, without
replacement, omissions, extras, or duplicates. Stability requires at least the
positive `--min-repeats` count, live uncached invocations, unique run IDs,
invocation IDs and trace hashes, complete observed configuration, and identical
observed config/version, source revision/hash, and fixtures across all repeats. The helper
rejects unknown effective settings; it does not infer them from requested ones.

Results include each case's pass rate, adjacent pass/fail flips, and whether all
repeats passed. Only positive executed passing outcomes bound to the run
source revision count as passes; stale, skipped
or unknown cases count as unsuccessful repeats. `stable` requires every required
case to pass in every repeat. Totals include failed runs. Accepted runs pass all
required cases. Cost per accepted run is total cost across all repeats divided by
accepted runs; it is null if any cost is unknown or no run was accepted. Other
metric totals independently remain null when any contributing value is unknown.
This is a comparison of supplied records, not proof that live invocations ran.

## Delegation and modernization

A delegation profile specifies script/agent method, explicit portable model and
effort strings, brief, scope, seconds/token budget, escalation rule, required
capabilities, and available capabilities. Core defaults do not pin provider model
IDs. `validate` assesses `ready` only when required capabilities are available.
Pure mechanics prefers a script: an agent profile marked `pure_mechanics: true`
is not ready until its method is changed to script. The helper never launches
the script or agent or discovers host capabilities on its own.

A modernization record identifies the pilot, baseline and candidate revisions,
input hash, baseline evidence, approved differences, exact required parity IDs,
actual parity checks, rollback instructions and verification boolean, and named
checkpoints with approval booleans and evidence. Readiness requires every parity
check to pass on the candidate revision, exact nonempty case coverage, approved
checkpoints with evidence, and verified rollback. Placeholder values such as
`TODO`, `TBD`, `unknown`, angle-bracket values, or the all-zero placeholder hash
cannot satisfy readiness. Empty parity catalogs and zero-execution passing checks
are invalid. Baseline evidence, approvals, and rollback verification must refer
to real results; structural acceptance does not independently prove them.

All assessments carry the same limitation: **record validation is not
authentication**. Inspect raw artifacts, instruction authority, actual host
configuration, execution identity, and independent review separately. Schema
acceptance is not behavioral validation, host runtime validation, or catalog
publication approval.
