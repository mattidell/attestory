<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "sale-block-explanations",
  "status": "Open 2026-11-24. ADR 0088 accepted; Track 1 next.",
  "retrospective": null,
  "scope": [
    "when a sale family's member-validation check blocks a line (holding-period mismatch, wash-sale floor, code W on a gain or break-even), the saved page shows a plain sentence for the reason and, where the filer can fix it, links the question that fixes it",
    "every recorded return keeps its numbers, and no saved sale record is unpinned"
  ],
  "non_goals": [
    "no edit to the pinned sale family `meaning` text or to any published sale family version",
    "no change to when a sale row blocks (ADR-0062 and the family checks stand)",
    "no kernel change; the projection and a presentation schema successor are in scope only under a new ADR the owner accepts"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/sale-block-explanations.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/sale-block-explanations.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/sale-block-explanations.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/sale-block-explanations.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# A Blocked Sale Says Why in Plain Words and Asks What Fixes It (2025)

Milestone key: sale-block-explanations.
Branch: milestone/sale-block-explanations-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-24.
Starting point: main at `e3cb00f4` (core v105, registry v103, release v103).
Expected target: a proposed ADR for the owner, then a projection change and
a presentation-model schema successor once it is accepted; possibly a core
version if content declarations are needed.

## What we are trying to accomplish

Two closed-on-P0 milestones converge on one decision. sale-reasons-plain
found three sale block reasons that read as engine text (the holding-period
mismatch, the wash-sale `floor_zero(basis - proceeds)` reason with its block
code, and the covered code W "on a gain" reason). They are the `meaning`
text on sale source-family checks; saved sale records pin those families by
version and a run copies the text into a published value, so a content
successor would break every sale workspace. code-w-gain-question found that
a code W adjustment on a gain or break-even row blocks with that reason and
no question; content cannot attach one without blocking valid wash-sale
losses, and the smallest route is a projection link at
`presentation_projection.py:849` from the family block codes to the box 1g
question. Both need the projection to map a sale family block code to
filer-facing text and, where one exists, a question, with a schema home for
that mapping: an ADR the owner must accept.

## Stages

1. **P0 (design, no build).** Inventory every sale family member-validation
   block code on core v105 and the page sentence and question group (if
   any) each shows today on synthetic demo.* sales. Design where a plain
   sentence and a fixing question for a block code are declared (content
   that does not unpin a family: for example a new citizen keyed by family
   id and block code, or a presentation-model successor field) and how the
   projection finds them. Draft plain sentences from the 2025 Form 8949 and
   Schedule D instructions (start from `sale-reasons-plain-evidence/wording.json`)
   and name the question each links, if any. Show on a scratch projection
   that the design changes only explanation text and question links: a
   full-surface replay against v105 with no number, disposition or code
   change. Draft the ADR text (proposed). Stop for the owner.
2. **Owner** accepts, amends or rejects the ADR.
3. **Track 1** builds it under the accepted ADR.
4. **Fresh review**, repair, closeout.

## P0 result

Completed on `milestone/sale-block-explanations-2025` (baseline core `v105`, registry `v103`, release `v103`). See [sale-block-explanations-evidence/p0.md](sale-block-explanations-evidence/p0.md) and [ADR 0088](../../../adr/0088-family-block-explanations.md).

- **Inventory (`v105`):** 8 of 32 `source-family.v2` citizens declare `member_constraints` (all 8 are sale families), totaling **30** declarations across **7 distinct `block_code`s** (`BOX_1G_FLAG_WITHOUT_AMOUNT`, `BOX_1G_AMOUNT_WITHOUT_FLAG`, `BASIS_WAS_REPORTED`, `HOLDING_PERIOD_MISMATCH`, `CODE_B_WITHOUT_CORRECTION`, `CODE_W_ON_GAIN`, `ADJUSTMENT_EXCEEDS_LOSS`). On synthetic `demo.*` sales today, all 30 block 32 downstream sections (`DEPENDENCY_ABSENT`), display pinned `meaning` prose in `resolved.reasons`, and emit `0` `questionGroups` and `0` `questionRefs` (while all 8 valid wash-sale loss controls publish cleanly). Sibling `IDENTITY_EXCLUSIVITY_COLLISION` blocks with `reasons: []`; `BASIS_NOT_REPORTED_ON_COVERED` already translates via `COVERED_FLAG_REFUSAL_SENTENCE`.
- **IRS 2025 wording:** Drafted IRS-grounded plain sentences and fixing `*-txn.adjustment` question links in [sale-block-explanations-evidence/wording.json](sale-block-explanations-evidence/wording.json) from 2025 Instructions for Form 8949 and Schedule D (`CODE_W_ON_GAIN` and `ADJUSTMENT_EXCEEDS_LOSS` link the family's `.adjustment` `input-question.v1`; the 5 structural/family-placement codes show plain sentences without adding a scalar question).
- **Recommended design (Home 1):** Add `family-block-explanation.v1` (keyed by `(family_id, block_code)` with required `explanation` and optional fixing `fact_type` pin), package schema `artifact-package.v44`, package cross-citizen validation in `packages/derivation/package_validation.py`, the 6 missing `*.adjustment` `input-question.v1` citizens, and a projection lookup in `presentation_projection.py` (`_closure_question_reasons`) keeping `presentation-model.v3` unchanged (`citation-walk.v1.html` renders plain `Why:` bullet + linked question anchor) and disambiguating multi-sale families via `<family>.member-validation.synthesized.<member_fact_id>` publications. No `source-family` version is unpinned.
- **Scratch proof & 775-list replay:** In an isolated scratch `v106` copy, `test_schema_registry.py` + `test_package_validation.py` passed (`27 passed`), all 38 synthetic cases plus a 2-sale disambiguation test passed (`validate_presentation_model` clean, 0 failures, valid wash-sale losses unaffected), and `tools/recorded_replay.py full` across all **775** recorded lists passed **`775 / 775`** (`691` `expected_changes`, `84` `identical`, **`0` failing**, **`0` unexpected differences**, zero number/disposition/code/outcome changes).
- **Owner / foreman decisions queued:** (1) Accept [ADR 0088](../../../adr/0088-family-block-explanations.md) (Home 1: `family-block-explanation.v1` + `presentation-model.v3`) vs. `presentation-model.v4`; (2) confirm allowing the 6 new `*.adjustment` `input-question.v1` citizens to fire on `DEPENDENCY_ABSENT` (restores missing-row questions on `v82/n_w_adjustment_row_missing/honest`); (3) confirm leaving `IDENTITY_EXCLUSIVITY_COLLISION` and `BASIS_NOT_REPORTED_ON_COVERED` out of scope.

## Decisions

1. **Accepted architecture — Home 1 (`docs/adr/0088-family-block-explanations.md`, accepted by owner 2026-11-24).**
   Filed and accepted ADR 0088 and its `docs/adr/INDEX.md` row selecting Home 1:
   new content citizen `family-block-explanation.v1` keyed by
   `(family_id, block_code)` with optional fixing `fact_type` pin, admitted in
   `artifact-package.v44`, resolved in `presentation_projection.py`
   (`_closure_question_reasons`) while keeping `presentation-model.v3`,
   `citation-walk.v1.html`, and all `source-family.v2` pins unchanged. Home 2
   (`presentation-model.v4`) is deferred because it would bump the presentation
   schema across unaffected returns and still require a content home for IRS
   wording. Track 1 proceeds under accepted ADR 0088.
2. **Allow the 6 new `*.adjustment` `input-question.v1` citizens to fire on
   `DEPENDENCY_ABSENT` (foreman recommends yes; part of ADR 0088 Decision 4).**
   On `v82/n_w_adjustment_row_missing/honest`, adopting
   `f1099b-covered-w-st-adjustment` turns a previously silent
   `DEPENDENCY_ABSENT` block into actionable questions and restores the
   unanswered `taxpayer-over-65`, `taxpayer-blind`, and
   `f1099b-no-sale-box4-present` questions that `reach_mixed` previously
   dropped.
3. **Two `reasons[]` bullets on `presentation-model.v3` when a block links a
   fixing question (foreman recommends yes; part of ADR 0088 Decision 3).**
   Emitting the unlinked IRS plain explanation plus the linked question anchor
   matches `citation-walk.v1.html:1452-1458` without a schema bump; Track 1
   will include a rendered-HTML DOM/text check confirming both bullets display
   clearly.
4. **Leave `BASIS_NOT_REPORTED_ON_COVERED` and `IDENTITY_EXCLUSIVITY_COLLISION`
   out of `family-block-explanation.v1` scope (foreman decision).**
   `BASIS_NOT_REPORTED_ON_COVERED` already renders
   `COVERED_FLAG_REFUSAL_SENTENCE`; `IDENTITY_EXCLUSIVITY_COLLISION` is a
   cross-family collision with no `member_constraints` declaration and stays
   separate.
5. **Opt-in `validate_package` + current-core coverage regression test (foreman
   decision for Track 1).** Keep `family-block-explanation` opt-in in
   `validate_package` so earlier cores (`v105` and earlier) and minimal test
   packages stay valid, and add a regression test in `tests/` requiring every
   `member_constraints` declaration on the current published core (`v106+`) to
   have an adopted `family-block-explanation.v1` citizen.
