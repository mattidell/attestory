# Capital-Gain Distributions / Line 7a — Track 3 F1–F3 Repair Recheck

Audience: Reviewer.

Status: **chartered for owner launch.**

## Context Capsule

- **Source ref and resolved launch commit:** branch
  `track/capital-gain-distributions-line7a-track3-presentation` at repair
  commit `202ae9740da7689478f0cb52386f061b4ff01b1d`. The review-charter/pointer
  commit is context and must be its direct successor.
- **Exact object or commit range:** focused repair range
  `3b3291307d7a4258a2f5476208e1cecd2c0ed103..202ae9740da7689478f0cb52386f061b4ff01b1d`.
  It contains exactly one repair commit. The original review credited every
  Track-3 measurement except F1, F2, and F3; the earlier repair-charter stop
  landed no implementation.
- **Role:** the original author-independent Track-3 Reviewer continues its own
  review lineage, High tier / high effort. This is a focused delta recheck,
  not a second broad review and not a review of the prior review record.
- **Scope and evidence-rung ceiling:** determine only whether the one repair
  commit closes F1–F3 without violating the amended repair charter or
  disturbing credited evidence. Static projector mutations plus the existing
  synthetic v8/v3 `live_coordinate_run` goldens are the ceiling. No real
  browser/workspace session, real data, new product surface, or contract
  reopening.
- **Stop conditions:** stop and report if the repair range, tip, or direct
  review-charter ancestry differs; if the repair changes anything outside
  `packages/derivation/presentation_projection.py` and
  `tests/test_capital_gain_distributions_line7a_t3_presentation.py`; if closure
  requires a new or changed schema, citizen, accepted ADR, tax rule,
  form-field, citation, package, release, adoption, resolver, evaluator
  operation, caller-facing result, or internal model version; if generic
  projector logic contains a tax-specific line-7a/line-7b identity or branch;
  if a valid golden, browser fixture/manifest, product/frozen-harness page,
  Track-1/2 computation, admission, lifecycle, package validation, or legacy
  no-citations presentation path changes; if an existing validator or test is
  weakened; if a failure cannot be attributed without a base comparison; if
  governance interpretation is required; or if any real/private material is
  encountered.
- **Full reads before acting:** this charter; `docs/roles/reviewer.md`;
  `docs/reviews/2026-07-30-capital-gain-distributions-line7a-track3-review.md`;
  `docs/reviews/charter-2026-07-30-capital-gain-distributions-line7a-track3-repair.md`;
  `docs/reviews/2026-07-30-capital-gain-distributions-line7a-track3-repair-charter-stop.md`;
  `docs/reviews/charter-2026-07-30-capital-gain-distributions-line7a-track3.md`;
  `docs/reviews/charter-2026-07-30-capital-gain-distributions-line7a-track3-review.md`;
  `docs/phases/engine-breadth/milestones/capital-gain-distributions-line7a.md`;
  `docs/adr/0050-capital-gain-distributions-and-line-7a.md`;
  `docs/adr/0046-presentation-surface-contract.md`;
  `docs/adr/0012-form-field-citizens-and-rendered-dispositions.md`;
  `docs/adr/0031-real-data-residency-boundary.md`; the exact repair diff;
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
  `tests/test_presentation_live_session.py`;
  `tests/test_capital_gain_distributions_line7a_line7b_prerequisite.py`;
  `tests/test_capital_gain_distributions_line7a_t2_coordinator.py`;
  `tools/generate_capital_gain_distributions_line7a_t3_presentation_goldens.py`;
  `packages/sample_data/capital_gain_distributions_line7a_t3/presentation/eligible.presentation-model.v1.json`;
  `packages/sample_data/capital_gain_distributions_line7a_t3/presentation/missing-authority.presentation-model.v1.json`;
  `packages/sample_data/capital_gain_distributions_line7a_t3/presentation/schedule-d-required.presentation-model.v1.json`;
  `AGENTS.md#Fixture Rules`; and `AGENTS.md#Data Safety Rules`.

Before reviewing, echo the exact repair range and ancestry, F1/F2/F3 closure
questions, credited evidence, generic categorical invariant, generic
declared-citation chain, byte-identity constraints, evidence ceiling,
independence posture, and every stop condition.

## Focused measurements

1. **Exact range and containment.** Confirm the repair range contains exactly
   one commit and changes only the two chartered projector/test files. Map each
   hunk to F1, F2, F3, a required kill test, or legacy-path preservation.
   Reject unrelated cleanup or any changed schema, content, package, golden,
   renderer, browser fixture, manifest, phase pointer, or process record.
2. **F1 exact fixed categorical value.** Independently exercise the declared
   categorical field with `"checked"`, `"no"`, `"unchecked"`, `""`,
   non-string, and another arbitrary string. Only a source value exactly equal
   to the field's fixed render instruction may project. Confirm the accepted
   categorical model remains atomic and contains no copied categorical value.
   Grep the generic projector for tax-specific field IDs or special-case
   branching.
3. **F2/F3 generic citation-chain closure.** Read the entire join and prove
   that duplicate resolved `citation.v1` identities reject globally rather
   than overwrite. For a published field whose joined owning rule declares a
   non-empty `citations` list, require a well-formed field citation; the owning
   rule to publish the joined symbol and declare that exact citation exactly
   once; and exactly one resolved citation citizen with the same identity and
   version. Independently mutate missing, duplicate, wrong-identity, and
   wrong-version citations for categorical line 7b and numeric line 7a,
   including a mutated field accompanied by the matching wrong resolved
   citizen. Every mutation must fail before a presentation artifact is
   written. Confirm a legacy owning rule with no `citations` declaration keeps
   the established v1/v6-compatible path.
4. **Kill-test honesty.** Inspect every new test input and assertion so it can
   fail for the named F1/F2/F3 reason rather than an earlier malformed fixture
   or a test-local identity check. Require explicit coverage for alternate and
   empty categorical strings; duplicate resolved citations; matching wrong
   field/resolved citation identity; wrong version; missing categorical
   citation; missing, wrong, and duplicate numeric citations; the legacy
   no-citations rule; and valid atomic numeric/categorical paths.
5. **Valid-output byte identity.** Independently regenerate the eligible,
   missing-authority, and Schedule-D-required Track-3 presentation models in a
   temporary location through `live_coordinate_run` and compare exact bytes to
   the committed goldens. Confirm the repair range leaves the established
   v1/v6 presentation golden, internal model version, product page, frozen
   harness copy, browser fixtures, and manifests byte-identical.
6. **Credited evidence and safety.** Re-run only the focused projector,
   integration, live-session, prerequisite, Track-2 coordinator, and
   slice-specific harness checks below. Confirm projector rejection still
   writes neither result nor presentation artifact, valid line-7a/line-7b
   output remains atomic, and the original review's other credited
   presentation, redaction, accessibility, DOM-safety, harness-parity, and
   lifecycle measurements remain outside the delta. Run the exact-range check,
   governance lint, and envelope scan.

## Verification

Run once, independently:

```text
python3 -m unittest tests.test_capital_gain_distributions_line7a_t3_presentation
python3 -m unittest tests.test_presentation_l2_integration
python3 -m unittest tests.test_presentation_live_session
python3 -m unittest tests.test_capital_gain_distributions_line7a_line7b_prerequisite
python3 -m unittest tests.test_capital_gain_distributions_line7a_t2_coordinator
node tools/presentation_harness/run.mjs --manifest tools/presentation_harness/examples/manifests/capital-gain-distributions-line7a.v1.json
git diff --check 3b3291307d7a4258a2f5476208e1cecd2c0ed103..202ae9740da7689478f0cb52386f061b4ff01b1d
python3 tools/governance_lint.py
python3 tools/envelope_scan.py --range main..HEAD
```

Do not run the full suite merely to duplicate CI. Use a base comparison only
to attribute a specific new failure.

## Review record and verdict

Write
`docs/reviews/2026-07-30-capital-gain-distributions-line7a-track3-repair-recheck.md`
and commit it on the same branch. Return exactly one verdict:

- `READY` — F1, F2, and F3 are closed, the amended repair charter holds, and
  credited evidence remains intact; or
- `NOT READY` — a numbered, reproducible residual explains which finding is
  not closed or how the repair violated its charter.

Do not edit implementation, tests, prior reviews, charters, phase state, the
milestone plan, goldens, renderer pages, browser fixtures, or manifests. Do not
design another repair, push, open or merge a PR, begin Track 4, or review your
own record. Stop after committing the focused recheck record and return custody
to the foreman.
