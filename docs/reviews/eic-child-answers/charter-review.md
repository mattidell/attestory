# Charter: fresh review of a counted child's missing credit answer is asked

Role: Reviewer, fresh context. Source HEAD on
milestone/eic-child-answers-2025. Plan:
docs/phases/engine-breadth/milestones/eic-child-answers.md (read it
whole). ADR: docs/adr/0087-question-walk-follows-roster-members.md
(proposed). Evidence: eic-child-answers-evidence/p0.md, track1.md,
scripts and JSON. Range: `github/main..HEAD`. Do not read governance.

## Questions

1. **The walk against ADR 0087.** Does `_closure_question_reasons` follow
   a member key only as Decision 1 says, and attach a question only when
   every root (each followed member included) resolves? Can it attach a
   question that is not the reason the line blocks, attach one member's
   question to another member, or show a partial explanation? Does a
   member with no rows, or two labels, stay silent? Are saved pages of
   cores up to v100 unchanged (the replay compares two cores under the
   same code, so it cannot show this; test it directly)?
2. **The label.** Is `member_label` only the member's own recorded label,
   escaped on the page, and never a value, path or id? Is snake_case
   right beside the existing camelCase keys (`statementLabel`,
   `responseLabel`)? Say which name to use.
3. **The 26 questions, adversarially.** Is each true to the 2025 Form
   1040 instructions (line 27a, Dependents, credit for other dependents)
   and the Schedule 8812 instructions (Track 1 fetched them into the
   ignored temp/eicc-sources/)? Every condition and example is a claim;
   check each against a source line. Read the whole rule section, including
   exceptions after the first sentence (a child born or who died in 2025, a
   temporary absence, a kidnapped child, a permanently disabled child of any
   age, a student, the sheltered-workshop exception). For the three
   questions whose yes records the fact's no, confirm the recorded
   polarity is right and a test fails if it is reversed.
4. **Nothing else moved.** Does every fully answered return compute as
   on v100? Is anyone newly asked something they were not required to
   answer on v100?
5. **Publication.** Only new files under packages/content and the release;
   no published file modified; loader v101 entries carry v100's.
6. **Tests.** Do the tests fail if the walk stops following members, if a
   label is swapped between two members, if a question is dropped, or if
   a polarity is reversed? Mutate in a scratch copy; do not commit
   mutations.

## Output

docs/reviews/eic-child-answers/review.md: a verdict (READY, READY with
notes, or NOT READY; ADR 0087 acceptance is the owner's and is not part of
your verdict), numbered findings (ECA-R1 …) each with file:line, a
concrete failure scenario and a severity, and what you ran. Commit it
under `$(git rev-parse --git-dir)/collaboration-commit.lock` with
separate simple commands (mkdir lock; git add that one path; git commit
-F file; rmdir lock). Bound every command that can hang; never `rm -rf`.
No code edits, no push, no spawn. Synthetic demo.* only; no absolute
paths in committed files.
