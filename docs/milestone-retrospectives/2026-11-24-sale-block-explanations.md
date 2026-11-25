# Retrospective: A Blocked Sale Says Why in Plain Words and Asks What Fixes It

Milestone key: sale-block-explanations. Plan:
`docs/phases/engine-breadth/milestones/sale-block-explanations.md`.
Closed 2026-11-24. Core v106, registry v104, release v104; ADR 0088 accepted.

## What happened

Two earlier P0 milestones (`sale-reasons-plain` and `code-w-gain-question`)
found that sale member-validation blocks showed pinned developer text from
`source-family.v2` `meaning` fields and linked no fixing question for wash-sale
blocks. P0 inventoried all 30 `member_constraints` across 8 sale families (7
block codes) on core v105, drafted IRS 2025 plain wording, compared a new
sibling content citizen (`family-block-explanation.v1`) against a
`presentation-model.v4` schema bump, and proved `family-block-explanation.v1`
on a scratch v106 across 38 synthetic cases, 2-sale disambiguation, and all 775
recorded lists with zero unexpected differences.

The owner accepted ADR 0088. Track 1 published `family-block-explanation.v1`
and `artifact-package.v44`, wired derivation validation, authorization closure,
and projection lookup on `presentation-model.v3` without unpinning any
`source-family` record or editing `citation-walk.v1.html`, and published core
v106 (registry v104, release v104) with 30 explanations and 6 missing
`*.adjustment` input questions. Track 1 passed full `pytest` (7,713 passed),
`mypy`, and the 775-list replay; fresh independent review returned `READY` with
no findings.

## What worked

- Running the 775-list full-surface replay in P0 surfaced the
  `DEPENDENCY_ABSENT` interaction on `v82/n_w_adjustment_row_missing/honest`
  before ADR drafting, so restoring those missing-row questions became an
  explicit ADR 0088 decision rather than a Track 1 surprise.
- Reusing the P0 builder lineage (Hydrogen High) for Track 1 carried full
  context from the scratch proof and produced a clean zero-finding independent
  review (Argon High).

## What to change

- Keep `packages/derivation/package_validation.py`'s per-version
  `artifact-package.v*` allowlists (`_reader_role_issues` and exact
  entrypoint-pin validation) checked whenever a new `artifact-package` schema
  is added; the parked capability-table consolidation remains the cleaner fix.
