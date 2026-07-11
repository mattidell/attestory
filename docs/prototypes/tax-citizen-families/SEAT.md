# Tax Citizen Families Prototype - Seat File

This is the execution state for First Tax Slice Track 0. A fresh agent resuming
this project reads this file first when `docs/phase-state.md` points here. Do
not self-assign the foreman seat unless it is marked vacant; record any
succession in `process-log.md`.

Context-starved seats are not filled by generic resumption. The owner launches
them by pasting the launch line from the role file into a fresh session.

## Current Step

**Rival builder seat is open for owner launch.** Iteration 1 is concluded and
preserved as exhibit tag `exhibits/tax-citizen-families/it1` at `88f0139`.
Round 1 is closed. The next build is the clean-room rival on branch
`prototypes/tax-citizen-families/it2`.

## Seats

| Seat | Role file | Holder | Status |
|---|---|---|---|
| Foreman | `roles/foreman.md` | codex (planning session, 2026-07-11) | active |
| Builder it1 | `roles/builder.md` | `codex-builder-it1-2026-07-11` | complete; exhibit `exhibits/tax-citizen-families/it1` |
| Rival builder | `roles/builder-rival.md` | owner launch needed | open on branch `prototypes/tax-citizen-families/it2` |
| Reviewer: governance | `roles/reviewer-governance.md` | `codex-governance-r1-2026-07-11` | round 1 complete |
| Reviewer: expressiveness | `roles/reviewer-expressiveness.md` | `codex-expressiveness-r1-2026-07-11` | round 1 complete |
| Reviewer: adversary | `roles/reviewer-adversary.md` | `codex-adversary-r1-2026-07-11` | round 1 complete |
| Reviewer: legibility | `roles/reviewer-legibility.md` | owner-launched fresh session | round 1 complete |

## Next Action

The owner launches the rival builder with the launch line in
`roles/builder-rival.md`. Do not use a subagent for the builder role. The rival
builder reads only the role-permitted materials and works on branch
`prototypes/tax-citizen-families/it2`.

## Planned Exhibits

- Tag `exhibits/tax-citizen-families/it1` - first candidate contract at
  `88f0139`.
- Branch `prototypes/tax-citizen-families/it2` - clean-room rival, open for
  owner launch.
