# Retrospective: Every Unconfirmed Family Asks Its Question (2025)

Milestone key: closure-question-coverage. Plan:
`docs/phases/engine-breadth/milestones/closure-question-coverage.md`.
Closed 2026-11-04.

## What happened

A parked note named two Form 1099-B families that never showed their
completeness question. P0 surveyed all 51 families core v74 reads and found
a third case (Form 1099-K's selection lines), and traced the wash-sale cause
to the substrate. Synthesized member validation is checked before
`require_closed`, and it reported an unconfirmed family as missing input.
P0 stopped on the engine condition. The owner chose an engine fix from v75
only and included the projection change. Track 1 put both behind one
version switch, and the review found no required fixes.

## What worked

- Surveying every family instead of fixing the two known ones turned up
  the third case, and confirmed the other 48.
- Stopping at P0 on the engine condition, with the cause traced, made the
  owner's decision a two-question choice.
- One switch read by both the runner and the projection kept earlier cores
  unchanged without a schema.

## What to change

- A version switch in the domain loader that the substrate imports works,
  but it is a second place where package-version behaviour lives (after
  companion declarations). If more switches follow, declare them in
  package content.

## Follow-ups

- Pass the switch into the run rather than importing it in the runner.
- The two wash-sale adjustment questions' wording.
