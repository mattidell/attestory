# Capital-Gain Distributions / Line 7a — Track 1 F1 Repair Recheck

Audience: Reviewer.

Status: **chartered for owner launch.**

## Context Capsule

- **Source ref and resolved launch commit:** branch
  `track/capital-gain-distributions-line7a-track1` at repair commit
  `8cbd274aafee6f1f9be2533e1141fff04f135096`.
- **Exact object or commit range:** focused repair range
  `1cbc3ad7f69c2c8bff755b95ff89dbfa4e476388..8cbd274aafee6f1f9be2533e1141fff04f135096`.
  The accepted build baseline is `b8a44e3`; original review `d5b4886`
  credited every measurement except F1.
- **Role:** the author-independent Track-1 Reviewer, High tier / high effort.
  This is a focused repair recheck, not a second broad review cycle.
- **Scope and evidence-rung ceiling:** determine only whether repair commit
  `8cbd274` closes F1 without violating the repair charter or disturbing
  credited passing measurements. Schema/content validation evidence only.
- **Stop conditions:** stop and report if the exact range or tip differs; if
  the repair changes anything outside the focused test surface; if closure
  would require accepting a test-local validator/private reconstruction as
  production evidence; if a specific failure cannot be attributed without a
  base comparison; if governance interpretation is required; or if any
  real/private material is encountered.
- **Full reads before acting:** this charter; `docs/roles/reviewer.md`;
  `docs/reviews/2026-07-29-capital-gain-distributions-line7a-track1-review.md`;
  `docs/reviews/charter-2026-07-29-capital-gain-distributions-line7a-track1-repair.md`;
  the exact repair diff;
  `tests/test_capital_gain_distributions_line7a_t1_citizens.py`;
  `packages/derivation/package_validation.py`;
  `packages/derivation/loader.py`;
  `packages/content/tax/2025/form1040.line-7b.form-field.json`;
  `packages/content/tax/2025/citation.form1040.line-7b.json`;
  both line-7b citation negatives; ADR-0050 Decision 8 and Production
  conditions; `AGENTS.md#Schema Publication Protocol`; and
  `AGENTS.md#Data Safety Rules`.

Before reviewing, echo the exact repair range, F1 closure question, credited
measurements, evidence ceiling, and stop conditions.

## Focused measurements

1. **Range containment.** Confirm the repair changes only the focused Track-1
   test and neither alters implementation citizens nor introduces runtime
   production behavior. Any unrelated change is `NOT READY`.
2. **Production-boundary honesty.** Read the helper and the invoked
   `validate_package` implementation. Determine whether the wrong-identity
   failure is produced by the established ADR-0029 exact citation-membership
   check on a structurally valid production-shaped package, rather than by a
   test-local identity comparison, private validator, hard-coded test
   allowlist, or an unrelated earlier error. Verify the helper does not smuggle
   the expected verdict into the validator input in a way no adopting package
   could honestly reproduce.
3. **Three-way result.** Independently exercise:
   - committed line-7b field + required citation: accepted;
   - wrong-identity field + required citation package member: rejected with
     exactly the citation-membership failure attributable to the wrong pin;
   - multiple-citation field: rejected at schema cardinality, not conflated with
     wrong identity.
4. **F1 contract.** Confirm the accepted case still has exactly one pin to
   `tax.us.2025.citation.form1040.line-7b@v1` at ADR-0050's fixed locus and that
   the named wrong-identity negative now supplies reproducible rejection
   evidence at the relevant production validation boundary.
5. **Credited measurements and safety.** Since the repair claims a test-only
   delta, verify the previously accepted C1–C4, conclusion, box-2a topology,
   universe, schemas, manifests, form fields, citations, and fixtures are
   byte-unchanged from `b8a44e3`. Run the envelope scan over the full unit.

## Verification

Run once:

```text
python3 -m unittest tests.test_capital_gain_distributions_line7a_t1_citizens
python3 -m unittest tests.test_schema_registry
git diff --check 1cbc3ad7f69c2c8bff755b95ff89dbfa4e476388..8cbd274aafee6f1f9be2533e1141fff04f135096
python3 tools/governance_lint.py
python3 tools/envelope_scan.py --range main..HEAD
```

Do not run the full suite merely to duplicate CI.

## Review record and verdict

Write
`docs/reviews/2026-07-29-capital-gain-distributions-line7a-track1-repair-recheck.md`
and commit it on the same branch. Return exactly one verdict:

- `READY` — F1 is closed and credited measurements remain intact; or
- `NOT READY` — a numbered, reproducible residual explains why F1 is not
  closed or why the repair violated its charter.

Do not edit implementation, tests, prior reviews, charters, phase state, or the
milestone plan. Do not design another repair, push, open/merge a PR, or begin
Track 2. Stop after committing the focused recheck record.
