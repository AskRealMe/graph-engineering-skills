# Independent review

Recorded on 2026-09-16 (Asia/Seoul). Attempt: `2cb0dbfa56ce49de9bcd9874d0d68796`. Implementation round: 3.

**Verdict: pass.** No material issue remains against `requirements.md`. The exact assigned input has `tests_passed: true`; the inspected actual execution evidence supports that value. Proposed outcome: `achieved`.

## Implementation and contract

- **Runtime and lifecycle (AC-01):** `server.cjs:3–5` imports only Node built-ins. `server.cjs:127–128` creates an independent in-memory store, and `server.cjs:197–211` validates the configurable port, binds to loopback, announces success only after listening, and reports startup errors with a nonzero exit status. `todo.integration.test.cjs:302–369` exercises real child-process startup, restart, occupied-port failure, and cleanup. `README.md:9–15` documents startup and data loss on restart.
- **Representation and operations (AC-02/03):** `server.cjs:8–9,155–158` assigns a process-wide increasing ID with a random prefix, trims titles, initializes `completed` to false, and returns 201 with Location. `server.cjs:128,143–180` uses Map insertion order, changes only completion on PATCH, returns a bodyless 204 on deletion, and rejects missing items. Independent assertions at `todo.integration.test.cjs:113–160` cover exact fields, default false, Unicode, duplicates, stable identifiers/order, reversible completion, deletion, and no reuse.
- **Validation and mutation integrity (AC-04):** `server.cjs:49–125,149–171` counts buffered bytes, rejects bodies above 65,536 bytes, waits for complete uploads, validates media type before JSON, requires an object with exactly the allowed field, and validates field types before mutation. The maintained suite verifies rejected requests leave listings unchanged (`todo.integration.test.cjs:107–110,162–187`) and tests multibyte limits plus buffered/streamed rejection (`239–267`).
- **Routing and errors (AC-05):** `server.cjs:31–46,134–141` preserves exact paths, ignores queries, checks percent encoding, disallows decoded slashes, and checks route/method before body validation. `server.cjs:20–28,181–188` emits structured JSON errors with the correct media type, suppresses HEAD bodies, and avoids exposed stack traces. `todo.integration.test.cjs:189–236` covers these behaviors, Allow headers, missing IDs, and ignored GET/DELETE bodies.

## Actual verification and focused check

`README.md:68` documents `node --test --test-reporter=tap todo.integration.test.cjs`. Testing visit 3 executed exactly that command on Node v22.23.1, with actual exit 0 and no signal (`evidence/testing-a161589fb9474389b101ef28a5ebf729/run.json`). Its complete TAP footer at `stdout.txt:614–622` reports 99 tests passed, zero failed/cancelled/skipped/todo; stderr is empty. The suite uses actual loopback HTTP/TCP listeners and built-in modules (`todo.integration.test.cjs:3–10,17–60`). `cleanup.json` records refused connections for all 12 emitted ports and exited test/child processes, supplementing suite cleanup assertions.

The maintained interrupted-PATCH fixture sends false to a seed already false (`todo.integration.test.cjs:272–273`), so its unchanged-state assertion alone is not sensitive to an erroneous same-value commit. To close that evidence limitation without changing the maintained suite, this review ran a focused real-listener check that interrupts a false-to-true PATCH after the complete JSON value arrives but before the declared upload length is satisfied. The todo remained false, and a subsequent complete PATCH changed it to true. Listener/socket cleanup succeeded. `focused-run.json` preserves the exact command and actual exit 0; `focused.stdout.txt` and `focused.stderr.txt` preserve the output. No broad suite was rerun.

`integrity.json` independently verifies that all four reviewed application/contract files match both testing visit 3's recorded hashes and its source snapshots, and remained unchanged during the focused check.

## Failure and repair integrity

The second implementation visit's preserved diff changes only the deliberately regressed new-todo completion default from true to false. Its before/after command records show actual exits 1 then 0; the test hash is unchanged. This agrees with the original failure's explicit default-false assertion and the current `server.cjs:156`.

Testing visit 2 separately found a real documented-command discovery failure: the formerly documented unqualified `node --test` also executed historical test/source snapshots. Its raw failure points to `evidence/implementation-5f1ddf27342c40c9ab0bc66e3bb86386/before/todo.integration.test.cjs`, and its footer records 296/297 passed with exit 1. Implementation visit 3 preserved that evidence and changed only the README verification command to select the maintained suite explicitly (`evidence/implementation-5fd94f11edff426d9f2f1635b89799d9/change.diff`). The corrected command then passed in the separate testing visit 3. The historical failure is not reclassified or concealed.

## Scope and ownership

This independent native review inspected the assigned immutable skill, input, STATE, implementation, maintained tests, documentation, and attempt evidence. STATE records three implementation visits with failed testing routed back before this review; graph state commitment and visit accounting remain the controller's responsibility (AC-07). Review writes are confined to this attempt's evidence directory and assigned result JSON. No implementation, maintained tests, documentation, graph/helper/state, or historical evidence was edited. Persistence, deployment, authentication, broad security/performance audits, and other runtimes are outside the acceptance scope.
