# Source Completeness Prototype - Seat File

Execution state for Source Completeness And Interest Slice Track 0. A fresh
agent resuming this project reads this file when `docs/phase-state.md` points
here. Do not self-assign the foreman seat unless it is marked vacant; record
any succession in `process-log.md`.

Committee reviewers named in the approved plan are foreman-spawned sub-agents
by default (ADR-0013). Non-reviewer seats require per-spawn owner
confirmation.

## Current Step

**Plan approved (2026-07-12); charter it1 issued but unworked.** The first
it1 builder dispatch was halted by the owner before producing anything; its
empty branch ref was deleted. The charter stands as issued.

## Seats

| Seat | Role file | Holder | Status |
|---|---|---|---|
| Foreman | `roles/foreman.md` | Fable 5 session, 2026-07-12 | active |
| Builder it1 | `roles/builder.md` | — (first dispatch halted by owner 2026-07-12, no output) | vacant; re-dispatch needs fresh owner confirmation |
| Rival builder | `roles/builder-rival.md` | — | next: owner-confirmed spawn or owner-launched clean-room session after it1 lands |
| Reviewer: governance | `roles/reviewer-governance.md` | — | opens for round 1 after it2 (standing-authorized) |
| Reviewer: adversary | `roles/reviewer-adversary.md` | — | opens for round 1 after it2 (standing-authorized) |
| Reviewer: expressiveness | `roles/reviewer-expressiveness.md` | — | conditional (opens only at evidence rung ≥ 3) |

## Next Action

When it1 lands (branch committed, `examination-it1.md` merged): dispatch the
clean-room rival (it2) on the same charter — per-spawn owner confirmation
required, or the owner pastes the launch line from `roles/builder-rival.md`
into a fresh session. Committee round 1 runs only after both designs exist.

## Planned Exhibits

None yet. Concluded iterations become `exhibits/source-completeness/it<N>`.
