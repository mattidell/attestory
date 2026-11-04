# Repair: observe the launch assertion during the marker poll

Measured on the worktree whose parent is `67c7914e09c69371dc30be4400422b0d64e482af` on `milestone/chrome-lifecycle-race-2025`. Node `v22.23.2`, 10 CPUs. Counts are in `repair-counts.json`.

The shared fake's `const setup` declaration is unchanged. It still writes the complete JSON to a sibling temp file and renames that sibling onto the marker. The prior natural and injected series in `after-counts.json` stay applicable. This repair does not repeat that matrix.

## Fix

In `tools/presentation_harness/tests/chrome-lifecycle.test.mjs`, `assert.rejects` still attaches to the launch before the marker poll. The promise it returns is observed on that same turn. The handler records fulfillment or rejection and does not throw. `finally` disposes the owned launch, awaits that observation, and then surfaces the recorded mismatch. When the marker read and the assertion both fail, the error is an `AggregateError` carrying both. A marker failure no longer discards the assertion mismatch.

The cancellation half still uses `launchTimeoutMs: 5000`, 100 polls, and 20 ms. The file's other launch timeouts remain 5000 and 1500. The success path still asserts that the profile is absent and the pid is `ESRCH`.

## Regressions

Both call actual `launchChrome` with `launchTimeoutMs: 5000`. Their marker polls are 50 by 20 ms, inside that allowance. An idle probe saw the fake's owner fact about 321 ms after `launchChrome` was called, so a shorter poll expired before the process had published it. Each case is a child `node --test`. The parent requires `failureType: 'testCodeFailure'`, no unhandled rejection, no late asynchronous activity, and cleanup of the real profile and process.

- Early non-cancellation: the fake writes an owner fact and exits 7 without a marker. The launch rejects during the poll. The child fails with an `AggregateError` whose leaves are the marker `ENOENT` and the assertion mismatch for `exited before readiness (code=7, signal=null)`.
- Poll expiry: the fake writes an owner fact and stays alive. The poll ends while the launch is still pending. The child fails with the marker `ENOENT` only. Disposal then satisfies `/launch cancelled/`.

## Loaded check

From the repository root:

```sh
node docs/phases/engineering-health/milestones/chrome-lifecycle-race-evidence/repair-probe.mjs
```

That command runs:

```sh
node --test tools/presentation_harness/tests/chrome-lifecycle.test.mjs
```

Load was four foreground children:

```sh
node -e 'let x=0;for(;;){x=(x+1)|0}'
```

They were killed by those exact pids. The test process was a group leader and was signalled by that group only while it was still running. There was no process-name search.

Result: code 0, tests 6, pass 6, fail 0, `unhandledRejection` false, `lateAsync` false, 4656 ms. After the load children were reaped, `load_alive_after_stop` was 0.

## Gates

- `python3 -m pytest tests/test_presentation_chrome_lifecycle.py`: 1 passed in 21.27 s. The wrapper timeout is still 30 s.
- `python3 -m mypy`: success, 452 source files.
- `python3 tools/governance_lint.py`: `governance lint: conformant`.
- `python3 -m pytest -m "not live"`: 1645 passed, 8 skipped, 3826 subtests passed, in 16.47 s. This run did not reproduce the earlier fast-lane budget failures. The budget constant was not changed.
- `python3 tools/envelope_scan.py --range origin/main..HEAD` was run before this commit and exited 0. That range did not yet contain this repair.

## Left untouched

`packages/derivation/live_viewing.py` and the harness acceptance of a torn browser path are unchanged. `chrome-observation.test.mjs` still holds the promise from `assert.rejects` across its grace wait before awaiting it. No kernel, derivation, schema, content, or proposal file was edited. Nothing was pushed.
