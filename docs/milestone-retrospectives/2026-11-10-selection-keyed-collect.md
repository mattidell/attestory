# Retrospective: A Selection Path Collects a Keyed Family Directly (2025)

Milestone key: selection-keyed-collect. Plan:
`docs/phases/engine-breadth/milestones/selection-keyed-collect.md`.
Closed 2026-11-10. ADR 0085 proposed.

## What happened

The owner took the derivation gap parked by f1099b-backup-withholding as
its own milestone. Core v83 needed a rule publishing 0 under the box 4
amount id, because a selection path had to name its collect as a symbol
and marshal never binds keyed members into one, and an inert second path
because `rule-artifact.v15` required two.

P0 surveyed every core: that stand-in is the only one, and 32 selection
rules carry an inert path. The fix is a validation change gated on core v86
(the runner already waits only on declared `requires`), a schema successor
allowing one path, and core v86 retiring the two box 4 stand-ins. All 596
recorded variants are identical. The fresh review found the exemption also
covered a categorical read the ADR does not name; the foreman narrowed it
to `collect` with a test that fails without the change.

## What worked

- A survey tool before the design: it showed the stand-in was unique, so
  the change could stay small, and it sized the inert-path follow-up.
- A per-package switch, as at core v75 and v76: every earlier core is
  untouched by construction, and the tests prove both directions by moving
  the threshold.
- Total grok cost about $33 for a substrate change with a schema
  successor.

## What to change

- Name every operator an exemption covers in the ADR draft, or narrow the
  code to the one the ADR names; the review caught the gap only because it
  read the operator set.

## Follow-ups

Parked in the roadmap: the 31 other inert paths, each retired when its
rule is next succeeded. ADR 0085 acceptance is with the owner.
