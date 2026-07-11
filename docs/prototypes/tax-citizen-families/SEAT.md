# Tax Citizen Families Prototype - Seat File

This is the execution state for First Tax Slice Track 0. A fresh agent resuming
this project reads this file first when `docs/phase-state.md` points here. Do
not self-assign the foreman seat unless it is marked vacant; record any
succession in `process-log.md`.

Context-starved seats are not filled by generic resumption. The owner launches
them by pasting the launch line from the role file into a fresh session.

## Current Step

**Iteration 1 builder seat is open.** The charter is `charter-it1.md` v3.
Round 0 review and delta-confirmation are complete. Builder work happens on
branch `prototypes/tax-citizen-families/it1`; prototype code never merges to
`main`.

## Seats

| Seat | Role file | Holder | Status |
|---|---|---|---|
| Foreman | `roles/foreman.md` | codex (planning session, 2026-07-11) | active |
| Reviewer: governance | `roles/reviewer-governance.md` | `codex-governance-delta-2026-07-11` | round 0 complete |
| Reviewer: adversary | `roles/reviewer-adversary.md` | `codex-adversary-delta-2026-07-11` | round 0 complete |
| Builder it1 | `roles/builder.md` | `codex-builder-it1-2026-07-11` | active on branch `prototypes/tax-citizen-families/it1` |
| Rival builder | `roles/builder-rival.md` | not opened | context-starved; opens after it1 review |
| Reviewer: expressiveness | `roles/reviewer-expressiveness.md` | not opened | opens after a build |
| Reviewer: legibility | `roles/reviewer-legibility.md` | not opened | context-starved; opens after a build |

## Next Action

Builder it1 is active in the separate worktree
`/tmp/tax-citizen-families-it1` on branch
`prototypes/tax-citizen-families/it1`. Context-starved rival and legibility
seats remain closed.

## Planned Exhibits

- Branch `prototypes/tax-citizen-families/it1` - first candidate contract once
  builder seat opens.
- Branch `prototypes/tax-citizen-families/it2` - clean-room rival after it1
  review, unless the owner stops the process earlier.
