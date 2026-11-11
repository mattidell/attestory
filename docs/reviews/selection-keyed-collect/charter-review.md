# Charter: fresh-reader review of a selection path collecting a keyed family

Role: Reviewer. Source HEAD on milestone/selection-keyed-collect-2025,
diffed against `github/main`. Plan:
docs/phases/engine-breadth/milestones/selection-keyed-collect.md (read it
whole). Proposed ADR: docs/adr/0085-selection-collect-by-family.md. You
have not seen the build, so judge from the committed code, content, tests
and evidence, not from summaries. Do not read governance.

## Questions

1. **Engine correctness.** Read the switch, validation and runner changes
   under packages/derivation/ and packages/tax/loader.py. Can a v86 rule
   now run a path before its collect's members are current, or read a
   family it does not name as its activity without a dependency? Does any
   pre-v86 core, or any non-core package, behave differently? Show each
   claim with a run or a test.
2. **Schema.** Are `rule-artifact.v16` and `artifact-package.v42` exactly
   their predecessors plus the stated change? Is `published.json`
   add-only? Does a one-path v15 rule still fail?
3. **Tax result.** On core v86, with synthetic `demo.*` findings: no box 4
   amount, one, two on different statements, a zero, superseded,
   withdrawn. Is line 25b the hand value, is nothing published under the
   amount id, and does the explanation walk show each recorded amount?
4. **ADR 0085.** Does the text match what was built? Is anything built
   that the ADR does not authorize, or anything it promises that is
   missing? Is its relation to ADR 0077 Part 4 stated correctly?
5. **Design weight.** Is a per-package switch the smallest safe change?
   The 31 other inert paths are parked: is that right, or should the
   switch's own tests cover one?
6. **Tests.** Do the new tests fail if the switch is removed or turned on
   for v85? Mutate in memory to show it. Is the package test's byte
   comparison honest given the prototype emits a v15 body?
7. **CI cost and isolation.** Name redundant live runs; check no module
   assigns another module's globals.
8. **Data safety.** Run
   `python3 tools/envelope_scan.py --range github/main..HEAD`. Write no
   absolute or temp-directory path in the review.

Run `pytest` only to confirm a specific failing claim.

## Deliverable

docs/reviews/selection-keyed-collect/review.md, committed (explicit path,
under the collaboration-commit lock; retry with backoff if held). For each
finding give: file:line; a reproduction; a severity (blocking, should-fix
or note); the fix you would make. End with a verdict: ready, or the
blocking list. Make no other edits.
