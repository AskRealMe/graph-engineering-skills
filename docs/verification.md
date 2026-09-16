# Verification

Recorded on 2026-09-16 (Asia/Seoul). Status: all 60 requirements covered; public main promotion and final workspace installation pending.

Graph Engineering is an Agent Skill that teaches an AI agent to create and edit graph skills. Codex is the first supported execution host. The helpers manage files and deterministic transitions; genuine native agents performed the work in the execution evaluations.

## Evidence and revisions

- The public develop skill was installed through the real `npx skills` CLI at `78cf349`. Independent evaluators used that installation and isolated local projects.
- The backend author generated a four-stage skill from a Korean request. A fresh-context orchestrator used only the generated skill and project inputs. The completed run used eight real native attempts and two failed-test returns to implementation. One failure was deliberately injected; the other was a naturally discovered documented-command issue. Final HTTP tests passed 99/99, independent review passed, and the parent reran the suite successfully.
- Management evaluation exercised 73 helper operations through natural-language requests. Two findings were fixed and independently retested with 13 operations against the published `f1e83bb` installation.
- Controls evaluation used 9 genuine native node attempts: fresh-context resume, approval, state changes, two actual missing-file errors, explicit retry, domain mismatch, rerun, native cancellation, inspected recovery, and an isolated trial. A second normal goal used three additional native attempts against the final skill revision; all 41 earlier run files remained unchanged.
- 31 deterministic helper tests passed locally on macOS with Python 3.14.7. These use synthetic handles and do not substitute for native-agent evidence.
- Real remote meta-skill updates preserved all 20 generated graph, cancelled-run, and registration files byte-for-byte. The final installed skill files matched the source manifest.

See [evidence descriptions](evidence/README.md), [exact skill hashes](evidence/skill-manifest.json), and the individual artifacts linked below. Local raw evidence retains full node inputs, result files, application artifacts, command outputs and native handles. Published evidence replaces home-directory paths with explicit placeholders.

## Requirement coverage

Each of the 60 requirements has an observed behavioral case and supporting helper checks where relevant. This is coverage of the requested capabilities, not a claim that every possible input or alternate model has been tested.

| Requirement | Observed behavior | Evidence |
| --- | --- | --- |
| SET-01 | Public GitHub install and fresh-session catalog discovery. | [Install/update](evidence/install-update.json), [discovery](evidence/discovery.md) |
| SET-02 | Repeated connect produced one managed block and preserved existing instructions. | [Management](evidence/management.md), [helper tests](evidence/helper-tests.log) |
| SET-03 | Doctor checked definitions/registration; native tools and fresh discovery were checked separately. | [Management](evidence/management.md), [helper tests](evidence/helper-tests.log) |
| SET-04 | Real remote updates changed only the meta skill; all 20 graph/history/registration files retained their hashes. | [Install/update](evidence/install-update.json) |
| SET-05 | Disconnect/reconnect preserved graph bytes and unrelated project instructions. | [Management](evidence/management.md), [helper tests](evidence/helper-tests.log) |
| CREATE-01 | Natural-language backend and research workflows became task-specific graph skills. | [Backend](evidence/backend.md), [controls](evidence/controls.md) |
| CREATE-02 | Generated failing-check branches return to implementation/draft with finite bounds. | [Backend](evidence/backend.md), [controls](evidence/controls.md) |
| CREATE-03 | Unsaved proposal was revised to add confirmation before creation. | [Management](evidence/management.md), [helper tests](evidence/helper-tests.log) |
| CREATE-04 | Root and node SKILL.md files, graph.json, GRAPH.md, initial state and execution resources were generated. | [Management](evidence/management.md), [helper tests](evidence/helper-tests.log) |
| CREATE-05 | A fresh Codex process discovered the generated backend skill; a fresh-context executor used it. | [Discovery](evidence/discovery.md), [backend](evidence/backend.md) |
| GRAPH-01 | List and numeric selection identified original and clone correctly. | [Management](evidence/management.md), [helper tests](evidence/helper-tests.log) |
| GRAPH-02 | Generated Mermaid and explanations matched saved entry, stages and conditions. | [Management](evidence/management.md), [helper tests](evidence/helper-tests.log) |
| GRAPH-03 | Renaming retained the stable graph ID and connections. | [Management](evidence/management.md), [helper tests](evidence/helper-tests.log) |
| GRAPH-04 | Clone had independent instructions and no inherited history. | [Management](evidence/management.md), [helper tests](evidence/helper-tests.log) |
| GRAPH-05 | Dry-run and archive deletion retained a cancelled-run record; active deletion was rejected in helper tests and a real installed-package check rejected a referenced graph. | [Management](evidence/management.md), [reference check](evidence/reference-deletion-check.json), [helper tests](evidence/helper-tests.log) |
| NODE-01 | Added confirmation, save and notes stages with skills and connections. | [Management](evidence/management.md), [helper tests](evidence/helper-tests.log) |
| NODE-02 | Draft instructions gained evidence and scope requirements. | [Management](evidence/management.md), [helper tests](evidence/helper-tests.log) |
| NODE-03 | Removed notes and repaired state/edges; updated package archived the owned retired node. | [Management retest](evidence/management-retest.md) |
| NODE-04 | Located and attached an independent fact-check skill. | [Management](evidence/management.md), [helper tests](evidence/helper-tests.log) |
| NODE-05 | Shared-to-copy adaptation retained resource files and original source hashes. | [Management](evidence/management.md), [helper tests](evidence/helper-tests.log) |
| NODE-06 | Selected the available default native role and inherited model settings; arbitrary model combinations are not claimed. | [Management](evidence/management.md), [helper tests](evidence/helper-tests.log) |
| NODE-07 | Declared typed results and downstream reads; native workers consumed prior output. | [Management](evidence/management.md), [helper tests](evidence/helper-tests.log) |
| FLOW-01 | Moved notes to entry, then restored research as entry. | [Management](evidence/management.md), [helper tests](evidence/helper-tests.log) |
| FLOW-02 | Added completion requiring saved output plus success flags; unsuccessful END outcomes remained distinct. | [Management](evidence/management.md), [helper tests](evidence/helper-tests.log) |
| FLOW-03 | Reordered stages and checked updated diagram and edges. | [Management](evidence/management.md), [helper tests](evidence/helper-tests.log) |
| FLOW-04 | Static paths and authentic backend test-failure routing selected the requested branches. | [Backend](evidence/backend.md), [controls](evidence/controls.md) |
| FLOW-05 | Natural-language limits were generated; boundary routes and deterministic exhaustion checks were verified. | [Management](evidence/management.md), [helper tests](evidence/helper-tests.log) |
| FLOW-06 | Ambiguous and unmatched routing returned explicit errors; repaired drafts routed normally. | [Management](evidence/management.md), [helper tests](evidence/helper-tests.log) |
| FLOW-07 | Native execution waited at a saved gate and proceeded only after an explicit evaluator reply. | [Controls](evidence/controls.md), [helper tests](evidence/helper-tests.log) |
| STATE-01 | Added language type/choices/default; latest generated skill exposes shared defaults separately. | [Management retest](evidence/management-retest.md) |
| STATE-02 | Missing required source input failed before dispatch; provided input enabled the run. | [Controls](evidence/controls.md), [helper tests](evidence/helper-tests.log) |
| STATE-03 | Native source, count and verification workers exchanged checkpointed output and evidence. | [Controls](evidence/controls.md), [helper tests](evidence/helper-tests.log) |
| STATE-04 | Status and STATE.md exposed paused, awaiting-input, failed and completed states. | [Controls](evidence/controls.md), [helper tests](evidence/helper-tests.log) |
| STATE-05 | Changed source input while paused; affected evidence was invalidated and recomputed. | [Controls](evidence/controls.md), [helper tests](evidence/helper-tests.log) |
| CHECK-01 | Invalid schema, undeclared read and dangling edge drafts were rejected; generated skill resources resolved. | [Management](evidence/management.md), [helper tests](evidence/helper-tests.log) |
| CHECK-02 | Diagnosed and repaired invalid drafts without overwriting the working graph. | [Management](evidence/management.md), [helper tests](evidence/helper-tests.log) |
| CHECK-03 | Diff and revised diagrams explained natural-language authoring changes. | [Management](evidence/management.md), [helper tests](evidence/helper-tests.log) |
| CHECK-04 | Example states evaluated routes without executing research work nodes. | [Management](evidence/management.md), [helper tests](evidence/helper-tests.log) |
| CHECK-05 | Edited definition and Mermaid stayed aligned; latest removed-node retest passed. | [Management retest](evidence/management-retest.md) |
| CHECK-06 | Paused run retained its snapshot; explicit compatible migration passed and completed-node change was rejected. | [Controls](evidence/controls.md), [helper tests](evidence/helper-tests.log) |
| RUN-01 | Generated backend skill ran an actual local HTTP API task. | [Backend](evidence/backend.md), [controls](evidence/controls.md) |
| RUN-02 | Backend goal/project inputs were inferred from its execution request; missing source input was diagnosed separately. | [Backend](evidence/backend.md), [controls](evidence/controls.md) |
| RUN-03 | Every backend and controls work attempt recorded a genuine native agent handle. | [Backend](evidence/backend.md), [controls](evidence/controls.md) |
| RUN-04 | Authentic results were validated, committed and routed from persisted state. | [Backend](evidence/backend.md), [controls](evidence/controls.md) |
| RUN-05 | Run state retained visits, attempts, step and waiting reasons. | [Backend](evidence/backend.md), [controls](evidence/controls.md) |
| RUN-06 | Reports distinguish ended execution, domain mismatch, errors and verified success. | [Backend](evidence/backend.md), [controls](evidence/controls.md) |
| RUN-07 | A second normal goal used three fresh native workers, produced count 3, and left all 41 earlier run files unchanged. | [New goal](evidence/controls-reuse.md) |
| CONTROL-01 | Pause was requested with a genuine in-flight worker and took effect before the next node. | [Controls](evidence/controls.md), [helper tests](evidence/helper-tests.log) |
| CONTROL-02 | Live cancellation required native interruption and terminal-handle evidence before settlement. | [Controls](evidence/controls.md), [helper tests](evidence/helper-tests.log) |
| CONTROL-03 | Paused backend and controls runs resumed from saved state. | [Controls](evidence/controls.md), [helper tests](evidence/helper-tests.log) |
| CONTROL-04 | Fresh-context orchestrator resumed from the generated skill and checkpoint without authoring history. | [Controls](evidence/controls.md), [helper tests](evidence/helper-tests.log) |
| CONTROL-05 | Two real missing-file errors exhausted the configured budget; explicit retry granted a new budget. | [Controls](evidence/controls.md), [helper tests](evidence/helper-tests.log) |
| CONTROL-06 | Missing-file execution errors differed from a completed count mismatch with a false domain flag. | [Controls](evidence/controls.md), [helper tests](evidence/helper-tests.log) |
| CONTROL-07 | Explicit reruns invalidated downstream results and retained prior attempts. | [Controls](evidence/controls.md), [helper tests](evidence/helper-tests.log) |
| CONTROL-08 | Interrupted work effects were inspected before recovery; committed-result replay was separately rejected by regression tests. | [Controls](evidence/controls.md), [helper tests](evidence/helper-tests.log) |
| TRACE-01 | History retained run goal, status and graph version across normal, cancelled and trial records. | [Controls](evidence/controls.md), [helper tests](evidence/helper-tests.log) |
| TRACE-02 | Authentic result files, input snapshots, native handles and existing artifacts were inspected. | [Controls](evidence/controls.md), [helper tests](evidence/helper-tests.log) |
| TRACE-03 | Saved routing events retained the evaluated state, conditions and selected path. | [Controls](evidence/controls.md), [helper tests](evidence/helper-tests.log) |
| TRACE-04 | Missing input, missing fixture, approval and finite retry exhaustion had specific explanations. | [Controls](evidence/controls.md), [helper tests](evidence/helper-tests.log) |
| TRACE-05 | A node-only trial used native delegation and its own run state. | [Controls](evidence/controls.md), [helper tests](evidence/helper-tests.log) |

## Boundaries

The supported scope is sequential nodes, branches, finite loops, explicit user gates, and saved-state controls on Codex with Python 3.10+ on macOS/Linux. Behavioral runs used the available default native role/model. Other hosts, Windows, parallel node execution, and every possible model override were not tested. One active execution per graph is enforced.

The actual gate workload used approval; decline has deterministic helper coverage. Native interrupted-worker recovery used retry; accepting an authentic retained result has helper coverage. A run reaching END is not proof of domain success, as demonstrated by the completed count-mismatch result. Cancellation preserves prior file changes and is not rollback.

Generated execution snapshots stayed pinned to their authoring revision. Later package fixes were validated through focused installed-skill retests and helper regression tests; the separate reuse run exercises the updated helper. The app-bundled Codex CLI discovered both meta and generated skills in fresh sessions. A separately installed older CLI was rejected by the model service; no user settings were changed.

GitHub Actions was not enabled because the connected credential could not publish workflow files. All recorded test results are local; no remote CI result is claimed.
