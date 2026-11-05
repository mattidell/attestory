# Retrospective: Every Question At Once (2025)

Milestone key: all-questions-at-once. Plan:
`docs/phases/engine-breadth/milestones/all-questions-at-once.md`.
Closed 2026-11-04.

## What happened

P0 drove six starting returns through the real coordinator on core v75,
answering every question shown each round, and counted rounds: up to six.
Of 29 questions that appeared after round one, 12 were knowable in round
one. Two causes hid them: consumers that read a family only after an
earlier block, and an `any` that stops at its first blocked `count`. A
prototype of a content-plus-evaluator fix cut the rounds. The owner chose
that fix from core v76. Track 1 matched the prototype and beat it on
foreign tax; the review found no required fixes.

## What worked

- Measuring rounds per start gave a number the owner could decide on, and
  the same probe became Track 1's acceptance test.
- Splitting late questions into knowable and truly conditional kept the
  fix from asking anything early that depends on an earlier answer.
- The presence guard (a later amount only when a statement is recorded)
  kept the evaluator change from asking a return with no W-2 for box 2.

## What to change

- The round test runs the whole loop on two cores and takes about six
  minutes. It is a live test; a smaller fixture per start would keep it
  cheaper.
- This is the second loader version switch the substrate imports. A third
  should move them into package content.

## Follow-ups

- The four subtotals that block with no filer question (parked).
- Pass the version switches into the run, or declare them in content.
