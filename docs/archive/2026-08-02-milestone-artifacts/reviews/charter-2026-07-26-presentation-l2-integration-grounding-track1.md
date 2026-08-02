# Presentation — L2 Integration Grounding Track 1 Charter

Audience: Builder

## Context Capsule

- Source ref and resolved launch commit: `main`; resolve and verify at launch
  with `python3 tools/build_orientation_block.py --ref main`.
- Exact object or commit range: Track 1 implementation on
  `track/presentation-l2-integration-grounding-track1`, based on the merged
  plan.
- Role: Builder.
- Scope and evidence-rung ceiling: production-shaped synthetic integration
  evidence only. Presentation remains L2; no real exercise or live-browser
  claim.
- Stop conditions: stop if the track needs a published schema or citizen, a
  caller-facing presentation authority, a live browser/profile design, a
  change to ADR-0031 or ADR-0046, governance interpretation, a real workspace,
  or output that cannot be structurally confined below `LiveWorkspace`.
- Full reads before acting:
  - `docs/roles/builder.md`
  - `docs/adr/INDEX.md`
  - `docs/archive/2026-08-02-milestone-artifacts/phases/real-return/milestones/presentation-l2-integration-grounding.md`
  - `docs/adr/0031-real-data-residency-boundary.md`
  - `docs/adr/0046-presentation-surface-contract.md`
  - `packages/derivation/live.py`
  - `packages/derivation/live_workspace.py`
  - `packages/derivation/runner.py`
  - `tools/presentation_harness/lib/manifest.mjs`
  - `tools/presentation_harness/lib/server.mjs`
  - `tools/presentation_harness/examples/manifests/citation-walk.v1.json`
  - `tools/presentation_harness/examples/pages/citation-walk.v1.html`
  - `tools/presentation_harness/examples/pages/citation-walk-fixtures/baseline.v1.json`
  - `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-26-presentation-citation-walk-track1-review.md`
  - `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-26-presentation-citation-walk-track1-repair-review.md`
  - `AGENTS.md#Data Safety Rules`
  - `AGENTS.md#Fixture Rules`

## Objective

Make the existing citation walk production-shaped end-to-end on synthetic data:
construct and validate its model inside `live_coordinate_run`, confine the
artifact below `LiveWorkspace`, and prove a regenerated synthetic golden through
a dedicated manifest on the unchanged browser harness.

## Deliverables

1. Add the smallest internal projector from the resolved graph, projected
   record state, `RunResult.publications`, and `RunResult.dispositions`.
2. Give its model an explicit internal version and strict validator. Do not
   create a published schema, citizen, or caller-facing contract.
3. On a successful coordinator run, write the validated model as a separate
   artifact below `LiveWorkspace`. Preserve the existing result JSON and all
   existing callers; expose at most the confined artifact path.
4. Regenerate one committed, obviously synthetic golden byte-for-byte from a
   canonical production-shaped `live_coordinate_run`. Add
   `citation-walk-production-shaped.v1.json` to route that golden through the
   browser harness as `synthetic: true`.
5. The production-shaped golden covers every Form 1040 field and attachment in
   its resolved package and only the dispositions the canonical run actually
   produces. Do not invent the demo fixture's line 2a, guard-inapplicable line
   9, identifiers, citations, values, or labels.
6. Preserve `citation-walk.v1.json` and its existing fixtures unchanged as the
   full five-disposition/T1–T3/F1–F2 renderer regression floor. Both manifests
   must pass.
7. Fail closed on missing/ambiguous joins, missing citations, unknown
   dispositions, invalid numeric publications, resolver refusal, path escape,
   and markup/closing-script serialization attacks.
8. Add `tests.test_presentation_l2_integration` covering deterministic
   regeneration, strict validation, coordinator-only construction, result
   compatibility, confinement, and all named attacks.

## Non-goals

- No real data, owner attestation, live browser, browser profile/cache, local
  viewer, remote URL, L3 claim, or maturity edit.
- No harness relaxation, non-synthetic fixture mode, or change to the existing
  citation-walk manifest/demo fixtures.
- No schema, citizen, tax content, rule, field, citation, attachment, domain,
  ADR, UI redesign, or presentation-economy change.
- No direct `runner.run`, fixture-derived `RunContext`, caller-authored
  presentation payload, or in-memory live payload returned to a caller.

## Required verification

Run while iterating:

```text
python3 -m unittest tests.test_presentation_l2_integration
node tools/presentation_harness/run.mjs \
  --manifest tools/presentation_harness/examples/manifests/citation-walk.v1.json
node tools/presentation_harness/run.mjs \
  --manifest tools/presentation_harness/examples/manifests/citation-walk-production-shaped.v1.json
python3 -m unittest tests.test_frrs_t4_w2_live_integration
python3 -m unittest tests.test_dsbs_t4_dividend_live_integration
python3 tools/envelope_scan.py --range main..HEAD
git diff --check
```

Do not rerun a deterministic passing command merely to confirm it. CI `verify`
is the gate of record.

## Handoff

Commit one atomic Track 1 implementation. Report changed files, exact
verification results, compatibility effects, and absence of personal or locator
material. Do not author the review, capability-state table, retrospective, or a
next milestone.
