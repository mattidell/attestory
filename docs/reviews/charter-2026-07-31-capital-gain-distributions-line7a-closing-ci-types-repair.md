# Capital-Gain Distributions / Line 7a — Closing CI Type Repair

Audience: Builder.

Status: **chartered for dispatch.**

## Context Capsule

- **Source ref and resolved launch commit:** branch
  `track/capital-gain-distributions-line7a-track3-presentation` at closing
  custody commit `2683a795c6e279aa37e65ec5d4e9ab03bc44ae83`.
  Closing PR #128 is open against `main`.
- **Exact object:** repair the four `no-any-return` errors reported by PR #128
  `verify` run `30615579462` in
  `tests/test_capital_gain_distributions_line7a_t3_presentation.py` lines 20,
  24, 28, and 32. Pytest passed before mypy failed; governance lint and the
  envelope scan were skipped by CI.
- **Role:** Closing CI Types Repair Builder, Low tier / medium effort.
- **Scope and evidence-rung ceiling:** change only
  `tests/test_capital_gain_distributions_line7a_t3_presentation.py`. Give the
  four JSON-loading test helpers an honest static return type accepted by
  mypy without changing their runtime values, fixtures, test cases,
  assertions, projector behavior, or production code. The failed CI log,
  focused module, and full repository mypy command are the ceiling.
- **Stop conditions:** stop and report if repair requires changing production
  code, another test or tool, content, fixtures, goldens, schemas, packages,
  records, charters, pointers, accepted ADRs, governance, or CI configuration;
  weakening/removing a test or assertion; changing JSON values or test
  behavior; ignoring the error globally; adding a broad untyped escape; using
  real/private material; or interpreting governance.
- **Full reads before acting:** this charter; `docs/roles/builder.md`; PR #128
  failed `verify` log for run `30615579462`;
  `tests/test_capital_gain_distributions_line7a_t3_presentation.py`;
  `docs/reviews/2026-07-30-capital-gain-distributions-line7a-track3-repair-recheck.md`;
  and `AGENTS.md#Data Safety Rules`.

Before editing, echo the four exact mypy errors, one-file ceiling, runtime and
test-semantics byte/behavior constraint, evidence ceiling, credited pytest
result, and every stop condition.

## Required repair

Resolve all four helper return-type errors locally and explicitly. The repair
must preserve:

1. the same four content files and UTF-8 reads;
2. the same decoded JSON objects at runtime;
3. every F1/F2/F3 mutation, positive, legacy, and golden assertion;
4. the six-test module count and outcomes; and
5. every file outside the focused test byte-for-byte.

Do not suppress mypy for the file or module, use `type: ignore`, widen helper
return types to `Any`, or alter production code.

## Verification

Run once after editing:

```text
python3 -m unittest tests.test_capital_gain_distributions_line7a_t3_presentation
python3 -m mypy
git diff --name-only <repair-charter-commit>..HEAD
git diff --check <repair-charter-commit>..HEAD
python3 tools/governance_lint.py
python3 tools/envelope_scan.py --range main..HEAD
```

The name-only result must be exactly the focused test file. Do not rerun the
full pytest suite; PR #128 already passed that step before the type failure.

## Handoff

Commit one type-repair commit after this charter/pointer commit. Leave the
worktree clean and report the SHA, exact typing change, runtime-equivalence
evidence, focused test and mypy results, one-file range, remaining safety
results, and any stop finding. Do not review, edit pointers, push, update the
PR, merge, select future scope, or perform closeout.
