# Tax Citizen Families Prototype - Seat File

This is the execution state for First Tax Slice Track 0. A fresh agent resuming
this project reads this file first when `docs/phase-state.md` points here. Do
not self-assign the foreman seat unless it is marked vacant; record any
succession in `process-log.md`.

Context-starved seats are not filled by generic resumption. The owner launches
them by pasting the launch line from the role file into a fresh session.

## Current Step

**Round 1 review is open.** Iteration 1 is built on branch
`prototypes/tax-citizen-families/it1` at commit `88f0139`; examination is
`examination-it1.md`. Review scope is `reviews/round-1.md`.

## Seats

| Seat | Role file | Holder | Status |
|---|---|---|---|
| Foreman | `roles/foreman.md` | codex (planning session, 2026-07-11) | active |
| Builder it1 | `roles/builder.md` | `codex-builder-it1-2026-07-11` | complete (`88f0139`; `examination-it1.md`) |
| Rival builder | `roles/builder-rival.md` | not opened | context-starved; opens after it1 review |
| Reviewer: governance | `roles/reviewer-governance.md` | `codex-governance-r1-2026-07-11` | round 1 complete |
| Reviewer: expressiveness | `roles/reviewer-expressiveness.md` | `codex-expressiveness-r1-2026-07-11` | round 1 complete |
| Reviewer: adversary | `roles/reviewer-adversary.md` | `codex-adversary-r1-2026-07-11` | round 1 complete |
| Reviewer: legibility | `roles/reviewer-legibility.md` | not opened | context-starved; owner launch for round 1 |

## Next Action

Round 1 unstarved reviews are complete and committed. The remaining open seat is
context-starved legibility; it must be owner-launched using
`roles/reviewer-legibility.md` and the scope in `reviews/round-1.md`. Foreman
conformance and outcome summaries wait until legibility lands or the owner
disposes without it.

## Planned Exhibits

- Branch `prototypes/tax-citizen-families/it1` - first candidate contract,
  built at `88f0139`; branch remains available for round 1 review.
- Branch `prototypes/tax-citizen-families/it2` - clean-room rival after it1
  review, unless the owner stops the process earlier.
