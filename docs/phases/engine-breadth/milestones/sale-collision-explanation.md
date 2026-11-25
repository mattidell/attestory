<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "sale-collision-explanation",
  "status": "Closed 2026-11-25. Projection and loader only (core v106+); no core or schema bump.",
  "retrospective": "docs/milestone-retrospectives/2026-11-25-sale-collision-explanation.md",
  "scope": [
    "when the same sale is recorded in two incompatible sale families and triggers IDENTITY_EXCLUSIVITY_COLLISION, the saved page shows a plain filer-facing sentence explaining why the line is blocked and what to check instead of empty reasons",
    "every recorded return keeps its numbers, dispositions, refusal codes, and question groups, and no saved sale record is unpinned"
  ],
  "non_goals": [
    "no edit to any published source-family version or published schema",
    "no change to when IDENTITY_EXCLUSIVITY_COLLISION fires in runner.py (ADR-0066 stands)",
    "no kernel change and no citation-walk.v1.html change unless P0 proves it necessary"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/sale-collision-explanation.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/sale-collision-explanation.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/sale-collision-explanation.md"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-11-25-sale-collision-explanation.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# A Sale Entered in Two Families Says Why It Blocked (2025)

Milestone key: sale-collision-explanation.
Branch: milestone/sale-collision-explanation-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-24.
Starting point: main at `2cdddff3d` (core v106, registry v104, release v104).
Expected target: projection-only explanation for `IDENTITY_EXCLUSIVITY_COLLISION`
(and its paired `identity_exclusivity:<id>` missing token) on `presentation-model.v3`
with no schema, kernel, or core version bump unless P0 shows a content home is needed.

## What we are trying to accomplish

`sale-block-explanations` (ADR 0088, core v106) gave every sale-family
`member_constraints` block a plain explanation and, for wash-sale blocks, a
fixing question. One sale-family validation block remained silent: when the
same sale (matching broker, statement, transaction, and tax year) is entered
in two incompatible sale families, `runner.py:1910-1915` blocks
`<family>.member-validation.synthesized` with both
`IDENTITY_EXCLUSIVITY_COLLISION` and `identity_exclusivity:<excl_id>` in
`missing`. Neither token is recognized by `explain()` in
`presentation_projection.py`, so `reach_mixed` fails closed and every blocked
downstream line shows `reasons: []` (generic line copy only).

The goal is for a cross-family sale collision to explain in plain words that
the same sale was entered in more than one sale category (naming the colliding
categories plainly where the declaration provides them, without leaking
engine ids or `"family"` jargon) and telling the filer to keep the sale in
only one category, without changing any numbers, dispositions, or pinned
schemas.

## Stages

1. **P0 (inventory & design, no committed code).** Inventory every
   `identity_exclusivity` declaration across all `source-family.v2` citizens on
   core v106; observe what `presentation_projection.py` emits today on
   synthetic `demo.*` collision pairs (and mixed collision + `member_constraints`
   or collision + unanswered question cases); check whether any of the 775
   recorded lists hit `IDENTITY_EXCLUSIVITY_COLLISION`; design how `explain()`
   handles both `IDENTITY_EXCLUSIVITY_COLLISION` and
   `identity_exclusivity:<excl_id>` cleanly (including deduplication when both
   colliding families declare mutual exclusivity!) without unpinning any
   schema or family; verify on a scratch copy against synthetic collisions and
   the 775-list corpus.
2. **Decisions** by the foreman (logged in `## Decisions`).
3. **Track 1** builds the projection change and tests (unit, live
   `live_coordinate_run`, multi-family collision, mixed collision + question,
   rendered HTML check, full `pytest`, `mypy`, and 775-list replay).
4. **Fresh independent review**, repair if needed, curation, closeout, final
   review, green CI `verify`, merge.

## P0 result

Completed on `milestone/sale-collision-explanation-2025` (baseline core `v106`, registry `v104`, release `v104`). See [sale-collision-explanation-evidence/p0.md](sale-collision-explanation-evidence/p0.md).

- **Inventory (`v106`):** **6** of `76` `source-family` members in `v106` declare `identity_exclusivity` (all Form 1099-B `source-family.v2` sale families), totaling **18** declarations across **17** distinct `excl.id` strings (`covered-w-st@v2` and `covered-w-lt@v2` share `tax.us.2025.block.covered-w.identity-key-collision`). All 18 are asymmetric (`reverse_count = 0`) and emit `["IDENTITY_EXCLUSIVITY_COLLISION", "identity_exclusivity:<excl_id>"]` in `missing` (`runner.py:1910-1915`). `IDENTITY_COMPONENT_MISSING` (`:1907-1909`) also emits `identity_exclusivity:<excl_id>` without `IDENTITY_EXCLUSIVITY_COLLISION`, so projection must require `IDENTITY_EXCLUSIVITY_COLLISION` in `current["missing"]`.
- **Current `v106` saved-page behavior & corpus (`775` lists):** On synthetic `demo.*` collisions, `explain()` (`presentation_projection.py:826-854`) returns `False` for both collision tokens, so `reach_mixed`/`reach_plain` fail closed (`reasons: []` on all `32`–`33` blocked sections) and suppress adjacent `taxpayer-over-65` questions and ADR 0088's `CODE_W_ON_GAIN` explanation + fixing `.adjustment` `questionGroup`. Across all **775** recorded lists on `v106`, **29 lists** (`3` `v81/case/*`, `18` `v82/p0_e_*`, `8` `v83/returns/case/*`) hit `IDENTITY_EXCLUSIVITY_COLLISION` and exercise all 18 declared pairs. Existing live golden suites (`test_code_b_sales_v81.py`, `test_sale_family_audit_v82.py`, `test_f1099b_backup_withholding_v83.py`) assert `reasons == []` on `v81`–`v83` collision cases, requiring `core-calculations >= v106` gating to preserve historical fixtures.
- **Recommended design (Option b1, no ADR or core/schema bump):** Gate collision explanation on `core-calculations >= v106` via `explains_identity_exclusivity_collision` in `packages/tax/loader.py`, passing `IDENTITY_EXCLUSIVITY_COLLISION_SENTENCE` (generic fallback) and `SALE_COLLISION_CATEGORY_LABELS` (8 plain Form 1099-B category labels) into `_closure_question_reasons` (`presentation_projection.py`). `explain()` resolves `identity_exclusivity:<excl_id>` through `members_by_id` to `incompatible_family.id`, sorts the two labels so symmetric collisions deduplicate in `frames[-1].extras` to 1 bullet, and handles `IDENTITY_EXCLUSIVITY_COLLISION` without leaking `"family"` or engine IDs.
- **Scratch verification (`v106` baseline vs. `v106` scratch):** All `22` `collision_probe.py` cases pass (`18` pairs, `three_way`, `mixed_unanswered`, `mixed_code_w_on_gain`, `control_distinct`), unit edge cases pass (symmetric dedup to `1` bullet, `IDENTITY_COMPONENT_MISSING` stays `[]`, unmapped fallback, `v105` stays `[]`), DOM checks (`check_page_dom.mjs`) report `0` `section_errors` and `0` `total_first_read_leaks`, `246` compatibility tests pass, and full-surface replay across all **775** recorded lists passes **`775 / 775`** (`746` `identical`, `29` `expected_changes`, `0` `failing`, `0` `unexpected_differences`, `31 / 31` expectations used, zero number/disposition/block-code changes).
- **Decisions for the foreman:** (1) Approve Option (b1) pair-specific closed map in `packages/tax/loader.py` + generic fallback vs. Option (a) generic-only vs. Option (b2) `v107` content citizen; (2) approve `core-calculations >= v106` version-gating to keep `v81`–`v105` fixtures untouched.

## Decisions

1. **Select Option (b1): pair-specific closed category map + generic fallback in `packages/tax/loader.py`, injected into domain-neutral `packages/derivation/presentation_projection.py` (foreman decision under owner direction, 2026-11-25).**
   Names both colliding Form 1099-B sale categories plainly across all 18 `v106` pairs without `"family"` or engine-id leaks, keeps `presentation_projection.py` domain-neutral (receives `collision_sentence` and `collision_category_labels` kwargs), deduplicates symmetric pairs by sorting the two labels in `frames[-1].extras`, falls back safely to `IDENTITY_EXCLUSIVITY_COLLISION_SENTENCE` for any unmapped future family, and requires no schema bump, core bump, or new ADR.
2. **Gate on `core-calculations >= v106` (`explains_identity_exclusivity_collision` in `packages/tax/loader.py`) (foreman decision, 2026-11-25).**
   Preserves all historical `v74`–`v105` fixtures (`test_code_b_sales_v81.py`, `test_sale_family_audit_v82.py`, `test_f1099b_backup_withholding_v83.py`, `test_closure_question_coverage.py`) byte-for-byte without mutating frozen goldens while enabling collision explanations on `v106+` without minting `v107`.
3. **Fail-closed guard on `IDENTITY_EXCLUSIVITY_COLLISION` presence (foreman decision, 2026-11-25).**
   `explain()` treats `identity_exclusivity:<excl_id>` as a collision ONLY when `artifact_id.endswith(".member-validation.synthesized")` AND `"IDENTITY_EXCLUSIVITY_COLLISION"` is present in `current["missing"]`, leaving `IDENTITY_COMPONENT_MISSING` and `IDENTITY_EXCLUSIVITY_FAMILY_ABSENT` strictly failing closed.
4. **Track 1 verification contract:** Unit tests (symmetric deduplication, `IDENTITY_COMPONENT_MISSING` non-interference, `IDENTITY_EXCLUSIVITY_FAMILY_ABSENT` non-interference, unmapped fallback, `v105` gate off, `v106` gate on), live integration tests (`live_coordinate_run` loading `collision_probe.py` via `tests/evidence_loader.py` across all 18 pairs + 3-way + mixed `taxpayer-over-65` + mixed `CODE_W_ON_GAIN` + distinct control), `check_page_dom.mjs` rendered HTML verification (`0` `section_errors`, `0` `total_first_read_leaks`), full `pytest`, `mypy`, `governance_lint.py`, `envelope_scan.py`, and 775-list full-surface replay.

## Closeout

Closed 2026-11-25. Added `explains_identity_exclusivity_collision`
(`core-calculations >= v106`), `SALE_COLLISION_CATEGORY_LABELS`, and
`IDENTITY_EXCLUSIVITY_COLLISION_SENTENCE` in `packages/tax/loader.py`, wired
into domain-neutral `_closure_question_reasons` in
`packages/derivation/presentation_projection.py` with fail-closed guards on
`IDENTITY_COMPONENT_MISSING` / `IDENTITY_EXCLUSIVITY_FAMILY_ABSENT` and
sorted-pair deduplication. No schema, core, content, `packages/kernel/`,
`runner.py`, or `citation-walk.v1.html` file changed. Full `pytest` (7,723
passed), `mypy`, rendered DOM checks (`0` section errors, `0` first-read
leaks), and the 775-list full-surface replay (`746` identical, `29` expected
changes, `0` unexpected diffs) passed, and independent review returned `READY`
with no findings.
