# Charter: repair of the separated-spouse question is asked only of a married filer

Role: Builder. Source HEAD on milestone/eic-separated-married-2025.
Plan: docs/phases/engine-breadth/milestones/eic-separated-married.md (read
it whole; Decision 8 binds). Review: docs/reviews/eic-separated-married/
review.md (ESM-R1 to R3; each finding's repair is in scope). Do not read
governance.

## Scope

1. **Question text (R1, R2).** Rewrite `input-question.eic-married-taxpayer`
   v1 and the fact type's description in the bundle to state the
   instructions' marital test (quote the 2025 Form 1040 instructions Head of
   Household text on decrees and "considered unmarried", Step 3 question 3,
   and Publication 596 Rule 3), and that "no" continues to question 6.
   Check each case the review names (interlocutory decree; final decree of
   separate maintenance with a shared household; lived apart and considered
   unmarried) answers the question as worded to the result the sources give.
2. **Inert path (R3).** Make a stored `eic.married-taxpayer-inert` fact
   unable to change line 27a or trip the exclusive-presence refusal, in
   both rules that carry the path. Prefer a path value equal to the default;
   otherwise refuse the fact at assertion. Say which and why.
3. **Regenerate** v103 (registry v101, release v101) in place; it is not on
   main. Loader entries unchanged except checksums the generator writes.
4. **Tests.** Live tests for the review's reproductions (interlocutory
   decree, final decree with shared household, stored inert fact with and
   without a separated-spouse answer), each against the sources' result;
   the review's mutants fail a test. Fast lane (includes
   tests/test_content_file_sizes.py after rebase onto main), the touched
   live tests, mypy. Full-surface replay v102 against v103: 0 unexpected,
   no number changes.

## Deliverables

Content, package, release and tests; track1.md gains a "Repair" section;
the plan's Track 1 result notes the repair. Commit in steps.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Do not edit packages/kernel/ or the engine. Stop and report if the repair
  needs more.
- Commit with separate simple commands (mkdir lock; git add <paths>;
  git commit -F file; rmdir lock) under
  `$(git rev-parse --git-dir)/collaboration-commit.lock`.
- Bound every command that can hang; never `rm -rf`.
- Write your JSON report before your final checks; update it when done.
- Never --no-verify or a bare git stash. Foreground commands only; leave
  no background jobs. No push and no spawn.
