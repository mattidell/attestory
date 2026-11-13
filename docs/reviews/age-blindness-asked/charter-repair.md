# Charter: repair of age and blindness asked after review

Role: Builder. Source HEAD on milestone/age-blindness-asked-2025. Plan:
docs/phases/engine-breadth/milestones/age-blindness-asked.md, Decision 11.
Review: docs/reviews/age-blindness-asked/review.md (F1-F4). Do not read
governance.

## Repair

1. **F1 and F4 in the prototype.** In age-blindness-asked-evidence/prototype.py:
   nest the spouse age and blindness facts in a separate-return set whose
   condition is the condition fact, as F1's fix describes; add the
   instructions' alternative statement to both blindness questions and both
   titles, quoting law.json's `blindness` text. Rerun the track0 cases on a
   separate return and the blindness cases; add a case for F1 (separate,
   condition no, spouse unanswered: computes 12e 15,750 and asks nothing
   about the spouse). Commit the JSON.
2. **Regenerate v88 in place** from prototype.py: the changed citizens,
   core v88, registry v86 and release v86 (branch-only; registry v86 stays
   add-only against main). Byte identity holds.
3. **Tests.** Update the pinned sentences; add the F1 case and the two
   F3 line 16 pins. Cut the recorded replay in
   tests/test_age_blindness_v88.py to the 298 v83 lists the v87 module
   replays (keep its parallel pool at most 4 workers); say in the module
   docstring that the 775-list result is in the committed evidence.
4. **Checks.** `pytest` on the v88 modules and every file you touched,
   `pytest -m "not live"`, `python3 -m mypy`,
   `python3 tools/envelope_scan.py --range github/main..HEAD`. Update
   "Track 1 result" with the new counts and wall times.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Never edit a citizen published on main.
- Commit after each numbered item, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
  retry every 10 s up to 5 min).
- Never --no-verify or a bare git stash. Foreground only. No push, no
  spawn.
