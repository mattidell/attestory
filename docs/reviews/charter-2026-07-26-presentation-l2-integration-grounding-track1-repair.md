# Presentation — L2 Integration Grounding Track 1 Repair Charter

Audience: Builder

## Context Capsule

- Source ref: `track/presentation-l2-integration-grounding-track1`. Resolve and
  verify it at launch with:
  `python3 tools/build_orientation_block.py --ref track/presentation-l2-integration-grounding-track1`.
- Exact object: repair only Finding 1 in
  `docs/reviews/2026-07-26-presentation-l2-integration-grounding-track1-review.md`
  (`e36086a`). The accepted residual is the untested coordinator-level
  projector-failure path and its stranded result/presentation artifacts.
- Role: Builder.
- Scope and evidence-rung ceiling: production-shaped synthetic integration
  evidence only. This is the plan's one findings-only repair.
- Stop conditions: stop if repair requires a published schema or citizen, new
  tax content, governance interpretation, a real workspace, live browser,
  caller-facing contract expansion, a new refusal taxonomy, or changes outside
  `packages/derivation/live.py` and focused tests.
- Full reads before acting:
  - `docs/roles/builder.md`
  - `docs/adr/INDEX.md`
  - `docs/phases/real-return/milestones/presentation-l2-integration-grounding.md`
  - `docs/reviews/charter-2026-07-26-presentation-l2-integration-grounding-track1.md`
  - `docs/reviews/2026-07-26-presentation-l2-integration-grounding-track1-review.md`
  - `docs/adr/0031-real-data-residency-boundary.md`
  - `docs/adr/0046-presentation-surface-contract.md`
  - `packages/derivation/live.py`
  - `packages/derivation/live_workspace.py`
  - `packages/derivation/presentation_projection.py`
  - `tests/test_presentation_l2_integration.py`
  - `AGENTS.md#Data Safety Rules`
  - `AGENTS.md#Fixture Rules`

Before acting, echo the exact finding, accepted disposition, scope, and stop
conditions.

## Foreman disposition

Accept Finding 1 as one blocking residual, narrowed to the boundary the Track 1
charter owns:

- a `PresentationModelError` reached through `live_coordinate_run` must fail
  closed without leaving either the reserved result artifact or the reserved
  presentation artifact; and
- that behavior must be exercised through `live_coordinate_run`, not only by a
  direct projector unit call.

Do not convert an internal projector error into the production resolver's
`Refusal` type or extend `LiveCoordinatorOutcome`. The original charter
preserves caller contracts and only specifies a structured refusal for resolver
failure. Preserving the existing projector exception while cleaning its
reserved artifacts is in scope. The derivation record stream may accurately
retain the derivation run it recorded; changing record semantics is not part of
this repair.

## Deliverables

1. Make the smallest change in `packages/derivation/live.py` that guarantees a
   projector rejection cannot leave a result artifact or an empty/partial
   presentation artifact.
2. Add a focused regression in `tests/test_presentation_l2_integration.py` that
   reaches a `PresentationModelError` through `live_coordinate_run`, confirms
   the error remains fail-closed, and proves neither reserved artifact remains.
3. Preserve successful-run output, resolver refusal, path confinement, result
   JSON compatibility, both manifests, and all original Track 1 authority and
   serialization boundaries.

## Non-goals

- No new refusal kind, outcome field, public exception contract, schema,
  citizen, package content, renderer, manifest, golden, ADR, maturity claim, or
  records change.
- No repair of passing review measurements and no opportunistic refactor.
- No real data, real workspace, live browser, or L3 evidence.

## Required verification

Run:

```text
python3 -m unittest tests.test_presentation_l2_integration
python3 -m unittest tests.test_frrs_t4_w2_live_integration
python3 -m unittest tests.test_dsbs_t4_dividend_live_integration
node tools/presentation_harness/run.mjs \
  --manifest tools/presentation_harness/examples/manifests/citation-walk.v1.json
node tools/presentation_harness/run.mjs \
  --manifest tools/presentation_harness/examples/manifests/citation-walk-production-shaped.v1.json
python3 tools/envelope_scan.py --range main..HEAD
git diff --check main..HEAD
```

Do not rerun a deterministic passing command merely to confirm it.

## Handoff

Commit only the focused repair and its regression on
`track/presentation-l2-integration-grounding-track1`, on top of the Foreman
custody commit containing this charter. Report the commit hash, changed files,
exact verification results, compatibility effects, and absence of personal or
locator material. Do not update phase state, the milestone plan, review
records, or Track 2 records.
