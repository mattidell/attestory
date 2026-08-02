# Capital-Gain Distributions / Line 7a — Track 2 CI Type Repair Charter

Audience: Builder.

Status: **chartered for the two mypy failures exposed after pytest became
green.**

## Context Capsule

- **Source ref and resolved launch commit:** branch
  `track/capital-gain-distributions-line7a-track2` (PR #120) at this committed
  charter/pointer. Resolve `HEAD` through the orientation command and verify it
  against Git before acting.
- **Exact object:** only the two errors reported by PR #120 `verify` run
  `30592111125` in
  `tests/tax/test_capital_gain_distributions_line7a_t2_package.py`: line 19
  returns `Any` from a `dict[str, Any]` loader, and line 128 indexes a value
  inferred as `object`.
- **Role:** the original Track-2 Builder lineage, performing a mechanical
  test-typing repair.
- **Scope and evidence-rung ceiling:** add only explicit typing needed for the
  existing test data shapes. No behavior, fixture, production, schema, package,
  golden, or assertion change. Static typing plus the affected unittest module
  is the ceiling.
- **Stop conditions:** stop if the repair requires changing production code,
  test behavior or assertions, fixture bytes, a schema/package/golden, the
  mypy configuration, or suppressing an error with `type: ignore`; if any file
  besides the named test module must change; if governance interpretation or
  real/private material is implicated.
- **Full reads before acting:** this charter; `docs/roles/builder.md`; the
  named test module; `packages/derivation/package_validation.py`;
  `packages/derivation/loader.py`; `AGENTS.md#Fixture Rules`; and
  `AGENTS.md#Data Safety Rules`.

Before editing, echo both errors, the one-file/no-behavior ceiling, and every
stop condition.

## Required repair and verification

Use ordinary typed narrowing (`typing.cast` and/or explicit local mapping
annotations) so mypy understands the shapes already used by the test. Do not
alter execution.

Run once:

```text
python3 -m unittest tests.tax.test_capital_gain_distributions_line7a_t2_package
python3 -m mypy
git diff --check <charter-commit>..HEAD
python3 tools/envelope_scan.py --range main..HEAD
```

Commit one repair commit, leave the worktree clean, and report the SHA, exact
typing changes, and results. Do not review, edit pointers/charters, push, merge,
or begin Track 3.
