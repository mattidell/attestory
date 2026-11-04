# Retrospective — A Blocked Line Names What Is Missing (2025)

## Result

- **The filer is told what to enter.** On core v72 a line blocked because
  W-2 box 2, a Form 1099 box 4, SSA-1099 box 6, or the line 26 or 36 amount
  is missing shows a declared question that says what to enter and that a
  blank box is $0, instead of "Missing dependency code(s):
  DEPENDENCY_ABSENT". A line with a missing amount and an unconfirmed family
  names both.
- **Two new schemas, owner-approved:** `input-question.v1` and
  `artifact-package.v39`, admitted at the same points the closure-question
  schema needed. Earlier cores render byte-identically.

## What the evidence changed

- **No usable wording existed anywhere.** P0 searched fact types, question
  bundles, recorders and the entry loop: the only declared filer sentence
  was a family's closure question, which never says $0 is an answer. Fact
  titles are engineering prose. Naming a missing input meant writing it.
- **The catalogue was larger than the gap that prompted it.** 88
  answerable roots across 72 lines; 79 are yes/no scope answers. Eight
  amounts were the useful first class.
- **A rule names one cause.** A named reason can still hide a second
  missing input behind the first; the filer sees it once the first is
  answered.

## Process

- P0 stopped on its schema stop condition and the owner chose the design
  and class in one question.
- The admission list the charter named missed one place
  (`packages/derivation/loader.py`'s role vocabulary) and one test listed
  every package schema; both were found by building and by the full suite.

## Follow-ups

- Questions for the 79 yes/no scope answers and filing status.
- Name the statement, not only its kind (keyed join).
- The two `f1099b.covered-w-*` families block `DEPENDENCY_ABSENT` on an
  unconfirmed closure, so their question is never shown.
