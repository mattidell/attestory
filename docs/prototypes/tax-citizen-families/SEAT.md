# Tax Citizen Families Prototype - Seat File

This is the execution state for First Tax Slice Track 0. A fresh agent resuming
this project reads this file first when `docs/phase-state.md` points here. Do
not self-assign the foreman seat unless it is marked vacant; record any
succession in `process-log.md`.

Context-starved seats are not filled by generic resumption. The owner launches
them by pasting the launch line from the role file into a fresh session.

## Current Step

**The narrow prototype decision is ratified and the prototype process is
complete.** The owner accepted Tier 2 ADR-0011 and ADR-0012 on 2026-07-11. The
broad prototype loop remains closed. First Tax Slice must be replanned to the
ratified scope before implementation begins.

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
| Builder it4 | `roles/builder.md` | owner-launched builder session | complete; exhibit `exhibits/tax-citizen-families/it4` |
| Reviewer: governance | `roles/reviewer-governance.md` | `Ampere` (`019f53df-8003-7131-860a-86b43dabb107`) | round 4 complete |
| Reviewer: expressiveness | `roles/reviewer-expressiveness.md` | `Lorentz` (`019f53df-7f81-7f01-8873-67ebffb46ce5`) | round 4 complete |
| Reviewer: adversary | `roles/reviewer-adversary.md` | `Harvey` (`019f53df-80d1-7470-b663-cdd74a312710`) | round 4 complete |
| Reviewer: legibility | `roles/reviewer-legibility.md` | owner-launched fresh session | round 4 complete |

## Next Action

Foreman or planning agent amends the First Tax Slice milestone plan and roadmap
to the ratified narrow scope in a separate planning commit before creating the
milestone execution branch. Proposed economic gates remain recommendations
until the owner ratifies a `PROJECT_PLANNING.md` amendment.

## Planned Exhibits

- Tag `exhibits/tax-citizen-families/it1` - first candidate contract at
  `88f0139`.
- Tag `exhibits/tax-citizen-families/it2` - clean-room rival at `989d9fe`.
- Tag `exhibits/tax-citizen-families/it3` - targeted repair candidate at
  `be72d63`.
- Tag `exhibits/tax-citizen-families/it4` - bounded integration proof at
  `9debc4d`.
