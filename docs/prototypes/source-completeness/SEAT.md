# Source Completeness Prototype - Seat File

Execution state for Source Completeness And Interest Slice Track 0. A fresh
agent resuming this project reads this file when `docs/phase-state.md` points
here. Do not self-assign the foreman seat unless it is marked vacant; record
any succession in `process-log.md`.

Committee reviewers named in the approved plan are foreman-spawned sub-agents
by default (ADR-0013). Non-reviewer seats require per-spawn owner
confirmation.

## Current Step

**Plan drafted — awaiting owner approval.** No charter exists and no seat
beyond the foreman is filled until the owner approves `plan.md`.

## Seats

| Seat | Role file | Holder | Status |
|---|---|---|---|
| Foreman | `roles/foreman.md` | Fable 5 session, 2026-07-12 | active |
| Builder it1 | `roles/builder.md` | — | not opened (plan approval pending) |
| Rival builder | `roles/builder-rival.md` | — | not opened |
| Reviewer: governance | `roles/reviewer-governance.md` | — | not opened |
| Reviewer: adversary | `roles/reviewer-adversary.md` | — | not opened |
| Reviewer: expressiveness | `roles/reviewer-expressiveness.md` | — | conditional (opens only at evidence rung ≥ 3) |

## Next Action

Owner reviews and approves (or amends) `plan.md`. On approval, the foreman
writes `charter-it1.md` within the plan's Gate 2 paper scope and requests
owner confirmation to spawn the it1 builder.

## Planned Exhibits

None yet. Concluded iterations become `exhibits/source-completeness/it<N>`.
