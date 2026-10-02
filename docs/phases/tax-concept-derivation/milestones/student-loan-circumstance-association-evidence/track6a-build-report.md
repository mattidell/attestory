# Track 6a build report

## Result and boundary

Implemented the experimental v12 statement-reader substrate and v34 package
successor. This is a prerequisite for the saved-reader demonstration, not a
completed reader, final wording/layout, production worksheet integration, or a
student-loan tax conclusion. All candidate wording in the synthetic tests is
provisional.

## Schema history and admission

- The first package proposal, v33, failed admission because its closed
  `members[].schema` enum does not include `rule-artifact.v12`. It remains
  refused history. Its manifested bytes/checksum were preserved exactly:
  `07e8912355ec871bf825e1dc4e23b143b8963f7b93c1aa0764ce5acb014e90a9`.
- Before creating v34, the package proposal was revised in the shared schema
  intent ledger. Events: `20260927T163200Z-rule-artifact-6a12c1` (v12
  propose), `20260927T163200Z-artifact-package-6a12c2` (v33 propose), and
  `20260927T164307Z-artifact-package-6a34c2` (v34 revise replacing v33).
- v34 was confirmed unused and manifested locally. After that, a complete v12
  member package was validated against its shape and the closed enum/condition
  locations were inspected; v34 bytes were then frozen. The manifest diff adds
  v12, v33 and v34 without changing existing entries. v34 checksum:
  `8ce6b19a71cdbc995f5a3d653c379f5ebf9cdbdfbbae7daafad44ba980524b2b`.
- Admission accepts exactly six roles: `statement-amount`, `link-count`,
  `statement-scope-classifier`, `statement-scope-disqualifier-count`,
  `bare-statement-conclusion`, and `responsibility`. The three responsibility
  declarations are permitted for one subject. Singular amount, link-count,
  and disqualifier-count roles remain exclusive. `link-count` must be the
  direct `{op: link_count, links: ...}` value. Disqualifier count must be a
  direct `link_coverage`. The bare conclusion must guard with exactly the
  required link-count and disqualifier-count publishers both equal to zero
  under `all`. Producer and consumer subject pins must all agree for both the
  bare conclusion and each responsibility rule; a disqualifier count's link
  type must match its classifier subject. Negative tests cover transformed
  counts, hidden `any` guards, unrelated link types, and each consumer subject
  mismatch.

## Runtime and Track 6b handoff

The v12 rule shape adds the six-value `reader_role` enum, `link_count` with a
single `links` fact-type operand, and optional `wording` / `lineNote` text.
`lineNote` is admitted only on a bare-statement conclusion. Neither text field
creates a finding or grants wording approval. The runtime requires a keyed
joined link source and counts its current rows; unbound scope or unavailable
keys blocks rather than returning zero. `link_count` contributes no parameter
or reduction dependency. The emitted finding pins its declared subject and
each counted source row; it does not pin a parameter. Track 6b can require the
roles by their explicit enum values and consume copied rule text while keeping
the candidate strings marked experimental.

## Evidence

The pre-fix `tests/test_sli_bare_statement_selection_probe.py` characterizes the old v10
marker path: zero-valued markers and cancelling `+1`/`-1` markers select the
bare-statement conclusion despite present links. The new synthetic live-path
tests prove S1 has count 0 and S2 count 1; both runners agree, findings retain
their own subject/link pins, and order changes do not cross-contaminate.
Missing S1 subject identity blocks S1 while the sound S2 statement still
publishes. A present link row without identity keys blocks both S1 and S2;
neither is silently counted as zero. The positive six-role package includes
three separate responsibility rules. v33 refusal and schema/admission
negatives remain covered.

Commands and results:

- `pytest tests/derivation/test_experimental_link_count.py -q` — 7 passed.
- Focused admission, exact-version, link-coverage, dispatch, schema-registry,
  fixture and envelope tests — 198 passed, 110 subtests passed.
- `python -m mypy` — no issues in 287 source files.
- `python tools/governance_lint.py` — conformant.
- First `pytest -q 2>&1 | tee temp/track6a/full-suite.log` attempt — 2,330
  passed, 20 skipped, 4,490 subtests passed; 25 tests failed on sandboxed
  loopback socket binds and one failed on the stale expected schema list.
- After updating that expected list, the escalated
  `pytest -q 2>&1 | tee temp/track6a/full-suite.log` run — 2,352 passed,
  20 skipped, 4,497 subtests passed. Captured output is retained at the
  ignored path `temp/track6a/full-suite.log` (session 69031). After the final
  consumer subject-pin admission change, the same captured command again
  passed: 2,352 passed, 20 skipped, 4,497 subtests passed in 126.60s (session
  24857). Local loopback access allowed the repository's integration tests to
  complete.

The full-suite run exposed a stale expected schema list in
`test_rule_artifact_v7_exists_only_in_the_unguarded_generation`; its expected
list now includes v33 and v34, which retain the prior v7 member set and remain
outside the v17 guard.

## Changed implementation paths

The substrate changes are in `packages/derivation/` validation, evaluation,
live resolution, marshalling, dispatch, runner and authorization closure; new
schemas are `rule-artifact.v12.schema.json` and
`artifact-package.v34.schema.json`, with v33 retained as frozen history. The
only existing test expectation updated was the v7 schema list described
above. Focused synthetic coverage is in
`tests/derivation/test_experimental_link_count.py`.

Remaining limits: wording and the owner-facing page remain experimental;
linked-borrowing tax outcomes and ADR 0076 Part 3 are out of scope. The builder
handed off uncommitted changes for foreman review; nothing was pushed.
