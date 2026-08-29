# Charter: Iteration 1 — Incumbent-Informed Design

Date: 2026-08-28. Foreman-issued under `plan.md`.

- **Branch:** `prototypes/canonical-value-extraction/it1`
- **Evidence rung:** 1 — static documents only (plan Gate 3). No production
  schema edits.
- **Builder seat:** `roles/builder.md`, High tier (high effort).
- **Propositions:** CV-P1 (primary), CV-P2 (secondary, rides CV-P1
  fixtures) — see `plan.md` Gate 0.

You may read the current incumbent path: the existing
`scheduleb-adjustment.accrued-interest` closure mapping and its consumers
(`grep -rl accrued_interest_paid_to_seller` and `grep -rl accrued-interest`
under `packages/content/tax/2025/`, `packages/derivation/`,
`packages/tax/`), and — as reference evidence only, not a pre-selected
answer — the prior single-track attempt's canonical-slice work at
`docs/milestones/document-ordinary-fact-translation/canonical-slice.md` and
`docs/milestones/document-ordinary-fact-translation/production-translation.md`
if that history exists in your worktree. That attempt was returned NOT READY;
treat its scalar-projection choice as one candidate to re-justify, not as
settled.

## Deliverables

1. For **all three candidates** (runtime scalar projection, explicit
   rule-produced numeric finding, direct per-item rule access): a design
   sketch sufficient to answer the six named test cases from `plan.md` Gate 2
   (authoritative amount, hostile scalar, correction, missing field, exact
   provenance, misspelled declaration failing closed).
2. A recommendation: which candidate you'd build first and why, stated
   against the milestone's decision rule ("if direct per-item access
   resolves every test without expression-language growth, prefer it").
3. `examination-it1.md` (≤ 200 lines): the six cases worked through for your
   recommended candidate in full, the other two candidates worked through at
   least for cases 2 (hostile scalar) and 6 (misspelled declaration) — the
   cases most likely to distinguish a real mechanism from a paper sketch —
   and the producer→authority→consumer→failure map.
4. Explicit statement per case: settled at paper / needs rung 2, with the one
   question that would justify a climb.

## Constraints

- Work only on the charter branch, `docs/prototypes/canonical-value-extraction/`,
  and `examination-it1.md`. No edits to `packages/` production schemas.
- All fixture data synthetic.
- Do not review `it2` or read its branch.

## Committee round 1

Declared now, runs after both `it1` and `it2` conclude, per `plan.md` Gate 8:
clean-room, adversarial, and eligibility reviewers, attack/read parity across
both builds.
