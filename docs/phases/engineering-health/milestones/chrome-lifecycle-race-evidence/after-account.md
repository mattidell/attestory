# After repair: marker publication and port-line readiness

Measured after the marker and port-line repair on `milestone/chrome-lifecycle-race-2025`, before the assertion-observation repair. Node `v22.23.2` on a 10-CPU machine. Counts are in `after-counts.json`. The procedure is the adapted `p0-reproduce.mjs`.

The lifecycle test blob stayed `1923a777872dfe88999f04972ab95d6c579ad5de`. Both runner invocations restored it (`bytesMatch` and `restoredMatch` true). The counted runs used that committed test and the committed readiness parser. The runner's setup matcher was not yet committed; it is the change that let the injected series run against the new setup body.

## Commands

From the repository root:

```sh
node docs/phases/engineering-health/milestones/chrome-lifecycle-race-evidence/p0-reproduce.mjs full
node docs/phases/engineering-health/milestones/chrome-lifecycle-race-evidence/p0-reproduce.mjs saturate
```

Each child ran:

```sh
node --test tools/presentation_harness/tests/chrome-lifecycle.test.mjs
```

The child environment dropped `DEMO_CHROME_STARTUP_DIR`, `DEMO_LAUNCHER`, `DEMO_CHROME_TRACE`, `NODE_OPTIONS`, `FORCE_COLOR`, and `NO_COLOR`. The first four were unset in the parent. The last two were set.

CPU load was a counted set of foreground children, killed later by those exact pids:

```sh
node -e 'let x=0;for(;;){x=(x+1)|0}'
```

Each Node test was a process-group leader. The runner killed that group from its recorded pid if the run exceeded 20 seconds. No counted run timed out. A later `kill -0` of every recorded load pid found none alive. The saturate report's immediate check, made in the same breath as `SIGKILL`, still listed its 10 worker pids. An immediate `kill -0` can see an unreaped zombie. That list is not evidence the workers survived.

The injector replaces the one current `const setup` declaration. It no longer looks for the old `writeFileSync` literal, so a change to the publication body does not skip the injected series. Natural rows keep the committed publisher. Injected rows still `openSync` an empty marker, `Atomics.wait` for the stated milliseconds, `writeSync` the JSON, and `closeSync`. A one-iteration idle probe of the natural row and the 80 ms row passed before the counted run. Those two runs are not in the table.

## Counts

Averages are the nearest integer, half up. The idle sum is 9426, mean 2356.5.

| Series | Workers | Publication | Runs | Pass | Incomplete JSON | Unhandled rejection | Wall ms min / avg / max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| natural, idle | 0 | rename of a complete sibling | 4 | 4 | 0 | 0 | 2340 / 2357 / 2378 |
| natural, load | 4 | rename of a complete sibling | 30 | 30 | 0 | 0 | 3055 / 3434 / 4014 |
| natural, all cores | 10 | rename of a complete sibling | 12 | 12 | 0 | 0 | 2408 / 2567 / 2693 |
| injected, no wait | 4 | open, then immediate write | 6 | 6 | 0 | 0 | 3412 / 3665 / 4240 |
| injected, 80 ms | 0 | empty file for 80 ms | 6 | 6 | 0 | 0 | 2430 / 2502 / 2579 |
| injected, 80 ms, load | 4 | empty file for 80 ms | 4 | 4 | 0 | 0 | 3370 / 3433 / 3500 |

Every counted run finished `tests 4`, `pass 4`, `fail 0`. None reported incomplete JSON, an unhandled rejection, or a missing marker.

P0's two 80 ms rows were 0/6 and 0/4, all 10 with `SyntaxError: Unexpected end of JSON input` and a later unhandled `InfraError: Chrome stayed alive without DevToolsActivePort before the launch timeout`. Those rows are now 6/6 and 4/4, and the wall time stays with the file's 1500 ms readiness timeout rather than that error's extra 5000 ms.

Natural rows are the committed publisher. Injected rows still expose an empty file for the wait. The injected passes are the cancellation half's usable-content poll and the rejection expectation attached before that poll. The rename is a separate closure: once the committed fake publishes, the path appears with a complete document, so a reader that only sees the path cannot observe an empty file from that publisher. Clean repetitions of the natural publisher do not, by themselves, show that the poll and the early expectation are present. The injected rows do.

## Lifecycle test

In `tools/presentation_harness/tests/chrome-lifecycle.test.mjs`, the shared fake writes the complete JSON to `DEMO_MARKER + '.tmp'` and `renameSync`s that sibling onto `DEMO_MARKER`.

The cancellation half of `live timeout and cancellation clean process and profile` now does this:

1. `pending = launchChrome(...)` with `launchTimeoutMs: 5000`.
2. `assert.rejects(pending, /launch cancelled/)` before any marker read.
3. Up to 100 parses, waiting 20 ms after each failure, stopping at the first object `JSON.parse` returns.
4. `finally` calls `cancel()` when ownership was handed over, then awaits the rejection expectation. A marker error is retained and rethrown after that drain. A rejection-expectation error is retained when the marker read succeeded.

The file's launch timeouts are still 5000, 1500, and 5000. The profile-absent and `ESRCH` assertions are unchanged.

The counted series takes the success path through that `finally`. The budget-expired path is the same `finally` with the marker error kept. An injected wait longer than the first half's 1500 ms readiness timeout throws on that half's one-shot parse before the cancellation half starts, so it does not measure the expired-budget branch. That branch was not given its own series.

## Port prefix before the parser change

Before the port-line repair, `waitForDevToolsActivePort` still used `Number.parseInt` on the first field. Four observation tests were run against that parser. One passed and three failed.

- `12345\n/devtools/browser/demo-path\n` resolved to `ws://127.0.0.1:12345/devtools/browser/demo-path`.
- Bytes `9222`, with a later replacement of the file, resolved to `ws://127.0.0.1:9222`. That execution replaced the file with `writeFileSync`. The committed test uses a sibling rename for the replacement. The failure is acceptance of the first four bytes, which happens before the replacement.
- Bytes `9222` left in place made `launchChrome` return success in about 321 ms.
- `9222xyz\n/devtools/browser/demo-path\n` made `launchChrome` return success in about 290 ms.

After the port-line repair the same four tests passed. The two files that never become a decimal port line took about 640 ms, recorded `not_ready_after_grace`, a malformed file state, no ready state, and `deadline_wall_ms >= 500`. The prefix that is later replaced resolved to `ws://127.0.0.1:12345/devtools/browser/demo-path`.

A port is accepted only when a newline has arrived, the port line matches `^[0-9]+$`, and `parseInt` of that whole line is a positive integer. `browserPath` is still the trimmed second `split("\n")` field. Existing fakes publish `12345\n/devtools/browser/demo-secret` and `12345\n/demo` with no second newline, and that shape still resolves. No port-range check was added. `CHROME_LAUNCH_TIMEOUT_MS` is still 45000. The existing late-readiness, grace-cancellation, and never-ready observation tests passed with the new rule. A leading `+` or a space-padded digit line falls outside the digit rule. No committed fake uses either, and neither had its own run.

## Adjacent marker reads

These readers are not the cancellation half's old existence-then-one-shot parse.

- The early-exit test and the live test's 1500 ms half pass `launchChrome` straight into `assert.rejects` and parse the marker after that promise settles. The early-exit read follows process exit. The 1500 ms read follows the timeout, so an 80 ms empty window has already closed. Both use the shared setup, which now renames a complete document. The 1500 ms half is still a one-shot parse. A publication slower than that timeout can still throw there. Its launch rejection is already owned.
- `spawn failure and immediate cancellation release ownership` does not read a marker. Both launches go straight into `assert.rejects`.
- `correction client exposes only sanitized startup diagnostics` does not read a marker. `tests/helpers/correction_browser_client.mjs` awaits `launchChrome` inside `try/catch`.
- `tools/presentation_harness/tests/chrome-observation.test.mjs` attaches `assert.rejects` before its waits. Its marker `JSON.parse` runs after the launch promise settles.
- `tools/presentation_harness/tests/startup-coordinator.test.mjs` parses one marker after rejection, and its dead-holder loop retries `JSON.parse`.
- `tools/presentation_harness/tests/correction-owner.test.mjs` retries `JSON.parse` until the document parses, 300 times at 20 ms.
- `tools/presentation_harness/tests/real-chrome-repair.test.mjs` waits until a marker whose body is the text `started` exists. `profileReady` treats a `DevToolsActivePort` path existing as ready. That helper does not parse port bytes and does not decide `launchChrome`. It was left unchanged.

## Derivation reader

`packages/derivation/live_viewing.py` `_wait_for_devtools` takes `int` of the first `splitlines()` field. Trailing junk raises `ValueError` and the loop retries. A digit-only buffer with no newline is a positive `int`. That file was not edited. A change there is derivation work and would require the full suite. This unit stops at the harness parser.

## Gates

- `node --test tools/presentation_harness/tests/chrome-lifecycle.test.mjs tools/presentation_harness/tests/chrome-observation.test.mjs`: 18 passed.
- `node --test tools/presentation_harness/tests/startup-coordinator.test.mjs tools/presentation_harness/tests/correction-owner.test.mjs`: 7 passed. Those fakes publish `12345\n/demo`.
- `python3 -m pytest tests/test_presentation_chrome_lifecycle.py`: 1 passed in 23.35 s. The wrapper timeout is still 30 s. It already runs the observation file, so the port regressions needed no wrapper edit.
- `python3 -m mypy`: success, 452 source files.
- `python3 tools/governance_lint.py`: `governance lint: conformant`.
- `python3 tools/envelope_scan.py --range origin/main..HEAD`: exit 0.
- `python3 -m pytest -m "not live"`, run with no other job: 10 failed, 1635 passed, 8 skipped, 3826 subtests passed, in 34.89 s. Every failure was `fast-lane budget exceeded` (3.1 s to 4.7 s against 3.0 s) in `tests/test_ci_historical_ref.py`, `tests/test_capital_gain_distributions_line7a_t3_presentation.py::ProductionShapedGoldens::test_three_dispositions_are_honest`, and `tests/test_mortgage_borrowing_checksum_generator.py::MortgagePackageRebuildTests::test_build_is_independent_of_git_history_and_guards_base_bytes`. Those paths are unchanged from `origin/main`. The same tests run as that set: 35 passed in 13.07 s. The budget was not raised, and none of those tests were marked live. This worktree was not switched onto `origin/main`, so the full fast lane was not re-run there.

## Left untouched

The plan Outcome, the spawn ledger, and the untracked `docs/proposals/2026-10-27-purpose-and-governance/` tree were not edited. No kernel, derivation, tax, schema, or content file was edited. Nothing was pushed.
