---
name: {{id}}
description: {{description_json}}
metadata:
  compatibility: "Codex subagent tools and Python 3.10+ on macOS/Linux"
---

# {{name}}

{{description}}

This is an execution skill. Follow its saved graph; use `$graph-engineering` to redesign the workflow.

Read `graph.json`, `STATE.md`, and [execution instructions](references/execution.md). Entry: `{{entry}}`. Resolve paths from this skill directory. `scripts/graph_ops.py` validates and checkpoints; you remain the orchestrating Codex agent.

Every work node is a skill executed by a native Codex subagent. Explicitly delegate each attempt, pass its skill and state, wait for authentic output, and commit results. Do not simulate delegation or silently do node work in the parent. If subagent tools are unavailable, explain and stop before executing a node.

The user supplies the goal and inputs naturally. Ask only for missing consequential inputs. Explain progress, conditions, and outcomes in their language. Support status, pause, stop, retry, node trial, and resume using the execution instructions.

`GRAPH.md` visualizes the workflow. `STATE.md` is a readable projection. `runs/<run-id>/state.json` is authoritative and preserves the definition, state, attempts, and routing evidence. Fresh sessions recover without the authoring conversation.

## Nodes

{{nodes}}

## Inputs

Gather required values without a default from the user's request or project context.

{{inputs}}

## Shared state

These fields carry intermediate results and defaults. A user can request suitable starting overrides in natural language; do not ask them to supply intermediate results that the nodes produce.

{{state}}
