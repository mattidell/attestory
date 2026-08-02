# Capital-Gain Distributions / Line 7a — Track 2 CI Type Repair Recheck

Audience: Reviewer.

Status: **chartered for a focused author-independent recheck.**

## Context Capsule

- **Source ref and resolved launch commit:** branch
  `track/capital-gain-distributions-line7a-track2` (PR #120) at this committed
  charter/pointer. Resolve and verify `HEAD` before acting.
- **Exact object:** the immediate parent commit titled
  `Fix Track 2 package test typing`, measured against its immediate parent
  charter. It may change only
  `tests/tax/test_capital_gain_distributions_line7a_t2_package.py`.
- **Role:** the existing independent Track-2 CI Reviewer, continuing its review
  lineage without Builder exposure.
- **Scope and evidence-rung ceiling:** verify the delta is typing-only, closes
  the two reported mypy errors, and preserves identical runtime tests. Static
  typing and the affected unittest module are the ceiling.
- **Stop conditions:** return `NOT READY` if any other file changed; runtime
  data, assertions, control flow, fixtures, production code, mypy
  configuration, or schema/package/golden bytes changed; an error was
  suppressed; the focused unittest or mypy fails; or governance/private
  material is implicated.
- **Full reads before acting:** this charter; `docs/roles/reviewer.md`;
  `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-30-capital-gain-distributions-line7a-track2-ci-types-repair.md`;
  the exact implementation delta; and `AGENTS.md#Data Safety Rules`.

Before measuring, echo the exact range/file, typing-only ceiling, and stop
conditions.

## Measurements and handoff

Inspect the parsed diff and confirm the only semantic additions are an imported
`cast`, a cast of the existing `json.loads` result to its declared
`dict[str, Any]` return type, and an explicit `dict[str, Any]` annotation on
the existing `bad_line9` mapping.

Run once:

```text
python3 -m unittest tests.tax.test_capital_gain_distributions_line7a_t2_package
python3 -m mypy
git diff --check <repair-charter>..<implementation>
python3 tools/envelope_scan.py --range main..HEAD
```

Commit one review record at
`docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-30-capital-gain-distributions-line7a-track2-ci-types-review.md`
with a falsifiable `READY` or `NOT READY` verdict and exact evidence. Leave the
tree clean. Do not repair, edit pointers/charters, push, merge, or begin Track
3.
