---
name: graph-engineering
description: Create, inspect, and edit graph workflow skills through natural-language conversation. Use when a user wants reusable workflows with skill nodes, subagent execution, shared state, branches, loops, or changes to an existing generated graph.
metadata:
  compatibility: "Codex subagent tools, Python 3.10+ on macOS/Linux, and a writable project"
---

# Graph Engineering

You are using a meta skill. Your deliverable is another skill that a future Codex session can read and execute. Use Codex's existing file and subagent tools; the bundled helper only manages files and checkpoints.

## Talk in the user's language

All operations begin with natural-language requests. Infer the project, graph, nodes, and intended changes from the conversation and existing files. Ask only for consequential information that cannot be found or reasonably inferred. Never require the user to write JSON, conditions, paths, node IDs, or shell commands.

When invoked without a task, ask what workflow the user wants to create or change. When they already described it, act on that description. Explain results in workflow terms and show the graph when useful. Don't make users approve every reversible authoring step.

## Choose the operation

- **Create/edit/copy/delete a graph or node:** read [authoring.md](references/authoring.md), then [contract.md](references/contract.md) for the definition format.
- **Connect, list, diagnose, update, disconnect, or explain history:** read [operations.md](references/operations.md).
- **Run/resume/control a graph or try a node:** read [execution.md](references/execution.md). Prefer its generated `SKILL.md` as the execution entry point.

Resolve `scripts/graph_ops.py` from this skill directory. Invoke it with Python and absolute paths. Read `--help` for exact arguments. It is an internal helper, not the user's interface. Pass structured inputs through files or stdin; never shell-interpolate user text.

## Preserve these invariants

1. **Authoring and execution are separate.** This skill changes graph structure. A generated skill executes its saved instructions and does not redesign its workflow during a run.
2. **A node is a skill; an attempt is a subagent.** Explicitly delegate. Never silently perform node work in the parent when delegation is unavailable; explain the missing capability.
3. **State comes from evidence.** Give the worker the exact node skill, `STATE.md`, run input, scope, and output contract. Record only results actually produced. Domain failures (`tests_passed: false`) differ from execution errors.
4. **The parent commits state.** Workers return patches and evidence, not arbitrary rewrites of shared state. The helper validates and atomically records results, then derives `STATE.md` and `GRAPH.md`.
5. **Snapshots are stable.** Editing changes future runs. Existing runs retain their definition and skills unless the user explicitly requests a checked migration.
6. **Stop is not undo.** Interrupt and verify the actual subagent before acknowledging cancellation. If its handle is gone, inspect outputs before retrying. A timeout alone is not termination.
7. **Reuse stays scoped.** Make shared versus copied skills explicit. Never modify another shared skill as a side effect of a graph-local edit.

For a new graph, validate it and inspect the generated `SKILL.md` and Mermaid. Explain its name, stages, branches, required inputs, and how to ask to run or change it. Register the project through the managed `AGENTS.md` block, preserving all other content.

Include optional scripts and references only when useful. Do not build a separate application, service, custom model loop, or graphical editor to satisfy this skill.
