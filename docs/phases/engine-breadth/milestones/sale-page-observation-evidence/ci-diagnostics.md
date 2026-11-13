# First CI failure and diagnostic iteration

Ready-event run [42333453979](https://github.com/mattidell/attestory/actions/runs/42333453979)
on the first curated v79 candidate failed the new live browser fixture during
collection after 200.96 seconds. Quick, precheck and the other three full-suite
shards passed. No page assertion ran in the failing fixture. The retained
JUnit message was browser-observation-failed; the observer's private trace was
not among uploaded artifacts. Neither startup failure nor a product defect is
established by that evidence.

The diagnostic change reports only closed-vocabulary Node failure stage,
category and reason, output byte counts and allowlisted existing launch
observer fields. The Python exception enters pytest.xml in the existing
always-uploaded shard artifact. Raw child output, URLs, paths, DOM and
environment are not forwarded. Launch deadlines, page waits, process cleanup,
all ten scenarios and their assertions remain unchanged. Diagnostic visibility
alone is not a claim that the original failure is fixed.

Builder checks: three focused diagnostic tests passed; Node syntax, whitespace
and configured mypy (469 files) passed. The single fast-lane run passed 1,677,
skipped eight and failed the following existing tests on the three-second
budget. These are observations, not infrastructure attributions or waived gates;
no retry, budget increase or unrelated repair was performed.

| Test | Seconds |
| --- | ---: |
| test_incremental_lattice.py::test_nested_exception_and_thread_context_cleanup | 4.7 |
| test_mortgage_borrowing_checksum_generator.py::MortgagePackageRebuildTests::test_build_is_independent_of_git_history_and_guards_base_bytes | 3.2 |
| test_ci_historical_ref.py::test_event_baselines[True-pr] | 3.0 |
| test_ci_historical_ref.py::test_converged_main_ui[False] | 3.1 |
| test_ci_historical_ref.py::test_event_baselines[True-pr-ui] | 3.0 |
| test_ci_historical_ref.py::DepthOneCheckoutTests::test_main_push_merge_uses_event_before_not_merge_parent | 3.6 |
| test_ci_historical_ref.py::DepthOneCheckoutTests::test_wrong_checkout_or_pr_base_is_rejected | 5.1 |
| test_ci_historical_ref.py::test_event_baselines[True-ui] | 3.0 |
| test_ci_historical_ref.py::test_converged_main_ui[True] | 3.3 |
| test_ci_historical_ref.py::DepthOneCheckoutTests::test_missing_historical_file_fails_closed | 3.2 |

Each listed file is under tests/. Rounded three-second durations still failed
the budget comparison. Final independent review and fresh exact-head CI must
judge the diagnostic candidate separately from earlier local passing checks.

Independent review exercised a real post-manifest synthetic Chrome failure:
the fixed stage/reason and launch exit status survived, arbitrary stderr/path/
URL sentinels did not cross, and the owned profile was cleaned. Review found
that invalid UTF-8 in the optional launch trace masked the primary diagnostic.
The repair treats it as unavailable; the reviewer independently confirmed that
the original reason/category/stage survives. Four focused diagnostic tests and
mypy (469 files) passed after repair; no whole-lane retry or browser recapture
was performed. The delta is independently accepted, not a claimed explanation
or repair of the original CI browser failure.

## Post-launch watchdog diagnostic on run 43365446465

Exact job [suite-shard (0), 131688890896](https://github.com/mattidell/attestory/actions/runs/43365446465/job/131688890896) ran commit `01af7aa596081024ba3149efc55c8b6e4a194bd3`. Its uploaded JUnit and launch trace show the Python subprocess watchdog firing after its existing 240-second bound: `browser-observation-timeout`, `stage=python-subprocess`, zero Node stdout bytes, and 88 Node stderr bytes. Chrome had `ready_accepted` after 6,193 ms and was still reported alive in the launch record; 1,626 Chrome stderr bytes had no recognized failure category. The artifact does not include raw Node stderr, a Node failure stage, or a page result. This establishes a watchdog timeout after Chrome readiness, not what the observer was doing or whether any model/page assertion ran.

A current closed-vocabulary Node record for `browser-cleanup-failed` at stage `cleanup` is exactly 88 bytes including its newline. The artifact does not identify that as the payload. A focused process reproducer wrote that valid 88-byte record to stderr and kept the child alive; `_run_bounded_subprocess` reported only the timeout and byte count, discarding the record. The supervisor now parses timeout-captured stderr as UTF-8 with replacement, retains only a Node record whose reason, category, and stage all pass the existing closed-vocabulary checks, and includes those three fields in the JUnit-safe message. It keeps the Python watchdog classification and captured byte counts. Raw child output is never attached to the exception or forwarded. The 240-second watchdog and its TERM/KILL cleanup windows are unchanged.

Focused verification passed all seven tests in `tests/test_sale_page_observation_diagnostics.py` in 1.14 seconds. The real Node child reproducer then reported `browser-observation-timeout`, 88 stderr bytes, and the safe `browser-cleanup-failed`/`cleanup`/`cleanup` fields, with no raw record retained. No full suite or browser recapture was run. The original CI failure remains an observation; this repair makes any completed safe Node record survive the Python watchdog, but does not identify or repair the underlying reason that job timed out.

Separately, source inspection found that `CDPClient.connect()` has no pre-open timeout or cancellation parameter. A focused fake-WebSocket probe remained pending after 25 ms and made no close call when the socket emitted neither `open` nor `error`. In the sale observer, the `await CDPClient.connect(...)` precedes its owned-resource `finally`, so such a stalled handshake would delay cleanup. This probe demonstrates the helper's behavior under a never-settling socket, not that run 43365446465 followed that path; the CI artifact has no Node stage. No shared CDP helper change is included in this charter. The normal cleanup path preserves an earlier error because `fail()` is first-write-wins; however, an exception in `client.close()` or Chrome disposal can skip later cleanup operations. That possibility was not reproduced, so no cleanup refactor is claimed.

## Owner-approved outer-watchdog follow-up

The Python observer bound is now 360 seconds, the owner-approved increase from
240 seconds. Chrome startup, per-step waits, and the two five-second TERM/KILL
cleanup windows are unchanged. The Node observer emits bounded JSONL progress
records with monotonic elapsed milliseconds and a numeric case index around
loopback/Chrome/CDP setup, each case start, page load, DOM read, per-case
cleanup, and outer cleanup. The Node process caps progress at 112 records and
uses a closed stage vocabulary; records contain no page, path, or environment
data. Its first closed-vocabulary failure record is written immediately when
set, before awaited case or process cleanup, and later cleanup failures do not
replace it.

The Python supervisor now captures pipe bytes. On a timeout it sends TERM,
waits the existing five seconds, then sends KILL and waits the existing five
seconds before parsing any captured JSON. This keeps malformed or deeply
nested input out of the cleanup path. It then retains only the first valid
closed-vocabulary error from stderr and the last valid progress record from
stdout. Parsing is bounded by total bytes, line bytes, and record count; bad
UTF-8, malformed JSON, and out-of-vocabulary fields are ignored. Successful
process output is decoded at the boundary with `surrogateescape`, preserving
valid text and round-tripping invalid bytes so captured byte counts remain
exact. Raw child output is not added to the failure message.

Focused verification passed all 11 diagnostic tests in 2.06 seconds. The real
timed child test emitted invalid UTF-8 beside the exact 88-byte safe failure
record and a progress record; the Python timeout retained both safe records
and counted every captured byte. A separate malformed/deep JSON case verified
that safe-record parsing occurs only after TERM and KILL. The focused module,
Node syntax check, whitespace check, and configured mypy (493 files) passed.
No browser recapture, broad suite, or CI retry was run. These checks establish
the watchdog and diagnostic behavior only: the exact stall in run 43365446465
remains unidentified, and this change does not claim to repair its cause.

## Owner-directed browser stress and v89 observation

On November 13, the existing saved v80 ten-page corpus was replayed directly
through the Node browser observer with fresh owned profiles and the normal
shared Chrome-startup coordinator. One direct Node replay took 3.265 seconds.
Twenty serial replays all exited successfully and reached `cleanup-complete`;
wall times ranged from 2.780 to 3.840 seconds, with 17 below three seconds.
Four simultaneous replays also all reached `cleanup-complete` and exited
successfully; wall times ranged from 4.942 to 5.948 seconds, with final Node
progress elapsed times from 4.770 to 5.869 seconds. None produced an error
record. The full Python v80 capture took about 67 seconds wall time, while the
ten coordinator runs summed to 31.157 seconds. The Node-only replays isolate
browser observation from Python case generation; they did not reproduce the
historic stall.

The ten-case core-v89 carry observation is recorded separately in
[`v89-reobservation.md`](v89-reobservation.md). Its actual coordinator, saved
page and Chrome path completed in all ten cases, with cleanup reported
complete. It records new unanswered v89 reasons and the same two parked
renderer alerts; it does not identify the former CI failure.

The Python outer watchdog is restored to 240 seconds. The v89 capture did not
justify a longer bound, and the local stress result is not a CI-cause
diagnosis. The exact prior CI run
[43510832698](https://github.com/mattidell/attestory/actions/runs/43510832698)
had successful quick and precheck jobs, including the fast lane and mypy. All
four full-suite shards were later cancelled, so it produced no observer stage
or page evidence; its verify dependency gate then failed. That cancelled run was left as historical evidence.

The real browser test remains marked `live` and is explicitly opt-in through
`SALE_PAGE_OBSERVATION_BROWSER=1`. With the variable unset,
`env -u SALE_PAGE_OBSERVATION_BROWSER python3 -m pytest tests/test_sale_page_observation.py -q`
reported one skipped test in 1.13 seconds. With the variable set,
`SALE_PAGE_OBSERVATION_BROWSER=1 python3 -m pytest tests/test_sale_page_observation.py -q`
ran the actual ten-case Chrome fixture and passed in 67.56 seconds. The gate
keeps the real browser test available while avoiding a browser launch in a
default direct module invocation.
