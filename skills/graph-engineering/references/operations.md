# Operations

Perform these through natural language. Commands are for Codex, not the user.

- Connect: `connect --project ABS` inserts an idempotent managed block in `AGENTS.md`, preserving outside text. It records graph location and natural-language usage. Global installation can connect multiple projects.
- Diagnose: `doctor --project ABS` checks Python, paths, definitions and registration. Separately confirm live native subagent tools and Codex skill discovery; the helper cannot inspect session capabilities.
- List/select: `list --project ABS` shows IDs, names, descriptions, paths and active runs. Match the request, asking only if ambiguous.
- Inspect: `GRAPH.md` holds Mermaid; `status --graph ABS`, `history --graph ABS`, and `trace --graph ABS --run ID` expose state and evidence. Explain naturally.
- Disconnect: `disconnect --project ABS` removes only the managed registration block, preserving generated graphs and runs.
- Install: `npx skills add AskRealMe/graph-engineering-skills`. Use project scope unless personal installation is requested; then add `--global`. Inspect an already supplied skill instead of reinstalling blindly.
- Update: inspect local customizations first. Update only the meta skill using `npx skills update graph-engineering --project --yes` or `--global --yes` for its actual scope. Check the installed CLI's help if needed. Preserve graphs and runs. Generated helpers stay pinned until explicit upgrade and compatibility verification.

`npx skills` installs from GitHub. `agentskills.io` defines the format; publishing to that website is not a separate package-release step. Do not claim a skills.sh search listing without checking it.

