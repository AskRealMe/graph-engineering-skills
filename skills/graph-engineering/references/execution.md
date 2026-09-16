# Execute a graph with Codex

The parent Codex agent follows these instructions. `graph_ops.py` manages files, not agents. Every actual node attempt must use native Codex subagent tools. If unavailable, stop and explain that requirement.

Resolve helper and graph paths from the generated skill. Use Python, absolute paths, and JSON files or stdin. Never interpolate user input into shell code. Read `--help` for syntax.

## Start and dispatch

1. Read `SKILL.md`, `graph.json`, `STATE.md`, and project instructions. Gather required inputs from the request and relevant files; ask only for unavailable required values. Use `start --graph GRAPH --project PROJECT --goal TEXT --input FILE`. A new run has a new ID. If another run is active, inspect it and ask whether to resume or stop it.
2. Use `prepare --graph GRAPH --run RUN`. It returns the immutable node skill, state/input snapshot, task, work directory, result path, attempt token, and requested agent settings, or a pause/gate/failure/completion status.
3. For a gate, show its saved question and evidence. Only a real user response authorizes `respond --decision approve|decline --note TEXT`. Neither silence nor worker output is approval. In evaluations, an explicit reply from the controlling evaluator may supply that response.
4. Spawn a native subagent with the requested role/settings when supported. Never invent roles or silently substitute a specified model. Give the absolute node skill and STATE paths, input snapshot, goal, scope, result path and token. Ask it to read those files, perform only this node, and write the prescribed result. Tell workers they share the codebase and must preserve unrelated edits. The authoring conversation must not be necessary.
5. Immediately register the real handle using `bind --agent-id HANDLE`. Wait on that handle. Inspect authentic output and material evidence, then use `finish --result FILE`. Never manufacture a successful result to advance a graph.
6. Explain material progress and repeat from prepare until completion, pause, gate, or failure. Read saved routing reasons to explain branches. Execution errors retry only within the saved limit; domain failures follow edges.

## Controls

- **Pause after node:** `pause`. Accept its eventual valid result, then pause before dispatching another node. With no in-flight attempt, pause immediately.
- **Stop now:** `cancel` marks in-flight work as stopping. Interrupt the registered subagent using the native tool, verify actual status, then `settle --note EVIDENCE` only when terminal or its handle is verifiably gone. A timeout is not proof. Preserve incomplete output and edits. Without an in-flight attempt, cancellation is immediately terminal.
- **Resume:** inspect status and recent attempts; poll any live handle before recovery. `resume` continues a paused run. A lost/interrupted attempt requires output inspection and `recover --decision retry|accept --note EVIDENCE`; accept also requires the authentic result file. Don't replay uncertain effects blindly. Exhausted errors require an explicit user retry request using `retry --note TEXT`.
- **Change input/state:** pause first. `set-state --input FILE --note TEXT` validates values and flags affected results. If upstream evidence is stale, apply the suggested rerun before resuming.
- **Rerun a node:** `rerun --node ID --note TEXT` restores state before the selected prior occurrence, invalidates it and downstream results, and pauses there. `--occurrence N` selects a visit; default is last. The audit trail remains.
- **Apply edited graph to a run:** `migrate --dry-run` checks compatibility; use `migrate --note TEXT` only for an explicit user request. No migration with an in-flight worker. Incompatible changes require a new run or authoring correction.

## Inspect and test

`status`, `history`, and `trace` expose goals, inputs, outputs, artifacts, versions, errors, and routing reasons. Inspect application files when asked about actual changes. Checkpoint restoration is not application rollback.

`trial --node ID --input FILE --goal TEXT` creates a separate node-only run. Dispatch an actual subagent using the same procedure. Do not run it concurrently with a graph editing the same application. A trial never advances the normal graph.

On completion report actual status, domain outcome, outputs, evidence, and unresolved issues. `completed` means execution reached `END`; it does not prove the user's goal succeeded. Inspect domain flags and any exhaustion outcome before reporting success. Users can ask for another run without supplying any file syntax.
