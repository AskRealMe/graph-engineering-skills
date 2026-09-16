# Fresh-session skill discovery

Recorded on 2026-09-16. A separate Codex process was launched with the evaluation project as its working directory and no authoring conversation. It was asked to inspect only its supplied skill catalog, without running tools or modifying files.

The fresh session identified both skills and expanded their catalog aliases:

| Skill | Catalog path, anonymized |
| --- | --- |
| graph-engineering | `EVALUATION_ROOT/.agents/skills/graph-engineering/SKILL.md` |
| backend-development | `EVALUATION_ROOT/backend-live/.agents/skills/backend-development/SKILL.md` |

This establishes discovery; native execution is evidenced separately. The host truncated catalog descriptions to its skill-context budget, but retained the skill names and paths. The full instructions are available on activation.

The successful process used the app-bundled Codex CLI 0.154.0-alpha.6.2. An initial attempt with another installed CLI, 0.145.0, was rejected by the model service as too old. No user configuration or model selection was changed. The successful process returned exit code 0. The original JSONL events and Korean answer remain in the local evaluation evidence.
