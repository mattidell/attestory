<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "entry-loop-rescope",
  "status": "Open. P0 designs moving the W-2 entry loop onto the workspace's adopted core: its surface, its evaluation lines and its seed.",
  "scope": [
    "the W-2 entry loop resolves its surface from the workspace's adoption (resolve_adopted_surface), as the correction session does",
    "its evaluation lines follow the adopted core's presentation (lines 11a, 11b and 12e on current cores, 11 and 12 on the v6-era core)",
    "a seed for the current core that answers every closure and question the current core asks, so a W-2 entry computes",
    "the existing v6 seed and its tests keep their behaviour"
  ],
  "non_goals": [
    "no tax content, package, schema or kernel change: this milestone publishes no core package",
    "no edit to the runner's attachment code",
    "no change to the entry loop's protocol, refusals or saved shape beyond what the line set requires",
    "no change to the correction session"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/entry-loop-current-core.md",
      "docs/phases/engine-breadth/milestones/correction-current-core.md",
      "docs/phases/engine-breadth/milestones/entry-loop-rescope.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/entry-loop-rescope.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/entry-loop-rescope.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/entry-loop-rescope.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# The Entry Loop on the Current Core (2025)

Milestone key: entry-loop-rescope.
Branch: milestone/entry-loop-rescope-2025, cut from `github/main` at
`2ebe6889` (core v70, after the merged Schedule A attachment milestone,
PR #248). It publishes no core package.
Phase: Engine Breadth, bounded return. Opening plan: 2026-10-31.

## What we are trying to accomplish

The entry-loop-current-core milestone (#242) closed on its trace: the W-2
entry loop (`packages/derivation/entry_loop.py`, `SyntheticW2EntryRuntime`)
runs only on the core its seed adopts (package v6). Three things tie it
there:

- **A fixed surface:** the `frrs_t3` release directory and the first registry
  (`published-packages.json`); a workspace that adopts a current core is
  refused at opening (`RELEASE_ABSENT_OR_MISMATCH`).
- **A fixed line set:** `EVALUATION_LINES` (1a, 2b, 3a, 3b, 9, 11, 12, 15, 16)
  and `_line_values`, which requires all nine. Current cores present 11a, 11b
  and 12e instead of 11 and 12, so the loop would end in
  `entry-state-unavailable`.
- **A thin seed:** it answers what the v6 core asked. On a current core a
  fresh run blocks 207 rows for closures and questions the seed never
  answers.

The useful outcome: a filer entering a W-2 in the entry loop on the current
core sees the same lines and values a fresh run on that core computes.

## What we know

- #242's trace and probe: `entry-loop-current-core-evidence/trace.md`.
- The correction session solved the surface part with
  `resolve_adopted_surface` (`packages/derivation/production_resolver.py`).
- `tests/helpers/current_core_returns.py` builds complete current-core
  returns (`base_return()`), which shows what a current-core seed must answer.
- The entry loop's tests: `tests/test_entry_loop_t1.py` and the entry loop
  evaluation runner (`packages/derivation/runners/entry_loop_evaluation.py`).

## Actions the team will take

1. **P0 — design.** The three changes: surface resolution; how the line set
   follows the adopted core's presentation (derived from the form fields the
   adopted package binds, not a second fixed list, if that is possible); and a
   current-core seed. What the v6 seed and its tests need to keep working.
   Hand-computed values for a W-2 entry on the current core. No code changes.
   Stop if a kernel, schema or content change is needed.
2. **Decide.**
3. **Track 1.** The changes and tests.
4. **Close.** Fresh-reader review, curated history, retrospective, roadmap.

## Boundary after PR #248

#248 is merged and this branch includes core v70 and its Schedule A
attachment work. This milestone must not publish a core package or edit
`runner.py`'s attachment code. Preserve that result and verify the entry loop
on core v70, with the v6 path unchanged. Reconcile any later main changes
before publication.

## Process

Dispatch to Luna agents at maximum reasoning, following the owner's latest
direction. Track 1 touches
`packages/derivation/`, so the full suite runs before handoff. Stop means
stop.

## P0 result

The real v70 coordinator run over the complete synthetic return has no blocked
rows. The thin legacy seed, re-adopted to v70, leaves 209 blocked rows. The
fixed release surface refuses that adoption; the legacy line reader refuses
the modern presentation. See `entry-loop-rescope-evidence/p0-design.md` and
its executable probe for the distinction between supplied inputs and derived
outputs.

## Decisions and Track 1 contract

- Resolve the publication surface from the workspace adoption on every run,
  using the existing resolver and explicit legacy/current search roots. Never
  substitute a package or infer a registry filename from its version.
- Use bounded profiles for core v6 and v70. Each selects exact adopted Form
  1040 field identities and versions, with explicit impact/comparison roles.
  Read labels and bindings from the package. The schema supplies no role or
  money-type metadata, so selecting all numeric fields would widen this UI
  without authority. Unknown profiles refuse rather than guessing.
- Keep blocked profile rows visible during partial entry. Both modern AGI
  rows (11a and 11b) remain distinct display fields. Verify numeric values,
  exact bindings and Form 1040 identity, not line-number equality alone.
- Add a complete synthetic v70 entry seed and an explicit way to select it;
  preserve the existing default v6 seed and its tests. Runtime code must not
  import test helpers. Box 2 remains supplied fixture data, not a new control.
- Track 1 proves first entry and correction through `live_coordinate_run`,
  checks partial states and refusal boundaries, and preserves the legacy
  results. No kernel, schema, content-package, runner attachment or protocol
  change is authorized.

Next: build Track 1 under `docs/reviews/entry-loop-rescope/charter-track1.md`,
then fresh-reader review and repair before closeout.
