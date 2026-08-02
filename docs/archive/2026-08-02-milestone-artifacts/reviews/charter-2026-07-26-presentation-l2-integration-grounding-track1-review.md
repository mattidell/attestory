# Presentation — L2 Integration Grounding Track 1 Review Charter

Audience: Reviewer

## Context Capsule

- Source ref: `track/presentation-l2-integration-grounding-track1`. Resolve and
  verify it at launch with:
  `python3 tools/build_orientation_block.py --ref track/presentation-l2-integration-grounding-track1`.
- Exact review object: implementation commit `81c5504`, based on `main`.
  Review these seven implementation files:
  - `packages/derivation/live.py`
  - `packages/derivation/presentation_projection.py`
  - `tests/test_frrs_t4_w2_live_integration.py`
  - `tests/test_presentation_l2_integration.py`
  - `tools/generate_presentation_l2_golden.py`
  - `tools/presentation_harness/examples/manifests/citation-walk-production-shaped.v1.json`
  - `tools/presentation_harness/examples/pages/citation-walk-fixtures/production-shaped.v1.json`
- Exclude the subsequent Foreman custody commit that adds this charter and
  advances plan/phase pointers; report it as administrative if needed, but do
  not review it as implementation.
- Role: Reviewer.
- Scope and evidence-rung ceiling: production-shaped synthetic integration
  evidence only. Presentation remains L2; no real exercise or live-browser
  claim.
- Stop conditions: stop if review would require a published schema or citizen,
  new tax content, governance interpretation, a real workspace, live browser,
  or an implementation edit. Return findings; do not repair.
- Full reads before acting:
  - `docs/roles/reviewer.md`
  - `docs/adr/INDEX.md`
  - `docs/archive/2026-08-02-milestone-artifacts/phases/real-return/milestones/presentation-l2-integration-grounding.md`
  - `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-26-presentation-l2-integration-grounding-track1.md`
  - `docs/adr/0031-real-data-residency-boundary.md`
  - `docs/adr/0046-presentation-surface-contract.md`
  - the seven review-object files listed above
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

Before reviewing, echo the exact review object, evidence ceiling, and stop
conditions. Do not seek the Builder's thread or treat its self-report as
evidence.

## Objective

Independently determine whether commit `81c5504` satisfies the amended Track 1
charter and the plan's implementation review gate without widening scope.

## Required measurements

1. Confirm the review object is exactly the seven implementation files above.
   Prove the original demo manifest, its fixtures, renderer, and harness
   boundary are byte-unchanged from `main`.
2. Independently run:

   ```text
   python3 -m unittest tests.test_presentation_l2_integration
   node tools/presentation_harness/run.mjs \
     --manifest tools/presentation_harness/examples/manifests/citation-walk.v1.json
   node tools/presentation_harness/run.mjs \
     --manifest tools/presentation_harness/examples/manifests/citation-walk-production-shaped.v1.json
   python3 -m unittest tests.test_frrs_t4_w2_live_integration
   python3 -m unittest tests.test_dsbs_t4_dividend_live_integration
   ```

3. Regenerate the production-shaped golden and prove byte-for-byte
   determinism. Directly grep and inspect to prove the generation path enters
   through `live_coordinate_run`, with no direct `runner.run`, fixture-derived
   `RunContext`, or caller-authored presentation payload.
4. Confirm the projector derives every field and attachment solely from the
   resolved graph, projected record state, `RunResult.publications`, and
   `RunResult.dispositions`. Confirm every join is exact and that no demo line
   2a, guard-inapplicable line 9, identifier, citation, value, or label was
   invented.
5. Probe strict validation and fail-closed behavior for unknown keys and
   dispositions, invalid numeric publications, missing or ambiguous joins,
   untraceable citation lineage, rejected-value echo, markup/closing-script
   serialization, resolver refusal, and workspace escape.
6. Confirm citation lineage and evidence labels are traceable to declared
   inputs, and that rejected values are redacted rather than echoed.
7. Confirm the presentation artifact is confined below `LiveWorkspace`, the
   existing result JSON shape and callers remain compatible, resolver refusal
   leaves no artifact, and path traversal is refused.
8. Run both manifests and inspect the touched boundary to confirm the unchanged
   demo suite remains the full five-disposition/T1–T3/F1–F2 regression floor,
   the new suite is production-shaped, and directly touched accessibility,
   blast-containment, and inert-serialization invariants remain intact.
9. Run:

   ```text
   python3 tools/envelope_scan.py --range main..HEAD
   git diff --check main..HEAD
   ```

## Verdict

Return `READY` only if every required measurement passes. Otherwise return
`NOT READY` with the smallest exact residual findings, file and line evidence,
and the focused commands that reproduce them. Do not edit implementation,
phase state, the plan, or this charter. CI is not a prerequisite for this
review: the milestone PR and its `verify` check occur only after all milestone
tracks and their reviews are complete.
