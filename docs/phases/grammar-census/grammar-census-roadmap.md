# Grammar Census Phase — Roadmap

Audience: Product (roadmap); Shared (status)

Status: **active phase, opening milestone PLANNED 2026-08-19.** The plan is
committed and was approved in direction by the owner, then repaired the same
day. No track has started.

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

- **State:** PLANNED. Branch `milestone/grammar-census-engine-language-map`,
  primary worktree `engine-worktree-2`, based on `origin/main` at `20cf03ab`.
- **Plan:** `milestones/engine-language-map.md`.
- **Implementation notes:** none — no track has started.
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
- **Lessons learned:** none yet.
- **Part of the project impacted:** documentation only. The milestone reads
  schemas, runtime code, packages, and tests as evidence and changes none of
  them. The one possible non-documentation artifact is an optional
  reproducibility script at `tools/grammar_census.py`, which may not alter
  production behavior, published schemas, or tax content.
