# Track 1: raise the Chrome launch allowance to 45 seconds

## Context capsule

- Source ref: `HEAD`; verify against Git. Branch `milestone/chrome-startup-flake`.
- Plan: `docs/phases/engineering-health/milestones/chrome-startup-flake.md`;
  its "Decisions" are binding.
- Role: Builder. Assigned paths only: `tools/presentation_harness/lib/chrome.mjs`
  and any other harness file that sets the same allowance (find every place
  the ten-second launch value is defined or asserted, in `tools/` and
  `tests/helpers/`); the harness tests under `tools/presentation_harness/tests/`;
  Python tests that assert the old allowance, edited only to the new value.
- Deep reads: the plan; P0's `p0-traces-and-design.md`; `chrome.mjs`,
  `chrome-observation.mjs`, `startup-coordinator.mjs`;
  `tests/helpers/chrome_startup_slot.py`, `correction_browser_owner.py`
  (the 210 s owner wait); the existing fake-Chrome controls.
- Ceiling: one allowance and its controls. No change to flags, the startup
  slot, scenario assertions, the workflow or any tax content.

## Build

1. Change the active launch allowance from ten seconds to 45 seconds at its
   single source. If it is defined in more than one place, make one the
   source and have the others read it; do not leave two values.
2. Confirm the arithmetic still fits: the slot queue wait plus 45 s must stay
   below the Python owner's startup wait. If it does not, **stop and
   report**.
3. Keep the diagnostic messages accurate (they name the allowance).
4. Controls, with fake Chrome processes as the existing tests do: ready at
   about 12 s (above the old limit) succeeds; never ready fails at the
   allowance with the existing "stayed alive without DevToolsActivePort"
   classification; exits early fails at once. Keep them fast by making the
   allowance injectable in tests, not by sleeping 45 s.

## Stop conditions

A change to flags, the slot, the workflow or any scenario assertion; a
retry of application assertions; the timing arithmetic not fitting. Stop
means stop.

## Handoff

Run the harness tests (`node --test tools/presentation_harness/tests/`), the
browser test modules locally if Chrome is available, `pytest -m "not live"`,
`python3 -m mypy` and `python3 tools/envelope_scan.py --range github/main..HEAD`.
One commit. Commit lock
`<git-common-dir>/worktrees/engine-worktree-1/collaboration-commit.lock`.
Stage explicit paths; never `--no-verify`; do not push. Report the SHA and
results.
