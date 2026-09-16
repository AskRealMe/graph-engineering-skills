# Graph Engineering Skills

Graph Engineering is a meta skill: Codex follows its instructions to create and edit other skills. Preserve the natural-language interface. Helpers may validate, render, and checkpoint files; they must not become a separate agent service or language-model runtime.

- Write repository documentation, skill instructions, issues, and pull requests in English. Respond to users in their requested language.
- Generated graphs execute work nodes through Codex subagents. Do not replace an actual delegation test with a scripted simulation.
- Keep all 60 requirements in `docs/requirements.md` traceable to tests and behavioral evidence. Distinguish helper tests from natural-language evaluations.
- Use isolated evaluation projects. Do not change unrelated projects or publish evaluation secrets/transcripts.
- Verify the skill installed from develop before promoting it to main. The user-facing develop surface is the installed skill and its generated graph, not a web page.
- Run `python3 -m unittest discover -s tests -v` after helper changes and the skill validator after instruction changes.

