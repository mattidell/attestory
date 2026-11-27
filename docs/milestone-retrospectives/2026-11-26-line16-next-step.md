# Retrospective: A Required Schedule D With No Sale Says What To Do Next

Milestone key: line16-next-step. Plan:
`docs/phases/engine-breadth/milestones/line16-next-step.md`.
Closed 2026-11-26. Content and projection (ADR 0091): core v109.

## What happened

line16-names parked L16-R2: when a return requires Schedule D, no sale is
recorded and the filer's Exception 1 "no" answers are right, no answer on
the page unblocks line 16, and the page did not say so. P0 found no
existing citizen that could hold a sentence about an answer, so the owner
accepted ADR 0091: a new `answer-explanation.v1` citizen, shown as an
unlinked reason in the "Why:" list (placement A). Core v109 adopts four
sentences, one per Exception 1 "no". 801 lists replay with no number,
disposition or code change; 25 gain an explanation.

The build was adopted across a Claude session limit and two Codex usage
limits, and ran beside statement-question-labels and same-label-ordinal,
which change the same projection function. Those merged first; this
branch was rebased onto both and its replay re-run on the new base.

## What worked

- Merging the three parallel milestones one at a time, and re-running
  each later one's replay on the new base, kept every replay claim tied
  to the code it would merge into.

## What to change

- Three milestones in parallel on one function cost two hand-resolved
  rebases. Run work that touches `_closure_question_reasons` one at a
  time, or merge each as soon as it is ready.
- The replay accepted any approved sentence without checking its line
  and answer (L16-T1), the same class of gap as SQL-R1 in
  statement-question-labels. A replay of added text must check where the
  text may appear, with a control that puts it somewhere it must not.
- The schema-intent ledger had not been used since 2026-10-03. The
  builder's handoff caught it; the foreman should record intents when a
  plan names a new schema version.
