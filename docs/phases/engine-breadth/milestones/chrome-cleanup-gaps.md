<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "chrome-cleanup-gaps",
  "status": "Open 2026-11-27. Track 1 chartered.",
  "retrospective": null,
  "scope": [
    "the presentation harness runner closes its server and exits even when Chrome cleanup fails, with the honest failure",
    "an interrupt at any point after the runner starts Chrome, including before the launch returns, leaves no Chrome running"
  ],
  "non_goals": [
    "no product, kernel, schema or content change; no package version change",
    "no longer timeout or retry (chrome-cleanup-hang Decision 1)",
    "no Python-side reaping of a SIGKILLed observer's group (chrome-cleanup-hang Decision 2)"
  ],
  "deep_reads": {
    "planning": [
      "docs/phases/engine-breadth/milestones/chrome-cleanup-hang.md",
      "docs/phases/engine-breadth/milestones/chrome-cleanup-gaps.md"
    ],
    "implementation": [
      "docs/phases/engine-breadth/milestones/chrome-cleanup-hang.md",
      "docs/phases/engine-breadth/milestones/chrome-cleanup-gaps.md"
    ],
    "review": [
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/chrome-cleanup-gaps.md"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-11-27-sale-question-names.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# The Harness Cleans Up When Cleanup Fails (tooling)

Milestone key: chrome-cleanup-gaps.
Branch: milestone/chrome-cleanup-gaps-2025.
Phase: Engine Breadth, tooling. Opening plan: 2026-11-27.
Starting point: main at `5993ce933` (core v109, registry v107, release v107).
Expected target: no package version change.

## What we are trying to accomplish

The chrome-cleanup-hang milestone parked:

- "`run.mjs` still skips its server close when `dispose()` fails and has
  no exit backstop. A Ctrl-C in its short window before launch returns
  leaves Chrome running. A SIGKILLed observer cannot kill a Chrome group,
  which Decision 2 accepts. Group cleanup was checked with real Chrome
  only on macOS; Linux is covered by CI alone."

A harness that cannot clean up should still release everything else it
holds and exit at once with its failure, so CI does not wait out a bound.

## Stages

Tooling milestone: no prototype, no ADR. Track 1 (build), one fresh
review, repair, closeout, final review, merge.

1. **Track 1.** In `tools/presentation_harness/run.mjs` and its Chrome
   library, close the server whether or not `dispose()` succeeds, and add
   an exit backstop that ends the process with the failure after cleanup
   is attempted. Make an interrupt (SIGINT, SIGTERM) arriving before the
   Chrome launch returns end the Chrome group once launch settles. Each
   behaviour gets a test that fails on main: a forced `dispose()` failure
   still closes the server and exits non-zero promptly; an interrupt
   during launch leaves no Chrome process in the group. Keep the SIGKILL
   gap as Decision 2 states. Say in the evidence which checks ran on
   real Chrome locally (macOS) and which only in CI (Linux).
