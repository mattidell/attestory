# Capital-Gain Distributions / Line 7a — Track 3 Findings-Only Repair Charter

Audience: Builder.

Status: **amended after a clean charter stop; ready for the continuing repair
Builder.**

## Context Capsule

- **Source ref and resolved launch commit:** branch
  `track/capital-gain-distributions-line7a-track3-presentation` at this amended
  charter/pointer commit. It descends from review commit
  `22f281e8094fa126a5424949e01478e15504d11c` through the original repair
  charter and the clean charter-stop record. Resolve `HEAD` through the
  orientation command and verify it against Git before acting.
- **Exact object:** repair only F1–F3 in
  `docs/reviews/2026-07-30-capital-gain-distributions-line7a-track3-review.md`:
  arbitrary categorical source strings are accepted as affirmative checked,
  duplicate or wrong categorical field citations are accepted, and published
  numeric line 7a does not require its exact resolved field citation.
- **Role:** the original Track 3 Builder continues its own implementation
  lineage as repair Builder, Medium tier / medium effort.
- **Scope and evidence-rung ceiling:** change only the generic internal
  presentation projector and focused projector tests needed to close F1–F3.
  Static mutation tests plus the existing synthetic v8/v3
  `live_coordinate_run` goldens are the ceiling. The three committed Track-3
  goldens and both HTML copies must remain byte-identical.
- **Stop conditions:** stop and report if repair requires a new or changed
  schema, citizen, accepted ADR, tax rule, form-field, citation, package,
  release, adoption, resolver, evaluator operation, caller-facing result, or
  internal model version; tax-specific line-7a/line-7b IDs or branching;
  changing a valid golden, browser fixture/manifest, product/frozen-harness
  page, Track-1/2 computation, admission, lifecycle, or package validation;
  weakening an existing validator or test; expanding into a UI redesign,
  Schedule D, Form 8949, Form 1099-B, excluded-box computation, real
  browser/workspace, filing, or transmission; governance interpretation; or
  real/private material.
- **Full reads before acting:** this charter;
  `docs/roles/builder.md`;
  `docs/reviews/2026-07-30-capital-gain-distributions-line7a-track3-review.md`;
  `docs/reviews/2026-07-30-capital-gain-distributions-line7a-track3-repair-charter-stop.md`;
  `docs/reviews/charter-2026-07-30-capital-gain-distributions-line7a-track3.md`;
  `docs/reviews/charter-2026-07-30-capital-gain-distributions-line7a-track3-review.md`;
  `docs/phases/engine-breadth/milestones/capital-gain-distributions-line7a.md`;
  `docs/adr/0050-capital-gain-distributions-and-line-7a.md` Decisions 5 and 8
  plus Production Conditions;
  `docs/adr/0046-presentation-surface-contract.md`;
  `docs/adr/0012-form-field-citizens-and-rendered-dispositions.md`;
  `docs/adr/0031-real-data-residency-boundary.md`;
  `packages/derivation/presentation_projection.py`;
  `packages/derivation/live.py`;
  `packages/content/tax/2025/form1040.line-7a.form-field.json`;
  `packages/content/tax/2025/form1040.line-7b.form-field.v2.json`;
  `packages/content/tax/2025/rule.form1040-line7a.json`;
  `packages/content/tax/2025/rule.form1040-line7b.json`;
  `packages/content/tax/2025/citation.form1040.line-7a.json`;
  `packages/content/tax/2025/citation.form1040.line-7b.json`;
  `tests/test_capital_gain_distributions_line7a_t3_presentation.py`;
  `tests/test_presentation_l2_integration.py`;
  `tools/generate_capital_gain_distributions_line7a_t3_presentation_goldens.py`;
  `AGENTS.md#Fixture Rules`; and `AGENTS.md#Data Safety Rules`.

Before editing, echo the exact three findings, repair file ceiling, generic
categorical-value invariant, generic citation chain, byte-identity constraints,
evidence ceiling, and every stop condition.

## Required repair

1. **Exact fixed categorical publication.** A fixed categorical field may
   project only when the current publication's value exactly equals the
   field's declared fixed render instruction. For the existing checked form,
   only source value `"checked"` is valid. Reject `"no"`, `"unchecked"`, the
   empty string, non-strings, or any other value before constructing a model.
   Keep the categorical value out of the presentation model and renderer.
2. **One generic declared-citation chain.** Reject duplicate resolved
   `citation.v1` identities globally rather than silently overwriting them.
   For a published form field whose owning resolved rule declares a non-empty
   `citations` list, require all of the following through generic identities:
   - the field declares one well-formed citation identity and version;
   - the owning rule publishes the joined symbol and declares that exact field
     citation once;
   - the resolved graph contains exactly one citation citizen with that
     identity and version.
   Missing, duplicate, wrong-identity, or wrong-version citations fail closed
   before a presentation artifact is written. Preserve existing behavior for
   legacy rules that declare no citations; this repair neither validates nor
   backfills their field-citation chain. Do not encode line IDs or expected
   citation IDs in projector logic.
3. **Focused kill tests.** Add explicit failures for each review mutation:
   alternate and empty categorical strings; duplicate resolved citation
   citizens; a mutated field citation accompanied by the matching wrong
   resolved citizen; wrong citation version; missing categorical citation; and
   missing, wrong, or duplicate numeric line-7a citations. Include a legacy
   owning rule without `citations` to prove the existing v1/v6-compatible path
   remains unchanged. Tests must also prove the valid line-7a and line-7b paths
   still succeed and remain atomic.
4. **No valid-output churn.** Regenerate the eligible, missing-authority, and
   Schedule-D-required Track-3 models in memory and prove exact equality with
   committed bytes. Preserve the established v1/v6 presentation golden,
   internal model version, product page, frozen harness copy, browser fixtures,
   and manifest byte-for-byte.

## Verification

Run each focused command once after the repair:

```text
python3 -m unittest tests.test_capital_gain_distributions_line7a_t3_presentation
python3 -m unittest tests.test_presentation_l2_integration
python3 -m unittest tests.test_presentation_live_session
python3 -m unittest tests.test_capital_gain_distributions_line7a_line7b_prerequisite
python3 -m unittest tests.test_capital_gain_distributions_line7a_t2_coordinator
node tools/presentation_harness/run.mjs --manifest tools/presentation_harness/examples/manifests/capital-gain-distributions-line7a.v1.json
git diff --check <repair-charter-commit>..HEAD
python3 tools/governance_lint.py
python3 tools/envelope_scan.py --range main..HEAD
```

Do not run the full suite. Use base comparison only for a specific new failure.

## Handoff

Commit one findings-only repair commit after this charter/pointer commit. Leave
the worktree clean and report the SHA, exact files, F1/F2/F3 kill-test evidence,
valid-golden byte-identity evidence, focused results, and any stop finding. Do
not review, push, open a PR, edit phase pointers, begin Track 4, or alter any
golden/browser artifact.
