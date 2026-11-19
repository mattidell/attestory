# Retrospective: Gains and Break-Even Sales Reach Schedule D (2025)

Milestone key: gain-break-even. Plan:
`docs/phases/engine-breadth/milestones/gain-break-even.md`.
Closed 2026-11-19. Tests only; no package, engine or schema change.

## What happened

The parked list carried a one-line item, "Gain and break-even reporting
on Form 8949 and Schedule D", with no detail. P0 (a Claude Opus builder)
recorded every coordinator run in the 94 relevant test files: every
sale path had run a gain and a break-even, but only on cores v11 to v94,
none on v96, and the long-term no-Form-1099-B break-even never. Its 54
synthetic returns on v96 matched hand values on all 1,134 checks; the
code W gain blocks by ADR-0062 Decision 2. A Claude Sonnet builder
pinned 27 returns. The fresh review found the code W probe passed for
the wrong reason (a second rule also blocks), repaired by asserting the
page sentence.

## What worked

- Recording runs from the existing suite instead of reading test names:
  it showed where gains ran and on which core.
- Checking ADRs and rule notes for a bound before calling a block a
  defect, as the cf-loss-limit retrospective asked.

## What to change

- When a rule can be blocked by more than one cause, a test of "it
  blocks" proves little; assert the cause the filer sees.
- A parked item with no detail is cheapest to retire with a census
  first; most of this one was already done.
