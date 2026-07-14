# Prototype Plan: Expression Language Extensions

Audience: Agents

Status: **approved** (owner approved the topic and chartering 2026-07-13; plan drafted by the principal foreman under that directive — owner may amend before builder launch).

Topic: Two contract gaps in the rule expression language, both established by the remediated conditional-selectors evidence: (1) a declared absence/default mechanism for optional scalar inputs, and (2) first-class categorical (string) comparison.

## Gate 0 — Decision inventory

| Id | Candidate decision | Standing |
|---|---|---|
| ELX-P1 | Optional scalar inputs gain a *declared* default mechanism: an unasserted optional input evaluates to its declared default and gives way — via ordinary supersession/displacement, no third edge kind — when the input is later asserted; asserted inputs are never overwritten. | Primary |
| ELX-P2 | Expressions gain categorical comparison: guards can match string/enumerated values (e.g. filing status) directly, without decimal coercion or numeric-code workarounds. | Secondary, same contract surface |

No UI, no new citizen families, no changes to publication/record contracts enter this topic.

## Gate 1 — Eligibility

- Future blast radius: 3 (the expression language is the contract all future tax content is written in)
- Migration cost: 2 (content written under interim workarounds must upgrade)
- Residual paper uncertainty: 2 (the impossibility result constrains the solution space but the conforming mechanism is undesigned; Article 7 edge integrity is the hard part)
- Inability to test cheaply: 1 (verifiable against the committed evaluator with probes)
Total: **8**. Prototype-eligible.

## Gate 2 — Paper evidence

Each builder must resolve these synthetic cases:
1. Single filer, `taxpayer_age65` unasserted → standard deduction resolves via declared default; no block, no overwrite.
2. Same workspace: `taxpayer_age65` later asserted true → dependent derived findings displace and re-derive through ordinary edges; the initial-run-then-assertion lifecycle trace is mandatory.
3. `taxpayer_age65` explicitly asserted false from the start → identical result to case 1, but pinned to the asserted finding, and no default may overwrite it.
4. Categorical guard: `filing_status = "married_filing_jointly"` matches and `"single"` does not, with no decimal coercion; a mismatch of types (categorical vs numeric operand) is a contained, explained failure.
5. Negative: a *non-optional* absent input still blocks exactly as today.

For each design: two positive instances, two negatives, one lifecycle trace, and claim → schema/contract change → evaluator/runner behavior → derived finding and pin map. **If paper makes the choices clear, stop at paper.**

## Gate 3 — Evidence depth per question

Authorized level: Rung 2 — static examples plus throwaway evaluator/runner probes in a scratch directory (read-only with respect to the repository). Authorized because the prior topic's failure mode was exactly paper designs that did not execute; every claimed behavior must be traced or probed against the committed evaluator, and proposed contract changes shown as versioned schema/canon diffs on paper.

## Gate 4 — Cost caps

- Two paper builders: incumbent plus clean-room rival (ADR-0013 amendment: genuine rivalry every round).
- No repair pass pre-authorized.
- Two Medium reviewers (Governance and Adversary), independent contexts.
- Charter ≤ 100 lines; examination ≤ 120 lines; total topic Markdown target ≤ 900 lines.

## Gate 5 — Triage

Foreman classifies every finding. Decision-blocking only: absence/default semantics (including displacement integrity and overwrite prohibition) and the categorical comparison contract. Numeric formatting, error-message wording, and broader type-system ambitions are deferred.

## Gate 6 — Minimum converged subset

The floor is ELX-P1: a validated mechanism for declared optional defaults that survives the round-2R adversary's three refuted constructions (multi-publisher staging, closure-aggregation misuse, evaluation-order tricks) without violating Articles 7 or 11.

## Gate 7 — Production boundary

Only documents merge. Accepted structures become a Tier-2/3 ADR (candidate number 0025); evaluator/runner/schema implementation lands in the milestone branch afterward. Content written under ADR-0024's interim decisions 5–6 upgrades then.

## Gate 8 — Roles

| Role | Tier | Reason |
|---|---|---|
| Foreman | Medium | Scope and conformance steward |
| Incumbent builder | High | First design, both propositions |
| Rival builder | High | Clean-room rival, both propositions |
| Governance reviewer | Medium | Article 7/11 edge and declaration conformance |
| Adversary reviewer | Medium | Counterexamples: overwrite, displacement, coercion, deadlock |

All seats owner-launched or foreman-spawned per standing directives at dispatch time.

## Review measurements

Governance: no third edge kind, no runner-resident policy, defaults declared in versioned content/schema, asserted findings never overwritten, ADR-0012 disposition vocabulary intact. Adversary: the Gate 2 cases plus deliberate attempts to reconstruct the three refuted workarounds and to break displacement ordering (assert-after-run, assert-then-supersede, default-then-remove).

## Data safety

All amounts, statuses, and identifiers synthetic.
