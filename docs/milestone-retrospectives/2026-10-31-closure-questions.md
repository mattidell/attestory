# Retrospective — A Blocked Line Names Its Question, Built (2025)

## Result

- **The filer is told what to confirm.** On core v69 a line held only by
  unconfirmed families names their questions ("Have you recorded every
  federal income tax withheld amount in box 4 of every Form 1099-G you or
  your spouse received for 2025?") instead of a generic "blocked" and a family
  id. All 51 closures have one.
- **Earlier cores render exactly as before**, checked byte for byte.

## What the evidence changed

- **A schema successor travels.** The mapping schema needed the package
  schema (`artifact-package.v37`) and four admission points, and two of
  those points in the validator were gated by exact package-schema tuples
  that would have skipped v69's checks silently. Each exact-version list is a
  place a successor can vanish without an error.
- **Writing the questions was the product work.** The first draft was
  correct and inconsistent; the review found three that misled a filer
  (scope words the engine uses and a filer does not). A question is judged by
  what a filer would answer, not by whether it matches the family's title.

## Process

- One builder across three tracks and two repairs; the foreman read all 51
  questions before the review and sent a wording pass first.

## Follow-ups

- Lines with a mixed cause keep the generic text; naming the non-closure
  cause too is a further step.
