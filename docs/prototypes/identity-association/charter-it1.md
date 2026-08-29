# Charter: Iteration 1 — Incumbent-Informed Design

Date: 2026-08-28. Foreman-issued under `plan.md`.

- **Branch:** `prototypes/identity-association/it1`
- **Evidence rung:** 1 — static documents only.
- **Builder seat:** `roles/builder.md`, High tier (high effort).
- **Propositions:** IA-P1 (primary), IA-P2 (secondary) — see `plan.md`
  Gate 0.

You may read, as reference evidence only (not a pre-selected answer): the
prior single-track attempt's canonical-slice work
(`docs/milestones/document-ordinary-fact-translation/canonical-slice.md`,
`production-translation.md`, if present in your worktree) — it built
payer-level association with an item-level amount constraint and was
returned NOT READY; treat its association shape as one candidate to
re-justify, and note it left statement-level association (one payer issuing
two statements covering different obligations) as named future work — your
design should say explicitly whether it closes that gap or inherits it.
Also read Seam 1's accepted decision,
`docs/adr/0067-canonical-acquisition-field-ref-access.md`, for what a
canonical acquisition fact already looks like.

## Deliverables

1. For **all three candidates** (generic family-declared association; a
   dedicated translation/association artifact; an existing rule-owned
   relationship mechanism, if one genuinely exists in the codebase — verify
   by grepping, don't assume): a design sketch answering all seven named
   cases in `plan.md` Gate 2.
2. A recommendation, with explicit treatment of the statement-level
   association gap the prior attempt left open.
3. `examination-it1.md` (≤ 200 lines): your recommended candidate worked
   through all seven cases in full; the other two at least for cases 2 (no
   match) and 3 (several matches) — the cases most likely to distinguish a
   real refusal/ambiguity mechanism from a paper sketch; producer→
   authority→consumer→failure map; per-case rung disposition.

## Constraints

- Work only on the charter branch, `docs/prototypes/identity-association/`,
  and `examination-it1.md`. No production schema edits under `packages/`.
- All fixture data synthetic.
- Do not review `it2` or read its branch. Do not decide tax arithmetic
  (IA-P2) — state the boundary, don't build a constraint check.

## Committee round 1

Declared now, runs after both `it1` and `it2` conclude: clean-room,
adversarial, and eligibility reviewers.
