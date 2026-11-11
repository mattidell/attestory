# Charter: Track 0 adversarial closure of question wording

Role: Builder. Source HEAD on milestone/question-wording-2025.
Plan: docs/phases/engine-breadth/milestones/question-wording.md (read it
whole, including the P0 result and Decisions 1-6). Evidence:
question-wording-evidence/ (start with p0.md). Gate: `PROJECT_PLANNING.md`,
"Track 0 Adversarial Closure Gate" (read that section and its closing
paragraphs whole). Precedent: f1099b-box4-only-evidence/track0-closure.md
and its track0.py. Do not read governance.

## Scope

Every claim must come from a `live_coordinate_run` output saved in a
committed JSON file and named by case id. Hand values come from the 2025
instructions (law.json), never from what the prototype publishes. A
question is tested by answering it as a truthful filer would read its
words, never by entering numbers by hand. Never work under
packages/content.

0. **Decisions.** Make the scratch v87 prototype match Decisions 1-4,
   including the two fact-title bundle successors.
1. **Authority-lifecycle table** for each changed question and title:
   who is asked, what answers it, which rule reads the answer, and what
   supersedes it.
2. **Empty/nonempty matrix** per question: wash sale with no covered
   sale, covered sales with no adjustment, with one, with both kinds;
   Exception 1 with no sale, a zero-net sale, a gain sale; student loan
   for single and joint filers, claimed and not, spouse claimed.
3. **Late-member traces:** a wash-sale adjustment added after the
   question was answered; a sale added after Exception 1 was answered
   yes; the dependency answer superseded.
4. **Claim reuse:** every rule that reads these answers composes
   unchanged; only words and titles differ between v86 and v87.
5. **Neighbour dependency diff:** the 298 recorded runs in
   tests/fixtures/f1099b_backup_withholding_v83/expected.json, and every
   other recorded fixture P0 named, on live v86 and scratch v87, in a
   subprocess. Classify every change.
6. **Integration surface:** a presentation probe of the exact text the
   filer sees for each changed question, on a page where it is asked.

Then write the closing declaration under a new "Track 0 adversarial
closure" heading in the plan. A row is PASS only if no counterexample
stands beside it. Repairs are changes in prototype.py. Where a fix cannot
pass without an engine, schema or recording change, mark it FAIL and stop.

## Deliverables

- question-wording-evidence/track0-closure.md;
- track0.py (mutates no other module's globals) and its JSON outputs;
- the plan's "Track 0 adversarial closure" section.

No production, test or content edits.

## Rules

- Synthetic demo.* only, and no absolute or temp-directory paths in
  committed files, prose included.
- Commit after each numbered item, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
  retry every 10 s for up to 5 min if held).
- Never use --no-verify or a bare git stash.
- Run foreground commands only.
- No push and no spawn. Do not edit packages/.
