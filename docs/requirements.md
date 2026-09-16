# Functional requirements

Recorded on 2026-09-16 from the user's requirements and corrections. All requests are natural language; Codex interprets them and performs authoring, file operations, validation, and native subagent delegation. This deliverable is the `graph-engineering` meta skill, not a separate application or agent service.

Implementation details are internal. Users need not write JSON, node IDs, paths, conditions, or commands. Infer from existing context; ask only for missing consequential information or ambiguous targets. Generated graph skills must work in a fresh Codex task without the authoring conversation.

| ID | Required user capability |
|---|---|
| SET-01 | Install the meta skill and make it discoverable in Codex. |
| SET-02 | Connect a project and register usage in AGENTS.md without duplication or unrelated changes. |
| SET-03 | Diagnose installation, paths, graph definitions, and native delegation availability. |
| SET-04 | Update only the installed meta skill while preserving generated graphs and run records. |
| SET-05 | Disconnect project registration while preserving graphs/history unless deletion is separately requested. |
| CREATE-01 | Describe a workflow and have its purpose, nodes, order, inputs, and outputs generated. |
| CREATE-02 | Include conditional branches and loops in a creation request. |
| CREATE-03 | Preview the proposal and revise it before saving when requested. |
| CREATE-04 | Save a standalone graph skill with node skills, executable definition, GRAPH.md, and initial state. |
| CREATE-05 | Discover and use the generated skill in a fresh Codex task. |
| GRAPH-01 | List graphs and select by name, description, or displayed number. |
| GRAPH-02 | Inspect Mermaid and an explanation of entry, nodes, edges, conditions, and termination. |
| GRAPH-03 | Rename display name/description without breaking references. |
| GRAPH-04 | Clone an independently editable graph without copying execution history. |
| GRAPH-05 | Delete a graph with active-work/reference checks and explicit history handling. |
| NODE-01 | Add a node and its skill, updating affected connections. |
| NODE-02 | Change node instructions, scope, or completion criteria. |
| NODE-03 | Remove a node and repair affected edges/dependencies, clarifying ambiguity. |
| NODE-04 | Find and attach an existing skill, clarifying ambiguous matches. |
| NODE-05 | Make a graph-local skill copy or intentionally share a skill; preserve unrelated users. |
| NODE-06 | Select supported saved subagent roles/models/reasoning or inherit defaults. |
| NODE-07 | Connect typed node outputs to subsequent node inputs. |
| FLOW-01 | Choose the starting stage through natural language. |
| FLOW-02 | Describe executable completion conditions. |
| FLOW-03 | Reorder stages and update connections. |
| FLOW-04 | Route different outcomes to different stages. |
| FLOW-05 | Bound loops and define behavior on exhaustion. |
| FLOW-06 | Handle missing/ambiguous routing outcomes explicitly. |
| FLOW-07 | Request a user-response gate before a stage. |
| STATE-01 | Define state fields, meanings, types, and defaults naturally. |
| STATE-02 | Define required start inputs and ask when they are unavailable. |
| STATE-03 | Carry outputs and evidence between nodes. |
| STATE-04 | Explain progress, remaining work, and failure/wait reasons from STATE.md and checkpoints. |
| STATE-05 | Pause, change input/state, inspect affected results, and resume appropriately. |
| CHECK-01 | Validate entry, references, skills, schemas, conditions, termination, and loop bounds. |
| CHECK-02 | Explain/fix invalid definitions, asking when intent is needed. |
| CHECK-03 | Explain authoring changes and their effects. |
| CHECK-04 | Simulate routing with example state without performing node work. |
| CHECK-05 | Keep executable definition and Mermaid synchronized after edits. |
| CHECK-06 | Preserve active run definitions; check compatibility before requested migration. |
| RUN-01 | Invoke a saved graph with a real goal, target project, and inputs. |
| RUN-02 | Infer available inputs from context and ask only for missing consequential values. |
| RUN-03 | Execute every work node in a real native Codex subagent by default. |
| RUN-04 | Validate authentic results, checkpoint, and follow saved routes. |
| RUN-05 | Inspect current/completed stages, repeat/retry counts, and waiting state. |
| RUN-06 | Get actual terminal status, outputs, evidence, and unresolved work. |
| RUN-07 | Reuse a graph for a separate goal without leaking state from earlier runs. |
| CONTROL-01 | Pause after an in-flight node and before dispatching the next. |
| CONTROL-02 | Stop live work and verify actual termination, preserving observed changes. |
| CONTROL-03 | Resume the intended saved execution from its last verified state. |
| CONTROL-04 | Resume from a fresh Codex task without the original worker's context. |
| CONTROL-05 | Configure bounded execution-error retries and exhaustion behavior. |
| CONTROL-06 | Distinguish domain failure from execution/tool error. |
| CONTROL-07 | Rerun a chosen node occurrence with downstream invalidation and retained history. |
| CONTROL-08 | Inspect interrupted/uncertain effects before accepting or replaying work. |
| TRACE-01 | List historical runs with goal, status, and graph version. |
| TRACE-02 | Inspect node inputs, authentic outputs, artifacts, and errors. |
| TRACE-03 | Explain routing using the state and conditions evaluated at that time. |
| TRACE-04 | Explain what blocks progress and what is needed to resume. |
| TRACE-05 | Trial one node through a subagent with isolated run state. |

## Execution scope

Sequential nodes, conditional branches, bounded loops, user gates, checkpoints, and resumption are required. One active run per graph is supported. Parallel-node execution is a separately scoped extension; it is not claimed. Worker interruption is not filesystem rollback. Helpers cannot independently verify native agent handles; the parent must observe their real state.

## Completion evidence

All requirements need relevant behavioral evidence. Unit tests verify only deterministic helper mechanics. Installed-skill evaluations must cover natural-language authoring/management, real backend development with native subagents, failure routing, controls, and fresh-session recovery. Publication and install/update must be exercised against the real public GitHub repository.

