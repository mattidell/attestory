# ADR-0050 Draft Repair Charter

Audience: Builder

Date: 2026-07-29. Track 0 of Capital-Gain Distributions and Form 1040
Line 7a.

## Context Capsule

- **Source ref and resolved launch commit:** use the current local
  `decisions/capital-gain-distributions-line7a` branch and verify its commit at
  launch.
- **Exact object:** bounded drafting repair of proposed ADR-0050 against
  findings 1–5 in
  `reviews/adr0050-contract-review.md`.
- **Role:** Contract Repair Builder, High capability / high effort; resume the
  synthesis context for continuity.
- **Scope:** close D6–D9, milestone Contracts 6–8, history compatibility, and
  ADR form using the already-committed evidence. No new prototype evidence.
- **Stop conditions:** any need to reopen D1–D5, change the selected topology,
  climb an evidence rung, interpret governance, edit accepted ADR or published
  history, invent a new rule-language feature, implement production, use real
  data, or ratify the ADR.
- **Full reads before acting:** this charter; proposed ADR-0050;
  `evaluation-analysis.md`; `reviews/adr0050-contract-review.md`;
  `charter-review-adr0050.md`; `final-disposition.md`;
  `repair2/design.md`; `reviews/repair2-confirmation.md`; selected
  `it2/design.md` P3; the milestone plan's Contracts and Tax-content boundary;
  ADR-0010, ADR-0012, ADR-0029, ADR-0035, ADR-0037, and ADR-0038; the exact
  linked 2025 Form 1040 instructions for line 7b and the QDCG worksheet; and
  `docs/adr/INDEX.md`.

## Assignment

Repair only the five review findings. The review of the pre-renumbered
The existing ADR-0050 contract review remains the controlling findings record.

### F1 — Close the line-9 disposition

Remove every suggestion that production may choose a different downstream
outcome. Adopt the selected R2-N result exactly: when line 7a is
`guard_inapplicable`, line 9 is `blocked(DEPENDENCY_ABSENT)` on the selected
line-7a publication and taxable income blocks through line 9. Preserve the
distinct missing-authority and closure-backed-zero paths. Update D6,
consequences, production conditions, N2, and the evidence map consistently.

### F2 — Preserve the qualified-positive declaration obligation

Correct D7 and D9 against ADR-0038 and the selected P3 paper:

- ADR-0038's accepted qualified-positive path has two contributed
  declarations, not a sole Schedule-D declaration.
- For the successor Q-positive / closure-backed-L-zero branch, retain and pin
  the current `capital-gain-distributions` declaration exactly as R2-Q2 does.
- State explicitly which old Schedule-D-required authority is replaced by the
  four components plus checked conclusion.
- State explicitly how the capital-gain-distributions declaration behaves on
  the direct positive-line-7a branch, so the successor cannot require a value
  that contradicts its current non-null box-2a signal.

Leave one deterministic declaration/pin set for every Q/L branch; do not
create a second producer or raw box-2a path.

### F3 — Align D8 with direct derivation edges

Replace the transitive “every result pins every upstream producer” wording
with the measured hop-by-hop direct pin graph:

- checked conclusion → C1–C4;
- line 7a → selected member/family/closure authority plus C1–C4 as supported;
- line 7b → checked conclusion and its exact citation;
- line 9 → its ordinary inputs plus line 7a exactly once;
- taxable income → the existing declared upstream publications; and
- line 16 → its selected taxable-income, Q/L, declaration/conclusion,
  parameter, and citation inputs for the active branch.

Use “pin” only with ADR-0010 direct-edge meaning. Describe transitive lineage
as transitive, not as additional direct pins.

### F4 — Close line-7b citation authority

Name the exact 2025 Form 1040 instruction locus that line 7b pins under
ADR-0029. Reflect it in D8, production conditions, kill tests, and the evidence
analysis. Do not leave citation choice to implementation.

### F5 — Repair stable evidence links and numbering

Add both stable refs directly to ADR-0050 Links:

- `exhibits/capital-gain-distributions-line7a/it1`
- `exhibits/capital-gain-distributions-line7a/it2`

Keep the ADR and index status `proposed` and inert. Ensure every live
synthesis reference uses ADR-0050 and the `0050-...` filename.

## Outputs

Modify exactly:

- `docs/adr/0050-capital-gain-distributions-and-line-7a.md`
- `docs/archive/2026-08-02-milestone-artifacts/prototypes/capital-gain-distributions-line7a/evaluation-analysis.md`
- `docs/adr/INDEX.md`

Do not modify the review, review charter, prototype exhibits, repairs,
confirmations, dispositions, plan, phase state, SEAT, accepted ADRs, schemas,
content, fixtures, tests, production files, or other documentation.

## Completion

Before writing, echo F1–F5, the fixed evidence ceiling, the three outputs,
proposed/inert status, and stop conditions.

Commit only the three repaired outputs locally and stop. Do not push, merge,
ratify ADR-0050, perform recheck, begin production, or advance the pointer.
Return the commit SHA and F1–F5 status.

## Data safety

All evidence remains synthetic and publishable. No personal values,
identities, dispositions, refusal reasons, workspace locations, documents,
screenshots, or private artifacts may enter the repair.
