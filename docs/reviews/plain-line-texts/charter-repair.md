# Charter: repair after the fresh review — every line speaking plainly

Role: Builder. Source HEAD on milestone/plain-line-texts-2025.
Plan: docs/phases/engine-breadth/milestones/plain-line-texts.md (read
Decisions 9-12). Review: docs/reviews/plain-line-texts/review.md
(PLT-R1, PLT-R2). Evidence: plain-line-texts-evidence/ (track1_replay.py,
track0_validate.py, p0c_compare.py, census.py). Do not read governance.

Stop and report if anything needs an edit under packages/kernel/,
packages/schemas/, packages/presentation/ or packages/derivation/.

## Work

1. **Every drawn text, read.** From the Track 1 v96 replay part (or a
   fresh parallel run of the 775 recorded lists on the current v96),
   list each distinct content text the saved pages draw: the active
   disposition's explain text per field, attachment headings (before
   the first colon), question and reason sentences, and drawn mortgage
   notes. For each, record plain or not, with a one-line reason; at
   least the review's four texts are not plain. Commit the table
   (`repair-drawn-texts.json`).
2. **Replace.** Write plain wording for each text judged not plain,
   checked against the local 2025 Form 1040 instructions, keeping the
   basis (absence versus rounding versus calculation). A citizen added
   on this branch (not on github/main) is edited in place; a citizen
   on github/main gets a successor (line 6a: v3). Never edit a citizen
   that is on github/main.
3. **Rebuild** core v96, registry v94 and release v94 in place with
   `python3 -m tools.package_successor` from published v95 (they are not
   on main), so the new members are included. Update the package test's
   expected member count and digests and the manifest
   (`track0-wording.json` stays as Track 0's record; add
   `repair-wording.json` with the new old→new pairs).
4. **Tests (PLT-R1).** The live test reads only the active
   disposition's text, attachment headings and drawn mortgage notes, and
   asserts each manifest text and that no text judged not plain in item 1
   remains drawn.
5. **Replay.** All 775 recorded lists plus the 9 synthetic on published
   v95 and the rebuilt v96, strict classifier and 16 mutation controls.
   Expected: 691 expected_sentences / 84 same_error recorded, nothing
   unexpected, each changed sentence equal to its manifest text.
6. **Checks.** The new and touched test modules, `pytest -m "not
   live"`, `python3 -m mypy`, `python3 tools/envelope_scan.py --range
   github/main..HEAD`. Append a "Repair result" section to the plan.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Commit after each numbered item, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir);
  if held, retry every 10 s up to 5 min. Never remove another holder's lock.
- Write your JSON report before your final checks; update it when done.
- Never --no-verify or a bare git stash. Foreground only. No push, no spawn.
