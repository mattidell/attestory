# Retrospective — A Blocked Line Asks Its Yes-or-No Question (2025)

## Result

- **Every filer-answerable missing input now has a question.** On core v73
  a line blocked on one of 79 yes/no scope answers or filing status names
  what to answer. 41 filer questions cover the 80 facts.
- **"Yes" always means present** (owner direction). Most facts assert an
  absence; the question asks about presence and a "no" records the absence.
- **No schema change.** Content on #252's `input-question.v1`, and a
  presentation-only binding map for filing status.

## What the evidence changed

- **Questions reduce to meaning** (owner direction). Grouping facts a filer
  settles with one answer took 80 facts to 41 questions; the 24 direct
  foreign tax credit facts became 12 questions.
- **The first draft asked for conclusions.** "Are you required to file Form
  1116?", "Do you owe an estimated tax penalty?" and "Are you claiming the
  QBI deduction?" each let a filer answer "no" and publish $0. The review
  turned each into facts a filer can check.
- **A catch-all clause lied.** S1A's "any other Schedule 1 adjustment"
  swept in student loan interest, which the engine computes.
- **Tracing beat drafting.** Three sentences changed once the rule that
  reads the fact was traced (FTC10/FTC12, L2A2, DEP1/DEP2).

## Process

- Two owner directions arrived while P0 ran; both reached the builder by
  message and plan amendment without restarting it.
- A wording review by a fresh reader found what the builder's own regex
  could not.

## Follow-ups

- Derive the answers the return already implies instead of asking them
  (Form 1098 scope, line 2a Form 1099-INT, other dependents, and in part
  Form 1116 and the capital-gain facts).
- A recording surface for group questions that does not fabricate a value
  for each member.
