# Charter: repair of every earned income credit answer has a question

Role: Builder. Source HEAD on milestone/eic-answer-questions-2025.
Plan: docs/phases/engine-breadth/milestones/eic-answer-questions.md
(Decision 5). Review: docs/reviews/eic-answer-questions/review.md. Do not
read governance.

v100 is not on main, so its files are regenerated in place on this
branch (core v100, registry v98, release v98 keep their numbers;
checksums and digests are regenerated).

## Scope

1. **Texts.** In the evidence design script, set three question texts to
   exactly these, and leave the dependent question unchanged:

   Age:

   > Were you, or your spouse if you file a joint return, at least age 25 but under age 65 at the end of 2025? Answer yes if you, or your spouse if you file a joint return, were born after December 31, 1960, and before January 2, 2001, with one exception: if that person died in 2025, answer yes for them only if they were at least age 25 but under age 65 at the time of death. A person is considered to reach age 25 on the day before their 25th birthday, and age 65 on their 65th birthday.

   Main home:

   > Was your main home, and your spouse's if you file a joint return, in the United States for more than half of 2025? Your main home can be any place where you regularly live, such as a house, apartment, shelter or temporary lodging, and it need not be the same place all year. The United States means the 50 states and the District of Columbia, not Puerto Rico or a U.S. territory. If you, or your spouse on a joint return, were on extended active military duty outside the United States (duty ordered for an indefinite period or for more than 90 days), count that time as time that person's main home was in the United States.

   Spouse SSN:

   > Does your spouse's Social Security number allow your spouse to work in the United States? Answer yes if it was issued by the Social Security Administration on or before the due date of your 2025 return (including extensions) and is not marked "Not Valid for Employment", or if it is marked "Valid for Work Only With DHS Authorization" and that authorization is still valid. Answer no if your spouse has only an individual taxpayer identification number (ITIN) or no number.

2. **Regenerate** v100/v98/v98 through the validating generator; confirm
   by diff that only the three question texts and the checksums and
   digests that depend on them changed.
3. **EAQ-R2.** Add a test that pins the dependent question's polarity:
   its text asks whether the filer can be claimed, the fact it names is
   the not-claimable fact, and a recorded "not claimable = no" (what a
   yes records) stops the credit live, while "yes" lets it continue.
   Follow how the existing qualifying-child-of-another question is
   tested, if it is. Confirm the test fails when the polarity is reversed
   in a scratch copy.
4. **Tests and docs.** Update any test that pins the three texts; add a
   live case for a spouse who died in 2025 before age 25 if the probe can
   express it, otherwise say so. Run the milestone modules,
   `tests/test_schema_registry.py`, the v78 switch test, `pytest -m "not live"`
   and `python3 -m mypy`; put the result lines and a Repair section in
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
