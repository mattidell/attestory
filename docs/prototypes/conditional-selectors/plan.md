# Prototype Plan: Conditional Selectors

Audience: Agents

Status: **proposed.**

Topic: How standard deduction selection and tax computation method selection (bracket table selection) are modeled and resolved within the derivation cascade.

## Gate 0 — Decision inventory

| Id | Candidate decision | Standing |
|---|---|---|
| CS-P1 | Conditional tax selections (like standard deduction status adjustments and tax table selection) are modeled as derived findings computed via rule expressions, rather than introducing a new specialized citizen type or hardcoded runner pathways. | Primary |
| CS-P2 | Standard deduction and tax bracket lookup tables are represented as structured parameter citizens that rules query, preserving separation between logic and data. | Tightly dependent secondary |

No multi-year filing, multi-state adjustments, or UI integration enters this topic.

## Gate 1 — Eligibility

Axes 0–2:
- Future blast radius: 2 (affects all downstream calculations on Form 1040)
- Migration cost: 2 (expensive to change if we commit to a complex selector schema that breaks saturation)
- Residual paper uncertainty: 1 (concept is clear on paper but needs validation in cascade)
- Inability to test cheaply: 1 (requires derivation integration to see cascading impact)
Total: **6**. Prototype-eligible.

## Gate 2 — Paper evidence

Each rival must resolve the following synthetic cases:
1. Single filer, standard deduction ($15,000 for 2025).
2. Married Filing Jointly, standard deduction ($30,000 for 2025).
3. Single filer, over 65 (additional standard deduction $2,000).
4. Married filer, blind (additional standard deduction $1,550).
5. Tax bracket lookup crossing a threshold (e.g., $10,000 to $11,000).

For each design: two positive instances, two negatives, one lifecycle trace, and claim → citizen schemas → runner logic → derived finding map. **If paper makes the choices clear, stop at paper.**

## Gate 3 — Evidence depth per question

Authorized level: static examples and throwaway evaluator mutations (Rung 2). A climb to Rung 2 is authorized because we need to verify how the saturation runner executes the rule expression without infinite loops or evaluation order bugs.

## Gate 4 — Cost caps

- Two paper builders: incumbent plus clean-room rival.
- No repair pass pre-authorized.
- Two Medium/medium reviewers (Governance and Adversary).
- Charter ≤ 100 lines; examination ≤ 120 lines; reviews have no line cap; total topic Markdown target ≤ 900 lines.

## Gate 5 — Triage

Foreman classifies every finding. Only standard deduction calculation and tax rate fold selector representation is decision-blocking. Itemized deduction overrides, other tax schedules, and credits are separate or deferred.

## Gate 6 — Minimum converged subset

The floor is CS-P1: a validated design that models standard deduction selection and tax computation selection without changing the core derivation engine's architecture.

## Gate 7 — Production boundary

Only documents merge. Accepted structures become a Tier-2 ADR and are then implemented in the milestone branch. Prototype schemas or code do not merge.

## Gate 8 — Roles

| Role | Tier | Reason |
|---|---|---|
| Foreman | Medium/medium | Scope and conformance steward |
| Incumbent builder | High/high | Design Shape A: Rule-driven derivation using existing rule language |
| Rival builder | High/high | Design Shape B: Specialized selector schema/citizen type |
| Governance reviewer | Medium/medium | Conformance checks against derivation schemas |
| Adversary reviewer | Medium/medium | Counterexamples to selector correctness and scalability |

Reviewers are spawned as sub-agents by the foreman by default upon plan approval.

## Review measurements

Governance checks that the schema conforms to the rules of derived findings and does not introduce out-of-order execution. Adversary tests with age/blindness combinations and threshold edge cases.

## Data safety

All amounts, bracket thresholds, and filing status labels are synthetic or standard IRS tables represented synthetically.
