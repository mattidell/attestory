# Retrospective — The Chrome Lifecycle Test Waits for Its Marker

## Result

The lifecycle fake publishes its marker by renaming a complete document,
then waits for usable JSON. The launch assertion is observed on the same
turn it is attached. Cancellation and drain still run when the wait fails.
A DevTools port is ready only as a whole decimal line. Deadlines,
`browserPath`, and the profile-absent and `ESRCH` assertions are unchanged.

An injected empty marker failed 10 of 10 counted runs before the repair and
passed 10 of 10 after. Unmodified publication passed 46 of 46 on both sides.
That natural rate does not measure how often CI would have hit the old gap.

## Lessons

Seeing the marker path exist is not a finished document. The old poll parsed
on existence, threw on the empty file, and skipped cancellation, so the
launch later rejected with nobody waiting.

Attaching `assert.rejects` does not observe the promise that call returns.
The repair records that settlement on the same turn, before the poll waits,
and keeps the mismatch after cancel when the marker also failed. The
success-path matrix never took poll expiry or a non-matching rejection.
Those regressions, and one loaded run of the lifecycle file, passed 6 of 6
after the repair.

A fast-lane budget miss on unchanged tests does not establish an
infrastructure cause, and it is not a reason to raise the budget or to skip,
weaken, or retry a test. The first run failed 10 budget checks. A later run
passed 1645 with the budget still 3.0. Semantic acceptance of the repair is
separate from exact-head `verify`.

A whole decimal port line is not a finished browser path. The harness and
the Python live viewer still accept a torn path, and the Python reader still
accepts a digit-only port buffer with no newline.

## Cost

The record is two counted matrices, the port-line cases, two failure-path
regressions, and one loaded lifecycle run, plus the recorded wrapper, mypy,
and fast-lane gates. No kernel, derivation, schema, or content file changed.

## Follow-ups

The Python partial-port read and the torn browser path stay outside this
milestone. Neither is selected next. Exact-head `verify` on the curated tree
remains the publication gate.
