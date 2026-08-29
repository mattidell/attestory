# Charter: Iteration 1 — Incumbent-Informed Design

Date: 2026-08-28. Foreman-issued under `plan.md`.

- **Branch:** `prototypes/standing-authorization-successor/it1`
- **Evidence rung:** 1 — static documents only.
- **Builder seat:** `roles/builder.md`, High tier (high effort).
- **Propositions:** SA-P1 (primary), SA-P2 (secondary) — see `plan.md` Gate 0.

You may read Seam 4's spike (`docs/prototypes/standing-authorization-currentness/charter.md`,
`examination.md`) as reference evidence: it establishes that the only real
committed mechanism (per-family closure) has no taxpayer/year identity at
all, is not "standing" by construction, and collapses suspension/withdrawal
into simple absence. Treat this as the negative space to design away from,
not a starting point to patch.

Ground your design in the real committed kernel machinery: how facts,
findings, and acts are declared, identified, and admitted
(`packages/kernel/`), and how `completeness-support-decision.md`'s
"Principal remaining decision" section already bounds the scope question
(workspace, taxpayer/return subject, tax year, adopted-package boundary).

## Deliverables

1. A candidate citizen shape for the standing workspace authorization:
   identity (what scopes it — taxpayer, year, workspace, package boundary),
   an explicit suspend/withdraw act kind distinct from absence, and how a
   consumer checks currentness against a calculation's actual
   taxpayer/year.
2. Work all six named cases from `plan.md` Gate 2 (correct taxpayer/year,
   wrong taxpayer, wrong year, ordinary additions/removals, suspension or
   withdrawal, no renewed per-family confirmation) against your design.
3. A stance on SA-P2: what changes to the adopted-package/vocabulary
   boundary should force re-authorization, stated as a checkable rule, not
   left as taste.
4. `examination-it1.md` (≤ 200 lines): the six cases worked in full,
   producer→authority→consumer→failure map, and an explicit per-case
   statement of settled-at-paper vs. needs-rung-2.

## Constraints

- Work only on the charter branch and `docs/prototypes/standing-authorization-successor/`.
  No production schema edits under `packages/`.
- All fixture data synthetic.
- Do not review `it2` or read its branch.

## Committee round 1

Declared now, runs after both `it1` and `it2` conclude: clean-room,
adversarial, and eligibility reviewers.
