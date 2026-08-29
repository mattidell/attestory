# Charter: Iteration 2 — Clean-Room Rival Design

Date: 2026-08-28. Foreman-issued under `plan.md`.

- **Branch:** `prototypes/canonical-value-extraction/it2`
- **Evidence rung:** 1 — static documents only (plan Gate 3). No production
  schema edits.
- **Builder seat:** `roles/builder-rival.md` (this topic's version), High
  tier (high effort). Dispatched via Grok CLI in an isolated worktree.
- **Propositions:** CV-P1 (primary), CV-P2 (secondary) — see `plan.md`
  Gate 0. Identical propositions to `it1`; the value here is independence,
  not a different question.

**Independence obligation (binding):** do not read `it1`'s branch,
examination, or the prior single-track milestone attempt
(`docs/milestones/document-ordinary-fact-translation/`,
`docs/domain-models/taxable-interest-translation.md`). Read only
`plan.md`, this charter, the governance set, the accepted rule-language and
fact/finding ADRs, and the real evaluator/schema code under
`packages/derivation/` and `packages/schemas/` needed to ground a mechanism
in real machinery.

## Deliverables

1. For **all three candidates** (runtime scalar projection, explicit
   rule-produced numeric finding, direct per-item rule access): a design
   sketch sufficient to answer the six named test cases from `plan.md` Gate 2.
2. A recommendation: which candidate you'd build first and why, stated
   against the milestone's decision rule.
3. `examination-it2.md` (≤ 200 lines): the six cases worked through for your
   recommended candidate in full, the other two candidates worked through at
   least for cases 2 (hostile scalar) and 6 (misspelled declaration), and the
   producer→authority→consumer→failure map.
4. Explicit statement per case: settled at paper / needs rung 2, with the one
   question that would justify a climb.

## Constraints

- Work only on the charter branch and `docs/prototypes/canonical-value-extraction/`,
  writing only `examination-it2.md` plus any small supporting fixture files
  you need in that directory. No edits to `packages/` production schemas.
- All fixture data synthetic.
- Do not review `it1` or read its branch. Report independently even if your
  recommendation happens to match a shape you'd expect the incumbent to have
  chosen.

## Committee round 1

Declared now, runs after both `it1` and `it2` conclude, per `plan.md` Gate 8:
clean-room, adversarial, and eligibility reviewers, attack/read parity across
both builds.
