# Review: Chrome cleanup does not hang CI

Reviewer: fresh context. Object: `github/main..HEAD` on
milestone/chrome-cleanup-hang-2025 at `37a6374d` (four commits: plan,
fix `b135ca08`, evidence `e42b3841`, plan decisions and this charter).
Governance not read.

## Verdict

**READY with notes.** The fix stops the hang that CI reports and
cleans up every Chrome process the harness starts on macOS. Two
findings are Medium. CCH-R1 says the evidence names the wrong handle
as the cause of the hang. CCH-R2 says a second process owner's
safety net no longer reaches Chrome, and Decision 2 does not mention
it. Neither finding blocks the observer fix. Required gate: the
full `verify` check has not run on this head. PR #293 is a draft, so
run 44490607780 stopped with "Draft PR: the full suite has not run on
this head". This record does not predict that result. The PR cannot
be merged until `verify` passes on the exact head.

## Findings

### CCH-R1 (Medium, evidence): the reproduction blames the wrong handle for the hang

- Claim: track1.md:13-17 says that when the helper does not hold the
  stderr pipe, the old observer "exits promptly (exit 2, 0.34 s)", and
  so "the held stderr pipe is what keeps the Node event loop alive".
- Measured: I made the same control in a scratch copy. The fake
  helper uses `stdio: ignore` and runs against the old sources. The
  observer still prints `browser-cleanup-failed` and
  `cleanup-complete` and then does not exit, until the 20 s guard
  kills it. `process.getActiveResourcesInfo()` at 8 s reports
  `TCPServerWrap`. The `locked` mode has no helper and no held pipe,
  and it hangs the same way on the old code. That is why test 3
  fails before the fix.
- Mechanism: in sale-page-observation.mjs:376-392, a rejected
  `chrome.dispose()` jumps to the `catch`. `server.close()` (line
  389) is skipped, and the open loopback server keeps the event loop
  alive. Any dispose rejection is enough to produce the CI signature
  (`cleanup-complete`, then no exit, `browser-cleanup-failed`). A
  helper that holds the pipe is not needed.
- Consequence: the observer is still fixed, because `process.exit`
  ends the process whatever handles are open. But the evidence's
  causal story is wrong, and the `stderr.destroy()` change is credited
  with work it does not do (see CCH-R3). The same skip-close pattern
  is still present in run.mjs (CCH-R4).
- Repair: correct track1.md. The hang comes from the loopback server
  (and any other open handle) when dispose rejects. Optionally close
  the server even when dispose rejects.

### CCH-R2 (Medium, lifecycle): the Python correction owner's SIGKILL fallback no longer reaches Chrome

- tests/helpers/correction_browser_owner.py:134-139 says "Its browser
  is in this private process group" and calls
  `os.killpg(owner.pid, SIGKILL)` when profiles remain. Since
  chrome.mjs:317 (`detached: true`), Chrome leads its own group, so
  this killpg reaches only the Node owner. The comment is now false.
  The `shutil.rmtree(..., ignore_errors=False)` that follows can then
  run while Chrome is still writing.
- Scenario: the owner is still alive 5 s after `terminate()`, which
  can happen because dispose may take 3 s TERM grace + 2 s KILL wait +
  about 2 s of profile retries. Python then calls `owner.kill()`.
  SIGKILL skips the owner's exit hook. If the group has not yet been
  killed, Chrome survives and rmtree may raise.
  `_run_bounded_subprocess` has the same issue
  (tools/sale_page_observation.py:542-553). Decision 2 covers that
  one for the observer only. It does not mention the correction
  owner, and it says "one owner for the process tree" while this
  Python fallback still exists.
- Repair: extend Decision 2 to name the correction owner and correct
  the comment, or have the Python side also kill the recorded browser
  group.

### CCH-R3 (Low, evidence): the stderr destroy is not tested, and a test name claims it is

- Mutant M2 removes `child?.stderr?.destroy()` (chrome.mjs:294). All
  four new tests still pass. The title of test 1 ("... and frees
  stderr", chrome-group-cleanup.test.mjs:37) observes nothing about
  stderr.
- Repair: assert that the stream is destroyed (or that no `PipeWrap`
  is left after dispose), or drop the claim from the title.

### CCH-R4 (Low, compatibility): sibling entry point run.mjs keeps the old hang and gains a signal window

- run.mjs `cleanup()` (lines ~123-129) awaits `chromeHandle.dispose()`
  before `server.close()` and never calls `process.exit`. If dispose
  rejects, run.mjs hangs on its open server, the same mechanism as
  CCH-R1. This predates the change, but the change touches the shared
  dispose that triggers it.
- run.mjs installs `process.once` SIGINT/SIGTERM before it launches
  Chrome, so `installExitHooks` skips those signals for the life of
  the process (chrome.mjs:83,90). run.mjs:170-172 removes its
  listeners before `await cleanup()`. A Ctrl-C in that window kills
  Node with the default action, and the exit hook does not run.
  Before, Chrome was in the terminal's foreground group and got the
  Ctrl-C too. Now it survives. The window is small.

### CCH-R5 (Low, ownership): a reused process-group id could be signalled

- `ownedGroups` (chrome.mjs:60) drops a pgid only after dispose
  confirms the group is gone (line 290). If a Chrome group exits by
  itself and is never disposed, the `exit` hook (line 84) sends
  SIGKILL to `-pgid` when the process ends. So does a late dispose's
  SIGTERM. If the system has given that id to a new group leader in
  the meantime, a process the harness did not start is signalled. On
  parallel CI with many detached spawns this is unlikely but possible.
  Repair: on child `exit`, check whether the group is gone and drop
  it from `ownedGroups` if so.

## Charter questions

1. **Mechanism.** The reproduction shows the CI signature, but it
   names the wrong handle (CCH-R1). The real handle is the unclosed
   loopback server after a dispose rejection. The fix covers it
   through `process.exit`.
2. **Process ownership.** On macOS with real Chrome (via the head
   `lib/chrome.mjs`, isolated TMPDIR), all 10 harness processes (main,
   gpu, 2 utility, 6 renderers) were in the pgid led by the main
   process, and 0 were left after dispose. No new crashpad handler
   appeared. Linux was not measured; only CI can show it. The exit
   hooks chain with existing handlers: they skip a signal that
   already has a listener when they install. That holds for run.mjs
   and the correction owner, apart from the CCH-R4 window. The
   SIGKILL gap is as Decision 2 states for the observer, and it also
   affects the correction owner (CCH-R2). The only way to signal a
   process the harness did not start is pgid reuse (CCH-R5).
3. **Honesty.** On head, an unremovable profile gives
   `browser-cleanup-failed`, exit 2, in about 2.2 s, and
   `cleanup_completed: false`. A group that survives SIGKILL makes
   dispose reject with `chrome-process-group-survived`, which maps to
   the same failure. The bounded profile retry (20 x 100 ms) is
   reported when it fails, so it hides no real failure, and it keeps
   within Decision 1. The 240 s bound is unchanged.
4. **Tests.** On the old sources the new tests give 1-3 fail, 4 pass,
   as claimed. Mutants in scratch copies:
   - M1, signal the main pid only, not the group: tests 1 and 2 fail.
   - M2, no stderr destroy: all pass (CCH-R3).
   - M3, no `process.exit`: test 3 fails.
   - M4, not `detached`: tests 1 and 2 fail, and the run hung until
     my 150 s bound.

   Both the group kill and the prompt exit are tested. The
   `real-chrome-repair.test.mjs` failure under a parallel run of the
   whole directory is pre-existing: it fails on base and on head
   (isolated TMPDIR) and passes alone on head.

## What I ran

- Orientation block at `37a6374d` (verified against Git).
- `node --test` of chrome-group-cleanup.test.mjs on head (4/4 pass,
  13.7 s), and the same test plus the fake helper copied onto the old
  sources (3 fail).
- The control repro with the helper's stderr set to `ignore`, plus an
  active-handle probe (`--import` preload), on the old sources.
- Mutants M1-M4 in scratch copies outside the repository, each run
  under a time bound.
- `node --test tools/presentation_harness/tests/*.test.mjs` on base
  and head with an isolated TMPDIR, and real-chrome-repair alone on
  head.
- A real-Chrome group-membership probe through the head library.
- `python3 tools/envelope_scan.py --range github/main..HEAD`: clean.
- `pytest tests/test_presentation_chrome_lifecycle.py -m "not live"
  --collect-only`: the new test is in the live lane (deselected).
- `gh pr checks 293`: `verify` has not run (draft).
- Cleanup: mutant M4 left four fake-Chrome main processes when its
  bound fired. I killed those four (all mine, matched by my scratch
  path) and removed their profiles. No Chrome or fake-Chrome
  processes from this review are still running.
