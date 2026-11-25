# ADR 0088 — Plain explanations and fixing questions for family member-validation blocks

- Status: **accepted** (owner, 2026-11-24, before Track 1)
- Tier: 2 — a content-citizen, package-admission, and presentation-projection
  contract that later packages and pages are written against.
- Date: 2026-11-24

## Context

Two closed-on-P0 milestones (`sale-reasons-plain` and `code-w-gain-question`)
converged on one gap in how source-family member-validation blocks render on a
saved page:

1. **Pinned engine text in `meaning`.** On core `v105`, 8 of 32
   `source-family.v2` citizens declare `member_constraints` (all 8 are sale
   families: `covered-w-{st,lt}`, `noncovered-{st,lt}`, `no1099b-{st,lt}`, and
   `code-b-{st,lt}`), totaling 30 declarations across 7 `block_code`s
   (`BOX_1G_FLAG_WITHOUT_AMOUNT`, `BOX_1G_AMOUNT_WITHOUT_FLAG`,
   `BASIS_WAS_REPORTED`, `HOLDING_PERIOD_MISMATCH`,
   `CODE_B_WITHOUT_CORRECTION`, `CODE_W_ON_GAIN`, and
   `ADJUSTMENT_EXCEEDS_LOSS`). When a member violates a constraint,
   `runner.py` records `DEPENDENCY_INVALID` with `missing=[<block_code>, ...]`
   on `<family_id>.member-validation.synthesized`, and
   `presentation_projection.py` (`meaning_for`) copies the family's `meaning`
   into `resolved.reasons` on every downstream blocked section. Several
   `meaning` strings expose developer or engine wording
   (`floor_zero(basis - proceeds)`, `ADR-0061 Decision 1`, internal block
   codes, and `"family"`). Editing `meaning` via `source-family` successors
   would unpin saved sale records and break recorded sale workspaces.
2. **No fixing question on wash-sale blocks.** When a filer enters a Form
   1099-B box 1g or Form 8949 column (g) wash-sale adjustment on a gain or
   break-even sale (`CODE_W_ON_GAIN`) or exceeding the sale's loss
   (`ADJUSTMENT_EXCEEDS_LOSS`), `explain(current, key)`
   (`presentation_projection.py:849`) adds the pinned `meaning` and returns
   before `record_input_fact` (`:860`), leaving `questionGroups=[]` and
   `questionRefs=[]`. Six of the eight constrained sale families also lack
   `input-question.v1` citizens for their `*-txn.adjustment` companion fact
   (`code-b-{st,lt}` already declare them in `v105`), which silently suppresses
   closure questions when an `.adjustment` fact itself is `DEPENDENCY_ABSENT`.

## Decision

1. **New content citizen: `family-block-explanation.v1` admitted by
   `artifact-package.v44`.**
   Add immutable schema
   `packages/schemas/derivation/family-block-explanation.v1.schema.json`, role
   `"family-block-explanation"` in `packages/derivation/loader.py`
   (`ROLE_VOCABULARY`), and package admission in
   `packages/schemas/derivation/artifact-package.v44.schema.json` (additive to
   `v43`). Each citizen declares:
   - `family_id` (required string): versionless source-family id matching
     `<family_id>.member-validation.synthesized`.
   - `block_code` (required string): a `block_code` declared in that family's
     `member_constraints`.
   - `explanation` (required non-empty string): IRS-grounded plain sentence
     shown to the filer on blocked lines.
   - `fact_type` (optional `{id, version}` pin): when a fixing input question
     applies (`CODE_W_ON_GAIN` and `ADJUSTMENT_EXCEEDS_LOSS` pin the family's
     `*-txn.adjustment` companion fact type), pins the fact type whose adopted
     `input-question` citizen projection should link.

   Because `family-block-explanation.v1` is a sibling package member pointing
   to `family_id`, no `source-family.v2` file changes and no saved sale record
   is unpinned.

2. **Package validation invariants (`packages/derivation/package_validation.py`).**
   For packages that admit `family-block-explanation` members (opt-in per
   package so earlier cores and minimal test packages stay valid),
   `validate_package` enforces:
   - `ROLE_MISMATCH`: pin role must be `"family-block-explanation"`.
   - `FAMILY_BLOCK_EXPLANATION_FAMILY_ABSENT`: `family_id` must match an
     adopted `source-family.*` member in the package.
   - `FAMILY_BLOCK_EXPLANATION_CODE_ABSENT`: `block_code` must be declared in
     that family's `member_constraints`.
   - `FAMILY_BLOCK_EXPLANATION_DUPLICATE`: at most one citizen per
     `(family_id, block_code)` in a package.
   - `FAMILY_BLOCK_EXPLANATION_FACT_TYPE_NOT_ADMITTED`: if `fact_type` is set,
     `(fact_type.id, fact_type.version)` must be in `fact_surface`.
   - `FAMILY_BLOCK_EXPLANATION_QUESTION_ABSENT`: if `fact_type` is set, an
     `input-question.*` citizen for that `(fact_type.id, fact_type.version)`
     must be adopted in the package.

   `authorization_closure.py` validates `"family-block-explanation"` role
   alignment on closure edges when present.

3. **Projection lookup on `presentation-model.v3` (no presentation schema bump).**
   `build_presentation_model` indexes adopted `family-block-explanation.*`
   citizens by `(family_id, block_code)` and indexes violating member fact ids
   (`member_violation_targets`) from the run's published
   `<family_id>.member-validation.synthesized.<member_fact_id>` derived
   findings whose `violations` list includes `block_code`.

   In `_closure_question_reasons` (`explain(current, key)`):
   - When `current["artifact_id"]` ends with `".member-validation.synthesized"`
     and `(family_id, key)` has an adopted `family-block-explanation`:
     1. Emit `declared["explanation"]` into `frames[-1].extras` (rendered as
        an unlinked bullet under `Why:`).
     2. If `declared` carries `fact_type`, derive transaction-scoped candidate
        fact ids (`f"{fix_ft_id}|{suffix}"` for each violating `member_fact_id`
        in `member_violation_targets[(family_id, key)]` present in
        `question_target_ids[fix_ft_id]`, falling back to `fix_ft_id` only if
        no identity-keyed target exists) and call `record_input_fact`.
   - Existing `questionGroups` / `questionRefs` machinery emits one
     `questionGroup` per violating transaction's `.adjustment` fact (leaving
     valid wash-sale losses in the same family untouched) and appends the
     linked `input-question` reason.
   - Because `citation-walk.v1.html:1452-1458` replaces any linked reason with
     `"See the question and affected lines above"`, emitting two `reasons[]`
     entries (the unlinked plain explanation bullet plus the linked question
     anchor) keeps `presentation-model.v3` and `citation-walk.v1.html`
     unchanged.
   - When no `family-block-explanation` is adopted for `(family_id, key)` (all
     cores `v105` and earlier), `explain` falls through unchanged to
     `meaning_for(current, key)`.

4. **Six missing `*.adjustment` `input-question.v1` citizens.**
   Core successor `v106` adopts the 6 missing `input-question.v1` citizens
   (`f1099b-covered-w-{st,lt}-adjustment`, `f1099b-noncovered-{st,lt}-adjustment`,
   `f8949-no1099b-{st,lt}-adjustment`) alongside the 2 existing
   `code-b-{st,lt}-adjustment` citizens, plus 30 `family-block-explanation.v1`
   citizens. These 6 `input-question.v1` citizens also fire on ordinary
   `DEPENDENCY_ABSENT` when a sale's `.adjustment` row is missing (closing the
   silent drop on `v82/n_w_adjustment_row_missing/honest`).

5. **What does not change.**
   - No `source-family.v2` file, version, or `meaning` text changes; no saved
     sale record is unpinned.
   - `packages/kernel/`, `runner.py` validation logic, block codes, tax
     numbers, and dispositions do not change.
   - `BASIS_NOT_REPORTED_ON_COVERED` (`packages/tax/loader.py`, already
     translated via `COVERED_FLAG_REFUSAL_SENTENCE`) and
     `IDENTITY_EXCLUSIVITY_COLLISION` (`runner.py`, cross-family collision with
     no `member_constraints` entry) stay outside `family-block-explanation.v1`.
   - Earlier cores (`v105` and earlier) and `artifact-package.v43` and earlier
     are unchanged in bytes and behavior.

## Consequences

- Track 1 publishes `family-block-explanation.v1`, `artifact-package.v44`,
  package validation and loader wiring, projection support in
  `packages/derivation/presentation_projection.py`, and core `v106` (registry
  `v104`, release `v104`) with 30 `family-block-explanation.v1` citizens and 6
  `*.adjustment` `input-question.v1` citizens.
- In P0's scratch proof on core `v106`, all 38 synthetic cases plus 2-sale
  disambiguation passed `validate_presentation_model`, valid wash-sale losses
  kept publishing with 0 questions, and full-surface replay across all 775
  recorded lists passed `775 / 775` (`691` expected changes, `84` identical,
  `0` failing, `0` unexpected differences, zero number/disposition/code
  changes).
- A blocked wash-sale line renders two `reasons[]` items on
  `presentation-model.v3` (the plain `Why:` explanation plus the linked
  `"See the question and affected lines above"` anchor).

## Alternatives considered

- **`presentation-model.v4` successor field:** Adds structured explanation and
  fixing-question fields on `resolved.reasons` or `questionGroups`, allowing a
  single reason bullet per block, but bumps the presentation schema across
  every return, requires `citation-walk.v1.html` changes, and still needs a
  content home for IRS wording. Deferred; remains additive later if the UI
  wants structured reason badges.
- **Editing `source-family.v2` `meaning` directly:** Unpins saved sale records
  and breaks recorded sale workspaces (proved in `sale-reasons-plain` P0).
- **Hardcoded Python table in `presentation_projection.py` or `loader.py`:**
  Scatters IRS wording into code outside package manifests and validation.

## Links

- Plan: `docs/phases/engine-breadth/milestones/sale-block-explanations.md`
- Evidence: `docs/phases/engine-breadth/milestones/sale-block-explanations-evidence/p0.md`
- Precedents: `sale-reasons-plain`, `code-w-gain-question`, ADR-0003, ADR-0062,
  ADR-0066, ADR-0086, ADR-0087
