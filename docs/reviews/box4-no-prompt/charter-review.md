# Charter: fresh-reader review of a box 4 "no" not being asked for an amount

Role: Reviewer. Source HEAD on milestone/box4-no-prompt-2025, diffed
against `github/main`. Plan:
docs/phases/engine-breadth/milestones/box4-no-prompt.md (read it whole,
Decisions 1-8 and the Track 1 result included). You have not seen the
build, so judge from the committed content, tests and evidence, not from
summaries. Do not read governance. Also apply
docs/roles/qualitative-review.md.

## Questions

1. **A "no" means zero, and only for its statement.** Read the published
   yes/no question, the box 4 amount question v2, the 16 helper rules,
   the selection and line 25b v9 yourself, with the 2025 Form 1040 line
   25b and Form 1099-B box 4 passages in the local sources. Does a
   truthful "no" mean nothing was withheld on that statement? Can one
   statement's "no" satisfy another statement, a different sale subject
   type, or a different tax year or filer? Does a statement with several
   sales count its amount once? Does the original `require_paired`
   expression still run, unchanged, whenever any statement is not
   satisfied?
2. **The new words are true.** Is every word of the v2 amount question
   true on every return that shows it, including a return with only
   "yes" statements, one with no "no" at all, and mixed returns? Does it
   still tell a filer with a blank box 4 what to do? Compare it with
   v1 and the yes/no question's words.
3. **Contradiction and correction.** "No" with a positive amount
   (Decision 2), changing "no" to "yes", withdrawing the answer. Is the
   behaviour true and what the page says consistent with it?
4. **Placement.** Run the real coordinator on published core v94 with
   synthetic `demo.*` act lists and read the saved page model; draw at
   least two pages in Chrome as tests/test_page_alerts_v92.py does. On a
   "no" return, is the amount sentence gone from lines 25b, 25d, 33 and
   37? Where line 25b still blocks, is what it names true and enough for
   the filer to finish? Does any computing return gain a question?
5. **Nothing else changed.** Core v94 equal to v93 except the added
   members and entrypoints and the replaced box 4 question; registry v92
   and release v92 add-only; loader change limited to v94; the diff over
   packages/kernel, packages/derivation, packages/schemas and
   packages/presentation empty. Are the 16 entries added to
   tools/required_versus_read_allowlist.json true, and narrow? Sample ten
   recorded lists across sets and diff v93 and v94 yourself with
   `tools/recorded_replay.py` in parallel; can the track1 classification
   hide a changed value, disposition or refusal code?
6. **Tests.** In tests/test_box4_no_prompt_v94.py and its package test:
   name any test that would pass if the content were wrong, any case
   named for a state its act list does not have, any check that
   classifies sentences by punctuation, and live runs that test nothing a
   sibling does not. Do hand values come from the facts? Evidence loaded
   only through tests/evidence_loader.py, with bare-name sibling imports
   bound by path first?
7. **Data safety.** `python3 tools/envelope_scan.py --range
   github/main..HEAD`. No absolute or temp-directory path in committed
   files or the review.

Run `pytest` only to confirm a specific failing claim. Run every command
in the foreground; never end your turn while a command is running.

## Deliverable

docs/reviews/box4-no-prompt/review.md, committed (explicit path, under
`$(git rev-parse --git-dir)/collaboration-commit.lock`, mkdir … rmdir;
retry every 10 s up to 5 min if held). Each finding: file:line,
reproduction, severity (blocking, should-fix or note), fix. End with a
verdict: ready, or the blocking list. No other edits. No push, no spawn.
