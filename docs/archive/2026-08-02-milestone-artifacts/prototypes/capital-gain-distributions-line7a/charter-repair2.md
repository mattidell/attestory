# Repair Charter 2 — Reconcile the Composite Paper Evidence

Audience: Builder

Date: 2026-07-28. Track 0 of Capital-Gain Distributions and Form 1040
Line 7a.

## Context Capsule

- **Source ref and resolved launch commit:** use the current local
  `prototypes/capital-gain-distributions-line7a/it2` branch and verify its
  commit at launch.
- **Exact object:** a final findings-only repair of the selected
  component-backed paper design, bounded to F1–F4 in
  `reviews/repair1-confirmation.md` and their foreman classifications in
  `repair1-confirmation-disposition.md`.
- **Role:** Repair Builder, High capability / high effort.
- **Scope and evidence-rung ceiling:** reconcile the composite it2 + repair
  paper evidence for T-F1/T-F2. Rung 1 static paper evidence only.
- **Stop conditions:** any new proposition, production code, schema/content
  edit, validator/evaluator probe, governance interpretation, Schedule D
  implementation, boxes 2b/2c/2d source-family implementation, real data,
  topology reopening, or scope beyond F1–F4. Stop rather than inventing tax
  values or pins that the selected paper cannot support.
- **Full reads before acting:** this charter;
  `repair1-confirmation-disposition.md`; `charter-repair1.md`;
  `charter-repair1-confirmation.md`; `reviews/repair1-confirmation.md`;
  `repair1/design.md`; `repair1/examination.md`; `it2/design.md`;
  `it2/examination.md`; `round-1-triage.md`; the topic `plan.md`; ADR-0035;
  ADR-0038; the milestone plan's Contracts, Fixtures, and Data Safety
  sections; the linked official 2025 Form 1040 instructions for lines 7a, 7b,
  and 16 and the Qualified Dividends and Capital Gain Tax Worksheet; and
  `packages/content/tax/2025/rule.form1040-line16.v2.json`.

## Assignment

Produce a self-consistent replacement layer over the selected it2 design. Do
not redesign the topology. Repair 2 must state exactly which it2 and Repair 1
sentences, maps, cost counts, shorthands, and cases it supersedes. After those
supersessions, a reader must have only one live meaning for E and only one live
outcome for Q=0 with positive line 7a.

### F1 — Complete and reconcile four-component eligibility

- Replace every retained “three components,” “all three,” `+3`, E-yes
  shorthand, producer-map entry, and eligible-case pin statement affected by
  the fourth component.
- Reinstantiate one eligible single-payer state with exact synthetic member,
  closure, all four current component finding identities and values, checked
  conclusion, pins, line 7a/7b dispositions, line 9, taxable income, and line
  16 path.
- Preserve the missing and current-`"no"` states, but make `blocked`,
  `guard_inapplicable`, published value, and closure-backed zero explicit.
- Keep the boxes-2b/2c/2d assertion distinct from box-2a closure and do not
  invent source families for excluded boxes.

### F2 — Make correction and supersession recoverable

Give one exact forward and reverse lifecycle table for the new component. It
must name synthetic finding versions, which version is current or displaced,
the pin edges, and the disposition of the checked conclusion, line 7a, line
7b, line 9, taxable income, and line 16 at every step. The reverse transition
must add a new correction rather than revive or overwrite history.

### F3 — Retire the contradictory Case 10

Explicitly supersede the selected it2 Case 10 and its unresolved-production
flag. Replace it with one authoritative Q=0 / positive-line-7a case in which
the QDCG worksheet is selected, worksheet line 3 is pinned to line 7a, and the
capital-gain amount enters the preferential path. No live retained sentence or
case may still prescribe ordinary-only tax for that state.

### F4 — Make the QDCG structure and cases exact

- Write the declared conditional structure as an explicit decision table or
  expression tree whose result is independent of incidental operand order.
- Keep blocked and guard-inapplicable inputs outside both the zero and positive
  numeric branches; never coerce either to zero.
- Provide exact paper rows for Q=0 / positive line 7a, Q>0 /
  closure-backed line 7a=0, and Q=0 / closure-backed line 7a=0.
- For each row, show selection, worksheet inputs and pins, line 9, taxable
  income, and line 16 disposition. Use an exact numeric line-16 result only if
  the selected paper already supplies every filing-status, taxable-income, and
  threshold input needed to derive it; otherwise give an exact named
  publication/disposition and pin set without inventing a number.
- Reaffirm successor/historical graph exclusivity, the non-null box-2a
  presence signal, closure-backed zero, no raw downstream reads, and honest
  non-publication.

## Outputs

Create exactly:

- `docs/archive/2026-08-02-milestone-artifacts/prototypes/capital-gain-distributions-line7a/repair2/design.md`
- `docs/archive/2026-08-02-milestone-artifacts/prototypes/capital-gain-distributions-line7a/repair2/examination.md`

`design.md` contains the explicit supersession ledger, corrected composite
maps and cost, exact affected paper cases, lifecycle table, QDCG decision
structure, and retained-boundary statements.

`examination.md` reports F1–F4 separately as resolved or unresolved, names
every superseded contradiction, and reports T-F1/T-F2 plus regression-boundary
status with exact file/section citations. Self-assessment does not replace
paper evidence in `design.md`.

Do not edit it2, Repair 1, any review, triage/disposition record, charter,
plan, phase state, SEAT, ADR, schema, content, fixture, test, production file,
or another prototype directory.

## Completion

Before writing, echo the exact repair object, F1–F4 scope, Rung-1 ceiling,
required outputs, official-instruction checks, and stop conditions.

Commit only the two Repair 2 outputs locally and stop. Do not push, merge, open
a PR, perform confirmation, synthesize the contract, draft an ADR, begin
production, or advance the pointer. Return the commit SHA and F1–F4 status.

## Data safety

Every example is synthetic and publishable. No personal values, identifiers,
dispositions, refusal reasons, workspace locations, documents, screenshots,
or private artifacts may enter the repair.
