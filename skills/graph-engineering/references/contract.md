# Graph contract, version 1

Codex authors `graph.json`; users describe behavior. Paths to skills resolve from the graph directory. Artifacts resolve from the absolute target project recorded at run start. Use JSON primitives.

```json
{
  "format_version": 1,
  "id": "backend-development-graph",
  "name": "Backend development",
  "description": "Develop backend features through analysis, implementation, testing, and review.",
  "entry": "analyze",
  "max_steps": 20,
  "routing": "exclusive",
  "state": {
    "goal": {"type": "string", "required": true},
    "requirements": {"type": "string", "default": ""},
    "tests_passed": {"type": "boolean", "default": false}
  },
  "nodes": [{
    "id": "analyze",
    "name": "Analyze requirements",
    "instructions": "Inspect the existing API and turn the goal into acceptance criteria. Do not implement code. Return requirements with evidence paths.",
    "reads": ["goal"], "writes": ["requirements"],
    "agent": {"type": "default"}, "max_attempts": 2, "max_visits": 3
  }],
  "edges": [{"from": "analyze", "to": "END"}]
}
```

This demonstrates the format, not a complete backend workflow. Generate every requested stage.

Required: `format_version`, `id`, `name`, `description`, `entry`, `state`, `nodes`, `edges`. IDs are unique lowercase letters/digits/hyphens, at most 64 characters. `END` terminates. Every node must have outgoing edges, be reachable from entry, and have a possible route to END. Loops are bounded by `max_steps` and node `max_visits`.

State types: `string`, `boolean`, `integer`, `number`, `array`, `object`. Optional `enum`, `default`, `required`. `goal` is a required string. Required fields without defaults are inputs to gather before starting. `reads` and `writes` are lists of state keys. Workers patch only declared writes. Missing patches preserve existing values. Require meaningful output and actual evidence in the node instructions.

Node: `id`, optional `name`, and either non-empty `instructions` or `skill` pointing to an existing `SKILL.md` plus `skill_mode: shared|copy`. Optional `agent` keys: `type`, `model`, `reasoning_effort`. Omit to inherit. `max_attempts` defaults to 1; `max_visits` defaults to 10. An `approval` string is shown to the user before the node. Workers cannot approve themselves.

Conditions are explicit data expressions, never code:

```json
{"field": "tests_passed", "op": "eq", "value": true}
{"all": [{"field": "tests_passed", "op": "eq", "value": true}, {"field": "review_passed", "op": "eq", "value": true}]}
{"any": [{"field": "tests_passed", "op": "eq", "value": false}, {"field": "review_passed", "op": "eq", "value": false}]}
{"not": {"field": "tests_passed", "op": "eq", "value": true}}
```

Operators: `eq`, `ne`, `gt`, `gte`, `lt`, `lte`, `in`, `contains`, `exists`. Fields name declared top-level state keys. An edge without `when` always matches. `otherwise: true` applies only if no regular edge matches; one fallback per source. `routing: exclusive` blocks on multiple matches; `first-match` uses array order and should be selected only for requested priority. No match without fallback blocks for clarification.

Give conditional edges a concise `label` such as `Tests pass` or `Needs changes`. It is used only for Mermaid display; `when` remains the executable rule. Keep labels consistent with conditions.

Worker result file: `attempt_id`, `status: success|error`, `summary`, `patch`, `artifacts` (project-relative or absolute file paths). Failing tests are a successful execution with `tests_passed: false` and test evidence. A failure to execute the tests is an error. `finish` validates the attempt token, patch, artifacts, then checkpoints and routes.
