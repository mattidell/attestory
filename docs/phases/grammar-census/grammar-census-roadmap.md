# Grammar Census Phase — Roadmap

Audience: Product (roadmap); Shared (status)

Status: **active phase, opening milestone CLOSED 2026-08-20.** The plan was
committed and approved in direction by the owner 2026-08-19, repaired the
same day, then executed through all three tracks (0, 1a/1b/1c, 2/2b, 3) and
closed with all eight exit criteria met. See
`docs/phases/grammar-census/final-report.md` and
`docs/phases/grammar-census/exit-criteria-assessment.md`. The phase remains
open; the next milestone is unselected and owner-held.

## Thesis

The engine's declarative language accumulated a capability at a time, as tax
milestones demanded them. Nobody has yet read it as one object. Before the
project extends that language again, or measures it against how other systems
express rules, it should be able to say plainly what language it already has —
and be able to show the evidence for each part of that answer.

## Milestone sequence

1. **Engine Language Map** (`grammar-census`) — the opening milestone.
   Delivers the boundary map between grammar and grammar-adjacent machinery,
   three independently-read construct sets reconciled against one another, a
   small set of traces from declared syntax to observable consequence, a
   catalog of tensions that could support later action, and a bounded brief
   scoping a future comparison with external rule languages. It matters
   because every later choice about the language — extend it, replace part of
   it, borrow from elsewhere, or leave it alone — currently rests on an
   account nobody has verified. It is sequenced first because it is the
   cheapest way to make those later choices real rather than speculative.

No further milestone is selected. **The phase stays open after Milestone 1
closes.** The owner chooses among the bounded options that milestone presents:
comparative review, a focused grammar decision or build, further internal
verification, or stop.

## Status

### Engine Language Map (`grammar-census`)

- **State:** CLOSED 2026-08-20. Branch
  `milestone/grammar-census-engine-language-map`, primary worktree
  `engine-worktree-2`, based on `origin/main` at `20cf03ab`, merged with
  `origin/main` at `226bf499` (Claim Boundary Exploration close, PR #182)
  before its own PR.
- **Plan:** `milestones/engine-language-map.md`.
- **Implementation notes:** Track 0 (boundary map and bounded corpus, five
  repair rounds, `4f66bc83`); Tracks 1a/1b/1c (three isolated construct-set
  readings, 108/90/84 constructs, `983b6102`/`495adeac`/`bb5ea26b`); Track 2
  (adversarial reconciliation, 166 constructs, `f276cc5b`) plus Track 2b
  (representative traces and tension catalog, `3dba1a80`/`5ba385c1`); Track 3
  (plain-language map and bounded comparison brief, `4dbc23e3`/`3bd1c5bd`).
  Full deliverable index and per-criterion assessment in
  `docs/phases/grammar-census/exit-criteria-assessment.md`.
- **Pivots:** one bounded planning repair on 2026-08-19, before dispatch. It
  added the plan's required metadata status, explicit Scope and Non-goals
  sections, the Parallel Work Manifest for Tracks 1a–1c, and named paths for
  every working deliverable; narrowed Track 1c to observed usage only, moving
  all set-difference claims to Track 2; changed Track 0's representational-gap
  handling from a stop condition to a record-and-continue; bounded
  claim-boundary evidence to merged CQ-1 as a validation lens for Tracks 2–3
  only; removed committed dispatch authorization from phase state; and
  resolved the phase-lifecycle contradiction in favor of leaving the phase
  open. The substantive census objective was not changed.
- **Lessons learned:** see
  `docs/milestone-retrospectives/2026-08-20-grammar-census-engine-language-map.md`
  — a Foreman ruling's own reasoning was falsified by adversarial evidence
  the milestone itself produced, corrected on the record rather than
  absorbed; incremental committing survived two unplanned process kills with
  minimal loss.
- **Part of the project impacted:** documentation only. The milestone reads
  schemas, runtime code, packages, and tests as evidence and changes none of
  them. The one possible non-documentation artifact is an optional
  reproducibility script at `tools/grammar_census.py`, which may not alter
  production behavior, published schemas, or tax content.
