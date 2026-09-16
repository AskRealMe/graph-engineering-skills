# Installed Graph Engineering management evaluation

Evaluation date: 2026-09-16 (Asia/Seoul). Tested installed source revision: **78cf349**, as supplied by the controlling evaluator. No source repository, tests, or plans were inspected. Only the installed skill, its authoring/contract/operations/execution references, helper help, and artifacts within this evaluation project were read. No original source was patched or published.

## Result

The requested management sequence passed: project connection; unsaved proposal; graph creation with a user approval gate; listing/selection/rename; default agent configuration; shared reuse and graph-local adaptation with resources; node addition/removal/reordering/entry changes; typed language default and reads; condition and completion changes; independent clone; archive deletion with history; disconnection/reconnection; static route checks; and invalid-draft rejection without overwriting the working graph.

Two low-severity, actionable authoring/readability findings remain in this revision. They do not invalidate the tested graph's routing:

1. **Generated SKILL.md hides optional state/defaults.** The final graph has a typed `language` state with English/Korean choices and default English, and all five nodes read it. The generated root SKILL.md's Inputs section contains only required `goal`. Its instructions do require reading graph.json, so execution can recover the setting, but the human-readable entry point does not expose the language option/default. Evidence: generated SKILL.md (`EVALUATION_ROOT/management-live/.agents/skills/research-workflow/SKILL.md`) and definition (`EVALUATION_ROOT/management-live/.agents/skills/research-workflow/graph.json`). A separate shared-state/defaults section could expose this without mislabeling all intermediate state as user inputs.
2. **Removed owned node skill remains in the live nodes directory.** After notes was removed from nodes, edges, state, reads, and entry, the definition and Mermaid correctly omit it, but nodes/notes/SKILL.md (`EVALUATION_ROOT/management-live/.agents/skills/research-workflow/nodes/notes/SKILL.md`) remains. It is no longer part of the graph, but looks like a live runnable node when browsing skill files. Actual fresh-session discovery behavior was not tested. Archive a retired owned directory outside live nodes while preserving snapshots/history.

No helper internals were opened to diagnose these observable findings. No repair was made to the installed package or source.

## Scope and limits

This was a **management and static routing evaluation**, not a research execution. No node was prepared, delegated, or finished. No fact-check, user approval, source research, or saved research document was fabricated. The only run was an explicit history-preservation fixture that was started and immediately cancelled before dispatch; its attempts array is empty. A `route` result only shows what an already-supplied example state would select. In particular, the save-success fixture's path is sample data, not evidence that a file was saved.

Native Codex collaboration tools and the `default` role are available in the evaluation session's tool schema. Their presence was checked from that live schema; no worker was spawned. Doctor independently reports registration, paths, Python 3.14.7 and definition health, but explicitly cannot verify subagent availability. Generated skills are in the registered `.agents/skills` structure; actual indexing/reload in a fresh Codex session was not claimed.

## Concrete request sequence and outcomes

Requests 1–3 below are the evaluator-supplied Korean prompts verbatim. Later requests are tester-authored Korean continuations implementing the evaluator's specified sequence. These are evaluated conversation inputs, not additional real user messages or simulated approvals.

### 1. Connect and propose without saving

> 이 프로젝트에 연결해줘. 연결 상태도 확인해줘. 문서 조사 → 초안 → 사실 확인 그래프를 만들고 싶은데, 틀리면 초안으로 돌아가고 세 번까지 고치게 해줘. 지금은 저장 전에 구조를 보여줘.

Operations: connect, repeat connect to check idempotence, doctor, author a temporary specification, validate the specification only. Existing unrelated AGENTS.md text was preserved. The proposed graph directory did not exist after validation. Interpreted “three fixes” as at most three revisions after the initial draft: draft/check max_visits 4, explicit revision_count, and unsuccessful exhaustion outcome. Explained this interpretation before saving. The proposal was shown as a diagram and stored at 01-PROPOSAL.md (`EVALUATION_ROOT/management-live/01-PROPOSAL.md`); the unsaved specification is 01-proposal-unsaved.json (`EVALUATION_ROOT/management-live/drafts/01-proposal-unsaved.json`).

### 2. Add user confirmation and save the graph

> 사실 확인 뒤에 사용자 확인 단계를 넣고, 승인을 받아야 결과 저장 단계로 넘어가게 바꿔서 저장해.

Operations: create, validate, list, inspect generated SKILL.md/GRAPH.md. Result: five stages; fact-check success reaches user-confirm with a native `approval` gate, then save-result. The confirmation worker cannot approve itself. Exhaustion remains an unsuccessful END path. The graph, not a research result, was saved. Draft: 02-save-approved-workflow.json (`EVALUATION_ROOT/management-live/drafts/02-save-approved-workflow.json`).

### 3. Select, rename, edit drafting instructions and default role

> 그래프 목록에서 방금 만든 걸 골라 이름을 Research publishing으로 바꿔줘. 초안 작성 지침에는 근거 링크가 없는 주장은 빼라고 추가해. 사용 가능한 기본 서브에이전트 역할을 쓰게 해.

Operations: list, select displayed number 1, read saved graph.json, diff, validate draft, apply, validate saved graph. Name became Research publishing while stable ID remained research-workflow. Draft instructions now remove claims without supporting links. Every node uses `agent.type: default`, a role actually available in this session. No role/model was invented. Draft: 03-rename-default-agents.json (`EVALUATION_ROOT/management-live/drafts/03-rename-default-agents.json`).

### 4. Reuse an independent skill, then adapt locally

> 이 프로젝트의 독립 사실 확인 스킬을 사실 확인 단계에서 공유해서 쓰게 해줘.
>
> 이제 이 그래프 전용 복사본으로 바꾸고, 인용문과 저자 귀속도 확인하게 지침을 보강해줘. 원본 스킬은 그대로 둬.

Created an explicitly labeled synthetic fixture with an actual reference file: fixture SKILL.md (`EVALUATION_ROOT/management-live/fixtures/independent-fact-check/SKILL.md`) and source-review.md (`EVALUATION_ROOT/management-live/fixtures/independent-fact-check/references/source-review.md`). Shared mode stored the absolute original SKILL.md path. Copy mode created nodes/fact-check/SKILL.md and copied references/source-review.md. The local copy's instructions were adapted through a new full specification and apply. Original fixture SKILL.md and reference hashes remained byte-identical; the copied reference remains present and readable. No external/shared file was edited as a side effect. Evidence: original hashes (`EVALUATION_ROOT/management-live/fixture-original-hashes.json`); specs 04a, 04b, and 04c in drafts.

### 5. Add/remove notes, reorder, change entry, language and completion

> 조사 뒤에 메모 단계를 추가해줘. 메모를 맨 앞으로 옮겨 시작 단계로 바꾸고, 조사 다음에는 초안을 작성하게 해줘. 바뀐 구조를 보여줘.
>
> 메모 단계는 다시 빼고 조사부터 시작해줘. 작성 언어는 영어를 기본값으로 하고 한국어도 선택할 수 있게 해줘. 각 단계가 선택한 언어를 읽게 해줘. 사실 확인 통과 상태도 확인한 뒤 사용자 확인으로 보내고, 파일이 실제 저장된 경우에만 성공으로 끝나게 해줘.

Each change followed diff → validate draft → apply. Added notes and editorial_notes state, moved notes to the first node and entry with notes → research → draft, then removed notes, its edges/state/read dependency, and restored research entry. Every intermediate structure validated. Added language as a string enum [English, Korean], default English, propagated it to all five reads/instructions. Changed the approval branch to require both fact_check_passed true and outcome verified. Save-result reaches END only with saved true, nonempty saved_path, and outcome saved. The checker’s exhausted branch remains clearly unsuccessful. Notes-entry diagram: 05b-NOTES-ENTRY-GRAPH.md (`EVALUATION_ROOT/management-live/05b-NOTES-ENTRY-GRAPH.md`). Final diagram: 05c-FINAL-GRAPH.md (`EVALUATION_ROOT/management-live/05c-FINAL-GRAPH.md`). The leftover removed-node file is finding 2, not an active graph node.

### 6. Clone, select by number, archive and reconnect

> 그래프를 독립 초안으로 복제해줘. 목록의 1번을 골라 초안 지침만 따로 바꿔줘. 삭제 시 이력이 보존되는지도 확인한 다음, 삭제 미리보기를 보여주고 복제본을 삭제해줘. 프로젝트 연결도 끊었다 다시 연결하되 그래프와 다른 AGENTS.md 문구는 남겨줘.

Clone created research-draft without history. Listing showed clone as number 1 and original as number 2; selected number 1 and changed its drafting instructions. Original node text was unchanged. For the requested history-preservation check, created a run with the explicit fixture goal “History-preservation fixture; do not execute any work nodes.” and immediately cancelled without prepare/bind/finish. Confirmed cancelled status and empty attempts.

Delete dry-run retained the clone; delete then archived it and removed its live directory. The dry-run displayed a provisional random archive suffix, and actual delete used another suffix; actual archive path was verified from the final response. Every archived run-file hash matched its pre-delete value and history remains readable. Archive: research-draft archive (`EVALUATION_ROOT/management-live/.graph-engineering/archive/research-draft-a77edc18`). Run: cancelled state.json (`EVALUATION_ROOT/management-live/.graph-engineering/archive/research-draft-a77edc18/runs/20260916T054452-2d54836e/state.json`). The original graph remains.

Disconnect removed only the managed block. Reconnect restored the exact full AGENTS.md bytes. All original graph-file hashes were identical before/after disconnect/reconnect. The unrelated instruction “Preserve this unrelated instruction: keep source evidence links in published research.” survived. Final doctor succeeded.

### 7. Static routes and invalid-draft diagnosis/repair

> 정상·실패·조건 충돌·해당 경로 없음 상태로 이동 경로만 시험해줘. 잘못된 수정 초안도 진단하고 고쳐줘. 정상 그래프는 덮어쓰지 말고 실제 단계는 실행하지 마.

Tested the example states below. Complete structured inputs and outputs are recorded in routing-summary.json (`EVALUATION_ROOT/management-live/routing-summary.json`) and the command log.

| Example | Actual outcome |
| --- | --- |
| facts true, outcome verified | user-confirm |
| facts false, revision_count 1 | draft |
| facts false, revision_count 3, attempts_exhausted | END, unsuccessful business outcome |
| facts true, outcome working | exit 2: No route matched from fact-check; ask for clarification |
| saved true, nonempty example saved_path, outcome saved | END; static match only |
| saved false, empty path, outcome approved | exit 2: No route matched from save-result; ask for clarification |
| probe with two simultaneously matching fact-check routes | exit 2: Multiple routes matched from fact-check; ask for clarification |
| repaired probe with overlap removed | user-confirm |

The ambiguous graph was a separate clone, routing-probe. Its structurally valid but overlapping conditions passed schema validation and were correctly blocked at route evaluation. Removed the overlap and verified routing, then archived the probe. Archive: routing probe archive (`EVALUATION_ROOT/management-live/.graph-engineering/archive/routing-probe-229e11ba`). The working graph was byte-identical throughout.

Invalid drafts: language default 7 instead of string; undeclared research read; dangling edge to removed-notes. Both validate and apply rejected each with exit 2 and the specific diagnostics “Invalid default: language”, “research: invalid reads”, and “Dangling edge…”. Hash checks across the entire working graph proved it was unchanged after each rejection. Corrected drafts validate successfully and are retained as 07-repaired-*.json; no working definition needed replacement.

## Questions and authorization

No user clarification or extra approval was necessary for this authoring sequence. Target project and graph were unambiguous; three revisions was stated as an explicit interpretation; English default followed the local official-document rule; default agent existed; removal paths were specified by the sequence. The requested gate is a saved future execution requirement, not permission to fabricate user approval. No gate was exercised in this evaluation. The route tool's “ask for clarification” diagnostics are expected static test outcomes, so no real user question was required to continue the controlled test.

## Generated skill format and readability

Six active SKILL.md files were parsed with a YAML parser: root plus five node skills. All have valid frontmatter, matching lowercase/hyphen names within 64 characters, nonempty descriptions, Markdown bodies, and resolving relative resource links. All node patch declarations match declared writes. The root separates authoring from execution, links execution instructions, requires actual delegation/evidence, identifies all five stages, and names the required goal. Nodes give meaningful task-specific responsibilities and evidence contracts. The reused fact-check reference survives copying and local adaptation. GRAPH.md is exactly one Mermaid fenced block and contains only current graph nodes.

The imported fixture body adds a second H1 within the node document; this was introduced by the tester's authored instructions, is readable, and is not attributed to an automatic helper defect. The two actual usability findings are optional-state discoverability and stale retired-node files. This is structural/local readability validation, not a claim of fresh-session skill indexing or production runtime certification.

Machine-readable checks: format-structure-checks.json (`EVALUATION_ROOT/management-live/format-structure-checks.json`). Final helper validation: valid, 5 nodes, version c23851c14c665693. Final list contains only Research publishing and no active runs. Final doctor errors: [].

## Evidence paths

- Evaluation project: `EVALUATION_ROOT/management-live`.
- Installed skill tested: `EVALUATION_ROOT/.agents/skills/graph-engineering/SKILL.md`.
- Working generated skill: SKILL.md (`EVALUATION_ROOT/management-live/.agents/skills/research-workflow/SKILL.md`).
- Definition: graph.json (`EVALUATION_ROOT/management-live/.agents/skills/research-workflow/graph.json`).
- Diagram: GRAPH.md (`EVALUATION_ROOT/management-live/.agents/skills/research-workflow/GRAPH.md`).
- Project registration: AGENTS.md (`EVALUATION_ROOT/management-live/AGENTS.md`).
- Full helper operation log (73 commands at report time): evidence-command-log.jsonl (`EVALUATION_ROOT/management-live/evidence-command-log.jsonl`). Each entry includes exact argument array, exit code, full stdout and stderr.
- Authoring/repair/input fixtures: `EVALUATION_ROOT/management-live/drafts/`.
- Artifact-format checker: check_artifacts.py (`EVALUATION_ROOT/management-live/check_artifacts.py`).
- Archived clone history digest manifest: 06-history-hashes.json (`EVALUATION_ROOT/management-live/06-history-hashes.json`).

All files created or changed for this evaluation are inside the owned management-live directory. Findings are recorded against revision 78cf349; any later package changes require a separate focused retest.

## Frozen evidence before focused retest

After completing this report, the controlling evaluator authorized a separate f1e83bb retest in the same project. The complete generated graph from 78cf349 was copied, byte for byte, to `EVALUATION_ROOT/management-live/evidence/78cf349/research-workflow` before any refresh. Original graph paths above describe the location tested; use this frozen snapshot for the reported old SKILL.md omissions and stale notes artifact. The original command log and format checks remain unchanged.
