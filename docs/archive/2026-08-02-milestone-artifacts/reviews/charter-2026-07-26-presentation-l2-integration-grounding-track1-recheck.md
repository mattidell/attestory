# Presentation — L2 Integration Grounding Track 1 Focused Recheck Charter

Audience: Reviewer

## Context Capsule

- Source ref: `track/presentation-l2-integration-grounding-track1`. Resolve and
  verify it at launch with:
  `python3 tools/build_orientation_block.py --ref track/presentation-l2-integration-grounding-track1`.
- Exact review object: repair commit `759c9fa`, limited to
  `packages/derivation/live.py` and
  `tests/test_presentation_l2_integration.py`.
- Finding under recheck: Finding 1 in
  `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-26-presentation-l2-integration-grounding-track1-review.md`
  (`e36086a`), as dispositioned by
  `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-26-presentation-l2-integration-grounding-track1-repair.md`.
- Role: the same independent Reviewer, performing the plan's one focused
  recheck.
- Scope and evidence-rung ceiling: production-shaped synthetic integration
  evidence only. Presentation remains L2.
- Stop conditions: stop if recheck would require implementation edits, a new
  finding outside the repaired failure path or directly touched invariants,
  governance interpretation, real data, a real workspace, or live browser.
- Full reads before acting:
  - `docs/roles/reviewer.md`
  - `docs/adr/INDEX.md`
  - `docs/archive/2026-08-02-milestone-artifacts/phases/real-return/milestones/presentation-l2-integration-grounding.md`
  - `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-26-presentation-l2-integration-grounding-track1-review.md`
  - `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-26-presentation-l2-integration-grounding-track1-repair.md`
  - `packages/derivation/live.py`
  - `packages/derivation/presentation_projection.py`
  - `tests/test_presentation_l2_integration.py`
  - `docs/adr/0031-real-data-residency-boundary.md`
  - `docs/adr/0046-presentation-surface-contract.md`
  - `AGENTS.md#Data Safety Rules`
  - `AGENTS.md#Fixture Rules`

Before reviewing, echo the exact repair object, finding, accepted disposition,
evidence ceiling, and stop conditions. Do not seek the Builder's thread or
accept its self-report as evidence.

## Objective

Determine whether `759c9fa` closes Finding 1 exactly as dispositioned while
preserving the directly touched successful-run and refusal invariants.

## Required measurements

1. Confirm `759c9fa` changes only `packages/derivation/live.py` and
   `tests/test_presentation_l2_integration.py`, with no unrelated repair.
2. Inspect and independently run the new coordinator-level regression. Confirm
   it reaches `PresentationModelError` through `live_coordinate_run`, preserves
   the exception, and proves neither the reserved result artifact nor reserved
   presentation artifact remains.
3. Inspect the coordinator control flow. Confirm the presentation model is
   constructed and validated before either output is durably written and that
   both reservations are removed on `PresentationModelError`; confirm no new
   `Refusal`, `LiveCoordinatorOutcome`, or derivation-record semantics were
   introduced.
4. Independently run:

   ```text
   python3 -m unittest tests.test_presentation_l2_integration
   python3 -m unittest tests.test_frrs_t4_w2_live_integration
   python3 -m unittest tests.test_dsbs_t4_dividend_live_integration
   node tools/presentation_harness/run.mjs \
     --manifest tools/presentation_harness/examples/manifests/citation-walk.v1.json
   node tools/presentation_harness/run.mjs \
     --manifest tools/presentation_harness/examples/manifests/citation-walk-production-shaped.v1.json
   ```

5. Confirm the directly touched successful coordinator path still writes both
   artifacts, resolver refusal still writes neither, result JSON compatibility
   and path confinement remain intact, and both renderer manifests remain
   unchanged and green.
6. Run:

   ```text
   python3 tools/envelope_scan.py --range main..HEAD
   git diff --check main..HEAD
   ```

## Verdict and handoff

Return `READY` only if the accepted finding and every directly touched invariant
pass. Otherwise return `NOT READY` with the smallest exact residual; do not
broaden the recheck.

Write the complete recheck to
`docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-26-presentation-l2-integration-grounding-track1-recheck.md`
and commit only that record on
`track/presentation-l2-integration-grounding-track1`, on top of the Foreman
custody commit containing this charter. Do not edit implementation, phase
state, the milestone plan, or either charter. Return the review commit hash and
verdict.
