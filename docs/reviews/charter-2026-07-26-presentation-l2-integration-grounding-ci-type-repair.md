# Presentation — L2 Integration Grounding CI Type Repair Charter

Audience: Builder

## Context Capsule

- Source ref: `track/presentation-l2-integration-grounding-track1`. Resolve and
  verify it at launch with:
  `python3 tools/build_orientation_block.py --ref track/presentation-l2-integration-grounding-track1`.
- Exact object: repair the three `mypy` `no-any-return` failures from closing
  PR #86, run `30225516518`, job `89854947620`:
  - `packages/derivation/presentation_projection.py:166`
  - `tools/generate_presentation_l2_golden.py:48`
  - `tools/generate_presentation_l2_golden.py:230`
- Role: Builder.
- Scope and evidence-rung ceiling: type-correctness repair only. This is the
  owner-approved CI-only exception; it adds no product evidence.
- Stop conditions: stop if repair requires runtime behavior, test, fixture,
  golden, manifest, schema, citizen, contract, record, dependency, or mypy
  configuration changes; a broad `Any` escape or suppression; governance
  interpretation; real data; or a real workspace.
- Full reads before acting:
  - `docs/roles/builder.md`
  - `docs/adr/INDEX.md`
  - `docs/phases/real-return/milestones/presentation-l2-integration-grounding.md`
  - `packages/derivation/presentation_projection.py`
  - `tools/generate_presentation_l2_golden.py`
  - `tests/test_presentation_l2_integration.py`
  - `docs/reviews/2026-07-26-presentation-l2-integration-grounding-track1-recheck.md`
  - `AGENTS.md#Data Safety Rules`

Before acting, echo the three failures, scope, and stop conditions.

## Objective

Make the two failing files satisfy the existing mypy configuration without
changing runtime behavior or weakening type checking.

## Deliverables

1. Replace each untyped return with the smallest structurally typed narrowing
   or local annotation that proves the declared return type.
2. Do not add `# type: ignore`, `cast(Any, ...)`, loosened return types, mypy
   configuration changes, or unrelated cleanup.
3. Preserve byte-for-byte golden regeneration and all reviewed coordinator,
   projector, renderer, and harness behavior.

## Required verification

Run once:

```text
python3 -m mypy packages/derivation/presentation_projection.py \
  tools/generate_presentation_l2_golden.py
python3 -m unittest tests.test_presentation_l2_integration
python3 tools/generate_presentation_l2_golden.py
git diff --exit-code -- \
  tools/presentation_harness/examples/pages/citation-walk-fixtures/production-shaped.v1.json
python3 tools/envelope_scan.py --range main..HEAD
git diff --check main..HEAD
```

Do not rerun a deterministic passing command merely to confirm it. The updated
PR's `verify` workflow remains the repository-wide gate.

## Handoff

Commit only the two type-correctness fixes on
`track/presentation-l2-integration-grounding-track1`, on top of the Foreman
custody commit containing this charter. Report the commit hash, exact changed
lines, exact verification results, and confirmation that runtime behavior,
goldens, tests, configuration, and contracts are unchanged. Do not edit the
plan, phase state, reviews, or retrospective.
