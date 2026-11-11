# Charter: fresh-reader review of live harness isolation

Role: Reviewer. Source HEAD on milestone/live-harness-isolation-2025,
diffed against `github/main`. Plan:
docs/phases/engine-breadth/milestones/live-harness-isolation.md (read it
whole) and the P0 record and inventory in
live-harness-isolation-evidence/. You have not seen the build, so judge
from the committed code, tests and evidence, not from summaries. Do not
read governance.

## Questions

1. **No weakened assertion.** Diff every moved test module against
   `github/main`. Did any assertion, case list, parametrization, marker,
   skip, fixture byte, or the fast-lane budget change? Did any module stop
   exercising a harness it exercised before? Show the diff hunks.
2. **Isolation is real.** Does `tests/evidence_loader.py` give each owning
   test module private copies of the harness modules, including nested
   bare imports (`import probe`, `import_module("probe")`), while keeping
   `packages.*` and `tests.*` shared? Show with a run on one worker that
   two owners loading the same harness get distinct module objects, and
   that a harness global assigned in one owner is not visible in another.
3. **Restore is exact.** For every unrestored `packages` write the
   inventory names, does the loader snapshot and restore it when the
   owning module finishes, including on failure? Is any write missed?
   Mutate in memory to show the guard catches an unlisted write.
4. **Guard.** Does the guard test fail if a module loads an evidence file
   by `spec_from_file_location`, `runpy`, `exec`, or `sys.path` insertion
   outside the loader? Show it failing on a temporary in-memory or
   scratch-copy violation, not a committed one.
5. **Hidden coupling.** The commits "Keep a package child module bound"
   and "Keep shared modules visible to the interpreter module dict" fixed
   failures found during the build. Are they correct, or do they reopen
   sharing between owners? Is anything in `tests/conftest.py` order- or
   worker-dependent?
6. **Cost.** Is the loader cheap enough for the fast lane? Is any live
   run redundant?
7. **Data safety.** Run
   `python3 tools/envelope_scan.py --range github/main..HEAD`. Write no
   absolute or temp-directory path in the review.

Run `pytest` only to confirm a specific claim, on the named modules only.

## Deliverable

docs/reviews/live-harness-isolation/review.md, committed (explicit path,
under the collaboration-commit lock; retry every 10 s for up to 5 min if
held). For each finding give: file:line; a reproduction; a severity
(blocking, should-fix or note); the fix you would make. End with a
verdict: ready, or the blocking list. Make no other edits. No push, no
spawn.
