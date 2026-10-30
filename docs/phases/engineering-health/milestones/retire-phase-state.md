<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engineering Health",
  "topic": "retire-phase-state",
  "status": "Closed. docs/phase-state.md is deleted. The foreman capsule finds the milestone plan from the branch name and derives open or closed from the plan; builders and reviewers are launched with their role and charter. Parked work and open owner-held questions live in the Engine Breadth roadmap.",
  "retrospective": "docs/milestone-retrospectives/2026-10-29-retire-phase-state.md",
  "scope": [
    "delete docs/phase-state.md and every live instruction that tells a seat to read or update it",
    "tools/foreman_context.py reads the plan from the branch name (or --plan) and derives open, closed or none",
    "tools/build_orientation_block.py takes --charter and --role, and --clean-room explicitly",
    "move parked work and open owner-held questions to the Engine Breadth roadmap"
  ],
  "non_goals": [
    "no product, schema, package or rule change",
    "no edit to closed plans, retrospectives, retired ADRs, archives or closed phase roadmaps that mention phase state as history",
    "no change to the plan front-matter format beyond what the tools read"
  ],
  "deep_reads": {
    "implementation": [
      "AGENTS.md#Which seat are you",
      "PROJECT_PLANNING.md#Milestone Lifecycle States"
    ],
    "review": [
      "AGENTS.md#Which seat are you",
      "PROJECT_PLANNING.md#Milestone Lifecycle States"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-10-29-retire-phase-state.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/coverage-frontier.md"
    ]
  }
}
-->

# Retire Phase State

Audience: Foreman. Owner-directed process milestone (2026-10-29): one plan,
one implementation commit, no tracks, no independent review stage.

## Why

`docs/phase-state.md` served hand-offs between threads: a cold foreman or
builder started from its pointers. The owner no longer hands off; the foreman
that plans a milestone also closes it, and dispatch briefs name the role and
charter. What remained was cost. Every closeout rewrote the same top sections,
so two milestones in parallel always conflicted on the file (PRs #229 and #230
both did). It had 51 commits in two months, a closeout dropped a whole section
by accident, and the pointer fields drifted from the charters four times.

Most of its content repeated other records: milestone summaries are in
retrospectives and roadmaps; state is a fact git and the plan already hold.
Only the parked list had no other home.

## Change

1. **Foreman capsule.** `tools/foreman_context.py` finds the plan from the
   branch name: `milestone/<key>-<purpose>` (or under `temp/`) reads
   `docs/phases/*/milestones/<key>.md`, longest key first; `--plan` overrides.
   A plan naming a landed retrospective is closed; otherwise open. Off a
   milestone branch the state is `none`, and the capsule lists the three most
   recent retrospectives. Divergence, spent and ratified-line reporting are
   unchanged.
2. **Orientation block.** `tools/build_orientation_block.py` takes
   `--charter <path>[#Section]` and `--role` (or `--action`); clean-room is
   the explicit `--clean-room` flag. Role detection from a free-text field is
   gone.
3. **Records.** Parked work and the two open owner-held questions move to the
   Engine Breadth roadmap's "Parked work and open questions". Four code and
   test comments that cited phase state now cite that section.
4. **Instructions.** `AGENTS.md`, `PROJECT_PLANNING.md` (re-entry, lifecycle
   states, closeout, post-merge), the four seat files, the `/pickup` and
   `/foreman` commands, the builder and reviewer agent definitions, the ADR
   index and the README stop naming the file.

## Outcome

Delivered as above. Tests: `tests/test_foreman_context.py` (branch
derivation, longest key, `temp/` branches, `--plan`, no plan, open and closed
derivation, missing retrospective) and
`tests/test_build_orientation_block_charter_anchor.py` (charter anchor
scoping, required role, clean-room manifest, `--plan` off a milestone branch).
