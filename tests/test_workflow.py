"""Portable workflow semantics; synthetic fixtures never invoke a host/model."""
import contextlib
import copy
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

CORE = Path(__file__).resolve().parents[1] / "skills/agent-engineering-kit/core"
spec = importlib.util.spec_from_file_location("aek_workflow", CORE / "workflow.py")
w = importlib.util.module_from_spec(spec)
spec.loader.exec_module(w)


class WorkflowTests(unittest.TestCase):
    def task(self):
        task = w.template("task")
        task["budgets"]["attempts"] = 8
        return task

    def attempt(self, task, history=None, passed=False):
        history = history or []
        a = w.template("attempt")
        a.update(id="attempt-%d" % (len(history) + 1), task_digest=w.task_digest(task),
                 task_id=task["id"], sequence=len(history) + 1,
                 previous_attempt_digest=w.digest(history[-1]) if history else None,
                 usage={"tokens": 10, "seconds": 2, "tool_calls": 1, "cost": .01})
        if passed:
            a["checks"][0].update(status="pass", executed=1, evidence=["synthetic-raw-result"])
            a["remaining_delta"] = []
            a["review"] = {"reviewer": "independent-test-reviewer", "independent": True,
                           "revision": a["revision"], "result": "pass", "evidence": ["synthetic-review"]}
        return a

    def make_run(self, index, passed=True):
        r = w.template("run")
        r.update(id="run-%d" % index, invocation_id="invocation-%d" % index,
                 trace_hash=w.digest(index), live=True, observed=copy.deepcopy(r["requested"]),
                 usage={"tokens": 10, "seconds": 2, "tool_calls": 1, "cost": .1})
        r["cases"][0].update(status="pass" if passed else "fail", executed=1, evidence=["synthetic-result"])
        return r

    def cli(self, args, stdin=""):
        stream = io.StringIO()
        with patch.object(sys, "stdin", io.StringIO(stdin)), contextlib.redirect_stdout(stream):
            code = w.main(args)
        return code, json.loads(stream.getvalue())

    def approval_files(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        spec_path = root / "spec.md"
        spec_path.write_bytes(b"# v1\nUse tabs.\n")
        plan_path = root / "plan.md"
        plan_path.write_bytes(b"# v1\nImplement the accepted output and verify it.\n")
        return root, spec_path, plan_path

    def gate(self, stage, spec_path, *, plan=None, approved_spec=None, approved_plan=None):
        args = ["gate", stage, "--spec", str(spec_path)]
        for option, value in (("--plan", plan), ("--approved-spec", approved_spec), ("--approved-plan", approved_plan)):
            if value is not None:
                args.extend((option, str(value)))
        return self.cli(args)

    def test_gate_requires_each_approval_and_is_read_only(self):
        root, spec_path, plan_path = self.approval_files()
        before = {path.name: path.read_bytes() for path in root.iterdir()}
        code, result = self.gate("plan", spec_path)
        self.assertEqual((code, result["status"]), (1, "awaiting_spec_approval"))
        spec_id = result["spec_id"]
        self.assertEqual(spec_id, hashlib.sha256(spec_path.read_bytes()).hexdigest())
        code, result = self.gate("plan", spec_path, approved_spec=spec_id)
        self.assertEqual((code, result["status"]), (0, "ready_to_plan"))
        code, result = self.gate("implement", spec_path, approved_spec=spec_id)
        self.assertEqual((code, result["status"]), (1, "awaiting_plan"))
        code, result = self.gate("implement", spec_path, plan=plan_path)
        self.assertEqual((code, result["status"]), (1, "awaiting_spec_approval"))
        self.assertIsNone(result.get("plan_id"))
        code, result = self.gate("implement", spec_path, plan=plan_path, approved_spec=spec_id)
        self.assertEqual((code, result["status"]), (1, "awaiting_plan_approval"))
        plan_id = result["plan_id"]
        self.assertRegex(plan_id, r"^[0-9a-f]{64}$")
        self.assertNotEqual(spec_id, plan_id)
        code, result = self.gate("implement", spec_path, plan=plan_path, approved_spec=spec_id, approved_plan=plan_id)
        self.assertEqual((code, result["status"]), (0, "ready_to_implement"))
        self.assertEqual((result["spec_id"], result["plan_id"]), (spec_id, plan_id))
        self.assertEqual({path.name: path.read_bytes() for path in root.iterdir()}, before)

    def test_gate_rejects_stale_swapped_and_other_spec_approvals(self):
        root, spec_path, plan_path = self.approval_files()
        code, spec_result = self.gate("plan", spec_path)
        self.assertEqual((code, spec_result["status"]), (1, "awaiting_spec_approval"))
        spec_id = spec_result["spec_id"]
        _, plan_result = self.gate("implement", spec_path, plan=plan_path, approved_spec=spec_id)
        plan_id = plan_result["plan_id"]
        for supplied_spec, supplied_plan, status in (
            (plan_id, spec_id, "awaiting_spec_approval"),
            (None, plan_id, "awaiting_spec_approval"),
            (spec_id, spec_id, "awaiting_plan_approval"),
        ):
            with self.subTest(approved_spec=supplied_spec, approved_plan=supplied_plan):
                code, result = self.gate("implement", spec_path, plan=plan_path,
                                         approved_spec=supplied_spec, approved_plan=supplied_plan)
                self.assertEqual((code, result["status"]), (1, status))

        progress = root / "tasks.md"
        progress.write_bytes(b"- [x] Verified actual output\n")
        code, result = self.gate("implement", spec_path, plan=plan_path, approved_spec=spec_id, approved_plan=plan_id)
        self.assertEqual((code, result["status"]), (0, "ready_to_implement"))
        self.assertEqual((result["spec_id"], result["plan_id"]), (spec_id, plan_id))

        plan_path.write_bytes(b"# v1\nImplement output, defer tests.\n")
        code, result = self.gate("implement", spec_path, plan=plan_path, approved_spec=spec_id, approved_plan=plan_id)
        self.assertEqual((code, result["status"]), (1, "awaiting_plan_approval"))
        self.assertNotEqual(plan_id, result["plan_id"])
        plan_path.write_bytes(b"# v1\nImplement the accepted output and verify it.\n")

        spec_path.write_bytes(b"# v1\nUse pipes.\n")
        code, result = self.gate("implement", spec_path, plan=plan_path, approved_spec=spec_id, approved_plan=plan_id)
        self.assertEqual((code, result["status"]), (1, "awaiting_spec_approval"))
        other_spec_id = result["spec_id"]
        self.assertNotEqual(spec_id, other_spec_id)
        code, result = self.gate("implement", spec_path, plan=plan_path, approved_spec=other_spec_id, approved_plan=plan_id)
        self.assertEqual((code, result["status"]), (1, "awaiting_plan_approval"))
        self.assertNotEqual(plan_id, result["plan_id"])

    def test_gate_rejects_invalid_input(self):
        root, spec_path, plan_path = self.approval_files()
        spec_id = hashlib.sha256(spec_path.read_bytes()).hexdigest()
        code, result = self.gate("plan", spec_path, approved_spec=spec_id)
        self.assertEqual((code, result["status"]), (0, "ready_to_plan"))
        for args in (
            ("gate", "plan"),
            ("gate", "plan", "--spec", str(root / "missing.md")),
            ("gate", "plan", "--spec", str(root)),
            ("gate", "plan", "--spec", str(spec_path), "--approved-spec", "bad"),
            ("gate", "implement", "--spec", str(spec_path), "--approved-spec", spec_id,
             "--plan", str(plan_path), "--approved-plan", "bad"),
            ("gate", "implement", "--spec", str(spec_path), "--approved-spec", spec_id,
             "--plan", str(root / "missing-plan.md")),
        ):
            with self.subTest(args=args):
                code, result = self.cli(list(args))
                self.assertEqual((code, result["status"]), (2, "error"))

    def test_templates_are_valid_but_not_observations(self):
        for kind in w.KINDS:
            self.assertEqual(w.validate(w.template(kind))["kind"], kind)
        self.assertFalse(w.assessment(w.template("modernization"))["ready"])
        self.assertFalse(w.assessment(w.template("delegation"))["ready"])
        with self.assertRaises(w.Invalid):
            w.stability(["case-1"], 1, [w.template("run")])

    def test_strict_types_nonfinite_and_duplicate_ids(self):
        for value in (True, 0, -1, float("inf"), float("nan")):
            task = self.task()
            task["budgets"]["attempts"] = value
            with self.assertRaises(w.Invalid):
                w.validate(task)
        for mutation in (lambda t: t.update(version=True),
                         lambda t: t["checks"].append(copy.deepcopy(t["checks"][0])),
                         lambda t: t["checks"][0].pop("id"),
                         lambda t: t.update(checks=[])):
            task = self.task()
            mutation(task)
            with self.assertRaises(w.Invalid):
                w.validate(task)

    def test_complete_requires_actual_current_checks_and_review(self):
        t = self.task()
        a = self.attempt(t, passed=True)
        self.assertEqual(w.next_action(t, [a])["action"], "complete")
        for mutate, expected in ((lambda x: x.update(review=None), "stop"),
                                 (lambda x: x["review"].update(reviewer=x["author"]), "stop"),
                                 (lambda x: x["review"].update(revision="old"), "stop"),
                                 (lambda x: x["checks"][0].update(revision="old"), "continue"),
                                 (lambda x: x["checks"][0].update(status="skip"), "continue"),
                                 (lambda x: x.update(checks=[]), "continue")):
            b = copy.deepcopy(a)
            mutate(b)
            self.assertEqual(w.next_action(t, [b])["action"], expected)
        a["checks"][0]["executed"] = 0
        with self.assertRaises(w.Invalid):
            w.next_action(t, [a])

    def test_material_findings_persist_across_retries(self):
        t = self.task()
        a = self.attempt(t)
        a["findings"] = [{"id": "bug", "severity": "high", "status": "open", "evidence": ["synthetic-result"]}]
        b = self.attempt(t, [a], passed=True)
        self.assertEqual(w.next_action(t, [a, b])["action"], "continue")
        b["findings"] = [dict(a["findings"][0], severity="low")]
        self.assertEqual(w.next_action(t, [a, b])["action"], "continue")
        b["findings"] = [dict(a["findings"][0], status="resolved")]
        self.assertEqual(w.next_action(t, [a, b])["action"], "complete")

    def test_history_binding_order_and_contract_changes(self):
        t = self.task()
        a = self.attempt(t)
        b = self.attempt(t, [a])
        for history in ([b, a], [a, a], [b]):
            with self.assertRaises(w.Invalid):
                w.next_action(t, history)
        b["previous_attempt_digest"] = "f" * 64
        with self.assertRaises(w.Invalid):
            w.next_action(t, [a, b])
        t["outcome"] += " changed"
        with self.assertRaises(w.Invalid):
            w.next_action(t, [a])

    def test_cumulative_budgets_include_failed_attempts(self):
        t = self.task()
        t["budgets"]["tokens"] = 20
        a = self.attempt(t)
        b = self.attempt(t, [a], passed=True)
        result = w.next_action(t, [a, b])
        self.assertEqual(result["usage"]["tokens"], 20)
        self.assertEqual(result["reasons"], ["budget_exhausted"])
        a["usage"]["tokens"] = None
        b = self.attempt(t, [a], passed=True)
        self.assertEqual(w.next_action(t, [a, b])["reasons"], ["unknown_token_usage_under_explicit_cap"])
        t = self.task()
        t["budgets"]["attempts"] = 1
        self.assertEqual(w.next_action(t, [self.attempt(t, passed=True)])["reasons"], ["budget_exhausted"])

    def test_authority_native_goals_and_no_progress(self):
        t = self.task()
        t["nativeGoals"] = {"requested": True}
        self.assertFalse(w.next_action(t, [])["native_goals_activated"])
        t["authority"]["requires_publication"] = True
        self.assertEqual(w.next_action(t, [])["reasons"], ["missing_authority"])
        t = self.task()
        a = self.attempt(t)
        a["failure_fingerprints"] = ["same-failure"]
        b = self.attempt(t, [a])
        b["failure_fingerprints"] = ["same-failure"]
        self.assertEqual(w.next_action(t, [a, b])["reasons"], ["unchanged_failure_fingerprints_without_progress"])
        a["remaining_delta"].append("another-delta")
        b["previous_attempt_digest"] = w.digest(a)
        self.assertEqual(w.next_action(t, [a, b])["action"], "continue")

    def test_stability_statistics_and_unknown_totals(self):
        runs = [self.make_run(1), self.make_run(2, False), self.make_run(3)]
        result = w.stability(["case-1"], 3, runs)
        self.assertEqual(result["status"], "unstable")
        self.assertEqual(result["cases"]["case-1"]["flips"], 2)
        self.assertEqual(result["cases"]["case-1"]["pass_rate"], 2 / 3)
        self.assertAlmostEqual(result["cost_per_accepted"], .15)
        self.assertEqual(result["usage"]["tokens"], 30)
        runs[0]["usage"]["cost"] = None
        runs[0]["usage"]["tokens"] = None
        result = w.stability(["case-1"], 3, runs)
        self.assertIsNone(result["cost_per_accepted"])
        self.assertIsNone(result["usage"]["tokens"])
        self.assertIsNone(w.stability(["case-1"], 1, [self.make_run(4, False)])["cost_per_accepted"])

    def test_stability_stale_revision_cannot_pass(self):
        run = self.make_run(1)
        run["cases"][0]["revision"] = "stale-revision"
        result = w.stability(["case-1"], 1, [run])
        self.assertEqual(result["status"], "unstable")
        self.assertEqual(result["accepted_runs"], 0)
        self.assertEqual(result["cases"]["case-1"]["pass_rate"], 0)
        self.assertIsNone(result["cost_per_accepted"])
        del run["source_revision"]
        with self.assertRaises(w.Invalid):
            w.validate(run)

    def test_stability_rejects_false_repeats_and_incomparable_runs(self):
        mutations = [lambda r: r.update(cache_enabled=True), lambda r: r.update(live=False),
                     lambda r: r.update(invocation_id="invocation-1"), lambda r: r.update(trace_hash=w.digest(1)),
                     lambda r: r["observed"].update(model=None), lambda r: r["observed"].update(effort="different"),
                     lambda r: r["observed"].update(version="different"), lambda r: r.update(source_hash="f" * 64),
                     lambda r: r.update(fixtures_hash="f" * 64), lambda r: r.update(source_revision="different"), lambda r: r["cases"][0].update(id="replacement")]
        for mutate in mutations:
            a, b = self.make_run(1), self.make_run(2)
            mutate(b)
            with self.assertRaises(w.Invalid):
                w.stability(["case-1"], 2, [a, b])
        for catalog in ([], ["case-1", "case-1"]):
            with self.assertRaises(w.Invalid):
                w.stability(catalog, 1, [self.make_run(1)])
        with self.assertRaises(w.Invalid):
            w.stability(["case-1"], 2, [self.make_run(1)])

    def test_delegation_capabilities_and_modernization_receipts(self):
        d = w.template("delegation")
        d["available_capabilities"] = d["required_capabilities"][:]
        self.assertTrue(w.assessment(d)["ready"])
        d["method"] = "agent"
        self.assertFalse(w.assessment(d)["ready"])
        m = w.template("modernization")
        m.update(pilot="synthetic component", baseline_revision="baseline-1", candidate_revision="synthetic-revision", input_hash=w.digest("synthetic-input"), rollback="restore baseline-1",
                 rollback_verified=True, baseline_evidence=["synthetic-baseline-result"])
        m["parity_checks"][0].update(status="pass", executed=1, evidence=["synthetic-parity-result"])
        m["checkpoints"][0].update(approved=True, evidence=["synthetic-review"])
        self.assertTrue(w.assessment(m)["ready"])
        for mutate in (lambda x: x.update(rollback="TODO"),
                       lambda x: x["checkpoints"][0].update(evidence=["TODO"]),
                       lambda x: x["parity_checks"][0].update(evidence=["TODO"]),
                       lambda x: x.update(input_hash="0" * 64),
                       lambda x: x["parity_checks"][0].update(revision="stale")):
            changed = copy.deepcopy(m)
            mutate(changed)
            self.assertFalse(w.assessment(changed)["ready"])

    def test_missing_nullable_attempt_fields_are_json_errors(self):
        t = self.task()
        for key in ("previous_attempt_digest", "review"):
            a = self.attempt(t)
            del a[key]
            with self.assertRaises(w.Invalid):
                w.next_action(t, [a])
            code, result = self.cli(["validate", "-"], json.dumps(a))
            self.assertEqual(code, 2)
            self.assertEqual(result["status"], "error")
            self.assertIn(key, result["error"])

    def test_cli_json_errors_and_stdin(self):
        code, result = self.cli(["validate", "-"], json.dumps(self.task()))
        self.assertEqual(code, 0)
        self.assertEqual(result["status"], "valid")
        for args, raw in ((["nonsense"], ""), (["validate", "-"], '{"version":1,"version":1}'),
                          (["validate", "-"], '{"version":NaN}'), (["validate", "-"], '[]'),
                          (["next", "--task", "-", "--history", "-"], "{}")):
            code, result = self.cli(args, raw)
            self.assertEqual(code, 2)
            self.assertEqual(result["status"], "error")


if __name__ == "__main__":
    unittest.main()
