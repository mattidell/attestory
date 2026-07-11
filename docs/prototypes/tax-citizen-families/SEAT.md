# Tax Citizen Families Prototype - Seat File

This is the execution state for First Tax Slice Track 0. A fresh agent resuming
this project reads this file first when `docs/phase-state.md` points here. Do
not self-assign the foreman seat unless it is marked vacant; record any
succession in `process-log.md`.

Context-starved seats are not filled by generic resumption. The owner launches
them by pasting the launch line from the role file into a fresh session.

## Current Step

**Round 2 comparative review is open.** Iteration 2 is built on branch
`prototypes/tax-citizen-families/it2` at commit `989d9fe`; examination is
`examination-it2.md`. Review scope is `reviews/round-2.md`.

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
| Reviewer: legibility | `roles/reviewer-legibility.md` | not opened | context-starved; owner launch for round 2 |

## Next Action

Round 2 unstarved reviews are complete and committed. The remaining open seat is
context-starved legibility; it must be owner-launched using
`roles/reviewer-legibility.md` and the scope in `reviews/round-2.md`. Foreman
conformance and outcome summaries wait until legibility lands or the owner
disposes without it.

## Planned Exhibits

- Tag `exhibits/tax-citizen-families/it1` - first candidate contract at
  `88f0139`.
- Branch `prototypes/tax-citizen-families/it2` - clean-room rival at `989d9fe`,
  available for round 2 review.
