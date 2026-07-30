# Capital-Gain Distributions / Line 7a — Track 1 F1 Repair Charter

Audience: Builder.

Status: **chartered for owner launch.**

## Context Capsule

- **Source ref and resolved launch commit:** branch
  `track/capital-gain-distributions-line7a-track1` at review commit
  `d5b48865fb82410240160c4d11e34d720dba5ee5`.
- **Exact object:** repair only F1 from
  `docs/reviews/2026-07-29-capital-gain-distributions-line7a-track1-review.md`.
  The accepted implementation baseline is
  `b8a44e37462c464e5f9989dff24477d17f51930f`; every passing review
  measurement is credited and must remain unchanged.
- **Role:** the original Track-1 Builder, Medium tier / medium effort. This is
  the one findings-only repair allowed by the milestone plan.
- **Scope and evidence-rung ceiling:** make the wrong line-7b citation identity
  fixture reject at the production-relevant content-validation boundary while
  preserving the valid citizen and the already-rejecting multiple-citation
  case. Schema/content validation only.
- **Stop conditions:** stop and report if the repair would require changing
  accepted ADR-0050, weakening or renaming the negative, accepting a test-only
  validator as production evidence, embedding tax-year/line-specific doctrine
  in a generic reusable schema, mutating any published historical schema or
  checksum, adding evaluator/coordinator/package/admission/presentation
  behavior, interpreting governance text, or touching real/private material.
  If no existing production-relevant validation boundary can enforce the
  content contract without one of those violations, return a charter-stop
  finding instead of inventing substrate.
- **Full reads before acting:** this charter; `docs/roles/builder.md`;
  `docs/reviews/charter-2026-07-29-capital-gain-distributions-line7a-track1.md`;
  `docs/reviews/2026-07-29-capital-gain-distributions-line7a-track1-review.md`;
  ADR-0050 Decision 8 and Production conditions;
  `packages/content/tax/2025/form1040.line-7b.form-field.json`;
  `packages/content/tax/2025/citation.form1040.line-7b.json`;
  `packages/sample_data/capital_gain_distributions_line7a_t1/negatives/form-field.v3.line-7b-wrong-citation-id.json`;
  `packages/sample_data/capital_gain_distributions_line7a_t1/negatives/form-field.v3.line-7b-multi-citation.json`;
  `tests/test_capital_gain_distributions_line7a_t1_citizens.py`;
  `packages/tax/loader.py`; `AGENTS.md#Schema Publication Protocol`; and
  `AGENTS.md#Data Safety Rules`.

Before editing, echo F1, the credited passing measurements, the evidence
ceiling, and every stop condition.

## Required repair

1. Preserve the valid line-7b field's single exact citation pin:
   `tax.us.2025.citation.form1040.line-7b@v1`, at ADR-0050's fixed 2025 Form
   1040 Instructions locus.
2. Make the committed wrong-identity negative fail specifically because its
   citation identity is not the required line-7b identity. The rejection must
   occur through an established production-relevant content loading or
   validation path, not a test-local helper or an assertion comparing fixture
   bytes.
3. Preserve rejection of the multiple-citation negative and acceptance of the
   valid committed line-7b citizen.
4. Keep the repair generic at the correct boundary: do not put 2025 line-7b
   doctrine into a reusable generic form-field schema. Do not change the
   already-reviewed C1–C4, conclusion, box-2a topology, universe, other form
   field, citations, examples, schemas, or manifest additions except for a
   mechanically necessary focused test/validation adjustment.
5. Add a focused regression assertion whose failure message distinguishes
   wrong identity from wrong cardinality.

## Verification

Run once:

```text
python3 -m unittest tests.test_capital_gain_distributions_line7a_t1_citizens
python3 -m unittest tests.test_schema_registry
git diff --check d5b48865fb82410240160c4d11e34d720dba5ee5..HEAD
python3 tools/governance_lint.py
python3 tools/envelope_scan.py --range main..HEAD
```

Run a touched established loader test module if the repair changes its
production surface. Do not rerun the full suite; CI remains the gate of record.

## Handoff

Commit one repair commit, leave the worktree clean, and report its SHA, exact
files changed, focused results, and whether every credited passing measurement
remains structurally untouched. Do not review the repair, edit the review
record or pointers, push, open a PR, or begin Track 2. The foreman will charter
the focused recheck.
