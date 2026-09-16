# Focused installed-package retest

Evaluation date: 2026-09-16 (Asia/Seoul). Revision: **f1e83bb**, supplied by the controlling evaluator. Result: **both previously reported behaviors are fixed for newly authored edits**.

Installed entry read: `EVALUATION_ROOT/install-lifecycle/.agents/skills/graph-engineering/SKILL.md`. Read its authoring, contract, and operations resources and helper help. No helper internals, source code, lifecycle graphs, or other evaluation artifacts were inspected or changed.

## Natural-language requests

1. “업데이트된 스킬로 Research publishing 안내를 새로 생성해줘. 작성 언어의 기본값과 선택지를 필수 입력과 구분해서 보여줘.”
2. “조사 뒤에 임시 메모 단계를 추가하고, 구조를 확인한 다음 그 단계를 다시 빼줘. 제거한 단계 파일은 이력으로 보관해줘.”

These are tester-authored concrete prompts implementing the controlling evaluator's focused request. No clarification was needed: existing target and removal replacement path were clear. No actual node work was requested or performed.

## Observed outcomes

- Refreshed the existing definition through diff, validate, and apply using the new installed helper. Semantic diff was empty. Generated SKILL.md now has distinct Inputs and Shared state sections. Inputs asks only for goal. Shared state displays `language` as string, default `"English"`, choices `["English", "Korean"]`, and explicitly explains that intermediate node results need not be supplied by the user. This resolves the original readability issue.
- Added `retest-note` between research and draft. Six-node validation passed, node SKILL.md existed, and Mermaid included Temporary retest note.
- Removed the temporary node and its state/edges, restoring research → draft. Five-node validation passed. Its live nodes/retest-note directory is gone. The complete node content was archived at `EVALUATION_ROOT/management-live/.agents/skills/research-workflow/.authoring-history/0675942e1ee142db954a5746b9361078/retest-note`; hashes match the pre-removal content exactly. Mermaid no longer contains the node. This resolves the removal behavior for newly removed owned nodes.
- The old nodes/notes orphan created by 78cf349 remains, as the evaluator anticipated. No broad retroactive cleanup was requested or inferred.
- Final graph.json and GRAPH.md are byte-identical to the pre-retest five-node definitions. All six active SKILL.md files still parse as YAML-frontmatter Markdown with correct names and descriptions. Project registration still has one managed block. The independent source fixture and earlier archived cancelled run remain byte-identical to their saved hash manifests.
- Final doctor has no errors. Final list contains Research publishing only, with no active run. No new test failure or helper error occurred in this focused retest.

## Provenance and limits

The installed meta SKILL.md hash is unchanged across the two revisions: `7382889ba9b389d79435932be4600dffbf1f188d427846dc051a97ce019822a9`. The new installed helper and regenerated local helper both hash to `36306827c3b32d8d3c153ab9dc7b3b831f319841e7bb96faed8a5360025329a7`. The previous installed helper hash was `81d20fae14f47155c453cb18835eb4c61648148639354a0742929fbca332dfbc`. This was an explicit evaluator-authorized refresh, not an implicit run migration.

The earlier revision's complete generated graph was frozen before refreshing at `EVALUATION_ROOT/management-live/evidence/78cf349/research-workflow`. Its report and 73-command evidence log remain available and distinct. The new retest log contains 13 helper commands. Native node trials were optional and omitted because this lane assesses management behavior and the controlling evaluator already covers full native runtime. This retest makes no claim about actual research, user approval handling during a run, or model output quality.

## Evidence

- Structured results (`EVALUATION_ROOT/management-live/retest-f1e83bb-results.json`)
- Exact helper arguments and output (`EVALUATION_ROOT/management-live/retest-f1e83bb-command-log.jsonl`)
- Installed file hashes (`EVALUATION_ROOT/management-live/retest-installed-hashes.json`)
- Refreshed SKILL.md snapshot (`EVALUATION_ROOT/management-live/retest-refreshed-SKILL.md`)
- Added-node diagram (`EVALUATION_ROOT/management-live/retest-added-GRAPH.md`)
- Final diagram (`EVALUATION_ROOT/management-live/retest-final-GRAPH.md`)
- Archived temporary node SKILL.md (`EVALUATION_ROOT/management-live/.agents/skills/research-workflow/.authoring-history/0675942e1ee142db954a5746b9361078/retest-note/SKILL.md`)
- Original revision report (`EVALUATION_ROOT/management-live/EVALUATION.md`)
