# Charter: repair of a counted child's missing credit answer is asked

Role: Builder. Source HEAD on milestone/eic-child-answers-2025.
Plan: docs/phases/engine-breadth/milestones/eic-child-answers.md
(Decision 7). Review: docs/reviews/eic-child-answers/review.md (ECA-R1,
R2, R4, R5, R6). ADR 0087 (proposed; now names `memberLabel`). Do not read
governance.

v101 is not on main, so its files are regenerated in place on this branch
(core v101, registry v99, release v99 keep their numbers).

## Scope

1. **ECA-R1.** Add the kidnapped-child rule to the EIC residency, child
   tax credit lived-with-you and relative over-half-support questions, in
   the words of the cited source lines (i1040gi 1916-1920, 4462-4464; Pub.
   596 1241-1254): a child presumed kidnapped by someone not a family
   member is treated as meeting the test for the part of the year before
   the kidnapping, when the conditions the source states hold. State those
   conditions; do not paraphrase them away.
2. **ECA-R2.** The age question's full-time-student definition adds that
   school does not include on-the-job training courses, correspondence
   schools, or schools offering courses only through the internet
   (i1040gi 4792-4794).
3. **ECA-R4.** The residency question's military note says that once
   extended active duty begins, it counts even if fewer than 90 days are
   served (i1040gi 4806-4808).
4. Quote the source lines for each changed text in track1.md's Repair
   section; change no other question.
5. **ECA-R5.** Rename the reason field `member_label` to `memberLabel` in
   the projection, the validator, the page and the tests.
6. **ECA-R6.** Add a unit test that a member with two recorded labels
   leaves the line silent, and confirm it fails on a scratch copy with the
   guard removed.
7. **Regenerate** v101/v99/v99 through the validating generator; confirm
   by diff that only the changed question texts and dependent checksums
   and digests changed. Re-run the probe replay and the 775-list replay.
8. **Checks.** The three milestone test modules, `tests/test_input_questions.py`,
   `tests/test_schema_registry.py`, the v78 switch test,
   `pytest -m "not live"` and `python3 -m mypy`; result lines in
   track1.md.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included. Never edit a file published on main.
- Commit with separate simple commands (mkdir lock; git add <paths>;
  git commit -F file; rmdir lock) under
  `$(git rev-parse --git-dir)/collaboration-commit.lock`.
- Bound every command that can hang; never `rm -rf`. Never raise a
  fast-lane budget or size cap.
- Write your JSON report before your final checks; update it when done.
- Never --no-verify or a bare git stash. Foreground commands only. No
  push and no spawn.
