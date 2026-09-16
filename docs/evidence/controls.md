# Installed skill live controls evaluation

Recorded on: 2026-09-16.

Scope: installed skill only; all generated projects and evidence remain under this directory. No source or test changes.

## Initial natural-language request

“Create a tiny reusable Word Summary workflow: read local source text, count its words, and independently verify against an expected-count fixture. Ask me before verification. Preserve authentic per-attempt evidence. Missing fixtures are execution errors with two attempts; mismatches are completed false checks. Let a count worker wait on a signal so cancellation can be exercised.”

The controlling evaluator requested live native Codex subagents for every node. The helper only manages definitions and checkpoints.

## Required input and first live node

Natural-language request: Run Word Summary and pause after the source has been read; show me status. Starting without source_path failed with exit 2 and Missing required inputs: source_path; no node ran. Supplied original.txt and missing-expected.txt from the request. Main run: 20260916T054212-f1afdae9.

Attempt 057ecabf88ee4b66829cdca556d63952 was dispatched to real native handle /root/controls_installed/read_initial, immediately bound, then pause was requested while it was live. Authentic results and state are in the generated graph run.

## Paused edits and source replacement

Request: Rename the workflow, preserve the existing paused snapshot, explicitly migrate the compatible rename, then reject migration after changing a completed node instruction. The future graph changed from 1acc80d791a0e01d to 1e13f68ecffe0c2a while status still showed the original snapshot. Compatible dry-run and explicit migration passed. A changed completed read-source instruction produced exit 2: Completed nodes changed; start a new run or rerun before migrating. The future graph was restored to the compatible definition.

Request: Use revised.txt and update affected results before resuming. set-state reported the affected read-source result and recommended rerunning it. rerun invalidated the original attempt, restored the pre-node state, retained the revised source override, and paused at read-source. Exact helper commands, output and audit reasons are saved in commands.jsonl.

## Installed revision and scope

The controlling evaluator identified the installed public develop commit as 78cf349ebf642553ec06fe45f78d0695b8abfd95 and package hash 0aff8c0d327827eb0ea8df709cf2c7df4717a18bc1fbe9bb1a5d033ef195a544. Local SHA-256 evidence is saved in provenance.json. This evaluation continues against that pinned copy; no installed or source edits were made. The parent separately discovered recovery replay and same-second latest-run selection bugs; these are not claimed as findings from this lane. Every control here uses explicit run IDs.

## Actual user-response gate

Fresh-context runner stopped at awaiting_input before spawning verification. The saved question was: May I independently verify this word summary using the expected-count fixture?

Actual controlling-evaluator reply received via collaboration message: Controlling evaluator reply: Approve. Please independently verify this word summary against the expected-count fixture. I explicitly authorize this local test-stage execution, including the two bounded attempts if the fixture is absent.

Only after this reply was respond approve recorded. No worker output or silence was used as approval. See fresh-context-evidence.md for the new-context native attempts.

## Methodology caveat

The fresh runner read the ancestor graph-engineering-skills/AGENTS.md instruction file as well as project instructions. This exceeded the delegated no-source-repository-read scope for that ancillary instruction file. It reported no implementation/test/source-skill reads; all subsequent workers were explicitly restricted to controls-live. This caveat is kept separate from product behavior findings.

## Bounded execution errors and explicit retry

Both actual native attempts e031028a73ab4f4d82340080434893cf and 6d055c80f8c24a47b854206edf79feb6 opened the missing fixture and captured FileNotFoundError tracebacks. After the first finish the run remained running; after the second it became failed. A further prepare failed and did not create a third attempt.

Actual controlling-evaluator request: Create the missing local expected-count fixture with value 4, then manually retry the failed verification stage with a fresh bounded retry budget. Do not alter the actual source or computed count. Report the authentic mismatch as a completed domain check with check_passed false, not as an execution error or goal success. Afterward explicitly set expected count to 5 as a new test-user correction and run the requested chosen-node rerun (retaining history) to verify success. This message authorizes both sequential local evaluator actions. Continue cancellation/recovery and isolated trial afterward.

Created only the requested expected-count fixture with value 4 before the explicit retry.

## Completed false check and chosen-node rerun

Attempt 1c0a2cc7a69a4241b27cef43135ddd82 returned authentic status success, calculated 5, reported 5, expected 4, check_passed false, outcome mismatch. finish reached completed/END with the Count mismatch routing reason. The user goal was not reported as achieved. The complete checkpoint was saved as completed-mismatch-state.json before correction.

Following the explicit sequential evaluator request, corrected only the fixture to 5, reran verify-count, resumed, and encountered the saved approval question again. The actual evaluator message explicitly authorized both sequential local verification actions; its authorization was recorded in respond. No new approval was inferred from silence. The graph retained all prior attempt records and evidence.

## Successful corrected verification and isolated trial

Authentic corrected attempt 9d47f0ef5b9c400b87d6a5a8d8203ecd calculated, reported, and expected 5, so the main run completed with check_passed true and outcome verified via Count verified.

Natural-language request: Try only word counting, cancel its waiting worker, inspect the partial artifact, and safely retry. Created separate node-only trial 20260916T055641-61a31608 after normal graph completion. It has trial true, starts at count-words, and does not rerun the normal graph. The main checkpoint before the trial is saved in main-before-trial.json.

## Native cancellation and safe recovery

Trial attempt 1d7b12b0a93a49cd88d32cb0754c985c ran under actual bound handle /root/controls_installed/cancel_waiting_count. The worker wrote its token to waiting-marker.txt and announced it was waiting for resume.signal. The parent inspected the marker, called cancel (status stopping, inflight retained), then called the native interrupt tool. Its response was previous_status running. A separate native list_agents call then returned agent_status interrupted. Only after that terminal confirmation did settle record cancelled and clear inflight.

Inspected partial output before recovery: marker preserved, no success result, no signal. Evidence is cancellation-inspection.json. recover retry was then justified by the inspection and terminal confirmation, invalidating the interrupted attempt without deleting its artifact. Created the external retry signal and dispatched new actual handle /root/controls_installed/recovered_count for attempt d68d2a10e9a8454abe96ddaf3922f685. A timeout was never treated as termination and no success result was manufactured.

## Final outcomes and trace inspection

All seven requested control scenarios passed in this lane against the pinned installed copy. No new product defect was observed. The main workflow completed with actual verified word_count 5. The separate node-only trial completed with word_count 5; its untouched verification fields remain check_passed false and outcome pending because that node-only trial does not run verification. It is not reported as an independently verified complete workflow.

The main checkpoint was byte-for-byte unchanged by the trial; both SHA-256 values are saved in trial-isolation.json. History shows two distinct completed run IDs, one normal and one trial. main-trace.json preserves original and revised inputs, invalidated attempts, two genuine execution errors, real user responses, migration/state/rerun reasons, and both conditional route decisions. The false comparison selected Count mismatch after its true predicate evaluated false; the corrected comparison selected Count verified after the same predicate evaluated true. trial-trace.json preserves bound handles, stopping/cancelled transitions, terminal-inspection reason, interrupted attempt, recovery reason, and authentic retry result.

Artifacts were produced by native node agents. The evaluator wrote fixtures, graph definitions, checkpoint-control requests, and evidence reports only; it never manufactured node success. No publishing, source edits, or external effects occurred.

### Native worker handles

| Run | Node | Attempt | Native handle | Status | Valid |
| --- | --- | --- | --- | --- | --- |
| Main | read-source | 057ecabf88ee4b66829cdca556d63952 | /root/controls_installed/read_initial | success | false |
| Main | read-source | f93b374cbced42b989a4bea74b8ad1be | /root/controls_installed/fresh_resume/read_revised | success | true |
| Main | count-words | fd9596484d274c9ea4180d24b46c8f03 | /root/controls_installed/fresh_resume/count_revised | success | true |
| Main | verify-count | e031028a73ab4f4d82340080434893cf | /root/controls_installed/verify_missing_first | error | false |
| Main | verify-count | 6d055c80f8c24a47b854206edf79feb6 | /root/controls_installed/verify_missing_second | error | false |
| Main | verify-count | 1c0a2cc7a69a4241b27cef43135ddd82 | /root/controls_installed/verify_mismatch | success | false |
| Main | verify-count | 9d47f0ef5b9c400b87d6a5a8d8203ecd | /root/controls_installed/verify_corrected | success | true |
| Trial | count-words | 1d7b12b0a93a49cd88d32cb0754c985c | /root/controls_installed/cancel_waiting_count | interrupted | false |
| Trial | count-words | d68d2a10e9a8454abe96ddaf3922f685 | /root/controls_installed/recovered_count | success | true |

### Evidence entry points

- commands.jsonl: exact helper argument lists, exit codes, stdout, and stderr after graph creation.
- fresh-context-evidence.md: generated-skill-only resume, paths read, actual dispatches, gate stop.
- completed-mismatch-state.json: authentic completed false-check snapshot before explicit correction.
- cancellation-inspection.json: actual native terminal observation and partial-file inspection.
- main-trace.json, trial-trace.json, history.json: authoritative audit output.
- trial-isolation.json: normal-run checkpoint equality across separate trial.
- provenance.json: installed and pinned helper hashes.

Initial authoring commands before the logging wrapper: installed graph_ops.py --help; create --project controls-live --spec controls-live/spec.json; generated graph_ops.py validate --graph controls-live/.agents/skills/word-summary (valid true); start with missing-input.json (exit 2, Missing required inputs: source_path). The initial create and missing-input outputs were directly observed in tool results.

### Limits and observations

The approval branch was exercised with actual approve replies; decline was not required for this workload and was not tested. Recovery used retry after authentic interruption; authentic-result accept was not tested. The fresh runner initially treated --graph as graph.json and got two pre-mutation errors before correcting to the graph directory; it then completed from saved instructions. The controlling evaluator clarified that reading ancestor AGENTS.md is required project instruction context, not implementation/test or authoring-history access, so no replay was needed. Parent-reported helper defects and their later source fixes were outside this pinned-copy behavioral pass.
