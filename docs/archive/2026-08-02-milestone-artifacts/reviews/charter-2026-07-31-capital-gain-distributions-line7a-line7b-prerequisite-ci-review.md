# Capital-Gain Distributions / Line 7a — Prerequisite CI Repairs Recheck

Audience: Reviewer.

Status: **chartered for a focused author-independent recheck.**

## Context Capsule

- **Source ref and resolved launch commit:** current prerequisite branch at this
  committed review charter/pointer. Resolve and verify `HEAD` before acting.
- **Exact object:** two implementation commits only:
  `Update line 7b loader successor assertion` and
  `Annotate line 7b prerequisite cases`, each measured against its immediate
  parent charter. Together they may change exactly
  `tests/test_capital_gain_distributions_line7a_t1_citizens.py` and
  `tests/test_capital_gain_distributions_line7a_line7b_prerequisite.py`.
- **Role:** the independent prerequisite Reviewer continues its own review
  lineage without Builder exposure.
- **Scope and evidence-rung ceiling:** verify the first delta updates the
  loader test to assert current v2 selection plus explicit v1 preservation, and
  the second is annotation-only. Focused tests, mypy, and static diff evidence
  are the ceiling. Credit the READY prerequisite implementation review.
- **Stop conditions:** return `NOT READY` if any production/publication file or
  third test file changed; the loader assertion weakens field/citation
  validation or drops the v1 contract; the type repair changes runtime values,
  cases, assertions, or control flow; an error is suppressed; focused tests or
  mypy fail; or governance/private material is implicated.
- **Full reads before acting:** this charter; `docs/roles/reviewer.md`; both CI
  repair charters; both exact implementation diffs; the prerequisite READY
  review; field v1/v2; `packages/tax/loader.py`; and
  `AGENTS.md#Data Safety Rules`.

Before measuring, echo both exact objects/files, credited evidence,
test-only/static ceiling, and stop conditions.

## Measurements and verification

1. Confirm object custody and no production/publication delta after the READY
   prerequisite review.
2. Confirm the loader test still validates line 7a, line 7b schema/line/citation,
   now requires current v2 and the rule-output symbol, and separately loads,
   schema-validates, and asserts historical v1's original conclusion binding.
3. Confirm the prerequisite-test delta adds only the explicit heterogeneous
   case-table type and changes no runtime expression.
4. Independently run:

```text
python3 -m unittest tests.test_capital_gain_distributions_line7a_t1_citizens
python3 -m unittest tests.test_capital_gain_distributions_line7a_line7b_prerequisite
python3 -m mypy
git diff --check <each-charter>..<its-implementation>
python3 tools/envelope_scan.py --range main..HEAD
```

Commit one review record at
`docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-31-capital-gain-distributions-line7a-line7b-prerequisite-ci-review.md`
with a falsifiable `READY` or `NOT READY` verdict and exact evidence. Leave the
tree clean. Do not repair, edit pointers/charters, push, merge, restart Track 3,
or begin Track 4.
