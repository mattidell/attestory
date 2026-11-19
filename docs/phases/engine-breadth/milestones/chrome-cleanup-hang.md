<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "chrome-cleanup-hang",
  "status": "Track 1 chartered 2026-11-19.",
  "scope": [
    "when the headless Chrome used by the saved-page observation harness cannot be cleaned up, the harness kills everything it owns and exits promptly with an honest failure, instead of hanging until the 240 s timeout",
    "the cleanup failure itself becomes rare on CI: every Chrome process the harness starts, including helpers, is ended and its profile removed"
  ],
  "non_goals": [
    "no change to packages/, to what the observation checks, or to the saved page",
    "no change to which tests are opt-in; the ten-case Chrome fixture stays opt-in",
    "no raised timeout or retry that hides a real failure"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/chrome-cleanup-hang.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/chrome-cleanup-hang.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/chrome-cleanup-hang.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/chrome-cleanup-hang.md"
    ]
  }
}
-->

# Chrome Cleanup Does Not Hang CI

Milestone key: chrome-cleanup-hang.
Branch: milestone/chrome-cleanup-hang-2025.
Phase: Engine Breadth, tooling. Opening plan: 2026-11-19.
Starting point: main at `a0f85a78` (core v97, registry v95, release v95).
Expected target: no package version change.

## What we are trying to accomplish

`tests/test_sale_page_observation_temp_paths.py::test_real_v80_chrome_launch_ignores_long_inherited_tmpdir_and_cleans_owned_root`
failed three CI `verify` runs in two days (44378633142, 44468976479,
44475264162) and passes locally in 18 s. Each failure reports the Node
observer at `cleanup-complete` after about 14 s with
`node_failure_reason=browser-cleanup-failed` and the process still
alive, so the Python side waits out its 240 s bound
(`tools/sale_page_observation.py:1502`). Each retry costs about an hour
of CI. The useful outcome is a harness that cleans up everything it
starts and, when it cannot, exits at once with the honest failure.

## Foreman's reading (to be confirmed, not assumed)

In `tools/presentation_harness/lib/chrome.mjs` `dispose()`, Chrome is
spawned without its own process group and with a piped stderr; on
dispose it sends SIGTERM, then SIGKILL after 3 s to the main process
only, then removes the profile directory. Chrome helper processes
(renderer, GPU, zygote) are not in a group the harness kills; they can
keep writing to the profile (so `rm` fails and `dispose` rejects, hence
`browser-cleanup-failed`) and keep the inherited stderr pipe open (so
Node's event loop never drains and the process never exits).
`sale-page-observation.mjs` sets `process.exitCode` but never calls
`process.exit`. `chrome-resource-probe.mjs` already kills a process
group with `process.kill(-pid, "SIGKILL")`.

## Stages

1. **Track 1.** Confirm or refute the reading with a reproduction
   (locally, with a synthetic helper that outlives the main process and
   holds the pipe or the profile), then fix: own the whole process
   tree, make profile removal robust to late writers, destroy owned
   streams, and make the observer exit promptly with its honest exit
   code once cleanup is done or has failed. Tests for each.
2. **Fresh review**, repair, closeout. The CI evidence is the next
   several `verify` runs; record them at closeout.

## Decisions

1. **No timeout or retry as the fix (2026-11-19, foreman).** A longer
   bound or an automatic retry would hide the hang, not remove it. The
   240 s bound stays.
