# Codex rollout observation

`python3 scripts/capture_codex_run.py ROLLOUT.jsonl` reads a Codex rollout
locally and writes one JSON object to stdout. Optional `--requested-model` and
`--requested-effort` values record the request separately from observed
`turn_context` metadata.

The schema is `codex_observation` version 1. It contains the rollout SHA256,
session and invocation identifiers and CLI version when present, observed and
requested model/effort, distinct tool names, a tool invocation count, and the
last cumulative token usage snapshot. `usage.total_tokens` is emitted only when
the provider supplied that field; it is never calculated from component counts.
`cache_write_input_tokens` is also retained when supplied. `cost` and `seconds`
are null because the rollout alone does not establish them. Missing or
conflicting turn contexts produce null observed values and a diagnostic.
Conflicting session or version metadata also produces a null value and a
diagnostic.

Only allowlisted metadata is emitted. Message bodies, reasoning, tool arguments
and results, unknown fields, environment values, and credentials are omitted.
The SHA256 identifies the exact input bytes; it does not authenticate the
rollout or prove that Codex actually executed it. Missing metadata remains
unknown, and no token usage or price is estimated.

Malformed JSONL, duplicate JSON keys, invalid UTF-8, and non-finite JSON numbers
are rejected. The command is read-only with respect to the rollout and reports
errors on stderr with a nonzero exit status.
