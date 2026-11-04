<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engineering Health",
  "topic": "chrome-lifecycle-race",
  "status": "Closed. The lifecycle fake publishes its marker by renaming a complete document, waits for usable content, and observes the launch assertion immediately, cancelling and draining when that wait fails. A DevTools port is ready only as a whole decimal line. Deadlines, browserPath, and cleanup assertions are unchanged. The Python live viewer still accepts a partial port, and a torn browser path remains accepted.",
  "scope": [
    "deterministic Chrome lifecycle test synchronization and rejection handling",
    "audit equivalent marker/ownership reads in the presentation harness",
    "before/after execution under CPU load without weakening tests"
  ],
  "non_goals": [
    "no tax package, content or schema publication",
    "no timeout increases, test skips, retries or weaker assertions",
    "no change to kernel, derivation or parallel scope-answer work"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engineering-health/milestones/chrome-lifecycle-race.md",
      "docs/milestone-retrospectives/2026-10-31-chrome-startup-flake.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engineering-health/milestones/chrome-lifecycle-race.md"
    ],
    "review": [
      "docs/roles/qualitative-review.md",
      "docs/phases/engineering-health/milestones/chrome-lifecycle-race.md"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-11-04-chrome-lifecycle-race.md",
      "docs/phases/engineering-health/milestones/chrome-lifecycle-race.md",
      "docs/phases/engineering-health/engineering-health-roadmap.md#Current boundary and remaining work"
    ]
  },
  "retrospective": "docs/milestone-retrospectives/2026-11-04-chrome-lifecycle-race.md"
}
-->

# The Chrome Lifecycle Test Waits for Its Marker

Key: chrome-lifecycle-race. Phase: Engineering Health.
Branch: milestone/chrome-lifecycle-race-2025, based on merged PR #252.
No tax package, schema, or content ships. Scope-answer questions and core
v73 were a separate milestone and are not part of this result.

## Purpose

A lifecycle test must distinguish a Chrome process that is still starting
from one that has been cancelled or cleaned up. Its fake browser writes a
marker containing the process and profile it owns. Seeing that path exist
does not mean the writer has finished the document.

PR #251, shard 2, run 41578701868, failed this test with incomplete JSON and
a later unhandled launch rejection. PR #240's startup allowance is a
different defect. This milestone does not give the race more time.

## Contract

`tools/presentation_harness/tests/chrome-lifecycle.test.mjs` publishes the
fake marker by writing the complete JSON to a sibling and renaming that
sibling onto the marker path. The cancellation half of `live timeout and
cancellation clean process and profile` calls `drainOwnedLaunch`: the launch
assertion is observed on the turn it is created, the poll reads until the
marker parses or the existing budget ends, and `finally` cancels the owned
launch and drains that observation. A marker failure is kept together with
an assertion mismatch.

`waitForDevToolsActivePort` in `tools/presentation_harness/lib/chrome.mjs`
accepts a port only after a newline, and only when the port line matches
`^[0-9]+$` and parses as a positive integer. `browserPath` remains the
trimmed second field. Launch deadlines in the lifecycle file stay 5000,
1500, and 5000 ms. `CHROME_LAUNCH_TIMEOUT_MS` stays 45000. The profile-absent
and `ESRCH` assertions stay. Observer grace is unchanged.

## Evidence

Counts and commands: `chrome-lifecycle-race-evidence/p0-account.md`,
`chrome-lifecycle-race-evidence/after-account.md`, and
`chrome-lifecycle-race-evidence/repair-account.md`.

The injected 80 ms empty-file window, 6 idle runs and 4 loaded runs:

- Before the repair, 10 of 10 failed. Each failing test was `live timeout
  and cancellation clean process and profile`, with `SyntaxError: Unexpected
  end of JSON input` and a later unhandled readiness-timeout rejection.
- After the repair, those 10 runs passed. Incomplete JSON and unhandled
  rejection were both 0. Wall time stayed with the file's 1500 ms readiness
  timeout.

Unmodified publication passed 46 of 46 on both sides: 4 idle, 30 with 4
workers, and 12 with one worker per CPU. That pass rate does not establish
how often the old gap would appear on a CI shard. The open-then-immediate
write also passed its 6 counted runs on both sides. The injected rows are
what show the poll and the early observation. The rename is a separate
closure: once the committed fake publishes, the path appears with a complete
document.

The success-path matrix does not take poll expiry or a non-matching
rejection. Those paths are the lifecycle tests `early noncancellation during
marker poll is an ordinary failure` and `marker poll expiry while launch is
pending cleans up without a late rejection`. Both call real `launchChrome`
with `launchTimeoutMs: 5000` and a 50 by 20 ms poll. The recorded idle
probes required `failureType: testCodeFailure`, no unhandled rejection, and
cleanup of the real profile and process:

- Early non-cancellation: `AggregateError` with the marker `ENOENT` and the
  assertion mismatch for exit code 7, `duringPoll` set, profile absent, pid
  `ESRCH`.
- Poll expiry while the launch is still pending: the marker `ENOENT` only,
  `duringPoll` false, then disposal matching `/launch cancelled/`, with the
  same cleanup.

`chrome-lifecycle-race-evidence/repair-probe.mjs` ran the lifecycle file
under four foreground workers. Result: code 0, tests 6, pass 6, no unhandled
rejection, 4656 ms.

The port-line cases live in
`tools/presentation_harness/tests/chrome-observation.test.mjs`: `a complete
decimal port line keeps the advertised browser path`, `readiness waits for a
complete port line instead of a positive prefix`, `a stuck positive port
prefix is not an advertised port`, and `a digit prefix before trailing junk
is not a complete port line`. Before the parser change, bytes `9222` and
`9222xyz` followed by a path were accepted as ready. After it, a complete
line still keeps `browserPath`, a prefix that is later replaced resolves
only once the whole line is present, and the stuck prefix and the junk
prefix are not ready.

## Review dispositions

The first repair attached `assert.rejects` before the marker poll and
awaited that promise only in `finally`. That left a second-order hole. The
promise `assert.rejects` returns can reject while the poll is still waiting.
A launch that failed during the poll for a reason other than cancellation
rejected that promise with nobody handling it: `node:test` recorded
`failureType: unhandledRejection`. Disposal still ran. Because the marker
error was already set, `finally` could discard the assertion error and
report only the marker `ENOENT`.

The verified repair is `drainOwnedLaunch` in
`tools/presentation_harness/tests/chrome-lifecycle.test.mjs`. It calls
`assert.rejects` and attaches a non-throwing handler on that same turn,
before the poll's first await. The handler stores fulfillment or the
mismatch and does not throw. `finally` then cancels, awaits the observation,
and builds one error from the marker failure, a dispose failure, and the
assertion error. Two or more become an `AggregateError`. A marker failure
keeps the assertion mismatch. The two failure-path tests and the loaded
six-test run above are the record of that repair. The cancellation test
still reaches the profile-absent and `ESRCH` assertions inside the 5000 ms
deadline.

That is semantic acceptance of the repair. It is not an exact-head `verify`
result. Publication still waits on that check of the curated tree.

The fast lane after the port-line change reported 10 `fast-lane budget
exceeded` failures, 3.1 s to 4.7 s against `FAST_LANE_BUDGET_SECONDS` of
3.0, in `tests/test_ci_historical_ref.py`,
`tests/test_capital_gain_distributions_line7a_t3_presentation.py`, and
`tests/test_mortgage_borrowing_checksum_generator.py`. Those paths were
unchanged from the ratified line. The run does not establish an
infrastructure cause. The budget was not raised, and none of those tests
were marked live or retried as the fix. The later fast lane, recorded in
`chrome-lifecycle-race-evidence/repair-account.md`, passed 1645. It did not
reproduce the budget failures. No test was skipped, weakened, or retried to
obtain the lifecycle result. The budget constant stayed 3.0.

## Residuals

This milestone does not make every readiness reader wait for a finished
port line and a finished path.

`packages/derivation/live_viewing.py` `_wait_for_devtools` is unchanged. A
digit-only `DevToolsActivePort` buffer with no newline is a positive `int`,
so `9222` resolves without waiting for a newline. Trailing junk on that
line makes `int` fail and the loop wait out `BROWSER_START_TIMEOUT`. That
is a partial-port reader. Changing it is derivation work and was not done.

The harness parser and that Python reader both still accept a torn browser
path. `12345\n/devtools/bro` is enough: a newline and a whole decimal port
line, with no completeness check on the path. `browserPath` stays the
trimmed second field. The Python reader returns that torn path.

Adjacent lifecycle reads were audited and left in place. The early-exit
test and the 1500 ms half own the launch promise before they parse. Other
harness tests parse after the launch settles, retry `JSON.parse`, or treat
a marker path's existence as their own ready signal without deciding
`launchChrome`. None of those observations extends the port-line rule to
the Python reader or to a torn path.

## Outcome

The fake marker is published atomically, the cancellation half waits for
usable marker content, and launch and assertion outcomes are observed
immediately, with cancel and drain when the wait fails. A DevTools port is
ready only as a whole decimal line. Deadlines, `browserPath`, and the
profile-absent and `ESRCH` assertions are unchanged. The injected window
went from 10 of 10 failures to 10 of 10 passes. Unmodified runs stayed 46
of 46. The two failure paths and one loaded six-test run hold in the
recorded probes. The Python partial-port read and the torn browser path
remain outside this result.

[Retrospective](../../../milestone-retrospectives/2026-11-04-chrome-lifecycle-race.md).
