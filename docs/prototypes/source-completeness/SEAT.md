# Source Completeness Prototype - Seat File

Execution state for Source Completeness And Interest Slice Track 0. A fresh
agent resuming this project reads this file when `docs/phase-state.md` points
here. Do not self-assign the foreman seat unless it is marked vacant; record
any succession in `process-log.md`.

Committee reviewers named in the approved plan are foreman-spawned sub-agents
by default (ADR-0013). Non-reviewer seats require per-spawn owner
confirmation.

## Current Step

**Iteration 1 built; foreman conformance checked; integration pending.** The
first dispatch was halted before producing anything, but its branch later
landed commit `d47d12c` with the four chartered paper deliverables. No further
builder dispatch is authorized unless the owner explicitly instructs it.

## Seats

| Seat | Role file | Holder | Status |
|---|---|---|---|
| Foreman | `roles/foreman.md` | Codex session, 2026-07-12 | active; succeeded prior session on owner instruction |
| Builder it1 | `roles/builder.md` | Claude Opus 4.8 session (commit `d47d12c`) | complete; branch awaits integration/exhibit preservation |
| Rival builder | `roles/builder-rival.md` | — | next: owner-confirmed spawn or owner-launched clean-room session after it1 lands |
| Reviewer: governance | `roles/reviewer-governance.md` | — | opens for round 1 after it2 (standing-authorized) |
| Reviewer: adversary | `roles/reviewer-adversary.md` | — | opens for round 1 after it2 (standing-authorized) |
| Reviewer: expressiveness | `roles/reviewer-expressiveness.md` | — | conditional (opens only at evidence rung ≥ 3) |

## Next Action

Integrate the already committed it1 documents and preserve branch tip
`d47d12c` as `exhibits/source-completeness/it1`. Then pause: the owner has
explicitly directed that no builder agent be spawned unless they instruct it.
Committee round 1 runs only after a separately authorized rival design exists.

## Planned Exhibits

- Pending integration: `exhibits/source-completeness/it1` at `d47d12c`.
