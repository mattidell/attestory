# Source Completeness Prototype - Seat File

Execution state for Source Completeness And Interest Slice Track 0. A fresh
agent resuming this project reads this file when `docs/phase-state.md` points
here. Do not self-assign the foreman seat unless it is marked vacant; record
any succession in `process-log.md`.

Committee reviewers named in the approved plan are foreman-spawned sub-agents
by default (ADR-0013). Non-reviewer seats require per-spawn owner
confirmation.

## Current Step

**Round-1 disposition ratified; iteration 3 repair charter prepared.** The
first dispatch was halted before producing anything, but its branch later
landed commit `d47d12c` with the four chartered paper deliverables. They are on
`main` and preserved at `exhibits/source-completeness/it1`. The clean-room rival
is integrated and preserved at `exhibits/source-completeness/it2`.

## Seats

| Seat | Role file | Holder | Status |
|---|---|---|---|
| Foreman | `roles/foreman.md` | Codex session, 2026-07-12 | active; succeeded prior session on owner instruction |
| Builder it1 | `roles/builder.md` | Claude Opus 4.8 session (commit `d47d12c`) | complete; exhibit tagged, branch deleted |
| Builder it3 repair | `roles/builder.md` | original it1 builder continuity requested by owner | ready; `charter-it3.md`, branch `prototypes/source-completeness/it3`, isolated worktree `/tmp/finances-source-completeness-it3` |
| Rival builder | `roles/builder-rival.md` | `/root/source_completeness_rival_it2`, 2026-07-12 | complete; exhibit tagged, branch/worktree deleted |
| Reviewer: governance | `roles/reviewer-governance.md` | `/root/sc_round1_governance` | round 1 complete; review integrated |
| Reviewer: adversary | `roles/reviewer-adversary.md` | `/root/sc_round1_adversary` | round 1 complete; review integrated |
| Reviewer: expressiveness | `roles/reviewer-expressiveness.md` | — | conditional (opens only at evidence rung ≥ 3) |

## Next Action

Owner resumes the original it1 builder on `charter-it3.md`, branch
`prototypes/source-completeness/it3`, in the prepared isolated worktree. The
foreman does not spawn this builder.

## Planned Exhibits

- `exhibits/source-completeness/it1` at `d47d12c`.
- `exhibits/source-completeness/it2` at `82ffb7f0`.
