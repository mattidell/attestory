# ADR 0085 — A selection path collects its activity family without a symbol

- Status: **proposed**
- Tier: 2 — a rule-language and schema-successor contract later rules are
  written against.
- Date: 2026-11-10

## Context

ADR 0077 Part 4 lets a return-level rule choose among paths by exclusive
presence. A path's `requires` are the `ref` names in that path and any
collect-family name that is not a per-subject read and not a closed-family
count. The runner waits until those names are in the symbol table. Marshal
puts keyed family members into collect sources and does not bind them as a
single symbol.

Form 1099-B box 4 on core v83 needed a selection that sums every current
amount, and a default of zero when none is recorded, without asking a
closure question. The amounts path collects the keyed family
`tax.us.2025.f1099b.b4`. Because that collect name had to be a symbol, a
content rule publishes 0 under the amount's own fact id. The explanation
walk of that id is 0 beside a recorded amount. Separately, Part 4 and
`rule-artifact.v15` require at least two paths, so the rule carries an
inert second path on a fact type nothing writes.

P0 of the selection-keyed-collect milestone surveyed every core from v2
through v85. The amount-symbol rule is the only stand-in of that kind.
Thirty-two selection rules on v85 still carry an inert second path. One
adopted rule, Form 1040 line 2b v8, has two real paths.

## Decision

1. **Collect of the path's activity family is not a symbol dependency.**
   On `core-calculations` from v86, a selection path whose activity is
   `source_nonempty` on an adopted family does not list that family's
   member collect in `requires`. Package validation expects the same
   omission. The runner waits only on the remaining `requires` (ordinary
   `ref` names). The collect still reads current sources of that member.
   Marshal is unchanged: keyed members stay sources, never a single
   symbol. Earlier cores, and packages that are not `core-calculations`,
   keep the ADR 0077 equality and the recorded stand-in wait. The switch
   is the adopted package id and version.

2. **A selection may have one path.** `rule-artifact.v16` is v15 with
   `paths.minItems` 1. Exclusive presence with one path and a default is
   that activity or the closed-empty default. Two or more real paths keep
   exclusive presence and refuse as they do today. `rule-artifact.v15`
   and earlier are unchanged. A successor core that needs one real path
   and a default uses v16 and does not carry an inert path.

3. **This record supplements ADR 0077 Part 4** for packages on which the
   v86 switch is on, and for rules that declare `rule-artifact.v16`. It
   does not change line 2b v8, v9 selection authorization, or any
   expression operator.

## Consequences

A successor core can retire `rule.f1099b-b4-amount-symbol` and the inert
path on the box 4 subtotal. The subtotal still publishes the sum of
current amounts, or zero when none is recorded. The member fact id is no
longer published as 0.

Track 1 must publish `rule-artifact.v16`, admit it on a package successor,
thread `v16` through the derivation enumerations that already list v15,
and add the v86 companion-declaration loader entry. It must not edit
published v15.

A later `ref` of a keyed member id still has no single symbol. That is the
existing marshal contract.

## Links

- Plan: `docs/phases/engine-breadth/milestones/selection-keyed-collect.md`
- Evidence: `docs/phases/engine-breadth/milestones/selection-keyed-collect-evidence/p0.md`
- ADR 0077 Part 4 (presence selection)
- Precedent switches: `unconfirmed_family_names_closure_question` (v75),
  `later_any_arm_refs_while_count_blocked` (v76)
