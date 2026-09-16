# Final revision: second normal goal reuse

Recorded on: 2026-09-16. Installed public develop revision supplied by the controlling evaluator: f1e83bb.

The controlling evaluator requested a second normal run of the same Word Summary skill using original.txt and a separate expected-count fixture of 3, without inheriting prior results, stopping at the user-response gate. This is a full graph run, not a node trial.

Natural-language test request, translated into English for this report: Run a new task with the same Word Summary skill, this time verifying the three words in original.txt. Start from new input without carrying forward prior execution results. Notify me when the user-confirmation stage is reached.

Refreshed generated resources through a no-behavior-change authoring apply from the updated public installed meta-skill. The saved graph specification was copied unchanged; prior runs were not migrated. Exact commands are in final-revision-commands.jsonl. Hash provenance is in final-revision-provenance.json and all prior run files were hashed before refresh in final-revision-prior-manifest.json.

## Independent initial state

No-op authoring diff was empty and definition version stayed 1e13f68ecffe0c2a. Generated helper SHA-256 changed from 81d20fae14f47155c453cb18835eb4c61648148639354a0742929fbca332dfbc to 36306827c3b32d8d3c153ab9dc7b3b831f319841e7bb96faed8a5360025329a7, matching the updated public installed helper. All 41 prior run files were unchanged immediately after refresh.

New normal run: 20260916T060457-7402ef9a. Starting checkpoint saved in final-revision-start-state.json: trial false, current read-source, step 0, attempts empty, visits empty, source_text empty, word_count 0, check_passed false, outcome pending, signal_path empty. Inputs point to original.txt and the separate expected-three.txt fixture. Prior count 5 and prior verification outcomes were not inherited.

## Fresh node execution and approval gate

Read-source attempt 65287c554ae24a8e9a56aaf337555fff was executed by actual bound native handle /root/controls_installed/reuse_read. It read original.txt and saved exact text alpha beta gamma with the trailing newline. Count-words attempt b01bebf6c0d44daeb5b196ae60c2bb7d was executed by separate actual bound native handle /root/controls_installed/reuse_count. It independently calculated 3 and saved summary.json. Authentic result files and evidence were inspected before finish.

Prepare then returned awaiting_input with the saved question: May I independently verify this word summary using the expected-count fixture? The gate checkpoint is preserved in final-revision-gate-state.json. No verification agent had been spawned at this point, and the evaluator was asked for an explicit reply with the new evidence.

Actual controlling-evaluator reply received: Controlling evaluator reply: Approve the independent verification of this new normal run against expected-three.txt. Confirm the new result is 3 and prior completed main/trial run files remain unchanged, then finish the separate final-revision reuse report. This is approval for this local test gate only.

Only after this reply was respond approve recorded and the independent verification worker dispatched.

## Final result and preservation

Verification attempt c8416dc983a549fab5f0b915721cf59a ran under actual bound native handle /root/controls_installed/reuse_verify. Its real evidence was calculated 3, reported 3, expected 3, passed true. The normal graph reached completed/END with word_count 3, check_passed true, outcome verified through Count verified. All three stages ran as separate native Codex subagents with genuine bound handles and authentic result files. No prior result or fabricated success advanced this run.

History now contains two completed normal goals on the same Word Summary graph: the earlier verified count 5 and this new verified count 3, plus the earlier separate node-only trial. The new start checkpoint proves independent defaults; final trace proves three new attempts and the actual evaluator approval.

All 41 files under the two prior run directories remain byte-for-byte unchanged after resource refresh and completion of the new run. Their state checkpoint SHA-256 values remain:

- Earlier main 20260916T054212-f1afdae9: 9d1f4573217c9d129b06fbc9d525b16914c20652ecb1809f03879af6f8b4a60c.
- Earlier trial 20260916T055641-61a31608: 43f0572823f2251840ef5be4a1a4041db8bc179fb67fea4c918de873b827cd34.

The graph definition is unchanged. Previous evaluation reports were preserved. No source files or installed package files were modified. RUN-07 is covered by a second normal goal on the refreshed final public installed helper. No defect was observed in this bounded reuse pass.

## Evidence

- final-revision-commands.jsonl: exact helper commands, exits, and full outputs.
- final-revision-provenance.json: final installed and generated helper SHA-256 equality.
- final-revision-start-state.json: independent default values and empty attempt history.
- final-revision-gate-state.json: actual awaiting_input before verifier dispatch.
- final-revision-trace.json: completed run, native handles, approval and route evidence.
- final-revision-history.json: two normal completed goals plus separate trial.
- final-revision-preservation.json: unchanged prior checkpoint hashes and all 41 prior files.
