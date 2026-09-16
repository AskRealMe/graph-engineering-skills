# Installed Skill Forward Evaluation

Recorded on 2026-09-16 (Asia/Seoul).

## Scope

This evaluation uses only the installed Graph Engineering skill and its documented resources. All side effects are confined to this backend-live project. Source implementation and source tests are not inspected.

## Natural-language request

Create a backend development graph with requirements analysis, implementation, testing, and review. Failed tests or review return to implementation. Allow at most three implementation visits; report the goal as unmet if attempts are exhausted. Every node must use a real native Codex subagent. Implement a Node.js built-in-only HTTP todo API with creation, listing, completion update, deletion, and proper request errors. Verify locally and preserve evidence.

## Installed artifact

Installed root: `EVALUATION_ROOT/.agents/skills/graph-engineering`. The per-file SHA-256 manifest is `evidence/installed-sha256.json`. Source revision will be recorded from the installer provenance.

## Authoring

The task-specific definition is `backend-spec.json`. The definition limits implementation to three visits and uses explicit exhausted outcomes.

Installed from the public source [AskRealMe/graph-engineering-skills develop](https://github.com/AskRealMe/graph-engineering-skills/tree/develop/skills/graph-engineering), at develop commit `78cf349ebf642553ec06fe45f78d0695b8abfd95`. Installer-reported package hash: `0aff8c0d327827eb0ea8df709cf2c7df4717a18bc1fbe9bb1a5d033ef195a544`. Installation used project scope and copy mode. Provenance was supplied by the controlling installer; this evaluator did not inspect source implementation.

Creation and validation both exited 0. Validator reported four nodes and version `c282d034787e30c5`. Actual validation output is preserved in `evidence/authoring-checks.json`. The generated SKILL.md, graph.json, GRAPH.md, node instructions, and managed AGENTS.md registration were inspected.

## Fresh-context execution

The native executor handle is `/root/backend_installed/backend_executor`, spawned with `fork_turns: none`. It received only the generated execution skill path, target project, natural-language API request, ownership constraints, evidence requirements, and an explicit pause-after-first-implementation control request. It received no graph-authoring conversation or source implementation. Node handles and execution results will be preserved by the executor.

## Static routing checks (not node execution)

Five helper route checks exited 0 and are preserved in `evidence/static-routing-checks.json`: first failed test returns to implementation, a third failed test reaches END, a second failed review returns to implementation, a third failed review reaches END, and a passed review reaches END. These are explicit data-expression checks only; they do not establish runtime subagent delegation, actual test failure, repair, review failure, or exhaustion. Those claims require separate native execution evidence.

The initial normal run ID is `20260916T054313-b130ae4b`. The requirements native handle is `/root/backend_installed/backend_executor/requirements_1` and was registered by the executor.

A read-only status probe occurred before the executor had started its run; it exited 2 with `No runs yet`. This was a timing observation, not a helper failure or application test. The executor subsequently created the run normally.

## Deliberate regression injection

The controlling evaluator requested a pause during implementation visit 1. The executor finished the authentic result and reported `status=paused`, `current=testing`, and `inflight=null` before any testing dispatch. At that checkpoint the evaluator changed exactly one production expression: newly created todos use `completed: true` instead of the specified `false`. This is a deliberately injected regression, not an organically discovered implementation defect. No test, result file, graph state, or definition was altered. Before/after source, a unified diff, timestamps, hashes, and authorization are in `evidence/deliberate-regression/`. The graph must discover and repair the defect through actual testing and implementation nodes.

The generated run remains pinned to the initial installed package from source revision `78cf349ebf642553ec06fe45f78d0695b8abfd95`; it was not migrated after later source updates. `evidence/generated-sha256.json` records the generated definition, node, helper, and execution-reference hashes and confirms its helper/reference bytes match the initial installed manifest. Final package exact-file verification is performed separately by the controlling release evaluator and is not claimed by this backend run.

## First actual HTTP test result

Native testing attempt `f7c609ae24f049ba98c89217b54ce462` executed `node --test --test-reporter=tap todo.integration.test.cjs` against real dynamically allocated loopback listeners and child server processes. Actual command exit: **1**; TAP totals: **99 tests, 98 pass, 1 fail, 0 cancelled, 0 skipped**. The failing assertion expected newly created todos to have `[false, false, false]` completion values and observed `[true, true, true]`, detecting the deliberate regression. Full TAP, exact command, runtime, source snapshots, and hashes are preserved under `evidence/testing-f7c609ae24f049ba98c89217b54ce462/`. The test snapshot SHA-256 is `e8de50833a3fc4713289ac985cda4b967bc0e2cf333b23152f01b0f7bae89303`; the tested production SHA-256 matches the deliberately injected version. The evaluator independently read the actual execution metadata, TAP summary, and HTTP test implementation.

The executor accepted the authentic failed test result with helper `finish` (actual exit 0). The recorded routing event selected `testing → implementation` under `tests_passed=false && implementation_round<3` (`Tests fail; attempts remain`). `evidence/controller/testing-1-finish.json` preserves the full real checkpoint/transition output. This is a domain failure returned by a successful test-node execution, not an execution error or a simulated route.

## Actual repair

Implementation visit 2, attempt `5f1ddf27342c40c9ab0bc66e3bb86386`, reproduced the failure and changed exactly the default completion value back to `false`. Its pre-repair integration command exited 1 (98 pass/1 fail), and the same unchanged test file exited 0 after repair (99 pass/0 fail). Syntax checks exited 0. The diff command exited 1 because it found the intended single-line change; this is not a test failure. Full before/after outputs, snapshots, exact commands, hashes, and diff are in `evidence/implementation-5f1ddf27342c40c9ab0bc66e3bb86386/`.

The evaluator independently inspected the repair summary, hash verification, and one-line diff. The test SHA-256 stayed `e8de50833a3fc4713289ac985cda4b967bc0e2cf333b23152f01b0f7bae89303`, so the repair did not weaken or modify the checks. The repaired production hash restored the original pre-injection SHA-256, `1254d735da49ff028e1b9e8d6d51c4f1db93636182c947af1fb14c912341b69b`.

## Naturally discovered verification-command failure

Independent testing visit 2 (`663668aec49143059228272b66ded7fe`) ran both the active integration suite and the README command. The explicit active-suite command exited **0**, with **99/99 passed**. The README command, `node --test`, exited **1**, with **297 tests, 296 pass, 1 fail, 0 cancelled/skipped**. It automatically discovered historical `.test.cjs` snapshots stored during the repair; the preserved pre-repair server correctly still contains the deliberate regression. This is a naturally discovered application/evaluation artifact-discovery problem, not a remaining production API defect and not automatically a meta-skill defect. No prior evidence was erased or rewritten. Exact command results, outputs, current-source hashes, and evidence snapshots are in `evidence/testing-663668aec49143059228272b66ded7fe/`. The failed documented verification command requires another real return to implementation, using the third and final allowed visit.

## Evaluation boundaries

This lane exercises one fresh-context full backend run, real native node delegation, in-flight pause followed by resume, two actual failed-test return edges, and three implementation visits within the saved limit. A fourth implementation dispatch was not attempted. Review-failure and exhausted-outcome conditions were checked only by static route evaluation; no actual review failure or attempts-exhausted run is claimed. Node-only trial and a second independent goal were explicitly omitted by the controlling evaluator because separate evaluation lanes cover those controls. This report makes no claim about their execution in backend-live.

## Final independent verification and outcome

**Completed; goal achieved.** Run `20260916T054313-b130ae4b` reached END with `tests_passed=true`, `review_passed=true`, `outcome=achieved`, and `inflight=null`. It used exactly eight authentic native node attempts: requirements 1, implementation 3, testing 3, review 1. No fourth implementation was attempted.

Implementation visit 3 changed only the README verification command to `node --test --test-reporter=tap todo.integration.test.cjs`, selecting the maintained suite while retaining all historical evidence. Independent testing visit 3 ran that exact command: exit **0**, **99 passed, 0 failed/cancelled/skipped**. Its evidence is `evidence/testing-a161589fb9474389b101ef28a5ebf729/`; the source-preservation and cleanup records show no application changes and closed listeners/child processes.

Independent review passed against the saved acceptance criteria. The reviewer additionally ran one focused real HTTP check for an interrupted false-to-true PATCH, closing a sensitivity gap in an existing same-value interrupted-upload fixture. That check exited 0 without changing the production code or maintained tests. The complete review and focused-check evidence are in `evidence/review-2cb0dbfa56ce49de9bcd9874d0d68796/`. The evaluator inspected the actual review and final checkpoint; no additional application audit was performed.

### Native node handles

| Node | Attempt | Native handle | Execution status |
| --- | --- | --- | --- |
| requirements | `1c283f941e4649118fd95fb93cd72262` | `/root/backend_installed/backend_executor/requirements_1` | success |
| implementation | `8373c5ea3aa241649641b8d1aaba91df` | `/root/backend_installed/backend_executor/implementation_1` | success |
| testing | `f7c609ae24f049ba98c89217b54ce462` | `/root/backend_installed/backend_executor/testing_1` | success |
| implementation | `5f1ddf27342c40c9ab0bc66e3bb86386` | `/root/backend_installed/backend_executor/implementation_2` | success |
| testing | `663668aec49143059228272b66ded7fe` | `/root/backend_installed/backend_executor/testing_2` | success |
| implementation | `5fd94f11edff426d9f2f1635b89799d9` | `/root/backend_installed/backend_executor/implementation_3` | success |
| testing | `a161589fb9474389b101ef28a5ebf729` | `/root/backend_installed/backend_executor/testing_3` | success |
| review | `2cb0dbfa56ce49de9bcd9874d0d68796` | `/root/backend_installed/backend_executor/review_1` | success |

All node execution statuses are success, including the two test visits whose domain result was failure. Their false test flags caused the recorded returns to implementation.

### Evidence map

- Generated execution entry: `.agents/skills/backend-development/SKILL.md`.
- Saved definition and Mermaid: `.agents/skills/backend-development/graph.json` and `GRAPH.md`.
- Immutable run, authentic results, and events: `.agents/skills/backend-development/runs/20260916T054313-b130ae4b/`.
- Raw final helper trace and actual command exit 0: `evidence/final-evaluation/trace.stdout.json` and `trace-command.json`.
- Compact verified final state, native handles, source hashes, and test totals: `evidence/final-evaluation/summary.json`.
- Complete controller command ledger: `evidence/executor-ledger.md`.
- Final helper status output: `evidence/controller/final-status.json`.
- Application and usage: `server.cjs`, `todo.integration.test.cjs`, `README.md`, and `requirements.md`.

No source meta-skill/helper defect blocked this run. The deliberate production regression and naturally discovered README/test-discovery issue were repaired through actual saved-graph transitions. Source skill code, source repository tests, and other evaluation projects were not modified by this lane.
