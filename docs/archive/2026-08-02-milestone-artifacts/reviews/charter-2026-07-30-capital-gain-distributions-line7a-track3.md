# Capital-Gain Distributions / Line 7a — Track 3 Presentation Builder Charter

Audience: Builder.

Status: **rebound after the line-7b prerequisite merge and ready for Builder
launch.**

## Context Capsule

- **Source ref and resolved launch commit:** `origin/main` at
  `ea542ece491d286c760a7409b68ab051e29bf2b1`, the no-fast-forward merge commit
  for prerequisite PR #125. Its `verify` run `30594747785` completed green.
  The prerequisite implementation review and both CI-repair `READY` records
  are ancestors of this commit.
- **Exact object or commit range:** branch
  `track/capital-gain-distributions-line7a-track3-presentation`, created from
  that exact merge commit. This charter-binding commit is the Builder's
  implementation base. The spent Track-2 and prerequisite branches are not
  implementation surfaces.
- **Role:** one Builder, Economy tier / medium effort. This is presentation and
  production-shaped synthetic integration, not a new contract or computation
  round.
- **Scope and evidence-rung ceiling:** project the accepted line-7a and line-7b
  form fields through the existing presentation model and citation-walk product
  page, add authoritative v8 synthetic presentation goldens and browser-manifest
  regressions, and preserve ADR-0046. Synthetic coordinator and synthetic
  browser evidence are the ceiling; no real workspace or real viewing session.
- **Stop conditions:** stop and report if prerequisite PR #125 is not merged
  with green `verify`; if an accepted ADR, published schema, historical
  content/package, existing golden unrelated to this slice, or Track-1/2
  computation would need mutation; if line 7b cannot be represented honestly
  without a new product
  contract, new published schema, tax-specific projector doctrine, or a generic
  substrate beyond the existing internal presentation model; if the product
  page and frozen harness copy cannot remain source-equivalent where the walk
  itself changes; if a real browser/workspace, personal material, Schedule D,
  Form 8949, Form 1099-B, excluded-box computation, filing, or transmission
  becomes necessary; or if governance interpretation is required.
- **Full reads before acting:** this charter; `docs/roles/builder.md`;
  `docs/phases/engine-breadth/milestones/capital-gain-distributions-line7a.md`;
  ADR-0050 Decisions 5 and 8 plus Production Conditions;
  `docs/adr/0046-presentation-surface-contract.md`;
  `docs/adr/0031-real-data-residency-boundary.md`;
  all Track-2 line-7a/line-7b field, rule, citation, package, release, adoption,
  coordinator-test, review, and recheck artifacts;
  `packages/derivation/presentation_projection.py`;
  `packages/derivation/live.py`;
  `packages/derivation/live_session.py`;
  `packages/presentation/pages/citation-walk.v1.html`;
  `tools/presentation_harness/examples/pages/citation-walk.v1.html`;
  `tools/generate_presentation_l2_golden.py`;
  `tools/generate_frrs_t3_fixtures.py`;
  `packages/derivation/loader.py`;
  `tools/presentation_harness/examples/manifests/citation-walk-production-shaped.v1.json`;
  `tests/derivation/test_language_schemas.py`;
  `tests/test_frrs_t3_resolver_bootstrap.py`;
  `tests/test_frrs_t4_w2_live_integration.py`;
  `tests/test_presentation_l2_integration.py`;
  `tests/test_presentation_live_session.py`;
  `tests/test_presentation_live_viewing_vehicle.py`;
  `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-31-capital-gain-distributions-line7a-track3-charter-stop.md`;
  `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-31-capital-gain-distributions-line7a-line7b-prerequisite.md`;
  `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-31-capital-gain-distributions-line7a-line7b-prerequisite-review.md`;
  `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-31-capital-gain-distributions-line7a-line7b-prerequisite-ci-review.md`;
  `packages/content/tax/2025/form1040.line-7b.form-field.v2.json`;
  `packages/content/tax/2025/package.core-calculations.v8.json`;
  `packages/content/tax/2025/published-packages.v3.json`;
  `packages/sample_data/frrs_t3/adoptions/adopt-core-v8-current.json`;
  `packages/sample_data/frrs_t3/publication_surface/releases/demo.release.2025.v3.json`;
  `tests/test_capital_gain_distributions_line7a_line7b_prerequisite.py`;
  `AGENTS.md#Fixture Rules`; and `AGENTS.md#Data Safety Rules`.

Before editing, echo the resolved prerequisite merge commit and ancestry proof,
the Track-3 scope and ceiling, zero-authority and blanket-redaction constraints,
authoritative golden entrypoint, immutable-history constraint, and every stop
condition.

## Goal

Make the new direct-route fields legible on the existing citation-walk product
surface without adding authority: line 7a presents its exact numeric/blocked/
inapplicable state, line 7b presents its affirmative checked state or honest
non-publication state, and every visible claim remains grounded in the accepted
field/citation/finding graph.

## Deliverables

1. **Authoritative v8 presentation fixtures.** Add a deterministic,
   production-shaped synthetic act log that adopts the prerequisite v8 chain
   through its v3 registry/release and enters only through
   `live_coordinate_run`.
   Commit new slice-specific presentation goldens rather than rewriting the
   established v6 golden. Cover at least eligible published line 7a/checked
   line 7b, missing authority, and Schedule-D-required inapplicability.
2. **Line-7a projection.** Project nonzero and closure-backed-zero line 7a with
   its exact field citation and source/closure lineage. Project blocked and
   guard-inapplicable states atomically with no value key or stale act. A
   malformed, ambiguous, uncited, or nonnumeric published line 7a must fail
   closed before a presentation artifact is written.
3. **Line-7b projection.** Represent the accepted affirmative categorical
   state without numeric coercion or tax-specific IDs in generic projector
   logic. Render the field's declared fixed `"checked"` instruction only from
   its current published authority, with the exact line-7b field citation.
   Missing authority is blocked; a checked conclusion of `"yes"` is
   guard-inapplicable. Neither state may display the rejected categorical value
   or fabricate a checkbox state.
4. **Strict internal model.** Preserve one frozen, strictly validated
   zero-authority source object. If the internal model shape/version must
   advance, keep the established v1 fixture valid or migrate only through an
   explicit compatible internal successor with deterministic validation and
   session tests. No published schema or citizen is created or changed for this
   implementation detail.
5. **Product-page rendering.** Extend the product citation walk with one
   accessible render path per new presentation disposition. The affirmative
   line-7b state must be legible to assistive technology; citations remain
   keyboard reachable with visible focus. Continue using node construction and
   `textContent` only—never dynamic `innerHTML`.
6. **ADR-0046 attack set.** Prove section-level blocking, fail-loud local error
   banners, sibling blast containment, structural citation identity, and
   blanket rejected-value redaction for line 7a/7b. Specifically kill-test a
   smuggled value on blocked/inapplicable fields, a malformed categorical
   publication, a missing/wrong line-7b citation, and a broken line-7a section
   alongside a healthy line-7b sibling.
7. **Frozen harness parity.** Apply walk changes to both the product page and
   the frozen synthetic harness copy, preserving their intentional provenance
   wording difference. Add a new slice-specific manifest/fixture matrix that
   measures published, blocked, inapplicable, citation, accessibility, and
   tamper cases in a synthetic browser. Existing baseline manifests and
   unrelated golden fixtures remain unchanged.
8. **Integrated regression.** Add one focused Track-3 module spanning
   coordinator → presentation artifact → strict validation → page behavior.
   Preserve every existing line/attachment/citation group, numeric diagnostic
   suppression, result-file shape, confinement, resolver refusal, unsafe-string
   rejection, and session teardown guarantee.

## Boundary

No tax computation, contribution/admission, package-validation, family/closure,
line-9, line-16, or correction-lifecycle redesign. No real session, real
browser/workspace, screenshot, owner attestation, matrix lift, coverage-frontier
edit, README claim, Track-4 record, or UI redesign beyond the existing citation
walk. Do not edit accepted ADRs, historical schemas/content/packages, or reuse
real/private material.

## Verification before handoff

Run focused modules while iterating, then once:

```text
python3 -m unittest tests.test_capital_gain_distributions_line7a_t3_presentation
python3 -m unittest tests.test_presentation_l2_integration
python3 -m unittest tests.test_presentation_live_session
python3 -m unittest tests.test_presentation_live_viewing_vehicle
python3 -m unittest tests.test_capital_gain_distributions_line7a_t2_coordinator
node --test tools/presentation_harness/tests/*.test.mjs
node tools/presentation_harness/run.mjs --manifest tools/presentation_harness/examples/manifests/capital-gain-distributions-line7a.v1.json
git diff --check main..HEAD
python3 tools/governance_lint.py
python3 tools/envelope_scan.py --range main..HEAD
```

Run no real-data session and do not rerun the full suite. Inspect every new
golden and browser report; commit only stable fixtures, never ad hoc output.
CI `verify` remains the gate of record.

## Handoff

Commit one Track-3 implementation commit after the charter/base commit. Leave
the worktree clean and report the SHA, exact files, focused results, golden
entrypoint and deterministic-regeneration evidence, product/harness parity,
browser-manifest result, and any stop finding. Do not review, push, open a PR,
begin Track 4, or edit pointers. The foreman will charter an author-independent
Track-3 review.
