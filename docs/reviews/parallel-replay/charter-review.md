# Charter: fresh-reader review of parallel recorded-return replay

Role: Reviewer. Source HEAD on milestone/parallel-replay-2025, diffed
against `github/main`. Plan:
docs/phases/engine-breadth/milestones/parallel-replay.md (read it whole).
You have not seen the build; judge from the committed tool, tests and
evidence, not from summaries. Do not read governance.

## Questions

1. **Same lists.** Does `recorded_lists()` gather exactly the lists, in the
   same order and de-duplication, as question-wording's
   `neighbour_tasks()`? Find any input it reads that the original did not,
   or the reverse.
2. **Independence from scheduling.** Can the result depend on worker
   count, finish order, a crash and resume, or a stale part file from a
   different pair of cores? Is a part file written so an interrupted write
   cannot corrupt it?
3. **Equivalence evidence.** Does compare_neighbour.py compare every row
   that matters, so a wrong replay could not pass? Is equivalence.json's
   claim true of the committed tool (spot-run 10 lists with the tool and
   compare, with `--workers 2`)?
4. **Isolation.** Do worker processes share any module state with the
   parent or each other that a live evidence harness writes (see
   tests/evidence_loader.py)? Do the new tests stay under the fast-lane
   budget?
5. **Use by a milestone.** Is "How a milestone uses it" enough for a
   builder to run a P0 rerun and a Track 0 neighbour diff from one replay
   with a new per-list function? Name what is missing.
6. **Data safety.** `python3 tools/envelope_scan.py --range
   github/main..HEAD`. No absolute or temp-directory path in the review.

Run `pytest` only to confirm a specific failing claim.

## Deliverable

docs/reviews/parallel-replay/review.md, committed (explicit path, under
the collaboration-commit lock; retry with backoff if held). For each
finding: file:line, reproduction, severity (blocking, should-fix or note),
fix. End with a verdict: ready, or the blocking list. No other edits.
