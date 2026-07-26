# Presentation — L2 Integration Grounding Completion Review Charter

Audience: Reviewer

## Context Capsule

- Source ref: `track/presentation-l2-integration-grounding-track1`. Resolve and
  verify it at launch with:
  `python3 tools/build_orientation_block.py --ref track/presentation-l2-integration-grounding-track1`.
- Exact review object: Track 2 records commit `8e29b52`, containing:
  - `docs/phases/real-return/maturity-matrix.md`
  - `docs/phases/real-return/real-return-roadmap.md`
  - `docs/phase-state.md`
  - `docs/phases/real-return/milestones/presentation-l2-integration-grounding.md`
  - `docs/milestone-retrospectives/2026-07-26-presentation-l2-integration-grounding.md`
- Exclude the subsequent Foreman custody commit that adds this charter and
  makes Reviewer current.
- Role: a fresh independent Reviewer who did not perform Track 1 review or
  recheck.
- Scope and evidence-rung ceiling: records and evidence linkage only;
  Presentation remains L2. No implementation review, real exercise, or next
  milestone selection.
- Stop conditions: stop if review requires implementation edits, governance
  interpretation, real data, a real workspace, live browser, a maturity lift,
  or selecting the next milestone.
- Full reads before acting:
  - `docs/roles/reviewer.md`
  - `docs/adr/INDEX.md`
  - the five Track 2 record files listed above
  - `docs/adr/0046-presentation-surface-contract.md`
  - `docs/reviews/2026-07-26-presentation-l2-integration-grounding-track1-review.md`
  - `docs/reviews/2026-07-26-presentation-l2-integration-grounding-track1-recheck.md`
  - `packages/derivation/live.py`
  - `packages/derivation/presentation_projection.py`
  - `tests/test_presentation_l2_integration.py`
  - `tools/presentation_harness/examples/manifests/citation-walk.v1.json`
  - `tools/presentation_harness/examples/manifests/citation-walk-production-shaped.v1.json`
  - `AGENTS.md#Data Safety Rules`

Before reviewing, echo the exact records commit, scope, evidence ceiling, and
stop conditions. Do not seek prior agent threads or accept their summaries as
evidence.

## Objective

Determine whether Track 2 leaves an exact, evidence-linked L2 Presentation
handoff and satisfies the milestone's records exit criteria without implying
that live operation is already executable.

## Required measurements

1. Confirm `8e29b52` changes exactly the five listed records and contains no
   implementation, schema, citizen, fixture, manifest, or ADR change.
2. Check each of maturity-matrix footnote 5's six capability rows against the
   cited committed evidence:
   surface contract, renderer behavior, coordinator projection, renderer input,
   browser path, and real operation.
3. Confirm the matrix remains L2 across all five Presentation cells and that no
   wording claims L3, owner attestation, live invocation, real operation, or a
   caller-facing presentation contract.
4. Confirm the handoff distinguishes the verified production-shaped synthetic
   coordinator path from the absent live browser invocation vehicle. It must
   not repeat the prior unsupported conclusion that only an immediately
   executable real exercise remains.
5. Confirm phase state, roadmap, plan, and matrix agree: Track 1 is `READY`,
   Track 2 records are in review, no milestone PR is open, Presentation remains
   L2, and the next milestone is unselected.
6. Confirm `initial_briefing_follow_up` is absent and the retrospective contains
   lessons, deviations, cost, and triggered follow-ups rather than restating
   the implementation or test record.
7. Confirm the plan's completion sequence is coherent with owner direction:
   completion review precedes the milestone PR, and CI gates that final PR
   rather than serving as impossible pre-review evidence.
8. Run:

   ```text
   python3 tools/envelope_scan.py --range main..HEAD
   python3 tools/governance_lint.py
   git diff --check main..HEAD
   ```

## Verdict and handoff

Return `READY` only if all eight measurements pass. Otherwise return `NOT READY`
with the smallest exact records residual; do not edit the records.

Write the complete review to
`docs/reviews/2026-07-26-presentation-l2-integration-grounding-completion-review.md`
and commit only that record on
`track/presentation-l2-integration-grounding-track1`, on top of the Foreman
custody commit containing this charter. Do not edit implementation, phase
state, the plan, matrix, roadmap, retrospective, or this charter. Return the
review commit hash and verdict.
