# Retrospective: Each Statement Is Checked For Its Own Withholding (2025)

Milestone key: statement-withholding-pairing. Plan:
`docs/phases/engine-breadth/milestones/statement-withholding-pairing.md`.
Closed 2026-11-05.

## What happened

A parked note said line 25b's count check could be fooled. P0 reproduced
it through the real coordinator on core v76: eleven reachable returns
published a wrong amount, ten on line 25b and one on line 25a (W-2), the
same gap. P0 found a content-only design, but it replaced the missing-amount
question with the income statement's id and needed two facts that nothing
records. The owner chose a guard operation instead and included line 25a.
Track 1 added `require_paired` with `rule-artifact.v15` and ADR 0083
(proposed); the review found no required fixes.

## What worked

- Reproducing every case against a hand-computed answer showed the gap was
  twice as wide as the note (the other-box statements published 0) and
  reached line 25a.
- Checking what the filer would see, not only the amount, caught that the
  content-only design lost the existing question.
- Naming the missing withholding fact in the block kept the v72 input
  questions working with no new wording.

## What to change

- P0 cost more than usual ($14.77) because it built a full content
  prototype before the owner decision. When P0 can see an engine option is
  likely, a sketch of both shapes is enough for the decision.

## Follow-ups

- The owner's decision on ADR 0083.
- Name which statement is short, not only its kind.
