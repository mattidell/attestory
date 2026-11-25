# Retrospective: A Sale Entered in Two Families Says Why It Blocked

Milestone key: sale-collision-explanation. Plan:
`docs/phases/engine-breadth/milestones/sale-collision-explanation.md`.
Closed 2026-11-25. Projection and loader only (`core-calculations >= v106`);
no core, schema, or page change.

## What happened

`sale-block-explanations` (ADR 0088, core v106) gave every sale-family
`member_constraints` block a plain explanation, leaving cross-family
`IDENTITY_EXCLUSIVITY_COLLISION` blocks silent (`reasons: []`). P0 inventoried
all 18 `identity_exclusivity` rules across 6 Form 1099-B `source-family.v2`
families on core v106, found 29 collision lists in the 775-list corpus (covering
all 18 pairs), and found three frozen `v81`–`v83` golden suites asserting
`reasons == []` on historical collisions.

Track 1 added `explains_identity_exclusivity_collision` (`core-calculations >=
v106`), `SALE_COLLISION_CATEGORY_LABELS`, and
`IDENTITY_EXCLUSIVITY_COLLISION_SENTENCE` in `packages/tax/loader.py`, wired
them into domain-neutral `_closure_question_reasons` (`explain_exclusivity` /
`exclusivity_pair_sentence`) in `packages/derivation/presentation_projection.py`
with a fail-closed guard requiring `IDENTITY_EXCLUSIVITY_COLLISION` in
`current["missing"]` and sorted-pair deduplication, and added unit, live, and
rendered-DOM tests. Full `pytest` (7,723 passed), `mypy`, and the 775-list
replay (`746` identical, `29` expected changes, `0` unexpected diffs) passed;
independent review returned `READY` with no findings.

## What worked

- Checking frozen pre-`v106` golden fixtures during P0 immediately justified
  `core-calculations >= v106` gating, avoiding both fixture churn and an
  unnecessary core `v107` bump.
- Inspecting sibling exclusivity codes (`IDENTITY_COMPONENT_MISSING` and
  `IDENTITY_EXCLUSIVITY_FAMILY_ABSENT`) upfront prevented `identity_exclusivity:*`
  tokens from being mislabeled as collisions.

## What to change

- Keep `SALE_COLLISION_CATEGORY_LABELS` in sync whenever a new sale family
  declares `identity_exclusivity` (unit test `test_sale_collision_explanation_unit.py`
  now enforces coverage across every declared `v106` pair, and unmapped families
  fall back safely to `IDENTITY_EXCLUSIVITY_COLLISION_SENTENCE`).
