# P0 account: the lifecycle marker race

Source: the unmodified lifecycle test at P0 on `milestone/chrome-lifecycle-race-2025`. Node `v22.23.2` on a 10-CPU machine. Counts are in `p0-counts.json`. The procedure is `p0-reproduce.mjs`.

The lifecycle test blob stayed `2d4fa22ba4b860ba823da0e6e127b3de55064e42`. Temporary marker instrumentation was restored before this commit. The test file diff is empty.

## Commands

From the repository root, each child ran:

```sh
node --test tools/presentation_harness/tests/chrome-lifecycle.test.mjs
```

The child environment dropped `DEMO_CHROME_STARTUP_DIR`, `DEMO_LAUNCHER`, `DEMO_CHROME_TRACE`, `NODE_OPTIONS`, `FORCE_COLOR`, and `NO_COLOR`. None of the first four were set in the parent. The last two were set together in the parent and produced an unrelated color warning when left in place, so the counted runs removed them.

CPU load was a counted set of foreground children, killed later by those exact pids:

```sh
node -e 'let x=0;for(;;){x=(x+1)|0}'
```

Each Node test was a process-group leader. The runner waited for it and killed that group from its recorded pid if the run exceeded 20 seconds. No run timed out. Load pids were signaled `SIGKILL` from the recorded list. A later check of those exact pids found none alive. An immediate `kill -0` after `SIGKILL` can still see an unreaped zombie; that check is not evidence the workers survived.

Unmodified runs used the committed `writeFileSync` marker publication. Injected runs replaced only the fake `setup` write for the duration of the run: `openSync` the marker, `Atomics.wait` for the stated number of milliseconds, `writeSync` the JSON, `closeSync`. The zero-wait series used that split with a 0 millisecond wait.

The counted unmodified rows and the zero-wait row came from one invocation that stopped before the 80 ms series, because a second edit saw the runner's own uncommitted test change and restored the file. The 80 ms rows are a second invocation. The 10-worker row is a third. `p0-reproduce.mjs` now replaces its own instrumentation, so one `full` run covers every row except `natural_load_all_cores` (`saturate`).

## Counts

| Series | Workers | Publication | Runs | Pass | Incomplete JSON | Unhandled rejection | Wall ms min / avg / max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| natural, idle | 0 | `writeFileSync` | 4 | 4 | 0 | 0 | 2274 / 2320 / 2387 |
| natural, load | 4 | `writeFileSync` | 30 | 30 | 0 | 0 | 2129 / 2220 / 2808 |
| natural, all cores | 10 | `writeFileSync` | 12 | 12 | 0 | 0 | 2341 / 2471 / 2730 |
| injected, no wait | 4 | open, then immediate write | 6 | 6 | 0 | 0 | 2156 / 2204 / 2269 |
| injected, 80 ms | 0 | empty file for 80 ms | 6 | 0 | 6 | 6 | 7004 / 7045 / 7148 |
| injected, 80 ms, load | 4 | empty file for 80 ms | 4 | 0 | 4 | 4 | 6962 / 7202 / 7712 |

Every 80 ms run finished `tests 4`, `pass 3`, `fail 1`. The failing test was `live timeout and cancellation clean process and profile`. The parse error was `SyntaxError: Unexpected end of JSON input`. After that test ended, the runner reported an `unhandledRejection` whose error was:

```text
InfraError: Chrome stayed alive without DevToolsActivePort before the launch timeout; stderr_bytes=26; stderr_categories=none
```

`stderr_bytes=26` is the length of the fake's `demo-unknown-private-value` stderr write. Wall time near 7 seconds matches the test's first 1500 ms readiness timeout plus the second launch's 5000 ms timeout. Two preliminary 80 ms runs, kept out of the table, failed with this same signature. No counted run reported a missing marker. No counted run failed a different test.

## What this establishes

The cancellation half of `live timeout and cancellation clean process and profile` in `tools/presentation_harness/tests/chrome-lifecycle.test.mjs` does the following in order:

1. `pending = launchChrome(...)` with a 5000 ms readiness timeout and no rejection handler.
2. `stat` the marker until the path exists, at most 100 times, with 20 ms between misses. The loop continues after every miss.
3. `JSON.parse` the file once.
4. `assert.rejects(pending, /launch cancelled/)`.
5. `cancel()`.

`writeFileSync` creates the path and truncates it before the bytes are written. A `stat` in that gap sees an empty file, and the loop treats existence as a finished document. `JSON.parse` of an empty or truncated document throws `Unexpected end of JSON input`. That throw happens before the rejection expectation and before `cancel()`. The launch keeps waiting and then rejects on the readiness timeout. The test function has already finished, so Node reports that rejection as unhandled.

The 80 ms publisher held an empty marker across the 20 ms poll. All 10 counted runs took that path. The observed rejection is the readiness timeout. `cancel()` is sequenced after the parse, and the thrown parse skips it.

Unmodified `writeFileSync` produced none of this signature in 46 runs: 4 idle, 30 with 4 workers, and 12 with one worker per CPU. The open-then-immediate-write split also passed all 6 runs under 4 workers. On this machine the unmodified gap stayed inside the 20 ms poll. That frequency under a CI shard is unmeasured. The same test emits the incomplete-JSON failure and the later unhandled timeout rejection as soon as `stat` can see the empty file.

## Audit of the same file

`early exit reports status and sanitized stderr, drains floods, removes profile` passes `launchChrome` straight into `assert.rejects` and reads the marker after that rejection. The fake writes the marker before exiting, and the read runs after the exit. This test kept passing while the marker write was delayed 80 ms.

The readiness-timeout half of the live test also passes `launchChrome` straight into `assert.rejects` and reads the marker after the 1500 ms rejection. It kept passing under the 80 ms delay.

`spawn failure and immediate cancellation release ownership` passes both launches straight into `assert.rejects`. It does not read a marker. It kept passing under the delay.

`correction client exposes only sanitized startup diagnostics` spawns the correction client. That client awaits `launchChrome` inside `try/catch` (`tests/helpers/correction_browser_client.mjs`). This test does not read a marker. It kept passing under the delay.

## Harness reads

`waitForDevToolsActivePort` in `tools/presentation_harness/lib/chrome.mjs` reads `DevToolsActivePort` and retries while the file is missing, unreadable, or not yet a positive integer port, until the launch deadline. Its `stat` records observer metadata after a read. That is the parser-readiness handling already present.

`tools/presentation_harness/run.mjs` and `tools/presentation_harness/chrome-startup-probe.mjs` await `launchChrome` on the ownership path. They do not read a fake marker. `tests/helpers/correction_browser_owner.mjs` awaits `launchChrome` inside `try/catch`.

Other marker readers, from the source, without a separate load run of those files:

- `tools/presentation_harness/tests/chrome-observation.test.mjs` attaches `assert.rejects` before its waits. Its marker `JSON.parse` runs after the launch promise settles.
- `tools/presentation_harness/tests/startup-coordinator.test.mjs` parses one marker after the launch rejection has settled, and its dead-holder loop retries `JSON.parse`.
- `tools/presentation_harness/tests/correction-owner.test.mjs` retries `JSON.parse` until the document parses.
- `tools/presentation_harness/tests/real-chrome-repair.test.mjs` waits until a fake marker path exists, then signals the child. That marker body is the text `started`. Its `profileReady` helper treats a `DevToolsActivePort` path existing as ready.

`tests/test_presentation_chrome_lifecycle.py` runs the Node file and has no separate marker read.

A partial `DevToolsActivePort` whose first bytes are digits can satisfy `Number.parseInt` before the line is complete. That residual is visible in the readiness parser. This run did not execute it.

## Smallest fix

Change `tools/presentation_harness/tests/chrome-lifecycle.test.mjs` only.

1. Publish the fake marker by writing the complete JSON to a sibling and `renameSync` onto `DEMO_MARKER`, so the path the test observes appears with a complete document.
2. Call `assert.rejects(pending, /launch cancelled/)` immediately after creating `pending`, before any marker wait.
3. Retry `JSON.parse` inside the existing poll (100 iterations, 20 ms). Call `cancel()` after a document parses. If the budget ends first, fail with the rejection handler already attached and dispose the launch.

The rename closes the empty-file window for every reader of `setup`. The early handler keeps a thrown read from leaving the 5000 ms timeout rejection unhandled. The parse retry covers a poll that currently falls through to a one-shot read. Leave `launchTimeoutMs`, the cleanup assertions, and `waitForDevToolsActivePort` as they are. This evidence shows the failure in the test's marker protocol. It does not show a production harness failure to repair first.

## Uncertainties

The unmodified gap's rate on a loaded CI shard is unmeasured. The historical CI log was not replayed. The spawn ledger is outside this assignment's committed paths, so this owner launch was not appended there.
