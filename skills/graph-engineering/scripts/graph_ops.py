#!/usr/bin/env python3
"""File helpers for the Graph Engineering skill. No model calls or agent runtime."""
from __future__ import annotations

import argparse
import contextlib
import copy
import difflib
import fcntl
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
from datetime import datetime, timezone
import uuid

BUNDLE = Path(__file__).resolve().parents[1]
BEGIN = "<!-- graph-engineering:start -->"
END = "<!-- graph-engineering:end -->"
ACTIVE = {"running", "paused", "awaiting_input", "blocked", "failed", "stopping"}
ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
TYPES = {"string": str, "boolean": bool, "integer": int, "number": (int, float), "array": list, "object": dict}


class Invalid(ValueError):
    pass


def require(ok, message):
    if not ok:
        raise Invalid(message)


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load(path):
    return json.loads(Path(path).read_text())


def data(path):
    return json.load(sys.stdin) if path == "-" else load(path)


def atomic(path, content):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix=".writing-", dir=path.parent)
    try:
        with os.fdopen(fd, "w") as out:
            out.write(content)
            out.flush()
            os.fsync(out.fileno())
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def save(path, value):
    atomic(path, json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


@contextlib.contextmanager
def lock(directory):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / ".graph.lock").open("a+") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        yield


def slug(value):
    return isinstance(value, str) and len(value) <= 64 and bool(ID.fullmatch(value))


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]


def typed(value, rule):
    kind = rule["type"]
    if kind in {"integer", "number"} and isinstance(value, bool):
        return False
    if kind == "number" and isinstance(value, (int, float)) and not math.isfinite(value):
        return False
    return isinstance(value, TYPES[kind]) and ("enum" not in rule or value in rule["enum"])


def check_values(spec, values, *, partial=False, allowed=None):
    require(isinstance(values, dict), "State/input/patch must be an object")
    for key, value in values.items():
        require(key in spec["state"], f"Unknown state field: {key}")
        require(allowed is None or key in allowed, f"Node cannot write field: {key}")
        require(typed(value, spec["state"][key]), f"Invalid value for {key}: expected {spec['state'][key]}")
    if not partial:
        missing = [k for k, r in spec["state"].items() if r.get("required") and k not in values]
        require(not missing, f"Missing required inputs: {', '.join(missing)}")


def check_condition(expr, state):
    require(isinstance(expr, dict), "Condition must be an object")
    if "all" in expr or "any" in expr:
        key = "all" if "all" in expr else "any"
        require(set(expr) == {key} and isinstance(expr[key], list) and expr[key], "Condition group needs a non-empty list")
        for item in expr[key]:
            check_condition(item, state)
    elif "not" in expr:
        require(set(expr) == {"not"}, "Invalid not condition")
        check_condition(expr["not"], state)
    else:
        require(expr.get("field") in state, f"Unknown condition field: {expr.get('field')}")
        op = expr.get("op", "eq")
        require(op in {"eq", "ne", "gt", "gte", "lt", "lte", "in", "contains", "exists"}, f"Unknown operator: {op}")
        require(op == "exists" or "value" in expr, "Condition needs value")
        if op in {"eq", "ne", "gt", "gte", "lt", "lte"}:
            require(typed(expr["value"], state[expr["field"]]), "Condition value has wrong type")
        if op in {"gt", "gte", "lt", "lte"}:
            require(state[expr["field"]]["type"] in {"number", "integer", "string"}, "Unordered field in comparison")
        if op == "in":
            require(isinstance(expr["value"], list), "in requires a list")
        if op == "contains":
            require(state[expr["field"]]["type"] in {"array", "object", "string"}, "contains needs collection field")


def matches(expr, values):
    if "all" in expr:
        return all(matches(x, values) for x in expr["all"])
    if "any" in expr:
        return any(matches(x, values) for x in expr["any"])
    if "not" in expr:
        return not matches(expr["not"], values)
    key, op = expr["field"], expr.get("op", "eq")
    if op == "exists":
        return (key in values) == expr.get("value", True)
    require(key in values, f"Routing needs state field: {key}")
    a, b = values[key], expr["value"]
    try:
        if op == "eq": return a == b and isinstance(a, bool) == isinstance(b, bool)
        if op == "ne": return not (a == b and isinstance(a, bool) == isinstance(b, bool))
        if op == "gt": return a > b
        if op == "gte": return a >= b
        if op == "lt": return a < b
        if op == "lte": return a <= b
        if op == "in": return a in b
        if op == "contains": return b in a
    except (TypeError, ValueError) as exc:
        raise Invalid(f"Cannot evaluate {expr}: {exc}") from exc
    raise Invalid(f"Unknown condition: {expr}")


def resolve_skill(root, node):
    path = Path(node.get("skill", f"nodes/{node['id']}/SKILL.md"))
    return (path if path.is_absolute() else root / path).resolve()


def validate(spec, root):
    require(isinstance(spec, dict), "Graph must be an object")
    for key in ("format_version", "id", "name", "description", "entry", "state", "nodes", "edges"):
        require(key in spec, f"Missing graph field: {key}")
    require(spec["format_version"] == 1, "Unsupported graph format_version")
    require(slug(spec["id"]), "Invalid graph id")
    require(isinstance(spec["name"], str) and spec["name"].strip(), "Graph needs name")
    require(isinstance(spec["description"], str) and 0 < len(spec["description"]) <= 1024, "Description must contain 1..1024 characters")
    require(spec.get("routing", "exclusive") in {"exclusive", "first-match"}, "Unknown routing policy")
    require(type(spec.get("max_steps", 50)) is int and spec.get("max_steps", 50) > 0, "max_steps must be positive")
    require(isinstance(spec["state"], dict), "state must be an object")
    require(spec["state"].get("goal", {}).get("type") == "string" and spec["state"]["goal"].get("required"), "State needs required string goal")
    for key, rule in spec["state"].items():
        require(isinstance(rule, dict) and rule.get("type") in TYPES, f"Invalid schema for {key}")
        if "enum" in rule:
            require(isinstance(rule["enum"], list) and rule["enum"], f"Empty enum: {key}")
        if "default" in rule:
            require(typed(rule["default"], rule), f"Invalid default: {key}")
    require(isinstance(spec["nodes"], list) and spec["nodes"], "Graph needs nodes")
    ids = [n.get("id") for n in spec["nodes"]]
    require(all(slug(x) for x in ids) and len(set(ids)) == len(ids), "Node IDs must be unique valid slugs")
    require(spec["entry"] in ids, "Entry node does not exist")
    for node in spec["nodes"]:
        for key in ("reads", "writes"):
            require(isinstance(node.get(key), list) and all(k in spec["state"] for k in node[key]), f"{node['id']}: invalid {key}")
        require(isinstance(node.get("agent", {}), dict), "agent must be an object")
        require(set(node.get("agent", {})) <= {"type", "model", "reasoning_effort"}, "Unknown agent setting")
        for key, default in (("max_attempts", 1), ("max_visits", 10)):
            require(type(node.get(key, default)) is int and node.get(key, default) > 0, f"Invalid {key}")
        require("approval" not in node or isinstance(node["approval"], str) and node["approval"].strip(), "approval must be a question")
        if "instructions" in node:
            require(isinstance(node["instructions"], str) and node["instructions"].strip(), f"Empty instructions: {node['id']}")
        else:
            require(node.get("skill_mode") in {"shared", "copy"}, "Referenced skill needs skill_mode shared|copy")
            require(resolve_skill(root, node).is_file(), f"Missing skill: {resolve_skill(root, node)}")
    require(isinstance(spec["edges"], list), "edges must be a list")
    outgoing = {node: [] for node in ids}
    for edge in spec["edges"]:
        require(edge.get("from") in ids and edge.get("to") in ids + ["END"], f"Dangling edge: {edge}")
        require(not (edge.get("otherwise") and "when" in edge), "Fallback cannot have a condition")
        if "when" in edge:
            check_condition(edge["when"], spec["state"])
        outgoing[edge["from"]].append(edge)
    for name, edges in outgoing.items():
        require(edges, f"No outgoing edge: {name}")
        require(sum(bool(e.get("otherwise")) for e in edges) <= 1, f"Multiple fallbacks: {name}")
    def reach(start, reverse=False):
        seen, queue = set(), [start]
        while queue:
            current = queue.pop()
            if current in seen: continue
            seen.add(current)
            queue.extend(e["from"] if reverse else e["to"] for e in spec["edges"] if e["to" if reverse else "from"] == current)
        return seen
    require(set(ids) <= reach(spec["entry"]), "Graph contains unreachable nodes")
    require(set(ids) <= reach("END", True), "A node has no possible path to END")
    return {"valid": True, "nodes": len(ids), "version": digest(spec)}


def route(spec, node, values):
    require(node in [n["id"] for n in spec["nodes"]], f"Unknown node: {node}")
    check_values(spec, values, partial=True)
    evaluated, hits, fallback = [], [], []
    for edge in spec["edges"]:
        if edge["from"] != node: continue
        if edge.get("otherwise"):
            fallback.append(edge)
            continue
        yes = "when" not in edge or matches(edge["when"], values)
        evaluated.append({"edge": edge, "matched": yes})
        if yes: hits.append(edge)
    hits = hits or fallback
    require(hits, f"No route matched from {node}; ask for clarification")
    require(len(hits) == 1 or spec.get("routing") == "first-match", f"Multiple routes matched from {node}; ask for clarification")
    return {"from": node, "to": hits[0]["to"], "selected": hits[0], "evaluated": evaluated, "state": copy.deepcopy(values)}


def project_of(graph):
    require(graph.parent.name == "skills" and graph.parent.parent.name == ".agents", "Expected project/.agents/skills/graph-id")
    return graph.parent.parent.parent


def connect(project, remove=False):
    project = Path(project).resolve()
    project.mkdir(parents=True, exist_ok=True)
    with lock(project / ".graph-engineering"):
        path = project / "AGENTS.md"
        text = path.read_text() if path.exists() else ""
        require(text.count(BEGIN) == text.count(END) <= 1, "Malformed Graph Engineering registration; preserve and repair manually")
        if BEGIN in text:
            before, rest = text.split(BEGIN, 1)
            _, after = rest.split(END, 1)
            text = before + after
        if not remove:
            block = f"{BEGIN}\n## Graph Engineering\n\nUse `$graph-engineering` to create or edit graph workflow skills through natural-language requests. Generated graphs are stored in `.agents/skills/<graph-id>/`. Read a generated graph's `SKILL.md` to execute or resume it. Each work node must run in a native Codex subagent; the parent commits validated state. Preserve run snapshots and inspect evidence before retrying interrupted work.\n{END}\n"
            text = text.rstrip() + ("\n\n" if text.strip() else "") + block
        atomic(path, text)
    return {"project": str(project), "connected": not remove}


def copy_skill(source, target):
    source, target = Path(source).resolve(), Path(target)
    require(source.is_dir(), f"Missing skill directory: {source}")
    ignore = {"runs", ".git", ".graph.lock", ".authoring-history", "__pycache__", ".DS_Store"}
    for item in source.rglob("*"):
        rel = item.relative_to(source)
        if any(x in ignore for x in rel.parts): continue
        require(not item.is_symlink(), f"Cannot snapshot symlink resource without inspection: {item}")
        if item.is_file():
            dest = target / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, dest)


def mermaid(spec):
    def label(text):
        return str(text).replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;").replace("|", "&#124;").replace("\n", " ")
    def condition(expr):
        for key in ("all", "any"):
            if key in expr:
                return "(" + (" and " if key == "all" else " or ").join(condition(x) for x in expr[key]) + ")"
        if "not" in expr: return "not " + condition(expr["not"])
        op = {"eq": "=", "ne": "!=", "gt": ">", "gte": ">=", "lt": "<", "lte": "<="}.get(expr.get("op", "eq"), expr.get("op", "eq"))
        return f"{expr['field']} {op} {json.dumps(expr.get('value', True), ensure_ascii=False)}"
    ids = {n["id"]: f"n{i}" for i, n in enumerate(spec["nodes"])}
    ids["END"] = "finished"
    lines = ["```mermaid", "flowchart TD", "  start([Start])", "  finished([End])", f"  start --> {ids[spec['entry']]}"]
    for node in spec["nodes"]:
        lines.append(f'  {ids[node["id"]]}["{label(node.get("name", node["id"]))}"]')
    for edge in spec["edges"]:
        cond = edge.get("label") or ("otherwise" if edge.get("otherwise") else condition(edge["when"]) if "when" in edge else "")
        link = f' -->|"{label(cond)}"| ' if cond else " --> "
        lines.append(f"  {ids[edge['from']]}{link}{ids[edge['to']]}")
    return "\n".join(lines + ["```", ""])


def materialize(root, spec):
    spec = copy.deepcopy(spec)
    validate(spec, root)
    for node in spec["nodes"]:
        if "instructions" in node:
            path = root / "nodes" / node["id"] / "SKILL.md"
            node["skill"] = str(path.relative_to(root))
            desc = f"Perform the {node.get('name', node['id'])} node in the {spec['name']} graph."
            body = f"---\nname: {node['id']}\ndescription: {json.dumps(desc, ensure_ascii=False)}\n---\n\n# {node.get('name', node['id'])}\n\nRead the assigned run's STATE.md and the input provided by the parent before working. Work only on this node and preserve unrelated edits.\n\n{node['instructions']}\n\nReturn the assigned attempt_id, status, summary, patch, and existing artifact paths as JSON at the assigned result path. Patch only these state fields: {', '.join(node['writes']) or '(none)'}. Do not edit graph state directly. Domain failure is a success result with the relevant state flag set to false; use error only when you cannot execute the task.\n"
            atomic(path, body)
        elif node.get("skill_mode") == "copy":
            source = resolve_skill(root, node).resolve()
            dest = root / "nodes" / node["id"]
            if source.parent != dest.resolve():
                dest.parent.mkdir(parents=True, exist_ok=True)
                with tempfile.TemporaryDirectory(prefix=".node-copy-", dir=dest.parent) as temporary:
                    copied = Path(temporary) / node["id"]
                    copy_skill(source.parent, copied)
                    if dest.exists():
                        backup = root / ".authoring-history" / uuid.uuid4().hex / node["id"]
                        backup.parent.mkdir(parents=True)
                        dest.rename(backup)
                    copied.rename(dest)
                skill_text = (dest / "SKILL.md").read_text()
                skill_text = re.sub(r"(?m)^name:.*$", f"name: {node['id']}", skill_text, count=1)
                atomic(dest / "SKILL.md", skill_text)
            node["source_skill"] = node.get("source_skill", str(source))
            node["skill"] = str((dest / "SKILL.md").relative_to(root))
    validate(spec, root)
    template = (BUNDLE / "assets" / "graph-skill.md").read_text()
    substitutions = {"id": spec["id"], "name": spec["name"], "description": spec["description"], "description_json": json.dumps(spec["description"], ensure_ascii=False), "entry": spec["entry"], "nodes": "\n".join(f"- `{n['id']}`: {n.get('name', n['id'])}; skill: `{n['skill']}`" for n in spec["nodes"]), "inputs": "\n".join(f"- `{k}` ({v['type']}): {'required' if v.get('required') and 'default' not in v else 'optional; default supplied'}" for k, v in spec["state"].items() if v.get('required')) or "No additional required inputs."}
    for key, val in substitutions.items():
        template = template.replace("{{" + key + "}}", val)
    for folder in ("references", "assets", "scripts"):
        (root / folder).mkdir(parents=True, exist_ok=True)
    for rel in ("references/execution.md", "references/contract.md", "assets/graph-skill.md", "scripts/graph_ops.py"):
        source, dest = BUNDLE / rel, root / rel
        if source.resolve() != dest.resolve(): shutil.copy2(source, dest)
    atomic(root / "SKILL.md", template)
    atomic(root / "GRAPH.md", mermaid(spec))
    save(root / "graph.json", spec)
    if not (root / "STATE.md").exists():
        atomic(root / "STATE.md", f"# {spec['name']} state\n\nNo run has started. Ask Codex to run this graph with a task goal.\n")
    return spec


def run_files(graph):
    return sorted((graph / "runs").glob("*/state.json"))


def active_runs(graph):
    return [load(p) for p in run_files(graph) if load(p)["status"] in ACTIVE]


def read_run(graph, run_id=None):
    if run_id:
        require(bool(re.fullmatch(r"[a-zA-Z0-9-]+", run_id)), "Invalid run ID")
        file = graph / "runs" / run_id / "state.json"
        require(file.is_file(), f"Run not found: {run_id}")
    else:
        active = active_runs(graph)
        require(len(active) <= 1, "Multiple active runs: choose a run ID")
        if active: return active[0]
        files = run_files(graph)
        require(files, "No runs yet")
        file = files[-1]
    return load(file)


def event(run, kind, **info):
    run["events"].append({"at": now(), "kind": kind, **info})


def write_run(graph, run):
    run["updated_at"] = now()
    folder = graph / "runs" / run["id"]
    save(folder / "state.json", run)
    projection = f"# {run['graph']['name']} state\n\n- Run: `{run['id']}`\n- Goal: {run['values'].get('goal', '')}\n- Status: **{run['status']}**\n- Current node: `{run['current']}`\n- Definition: `{run['version']}`\n- Updated: {run['updated_at']}\n- Reason: {run.get('reason', '')}\n\n## Values\n\n```json\n{json.dumps(run['values'], ensure_ascii=False, indent=2)}\n```\n\n## Attempts\n\n"
    for attempt in run["attempts"]:
        projection += f"- {attempt['node']} / {attempt['id']}: {attempt['status']} {'(invalidated)' if not attempt.get('valid', True) else ''} — {attempt.get('summary', '')}\n"
    atomic(folder / "STATE.md", projection)
    atomic(graph / "STATE.md", projection)


def snapshot(graph, folder, spec):
    for node in spec["nodes"]:
        copy_skill(resolve_skill(graph, node).parent, folder / "skills" / node["id"])


def start(graph, project, goal, inputs, trial=None):
    require(not active_runs(graph), "Graph already has an active run; inspect, resume, or stop it first")
    spec = load(graph / "graph.json")
    validate(spec, graph)
    require(Path(project).is_dir(), "Target project does not exist")
    values = {k: copy.deepcopy(v["default"]) for k, v in spec["state"].items() if "default" in v}
    values.update(inputs)
    if goal is not None: values["goal"] = goal
    check_values(spec, values)
    require(not trial or trial in [n["id"] for n in spec["nodes"]], "Unknown trial node")
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S") + "-" + uuid.uuid4().hex[:8]
    folder = graph / "runs" / run_id
    snapshot(graph, folder, spec)
    run = {"id": run_id, "graph": spec, "version": digest(spec), "project": str(Path(project).resolve()), "created_at": now(), "status": "running", "current": trial or spec["entry"], "values": values, "attempts": [], "events": [], "step": 0, "visits": {}, "approvals": {}, "inflight": None, "trial": bool(trial), "pause_requested": False}
    event(run, "started", trial=bool(trial), version=run["version"])
    write_run(graph, run)
    return run


def node_of(run):
    return next(n for n in run["graph"]["nodes"] if n["id"] == run["current"])


def inflight(run):
    return next((a for a in run["attempts"] if a["id"] == run["inflight"]), None)


def check_idle(run):
    require(not run["inflight"], "A worker is in flight; inspect its actual handle before continuing")


def prepare(graph, run):
    require(run["status"] == "running", f"Run is {run['status']}: {run.get('reason', '')}")
    check_idle(run)
    node = node_of(run)
    key = f"{run['current']}:{run['step']}"
    if node.get("approval") and not run["approvals"].get(key):
        run.update(status="awaiting_input", reason=node["approval"])
        event(run, "approval_requested", node=node["id"], question=node["approval"])
        write_run(graph, run)
        return {"status": "awaiting_input", "question": node["approval"], "run": run["id"]}
    previous = [a for a in run["attempts"] if a["node"] == node["id"] and a["step"] == run["step"] and a.get("valid", True)]
    if run["step"] >= run["graph"].get("max_steps", 50) or (not previous and run["visits"].get(node["id"], 0) >= node.get("max_visits", 10)):
        run.update(status="blocked", reason="Configured loop/step limit reached")
        event(run, "limit_reached", node=node["id"])
        write_run(graph, run)
        return {"status": "blocked", "reason": run["reason"]}
    missing = [key for key in node["reads"] if key not in run["values"]]
    require(not missing, f"Node requires missing inputs: {missing}")
    attempt_id = uuid.uuid4().hex
    attempt = {"id": attempt_id, "node": node["id"], "step": run["step"], "status": "prepared", "input": copy.deepcopy(run["values"]), "created_at": now(), "agent_id": None, "valid": True}
    if not previous: run["visits"][node["id"]] = run["visits"].get(node["id"], 0) + 1
    run["attempts"].append(attempt)
    run["inflight"] = attempt_id
    run.pop("reason", None)
    folder = graph / "runs" / run["id"]
    skill_root = Path(run.get("skill_snapshot", folder / "skills"))
    handoff = {"run": run["id"], "attempt_id": attempt_id, "node": node["id"], "skill": str(skill_root / node["id"] / "SKILL.md"), "state_file": str(folder / "STATE.md"), "project": run["project"], "goal": run["values"]["goal"], "input": {k: run["values"][k] for k in node["reads"]}, "agent": node.get("agent", {}), "allowed_writes": node["writes"], "result_path": str(folder / "results" / f"{attempt_id}.json"), "result_contract": {"attempt_id": attempt_id, "status": "success or error", "summary": "actual result", "patch": {}, "artifacts": []}}
    (folder / "results").mkdir(exist_ok=True)
    event(run, "prepared", node=node["id"], attempt_id=attempt_id)
    write_run(graph, run)
    save(folder / "handoffs" / f"{attempt_id}.json", handoff)
    return handoff


def advance(run, previous_node):
    if run["trial"]:
        run.update(current="END", status="completed", reason="Node trial completed")
        return
    try:
        decision = route(run["graph"], previous_node, run["values"])
    except Invalid as exc:
        run.update(status="blocked", reason=str(exc), needs_route=previous_node)
        event(run, "routing_blocked", node=previous_node, reason=str(exc))
        return
    event(run, "routed", **decision)
    run["current"] = decision["to"]
    run.pop("needs_route", None)
    run["status"] = "completed" if decision["to"] == "END" else "paused" if run["pause_requested"] else "running"
    run["reason"] = "Workflow completed" if run["status"] == "completed" else "Pause requested" if run["status"] == "paused" else ""
    run["pause_requested"] = False


def finish(graph, run, result):
    require(run["status"] in {"running", "stopping"}, f"Cannot accept result while {run['status']}")
    attempt = inflight(run)
    require(attempt and result.get("attempt_id") == attempt["id"], "Result is stale or belongs to a different attempt")
    require(attempt.get("agent_id"), "Bind the real subagent handle before accepting results")
    require(result.get("status") in {"success", "error"}, "Result needs success/error status")
    require(isinstance(result.get("summary"), str) and result["summary"].strip(), "Result needs a summary")
    node = node_of(run)
    patch = result.get("patch", {})
    check_values(run["graph"], patch, partial=True, allowed=node["writes"])
    require(isinstance(result.get("artifacts", []), list), "Artifacts must be a list of paths")
    for artifact in result.get("artifacts", []):
        require(isinstance(artifact, str), "Artifact must be a path string")
        path = Path(artifact)
        if not path.is_absolute(): path = Path(run["project"]) / path
        require(path.exists(), f"Artifact not found: {path}")
    attempt.update(status=result["status"], summary=result["summary"], result=copy.deepcopy(result), completed_at=now())
    run["inflight"] = None
    event(run, "result", node=node["id"], attempt_id=attempt["id"], status=result["status"], summary=result["summary"])
    if run["status"] == "stopping":
        run.update(status="cancelled", reason="Stopped; result retained but not applied")
    elif result["status"] == "error":
        errors = sum(a["step"] == run["step"] and a["status"] == "error" and a.get("valid", True) for a in run["attempts"])
        run["status"] = "failed" if errors >= node.get("max_attempts", 1) else "paused" if run["pause_requested"] else "running"
        run["reason"] = result["summary"]
    else:
        run["values"].update(patch)
        run["step"] += 1
        advance(run, node["id"])
    write_run(graph, run)
    return run


def control(graph, run, args):
    action = args.command
    note = args.note or ""
    if action in {"resume", "retry", "recover", "rerun"}:
        require(not any(r["id"] != run["id"] for r in active_runs(graph)), "Another execution is active; stop it before reactivating this run")
    if action == "pause":
        require(run["status"] in ACTIVE, "Run is terminal")
        if run["inflight"]: run["pause_requested"] = True
        else: run.update(status="paused", reason="Paused by user")
    elif action == "cancel":
        require(run["status"] in ACTIVE, "Run is terminal")
        run.update(status="stopping" if run["inflight"] else "cancelled", reason="Stop requested")
    elif action == "settle":
        require(run["status"] == "stopping" and note, "Settle needs stopping status and evidence of terminal/missing handle")
        attempt = inflight(run)
        if attempt: attempt.update(status="interrupted", summary=note)
        run.update(inflight=None, status="cancelled", reason=note)
    elif action == "respond":
        require(run["status"] == "awaiting_input" and args.decision in {"approve", "decline"} and note, "Expected explicit gate response")
        run["approvals"][f"{run['current']}:{run['step']}"] = args.decision == "approve"
        run.update(status="running" if args.decision == "approve" else "paused", reason=note)
    elif action == "resume":
        check_idle(run)
        require(run["status"] in {"paused", "blocked"}, "Use retry for exhausted errors, recover for interrupted work, or respond for a gate")
        require(not run.get("stale_nodes"), f"Rerun affected nodes before resuming: {run.get('stale_nodes')}")
        run.update(status="running", pause_requested=False, reason="")
        if run.get("needs_route"): advance(run, run["needs_route"])
    elif action == "retry":
        check_idle(run)
        require(run["status"] == "failed" and note, "Retry needs failed status and user's reason/request")
        for attempt in run["attempts"]:
            if attempt["step"] == run["step"] and attempt["status"] == "error": attempt["valid"] = False
        run.update(status="running", reason=note, pause_requested=False)
    elif action == "recover":
        require(note and args.decision in {"retry", "accept"}, "Recovery requires an inspected outcome and retry|accept")
        require(run["status"] in {"cancelled", "running", "stopping"}, "Run does not need interrupted-worker recovery")
        # The parent must verify termination; this helper cannot query Codex handles.
        attempt = inflight(run) or (run["attempts"][-1] if run["attempts"] else None)
        require(attempt is not None and attempt["status"] in {"prepared", "running", "interrupted", "success", "error"}, "No attempt to recover")
        require(attempt["node"] == run["current"] and attempt["step"] == run["step"], "Attempt was already committed; use an explicit rerun instead of recovery")
        if args.decision == "accept":
            require(args.result, "Accept requires the original worker result")
            run.update(status="running", inflight=attempt["id"])
            event(run, "recovery_checked", note=note, decision="accept")
            return finish(graph, run, data(args.result))
        attempt.update(status="interrupted", valid=False, summary=note)
        run.update(status="running", inflight=None, reason=note, pause_requested=False)
    elif action == "set-state":
        check_idle(run)
        require(run["status"] in {"paused", "blocked"}, "Pause before changing state")
        require(args.input and note, "State changes need input and a reason")
        patch = data(args.input)
        check_values(run["graph"], patch, partial=True)
        changed = {key for key, val in patch.items() if run["values"].get(key) != val}
        affected = []
        nodes = {n["id"]: n for n in run["graph"]["nodes"]}
        for i, attempt in enumerate(run["attempts"]):
            if attempt.get("valid", True) and attempt["status"] == "success" and (changed & set(nodes[attempt["node"]]["reads"]) or affected):
                attempt["valid"] = False
                if not affected: run["stale_from"] = min(run.get("stale_from", i), i)
                affected.append(attempt["node"])
        run["values"].update(patch)
        run["pending_input_patch"] = {**run.get("pending_input_patch", {}), **patch}
        run["stale_nodes"] = list(dict.fromkeys(run.get("stale_nodes", []) + affected))
        event(run, "state_changed", patch=patch, affected=run["stale_nodes"], note=note)
    elif action == "rerun":
        check_idle(run)
        require(run["status"] != "running" and note, "Pause before rerun and record the user's request")
        candidates = [(i, a) for i, a in enumerate(run["attempts"]) if a["node"] == args.node]
        require(candidates, "Node has not run; use trial for an isolated test")
        index = -1 if args.occurrence is None else args.occurrence - 1
        require(-len(candidates) <= index < len(candidates), "Occurrence out of range")
        offset, chosen = candidates[index]
        require(offset <= run.get("stale_from", offset), "Rerun from the earliest affected node, not a downstream node")
        for attempt in run["attempts"][offset:]: attempt["valid"] = False
        values = copy.deepcopy(chosen["input"])
        values.update(run.pop("pending_input_patch", {}))
        run.update(values=values, current=args.node, step=chosen["step"], status="paused", reason=note, approvals={}, pause_requested=False, stale_nodes=[])
        run.pop("needs_route", None)
        run.pop("stale_from", None)
        run["visits"] = {}
        seen = set()
        for a in run["attempts"][:offset]:
            pair = (a["node"], a["step"])
            if a.get("valid", True) and pair not in seen:
                run["visits"][a["node"]] = run["visits"].get(a["node"], 0) + 1
                seen.add(pair)
    elif action == "migrate":
        check_idle(run)
        require(run["status"] in {"paused", "blocked", "failed"}, "Pause before migration")
        spec = load(graph / "graph.json")
        validate(spec, graph)
        require(run["current"] in [n["id"] for n in spec["nodes"]], "Current node was removed")
        check_values(spec, run["values"])
        old_nodes = {n["id"]: n for n in run["graph"]["nodes"]}
        new_nodes = {n["id"]: n for n in spec["nodes"]}
        changed = [n for n in old_nodes if old_nodes[n] != new_nodes.get(n)]
        completed = {a["node"] for a in run["attempts"] if a.get("valid", True) and a["status"] == "success"}
        require(not completed.intersection(changed), "Completed nodes changed; start a new run or rerun before migrating")
        if args.dry_run: return {"compatible": True, "from": run["version"], "to": digest(spec)}
        require(note, "Migration requires user's request")
        folder = graph / "runs" / run["id"]
        destination = folder / f"skills-{digest(spec)}"
        snapshot(graph, destination, spec)
        run["skill_snapshot"] = str(destination / "skills")
        run.update(graph=spec, version=digest(spec), approvals={})
    event(run, action, note=note, decision=args.decision)
    write_run(graph, run)
    return run


def list_graphs(project):
    rows = []
    for file in sorted((project / ".agents" / "skills").glob("*/graph.json")):
        spec = load(file)
        rows.append({"number": len(rows) + 1, "id": spec["id"], "name": spec["name"], "description": spec["description"], "path": str(file.parent), "active": [{"id": r["id"], "status": r["status"]} for r in active_runs(file.parent)]})
    return rows


def main(argv=None):
    commands = "connect disconnect doctor list create apply diff validate render clone delete route start trial prepare bind finish status history trace pause cancel settle respond resume retry recover set-state rerun migrate".split()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=commands)
    for field in ("project", "graph", "spec", "input", "result", "run", "goal", "node", "id", "name", "agent-id", "note", "decision"):
        parser.add_argument("--" + field)
    parser.add_argument("--occurrence", type=int)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    project = Path(args.project).resolve() if args.project else None
    graph = Path(args.graph).resolve() if args.graph else None
    cmd = args.command
    if cmd in {"connect", "disconnect", "doctor", "list", "create"}:
        require(project is not None, "--project is required")
    if cmd in {"connect", "disconnect"}: return connect(project, cmd == "disconnect")
    if cmd == "list": return list_graphs(project)
    if cmd == "doctor":
        errors = []
        for row in list_graphs(project):
            try: validate(load(Path(row["path"]) / "graph.json"), Path(row["path"]))
            except (Invalid, OSError) as exc: errors.append({"graph": row["id"], "error": str(exc)})
        return {"python": sys.version.split()[0], "project_exists": project.is_dir(), "registered": (project / "AGENTS.md").exists() and BEGIN in (project / "AGENTS.md").read_text(), "errors": errors, "native_subagents": "Check live Codex tools separately"}
    if cmd == "validate":
        require(args.spec or graph, "--spec or --graph is required")
        spec = data(args.spec) if args.spec else load(graph / "graph.json")
        return validate(spec, graph or (project / ".agents" / "skills" / spec["id"] if project else Path.cwd()))
    if cmd == "create":
        require(args.spec, "--spec is required")
        spec = data(args.spec)
        require(slug(spec.get("id")), "Invalid graph id")
        graph = project / ".agents" / "skills" / spec["id"]
        validate(spec, graph)
        for node in spec["nodes"]:
            if "instructions" not in node:
                node["skill"] = str(resolve_skill(graph, node).resolve())
        with lock(project / ".graph-engineering"):
            require(not graph.exists(), f"Graph already exists: {graph}")
            graph.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.TemporaryDirectory(prefix=".graph-draft-", dir=graph.parent) as temporary:
                staged = Path(temporary) / spec["id"]
                materialize(staged, spec)
                staged.rename(graph)
        connect(project)
        return {"graph": str(graph), "id": spec["id"], "created": True}
    require(graph and (graph / "graph.json").is_file(), "--graph must point to a generated graph")
    with lock(graph):
        spec = load(graph / "graph.json")
        if cmd in {"apply", "diff"}:
            require(args.spec, "--spec is required")
            draft = data(args.spec)
            require(draft.get("id") == spec["id"], "Graph ID is immutable; change its display name or clone it")
            validate(draft, graph)
            changes = "".join(difflib.unified_diff(json.dumps(spec, indent=2).splitlines(True), json.dumps(draft, indent=2).splitlines(True), fromfile="saved", tofile="proposed"))
            if cmd == "diff": return {"diff": changes}
            changed = materialize(graph, draft)
            return {"version": digest(changed), "diff": changes, "existing_runs_preserved": True}
        if cmd == "render":
            validate(spec, graph)
            atomic(graph / "GRAPH.md", mermaid(spec))
            return {"mermaid": str(graph / "GRAPH.md")}
        if cmd == "clone":
            require(project and slug(args.id) and args.name, "Clone needs --project --id --name")
            dest = project / ".agents" / "skills" / args.id
            require(not dest.exists(), "Clone destination already exists")
            cloned = copy.deepcopy(spec)
            cloned.update(id=args.id, name=args.name)
            for node in cloned["nodes"]:
                if "instructions" not in node: node["skill"] = str(resolve_skill(graph, node).resolve())
            materialize(dest, cloned)
            connect(project)
            return {"graph": str(dest), "id": args.id}
        if cmd == "delete":
            require(not active_runs(graph), "Cannot delete a graph with active runs")
            project = project_of(graph)
            references = []
            for row in list_graphs(project):
                other = Path(row["path"])
                if other == graph: continue
                for n in load(other / "graph.json")["nodes"]:
                    if resolve_skill(other, n).resolve().is_relative_to(graph): references.append(row["id"])
            require(not references, f"Referenced by graphs: {references}")
            archive = project / ".graph-engineering" / "archive" / f"{spec['id']}-{uuid.uuid4().hex[:8]}"
            if not args.dry_run:
                archive.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(graph), str(archive))
            return {"source": str(graph), "archive": str(archive), "history_preserved": True, "dry_run": args.dry_run}
        if cmd == "route":
            require(args.node and args.input, "Route needs --node and --input")
            return route(spec, args.node, data(args.input))
        if cmd in {"start", "trial"}:
            project = project or project_of(graph)
            require(cmd != "trial" or args.node, "Trial requires --node")
            return start(graph, project, args.goal, data(args.input) if args.input else {}, args.node if cmd == "trial" else None)
        if cmd == "history":
            return [{k: load(file).get(k) for k in ("id", "created_at", "status", "version", "current", "values", "trial")} for file in run_files(graph)]
        run = read_run(graph, args.run)
        if cmd in {"status", "trace"}: return run
        if cmd == "prepare":
            return prepare(graph, run)
        if cmd == "bind":
            attempt = inflight(run)
            require(attempt and args.agent_id, "Bind needs an in-flight attempt and real --agent-id")
            require(not attempt.get("agent_id") or attempt["agent_id"] == args.agent_id, "Attempt already belongs to another agent")
            attempt.update(agent_id=args.agent_id, status="running")
            event(run, "bound", attempt_id=attempt["id"], agent_id=args.agent_id)
            write_run(graph, run)
            return {"bound": True, "attempt_id": attempt["id"]}
        if cmd == "finish":
            require(args.result, "--result required")
            return finish(graph, run, data(args.result))
        return control(graph, run, args)


if __name__ == "__main__":
    try:
        print(json.dumps(main(), ensure_ascii=False, indent=2, allow_nan=False))
    except (Invalid, OSError, ValueError, KeyError, TypeError, StopIteration) as error:
        print(json.dumps({"error": str(error), "type": type(error).__name__}, ensure_ascii=False), file=sys.stderr)
        sys.exit(2)
