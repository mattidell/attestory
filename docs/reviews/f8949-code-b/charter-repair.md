# Charter: repair after the fresh-reader review of broker basis corrections

Role: Builder. Source HEAD on milestone/f8949-code-b-2025. Read in full
the plan docs/phases/engine-breadth/milestones/f8949-code-b.md and the
review docs/reviews/f8949-code-b/review.md. Do not read governance.

Stop and report if a fix needs an edit under packages/kernel/,
packages/derivation/ or packages/schemas/, or a recording change.

Core v81, registry v79 and release v79 exist only on this unmerged
branch. Rebuild them in place, with no v82. Keep the prototype in step so
that the byte-identity test holds.

## Fixes

1. **B1.** A covered direct (line 1a or 8a) sale with zero proceeds must
   require the Schedule D attachment. Form 1040 line 7a must treat a
   nonzero line 1a or 8a as Schedule D activity. Add both terms as
   Decision 6 probes, with hand values.
2. **B2.** Measure every test in tests/test_incremental_lattice.py that is
   not marked live, with `-n0 --durations=0`. Mark any test whose call or
   setup time is over 1.0 s locally `@pytest.mark.live`, with a
   measured-reason comment, so the next slow sibling stops tripping CI
   one at a time. Do not raise the budget.
3. **S1 to S4.** Field wording:
   - S1: the zero sentences on lines 1b and 8b;
   - S2: the blocked text on lines 1b and 8b, which gets the "pass its
     checks" clause and the refusal;
   - S3: plain words on line 8a v2;
   - S4: the route to code B in the taxpayer-side sentence.

   Every sentence must be true of its rule's state in every case.
4. **S5.** The admission rules refuse a covered sale when any of the five
   eligibility flags is "yes": `taxpayer_side_adjustment`,
   `ordinary_indicated`, `box_1f_market_discount`, `qof_indicated` and
   `collectibles_or_special_rate`. Add a probe for each flag.
5. **S6.** Pin the Form 8949 parts' tie-out text for publishing cases in
   the projection.
6. **S7.** In the v80 group, keep one return per distinct v81
   projection, plus the five `ATTACHMENT_ROW_CHANGES`. List each dropped
   name next to the name it duplicates.
7. **N3.** Reword Q3 to "…show a cost or other basis, reported to the
   IRS, that is wrong?" and update its pinned test. N2: split IC3 into
   two sentences, or a short list, if it stays true to the proposition.

Then:
- rerun the Track 0 harness;
- regenerate the expected table;
- list every v80 return that changes, and why;
- run `pytest -m "not live"`, the full `pytest` and `python3 -m mypy`;
- append a "Repair" subsection to the plan's "Track 1 result".

## Rules

- Synthetic demo.* only, and no absolute or temp-directory paths in
  committed files.
- Published citizens on `main` are immutable.
- Commit after each fix, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir).
- Never use --no-verify or a bare git stash.
- Run foreground commands only.
- No push and no spawn.
