# Source Completeness Prototype - Seat File

Execution state for Source Completeness And Interest Slice Track 0. A fresh
agent resuming this project reads this file when `docs/phase-state.md` points
here. Do not self-assign the foreman seat unless it is marked vacant; record
any succession in `process-log.md`.

Committee reviewers named in the approved plan are foreman-spawned sub-agents
by default (ADR-0013). Non-reviewer seats require per-spawn owner
confirmation.

## Current Step

**Prototype complete; ADR-0014 and ADR-0015 ratified.** The
first dispatch was halted before producing anything, but its branch later
landed commit `d47d12c` with the four chartered paper deliverables. They are on
`main` and preserved at `exhibits/source-completeness/it1`. The clean-room rival
is integrated and preserved at `exhibits/source-completeness/it2`.

## Seats

| Seat | Role file | Holder | Status |
|---|---|---|---|
| Foreman | `roles/foreman.md` | Codex session, 2026-07-12 | active; succeeded prior session on owner instruction |
| Builder it1 | `roles/builder.md` | Claude Opus 4.8 session (commit `d47d12c`) | complete; exhibit tagged, branch deleted |
| Builder repair1 | `roles/builder.md` | original it1 builder (deliberate continuity) | complete; exhibit `exhibits/source-completeness/repair1` |
| Builder repair2 | `roles/builder.md` | original it1 builder (deliberate continuity) | complete; exhibit `exhibits/source-completeness/repair2` |
| Builder repair3 | `roles/builder.md` | original it1 builder (deliberate continuity) | complete; exhibit `exhibits/source-completeness/repair3` |
| Builder repair4 | `roles/builder.md` | original it1 builder (deliberate continuity) | complete; exhibit `exhibits/source-completeness/repair4` |
| Rival builder | `roles/builder-rival.md` | `/root/source_completeness_rival_it2`, 2026-07-12 | complete; exhibit tagged, branch/worktree deleted |
| Reviewer: governance | `roles/reviewer-governance.md` | `/root/sc_round2_governance` | round 2 complete; review integrated |
| Reviewer: adversary | `roles/reviewer-adversary.md` | `/root/sc_round2_adversary` | round 2 complete; review integrated |
| Reviewer: expressiveness | `roles/reviewer-expressiveness.md` | `/root/sc_round2_expressiveness` | round 2 complete; review integrated |
| Reviewer: governance r3 | `roles/reviewer-governance.md` | owner-launched | complete; review integrated |
| Reviewer: adversary r3 | `roles/reviewer-adversary.md` | owner-launched | complete; review integrated |
| Reviewer: expressiveness r3 | `roles/reviewer-expressiveness.md` | owner-launched | complete; review integrated |
| Reviewer: governance r4 | `roles/reviewer-governance.md` | owner-launched | complete; review integrated |
| Reviewer: adversary r4 | `roles/reviewer-adversary.md` | owner-launched | complete; review integrated |
| Reviewer: expressiveness r4 | `roles/reviewer-expressiveness.md` | owner-launched | complete; review integrated |

## Next Action

Track 0 is complete. Foreman records the process retrospective and rewrites the
provisional milestone tracks against accepted ADR-0014/0015. SC-P3 remains
explicitly unresolved and cannot be improvised during implementation.

## Planned Exhibits

- `exhibits/source-completeness/it1` at `d47d12c`.
- `exhibits/source-completeness/it2` at `82ffb7f0`.
- `exhibits/source-completeness/repair1` at `5eee68c`.
- `exhibits/source-completeness/repair2` at `6144b65`.
- `exhibits/source-completeness/repair3` at `b09d0b5`.
- `exhibits/source-completeness/repair4` at `1c3ccb1`.
