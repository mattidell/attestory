# Capital-Gain Distributions / Line 7a — Closing CI Type Recheck

Audience: Reviewer.

Status: **chartered for dispatch.**

## Context Capsule

- **Source ref and resolved launch commit:** branch
  `track/capital-gain-distributions-line7a-track3-presentation` at type-repair
  commit `9d3627fd0cebe5092de1025a3d2ef62ffeefc8cd`. The recheck
  charter/pointer commit is context and must be its direct successor.
- **Exact object or commit range:** focused repair range
  `ba581ad02ae99ba91dcc3f3b610d6377650e0f69..9d3627fd0cebe5092de1025a3d2ef62ffeefc8cd`.
  It must contain exactly one commit and the one Track-3 presentation test.
- **Role:** the original author-independent Track-3 Repair Reviewer continues
  its own review lineage, Medium tier / medium effort. This is a focused CI
  type recheck, not another Track-3 behavior review.
- **Scope and evidence-rung ceiling:** determine only whether the repair closes
  the four PR #128 `no-any-return` errors without altering decoded JSON values,
  test behavior, F1/F2/F3 coverage, or any file outside the focused test.
  Credit PR #128's passed pytest step and the prior Track-3 `READY` review.
  The exact diff, focused six-test module, and repository mypy command are the
  ceiling.
- **Stop conditions:** stop and report if the range, tip, or ancestry differs;
  if any other file changed; if repair changes JSON paths, reads, decoding,
  runtime values, fixtures, assertions, test count, or test semantics; if it
  uses a global suppression, `type: ignore`, `Any` return widening, or
  production-code change; if a specific failure cannot be attributed; if
  governance interpretation is required; or if real/private material appears.
- **Full reads before acting:** this charter; `docs/roles/reviewer.md`;
  `docs/reviews/charter-2026-07-31-capital-gain-distributions-line7a-closing-ci-types-repair.md`;
  PR #128 failed `verify` log for run `30615579462`; the exact repair diff;
  `tests/test_capital_gain_distributions_line7a_t3_presentation.py`;
  `docs/reviews/2026-07-30-capital-gain-distributions-line7a-track3-repair-recheck.md`;
  and `AGENTS.md#Data Safety Rules`.

Before reviewing, echo the exact range, four type-error closure question,
credited pytest and Track-3 evidence, one-file ceiling, runtime-equivalence and
test-semantics constraints, evidence ceiling, and every stop condition.

## Focused measurements

1. Confirm one repair commit changes only
   `tests/test_capital_gain_distributions_line7a_t3_presentation.py`.
2. Confirm each of the four helpers still reads the same content path as UTF-8,
   calls the same `json.loads`, and returns the identical decoded object at
   runtime. Prove `typing.cast` is the only semantic addition and is runtime
   identity.
3. Confirm there is no `type: ignore`, global/module suppression, `Any` helper
   return, changed fixture/assertion, removed test, or production import/change.
4. Run the six-test module and full mypy command independently. All four
   original errors must be absent, mypy must be clean, and the module must
   still report six passing tests.
5. Confirm diff hygiene, governance lint, envelope safety, and unchanged
   credited Track-3 behavior.

## Verification

Run once:

```text
python3 -m unittest tests.test_capital_gain_distributions_line7a_t3_presentation
python3 -m mypy
git rev-list --count ba581ad02ae99ba91dcc3f3b610d6377650e0f69..9d3627fd0cebe5092de1025a3d2ef62ffeefc8cd
git diff --name-only ba581ad02ae99ba91dcc3f3b610d6377650e0f69..9d3627fd0cebe5092de1025a3d2ef62ffeefc8cd
git diff --check ba581ad02ae99ba91dcc3f3b610d6377650e0f69..9d3627fd0cebe5092de1025a3d2ef62ffeefc8cd
python3 tools/governance_lint.py
python3 tools/envelope_scan.py --range main..HEAD
```

Do not rerun the full pytest suite; PR #128 already passed it before mypy.

## Review record and verdict

Write
`docs/reviews/2026-07-31-capital-gain-distributions-line7a-closing-ci-types-recheck.md`
and commit only that record. Return exactly one verdict:

- `READY` — all four errors are closed with runtime/test semantics unchanged
  and credited evidence intact; or
- `NOT READY` — a numbered, reproducible residual explains why the type repair
  remains open or exceeded its boundary.

Do not edit the test, implementation, records, reviews, charters, pointers,
plan, frontier, roadmap, ledger, retrospective, or README. Do not implement a
repair, push, update or merge the PR, select future scope, or close out. Stop
after committing the recheck record and return custody.
