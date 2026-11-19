# Charter: Track 1 of the earned income credit for a head of household

Role: Builder. Source HEAD on milestone/hoh-eic-2025.
Plan: docs/phases/engine-breadth/milestones/hoh-eic.md (read it whole,
especially the P0 result and Decisions 2-6). Evidence:
hoh-eic-evidence/p0.md, design.py, build.py, probe.py, replay.py. For
how content successors are published, follow the most recent content
milestone, hoh-qualifying-person (core v98). Do not read governance.

## Scope

1. **Wording.** In design.py set `QUESTION` to exactly:

   > You file as head of household and no child is counted as your qualifying child for the earned income credit. Were you unmarried at the end of 2025? Answer yes if, on December 31, 2025, you had never married, your spouse had died before 2025 and you had not remarried, your divorce or annulment was final, or you were legally separated from your spouse under a decree of divorce or separate maintenance. Answer no if you were still married then, even if you lived apart from your spouse and file as head of household because you are considered unmarried: a married taxpayer filing as head of household cannot take the earned income credit without a qualifying child.

2. **Separated-spouse question (Decision 4).** Add an input question for
   the existing fact that `rule.eic-answer.separated-spouse` reads, worded
   from the 2025 Form 1040 line 27a instructions, Step 3 questions 3 to 5
   (quote the source lines you used in track1.md). Keep it a plain
   question that says what a yes and a no mean. If the fact's shape makes
   a plain question impossible without a schema or rule change, stop
   and report instead.
3. **Publish** core v99, registry v97, release v97 from the corrected
   design: P0's variant plus that question. New files only; never edit a
   file published on main. Check the validator's `_successor_graphs` table
   and the loader's v99 entries (carry v98's).
4. **Tests.** P0's probe returns as a live test module on v99 through the
   real coordinator and saved page, with hand values: an unmarried head of
   household with no counted child gets the single amounts, a married one
   gets $0, unanswered asks the question. A head of household with a
   counted child is unchanged and now sees the separated-spouse question
   when it is unanswered. Single, married filing jointly, married filing
   separately and qualifying surviving spouse are unchanged. Add a test that
   changes the answer from yes to no. Add a fast package test that v99 admits
   exactly the new members and successors. Re-pin any test that pins the
   current core version.
5. **Replay.** Full-surface replay of the 775 recorded lists, v98 against
   published v99, with P0's two added checks. Report pass/unexpected and
   unused expectations.

No engine, schema, projection or page edits.

## Deliverables

Content under packages/content/tax/2025/, tests, and track1.md in the
evidence directory. This touches published content: run the full suite
(`pytest`), `python3 -m mypy` and `pytest tests/test_schema_registry.py`,
and put the result lines in track1.md.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Commit with separate simple commands (mkdir lock; git add <paths>;
  git commit -F file; rmdir lock) under
  `$(git rev-parse --git-dir)/collaboration-commit.lock`.
- Bound every command that can hang; never `rm -rf`.
- Write your JSON report before your final checks; update it when done.
- Never --no-verify or a bare git stash. Foreground commands only. No
  push and no spawn.
