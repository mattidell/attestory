# Charter: Track 0 adversarial closure of line 12d's boxes

Role: Builder. Source HEAD on milestone/line12d-boxes-2025.
Plan: docs/phases/engine-breadth/milestones/line12d-boxes.md (read it
whole, including the P0 result and Decisions 1-6). Evidence:
line12d-boxes-evidence/ (start with p0.md). Gate: `PROJECT_PLANNING.md`,
"Track 0 Adversarial Closure Gate" (read that section and its closing
paragraphs whole). Precedent: age-blindness-asked-evidence/track0-closure.md
and its track0.py; tools/sale_page_observation.py and
tests/test_sale_page_observation.py for driving the saved page in Chrome.
Do not read governance.

## Scope

Every claim comes from a `live_coordinate_run` output, or a drawn-page
observation, saved in a committed JSON file and named by case id, on
published v89 and scratch v90. Box states come from the 2025 instructions
(law.json), never from what the prototype publishes. Never work under
packages/: prototype the Decision 1 page change on a scratch copy of the
page outside packages/ and outside the repo's tracked pages, and commit
the exact diff as evidence (a .diff file), not an edited page.

0. **Page prototype.** The smallest change to the categorical branch that
   draws `not_checked` with its explanation and citation and never reads
   the finding's value. Show the diff.
1. **Authority-lifecycle table**, per box: which answer feeds it, which
   rule and field show it, when it is hidden, and what replaces it.
2. **Empty/nonempty matrix**: single, joint, separate (condition yes and
   no), head of household, qualifying surviving spouse and a dependent
   filer; each with answers true, false and unanswered. For each: the four
   box states against the instructions, and line 12e against the chart.
3. **Late-member traces:** joint to separate with a spouse box checked;
   joint to head of household; an answer replaced.
4. **Claim reuse:** the new members add no read that changes a number; the
   v89 rules compose unchanged.
5. **Neighbour sample** (Decision 5): with
   `python3 tools/recorded_replay.py`, at most 4 workers, a sample of
   about 40 recorded lists spread across all five fixture sets (v81, v82,
   v83, v84, v85), answered as their records imply. Keep it under about
   10 minutes of wall time. Classify every change. State plainly that the
   full 775-list replay was not run.
6. **Integration surface, in a browser.** Drive the scratch page in Chrome
   for at least: single both false; single age true; joint with one spouse
   box checked; separate with the condition no; head of household. Record
   the exact text drawn for each of the four boxes, that no
   `missing-instruction` alert appears for a line 12d field, what happens
   to the existing line 6d and line 6c alerts, and the text for a hidden
   spouse box (Decision 4). Also draw one v89 return on the unmodified
   page and on the scratch page to show nothing else changes.

Do not run the full test suite, mypy or the full replay. Stop and report
if the page change needs more than the categorical branch, or if anything
needs an engine, schema or projection change.

## Deliverable

line12d-boxes-evidence/track0-closure.md and track0.py with its
`track0-*.json` outputs and the page .diff, and a "Track 0 adversarial
closure" section in the plan: each table PASS or FAIL with counts and case
ids, and "Known limitations affecting correctness" (the full replay owed
is one).

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Commit after each numbered item, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir);
  if held, retry every 10 s up to 5 min.
- Never --no-verify or a bare git stash. Foreground only. No push, no
  spawn.
