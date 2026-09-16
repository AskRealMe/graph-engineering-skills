# Graph Engineering

A meta skill for creating and editing graph workflow skills from natural-language requests. Its first supported host is Codex.

Ask for a workflow. Codex writes a new skill containing node skills, transitions, state, and a Mermaid diagram. Invoke that generated skill later with a real task; Codex delegates each work node to a subagent and carries results between nodes.

The reusable product is the skill itself: instructions an AI agent reads and follows, with supporting references, templates, and file helpers. `graph-engineering` teaches authoring; a generated graph skill teaches execution; each node skill teaches one stage of work. The user describes all of these operations in natural language.

## Install

```sh
npx skills add AskRealMe/graph-engineering-skills --skill graph-engineering --agent codex
```

Add `--global` for a personal installation. Installation uses the open `skills` CLI and this GitHub repository; no separate server or npm package from this repository is required.

## Use natural language

```text
Use $graph-engineering to create a backend development graph: analyze the
requirements, implement, test, and review. Failed tests or reviews return to
implementation. Stop after three implementation passes.
```

```text
Add a security review after tests. Use my existing security-review skill.
Show me the updated graph and explain what changed.
```

```text
Use $backend-development-graph to implement a small HTTP task API.
Pause after the next node, then continue from another Codex task.
```

Codex handles file formats, node identifiers, and helper commands. Users describe desired behavior. Ask for status, routing explanations, graph copies, isolated node trials, retries, or resumption in the same way.

## What is installed

`skills/graph-engineering/SKILL.md` is the entry point. Focused references describe authoring and operation. A Python standard-library helper validates definitions, generates portable skill files, and records execution state. The helper does not call a model or spawn agents; Codex does that using its native subagent tools.

Generated graphs live in `.agents/skills/<graph-id>/` in the target project. Each contains `SKILL.md`, node skills, `graph.json`, `GRAPH.md`, and `STATE.md`. Each run keeps its own definition and skill snapshot, inputs, attempts, outputs, and routing evidence. Generated skills include execution instructions and the helper so they remain usable independently of the authoring conversation.

Requires Codex with subagent tools, Python 3.10+ on macOS/Linux, and write access to the project. The initial execution scope is sequential nodes, branches, bounded loops, user gates, and pause/resume. One active run per graph is supported. Graphs and node trials must not write the same application files concurrently.

Stopping an agent does not undo edits. Resuming an interrupted attempt requires checking actual output first. Conditions are explicit data comparisons; semantic judgments belong in node results.

## Development

```sh
python3 -m unittest discover -s tests -v
```

See [requirements](docs/requirements.md) and [verification evidence](docs/verification.md). Natural-language behavioral evaluation is separate from helper tests.
