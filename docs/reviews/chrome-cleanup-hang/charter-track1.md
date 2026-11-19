# Charter: Track 1 of Chrome cleanup does not hang CI

Role: Builder. Source HEAD on milestone/chrome-cleanup-hang-2025.
Plan: docs/phases/engine-breadth/milestones/chrome-cleanup-hang.md (read
it whole, especially "Foreman's reading" and Decision 1). Read:
tools/presentation_harness/lib/chrome.mjs (launch and `dispose`),
tools/presentation_harness/sale-page-observation.mjs (the `finally`
cleanup and `fail`), tools/presentation_harness/chrome-resource-probe.mjs
(process-group kill precedent), tools/sale_page_observation.py
(`_run_bounded_subprocess`, the 240 s call), the Node tests under
tools/presentation_harness/tests/ and
tests/test_sale_page_observation_temp_paths.py. Do not read governance.

## Scope

1. **Reproduce.** Show the hang mechanism locally without CI: for
   example a fake "Chrome" executable that forks a helper which outlives
   the main process, holds the inherited stderr and writes into the
   profile directory. Show today's code reaching `cleanup-complete` and
   then not exiting, and `dispose` failing on the profile. If the
   reading is wrong, find the real mechanism and say so before fixing.
2. **Fix.**
   - Start Chrome in its own process group and end the whole group
     (SIGTERM, then SIGKILL) on dispose; confirm no owned process
     survives.
   - Remove the profile robustly once the group is gone (bounded retry
     on ENOTEMPTY/EBUSY), and report honestly if it still fails.
   - Destroy owned streams so they cannot keep the event loop alive.
   - The observer exits promptly after its `finally` with its exit code
     (2 on any failure), so the Python bound is never the thing that
     ends a run.
   Keep diagnostics (the progress and failure records) exactly as
   informative as today. Apply the same group handling to the other
   harness entry points that use `lib/chrome.mjs` if they share it.
3. **Tests.** Node tests with the fake Chrome: the helper is killed, the
   profile removed, the process exits within a few seconds, and a
   genuinely unremovable profile still yields `browser-cleanup-failed`
   with a prompt exit. Run the Python Chrome tests
   (tests/test_sale_page_observation_*.py) locally several times.
4. **Evidence.** track1.md: the reproduction before and after, timings,
   and what is still not covered (only CI can show the real-Chrome
   frequency).

No change under packages/; no raised timeout or retry (Decision 1).

## Deliverables

Changes under tools/presentation_harness/ (and tools/sale_page_observation.py
only if needed), tests, evidence in
docs/phases/engine-breadth/milestones/chrome-cleanup-hang-evidence/.
Run the Node harness tests, the Python sale-page observation tests,
`pytest -m "not live"` and `python3 -m mypy`; report the lines.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Commit incrementally, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
  retry every 10 s for up to 5 min if held).
- Never kill a process the harness did not start. Leave no Chrome or
  fake-Chrome processes running when you finish.
- Write your JSON report before your final checks; update it when done.
- Never --no-verify or a bare git stash. Foreground commands only; leave
  no background jobs. No push and no spawn.
