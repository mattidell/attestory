# Capital-Gain Distributions / Line 7a — Track 1 F1 Repair Recheck

**Verdict: READY**

## Object and posture

- Reviewed branch: `track/capital-gain-distributions-line7a-track1`.
- Orientation resolved `HEAD` to
  `51c16bb306d1054d775a117157d24d9374a9b57e`; `git rev-parse HEAD`
  independently matched it.
- Exact repair object:
  `1cbc3ad7f69c2c8bff755b95ff89dbfa4e476388..8cbd274aafee6f1f9be2533e1141fff04f135096`.
- This was an author-independent focused recheck of F1 only. The Builder's
  thread and self-assessment were not consulted.
- Evidence ceiling: schema/content validation only. Track-2 runtime behavior
  was not evaluated.
- Freshness: after `git fetch origin --prune`,
  `git rev-list --left-right --count origin/main...HEAD` returned `0 7` and
  the merged-PR query for this branch returned no result.

## Measurements

1. **Range containment — pass.** The exact repair diff changes only
   `tests/test_capital_gain_distributions_line7a_t1_citizens.py`. It does not
   alter implementation citizens, schemas, manifests, fixtures, package
   validator implementation, or runtime behavior.
2. **Production-boundary honesty — pass.** The focused helper constructs a
   schema-valid `artifact-package.v4` with normal form-field, citation, and
   computation members, recomputes its package checksum, and calls the
   established production `validate_package` with `DerivationSchemas`. It does
   not compare the wrong pin to a hard-coded expected identity; the production
   validator's generic form-field citation-membership check performs the exact
   `(id, version)` membership decision at
   [`packages/derivation/package_validation.py:457`](../../packages/derivation/package_validation.py#L457).
   The package membership is the ordinary, reproducible boundary any adopting
   package uses; the test wrapper supplies no private validator or alternate
   verdict logic.
3. **Independent three-way result — pass.** A separate in-memory construction
   of the same production-shaped package, calling `validate_package` directly,
   produced:

   ```text
   committed      ok=True,  issues=[]
   wrong-identity ok=False, issues=[
     (CITATION_ABSENT, demo.form1040.line-7b,
      "form-field citation ('demo.citation.form1040.line-7a', 'v1') is not an exact citation package member")
   ]
   multi-citation form-field.v3 schema error:
     citation ... is not of type 'object'
   ```

   Thus the wrong identity is a single attributable package citation-membership
   failure, while the multiple-citation negative remains a distinct earlier
   schema-cardinality failure.
4. **F1 contract — pass.** The committed line-7b citizen remains an atomic
   single pin to `tax.us.2025.citation.form1040.line-7b@v1`, and its printed
   locator retains ADR-0050's fixed 2025 Form 1040 Instructions line-7b
   paragraph at
   [`packages/content/tax/2025/form1040.line-7b.form-field.json:13`](../../packages/content/tax/2025/form1040.line-7b.form-field.json#L13).
   The wrong-identity negative now has reproducible rejection evidence at the
   production package-validation boundary.
5. **Credited measurements and safety — pass.** Comparing
   `b8a44e37462c464e5f9989dff24477d17f51930f` with the repair commit over
   `packages/content`, `packages/schemas`, and the Track-1 sample-data tree
   produced no diff. The previously credited C1–C4, checked conclusion,
   box-2a topology, universe, schemas, manifests, fields, citations, and
   fixtures therefore remain byte-unchanged. The full-unit envelope scan
   completed cleanly; the focused test change contains only synthetic
   `demo.*` material.

## Commands run once and results

```text
python3 -m unittest tests.test_capital_gain_distributions_line7a_t1_citizens
# Ran 21 tests in 2.695s — OK

python3 -m unittest tests.test_schema_registry
# Ran 10 tests in 0.070s — OK

git diff --check 1cbc3ad7f69c2c8bff755b95ff89dbfa4e476388..8cbd274aafee6f1f9be2533e1141fff04f135096
# clean

python3 tools/governance_lint.py
# governance lint: conformant

python3 tools/envelope_scan.py --range main..HEAD
# clean (exit 0)
```

F1 is closed. No residual finding is recorded.
