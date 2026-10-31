<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "entry-loop-current-core",
  "status": "Closed on its trace. The entry loop refuses a current-core workspace; resolving the surface is not enough, because its line set and seed target an older presentation. The re-scope is parked.",
  "scope": [
    "the W-2 entry loop calculates on the core the workspace has adopted",
    "its existing seeds and saved behaviour are unchanged"
  ],
  "non_goals": [
    "no change to the entry loop's questions, refusals or saved shape",
    "no tax content or package change",
    "no kernel or schema change"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/correction-current-core.md",
      "docs/phases/engine-breadth/milestones/entry-loop-current-core.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/entry-loop-current-core.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/entry-loop-current-core.md"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-10-31-entry-loop-current-core.md",
      "docs/phases/engine-breadth/milestones/entry-loop-current-core.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  },
  "retrospective": "docs/milestone-retrospectives/2026-10-31-entry-loop-current-core.md"
}
-->

# The Entry Loop Calculates on the Current Core (2025)

Milestone key: entry-loop-current-core.
Branch: milestone/entry-loop-current-core-2025, stacked on
`milestone/correction-current-core-2025` (PR #241), whose resolver it reuses.
Phase: Engine Breadth, bounded return. Opening plan: 2026-10-31.

## What we are trying to accomplish

The correction-current-core review found that `packages/derivation/entry_loop.py`
builds its surface from fixed paths: the `frrs_t3` release directory and
`published-packages.json`, the first registry. A workspace in the W-2 entry
loop that adopted a later core would, by the same mechanism as the correction
session, be refused or calculated on old content.

The useful outcome: the entry loop resolves its surface from the workspace's
adoption, as the correction session now does.

## Actions the team will take

1. **Track 1 — trace and resolve.** One builder unit: confirm on the real
   path what the entry loop does for a workspace adopting a current core
   (trace first, committed as evidence), then resolve the surface with
   `resolve_adopted_surface`, keeping the `frrs_t3` release directory as a
   search location if the seeds need it. Tests: a current-core workspace
   calculates and matches a fresh run; the existing seeds are unchanged; the
   refusals keep today's outcomes. Stop if the entry loop's seeds cannot
   adopt a current core at all (then report the trace only), or if the fix
   needs more than the resolver.
2. **Close.** Fresh-reader review, curated history, retrospective, roadmap.

## Process

Dispatch to a Sonnet 5.5 Agent sub-agent. This touches `packages/derivation/`,
so the full suite runs before handoff. Stop means stop.

## Trace result

The trace is in [entry-loop trace](entry-loop-current-core-evidence/trace.md),
with its probe.

- The shipped seed adopts package v6 and release `demo.release.2025@v1`; for
  it, the resolver and the fixed surface agree, and it runs unchanged.
- With a core v66 adoption the fixed surface refuses at opening
  (`entry-run-refused:RELEASE_ABSENT_OR_MISMATCH`): the loop refuses rather
  than calculating on old content.
- With the surface resolved correctly, a fresh run blocks 207 rows: the thin
  entry seed lacks the closures later cores ask for. The loop also requires
  presentation lines 11 and 12, which v66 presents as 11a, 11b and 12e, so it
  would end in `entry-state-unavailable` even with the right surface.

## Decision

Foreman, 2026-10-31: closed on the trace. Moving the entry loop to a current
core means changing its line set and its seed, which this milestone
excluded; the re-scope is parked in the Engine Breadth roadmap. No code
changed.

## Outcome

No product change. The entry loop runs on the core its seed adopts, and
refuses a later one at opening.
