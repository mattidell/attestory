# Charter: fresh review of Track 1, statement question labels

Role: Reviewer. Source HEAD on milestone/statement-question-labels-2025.
Plan: docs/phases/engine-breadth/milestones/statement-question-labels.md
(Decisions 1-6 and "Track 1 result"). ADR: docs/adr/0089 (accepted).
Built unit: commits after 9d3c2e2fa. Do not read governance or the
builder's thread.

## Questions

1. Does each per-statement Form 1099-B box 4 amount and box 7 question
   carry `statementLabel` only when the evaluator's own pairing test
   (`require_paired`, not a copy) attributes it to one statement? Does
   it fail closed (original sentence, no label) when attribution is
   ambiguous?
2. Is the box 4 need table in packages/tax gated to core v106 or later,
   and is every other form left unchanged (Decision 2)?
3. Is a single statement labelled (Decision 4), and do two statements
   with one label keep two reasons (Decision 5)?
4. Do question links, `reasonIndices`, sorting, the page and the
   observation tool still agree after labels are added?
5. Do the tests fail on the parent code where they claim? Is the replay
   comparison strict, and do its totals hold (775 lists and 18 P0 cases,
   0 unexpected; 141 lists gain labels)?
6. Evidence prose: accurate, plain, no absolute or temp paths, demo.* only.

## Evidence ceiling and rules

Read and run targeted tests only (`pytest tests/<file>`); do not run the
full suite or the replay. Run `python3 tools/envelope_scan.py --range
github/main..HEAD`. Make no edits and write no files. Put the whole report
in your final message: READY or NOT READY, then findings (id SQL-R<n>,
severity, file:line, one line, failure scenario). No push, no spawn, never
rm -rf, never --no-verify.
