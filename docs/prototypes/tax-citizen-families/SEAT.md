# Tax Citizen Families Prototype - Seat File

This is the execution state for First Tax Slice Track 0. A fresh agent resuming
this project reads this file first when `docs/phase-state.md` points here. Do
not self-assign the foreman seat unless it is marked vacant; record any
succession in `process-log.md`.

Context-starved seats are not filled by generic resumption. The owner launches
them by pasting the launch line from the role file into a fresh session.

## Current Step

**Iteration 4 bounded integration proof is open for owner-launched builder.**
The owner authorized the recommended continuation at the three-iteration
disposition point. Branch `prototypes/tax-citizen-families/it4` starts from
exhibit it3 at `be72d63` and is governed by `charter-it4.md`.

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
| Reviewer: governance | `roles/reviewer-governance.md` | `Lovelace` (`019f5384-e415-7691-af20-9fbe46907be3`) | round 3 complete |
| Reviewer: expressiveness | `roles/reviewer-expressiveness.md` | `Nietzsche` (`019f5384-e48f-7403-a906-71a39169e794`) | round 3 complete |
| Reviewer: adversary | `roles/reviewer-adversary.md` | `Hume` (`019f5384-e559-7673-87f9-1fba1b904f68`) | round 3 complete |
| Reviewer: legibility | `roles/reviewer-legibility.md` | owner-launched fresh session | round 3 complete |
| Builder it4 | `roles/builder.md` | not opened | owner launch pending; bounded integration proof |

## Next Action

Owner launches the it4 builder in a fresh session using `roles/builder.md` and
`charter-it4.md`. Work only on branch
`prototypes/tax-citizen-families/it4`; produce final artifacts under `it4/` and
write `examination-it4.md` with the I1-I9 checklist. Per owner instruction, the
foreman does not spawn a builder subagent.

## Planned Exhibits

- Tag `exhibits/tax-citizen-families/it1` - first candidate contract at
  `88f0139`.
- Tag `exhibits/tax-citizen-families/it2` - clean-room rival at `989d9fe`.
- Tag `exhibits/tax-citizen-families/it3` - targeted repair candidate at
  `be72d63`.
- Branch `prototypes/tax-citizen-families/it4` - bounded integration proof
  opened from exhibit it3 at `be72d63`.
