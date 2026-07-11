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
| Reviewer: governance | `roles/reviewer-governance.md` | open | round 1 open |
| Reviewer: expressiveness | `roles/reviewer-expressiveness.md` | open | round 1 open |
| Reviewer: adversary | `roles/reviewer-adversary.md` | open | round 1 open |
| Reviewer: legibility | `roles/reviewer-legibility.md` | not opened | context-starved; owner launch for round 1 |

## Next Action

Generic resumption may claim one open unstarved reviewer seat for round 1.
Do not read same-round peer outputs before submitting. Expressiveness must run
reproduction checks before opening `examination-it1.md`. The legibility seat is
context-starved and must be owner-launched using `roles/reviewer-legibility.md`
and the scope in `reviews/round-1.md`.

## Planned Exhibits

- Branch `prototypes/tax-citizen-families/it1` - first candidate contract,
  built at `88f0139`; branch remains available for round 1 review.
- Branch `prototypes/tax-citizen-families/it2` - clean-room rival after it1
  review, unless the owner stops the process earlier.
