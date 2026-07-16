# Prototype Plan: Non-Publication Explanations

Audience: Agents

Status: **proposed.**

Topic: How non-publication dispositions (`blocked`, `guard_inapplicable`, and `invalid`) are explained and walked in the derivation cascade.

## Gate 0 — Decision inventory

| Id | Candidate decision | Standing |
|---|---|---|
| NPE-P1 | Explanation walking for non-publication states (blocked/inapplicable/invalid) reconstructs lineage from the dependency/guard references of the unexecuted rules, rather than storing mock values or empty findings in the active log. | Primary |
| NPE-P2 | The explanation walk API returns structured lineage trees that distinguish between missing dependencies (`blocked`) and unsatisfied applicability conditions (`guard_inapplicable`). | Tightly dependent secondary |

No execution performance optimization or UI presentation logic enters this topic.

## Gate 1 — Eligibility

Axes 0–2:
- Future blast radius: 2 (affects how explanation consumers read and present lineage)
- Migration cost: 1 (explanation walker API is relatively isolated)
- Residual paper uncertainty: 2 (unclear how to represent and walk unexecuted path dependencies cleanly)
- Inability to test cheaply: 1 (can write tests once implemented)
Total: **6**. Prototype-eligible.

## Gate 2 — Paper evidence

Each rival must resolve the following synthetic cases:
1. Wage citizen is present but 1099-INT family is unclosed, causing line 2b and all downstream lines to block (unclosed interest composition).
2. Married Filing Jointly return, but itemization override is inapplicable because standard deduction is larger (and itemization bypass is not asserted).
3. Invalid finding (e.g., failed validation constraint on a fact) blocking down-cascade derivations.

For each design: two positive instances, two negatives, one walk lifecycle trace, and input state → evaluation walk path → returned lineage representation. **If paper makes the choices clear, stop at paper.**

## Gate 3 — Evidence depth per question

Authorized level: static examples and throwaway evaluator mutations (Rung 2). A climb to Rung 2 is authorized because tracing the walk over an unexecuted rule's dependencies requires verifying if the saturation runner retains enough structure of the unexecuted rules to query them.

## Gate 4 — Cost caps

- Two paper builders: incumbent plus clean-room rival.
- No repair pass pre-authorized.
- Two Medium/medium reviewers (Governance and Adversary).
- Charter ≤ 100 lines; examination ≤ 120 lines; reviews have no line cap; total topic Markdown target ≤ 900 lines.

## Gate 5 — Triage

Foreman classifies every finding. Only explanation walking and lineage representation is decision-blocking. Formatting, graph rendering, and localized error messages are separate or deferred.

## Gate 6 — Minimum converged subset

The floor is NPE-P1: a validated design that allows walking non-publication lineage without polluting the kernel act log with mock findings.

## Gate 7 — Production boundary

Only documents merge. Accepted structures become a Tier-2 ADR and are then implemented in the milestone branch. Prototype schemas or code do not merge.

## Gate 8 — Roles

| Role | Tier | Reason |
|---|---|---|
| Foreman | Medium/medium | Scope and conformance steward |
| Incumbent builder | High/high | Design Shape A: Rule-definition query (extracting dependencies directly from unexecuted rule AST/schemas) |
| Rival builder | High/high | Design Shape B: Explicit dry-run finding acts (creating lightweight stub findings representing blocked status) |
| Governance reviewer | Medium/medium | Conformance checks against kernel/derivation schemas |
| Adversary reviewer | Medium/medium | Counterexamples to walk accuracy (e.g. cyclic/multi-path blocks) |

Reviewers are spawned as sub-agents by the foreman by default upon plan approval.

## Review measurements

Governance checks that the design does not violate the append-only finding/fact invariants. Adversary tests with complex multi-step blocks and inapplicable conditions.

## Data safety

All amounts, bracket thresholds, and filing status labels are synthetic or standard IRS tables represented synthetically.
