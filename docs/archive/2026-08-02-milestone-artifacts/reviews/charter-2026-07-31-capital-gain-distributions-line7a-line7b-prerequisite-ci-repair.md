# Capital-Gain Distributions / Line 7a — Line 7b Prerequisite CI Repair

Audience: Builder.

Status: **chartered for the single stale loader assertion exposed by CI.**

## Context Capsule

- **Source ref and resolved launch commit:** branch
  `track/capital-gain-distributions-line7a-line7b-prerequisite` at this committed
  charter/pointer. Resolve and verify `HEAD` before acting.
- **Exact object:** PR #125 `verify` run `30594309628` passed 743 tests and
  failed only
  `Line7FormAndCitation.test_line_7a_and_7b_form_fields_load_through_production_loader`.
  The test still expects the historical v1 line-7b binding although the
  production loader now correctly selects the published v2 successor.
- **Role:** the prerequisite Builder continues its own lineage for this
  one-file CI repair.
- **Scope and evidence-rung ceiling:** update only
  `tests/test_capital_gain_distributions_line7a_t1_citizens.py` so it asserts
  current v2 selection and explicit historical v1 preservation. No production,
  fixture, package, registry, release, adoption, generator, schema, or
  configuration change. Focused unittest and mypy are the ceiling.
- **Stop conditions:** stop if any other file must change; if fixing the test
  requires changing loader behavior, weakening citation/field validation,
  deleting the v1 expectation rather than preserving it explicitly,
  suppressing typing, interpreting governance, or touching real/private
  material.
- **Full reads before acting:** this charter; `docs/roles/builder.md`; the
  failing test class; `packages/tax/loader.py`; field v1 and v2; the
  prerequisite review record; and `AGENTS.md#Data Safety Rules`.

Before editing, echo the exact failure, one-file ceiling, v1/v2 assertions, and
every stop condition.

## Required repair and verification

Keep the existing line-7a and citation assertions. Assert that
`load_form_fields` selects line-7b v2 with the new generic line-7b rule symbol,
and separately load the historical v1 file to prove its version and original
conclusion binding remain unchanged.

Run once:

```text
python3 -m unittest tests.test_capital_gain_distributions_line7a_t1_citizens
python3 -m unittest tests.test_capital_gain_distributions_line7a_line7b_prerequisite
python3 -m mypy
git diff --check <charter-commit>..HEAD
python3 tools/envelope_scan.py --range main..HEAD
```

Commit one CI-repair commit and leave the tree clean. Report the SHA, exact
assertion changes, and results. Do not review, edit pointers/charters, push,
merge, restart Track 3, or begin Track 4.
