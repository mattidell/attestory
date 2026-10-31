# P0: read the Chrome startup traces and design the remedy

## Context capsule

- Source ref: `HEAD`; verify against Git. Branch `milestone/chrome-startup-flake`.
- Plan: `docs/phases/engineering-health/milestones/chrome-startup-flake.md`.
- Role: Builder. Assigned paths only:
  `docs/phases/engineering-health/milestones/chrome-startup-flake-evidence/`
  (`p0-traces-and-design.md`, `analyze.py`, `traces-summary.json`). Raw
  downloaded artifacts go in the scratchpad named at launch, never the
  repository (they may contain runner paths).
- Deep reads: the plan; #229's evidence
  (`docs/phases/engineering-health/milestones/explanation-sharing-evidence/chrome-startup.md`,
  `browser-resources.md`, `chrome-startup-summary.json`);
  `.github/workflows/ci.yml` (the shard step, `DEMO_CHROME_TRACE`, the
  probe, which artifacts are uploaded); `tools/presentation_harness/lib/chrome.mjs`,
  `lib/chrome-observation.mjs`, `lib/startup-coordinator.mjs`;
  `tests/helpers/chrome_startup_slot.py`, `correction_browser_owner.*`;
  `tests/test_sli_correction_resumption.py` around its browser probe.
- Ceiling: measured evidence and a paper design. No code, workflow or test
  changes. Committed evidence must be sanitized: no absolute paths, runner
  names or raw stderr.

## Questions to answer

1. **Inventory.** Every required run that failed on this timeout since
   2026-10-29, from `gh run list` and the job logs: run id, PR, shard, test,
   message. Which of them carry startup traces (#229's observer)?
2. **Traces.** For each failing launch with a trace: launch start, each
   observation, whether and when DevToolsActivePort appeared after ten
   seconds, process state, what the startup slot held. Compare with a sample
   of at least five passing shards: the distribution of launch-to-ready
   times. How close to ten seconds do passing launches come?
3. **Load.** Shard wall times for failing versus passing shards; whether the
   new live modules (absent from `ci-node-durations.json`) cluster in the
   failing shards.
4. **Design.** The smallest remedy the data supports, with its cost, what
   it could hide, and the controls that would prove it (for example: raise
   the active startup allowance from ten seconds to N within the slot; one
   relaunch with a fresh profile before page load; refresh shard durations).
   Name every file. If the traces show launches that never become ready,
   say so: a longer wait would not help.
5. **If the data is insufficient,** stop and propose the cheapest change
   that would capture it.

## Stop conditions

Stop and report if the traces cannot distinguish late readiness from none;
if the remedy would retry application assertions; or if it needs a runner
image or dependency change. Stop means stop.

## Handoff

Make GitHub API calls sequentially with pauses (a rate limit was hit on
2026-10-31; check `gh api rate_limit` if a call is refused). Commit
incrementally. Commit lock
`<git-common-dir>/worktrees/engine-worktree-1/collaboration-commit.lock`
(`mkdir` before, `rmdir` after). Stage explicit paths; never `--no-verify`;
do not push. Report the SHAs and a short answer per question.
