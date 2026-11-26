# Retrospective: Each Form 1099-B Statement Question Names Its Statement

Milestone key: statement-question-labels. Plan:
`docs/phases/engine-breadth/milestones/statement-question-labels.md`.
Closed 2026-11-26. Projection only (ADR 0089).

## What happened

P0 found that the saved page asked the per-statement Form 1099-B box 4
amount and box 7 questions once per statement with the same words. The
reason schema already admitted `statementLabel`, so the route was a
projection change, but deciding which statement a missing answer belongs
to needed a contract: ADR 0089, accepted by the owner. Track 1 labels the
question through the evaluator's own pairing test and a box 4 need table
gated to core v106 or later. All 775 recorded lists and 18 P0 cases
replay with no number, disposition or code change; 141 lists gain labels.

The Track 1 builder was adopted twice across usage limits (a Claude
builder, then Codex) and finished on the tested commit; the foreman left
the rest of the local suite to CI `verify`.

## What worked

- Reusing the evaluator's pairing function rather than a copy kept the
  page and the run from disagreeing about which statement is meant.

## What to change

- A replay that compares by folding labels back to the original sentence
  passes whether or not the labels appear (SQL-R1). When a change adds
  text, the comparison must assert the added text and its count, with a
  control that removes it.
- A resume cache keyed only to package content can reuse results from
  older code (SQL-R2). Key evidence caches to the code under test too, or
  do not resume.
