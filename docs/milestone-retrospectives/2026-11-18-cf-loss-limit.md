# Retrospective: Box C and F Losses Are Limited (2025)

Milestone key: cf-loss-limit. Plan:
`docs/phases/engine-breadth/milestones/cf-loss-limit.md`.
Closed 2026-11-18. Tests only; no package, engine or schema change.

## What happened

The parked list said the married-filing-separately loss limit and the
2026 carryover were not exercised for Form 8949 boxes C and F. P0 (a
Claude Opus builder) ran 90 synthetic returns across all five filing
statuses: 900 of 900 line checks matched hand values from the 2025
Schedule D instructions, and every C/F return equalled its A/D control.
It also found the plan had asked for something accepted ADRs forbid:
no box publishes a 2025-to-2026 carryover (ADR-0058 and ADR-0060
Decision 7). The foreman narrowed the milestone to the limit and parked
the carryover as an owner question. A Claude Sonnet builder pinned 30
returns as tests against the hand values, with a boundary test that no
2026 carryover is published. The fresh review confirmed the hand values
and killed four mutations with the tests; its notes were wording and
counts, repaired by the foreman.

## What worked

- Testing against hand values and an independent box A/D control, not
  against captured engine output.
- P0 reading the rule's own notes and the ADRs before computing a
  carryover nobody publishes.

## What to change

- The foreman wrote "the right 2026 carryover" into scope from the
  parked note without checking the accepted ADRs. When a parked item
  names an amount, check whether an ADR bounds it before chartering.
