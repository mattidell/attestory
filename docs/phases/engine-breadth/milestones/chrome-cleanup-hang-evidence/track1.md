# Track 1 evidence: Chrome cleanup does not hang CI

## Reproduction (before the fix)

A synthetic Chrome (`tools/presentation_harness/tests/helpers/fake-chrome-group.mjs`)
whose main process serves just enough DevTools protocol and starts a helper
process that (a) outlives the main process and ignores SIGTERM, (b) inherits the
main process's stderr pipe, and (c) keeps writing files into the profile.

- Observer (`sale-page-observation.mjs`) against it: prints `cleanup-complete`
  and then does not exit. Killed by an outer 25 s limit; helper still alive.
- `lib/chrome.mjs` `dispose()` against a profile the helper is writing to:
  rejects with `ENOTEMPTY` after about 150 ms.
- Control (corrected after review, CCH-R1): the builder reported that a helper
  which does not hold the stderr pipe let the old observer exit promptly. The
  fresh review could not reproduce that: with `stdio: ignore`, and in the
  `locked` mode with no helper at all, the old observer still hangs after
  `cleanup-complete`, and `process.getActiveResourcesInfo()` reports a
  `TCPServerWrap`. The cause is the old cleanup block: a rejected
  `chrome.dispose()` jumped past `server.close()`, so the loopback DevTools
  server kept the event loop alive. The held stderr pipe is not needed for the
  hang; the profile writes are what fail `dispose`.

The foreman's reading was half right: the profile writes fail `dispose`, but
the open handle is the server, not the pipe.

### Repair

The observer now closes its server whether or not `dispose()` succeeds, and
reports `cleanupCompleted` false if either fails. With the `process.exit`
backstop removed in a scratch copy, test 3 (an unremovable profile) passes on
the repaired sources; it failed before. The exit backstop stays. The stderr
`destroy()` is defence in depth: no test fails without it, so test 1 no longer
claims to check it.

## Fix

- `lib/chrome.mjs`: Chrome is spawned `detached` as the leader of its own process
  group. `dispose()` signals the whole group (SIGTERM, up to 3 s grace, then
  SIGKILL, up to 2 s wait), destroys the stderr stream, then removes the profile
  with a bounded retry (20 attempts, 100 ms apart, on ENOTEMPTY, EBUSY, EPERM,
  EACCES, EMFILE, ENFILE). A group that survives SIGKILL or a profile that stays
  unremovable makes `dispose()` reject, so the observer still reports
  `browser-cleanup-failed`.
- Because Chrome is no longer in its owner's process group, an exit hook kills any
  still-owned group on process exit, and a process with no signal handler of its
  own kills the groups on SIGINT, SIGTERM or SIGHUP and then dies by that signal.
  A process that already handles those signals (`run.mjs`, the correction
  owner) keeps its own cleanup path.
- `sale-page-observation.mjs`: calls `process.exit(process.exitCode ?? 0)` once
  `main` has finished, so the Python 240 s bound is never what ends a run. The
  progress and failure records are unchanged.
- All entry points that use `lib/chrome.mjs` (`run.mjs`, the startup probe, the
  correction owner, the entry probe) get the group handling from the library.

## After the fix

- Same observer repro: exit 0 in 4.6 s (3 s of that is the fake helper ignoring
  SIGTERM, which a real Chrome helper does not do), helper gone, profile removed.
  Before: no exit (25 s limit).
- Unremovable profile: observer prints `browser-cleanup-failed`, exits 2 in
  about 2 s (the retry window).

## Tests

`tools/presentation_harness/tests/chrome-group-cleanup.test.mjs`, also run from
`tests/test_presentation_chrome_lifecycle.py`:

- dispose ends the helper, removes the profile, and is bounded;
- the observer exits 0 promptly, helper dead, profile gone, `cleanup_completed` true;
- an unremovable profile gives `browser-cleanup-failed`, exit 2, prompt exit;
- an unremovable profile makes `dispose()` reject rather than hang.

Against the pre-fix sources the first three fail (ENOTEMPTY, and the observer
hung until the test's own guard) and the fourth passes, as expected.

`real-chrome-repair.test.mjs` fails when the whole Node test directory runs in
parallel, with or without this change (it compares the global list of profile
directories while other test files create profiles). It passes when run alone.

The Python real-Chrome tests (`tests/test_sale_page_observation_temp_paths.py`,
`tests/test_sale_page_observation_diagnostics.py`) passed three consecutive local
runs with real Chrome.

## Not covered

Only CI can show how often real Chrome produces the failure and whether this
removes it. The fake helper reproduces the mechanism, not the cause of a real
helper surviving. A SIGKILL of the observer itself (the Python bound's last escalation) cannot
run any hook. Before this change Chrome shared the observer's process group and
died with it; now it is in its own group and would survive that one path. The
Python bound's earlier SIGTERM is handled (the groups are killed first).
Record the next several `verify` runs at closeout.
