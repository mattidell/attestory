# Tax Citizen Families Prototype - Seat File

This is the execution state for First Tax Slice Track 0. A fresh agent resuming
this project reads this file first when `docs/phase-state.md` points here. Do
not self-assign the foreman seat unless it is marked vacant; record any
succession in `process-log.md`.

Context-starved seats are not filled by generic resumption. The owner launches
them by pasting the launch line from the role file into a fresh session.

## Current Step

**Round 0 delta-confirmation is open.** The charter is `charter-it1.md` v2. No
builder seat opens until bounded delta-confirmation closes or the owner
overrides remaining dissent.

## Seats

| Seat | Role file | Holder | Status |
|---|---|---|---|
| Foreman | `roles/foreman.md` | codex (planning session, 2026-07-11) | active |
| Reviewer: governance | `roles/reviewer-governance.md` | `codex-governance-delta-2026-07-11` | round 0 delta complete |
| Reviewer: adversary | `roles/reviewer-adversary.md` | `codex-adversary-delta-2026-07-11` | round 0 delta complete |
| Builder it1 | `roles/builder.md` | not opened | blocked on round 0 disposition |
| Rival builder | `roles/builder-rival.md` | not opened | context-starved; opens after it1 review |
| Reviewer: expressiveness | `roles/reviewer-expressiveness.md` | not opened | opens after a build |
| Reviewer: legibility | `roles/reviewer-legibility.md` | not opened | context-starved; opens after a build |

## Next Action

Round 0 reviewers perform bounded delta-confirmation against `charter-it1.md`
v2 and `reviews/round-0-delta.md`. Generic resumption may claim an open
unstarved delta seat, but only one reviewer seat per identity per round. Do not
read same-round peer outputs before submitting.

## Planned Exhibits

- Branch `prototypes/tax-citizen-families/it1` - first candidate contract once
  builder seat opens.
- Branch `prototypes/tax-citizen-families/it2` - clean-room rival after it1
  review, unless the owner stops the process earlier.
