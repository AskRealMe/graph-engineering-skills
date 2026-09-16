# Verification artifacts

Recorded on 2026-09-16. These are compact, sanitized artifacts from local behavioral evaluations, not a production certification or an exhaustive test of every possible workflow.

- `backend.md`, `backend-run.json`, and `backend-events.json`: completed backend graph, eight authentic native attempts, and two actual failed-test return edges. Routing state is explicitly projected to the control values; full local events are retained.
- `backend-testing-1.json`, `backend-testing-2.json`, and `backend-testing-3.json`: actual HTTP test command outcomes, preserving the initial deliberate regression and the distinct documented-command failure.
- `backend-review.md`, `backend-review-check.json`, and `backend-parent-final.json`: independent review, its additional focused HTTP check, and the parent verification of all 99 final tests.
- `backend-graph.json` and `backend-GRAPH.md`: the generated backend definition and its Mermaid representation.
- `controls.md` and `controls-runs.json`: nine authentic attempts covering pause, fresh-context resume, a user gate, execution errors, retry, domain failure, rerun, cancellation, recovery, and a trial.
- `cancellation-inspection.json` and `trial-isolation.json`: observed terminal native handle and retained normal-run hashes.
- `controls-reuse.md` and related JSON files: a second normal goal on the final installed revision, three fresh native attempts, and all 41 prior run files preserved.
- `management.md` and `management-commands.json`: natural-language authoring and management using the public develop installation, including expected rejected operations.
- `management-retest.md` and `.json`: observed findings retested against the updated public installation.
- `reference-deletion-check.json`: deletion refused while another graph referenced the node skill.
- `release.json`: public main installation, exact-file match, preserved workspace instructions, and fresh-session discovery.
- `install-update.json`: actual remote update and unchanged graph, history, and registration hashes.
- `discovery.md`: independent fresh-session Codex catalog discovery.
- `skill-manifest.json`: exact skill files compared with the published installation.
- `helper-tests.log` and `.json`: 31 deterministic helper tests. Their synthetic handles are not native execution evidence.

Local raw logs retain full command output, node input snapshots, result files, application artifacts, and native handles. Public copies replace local home/project paths with placeholders; evaluator prompts are preserved in their original language. Relative paths inside evaluation reports refer to their isolated raw evaluation projects unless explicitly linked. Refer to the parent verification document for requirement coverage and the exact scope of each lane.
