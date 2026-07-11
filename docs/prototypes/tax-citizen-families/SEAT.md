# Tax Citizen Families Prototype - Seat File

This is the execution state for First Tax Slice Track 0. A fresh agent resuming
this project reads this file first when `docs/phase-state.md` points here. Do
not self-assign the foreman seat unless it is marked vacant; record any
succession in `process-log.md`.

Context-starved seats are not filled by generic resumption. The owner launches
them by pasting the launch line from the role file into a fresh session.

## Current Step

**Round 3 targeted repair review is open.** Iteration 3 is preserved as exhibit
tag `exhibits/tax-citizen-families/it3` at `be72d63`; its active prototype
branch has been removed. Governance, expressiveness, and adversary seats are
open for foreman dispatch. The context-starved legibility seat requires owner
launch.

## Seats

| Seat | Role file | Holder | Status |
|---|---|---|---|
| Foreman | `roles/foreman.md` | codex (planning session, 2026-07-11) | active |
| Builder it1 | `roles/builder.md` | `codex-builder-it1-2026-07-11` | complete; exhibit `exhibits/tax-citizen-families/it1` |
| Rival builder | `roles/builder-rival.md` | owner-launched clean-room session | complete (`989d9fe`; `examination-it2.md`) |
| Reviewer: governance | `roles/reviewer-governance.md` | `codex-governance-r1-2026-07-11` | round 1 complete |
| Reviewer: expressiveness | `roles/reviewer-expressiveness.md` | `codex-expressiveness-r1-2026-07-11` | round 1 complete |
| Reviewer: adversary | `roles/reviewer-adversary.md` | `codex-adversary-r1-2026-07-11` | round 1 complete |
| Reviewer: legibility | `roles/reviewer-legibility.md` | owner-launched fresh session | round 1 complete |
| Reviewer: governance | `roles/reviewer-governance.md` | `codex-governance-r2-2026-07-11` | round 2 complete |
| Reviewer: expressiveness | `roles/reviewer-expressiveness.md` | `codex-expressiveness-r2-2026-07-11` | round 2 complete |
| Reviewer: adversary | `roles/reviewer-adversary.md` | `codex-adversary-r2-2026-07-11` | round 2 complete |
| Reviewer: legibility | `roles/reviewer-legibility.md` | owner-launched fresh session | round 2 complete |
| Builder it3 | `roles/builder.md` | owner-launched it2 builder session | complete; exhibit `exhibits/tax-citizen-families/it3` |
| Reviewer: governance | `roles/reviewer-governance.md` | dispatch pending | round 3 open |
| Reviewer: expressiveness | `roles/reviewer-expressiveness.md` | dispatch pending | round 3 open |
| Reviewer: adversary | `roles/reviewer-adversary.md` | dispatch pending | round 3 open |
| Reviewer: legibility | `roles/reviewer-legibility.md` | owner launch needed | round 3 open |

## Next Action

Foreman dispatches governance, expressiveness, and adversary reviewers using
`gpt-5.6-luna` with high reasoning. Owner launches the context-starved
legibility reviewer using `roles/reviewer-legibility.md` and `reviews/round-3.md`.
No reviewer may read same-round peer output before submission.

## Planned Exhibits

- Tag `exhibits/tax-citizen-families/it1` - first candidate contract at
  `88f0139`.
- Tag `exhibits/tax-citizen-families/it2` - clean-room rival at `989d9fe`.
- Tag `exhibits/tax-citizen-families/it3` - targeted repair candidate at
  `be72d63`.
