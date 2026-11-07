# Charter: repair after the fresh-reader review of sales without a Form 1099-B

Role: Builder. Source HEAD on milestone/f8949-boxes-cf-2025.
Read in full: the plan docs/phases/engine-breadth/milestones/f8949-boxes-cf.md
and the review docs/reviews/f8949-boxes-cf/review.md. Do not read
governance. Stop and report if a fix needs an edit under
packages/kernel/, packages/derivation/ or packages/schemas/, or a
recording change.

Core v80, registry v78 and release v78 exist only on this unmerged
branch. Rebuild them in place with the changes below; do not cut a v81.
Keep the scratch prototype (cf_prototype.py and cf-prototype-rules/) in
step, so that the byte-identity test still holds.

## Fixes

1. **B1.** Reword the new in-class input question so a covered sale is
   exempt only if it has no adjustment or only code W. The text must be
   true of the bundle proposition. Add a test that pins the question
   wording to the proposition.
2. **B2.** Mark
   `tests/test_incremental_lattice.py::test_collision_order_backtracking_and_duplicate_declared_id_boundary`
   `@pytest.mark.live`, with a measured-reason comment like its sibling's.
   Do not raise the budget.
3. **S1.** On lines 3 and 10, the guard against an unbacked "yes" must
   not block on the other term's failing sale. Read the other term's
   member count instead of its subtotal, if that works. Otherwise make
   both blocked sentences true.
4. **S2.** A sale entity recorded as both a box C and a box F sale must
   block, not count twice. Have each term's amounts-agree rule require
   the other term's count for the same sale to be 0. Add the case.
5. **S3.** Have the live test's projection pin each blocked Schedule D
   line's reason sentences, and the (disposition, code, missing) of the
   rows for lines 2, 3, 9 and 10 and the four amount checks. Then drop
   the exact-duplicate cases the review lists in Q5. Keep any case whose
   projection is now distinct.
6. **S4.** On a box C or F-only return with the ADR-0061 Path B
   unanswered, line 10 or 3 blocks with no question. Split the zero-path
   admission into `choose` arms so the Q2 plus new in-class arm is not
   blocked by Path B, if content can do it. Otherwise record the limit
   and add the case pinned as it behaves.
7. **N1.** Retitle the Schedule D and Form 8949 attachment successors so
   they name lines 3 and 10 and boxes C and F.

Rerun the Track 0 harness on the changed design and confirm that every
hand value still holds. Then run `pytest -m "not live"`, the full
`pytest` and `python3 -m mypy`. Append a "Repair" subsection to the
plan's "Track 1 result" section.

## Rules

- Synthetic demo.* data only.
- No absolute local paths in committed files.
- Published citizens on `main` are immutable.
- Commit after each fix, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir).
  If the lock is held, retry every 10 s for up to 5 min.
- Never use --no-verify or a bare git stash.
- Run foreground commands only.
- Do not push and do not spawn.
