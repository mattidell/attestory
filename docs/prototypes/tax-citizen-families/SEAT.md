# Tax Citizen Families Prototype - Seat File

This is the execution state for First Tax Slice Track 0. A fresh agent resuming
this project reads this file first when `docs/phase-state.md` points here. Do
not self-assign the foreman seat unless it is marked vacant; record any
succession in `process-log.md`.

Context-starved seats are not filled by generic resumption. The owner launches
them by pasting the launch line from the role file into a fresh session.

## Current Step

**Iteration 3 targeted repair is returned to the owner-launched builder for
mandatory closeout.** The branch has a clean checkpoint at `d5ace21`, but the
required `examination-it3.md`, R1-R13 evidence checklist, and gate-specific
harness increments are not present. Round 3 review is not open.

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
| Builder it3 | `roles/builder.md` | owner-launched it2 builder session | active; closeout required after checkpoint `d5ace21` |

## Next Action

Owner should return control to the same it3 builder session to complete the
charter. The builder must work only on branch
`prototypes/tax-citizen-families/it3`, finish gate-specific evidence for
R1-R13, correct the it3 README/handoff text, and write
`docs/prototypes/tax-citizen-families/examination-it3.md` with the required
R1-R13 path-and-command checklist. The foreman will then rerun verification and
open round 3. Per owner instruction, the foreman does not spawn a builder
subagent.

## Planned Exhibits

- Tag `exhibits/tax-citizen-families/it1` - first candidate contract at
  `88f0139`.
- Tag `exhibits/tax-citizen-families/it2` - clean-room rival at `989d9fe`.
- Branch `prototypes/tax-citizen-families/it3` - targeted repair branch opened
  from it2 at `989d9fe`.
