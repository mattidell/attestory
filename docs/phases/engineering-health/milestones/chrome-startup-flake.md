<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engineering Health",
  "topic": "chrome-startup-flake",
  "status": "Open. The traced failure was a late cold start (11.2 s against a 10 s allowance); Track 1 raises the launch allowance to 45 s inside the startup slot.",
  "scope": [
    "find, from recorded CI traces, whether the failing Chrome launches become ready late or never",
    "make the required verify gate stop failing on this startup timeout without hiding a real browser failure",
    "keep every browser scenario's assertions, flags and coverage"
  ],
  "non_goals": [
    "no change to any tax content, package or computed value",
    "no change to the fast-lane budget",
    "no retry of an application scenario's assertions; a remedy may wait or relaunch only before the page loads"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engineering-health/milestones/explanation-sharing-evidence/chrome-startup.md",
      "docs/phases/engineering-health/milestones/explanation-sharing-evidence/browser-resources.md",
      "docs/phases/engineering-health/milestones/chrome-startup-flake.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engineering-health/milestones/chrome-startup-flake.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engineering-health/milestones/chrome-startup-flake.md"
    ],
    "new_milestone": [
      "docs/phases/engineering-health/milestones/chrome-startup-flake.md",
      "docs/phases/engineering-health/engineering-health-roadmap.md"
    ]
  }
}
-->

# Chrome Starts Before the Gate Gives Up

Milestone key: chrome-startup-flake.
Branch: milestone/chrome-startup-flake, stacked on
`milestone/closure-question-wording-2025` (PR #239).
Phase: Engineering Health. Opening plan: 2026-10-31.

## What we are trying to accomplish

Between 2026-10-30 and 2026-10-31, seven required `verify` runs failed on
one Chrome startup timeout, in `tests/test_sli_correction_resumption.py` or
`tests/test_sli_correction_session.py`: "Chrome did not write
DevToolsActivePort before the launch timeout". Each cost a fresh full run
(about 20 minutes and 3 CPU-hours). PR #229 coordinated startup across
workers and reused one browser for ordinary scenarios, but kept the
ten-second allowance and added an observer "for the next naturally triggered
CI failure". The flake recurred after #229 merged, on #233's run
41197479002, now worded "Chrome stayed alive without DevToolsActivePort".

The useful outcome: the gate stops failing on Chrome startup, and the
remedy rests on measured startup times rather than a guess.

## What we know

- #229's evidence: a slow launch was sampled in Linux disk-wait state;
  launches of 5.21 s and 7.39 s were seen; no launch crossed ten seconds in
  its observed runs, so late readiness and permanent non-readiness were
  never distinguished.
- CI writes startup traces (`DEMO_CHROME_TRACE`, `test-results/`) and a
  post-shard probe (`tools/presentation_harness/chrome-startup-probe.mjs`).
- The parked note offered "a longer startup wait or one retry".
- New live test modules from this series are absent from
  `ci-node-durations.json`, so the shard balancer places them without cost.

## Actions the team will take

1. **P0 — read the traces and design.** Download the shard artifacts (the
   startup traces and probe output) from every failing run since #229's
   observer existed, at least run 41197479002, and from a sample of passing
   runs. For each failing launch: did it become ready after ten seconds, and
   when, or never? What else was running? Then design the smallest remedy
   the data supports (for example a larger startup allowance inside the
   startup slot, one relaunch before page load, or refreshed shard
   durations), with its cost and what it could hide. No code changes. Stop
   if the data cannot distinguish late from never; then propose the cheapest
   way to capture it.
2. **Decide.**
3. **Track 1.** The remedy and its controls.
4. **Close.** Fresh-reader review, curated history, retrospective, roadmap.

## Process

Dispatch to Sonnet 5.5 Agent sub-agents. Use slow, sequential GitHub API
calls (the API rate limit was hit on 2026-10-31). Stop means stop.

## P0 result

P0 is in [traces and design](chrome-startup-flake-evidence/p0-traces-and-design.md),
with the analysis script and a sanitized summary.

- **Nine failed shards in eight runs**, all in the correction-browser tests.
  Only the post-#229 failure (run 41197479002) carries a startup trace.
- **That launch was late, not dead.** It was the first launch in its shard,
  waited 0 ms for the startup slot, stayed alive in disk-wait with memory
  and threads rising, and wrote DevToolsActivePort at 11,193 ms, about 1.2 s
  past the 10,024 ms deadline.
- **Passing launches:** 51 launches over 15 traced shards. Later launches
  take 248-414 ms; first launches usually take about 300 ms, but four took
  5.0-8.4 s, within 1.6 s of the deadline. Shard 0's first launch was slow
  in every traced run.
- **Load is not the cause:** failing and passing shards carry the same wall
  time and the same share of the new live modules.
- **Remedy:** raise the active launch allowance from 10 s to 45 s inside the
  startup slot. That fits the Python owner's 210 s startup wait (120 s queue
  plus 45 s launch). A fast launch costs nothing; a dead Chrome fails after
  45 s instead of 10 s; a Chrome that exits early still fails at once. One
  relaunch is not supported by the data: no launch was seen that never came
  up.
- **Limits:** one failing launch is traced; the other eight are assumed to
  be the same pattern. The disk explanation is inference.

## Decisions

Foreman, 2026-10-31, on P0's recommendation:

1. **Raise the launch allowance to 45 s,** keeping the startup slot, the
   flags and every scenario assertion.
2. **Keep #229's observer** so the next late launch is recorded with its
   time.
3. **Not now:** a relaunch, warming the Chrome binary in the workflow, and
   refreshing shard durations.

## Tracks

1. **Track 1 — allowance.** The default in
   `tools/presentation_harness/lib/chrome.mjs`, its diagnostic, and fake-Chrome
   controls: late but within the allowance succeeds; never ready fails at the
   allowance; exits early fails at once.
