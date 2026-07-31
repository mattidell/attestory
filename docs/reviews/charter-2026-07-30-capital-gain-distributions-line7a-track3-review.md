# Capital-Gain Distributions / Line 7a — Track 3 Independent Review Charter

Audience: Reviewer.

Status: **chartered for owner launch.**

## Context Capsule

- **Source ref and resolved launch commit:** branch
  `track/capital-gain-distributions-line7a-track3-presentation` with
  implementation commit `75c0de90ecd271a8f552657af66206be111b0038`.
  The review-charter commit is context and must be its direct successor.
- **Exact object or commit range:** implementation range
  `53a9ecf86ee6f634c859704e8c068c9de9540476..75c0de90ecd271a8f552657af66206be111b0038`.
  The preceding `53a9ecf` commit binds the Builder charter and phase pointer;
  it is context, not part of the implementation object.
- **Role:** one fresh author-independent Reviewer, High tier / high effort.
  Do not consult the Builder's thread, summary, rationale, or self-assessment.
- **Scope and evidence-rung ceiling:** measure Track 3's zero-authority
  line-7a/line-7b projection, strict internal model, v8/v3 synthetic goldens,
  product/frozen-harness rendering, browser attack matrix, and integrated
  regression through `live_coordinate_run` and the synthetic harness. No real
  browser/workspace session, real data, tax computation redesign, repair
  implementation, Track 4 records, or reopening ADR-0050/ADR-0046.
- **Stop conditions:** stop and report if the implementation object is not the
  exact single-commit range above or the review-charter commit is not its direct
  successor; if an accepted ADR, published schema, historical content/package,
  v1/v6 presentation golden, Track-1/2 computation, contribution/admission,
  package-validation, or resolver behavior changed; if projection requires
  tax-specific IDs or doctrine rather than generic resolved symbol/citation
  joins; if product and frozen harness pages drift beyond their intentional
  provenance wording; if a real browser/workspace, personal material,
  Schedule D, Form 8949, Form 1099-B, excluded-box computation, filing, or
  transmission appears; if governance interpretation is required; or if a
  failure cannot be attributed to this range without a base comparison.
- **Full reads before acting:** this charter;
  `docs/roles/reviewer.md`;
  `docs/reviews/charter-2026-07-30-capital-gain-distributions-line7a-track3.md`;
  `docs/reviews/2026-07-31-capital-gain-distributions-line7a-track3-charter-stop.md`;
  `docs/reviews/2026-07-31-capital-gain-distributions-line7a-line7b-prerequisite-review.md`;
  `docs/phases/engine-breadth/milestones/capital-gain-distributions-line7a.md`;
  `docs/adr/0050-capital-gain-distributions-and-line-7a.md`;
  `docs/adr/0046-presentation-surface-contract.md`;
  `docs/adr/0031-real-data-residency-boundary.md`;
  `docs/adr/0012-form-field-citizens-and-rendered-dispositions.md`;
  every file in the exact implementation range;
  `packages/derivation/live.py`;
  `packages/derivation/live_session.py`;
  `tools/generate_presentation_l2_golden.py`;
  `tools/presentation_harness/examples/manifests/citation-walk.v1.json`;
  `tools/presentation_harness/examples/manifests/citation-walk-production-shaped.v1.json`;
  `tests/test_presentation_l2_integration.py`;
  `tests/test_presentation_live_session.py`;
  `tests/test_presentation_live_viewing_vehicle.py`;
  `tests/test_capital_gain_distributions_line7a_line7b_prerequisite.py`;
  `tests/test_capital_gain_distributions_line7a_t2_coordinator.py`;
  `AGENTS.md#Fixture Rules`; and `AGENTS.md#Data Safety Rules`.

Before reviewing, echo the resolved implementation commit and ancestry, exact
range, review ceiling, independence constraint, authoritative golden
entrypoint, zero-authority and blanket-redaction constraints,
immutable-history constraint, and every stop condition.

## Required measurements

1. **Exact object, history, and boundary.** Enumerate the one-commit range and
   map all 13 changed files to the Builder charter's eight deliverables.
   Confirm no tax computation, admission, package/resolver, schema, accepted
   ADR, Track-4 record, real-session, or unrelated UI work rode inside it.
   Treat both HTML copies and every generated JSON file as review surfaces.
2. **Authoritative v8/v3 goldens.** Independently regenerate the three
   slice-specific presentation models and compare exact bytes with the
   committed goldens. Prove their act logs adopt the v8 package through the v3
   registry/release route and enter only through `live_coordinate_run`, never
   a hand-built `RunContext`. Confirm the established v1/v6 golden and
   generator remain unchanged. Exercise eligible, missing-authority, and
   Schedule-D-required cases at the authoritative entrypoint.
3. **Generic projection and citation identity.** Recover the projector's join
   from resolved form-field `binds_symbol` to one atomic rule disposition.
   Confirm line 7a accepts only finite numeric publications and line 7b accepts
   only the field's declared fixed categorical `"checked"` presentation.
   Grep for tax-specific line-7a/line-7b identifiers or branching in generic
   projector code. Independently mutate missing, duplicate, wrong-version, and
   wrong-identity field citations, ambiguous dispositions, nonnumeric line 7a,
   and malformed categorical line 7b; each must fail closed before an artifact
   is written.
4. **Atomic states and blanket redaction.** For both fields, verify published,
   blocked, and guard-inapplicable states are atomic. Blocked/inapplicable rows
   must carry no value key, stale act, checkbox state, or rejected categorical
   value. Independently inject smuggled values into blocked and inapplicable
   models and prove no visible text, accessible name, diagnostic, citation, or
   serialized browser result leaks them.
5. **Strict internal model and write boundary.** Validate each committed model
   through the strict internal validator. Mutate schema version, unknown keys,
   citation structure, value type, disposition cardinality, and unsafe strings.
   Confirm projection or validation failure leaves neither result nor reserved
   presentation artifact, and does not change the established caller-facing
   result shape or session behavior.
6. **Product-page accessibility and DOM safety.** Inspect and exercise every
   new render path. The affirmative line-7b checked state must be legible to
   assistive technology; citations must remain structurally associated,
   keyboard reachable, and visibly focusable. Confirm dynamic content uses
   node construction and `textContent`, never dynamic `innerHTML`, and that
   unsafe strings remain inert.
7. **ADR-0046 attack set and blast containment.** Independently measure
   section-level blocking, fail-loud local error banners, healthy-sibling
   survival when line 7a is broken, structural citation identity, and rejected
   value redaction. A malformed field may block only its owned subsection;
   it must not erase an otherwise valid line-7b sibling or unrelated existing
   line/attachment/citation groups.
8. **Frozen harness parity and browser matrix honesty.** Compare the product
   and frozen harness pages after normalizing only the established intentional
   provenance wording. Run every new manifest case and inspect its selectors,
   assertions, and input fixture so each can fail for the named reason rather
   than an unrelated earlier parse error. Confirm published, blocked,
   inapplicable, citation, accessibility, tamper, and sibling-containment
   classes are represented. Existing baseline manifests must remain unchanged
   and green.
9. **Regression and lifecycle isolation.** Re-run the focused presentation,
   live-session, viewing-vehicle, prerequisite, and Track-2 coordinator
   modules. Confirm result-file confinement, resolver refusal, session teardown,
   numeric diagnostic suppression, existing attachment/citation groups, and
   historical v1 line-7b validity remain intact. Use a base comparison before
   attributing any failure to the implementation range.
10. **Immutable history and data safety.** Verify the exact range does not
    modify any published schema/checksum, accepted ADR, historical tax
    content/package/release/adoption, or established golden unrelated to this
    slice. Inspect every committed identity, value, path, and generated artifact
    for obvious synthetic labeling and run the required envelope scan. No real
    value, disposition, workspace location, absolute machine path, credential,
    or private output may appear.

## Verification

Run once, independently:

```text
python3 -m unittest tests.test_capital_gain_distributions_line7a_t3_presentation
python3 -m unittest tests.test_presentation_l2_integration
python3 -m unittest tests.test_presentation_live_session
python3 -m unittest tests.test_presentation_live_viewing_vehicle
python3 -m unittest tests.test_capital_gain_distributions_line7a_line7b_prerequisite
python3 -m unittest tests.test_capital_gain_distributions_line7a_t2_coordinator
node --test tools/presentation_harness/tests/*.test.mjs
node tools/presentation_harness/run.mjs --manifest tools/presentation_harness/examples/manifests/citation-walk.v1.json
node tools/presentation_harness/run.mjs --manifest tools/presentation_harness/examples/manifests/citation-walk-production-shaped.v1.json
node tools/presentation_harness/run.mjs --manifest tools/presentation_harness/examples/manifests/capital-gain-distributions-line7a.v1.json
git diff --check 53a9ecf86ee6f634c859704e8c068c9de9540476..75c0de90ecd271a8f552657af66206be111b0038
python3 tools/governance_lint.py
python3 tools/envelope_scan.py --range main..HEAD
```

Do not run the full suite merely to duplicate CI. Use a base comparison only
to attribute a specific failure.

## Review record and verdict

Write
`docs/reviews/2026-07-30-capital-gain-distributions-line7a-track3-review.md`
and commit it on the same branch. Report one explicit verdict:

- `READY` — every required measurement passes with cited evidence; or
- `NOT READY` — numbered findings F1… identify the violated
  charter/ADR/publication/safety clause, precise file/line evidence, and a
  reproducible measurement.

Record all commands and results. Findings recommend no scope expansion and no
repair design. Do not edit implementation, manifests, charters, phase state,
or the milestone plan; do not push, open or merge a PR, begin Track 4, or
review your own record. Stop after the review-record commit and return custody
to the foreman.
