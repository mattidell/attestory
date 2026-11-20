# Charter: Track 1 of a counted child's missing credit answer is asked

Role: Builder. Source HEAD on milestone/eic-child-answers-2025.
Plan: docs/phases/engine-breadth/milestones/eic-child-answers.md (read it
whole, especially the P0 result and Decisions 1-6). ADR:
docs/adr/0087-question-walk-follows-roster-members.md (proposed; build to
its Decision exactly). Evidence: eic-child-answers-evidence/p0.md
(section 6 names the change and its file:line), probe and build scripts.
For publishing a content successor, follow eic-answer-questions (core
v100). Do not read governance.

## Scope

1. **Projection.** In `packages/derivation/presentation_projection.py`,
   `_closure_question_reasons` follows a blocked roster member's subject key
   to that member's own blocked rows and walks their missing names
   (ADR 0087 Decision 1). Each such reason carries `member_label`, the
   member's recorded label (Decision 2). Extend the reason validator and
   the page's reason rendering (`citation-walk.v1.html`) to show it beside
   the question. Nothing else in the projection changes. If the member's
   recorded label is not reachable from the projection without a schema or
   kernel change, stop and report.
2. **Questions.** Input questions for every per-member answer of the four
   rosters that P0 found unasked (earned income child tests, tie-breaker
   answers, child tax credit tests, other-dependent child TIN, the seven
   relative answers), written from the 2025 Form 1040 instructions
   (line 27a, Schedule 8812, Dependents, credit for other dependents).
   Quote each question's source lines in track1.md. Each question is a
   plain question that says what yes and no mean; do not add examples the
   source does not give. Publish them as core v101, registry v99, release
   v99 (new files only; loader v101 entries carry v100's).
3. **Tests.** Live tests through the real coordinator and saved page, with
   nothing pre-filled that a test is about: for each roster, one and two
   members, each missing one answer for one member; the page shows the
   question with the right member's label on every blocked line, and the
   lines still block. A return with every answer given computes exactly as
   on v100. Unit tests for the walk (member key resolves; member key with
   no rows leaves the line silent; two members each missing an answer get
   two labelled reasons). A fast package test that v101 admits exactly
   the new questions.
4. **Replay.** Full-surface replay of the 775 recorded lists, v100
   against v101, and P0's probe lists. No number may change.

This touches `packages/derivation/`: run the full suite (`pytest`) and
`python3 -m mypy` after your last edit, and put the result lines in
track1.md. No kernel edits.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included. Never edit a file published on main.
- Commit with separate simple commands (mkdir lock; git add <paths>;
  git commit -F file; rmdir lock) under
  `$(git rev-parse --git-dir)/collaboration-commit.lock`.
- Bound every command that can hang; never `rm -rf`. Never raise a
  fast-lane budget or size cap; report instead.
- Write your JSON report before your final checks; update it when done.
- Never --no-verify or a bare git stash. Foreground commands only. No
  push and no spawn.
