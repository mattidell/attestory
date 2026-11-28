# Retrospective: Each Sale Question Names Its Sale

Milestone key: sale-question-names. Plan:
`docs/phases/engine-breadth/milestones/sale-question-names.md`.
Closed 2026-11-27. Projection and page (ADR 0089 third amendment); core
v109 unchanged.

## What happened

ADR 0089 parked naming a sale with no Form 1099-B. P0 found that the sale
entity's recorded label reaches the proceeds, basis and wash-sale
questions through the pinned pairing, the published amount disagreement
or the per-sale validation witness. The owner accepted the amendment the
same day; the basis consistency route, whose rule does not say which
amount disagrees, stays generic. The page now prefixes a box C or F sale
question with the sale's label when the return has more than one such
sale and the label is unique among its peers. No recorded list changes;
7 synthetic lists gain 352 names. The repair was resumed across a Codex
usage limit.

While reviewing the shape, the owner asked why a no-1099-B sale records
its amounts both on the sale and in per-column facts. ADR 0054 added the
per-column facts before field reads and per-subject results existed. The
owner directed that amounts be captured once, with any second
representation crossing a named boundary; the question is open in the
roadmap.

## What worked

- Charter lessons from the two earlier ADR 0089 milestones (pins,
  successor and older cores, every replay acceptance path) held: the
  review found no core-pin or successor gap.

## What to change

- Three of six findings were about inputs agreeing across layers: peer
  currency, witness payload against its id, and blankness in four
  places. A label charter should name one shared rule for text tests and
  ask for a test that each layer uses it.
- A replay should pin its baseline census and error set, not only the
  differences, so a matching failure on both sides cannot pass.
