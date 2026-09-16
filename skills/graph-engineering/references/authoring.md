# Authoring graph skills

## Create

1. Read project instructions. Inspect existing skills when reuse is requested. Establish purpose, entry, nodes, outputs, conditions, termination, and finite loop limits. Infer from context; ask only about consequential ambiguity.
2. Read `contract.md`. Write a temporary JSON specification with real task-specific node instructions, work boundaries, evidence, and outputs. Do not use a canned backend graph for unrelated requests.
3. Show a proposal first if requested; otherwise create within scope using `graph_ops.py create --project ABS --spec ABS`. This connects the project, validates, and generates a discoverable skill. Never overwrite an existing graph with create.
4. Use `validate --graph ABS`; inspect `SKILL.md` and `GRAPH.md`. Explain the workflow and how to invoke it naturally.

## Edit

Use `list --project ABS`, select the intended graph, and read `graph.json`. Display numbers are selectors only. Stable IDs survive renaming and reordering.

Translate the request into an updated full spec based on the existing one. Save it outside the graph, then use:

```text
diff --graph ABS --spec DRAFT
validate --spec DRAFT --project PROJECT
apply --graph ABS --spec DRAFT
```

`apply` synchronizes instructions, node skills, and Mermaid. `id` stays stable; change display `name` and `description` to rename. Existing run snapshots are unaffected.

For removal, repair affected edges and state dependencies; ask if the replacement path is ambiguous. Semantic conditions need typed node outputs such as `review_passed` plus judgment instructions. Route using that output. Use a node's `approval` for a user gate. Discover available Codex roles/models before setting `agent`; never invent an unavailable role.

Use an absolute `skill` path with `skill_mode: shared` to reuse an existing skill. Use `skill_mode: copy` for graph-local adaptation; its resources are copied. Own-node text goes in `instructions`. Shared edits require checking other references and explicit scope; a graph-local edit should use a copy.

- Copy: `clone --graph ABS --project TARGET --id NEW --name DISPLAY`. Identity and state are independent; no history is copied.
- Delete: `delete --graph ABS` archives definition and history under `.graph-engineering/archive/`. It refuses active runs and references. Inspect `--dry-run` first. Permanently remove an owned archive only if the user explicitly requests that scope.
- Dry routing: `route --graph ABS --node ID --input FILE` evaluates conditions without doing work.
- Node trial: follow the execution reference; use an actual subagent and a separate run.

Give branch edges short human-readable `label` values describing their actual conditions. `GRAPH.md` contains only a Mermaid fenced block. Follow project language rules for files and the user's language in conversation.
