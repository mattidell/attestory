# Charter: repair of the earned income credit for a head of household

Role: Builder. Source HEAD on milestone/hoh-eic-2025.
Plan: docs/phases/engine-breadth/milestones/hoh-eic.md (Decision 7).
Review: docs/reviews/hoh-eic/review.md (EIC-R1 to R4). Do not read
governance.

v99 is not on main, so its files are regenerated in place on this branch
(core v99, registry v97, release v97 keep their numbers; checksums and
digests are regenerated).

## Scope

1. **EIC-R1.** When `eic.answer.not-married` is 0, the credit is $0 and
   none of the Step 4 question 2-6 answers (age, main home, not claimable
   as a dependent, not a qualifying child of another, no unsupported
   situations) is required. Choose the smallest set of rule successors
   that does this. Prefer a single successor of the rule that decides
   whether those answers are required, if that avoids a cycle with the
   not-married question's own condition; otherwise successors of the
   answer rules, as the review suggests. Do not change the result for any
   other filer: an unmarried yes still needs those answers, and every
   other status keeps v98's behaviour exactly. Add live tests that leave
   the age and main-home answers unanswered: married "no" computes $0 and
   the v98 refund, and unmarried "yes" blocks as a single filer does.
2. **EIC-R4.** In design.py replace the question's "Answer no" sentence
   with exactly:

   > Answer no if you were still married then, even if you lived apart from your spouse or had a written separation agreement but no decree, and file as head of household because you are considered unmarried: a married taxpayer filing as head of household cannot take the earned income credit without a qualifying child.

3. **EIC-R3.** Correct the comment in both size tests and track1.md: the
   growth is mostly formatting (v2 was hand-compacted; v2 written as v3
   is 5,944 bytes), not one extra nested check. If the regenerated
   gate rule changes size, set the exception to the smallest round figure
   above it.
4. **EIC-R2.** `tests/derivation/test_bounded_nominee_selection_contract.py::BoundedNomineeRuntime::test_path_pin_version_origin_and_identity_are_admission_contracts`
   takes about 4 s against the 3.0 s fast-lane budget, and
   `tests/test_market_discount_interest_contracts.py::SuccessorPackageContracts::test_md_n10_mixed_successor_graph_rejects_older_fields`
   was 3.0 s on CI. Find why (likely work that grows with each package
   version) and make each fast, for example by caching a published read
   as `tests/test_k1_interest_breadth_contracts.py` does with
   `_published_corpus`. If that is not possible, make it an honest live
   test. Never raise `FAST_LANE_BUDGET_SECONDS`.
5. **Regenerate** v99/v97/v97 with build.py through the validating
   generator; confirm by diff what changed. Re-run P0's probe and paired
   comparison and the 775-list replay against v98.
6. **Checks.** The two milestone modules, the two size tests, the two
   speed-fixed modules, `tests/test_schema_registry.py`, the v78 switch
   test, `pytest -m "not live"` and `python3 -m mypy`. Put the result
   lines and a Repair section in track1.md.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included. Never edit a file published on main.
- Commit with separate simple commands (mkdir lock; git add <paths>;
  git commit -F file; rmdir lock) under
  `$(git rev-parse --git-dir)/collaboration-commit.lock`.
- Bound every command that can hang; never `rm -rf`.
- Write your JSON report before your final checks; update it when done.
- Never --no-verify or a bare git stash. Foreground commands only. No
  push and no spawn. Stop and report if EIC-R1 needs an engine, schema or
  kernel change.
