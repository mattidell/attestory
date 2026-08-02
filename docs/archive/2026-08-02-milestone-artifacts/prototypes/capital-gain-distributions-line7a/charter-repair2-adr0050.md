# ADR-0050 Draft Repair 2 Charter — Both-Zero Direct Pins

Audience: Builder

Date: 2026-07-29. Track 0 of Capital-Gain Distributions and Form 1040
Line 7a.

## Context Capsule

- **Source ref and resolved launch commit:** use the current local
  `decisions/capital-gain-distributions-line7a` branch and verify its commit at
  launch.
- **Exact object:** one findings-only drafting repair of the sole residual in
  `reviews/adr0050-contract-recheck.md`, as classified in
  `adr0050-recheck-disposition.md`.
- **Role:** Contract Repair Builder, Medium–High capability / medium effort;
  resume the synthesis context for continuity.
- **Scope:** make D7, D8, D9 where affected, and the evidence analysis state
  one exact declaration/conclusion direct-pin set for each Q/L branch. No
  other contract change.
- **Stop conditions:** any need for new evidence, a topology change, a new
  rule-language feature, an index change, governance interpretation, accepted
  ADR/history edits, production work, real data, or owner ratification.
- **Full reads before acting:** this charter;
  `adr0050-recheck-disposition.md`;
  `reviews/adr0050-contract-recheck.md`; proposed ADR-0050;
  `evaluation-analysis.md`; `repair2/design.md` §7 and Case R2-Q3;
  `reviews/repair2-confirmation.md` F4; selected `it2/design.md` P3 sentence 4;
  ADR-0010 and ADR-0038.

## Assignment

Remove the one conflict identified by the recheck.

State these four branches explicitly and consistently in D7 and D8:

| Qualified dividends Q | Selected line 7a L | Required direct declaration/conclusion pins |
| --- | --- | --- |
| Q>0 | closure-backed L=0 | current `capital-gain-distributions="no"` plus checked conclusion `"no"` |
| Q=0 | L>0 | checked conclusion `"no"`; no separate line-16 read of `capital-gain-distributions` |
| Q>0 | L>0 | current `capital-gain-distributions="yes"` plus checked conclusion `"no"` |
| Q=0 | closure-backed L=0 | **neither declaration nor checked conclusion**; reproduce R2-Q3's exact ordinary-result direct set |

For the both-zero branch, line 16 directly pins taxable income, filing status,
rounding, Q=0, the selected closure-backed line-7a-zero publication, ordinary
tax parameters, and its citation. The line-7a-zero publication carries its own
authority/closure pins; those remain transitive lineage for line 16 and must
not be restated as new direct pins.

Update D9 only as needed to say that ADR-0038's declaration-free
qualified-zero reduction remains declaration/conclusion-free when the
successor's selected line 7a is also closure-backed zero. Do not weaken the
other three repaired branch contracts.

Update `evaluation-analysis.md` so D7, D8, D9, F2/F3, Contracts 7/8, and
history compatibility route to the same four-row result. Remove any sentence
that says all Q-zero branches use the checked conclusion.

## Outputs

Modify exactly:

- `docs/adr/0050-capital-gain-distributions-and-line-7a.md`
- `docs/archive/2026-08-02-milestone-artifacts/prototypes/capital-gain-distributions-line7a/evaluation-analysis.md`

Do not modify the ADR index, review or recheck, charters, dispositions,
prototype evidence, plan, phase state, SEAT, accepted ADRs, schemas, content,
fixtures, tests, production files, or other documentation.

## Completion

Before writing, echo the single residual, the four branch pin sets, the two
outputs, fixed Rung-1 evidence ceiling, and stop conditions.

Commit only the two repaired outputs locally and stop. Do not push, merge,
ratify ADR-0050, perform final recheck, begin production, or advance the
pointer. Return the commit SHA and R1 status.

## Data safety

All evidence remains synthetic and publishable. No personal values,
identities, dispositions, refusal reasons, workspace locations, documents,
screenshots, or private artifacts may enter the repair.
