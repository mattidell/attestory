# Charter: P0b of the separated-spouse question is asked only of a married filer

Role: Builder. Source HEAD on milestone/eic-separated-married-2025.
Plan: docs/phases/engine-breadth/milestones/eic-separated-married.md (read
it whole; Decisions 1-3 bind). Evidence: eic-separated-married-evidence/
p0.md and its scripts. Do not read governance.

## Scope

1. **The question.** Draft the new fact type and input question from Step
   3 question 3 of the 2025 Form 1040 instructions (quote it): whether a
   head of household filer was married at the end of 2025, with the
   instructions' own words on who counts as married for the credit
   (Publication 596 Rule 3 and the special rule). Model it on an existing
   EIC answer fact and question (for example `eic.not-married`).
2. **Successors (scratch, on published v102).** The new question is
   required only of a head of household with a qualifying child present;
   the separated-spouse question is required of a married filing
   separately filer and of a head of household who answered "married". An
   unmarried head of household skips Step 3 questions 4 and 5. A recorded
   separated-spouse "yes" without the new answer still passes, if the rule
   language can say it (look at how selection and paths handle an answer
   that is present or absent; ADR 0081 and existing rule-artifact
   selection). Say exactly how.
3. **Trace.** Re-run the 21 P0 cases plus: a head of household with a
   recorded separated-spouse "yes" and no new answer; unmarried "no" to the
   new question; married "yes" then separated-spouse "no". Hand credit for
   each from the 2025 table.
4. **Replay.** Full-surface replay of the 775 recorded lists, v102 against
   the scratch successor, expected changes declared. Count and describe any
   list that newly blocks or changes a number. If any recorded list newly
   blocks, stop and report the count and kind before Track 1.
5. **Size.** Report each new or successor rule file's bytes against the
   5,000-byte cap, and run
   `pytest tests/test_earned_income_credit_track1.py tests/test_eic_qualifying_children_track1.py -k 5kb`
   against a scratch copy if needed.

## Deliverables

In eic-separated-married-evidence/: p0b.md (question text with sources,
successor design, trace table, replay, sizes, decisions for the foreman),
scripts a later test will need, small JSON. Add a "P0b result" section to
the plan. No production, test or content edits.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included. Nothing over 200 KB committed. Fetched sources
  stay in ignored temp/.
- An evidence script that imports a sibling harness by bare name loads it
  by path under a unique name instead.
- Commit with separate simple commands (mkdir lock; git add <paths>;
  git commit -F file; rmdir lock) under
  `$(git rev-parse --git-dir)/collaboration-commit.lock`.
- Bound every command that can hang; never `rm -rf`.
- Write your JSON report before your final checks; update it when done.
- Never --no-verify or a bare git stash. Foreground commands only; leave
  no background jobs. No push and no spawn. Do not edit packages/ or
  tests/.
