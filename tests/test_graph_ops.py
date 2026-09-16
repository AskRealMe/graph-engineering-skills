"""Deterministic file/transition tests, not evidence of real subagent execution."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).parents[1] / "skills/graph-engineering/scripts/graph_ops.py"
module = importlib.util.spec_from_file_location("graph_ops", SCRIPT)
ops = importlib.util.module_from_spec(module)
module.loader.exec_module(ops)


def example():
    return {
        "format_version": 1, "id": "backend-development-graph", "name": "Backend development",
        "description": "Build backend features with analysis, implementation, tests, and review.",
        "entry": "analyze", "max_steps": 30, "routing": "exclusive",
        "state": {
            "goal": {"type": "string", "required": True},
            "service": {"type": "string", "required": True},
            "requirements": {"type": "string", "default": ""},
            "implemented": {"type": "boolean", "default": False},
            "tests_passed": {"type": "boolean", "default": False},
            "review_passed": {"type": "boolean", "default": False},
        },
        "nodes": [
            {"id": "analyze", "instructions": "Inspect requirements; return acceptance criteria.", "reads": ["goal", "service"], "writes": ["requirements"]},
            {"id": "implement", "instructions": "Implement the requested backend feature.", "reads": ["goal", "requirements", "service"], "writes": ["implemented"], "max_visits": 3, "max_attempts": 2},
            {"id": "test", "instructions": "Run real acceptance tests and report their result.", "reads": ["implemented", "requirements"], "writes": ["tests_passed"]},
            {"id": "review", "instructions": "Review implementation against requirements.", "reads": ["requirements", "tests_passed"], "writes": ["review_passed"]},
        ],
        "edges": [
            {"from": "analyze", "to": "implement"}, {"from": "implement", "to": "test"},
            {"from": "test", "to": "review", "when": {"field": "tests_passed", "op": "eq", "value": True}},
            {"from": "test", "to": "implement", "otherwise": True},
            {"from": "review", "to": "END", "when": {"all": [{"field": "tests_passed", "op": "eq", "value": True}, {"field": "review_passed", "op": "eq", "value": True}]}},
            {"from": "review", "to": "implement", "otherwise": True},
        ],
    }


class GraphTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.project = Path(self.temp.name) / "project with spaces"
        self.project.mkdir()
        (self.project / "AGENTS.md").write_text("# Existing guidance\nPreserve this.\n")
        self.spec = example()
        self.specfile = Path(self.temp.name) / "draft.json"
        self.write_spec()
        self.graph = self.project / ".agents/skills/backend-development-graph"
        self.call("create", project=True, spec=str(self.specfile))

    def tearDown(self):
        self.temp.cleanup()

    def write_spec(self):
        self.specfile.write_text(json.dumps(self.spec))

    def call(self, command, project=False, **kwargs):
        args = [command]
        if command not in {"connect", "disconnect", "doctor", "list", "create"}:
            args += ["--graph", str(self.graph)]
        if project: args += ["--project", str(self.project)]
        for k, v in kwargs.items():
            args += ["--" + k.replace("_", "-")]
            if v is not True: args += [str(v)]
        return ops.main(args)

    def jsonfile(self, value, name="input.json"):
        p = Path(self.temp.name) / name
        p.write_text(json.dumps(value))
        return str(p)

    def start(self):
        return self.call("start", project=True, goal="Build a task API", input=self.jsonfile({"service": "tasks"}))

    def finish(self, patch=None, status="success", summary="Synthetic unit-test result", artifacts=None):
        handoff = self.call("prepare")
        self.call("bind", agent_id="unit-test-handle-not-real")
        result = {"attempt_id": handoff["attempt_id"], "status": status, "summary": summary, "patch": patch or {}, "artifacts": artifacts or []}
        return self.call("finish", result=self.jsonfile(result, "result.json"))

    def reach_test(self):
        self.start()
        self.finish({"requirements": "GET /health returns status ok"})
        return self.finish({"implemented": True})

    def complete(self):
        self.reach_test()
        self.finish({"tests_passed": True})
        return self.finish({"review_passed": True})

    def test_create_discovery_portability_and_registration(self):
        self.assertTrue(self.call("validate")["valid"])
        self.assertEqual(len(self.call("list", project=True)), 1)
        for path in ["SKILL.md", "STATE.md", "GRAPH.md", "graph.json", "nodes/analyze/SKILL.md", "scripts/graph_ops.py", "references/execution.md", "assets/graph-skill.md"]:
            self.assertTrue((self.graph / path).is_file(), path)
        self.assertIn("backend-development-graph", (self.graph / "SKILL.md").read_text())
        text = (self.project / "AGENTS.md").read_text()
        self.call("connect", project=True)
        self.assertEqual(text, (self.project / "AGENTS.md").read_text())
        self.call("disconnect", project=True)
        self.assertIn("Preserve this.", (self.project / "AGENTS.md").read_text())
        self.assertTrue(self.graph.exists())
        self.assertFalse(self.call("doctor", project=True)["registered"])

    def test_reject_invalid_graph_before_creation(self):
        bad = example()
        for mutate in [lambda s: s.update(entry="missing"), lambda s: s["edges"].append({"from": "test", "to": "missing"}), lambda s: s["nodes"][0].update(reads=["missing"]), lambda s: s["edges"][2]["when"].update(op="execute"), lambda s: s.update(max_steps=0)]:
            bad = example()
            mutate(bad)
            with self.assertRaises(ops.Invalid): ops.validate(bad, self.graph)
        with self.assertRaises(ops.Invalid): self.call("create", project=True, spec=str(self.specfile))

    def test_preview_edit_and_mermaid_sync(self):
        before = (self.graph / "graph.json").read_text()
        self.spec["name"] = "API engineering"
        self.spec["nodes"][3]["name"] = 'Quality "review"'
        self.write_spec()
        self.assertIn("API engineering", self.call("diff", spec=str(self.specfile))["diff"])
        self.assertEqual(before, (self.graph / "graph.json").read_text())
        self.call("apply", spec=str(self.specfile))
        self.assertIn("API engineering", (self.graph / "SKILL.md").read_text())
        self.assertIn("&quot;review&quot;", (self.graph / "GRAPH.md").read_text())
        self.assertTrue((self.graph / "GRAPH.md").read_text().startswith("```mermaid\n"))

    def test_missing_inputs_and_one_active_run(self):
        with self.assertRaisesRegex(ops.Invalid, "service"):
            self.call("start", goal="Build API")
        self.start()
        with self.assertRaisesRegex(ops.Invalid, "active run"): self.start()
        self.call("cancel")
        second = self.start()
        self.assertEqual(second["values"]["requirements"], "")
        self.assertEqual(len(self.call("history")), 2)

    def test_removing_node_archives_owned_skill_and_keeps_run_snapshot(self):
        run = self.start()
        self.call("pause")
        old = (self.graph / "nodes/review/SKILL.md").read_text()
        self.spec["nodes"] = [n for n in self.spec["nodes"] if n["id"] != "review"]
        self.spec["edges"] = [e for e in self.spec["edges"] if e["from"] != "review"]
        for edge in self.spec["edges"]:
            if edge["to"] == "review": edge["to"] = "END"
        self.write_spec()
        self.call("apply", spec=str(self.specfile))
        self.assertFalse((self.graph / "nodes/review").exists())
        archived = list((self.graph / ".authoring-history").glob("*/review/SKILL.md"))
        self.assertEqual(archived[0].read_text(), old)
        self.assertEqual((self.graph / "runs" / run["id"] / "skills/review/SKILL.md").read_text(), old)

    def test_optional_defaults_are_visible_separately_from_required_inputs(self):
        self.spec["state"]["language"] = {"type": "string", "default": "English", "enum": ["English", "Korean"]}
        self.write_spec()
        self.call("apply", spec=str(self.specfile))
        text = (self.graph / "SKILL.md").read_text()
        inputs, state = text.split("## Inputs", 1)[1].split("## Shared state", 1)
        self.assertIn("`goal`", inputs)
        self.assertNotIn("tests_passed", inputs)
        self.assertIn('`language` (string); default: `"English"`', state)
        self.assertIn("Korean", state)

    def test_latest_run_uses_creation_time_not_random_identifier(self):
        first = self.start()
        self.call("cancel")
        second = self.start()
        self.call("cancel")
        runs = self.graph / "runs"
        old_dir, new_dir = runs / first["id"], runs / second["id"]
        old = ops.load(old_dir / "state.json")
        new = ops.load(new_dir / "state.json")
        old.update(id="20260101T000000-zzzz", created_at="2026-01-01T00:00:00.100000+00:00")
        new.update(id="20260101T000000-aaaa", created_at="2026-01-01T00:00:00.200000+00:00")
        ops.save(old_dir / "state.json", old)
        ops.save(new_dir / "state.json", new)
        old_dir.rename(runs / old["id"])
        new_dir.rename(runs / new["id"])
        self.assertEqual(self.call("status")["id"], new["id"])
        self.assertEqual([r["id"] for r in self.call("history")], [old["id"], new["id"]])

    def test_real_handle_required_and_stale_results_rejected(self):
        self.start()
        handoff = self.call("prepare")
        self.assertTrue(Path(handoff["skill"]).exists())
        result = {"attempt_id": handoff["attempt_id"], "status": "success", "summary": "Unit test", "patch": {"requirements": "one"}, "artifacts": []}
        with self.assertRaisesRegex(ops.Invalid, "Bind"):
            self.call("finish", result=self.jsonfile(result))
        self.call("bind", agent_id="unit-test-handle")
        result["attempt_id"] = "wrong"
        with self.assertRaisesRegex(ops.Invalid, "stale"):
            self.call("finish", result=self.jsonfile(result))
        result["attempt_id"] = handoff["attempt_id"]
        self.call("finish", result=self.jsonfile(result))
        with self.assertRaises(ops.Invalid): self.call("finish", result=self.jsonfile(result))

    def test_wrong_patch_type_scope_and_nonexistent_artifact(self):
        self.start()
        handoff = self.call("prepare")
        self.call("bind", agent_id="unit-test")
        for patch, paths in [({"requirements": False}, []), ({"goal": "changed"}, []), ({"requirements": "ok"}, ["missing-proof.log"])]:
            result = {"attempt_id": handoff["attempt_id"], "status": "success", "summary": "Unit test", "patch": patch, "artifacts": paths}
            with self.assertRaises(ops.Invalid): self.call("finish", result=self.jsonfile(result))
        self.assertEqual(self.call("status")["values"]["requirements"], "")

    def test_branch_loop_and_trace(self):
        self.reach_test()
        failed_test = self.finish({"tests_passed": False})
        self.assertEqual(failed_test["current"], "implement")
        self.assertEqual(failed_test["status"], "running")
        decision = [e for e in failed_test["events"] if e["kind"] == "routed"][-1]
        self.assertEqual(decision["state"]["tests_passed"], False)
        self.finish({"implemented": True})
        self.finish({"tests_passed": True})
        completed = self.finish({"review_passed": True})
        self.assertEqual(completed["status"], "completed")
        self.assertEqual(completed["current"], "END")
        self.assertIn("completed", (self.graph / "STATE.md").read_text())

    def test_route_dry_run_missing_ambiguous_and_priority(self):
        original = (self.graph / "STATE.md").read_text()
        answer = self.call("route", node="test", input=self.jsonfile({"tests_passed": False}))
        self.assertEqual(answer["to"], "implement")
        self.assertEqual(original, (self.graph / "STATE.md").read_text())
        spec = example()
        spec["edges"].append({"from": "test", "to": "END"})
        with self.assertRaisesRegex(ops.Invalid, "Multiple"):
            ops.route(spec, "test", {"tests_passed": True})
        spec["routing"] = "first-match"
        self.assertEqual(ops.route(spec, "test", {"tests_passed": True})["to"], "review")
        spec["edges"] = [e for e in example()["edges"] if not e.get("otherwise")]
        with self.assertRaisesRegex(ops.Invalid, "No route"):
            ops.route(spec, "test", {"tests_passed": False})

    def test_pause_during_inflight_then_fresh_read_resume(self):
        self.start()
        handoff = self.call("prepare")
        self.call("bind", agent_id="unit-test")
        self.call("pause")
        result = {"attempt_id": handoff["attempt_id"], "status": "success", "summary": "Unit test", "patch": {"requirements": "API"}, "artifacts": []}
        state = self.call("finish", result=self.jsonfile(result))
        self.assertEqual(state["status"], "paused")
        self.assertEqual(state["current"], "implement")
        # Every command reloads the serialized run, including a fresh process equivalent.
        self.assertEqual(self.call("resume")["status"], "running")
        self.assertEqual(self.call("prepare")["input"]["requirements"], "API")

    def test_stop_requires_settlement_and_preserves_effects(self):
        self.start()
        handoff = self.call("prepare")
        self.call("bind", agent_id="unit-test")
        actual = self.project / "partial.txt"
        actual.write_text("already changed")
        self.assertEqual(self.call("cancel")["status"], "stopping")
        with self.assertRaises(ops.Invalid): self.call("settle")
        stopped = self.call("settle", note="Unit-test terminal handle evidence")
        self.assertEqual(stopped["status"], "cancelled")
        self.assertTrue(actual.exists())
        with self.assertRaises(ops.Invalid): self.call("resume")
        self.call("recover", decision="retry", note="Inspected partial output; retry explicitly requested")
        retry = self.call("prepare")
        self.assertNotEqual(handoff["attempt_id"], retry["attempt_id"])

    def test_errors_retry_then_exhaust_and_manual_retry(self):
        self.start()
        self.finish({"requirements": "API"})
        first = self.finish(status="error")
        self.assertEqual(first["status"], "running")
        second = self.finish(status="error")
        self.assertEqual(second["status"], "failed")
        self.assertFalse(second["values"]["implemented"])
        self.call("retry", note="User requests one new retry budget")
        self.assertEqual(self.finish({"implemented": True})["current"], "test")

    def test_recovery_cannot_replay_a_committed_attempt(self):
        self.start()
        finished = self.finish({"requirements": "Already applied"})
        result = finished["attempts"][-1]["result"]
        with self.assertRaisesRegex(ops.Invalid, "already committed"):
            self.call("recover", decision="accept", note="Inspected result", result=self.jsonfile(result))
        self.call("cancel")
        with self.assertRaisesRegex(ops.Invalid, "already committed"):
            self.call("recover", decision="retry", note="Inspected result")
        self.assertEqual(self.call("status")["values"]["requirements"], "Already applied")

    def test_recovery_can_accept_a_result_retained_during_stop(self):
        self.start()
        handoff = self.call("prepare")
        self.call("bind", agent_id="unit-test-handle")
        self.call("cancel")
        result = {"attempt_id": handoff["attempt_id"], "status": "success", "summary": "Synthetic retained result", "patch": {"requirements": "Checked output"}, "artifacts": []}
        file = self.jsonfile(result)
        stopped = self.call("finish", result=file)
        self.assertEqual(stopped["values"]["requirements"], "")
        accepted = self.call("recover", decision="accept", note="Terminal handle and output inspected", result=file)
        self.assertEqual(accepted["values"]["requirements"], "Checked output")
        self.assertEqual(accepted["current"], "implement")

    def test_loop_limit_is_not_an_implicit_success(self):
        self.reach_test()
        self.finish({"tests_passed": False})
        for _ in range(2):
            self.finish({"implemented": True})
            self.finish({"tests_passed": False})
        self.assertEqual(self.call("prepare")["status"], "blocked")
        self.assertEqual(self.call("status")["visits"]["implement"], 3)

    def test_gate_needs_actual_response(self):
        self.spec["nodes"][0]["approval"] = "May I inspect the application?"
        self.write_spec()
        self.call("apply", spec=str(self.specfile))
        self.start()
        self.assertEqual(self.call("prepare")["status"], "awaiting_input")
        with self.assertRaises(ops.Invalid): self.call("respond", decision="approve")
        self.call("respond", decision="decline", note="User says wait")
        self.call("resume")
        self.assertEqual(self.call("prepare")["status"], "awaiting_input")
        self.call("respond", decision="approve", note="User explicitly approved")
        self.assertIn("attempt_id", self.call("prepare"))

    def test_snapshot_preserved_when_authoring_changes(self):
        started = self.start()
        path = self.graph / "runs" / started["id"] / "skills/analyze/SKILL.md"
        old = path.read_text()
        self.spec["nodes"][0]["instructions"] = "Changed instructions for future runs"
        self.write_spec()
        self.call("apply", spec=str(self.specfile))
        self.assertEqual(path.read_text(), old)
        self.assertEqual(self.call("status")["version"], started["version"])
        self.assertNotEqual(ops.digest(ops.load(self.graph / "graph.json")), started["version"])

    def test_rerun_restores_inputs_invalidates_outputs_preserves_history(self):
        self.complete()
        rerun = self.call("rerun", node="test", note="User asks to repeat tests")
        self.assertEqual(rerun["status"], "paused")
        self.assertFalse(rerun["values"]["tests_passed"])
        self.assertFalse(rerun["attempts"][2]["valid"])
        self.assertFalse(rerun["attempts"][3]["valid"])
        self.assertEqual(len(rerun["attempts"]), 4)
        self.call("resume")
        self.finish({"tests_passed": True})
        self.assertEqual(self.finish({"review_passed": True})["status"], "completed")

    def test_state_change_requires_recomputing_affected_nodes(self):
        self.reach_test()
        self.call("pause")
        changed = self.call("set-state", input=self.jsonfile({"service": "billing"}), note="User changed target")
        self.assertIn("analyze", changed["stale_nodes"])
        with self.assertRaises(ops.Invalid): self.call("resume")
        rerun = self.call("rerun", node="analyze", note="Refresh requirements for changed service")
        self.assertEqual(rerun["values"]["service"], "billing")
        self.call("resume")
        self.assertEqual(self.call("prepare")["input"]["service"], "billing")

    def test_trial_and_clone_have_independent_states(self):
        completed = self.complete()
        trial = self.call("trial", project=True, node="review", goal="Review node test", input=self.jsonfile({"service": "tasks", "requirements": "test", "tests_passed": True}))
        self.assertNotEqual(trial["id"], completed["id"])
        self.assertEqual(self.finish({"review_passed": False})["status"], "completed")
        clone = self.call("clone", project=True, id="frontend-development-graph", name="Frontend")
        self.assertFalse(list((Path(clone["graph"]) / "runs").glob("*/state.json")))
        self.assertEqual(len(self.call("list", project=True)), 2)

    def test_shared_and_copied_skill_resources(self):
        source = self.project / "existing-review"
        source.mkdir()
        (source / "SKILL.md").write_text('---\nname: existing-review\ndescription: Review backend code.\n---\nRead references/policy.md.\n')
        (source / "references").mkdir()
        (source / "references/policy.md").write_text("Look for actual bugs.")
        node = self.spec["nodes"][3]
        del node["instructions"]
        node.update(skill=str(source / "SKILL.md"), skill_mode="shared")
        self.write_spec()
        self.call("apply", spec=str(self.specfile))
        self.start()
        run = self.call("status")
        snapshot = self.graph / "runs" / run["id"] / "skills/review/references/policy.md"
        self.assertEqual(snapshot.read_text(), "Look for actual bugs.")
        (source / "references/policy.md").write_text("New policy")
        self.assertEqual(snapshot.read_text(), "Look for actual bugs.")
        self.call("cancel")
        # A graph-local copy is created at a new node ID to avoid overwriting existing work.
        node.update(id="local-review", skill_mode="copy")
        for edge in self.spec["edges"]:
            if edge["from"] == "review": edge["from"] = "local-review"
            if edge["to"] == "review": edge["to"] = "local-review"
        self.write_spec()
        self.call("apply", spec=str(self.specfile))
        self.assertEqual((self.graph / "nodes/local-review/references/policy.md").read_text(), "New policy")

    def test_delete_archives_history_and_refuses_active(self):
        self.start()
        with self.assertRaises(ops.Invalid): self.call("delete")
        self.call("cancel")
        preview = self.call("delete", dry_run=True)
        self.assertTrue(self.graph.exists())
        archive = Path(self.call("delete")["archive"])
        self.assertFalse(self.graph.exists())
        self.assertTrue((archive / "graph.json").exists())
        self.assertEqual(len(list((archive / "runs").glob("*/state.json"))), 1)

    def test_migration_checks_and_replaces_skill_snapshot(self):
        self.start()
        self.call("pause")
        self.spec["nodes"][0]["instructions"] = "New requested analysis"
        self.write_spec()
        self.call("apply", spec=str(self.specfile))
        self.assertTrue(self.call("migrate", dry_run=True)["compatible"])
        self.call("migrate", note="User explicitly wants new instructions")
        self.call("resume")
        handoff = self.call("prepare")
        self.assertIn("New requested analysis", Path(handoff["skill"]).read_text())

    def test_old_execution_cannot_overlap_new_active_run(self):
        completed = self.complete()
        self.start()
        with self.assertRaisesRegex(ops.Invalid, "Another execution"):
            self.call("rerun", run=completed["id"], node="review", note="Repeat review")

    def test_state_change_cannot_skip_stale_upstream_results(self):
        self.reach_test()
        self.call("pause")
        self.call("set-state", input=self.jsonfile({"service": "billing"}), note="Change target")
        with self.assertRaisesRegex(ops.Invalid, "earliest affected"):
            self.call("rerun", node="implement", note="Skip analysis")

    def test_atomic_create_does_not_leave_a_broken_skill(self):
        source = self.project / "unsafe-source"
        source.mkdir()
        (source / "SKILL.md").write_text("---\nname: unsafe-source\ndescription: Fixture\n---\n")
        (source / "link").symlink_to(self.project / "AGENTS.md")
        spec = example()
        spec["id"] = "cannot-create"
        node = spec["nodes"][0]
        del node["instructions"]
        node.update(skill=str(source / "SKILL.md"), skill_mode="copy")
        with self.assertRaisesRegex(ops.Invalid, "symlink"):
            self.call("create", project=True, spec=self.jsonfile(spec))
        self.assertFalse((self.project / ".agents/skills/cannot-create").exists())

    def test_migration_handoff_is_persisted_consistently(self):
        self.start()
        self.call("pause")
        self.spec["nodes"][0]["instructions"] = "Updated analysis"
        self.write_spec()
        self.call("apply", spec=str(self.specfile))
        self.call("migrate", note="Requested migration")
        self.call("resume")
        handoff = self.call("prepare")
        saved = ops.load(self.graph / "runs" / handoff["run"] / "handoffs" / (handoff["attempt_id"] + ".json"))
        self.assertEqual(saved, handoff)

    def test_same_node_can_switch_to_local_copy_without_losing_old_files(self):
        source = self.project / "shared-review"
        source.mkdir()
        (source / "SKILL.md").write_text("---\nname: shared-review\ndescription: Review behavior.\n---\nInspect bugs.\n")
        old = (self.graph / "nodes/review/SKILL.md").read_text()
        node = self.spec["nodes"][3]
        del node["instructions"]
        node.update(skill=str(source / "SKILL.md"), skill_mode="copy")
        self.write_spec()
        self.call("apply", spec=str(self.specfile))
        copied = (self.graph / "nodes/review/SKILL.md").read_text()
        self.assertIn("name: review", copied)
        self.assertIn("Inspect bugs.", copied)
        backups = list((self.graph / ".authoring-history").glob("*/review/SKILL.md"))
        self.assertEqual(backups[0].read_text(), old)
        self.assertIn("name: shared-review", (source / "SKILL.md").read_text())

    def test_relative_reference_survives_staged_creation(self):
        source = self.project / ".agents/skills/shared"
        source.mkdir()
        (source / "SKILL.md").write_text("---\nname: shared\ndescription: Review.\n---\nInspect.\n")
        spec = example()
        spec["id"] = "relative-reference"
        node = spec["nodes"][3]
        del node["instructions"]
        node.update(skill="../shared/SKILL.md", skill_mode="shared")
        result = self.call("create", project=True, spec=self.jsonfile(spec))
        self.assertTrue((Path(result["graph"]) / "SKILL.md").exists())


if __name__ == "__main__":
    unittest.main()
