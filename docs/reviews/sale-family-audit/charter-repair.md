# Charter: repair of the sale family audit review

Role: Builder. Source HEAD on milestone/sale-family-audit-2025.
Plan: docs/phases/engine-breadth/milestones/sale-family-audit.md.
Review: docs/reviews/sale-family-audit/review.md (read it whole; it has the
reproductions). Do not read governance.

Core v82, registry v80 and release v80 are unpublished on this branch, so
rebuild them in place with `python3 -m tools.package_successor`; do not
make v83. Stop and report if anything needs an edit under
packages/kernel/, packages/derivation/ or packages/schemas/, or a
recording change.

## Repairs

1. **F1, blocking.** Covered and code W amount rows with no sale of their
   own must not count. Add row-needs-sale for both kinds to the v82
   loader entry, as the other three kinds have, plus any content the
   pairing needs. Prototype it first as a `REPAIRS` switch, rerun Track 0
   and the v81 classification, and add the review's four reproductions as
   Track 0 cases (extra rows beside a covered sale, rows alone, extra rows
   beside a code W sale, sale removed with rows left). Each must refuse or
   block with a true reason. Classify every v81 return that changes.
2. **F2, blocking.** Form 1040 line 7b must not say Schedule D is not
   required while Form 8949 or Schedule D is required. Make a line 7b
   successor that reads the sale counts, add line 7b to the test
   projection and the audit tables, and add the review's zero-net cases.
3. **F3.** Correct the line 16 v3 "not applicable" sentence and the line
   7a v2 blocked sentence so each is true of its rule's `when`.
4. **F4.** Extend the audit to amount rows, or correct the `tables.py`
   docstring if a row field is out of scope with a reason. Make the live
   test's honest Exception 1 answers follow the v2 wording.
5. **F5.** Drop the 321 runs the review names as repeats (the v81 honest
   reruns, already asserted equal, and the default-answer Track 0 runs
   identical to their honest runs), keeping every Track 0 row witnessed.
   Regenerate the fixture and report its size and the run count.
6. **Notes N1-N5.** Fix any that cost a few lines; list the rest in the
   plan's "Track 1 result" as parked, with reasons.

Then run `pytest -m "not live"`, the full `pytest` and `python3 -m mypy`,
and update the plan's "Track 1 result" and the closure addendum with the
new counts and classifications.

## Rules

- Synthetic demo.* only, and no absolute or temp-directory paths in
  committed files, prose included.
- Load evidence harnesses under unique module names; never assign another
  evidence module's globals.
- Keep every test under the 3.0 s fast-lane budget or `@pytest.mark.live`
  with a measured reason.
- Commit after each numbered item, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir).
- Never use --no-verify or a bare git stash. Foreground commands only.
- No push and no spawn.
