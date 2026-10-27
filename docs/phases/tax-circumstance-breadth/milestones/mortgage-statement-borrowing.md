<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Circumstance Breadth",
  "topic": "mortgage-statement-borrowing",
  "status": "Publication candidate reconstructed on the milestone branch. Independent publication review and CI remain pending. ADR-0080 is owner-approved.",
  "scope": [
    "one continuing original borrowing for one main home, described by one or two 2025 Forms 1098",
    "exact report relationships, separately scoped ordinary answers, supported calculation and saved explanation"
  ],
  "non_goals": [
    "no refinancing, second-home, mixed-use, partial-payment or above-limit allocation calculator",
    "no automatic loan matching, copied shared answers, general assumption framework or complete filing claim"
  ],
  "deep_reads": {
    "review": [
      "docs/process/planning-and-development.md",
      "docs/phases/tax-circumstance-breadth/milestones/mortgage-statement-borrowing.md#What we are trying to accomplish",
      "docs/phases/tax-circumstance-breadth/milestones/mortgage-statement-borrowing.md#Selected product contract",
      "docs/phases/tax-circumstance-breadth/milestones/mortgage-statement-borrowing.md#Publication gates"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/tax-circumstance-breadth/milestones/mortgage-statement-borrowing.md#What we are trying to accomplish",
      "docs/phases/tax-circumstance-breadth/milestones/mortgage-statement-borrowing.md#Selected product contract",
      "docs/phases/tax-circumstance-breadth/milestones/mortgage-statement-borrowing.md#Publication gates"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-10-25-mortgage-statement-borrowing.md",
      "docs/phases/tax-circumstance-breadth/milestones/mortgage-statement-borrowing.md",
      "docs/phases/tax-circumstance-breadth/tax-circumstance-breadth-roadmap.md"
    ]
  },
  "retrospective": "docs/milestone-retrospectives/2026-10-25-mortgage-statement-borrowing.md"
}
-->

# One Home Loan, More Than One Interest Statement

Milestone key: `mortgage-statement-borrowing`.
Primary branch: `milestone/mortgage-statement-borrowing-same-loan`.
Publication candidate prepared for independent review and CI; not yet ready
to merge.

## What we are trying to accomplish

A person may receive two mortgage-interest statements for one continuing home
loan, for example after the company collecting payments changes. Keep both
forms, help the person identify what each describes, and calculate and explain
only the supported interest amount. Linking forms must not turn them into two
borrowings or erase their separate amounts, observations or correction
histories.

This route covers one continuing original borrowing for one main home and one
or two explicitly linked 2025 Forms 1098. It does not establish general
multiple-mortgage support.

## Selected product contract

### Reports, borrowing and payments

- Preserve each form's payer, statement and year identity, Box 1 interest,
  Box 2 dated principal observation and Box 3 origination date. Equal amounts
  or similar labels do not establish a common borrowing.
- A mortgage-specific opaque reference identifies the borrowing. The person
  explicitly recognizes it and records an affirmed, denied, cannot-tell or
  withdrawn outcome for each exact report/borrowing pair.
- Recognition that both reports concern one borrowing is separate from whether
  their interest payments overlap. For each linked report, ask whether **all**
  of its payments are separate from the payments on the other linked report,
  or whether it is a copy/correction, or the person cannot tell. Only current
  `different-payments` support on every linked report permits combining Box 1.
  Missing, unusable, uncertain or withdrawn support withholds the sum;
  copy/correction directs correction of the existing report, not addition.
  Equal amounts alone prove neither copying nor distinct payments.
- A confirmation is about its exact named report pair and their current source
  and link support. Changing either report, source or link requires fresh
  support; a new pair cannot inherit the old answer. An unchanged A/B pair may
  retain its ordinary confirmations after a temporary third C is added and
  removed. While C is present, the one-or-two-report calculation is withheld;
  the old derived result does not revive, and a current reclose/rerun is
  required.

### Answers and scope

- Nine existing ordinary answers remain report-local. Five separate
  propositions may be explicitly shared at borrowing/year scope: who owes the
  loan, whether anyone outside the joint-filing spouses also owes it, use of
  proceeds, original-versus-refinance, and receipt of a mortgage credit
  certificate. Shared answers are never inferred from matching local answers.
- Once reports are linked, review offers the five propositions at borrowing
  scope and shows prior locals for confirmation or correction rather than
  collecting both scopes independently. Payment, ownership, home and
  collateral circumstances remain local. Continuing-borrowing recognition
  does not decide whether the loan is original or refinanced.
- Shared/local disagreement does not select favorable support. Shared
  uncertainty cannot fall through to a favorable local answer. Independently
  scoped local support may remain usable after shared support is withdrawn.
- The annual balance input is a person-confirmed upper bound on the highest
  balance during 2025, not an exact maximum or an average. Box 2 observations
  remain separate and cannot supply that bound. The other-debt answer is about
  secured debt on either home besides this named borrowing and cannot authorize
  another borrowing.

### Calculation and coverage

- The connected calculation requires complete current report coverage and one
  common recognized borrowing. It supports at most two reports. A third
  report, unresolved or denied links, affirmative orphans, or another active
  borrowing cannot yield a favorable partial sum.
- Each Box 2 must fit under the annual ceiling, which must fit the conservative
  $750,000 limit ($375,000 for married filing separately). A loose bound above
  the limit withholds support; it does not establish actual excess. Linked
  Box 3 dates must agree; disagreement is not a choice between dates.
  Origination on or before 1987-10-13 and the higher grandfathered $1 million
  limit are outside this calculation.
- Actual local answers and applicable shared support determine each report's
  reason. Recognition, linking and a ceiling alone establish no deduction.
  Additional secured debt or unsupported circumstances withhold this route;
  they do not establish legal nondeductibility.
- One family-authorized line8a producer combines supported Box 1 amounts once.
  Schedule A and line12e use that selected result and retain their own
  prerequisites. Genuine closed-empty makes line8a inapplicable and the
  separate Schedule A total zero; missing closure is not closed-empty. An
  affirmative orphan still blocks integrity beside a zero result.
- A blocked amount is not zero, and ordinary answers cannot bypass missing
  applicability. System-unusable comparison context remains distinct from a
  person's cannot-tell answer. Current result dependencies include the report,
  source, link and answer support actually consumed.

### Changes, exit and history

- Local correction changes that report; shared correction changes that
  borrowing/year. Neither changes an unrelated account or relabels a source.
- Withdrawal ends selected support. Clear ends current recognition, report
  links, payment comparisons, five shared answers and the annual ceiling. It
  preserves forms, local answers, entities, evidence and history, plus the
  independently scoped other-debt answer. Clear is not deletion. One remaining
  independent form may use its actual legacy route; two forms do not become a
  supported singleton.
- Late membership advances the family horizon and invalidates prior closure.
  Reclose and rerun against current membership; do not reuse an old subtotal.
- Owner-approved ADR 0080 permits a fresh finding for an exact removed member
  only through the removing horizon's valid descendant lineage. Old findings,
  calculations and closure do not revive. Historical unrelated-chain re-adds
  remain readable but non-current; unsupported attempts refuse atomically.
  Restoration is not general undo or migration of saved outputs.
- Saved files remain unchanged after correction. Saved-run association marks
  recalculation needed rather than treating history as today's calculation.

## Adversarial design closure

Before production, the connected design closed the following boundaries:

| Question | Selected boundary |
| --- | --- |
| Whose answer, about what and when? | Exact report, borrowing/year and report-pair scopes; correction and clear isolation. |
| Empty, missing or incomplete? | Closed-empty, unresolved coverage and affirmative-orphan refusal remain distinct. |
| What changes after a late form? | New membership invalidates closure and old derived results; only a current reclose/rerun may publish. |
| What may be reused? | Explicit shared statements and declared dependencies, not copied answers or a tax-specific admission list. |
| What reaches the return and reader? | One line8a producer, retained Schedule A/line12e prerequisites and a saved explanation of current support. |
| What stays outside? | Allocation, refinancing, another borrowing/home, the higher grandfathered limit, a third report and general undo/assumption machinery. |

The repaired candidate uses actual recorders, coordinator outputs, currentness
checks and reloaded saved explanations. Interim feasibility notes are not
production evidence. Final publication review and exact-head CI remain open.

## Interaction and explanation

Finite review snapshots show recognizable forms, borrowing, answer scope,
offered choices and unanswered numeric inputs. Save, correct, withdraw and
clear revalidate displayed scope, current answers and revision before writes.
No free-text interpreter or automatic matcher is added.

The saved explanation retains the two forms, observations, applicable and
unusable answers, findings, dispositions, pins and resolved content. It
distinguishes available support from support actually consumed. Projection and
rendering perform no tax math; only a finite publication supplies a number.
A local/shared conflict names both scoped answers, values and finding
identities and offers a correction path without deciding which account is
true. Product and evaluation pages share the validation/render path. Bounded
Node checks and pytest parity cover it; browser appearance has not been
observed.

## Production sequence

1. **Recording:** borrowing reference, exact report links, local/shared answers,
   comparison answers, correction, withdrawal and clear.
2. **Calculation:** declared keyed support, coverage barriers, one line8a
   producer, Schedule A/line12e and saved calculation chain.
3. **Reader:** finite revision-checked operations and actual saved support.
4. **Restoration:** source-family member restoration through a narrow successor
   contract, without changing mortgage tax scope.
5. **Publication:** reconstruct the reviewed product on the ratified base with
   unused generated versions and preserved bytes.
6. **Closeout:** independent candidate review and exact-head CI remain
   required; the owner merges.

## Publication gates

The ratified base includes PR #225; its core v56, registry v54 and release v54
are preserved byte-for-byte, including unrelated return and credit
selections. The mortgage additions use core v57, registry v55 and release v55.
The generated chain is reproducible from committed base artifacts and an
explicit mortgage delta; it does not depend on temporary Git history and
refuses existing output targets. No published schema or content version is
overwritten.

ADR 0080 is owner-approved. Existing expressions and dependency guards express
source availability, effective answers, report coverage, ceiling selection
and Schedule A completion as actual reads. Focused tests check intermediate
currentness as well as final amounts, correction/withdrawal, exact-source
recovery, unchanged-pair behavior, singleton behavior and preservation of
unrelated credit calculations.

The publication candidate remains in progress. Final independent publication
review, changed-base verification and exact-head CI are pending. Focused passes
do not substitute for CI. The numeric Box 11 acquisition-date model remains a
separate known limitation and is not repaired here.

## Planning sources

- [Mortgage circumstances retrospective](../../../milestone-retrospectives/2026-10-15-mortgage-interest-circumstances.md)
  and [multiple-statement retrospective](../../../milestone-retrospectives/2026-10-19-multiple-statement-circumstances.md).
- [2025 Publication 936](https://www.irs.gov/pub/irs-prior/p936--2025.pdf)
  and [2025 Form 1098 instructions](https://www.irs.gov/pub/irs-prior/i1098--2025.pdf)
  are the source authorities for interest/debt coverage and the distinct
  meanings of interest, principal and origination observations.
- Accepted ADRs 0076/0077 govern declared per-subject composition and ADR 0079
  family-version handover; accepted ADR 0080 governs exact-source restoration.
