# Prototype Plan: Source-Family Semantics

Audience: Agents

Status: **draft — owner approval required before charter or builder dispatch.**

Topic: the SC-P3 boundary deferred by the Source Completeness evaluation: what
a source family means, what a closure assertion claims complete, and when that
claim is coextensive with mapping and coverage consumers.

## Gate 0 — Decision inventory

| Id | Candidate decision | Standing |
|---|---|---|
| SFS-P1 | A closure-authorized source family has one declared universe shared by its user-facing claim, member fact types/source instances, adopted mapping, and coverage consumer; closure never silently broadens from a document family to a tax concept. | Primary |
| SFS-P2 | A Form 1099-INT box-1 family and the full taxable-interest concept are either explicitly distinct families/subtotals or proven coextensive before closure may authorize a Form 1040 line-2b zero. | Tightly dependent secondary |

No coverage storage, UI wording system, full interest taxonomy, or production
content enters this topic.

## Gate 1 — Eligibility

Axes 0–2: blast radius 2; migration cost 1; residual paper uncertainty 2;
inability to test cheaply during implementation 1; total **6**. Prototype-
eligible, but paper is expected to suffice. The uncertainty increased after two
clean-room designs failed the same family/claim alignment attack.

## Gate 2 — Paper evidence

Each rival must resolve the same synthetic cases:

1. no forms and no interest;
2. two box-1 statements from one payer;
3. taxable interest received without Form 1099-INT;
4. Form 1099-INT box 3 Treasury interest alongside box 1;
5. a late statement discovered after closure and prior zero publication;
6. closure of a document family while a broader taxable-interest family remains
   open.

For each design: two positives, at least two negatives, one closure-correction
lifecycle, and claim → member universe → mapping → calculation → coverage →
failure map. Every term must be ordinary-language recoverable. **If paper makes
the universes extensionally clear, stop at paper.**

## Gate 3 — Evidence depth per question

Authorized level: static examples only. SFS-P1 and SFS-P2 are evaluated
separately even when carried in one iteration. A climb is justified only if a
paper design cannot determine whether a narrow closed subtotal can compose into
a broader still-open result without falsely publishing zero. The next level
would be a tiny resolver table, not a calculation engine.

## Gate 4 — Cost caps

- Two paper builders: incumbent plus clean-room rival.
- No repair pass pre-authorized; foreman may authorize one bounded pass under
  the owner's standing progression delegation only after logged triage.
- Two Medium/medium reviewers by default. No expressiveness seat unless code is
  authorized.
- Charter ≤ 100 lines; examination/review ≤ 120 lines; total topic Markdown
  target ≤ 900 lines.

## Gate 5 — Triage

Foreman classifies every finding. Only alignment among claim, member universe,
mapping, calculation, and coverage is decision-blocking. UI copy, extra boxes,
manual-entry product design, and complete interest taxonomy are separate or
deferred decisions, not charter expansion.

## Gate 6 — Minimum converged subset

The floor is SFS-P1: a precise family/closure semantic contract that prevents a
narrow document closure from authorizing a broader tax-concept zero. SFS-P2 may
settle only the box-1/line-2b relationship and explicitly defer other interest
families.

## Gate 7 — Production boundary

Only documents merge. Accepted semantics become a separate Tier-2 ADR and are
then instantiated in the Source Completeness milestone plan. Prototype labels,
ids, and examples are not production content.

## Gate 8 — Roles

| Role | Tier | Reason |
|---|---|---|
| Foreman | High/high | Semantic triage and partial-ratification judgment |
| Incumbent builder | High/high | First synthesis across tax/document universes |
| Rival builder | High/high | Independent semantic alternative |
| Governance reviewer | Medium/medium | Bounded Articles 1/7/11 and ADR-0014 fidelity |
| Adversary reviewer | Medium/medium | Counterexamples to universe alignment |

Reviewers are owner-launched unless the owner later directs foreman spawning.

## Review measurements

Governance checks that each family is declared, closure remains determinable and
affirmative-only, and no consumer silently changes the universe. Adversary
substitutes non-form interest, other boxes, late statements, and narrow-closed/
broad-open cases. Failure is any zero or coverage-complete result whose claim
universe is broader than its authority.

## Data safety

All payers, statements, amounts, and labels are synthetic and visibly non-real.
