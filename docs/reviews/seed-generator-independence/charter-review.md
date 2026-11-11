# Charter: fresh-reader review of the v70 entry seed generating without test helpers

Role: Reviewer. Source HEAD on milestone/seed-generator-independence-2025,
diffed against `github/main`. Plan:
docs/phases/engine-breadth/milestones/seed-generator-independence.md (read
it whole) and the P0 record in seed-generator-independence-evidence/. You
have not seen the build, so judge from the committed code, tests and
evidence, not from summaries. Do not read governance.

## Questions

1. **Bytes.** Regenerate the v70 seed with the new generator and compare
   every committed file under `packages/sample_data/entry_loop_v70/`
   except the new source. Is `complete-core-return.jsonl` exactly what the
   old generator's helper chain produces on `github/main`? Show it with a
   run.
2. **Independence.** Does the generator import any `tests` module,
   directly or transitively? Does the new test fail if it does? Show it
   failing on a scratch copy or an in-memory change, not a committed one.
3. **Drift.** What does the byte-regeneration test catch now, and what
   did it catch before? Is anything that used to be caught now silently
   lost, for example a core or release change the seed should follow? Is
   the docstring's refresh recipe accurate and runnable?
4. **Enumerators.** Does any loader, manifest, checksum, data-safety
   check or browser launcher that reads `entry_loop_v70/` behave
   differently with the new file present?
5. **Assertions.** Did any assertion, skip, or marker change? Are the 13
   skips in `tests/test_entry_loop_t1.py` the same before and after?
6. **Evidence weight.** P0 committed a moved-helper prototype of about
   2,500 lines under the evidence directory. Does it run in CI, is it
   type-checked, and should it stay?
7. **Data safety.** Run
   `python3 tools/envelope_scan.py --range github/main..HEAD`. Is the new
   source synthetic `demo.*` only? Write no absolute or temp-directory
   path in the review.

Run `pytest` only to confirm a specific claim, on the named modules only.

## Deliverable

docs/reviews/seed-generator-independence/review.md, committed (explicit
path, under the collaboration-commit lock; retry every 10 s for up to 5 min
if held). For each finding give: file:line; a reproduction; a severity
(blocking, should-fix or note); the fix you would make. End with a
verdict: ready, or the blocking list. Make no other edits. No push, no
spawn.
