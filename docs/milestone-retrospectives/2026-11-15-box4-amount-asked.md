# Retrospective: The Box 4 Withholding Amount Is Asked (2025)

Milestone key: box4-amount-asked. Plan:
`docs/phases/engine-breadth/milestones/box4-amount-asked.md`.
Closed 2026-11-15 on P0.

## What happened

preferential-base-reason P0 reported that Form 1040 lines 25b and 25d
block with no question when a Form 1099-B box 4 amount is missing, and
the item was parked. This milestone opened to add the question. P0 ran
the plan's cases on published core v91 and found the question already
there: line 25b blocks on the amount fact, the projection attaches the
published amount prompt, and lines 25d, 33, 34, 35a and 37 show it too.
Entering the amount reaches the instruction values. The earlier probe
counted a sentence as a question only if it contained a question mark,
and the amount prompt is an imperative ("Enter the federal income tax
withheld …"). No paired withholding amount on v91 lacks both an input
question and a closure question. Nothing was built.

## What worked

- A P0 that reproduces before it designs. The defect did not survive
  reproduction, at the cost of one builder turn and no Track 0 or build.
- Asking P0 to reconcile two committed statements that disagreed (the
  core v83 roadmap entry and the parked item).

## What to change

- Evidence probes read the projection's reason and question lists as
  published; they do not classify sentences by punctuation. The
  blocked-names-question and preferential-base-reason probes both keep
  only sentences with a question mark. Their repaired fields were
  identified through an inapplicable or name-less producer and their
  tests check the named questions on the published package, so their
  results stand, but a field counted there as showing no question may
  have shown an imperative prompt. A later milestone that reuses those
  probes replaces the filter first.
- Before parking a "no question" finding, look at the field's sentences
  on the page model, not at a filtered list.

## Follow-ups

Parked in the roadmap: a filer who answered the box 4 yes/no "no" is
still shown the amount prompt until they enter $0.
