# Charter: repair of question wording after review

Role: Builder. Source HEAD on milestone/question-wording-2025. Plan:
docs/phases/engine-breadth/milestones/question-wording.md, Decision 7.
Review: docs/reviews/question-wording/review.md (F1, F2, F4, F5). Do not
read governance.

## Repair

1. **F1.** In question-wording-evidence/prototype.py, limit the Exception
   1 only-box-2a v3 question's sale clause to sales that must be reported
   on Form 8949 or Schedule D (even one with no gain or loss), and add one
   short sentence that sales inside an IRA or 401(k) and losses on
   personal items do not count. Give the exception1 bundle successor's
   fact title the same scope. Quote the Schedule D instruction on
   personal-use property in law.json. Add a Track 0 row in track0.py: no
   sale recorded, the filer sold only a personal item at a loss, answers
   the v87 words truthfully (yes), and computes to the hand values; rerun
   track0.py and commit its JSON.
2. **F4.** The vocabulary bundle successor's blindness title names
   December 31, 2025.
3. **Regenerate v87 in place** from prototype.py: the changed citizens,
   core v87, registry v85, release v85 (none is on a ratified line yet;
   the registry stays add-only against
   `github/milestone/selection-keyed-collect-2025`). Byte identity to the
   prototype holds.
4. **F2.** Reword the plan's late-member line (and track0-closure.md) to
   what the traces show: each later answer replaces the earlier one in
   the act list; no supersession act is exercised.
5. **F5.** Drop `late_sli_claimed` and `late_sli_not_claimed` from the
   live module; update the pinned words and the new row.
6. **Checks.** `pytest` on the two v87 modules and
   tests/test_noncovered_sales_v78_switch.py, `pytest -m "not live"`,
   `python3 -m mypy`, and `python3 tools/envelope_scan.py --range
   github/milestone/selection-keyed-collect-2025..HEAD`. Update "Track 1
   result" with the new counts.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Never edit a citizen published on main; the v87 members are
  branch-only.
- Commit after each numbered item, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir);
  if held, retry every 10 s up to 5 min.
- Never --no-verify or a bare git stash. Run foreground commands only. No
  push, no spawn.
