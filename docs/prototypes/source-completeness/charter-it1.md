# Charter: Iteration 1 — Incumbent Paper Design

Date: 2026-07-12. Foreman-issued under the approved `plan.md`.

- **Branch:** `prototypes/source-completeness/it1`
- **Evidence rung:** 1 — static documents only (plan Gate 3). No code, no
  schema files consumed by any runner, no rung climb. If the builder believes
  paper cannot settle a question, that is a *finding in the examination*, not
  a license to climb.
- **Builder seat:** `roles/builder.md`, High tier (high effort), per Gate 8.
- **Propositions:** SC-P1 (primary), SC-P2, SC-P3 — as inventoried in
  `plan.md` Gate 0. Nothing else. SC-D1 work is out of charter.

## Deliverables (all on the branch, plus the examination)

Per the plan's Gate 2 paper-evidence plan:

1. **SC-P1 mapping design** — a candidate design for how a current,
   affirmative closure finding becomes closed membership for a source family
   via a pinned, adopted artifact, with:
   - positive instance (a): interest source family, true current closure
     finding → empty-source zero publication, pins traced to the closure
     finding;
   - positive instance (b): the same shape instantiated for the existing W-2
     closure fact type (`packages/schemas/tax/`, ADR-0011) — proving the
     shape is not interest-specific;
   - negative (c): false closure finding → blocked, never zero;
   - negative (d): superseded (displaced) closure finding → blocked;
   - lifecycle trace: closure asserted → mapping adopted → run publishes
     zero → closure corrected/withdrawn → displacement cascades to the
     derived zero → explicit rerun blocks;
   - producer → authority → consumer → failure map (who writes the closure
     finding, what adopts the mapping, what the runner reads, each failure
     mode).
2. **SC-P2 identity design** — a chosen identity key with:
   - the one-payer-two-accounts distinctness case worked under the chosen
     key *and* under at least one rejected rival key showing the collision;
   - a same-fact correction preserving identity (lifecycle: original →
     corrected 1099-INT with displacement);
   - negative: an evidence-keyed candidate rejected by Article 1.
3. **SC-P3** — the source-family definition, stated once and exercised by
   the instances above; no separate fixtures.
4. **`examination-it1.md`** (≤ 200 lines) — evidence paths, negative
   results disclosed, and an explicit statement per proposition: settled at
   paper / needs rung 2 / needs rung 3, with the single question driving any
   climb recommendation.

## Pre-declared checks (the examination must show each)

1. Every Gate 2 fixture above is present and fully resolved (no
   placeholders).
2. Affirmative-only enforcement is stated against the real two-layer
   `collect` check (`evaluator.py`), not an abstraction of it.
3. No identity key contains an evidence or document key (Article 1).
4. The empty-source zero's explanation walk reaches the authorizing closure
   finding through pins.
5. Negatives fail for the declared reasons, not incidentally.

## Constraints

- Work only on the charter branch; restore or use a separate worktree
  (builder worktree hygiene).
- No production schemas in `packages/`; no edits outside the branch's
  prototype directory and `docs/prototypes/source-completeness/
  examination-it1.md`.
- All fixture data synthetic: manufactured payers, accounts, amounts; no
  account-number-realistic strings.
- Reserved T1/T2 doctrine untouched.

## Committee round 1 (declared now, runs after it2)

Per plan: governance-fidelity and adversary reviewers only, dispatched after
the rival (it2) concludes so attack parity is possible. Measures and failure
shapes are declared in the plan's review-measurement section and the role
files.
