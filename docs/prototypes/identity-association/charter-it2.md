# Charter: Iteration 2 — Clean-Room Rival Design

Date: 2026-08-28. Foreman-issued under `plan.md`.

- **Branch:** `prototypes/identity-association/it2`
- **Evidence rung:** 1 — static documents only.
- **Builder seat:** `roles/builder-rival.md` (this topic's version), High
  tier (high effort). Dispatched via Grok CLI in an isolated worktree.
- **Propositions:** IA-P1 (primary), IA-P2 (secondary) — identical to
  `it1`; the value here is independence.

**Independence obligation (binding):** do not read `it1`'s branch or
examination, or the prior single-track milestone attempt
(`docs/milestones/document-ordinary-fact-translation/`). Read only
`plan.md`, this charter, the governance set, ADR-0067, and the real
fact/finding/identity code under `packages/kernel/` and
`packages/derivation/`.

## Deliverables

1. For **all three candidates**: a design sketch answering all seven named
   cases in `plan.md` Gate 2.
2. A recommendation, with explicit treatment of whether one payer issuing
   two statements covering different obligations (a statement-level
   association question) is handled by your design or named as a gap.
3. `examination-it2.md` (≤ 200 lines): your recommended candidate worked
   through all seven cases in full; the other two at least for cases 2 and
   3; producer→authority→consumer→failure map; per-case rung disposition.

## Constraints

- Work only on the charter branch and `docs/prototypes/identity-association/`,
  writing only `examination-it2.md` plus any small supporting fixture files.
  No production schema edits under `packages/`.
- All fixture data synthetic.
- Do not review `it1` or read its branch. Do not decide tax arithmetic
  (IA-P2).

## Committee round 1

Declared now, runs after both `it1` and `it2` conclude: clean-room,
adversarial, and eligibility reviewers.
