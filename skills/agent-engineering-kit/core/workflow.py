#!/usr/bin/env python3
"""Read-only workflow records and conservative decisions; Python 3.9+, stdlib only."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import sys

LIMIT = "Record validation is not authentication; verify raw artifacts and host observations independently."
KINDS = ("task", "attempt", "run", "delegation", "modernization")
METRICS = ("tokens", "seconds", "tool_calls", "cost")
CONFIG = ("model", "effort", "harness", "version", "entry", "tools", "permission")


class Invalid(ValueError):
    pass


def need(condition, message):
    if not condition:
        raise Invalid(message)


def obj(value, label):
    need(isinstance(value, dict), label + " must be an object")
    return value


def string(value, label):
    need(isinstance(value, str) and bool(value.strip()), label + " must be a nonempty string")
    return value


def strings(value, label, nonempty=False):
    need(isinstance(value, list), label + " must be a list")
    for item in value:
        string(item, label + " item")
    need(len(value) == len(set(value)), label + " has duplicate IDs/values")
    need(not nonempty or bool(value), label + " must not be empty")
    return value


def number(value, label, integer=False, positive=False):
    need(type(value) in ((int,) if integer else (int, float)), label + " must be a number (not bool)")
    need((type(value) is int or math.isfinite(value)) and (value > 0 if positive else value >= 0), label + " must be finite and " + ("positive" if positive else "nonnegative"))


def boolean(value, label):
    need(type(value) is bool, label + " must be boolean")


def sha(value, label):
    need(isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None, label + " must be a SHA-256 hex digest")


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def task_digest(task):
    validate(task)
    need(task["kind"] == "task", "expected task")
    return digest(task)


def indexed(value, label):
    need(isinstance(value, list), label + " must be a list")
    found = {}
    for item in value:
        obj(item, label + " item")
        key = string(item.get("id"), label + ".id")
        need(key not in found, label + " has duplicate ID: " + key)
        found[key] = item
    return found


def evidence(value, label):
    strings(value, label, nonempty=True)


def checks(value, label):
    found = indexed(value, label)
    for item in found.values():
        need(item.get("status") in ("pass", "fail", "skip", "unknown"), label + " invalid status")
        number(item.get("executed"), label + ".executed", integer=True)
        strings(item.get("evidence"), label + ".evidence")
        string(item.get("revision"), label + ".revision")
        if item["status"] == "pass":
            need(item["executed"] > 0, label + " pass requires executed > 0")
            evidence(item["evidence"], label + ".evidence")
    return found


def usage(value):
    obj(value, "usage")
    for key in METRICS:
        need(key in value, "usage requires " + key + " (null means unknown)")
        if value[key] is not None:
            number(value[key], "usage." + key, integer=key in ("tokens", "tool_calls"))


def review(value):
    if value is None:
        return
    obj(value, "review")
    for key in ("reviewer", "revision"):
        string(value.get(key), "review." + key)
    boolean(value.get("independent"), "review.independent")
    need(value.get("result") in ("pass", "changes_requested"), "review.result invalid")
    evidence(value.get("evidence"), "review.evidence")


def config(value, label, observed=False):
    obj(value, label)
    for key in CONFIG:
        need(key in value, label + " requires " + key + " (null means unknown)")
        if value[key] is not None:
            if key == "tools":
                strings(value[key], label + ".tools")
            else:
                string(value[key], label + "." + key)
        elif not observed:
            raise Invalid(label + "." + key + " must be explicitly requested")


def validate(record):
    """Validate structure only, returning the same record without mutation."""
    obj(record, "record")
    need(type(record.get("version")) is int and record["version"] == 1, "version must be integer 1")
    kind = record.get("kind")
    need(isinstance(kind, str) and kind in KINDS, "unsupported kind")
    string(record.get("id"), "id")
    # Even extension fields must obey JSON's finite-number restriction.
    try:
        json.dumps(record, allow_nan=False)
    except (ValueError, TypeError) as exc:
        raise Invalid("record must contain finite JSON values") from exc
    if kind == "task":
        string(record.get("outcome"), "outcome")
        cs = indexed(record.get("checks"), "checks")
        need(bool(cs), "task requires nonempty checks")
        for item in cs.values():
            string(item.get("invariant"), "check.invariant")
            boolean(item.get("mandatory"), "check.mandatory")
        need(any(c["mandatory"] for c in cs.values()), "task requires mandatory checks")
        a = obj(record.get("authority"), "authority")
        for key in ("read_scope", "write_scope", "required_read_scope", "required_write_scope"):
            strings(a.get(key), "authority." + key)
        for key in ("publication", "requires_publication"):
            boolean(a.get(key), "authority." + key)
        b = obj(record.get("budgets"), "budgets")
        number(b.get("attempts"), "budgets.attempts", integer=True, positive=True)
        number(b.get("seconds"), "budgets.seconds", positive=True)
        if b.get("tokens") is not None:
            number(b["tokens"], "budgets.tokens", integer=True, positive=True)
        boolean(record.get("independent_review_required"), "independent_review_required")
        strings(record.get("checkpoints", []), "checkpoints")
        if "nativeGoals" in record:
            obj(record["nativeGoals"], "nativeGoals")
    elif kind == "attempt":
        sha(record.get("task_digest"), "task_digest")
        number(record.get("sequence"), "sequence", integer=True, positive=True)
        need("previous_attempt_digest" in record, "attempt requires previous_attempt_digest (null for first attempt)")
        need("review" in record, "attempt requires review (null means no review receipt)")
        previous = record.get("previous_attempt_digest")
        if record["sequence"] == 1:
            need(previous is None, "first attempt must have null previous_attempt_digest")
        else:
            sha(previous, "previous_attempt_digest")
        for key in ("task_id", "revision", "author"):
            string(record.get(key), key)
        checks(record.get("checks"), "checks")
        for finding in indexed(record.get("findings"), "findings").values():
            need(finding.get("severity") in ("critical", "high", "medium", "low"), "finding severity invalid")
            need(finding.get("status") in ("open", "resolved"), "finding status invalid")
            evidence(finding.get("evidence"), "finding.evidence")
        strings(record.get("remaining_delta"), "remaining_delta")
        strings(record.get("failure_fingerprints"), "failure_fingerprints")
        usage(record.get("usage"))
        review(record.get("review"))
    elif kind == "run":
        string(record.get("source_revision"), "source_revision")
        string(record.get("invocation_id"), "invocation_id")
        sha(record.get("trace_hash"), "trace_hash")
        boolean(record.get("live"), "live")
        boolean(record.get("cache_enabled"), "cache_enabled")
        config(record.get("requested"), "requested")
        config(record.get("observed"), "observed", observed=True)
        for key in ("source_hash", "fixtures_hash"):
            sha(record.get(key), key)
        artifacts = obj(record.get("artifacts"), "artifacts")
        need(bool(artifacts), "artifacts must not be empty")
        for key, value in artifacts.items():
            string(key, "artifact name")
            sha(value, "artifact hash")
        need(bool(checks(record.get("cases"), "cases")), "run cases must not be empty")
        usage(record.get("usage"))
    elif kind == "delegation":
        need(record.get("method") in ("script", "agent"), "method must be script or agent")
        for key in ("model", "effort", "brief", "escalation"):
            string(record.get(key), key)
        strings(record.get("scope"), "scope", nonempty=True)
        strings(record.get("required_capabilities"), "required_capabilities")
        strings(record.get("available_capabilities"), "available_capabilities")
        boolean(record.get("pure_mechanics"), "pure_mechanics")
        b = obj(record.get("budget"), "budget")
        number(b.get("seconds"), "budget.seconds", positive=True)
        if b.get("tokens") is not None:
            number(b["tokens"], "budget.tokens", integer=True, positive=True)
    else:
        for key in ("pilot", "baseline_revision", "candidate_revision", "rollback"):
            string(record.get(key), key)
        sha(record.get("input_hash"), "input_hash")
        strings(record.get("approved_differences"), "approved_differences")
        strings(record.get("required_parity_ids"), "required_parity_ids", nonempty=True)
        checks(record.get("parity_checks"), "parity_checks")
        checkpoints = indexed(record.get("checkpoints"), "checkpoints")
        need(bool(checkpoints), "modernization requires checkpoints")
        for item in checkpoints.values():
            boolean(item.get("approved"), "checkpoint.approved")
            strings(item.get("evidence"), "checkpoint.evidence")
        boolean(record.get("rollback_verified"), "rollback_verified")
        evidence(record.get("baseline_evidence"), "baseline_evidence")
    return record


def total_usage(records):
    return {key: (sum(r["usage"][key] for r in records)
                  if all(r["usage"][key] is not None for r in records) else None)
            for key in METRICS}


def passing(check, revision=None):
    return (check["status"] == "pass" and check["executed"] > 0
            and bool(check["evidence"]) and (revision is None or check["revision"] == revision))


def next_action(task, history):
    validate(task)
    need(task["kind"] == "task", "--task must contain task")
    need(isinstance(history, list), "history must be an ordered list of attempts")
    identities = set()
    for i, attempt in enumerate(history):
        validate(attempt)
        need(attempt["kind"] == "attempt", "history may contain attempts only")
        need(attempt["id"] not in identities, "duplicate attempt ID")
        identities.add(attempt["id"])
        need(attempt["sequence"] == i + 1, "attempt sequence is missing, reordered, or reset")
        need(attempt["task_id"] == task["id"] and attempt["task_digest"] == digest(task), "attempt is bound to a different task contract")
        need(attempt["previous_attempt_digest"] == (digest(history[i - 1]) if i else None), "previous attempt digest differs")
        need(set(c["id"] for c in attempt["checks"]).issubset(c["id"] for c in task["checks"]), "attempt includes unknown check IDs")
    totals = total_usage(history)
    result = {"action": "continue", "reasons": [], "usage": totals,
              "attempts": len(history), "authenticity": LIMIT, "native_goals_activated": False}
    def decide(action, *reasons):
        result.update(action=action, reasons=list(reasons))
        return result
    a, b = task["authority"], task["budgets"]
    if (not set(a["required_read_scope"]).issubset(a["read_scope"])
            or not set(a["required_write_scope"]).issubset(a["write_scope"])
            or (a["requires_publication"] and not a["publication"])):
        return decide("stop", "missing_authority")
    if totals["seconds"] is None:
        return decide("stop", "unknown_time_usage")
    if b.get("tokens") is not None and totals["tokens"] is None:
        return decide("stop", "unknown_token_usage_under_explicit_cap")
    # Exhaustion is a stop, never a completion, including the final failed attempt.
    if (len(history) >= b["attempts"] or totals["seconds"] >= b["seconds"]
            or (b.get("tokens") is not None and totals["tokens"] >= b["tokens"])):
        return decide("stop", "budget_exhausted")
    if not history:
        return result
    latest = history[-1]
    observed = {c["id"]: c for c in latest["checks"]}
    mandatory = [c["id"] for c in task["checks"] if c["mandatory"]]
    unresolved = {}
    for attempt in history:
        for finding in attempt["findings"]:
            prior = unresolved.get(finding["id"])
            severity = ("low", "medium", "high", "critical")
            if prior is not None and prior["status"] == "open" and finding["status"] == "open":
                # Downgrading a label is not a resolution receipt. Preserve the
                # highest severity until an explicit resolved finding arrives.
                finding = dict(finding, severity=max((prior["severity"], finding["severity"]), key=severity.index))
            unresolved[finding["id"]] = finding
    material = [f for f in unresolved.values() if f["status"] == "open" and f["severity"] != "low"]
    verified = all(key in observed and passing(observed[key], latest["revision"]) for key in mandatory)
    receipt = latest["review"]
    reviewed = (receipt is not None and receipt["independent"]
                and receipt["reviewer"] != latest["author"] and receipt["revision"] == latest["revision"]
                and receipt["result"] == "pass")
    if verified and not material and not latest["remaining_delta"]:
        if task["independent_review_required"] and not reviewed:
            return decide("stop", "missing_independent_review_for_current_revision")
        return decide("complete", "mandatory_checks_verified")
    if len(history) > 1:
        previous = history[-2]
        same_failures = bool(latest["failure_fingerprints"]) and set(latest["failure_fingerprints"]) == set(previous["failure_fingerprints"])
        progress = set(latest["remaining_delta"]) < set(previous["remaining_delta"])
        previous_pass = {c["id"] for c in previous["checks"] if passing(c, previous["revision"])}
        current_pass = {c["id"] for c in latest["checks"] if passing(c, latest["revision"])}
        if same_failures and not progress and not current_pass > previous_pass:
            return decide("stop", "unchanged_failure_fingerprints_without_progress")
    return result


def stability(required, min_repeats, runs):
    if isinstance(required, dict):
        required = required.get("required_ids")
    strings(required, "required case IDs", nonempty=True)
    number(min_repeats, "min_repeats", integer=True, positive=True)
    need(isinstance(runs, list) and len(runs) >= min_repeats, "insufficient live repeats")
    invocations, traces, ids = set(), set(), set()
    identity = None
    for run in runs:
        validate(run)
        need(run["kind"] == "run", "stability requires run manifests")
        need(run["live"] and not run["cache_enabled"], "stability requires live runs with cache disabled")
        for key, seen in (("id", ids), ("invocation_id", invocations), ("trace_hash", traces)):
            need(run[key] not in seen, "duplicate " + key)
            seen.add(run[key])
        need(all(run["observed"][k] is not None for k in CONFIG), "effective configuration is unknown, not observed")
        effective = {k: run[k] for k in ("observed", "source_revision", "source_hash", "fixtures_hash")}
        if identity is None:
            identity = effective
        need(effective == identity, "effective config/version/source/fixtures differs across repeats")
        need(set(c["id"] for c in run["cases"]) == set(required), "run must contain exact required case IDs")
    per_case = {}
    for key in required:
        outcomes = [passing(next(c for c in r["cases"] if c["id"] == key), r["source_revision"]) for r in runs]
        per_case[key] = {"pass_rate": sum(outcomes) / len(runs), "flips": sum(a != b for a, b in zip(outcomes, outcomes[1:])), "all_repeats_pass": all(outcomes)}
    accepted = sum(all(passing(c, r["source_revision"]) for c in r["cases"]) for r in runs)
    totals = total_usage(runs)
    return {"status": "stable" if all(v["all_repeats_pass"] for v in per_case.values()) else "unstable",
            "repeats": len(runs), "cases": per_case, "accepted_runs": accepted,
            "usage": totals, "cost_per_accepted": totals["cost"] / accepted if accepted and totals["cost"] is not None else None,
            "authenticity": LIMIT}


def placeholder(value):
    return isinstance(value, str) and (value.lower().strip() in ("todo", "tbd", "placeholder", "unknown") or value.startswith("<"))


def has_placeholder(value):
    if isinstance(value, dict):
        return any(has_placeholder(v) for v in value.values())
    if isinstance(value, list):
        return any(has_placeholder(v) for v in value)
    return placeholder(value) or value == "0" * 64


def assessment(record):
    validate(record)
    result = {"status": "valid", "kind": record["kind"], "digest": digest(record), "authenticity": LIMIT}
    if record["kind"] == "delegation":
        missing = sorted(set(record["required_capabilities"]) - set(record["available_capabilities"]))
        result.update(ready=not missing, missing_capabilities=missing,
                      preferred_method="script" if record["pure_mechanics"] else record["method"])
        if record["pure_mechanics"] and record["method"] != "script":
            result["ready"] = False
            result["reason"] = "pure_mechanics_prefers_script"
    elif record["kind"] == "modernization":
        current = {c["id"]: c for c in record["parity_checks"]}
        result["ready"] = (set(current) == set(record["required_parity_ids"])
                           and all(passing(c, record["candidate_revision"]) for c in current.values())
                           and all(c["approved"] and c["evidence"] for c in record["checkpoints"])
                           and record["rollback_verified"]
                           and not has_placeholder(record))
    return result


def template(kind):
    """Synthetic examples are examples of shape, never evidence of execution."""
    need(kind in KINDS, "unknown template kind")
    base = {"version": 1, "kind": kind, "id": "synthetic-" + kind}
    check = {"id": "case-1", "status": "unknown", "executed": 0, "evidence": [], "revision": "synthetic-revision"}
    use = {k: None for k in METRICS}
    if kind == "task":
        base.update(outcome="Synthetic: implement the stated invariant", checks=[{"id": "case-1", "invariant": "Expected behavior holds", "mandatory": True}],
                    authority={"read_scope": ["src"], "write_scope": ["src"], "required_read_scope": ["src"], "required_write_scope": ["src"], "publication": False, "requires_publication": False},
                    budgets={"attempts": 5, "seconds": 3600, "tokens": None}, independent_review_required=True, checkpoints=["review-current-revision"])
    elif kind == "attempt":
        task = template("task")
        base.update(task_id=task["id"], task_digest=digest(task), sequence=1, previous_attempt_digest=None,
                    revision="synthetic-revision", author="synthetic-author", checks=[check], findings=[], remaining_delta=["case-1"], failure_fingerprints=[], usage=use, review=None)
    elif kind == "run":
        requested = {k: "host-selected-" + k for k in CONFIG}
        requested["tools"] = []
        base.update(source_revision="synthetic-revision", invocation_id="synthetic-invocation", trace_hash="0" * 64, live=False, cache_enabled=False,
                    requested=requested, observed={k: None for k in CONFIG}, source_hash="0" * 64, fixtures_hash="0" * 64,
                    artifacts={"synthetic-trace": "0" * 64}, cases=[check], usage=use)
    elif kind == "delegation":
        base.update(method="script", model="host-selected-model", effort="host-selected-effort", brief="Synthetic: inspect explicit input", scope=["src"],
                    budget={"seconds": 60, "tokens": None}, escalation="Stop on missing input or authority", pure_mechanics=True,
                    required_capabilities=["read-files"], available_capabilities=[])
    else:
        base.update(pilot="TODO", baseline_revision="TODO", candidate_revision="TODO", input_hash="0" * 64, baseline_evidence=["TODO"], approved_differences=[],
                    required_parity_ids=["case-1"], parity_checks=[check], rollback="TODO", rollback_verified=False,
                    checkpoints=[{"id": "pilot-review", "approved": False, "evidence": []}])
    return base


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise Invalid(message)


def load(path):
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, "duplicate JSON key: " + key)
            result[key] = value
        return result
    raw = sys.stdin.read() if path == "-" else Path(path).read_text(encoding="utf-8")
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=lambda v: (_ for _ in ()).throw(Invalid("nonfinite JSON number: " + v)))


def main(argv=None):
    try:
        parser = Parser(description=__doc__)
        sub = parser.add_subparsers(dest="command", required=True)
        p = sub.add_parser("template")
        p.add_argument("kind", choices=KINDS)
        p = sub.add_parser("validate")
        p.add_argument("record")
        p = sub.add_parser("next")
        p.add_argument("--task", required=True)
        p.add_argument("--history", required=True)
        p = sub.add_parser("stability")
        p.add_argument("--required", required=True)
        p.add_argument("--min-repeats", type=int, required=True)
        p.add_argument("runs", nargs="+")
        args = parser.parse_args(argv)
        paths = [getattr(args, k, None) for k in ("record", "task", "history", "required")] + getattr(args, "runs", [])
        need(paths.count("-") <= 1, "stdin '-' may be consumed only once")
        if args.command == "template":
            result = template(args.kind)
        elif args.command == "validate":
            result = assessment(load(args.record))
        elif args.command == "next":
            result = next_action(load(args.task), load(args.history))
        else:
            runs = []
            for path in args.runs:
                value = load(path)
                runs.extend(value if isinstance(value, list) else [value])
            result = stability(load(args.required), args.min_repeats, runs)
        print(json.dumps(result, sort_keys=True, indent=2, allow_nan=False))
        return 0
    except (Invalid, OSError, ValueError, UnicodeError) as exc:
        print(json.dumps({"status": "error", "error": str(exc), "authenticity": LIMIT}))
        return 2


if __name__ == "__main__":
    sys.exit(main())
