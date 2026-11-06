# Exact browser-resource diagnostics

## Object and limits

The owner-directed diagnostic unit on core v78 attaches
the observer to the actual shared-browser launch inside
`tests/test_chrome_test_resources.py::test_node_browser_resource_controls`.
It does not repair or explain CI run 42162291620. That run recorded a 20,092 ms
launch and then exceeded the unchanged Python 30-second subprocess timeout;
the launch lacked an observer. Its three unrelated traced correction launches
and later fast probes cannot establish why this launch was slow.

No timeout, retry, existing assertion, marker or budget was changed. The
observer is absent unless `DEMO_CHROME_TRACE` is set. This fixed
`resource-controls` label opts into progress with diagnostic grace exactly zero.
Legacy observers still emit their original single final record.

## What the instrument observes

Fixed stage names cover launch, CDP connection, context creation, target loads,
isolation assertions, disposal, child readiness/reaping, actual borrowed-client
error/wait paths, browser-close rejection and cleanup. Stages and snapshots use
observation-lifetime milliseconds; startup fields retain the existing active
launch clock and separately recorded queue time. Samples retain active-launch
`ms`, lifetime sample gaps and sampling duration; poll count and maximum poll
gap expose delayed observation without identifying its cause.

An unreferenced two-second timer persists progress during later waits. Startup
polling starts samples asynchronously, so diagnostic sampling/writes are not
awaited by this opt-in test path. One write and one sampler may be outstanding;
only the latest dirty snapshot is retained, not an unbounded promise queue.
Closing clears the timer, refuses further stages and discards pending sample
results. A write already in flight may finish and at most its bounded dirty
snapshot follows. `flushed()` is for diagnostic tests, not a new wait in the
resource test. Failed progress I/O stops further writes without printing errors
or changing the original test result. Crash-time durability is best effort:
data already appended survives a Node kill; an in-flight final write can be
partial and an unavailable or stalled filesystem cannot guarantee a record.

Per observation: at most 32 stages, 32 file-state transitions, 40 samples and
64 progress records, each at most 65,536 bytes before newline (at most about
4 MiB appended). Labels/stages are allowlisted. Browser output, endpoints,
paths, command lines, DOM, environment values and process IDs are not recorded.
Large-stderr verification uses synthetic `demo.*` content and the existing
bounded launcher byte/category retention.

On Linux root counters remain separate from descendant aggregates. Descendant
discovery follows only the launched root's per-thread children files, not a
system-wide process scan: at most 64 process identities, 64 task entries per
process, 256 reads and 8 KiB per stat/status/children read. Truncation, exit races
or exhausted bounds make `complete` false. Unknown RSS stays null. Summed RSS
double-counts shared pages. Tree tick totals include only currently visible
processes: exited-child CPU can disappear, so successive totals are not a
cumulative process-tree CPU account. Tick-to-second conversion is unavailable
(`tick_seconds: null`), not guessed. Existing cgroup memory/PID fields describe
the shared cgroup, not this root or tree. No host CPU is attributed to Chrome.

`sampling_interval_process_cpu_us` is Node process CPU consumed during the
sampling interval, including unrelated event-loop work while file I/O awaits;
it is not isolated observer overhead. This macOS run has no `/proc`, so root
and tree process counters are explicitly unavailable, not zero. CPU-work and
timer-delay synthetic calibration verifies timing and that unavailable state
locally; its conditional Linux tick comparison has not executed on this host.

## Reproduction and preliminary measurements

Driver command (repository-relative ignored output):
`node tools/presentation_harness/chrome-resource-probe.mjs temp/lattice-rebuild-p0/chrome-resource-v78`.
It invokes the exact pytest wrapper with normal workers, retaining its original
30-second Node subprocess timeout. The outer diagnostic subprocess has 55
seconds, a driver kill at 60 seconds, and a 300-second total experiment cap.
Each loaded execution owns four foreground-driver-managed Node CPU burners,
each bounded to 40 seconds, killed/reaped in `finally`. Its subprocess groups
are also killed after completion so a wrapper timeout cannot leave its owned
descendants behind. No shell-background workers or process-name searches.

The preliminary seven executions (one untraced control, three no-burner,
three loaded) all passed, with 297–376 ms readiness and 7.63–8.32 seconds
wrapper elapsed. They overlapped synthetic observer tests, so they are not a
clean isolated/load comparison. Their initial instrumentation predates the
metric/clock/close refinements; they are not attributed to the final source.
They are not silently attributed to the final source or used as isolated
observer overhead. `RUSAGE_CHILDREN` CPU deltas cover reaped pytest descendants,
not the four separately owned burners, and are not isolated Chrome CPU.

## Verification and preserved failures

Initial observer tests: 16 passed, one failed because the new test cancelled
the fake before its marker existed. The setup now waits for both marker and
unfinished-progress evidence, retaining the same cancellation/cleanup checks.
The three new cases then passed. Final focused Node command includes
`chrome-observation.test.mjs`, `startup-coordinator.test.mjs`,
`shared-browser-context.test.mjs` and `correction-owner.test.mjs`: 25 passed
in 26.44 seconds. This includes untraced actual-browser behavior, original
resource assertions, legacy records, zero-grace unfinished startup, large
stderr, safe progress bounds, I/O-failure success/timeout cleanup and calibration.

`python3 -m pytest tests/test_chrome_test_resources.py`: 10 passed in 29.17 s.
Final tracing-enabled exact Python wrapper: one passed in 7.40 s. Repository-wide
`python3 -m mypy`: passed 461 source files.

First fast-lane command `python3 -m pytest -m 'not live'` overlapped the complete
Python resource-module command above. It completed in 22.08 s: 1662 passed,
8 skipped and one failure at
`tests/test_incremental_lattice.py::test_registry_phase_rejects_nondefault_standard_validator_runtime_policy`:
3.5 s exceeded the unchanged 3.0 s fast-lane budget. This is preserved as a
verification failure, not waived or assigned an established cause. No kernel
test/budget change was made. The foreman requested one isolated fast-lane
comparison after all resource/calibration children had ended.

That isolated comparison also failed the same nodeid: 3.2 s > 3.0 s;
1662 passed, 8 skipped, one failed in 17.56 s. No other test/probe overlapped.
At that handoff this remained a fast-lane failure requiring separate disposition,
not evidence that the first failure was solely resource-test contention.
There was no further fast-lane retry or kernel/test/budget edit.

No full suite was repeated. Independent review and exact-head CI remain gates;
local fast startups do not explain the prior runner timeout.

## Final frozen-source isolated/load comparison

After all other test/probe processes ended, the approved final matrix ran alone:
`node tools/presentation_harness/chrome-resource-probe.mjs temp/lattice-rebuild-p0/chrome-resource-v78-final`.
All five measured source hashes matched before/after the matrix. Documentation
commits advanced the parent without changing the instrument. No source edit occurred
during this matrix, and no broad verification was repeated afterward.

| Mode | Iteration | Elapsed seconds | Waited descendant CPU seconds | Startup ms | Cleanup ms |
| --- | --- | --- | --- | --- | --- |
| Trace off, no burners | 1 | 8.341921 | 13.661660 | unavailable | unavailable |
| Traced isolated | 1 | 7.574265 | 13.556732 | 299 | 134 |
| Traced isolated | 2 | 7.588865 | 13.497709 | 299 | 192 |
| Traced isolated | 3 | 7.572345 | 13.535797 | 296 | 180 |
| Traced, four burners | 1 | 7.537165 | 13.296490 | 307 | 228 |
| Traced, four burners | 2 | 7.800632 | 12.998705 | 332 | 87 |
| Traced, four burners | 3 | 7.523483 | 13.352672 | 301 | 212 |

All seven passed, with zero wrapper timeouts. All six traced runs persisted
25 records and reached `cleanup_finished`; 1,223–1,555 ms elapsed after readiness
through the remaining browser/client work and cleanup. Cleanup here is the
explicit cleanup-stage duration, not all browser shutdown (the explicit
`Browser.close` operation occurs earlier). Maximum startup poll gaps were
27–31 ms. Every driver-owned process group was killed after its run; every
burner was terminated/reaped in `finally`. Burner CPU is not included or
measured. Four burners on this ten-CPU macOS host do not recreate a particular
CI runner's contention, storage or cgroup state.

The control was slower than these isolated traced runs, but one sequential
control and three traced observations do not isolate instrumentation overhead
or establish a speedup. Only 296–308 microseconds of Node process CPU happened
inside recorded sampling intervals in these isolated runs (257–362 across all
six), which is neither a complete overhead measure nor Chrome CPU. Progress
I/O, timer effects and different scheduling remain possible influences.
Root/tree CPU counters remain unavailable on macOS. The observed result is
bounded diagnostic coverage and non-reproduction, not a CI cause or repair.

## Independent-review P2 reader repair

After the guard-test setup repair, the probe's whole-file `map(JSON.parse)` was replaced by
linewise recovery. A malformed or partial final append no longer discards
earlier complete records. Output distinguishes `trace_status` values `read`,
`missing`, `unreadable` and (control only) `disabled`, an allowlisted read-error
code, a numeric malformed-record count, and separate incomplete/unterminated
tail flags. An invalid undelimited final line is treated as potentially
incomplete; a valid undelimited final object is retained but still marked
unterminated. Complete malformed lines are counted and skipped; later good
records remain usable. No partial text, error message or trace locator is
included in these flags. Trace contents remain the existing sanitized observer
format, not a new arbitrary-data publication channel.

The driver is now importable without running an experiment, allowing the
permanent observer test module to test its actual parser. Focused regressions
cover two complete snapshots plus a partial third, malformed complete lines,
invalid record shapes, a valid undelimited record, empty/other-label input,
missing files, unreadable directory input and file-backed partial recovery.
Synthetic private markers in rejected bytes and paths do not appear in results.

`node --test --test-name-pattern='resource trace'
tools/presentation_harness/tests/chrome-observation.test.mjs`: three passed
in 60.80 ms. `node --check tools/presentation_harness/chrome-resource-probe.mjs`
passed; mypy passed 461 source files. No browser, load matrix, fast lane or full
suite was repeated for this reader-only repair. Prior matrix/source hashes
retain their historical provenance; this change does not revise those timings
or resolve the CI failure's cause. The separate guard-test setup repair and
its passing isolated fast lane are recorded in `guard-test-cost.md`.
