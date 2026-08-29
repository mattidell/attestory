# Charter: Ordinary Input Mapping (Seam 6)

Date: 2026-08-28. Foreman-issued.

Route: `PROJECT_PLANNING.md` **Frontier Reduction and Direct-Build
Routing** — "an accepted contract already fixes the proposition, producer,
consumer, and correction behavior; the change is additive and reversible" ->
build directly. **Correction (post eligibility-review R1, 2026-08-28): this
was a first build, not a repair of a pre-existing mapper** — the named
target files did not exist on this branch (see `examination.md`, "Starting
condition"). The routing conclusion (direct-build, no rival) still holds on
the merits; only the "repair" framing was wrong. No rival builder.

- **Branch:** `prototypes/ordinary-input-mapping/it1` (may graduate straight
  to a production branch once reviewed, per Gate 7 in the sibling seam
  plans — this seam has no separate prototype/production boundary because it
  is direct-build).
- **Builder seat:** `roles/builder.md`, Medium tier (medium effort).

## Question

Build the ordinary-language input mapper
(`packages/tax/obligation_acquisition_mapping.py` and its test,
`tests/test_obligation_acquisition_translation.py` — this charter was
originally written expecting these files to already exist and need repair;
they did not exist on this branch, so this is a first build, not a repair —
see the correction note above. Read the current committed versions, not the
uncommitted working-tree edits on `milestone/document-ordinary-fact-translation`
in the sibling worktree, which belong to the NOT-READY attempt) so that:

- its subject and scope agree;
- it accepts ordinary-language structured answers;
- contribution admission validates its output;
- it emits only canonical circumstance facts;
- no tax classification is requested from the user.

## Deliverables

- The mapper and its tests, on the charter branch.
- `examination.md` (≤ 150 lines): what was wrong before (subject/scope
  mismatch, missing validation, or over-broad emission — whichever applies),
  what changed, and a walk-through showing the mapper now emits only
  canonical circumstance facts (name the fact fields) with no embedded tax
  classification.

## Committee

Full three-seat committee (clean-room, adversarial, eligibility) reviews the
repair. The eligibility reviewer confirms this seam was correctly routed as
direct-build (no prototype-eligible proposition was hiding in it) rather than
needing its own Gate 1 score.

## Constraints

- Do not read or depend on the sibling worktree's uncommitted changes to
  `packages/derivation/package_validation.py`,
  `packages/derivation/source_authority.py`,
  `packages/tax/obligation_acquisition_mapping.py`, or
  `tests/test_obligation_acquisition_translation.py` on
  `milestone/document-ordinary-fact-translation` — that branch's repair was
  returned NOT READY and is reference evidence only, read (if useful) but
  never merged or assumed correct.
- No tax-classification input from the user; canonical circumstance facts
  only.
- All fixture data synthetic.
