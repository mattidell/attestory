<!-- foreman-context-v1
{
  "version": 1,
  "topic": "f1098e-student-loan-interest-line21",
  "milestone_state": "track-0",
  "retrospective": null,
  "status": "**ENGINE BREADTH / 2025 FORM 1098-E STUDENT-LOAN INTEREST THROUGH SCHEDULE 1 LINE 21 AND FORM 1040 AGI \u2014 TRACK 0 REOPENED.** The Track 0 settled declaration is WITHDRAWN. Owner review returned three findings, all accepted: (F1, P1) sixteen of the seventeen eligibility components are statement-set-dependent but keyed by tax-year alone, so a late statement is silently authorized by an attestation never made about it; (F2, P1) a closed-empty 1098-E family lets B1 not-claimed-as-dependent block line 21, line 26, line 10 and therefore AGI, which is semantically wrong; (F3, P2) the T0-5 reuse of the twelve ss-benefits-scope Schedule 1 absences was priced against an unratified PR #163 that has now merged, and the reused facts declare Social Security Benefits Worksheet scope in their own titles, so reuse fails the claim-reuse proof on declared authority scope. Pricing: F1 does NOT fire the stop condition \u2014 the identity-key vocabulary already admits {kind: entity, name: family-horizon} and the ratified line uses it 37 times on every *.source-closure fact type, so horizon-binding substantive declarations is content-level reuse needing no evaluator change and no ADR; the alternative (per-statement authority plus a real aggregate) WOULD need new substrate, since the evaluator has no categorical or boolean aggregate at all. F2 resolves to a closed-empty canonical-zero branch carrying closure and C2 provenance, and exposes a second correction: B1=no is a legal zero, not an unsupported block, so every component must be decided individually. F3 blast radius is three files (ss-benefits-scope.bundle.json, rule.ss-benefits-worksheet.json, tests/test_ssa1099_benefits_line6_track2.py); disposition is a shared return-level successor with the SSA-scoped originals superseded, a bridging rule being rejected as repairing upstream scope with a downstream note. Track 0c is chartered with five work items T0c-1..T0c-5 and five now-mandatory Track 0 outputs (authority-lifecycle table, empty/nonempty authority matrix, late-authority counterexample walk, claim-reuse proof, neighboring-capability dependency diff) plus a required Track 0 adversarial-closure declaration, currently four FAILs. Standing rule adopted: Track 0 may not be marked settled while it contains a known semantic coupling unless the plan carries a counterexample showing the coupling is correct. INTEGRATION DONE: PR #163 and PR #168 both merged; this branch rebased --onto origin/main from b25562f (the old base was not an ancestor, the mortgage milestone having been curated before merge), nine commits replayed, one docs/phase-state.md conflict resolved; PR #169 retargeted to main. Delta verified: evaluator operator set unchanged, rule.form1040-line11 still a bare AGI passthrough, the twelve absences present and unchanged; but CURRENT_RECORD_SCHEMA advanced to derivation-record.v6 and packages/tax/ssa_benefits.py was substantially reduced. Track 1 is not chartered. No version numbers allocated. The attachment-rule.v5 provenance defect from T0-7 remains open and untouched.",
  "scope": [
    "add a bounded 2025 Form 1098-E student-loan-interest statement family with lender, borrower, account, and tax-year identity, correction, duplicate, and closure behavior",
    "establish component-level taxpayer-side eligibility authority rather than a contributed qualified/deductible conclusion",
    "model the ordinary Student Loan Interest Deduction Worksheet (Schedule 1 line 21) as an auditable derived citizen, including the $2,500 ceiling and the 2025 MAGI phaseout",
    "extend the expression language with the multiply and divide operators the worksheet phaseout requires",
    "publish Schedule 1 line 21 and a composition-complete Schedule 1 Part II line-26 successor",
    "compose Schedule 1 Parts I and II into one attachment citizen without losing the existing Part I unemployment itemization",
    "introduce Form 1040 line 10 and correct the AGI publication to the printed 2025 line-11a/11b structure",
    "carry the result through taxable income, regular tax, package/registry/release/adoption, explanation, citations, and production-shaped presentation",
    "preserve the SSA, unemployment, IRA, interest, dividend, capital-gain, Schedule A, and Schedule D results on the final base"
  ],
  "non_goals": [
    "no education credits, Form 1098-T, tuition-and-fees deduction, or general education-benefit support",
    "no student-loan principal, cancellation or forgiveness of student debt, or employer educational-assistance computation",
    "no qualified-tuition-program, Coverdell, or education-savings-account computation",
    "no loans from related persons or from qualified employer plans (guarded exclusions, not supported cases)",
    "no Publication 970 Worksheet 4-1 foreign or territorial-income variant (Form 2555, Form 4563, excluded Puerto Rico income)",
    "no Schedule 1 Part II adjustment other than line 21 as a computed source",
    "no Form 1040-NR, no married-filing-separately eligibility, no itemized-deduction changes, no state tax treatment",
    "no payments, refund, balance-due, filing, transmission, real-data operation, or UI redesign",
    "no change to the Form 1040 line 12e/13a/13b/14 deduction spine, which the mortgage-interest milestone already repaired"
  ],
  "deep_reads": {
    "paper": [
      "docs/roles/builder.md",
      "docs/adr/0011-tax-fact-identity-and-source-closure.md",
      "docs/adr/0015-1099-int-statement-instance-identity.md",
      "docs/adr/0016-source-family-claim-and-composition.md",
      "docs/adr/0017-recorded-family-horizons-for-closure-freshness.md",
      "docs/adr/0024-conditional-structures-in-the-rule-language.md",
      "docs/adr/0025-expression-language-extensions.md",
      "docs/adr/0032-contribution-boundary.md",
      "docs/adr/0036-schedule-attachment-ontology.md",
      "docs/adr/0037-conditional-multi-dependency-nonpublication.md",
      "docs/adr/0038-qdcg-worksheet-and-declared-absence.md",
      "docs/adr/0055-attachment-completeness-violation-semantics.md",
      "packages/content/tax/2025/rule.ss-benefits-worksheet.json",
      "packages/content/tax/2025/ss-benefits-scope.bundle.json",
      "packages/content/tax/2025/rule.attachment.schedule-1.json",
      "packages/content/tax/2025/schedule1-part1-scope.bundle.json",
      "packages/content/tax/2025/rule.schedule1-line10.json",
      "packages/content/tax/2025/rule.form1040-line11.json",
      "packages/content/tax/2025/rule.form1040-line15.v2.json",
      "packages/content/tax/2025/form1040.line-14.form-field.json",
      "packages/content/tax/2025/family.f1099g-1.json",
      "packages/content/tax/2025/closure-mapping.f1099g-1.json",
      "AGENTS.md#Schema Publication Protocol",
      "AGENTS.md#Data Safety Rules"
    ],
    "implementation": [
      "docs/roles/builder.md",
      "docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-line21.md#Official 2025 paper boundary",
      "docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-line21.md#Proposed contracts (Track 0 must confirm, refine, or replace)",
      "docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-line21.md#Evidence matrix",
      "docs/adr/0015-1099-int-statement-instance-identity.md",
      "docs/adr/0016-source-family-claim-and-composition.md",
      "docs/adr/0017-recorded-family-horizons-for-closure-freshness.md",
      "docs/adr/0020-non-publication-explanation-walking.md",
      "docs/adr/0025-expression-language-extensions.md",
      "docs/adr/0027-adopted-content-manifests.md",
      "docs/adr/0029-citation-resolution-contract.md",
      "docs/adr/0031-real-data-residency-boundary.md",
      "docs/adr/0032-contribution-boundary.md",
      "docs/adr/0033-production-package-resolver.md",
      "docs/adr/0036-schedule-attachment-ontology.md",
      "docs/adr/0046-presentation-surface-contract.md",
      "docs/adr/0055-attachment-completeness-violation-semantics.md",
      "docs/adr/0056-attachment-disposition-visibility.md",
      "packages/content/tax/2025/rule.attachment.schedule-1.json",
      "packages/content/tax/2025/rule.schedule1-line10.json",
      "packages/content/tax/2025/rule.form1040-line9.v7.json",
      "packages/content/tax/2025/rule.form1040-line11.json",
      "packages/content/tax/2025/rule.form1040-line15.v2.json",
      "packages/content/tax/2025/form1040.line-14.form-field.json",
      "packages/content/tax/2025/rule.ss-benefits-worksheet.json",
      "AGENTS.md#Schema Publication Protocol",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "docs/roles/reviewer.md",
      "docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-line21.md#Proposed contracts (Track 0 must confirm, refine, or replace)",
      "docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-line21.md#Evidence matrix",
      "docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-line21.md#Stop conditions",
      "docs/adr/0016-source-family-claim-and-composition.md",
      "docs/adr/0025-expression-language-extensions.md",
      "docs/adr/0032-contribution-boundary.md",
      "docs/adr/0036-schedule-attachment-ontology.md",
      "docs/adr/0046-presentation-surface-contract.md",
      "AGENTS.md#Schema Publication Protocol",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ],
    "merge_or_records": [
      "docs/roles/foreman.md#Standing disciplines",
      "PROJECT_PLANNING.md#Branch, PR, and Merge Protocol",
      "PROJECT_PLANNING.md#Milestone Closeout",
      "PROJECT_PLANNING.md#Owner-directed semantic ledger during final base synchronization"
    ],
    "schema_or_fixture": [
      "AGENTS.md#Schema Publication Protocol",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ]
  },
  "current_role": "Foreman (Track 0 reopened; Track 0c chartered, not yet performed)",
  "current_prompt": "docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-line21.md#Track 0c work items"
}
-->
# Milestone: 2025 Form 1098-E Student-Loan Interest → Schedule 1 Line 21 → Form 1040 Adjusted Gross Income

Audience: Product (planning instrument); Shared (contracts and verification)

Phase: Engine Breadth. Selected by the owner on 2026-08-09. This is a bounded,
independent milestone in a new domain: it is the first **adjustment to income**
the engine has ever computed, and therefore the first work that puts a value on
Form 1040 line 10 and makes adjusted gross income differ from total income.

**State:** planned — Track 0 chartered, not yet performed.

## Objective

Make a narrowly bounded class of 2025 returns containing one or more Forms
1098-E computable through:

1. aggregation of supported Form 1098-E box-1 interest;
2. the ordinary Student Loan Interest Deduction Worksheet;
3. the $2,500 deduction ceiling;
4. the 2025 modified-adjusted-gross-income phaseout;
5. Schedule 1 line 21;
6. Schedule 1 line 26;
7. Form 1040 line 10;
8. the correct 2025 adjusted-gross-income publication (line 11a / line 11b);
9. taxable income and the existing regular-tax path;
10. Schedule 1 attachment disposition composing Parts I and II;
11. package resolution;
12. exact explanation and citation pins; and
13. production-shaped presentation.

The engine **must calculate** the allowable deduction. It must not accept
contributed conclusions such as "qualified student loan", "eligible student",
"eligible taxpayer", modified AGI, or final deductible interest without
component authority.

## Preconditions and workspace discipline

Observed at plan time by the foreman, reconciled against Git:

| Check | Result |
| --- | --- |
| `git fetch origin --prune` | Done |
| Foreman re-entry capsule | `python3 tools/foreman_context.py --ref HEAD --format markdown` run and reconciled; capsule pointed at the *mortgage-interest* milestone, a different milestone |
| Ratified line (derived) | `origin/main` @ `9cecf30` (PR #162, IRA line 4b) |
| Open milestone PRs at plan time | **#163** SSA-1099 lines 6a/6b (draft); **#168** Form 1098 mortgage interest line 12e (draft). Both expected to merge when complete. |
| Merged and reachable from `origin/main` | #164 (1099-INT box 8), #166 (1099-G box 1 / Schedule 1), #167 (1099-DIV box 7 direct FTC) |
| **Planning base (owner-selected)** | `milestone/f1098-mortgage-interest-line12e` @ **`b25562f`** — "track-2: line-12e succession, Schedule A attachment, package v29, evidence" |
| Why this base | The owner selected it so that schema, package, and registry allocation sees the true highest allocated version numbers across the SSA-1099 and mortgage-interest milestones. It is **not** a claim that either milestone is ratified. |
| Worktree | New and clean, sibling to the primary checkout, on `milestone/f1098e-student-loan-interest-line21`, cut from `b25562f` |
| Worktrees NOT touched | `engine-4` (mortgage-interest WIP), `claude-ssa1099-line6`, `finances-engine*`, and every `.codex/worktrees/*` tree |
| Dispatch | **Not authorized and not requested.** Every track runs owner-launched. |

### Ancestry the base carries

`b25562f` is `origin/main` @ `9cecf30` **plus** two unratified milestones:

- SSA-1099 lines 6a/6b (10 commits, PR #163) — contributes the Social Security
  Benefits Worksheet, the `ss-benefits-scope` absence vocabulary, and line-9 v5–v7;
- Form 1098 mortgage interest line 12e (6 commits, PR #168) — contributes the
  Schedule A attachment citizen, `form1040.line-12e`, the `count` and `block`
  operators, and `rule-artifact.v4`.

This milestone therefore **depends on both landing**. See
"Dependencies and integration order".

## Current inventory at the planning base

### Form 1040 line 10 — absent

There is no `tax.us.2025.form1040.line-10` form-field, rule, citation, or
symbol. Nothing anywhere in `packages/content/tax/2025/` references Schedule 1
line 26. Adjustments to income do not exist in the engine.

### Form 1040 line 11 — present but does not match the printed 2025 form

`rule.form1040-line11.json` (v1, `rule-artifact.v2`):

```json
"requires": ["tax.us.2025.income.total-income"],
"value": { "op": "ref", "name": "tax.us.2025.income.total-income" },
"publishes": "tax.us.2025.income.agi"
```

AGI is a **bare passthrough of total income**. `form1040.line-11.form-field.json`
declares `"line": "11"`.

The printed 2025 Form 1040 has no line "11". It has:

- **line 11a** (page 1): "Subtract line 10 from line 9. This is your adjusted gross income"
- **line 11b** (page 2): "Amount from line 11a (adjusted gross income)"

and `rule.form1040-line15.v2` subtracts `deductions.line-14` from `income.agi`,
whereas the printed line 15 reads "Subtract line 14 from line **11b**".

**Owner disposition (2026-08-09):** repair narrowly — introduce line 10, line
11a, and line 11b in this milestone.

### Form 1040 lines 12e–15 — already repaired by the mortgage-interest milestone

The base carries a corrected deduction spine. This was verified in the base
worktree, not assumed:

| Printed 2025 line | Engine at base | Status |
| --- | --- | --- |
| 12e Standard deduction or itemized deductions | `form1040.line-12e.form-field.json`, `rule.form1040-line12e.json` | Present |
| 13a QBI deduction (Form 8995/8995-A) | `form1040.line-13a.form-field.json`, `citation.form1040.line-13a.json` | Present |
| 13b Additional deductions from Schedule 1-A, line 38 | `form1040.line-13b.form-field.json`, `citation.form1040.line-13b.json` | Present |
| 14 Add lines 12e, 13a, and 13b | `form1040.line-14.form-field.json`, `rule.form1040-line14.json` | Present |
| 15 Subtract line 14 from line 11b | `rule.form1040-line15.v2.json` (`rule-artifact.v4`) — `requires` `income.agi` and `deductions.line-14` | Present; consumes the real line-14 combine |

**Consequence for this milestone.** The deduction side of the spine is correct.
The **only** remaining spine gap is the income side: line 10 does not exist and
AGI is a passthrough on a line number the form does not have. That is exactly
this milestone's job, and nothing else needs repairing to do it. Line-15 v2
already consumes `tax.us.2025.income.agi`, so re-pointing it at line 11b is a
naming and citation question, not a structural one.

### Schedule 1 — Part I only

| Artifact | Version | Notes |
| --- | --- | --- |
| `rule.attachment.schedule-1.json` | v1, `attachment-rule.v4` | One itemization: `line-7-unemployment`, from the closed `f1099g.1` family. Requirement trigger is `strictly_greater_than` zero on the box-1 subtotal. Completeness is ten `check: "value"` answers against `schedule1-part1-scope.*`. Title states explicitly: "**Part II adjustments are out of scope.**" |
| `rule.schedule1-line10.json` | v1, `rule-artifact.v3` | Line 10 = closed unemployment subtotal, gated on `require_closed` plus ten categorical absence checks |
| `schedule1-part1-scope.bundle.json` | v1, `bundle.v2` | Ten Part I / Form 1099-G residual absence fact types, domain `{yes,no}`, no default, free supersession |

There is **no Part II, no line 26, and no Part II completeness vocabulary.**
Part II is genuinely new substrate for the Schedule 1 attachment citizen.

### MAGI component vocabulary — already exists, under another name

The SSA-1099 milestone introduced `ss-benefits-scope.bundle.json` (v1,
`bundle.v2`, 23 fact types). Twelve of them are exactly the Schedule 1
adjustment lines the Student Loan Interest Deduction Worksheet subtracts:

```
no-sch1-line11-educator          no-sch1-line17-se-health
no-sch1-line12-business-expenses no-sch1-line18-penalty
no-sch1-line13-hsa               no-sch1-line19-alimony-paid
no-sch1-line14-moving            no-sch1-line20-ira-deduction
no-sch1-line15-deductible-se     no-sch1-line23-archer-msa
no-sch1-line16-se-retirement     no-sch1-line25-other-adjustments
```

It also carries `no-form-2555`, `no-form-4563`,
`no-puerto-rico-or-samoa-income`, and `no-schedule1-line24z-writein` — which
are precisely the conditions that force Publication 970 Worksheet 4-1 instead
of the ordinary worksheet.

**This is the milestone's single most important reuse-versus-mint decision**
and Track 0 must settle it. See SLI-C5.

### Expression language

Operators available at the base:

```
ref  collect  count  block  parameter  add  subtract  max  compare
all  any  not  choose  round  range_lookup  bracket_fold
require_closed  categorical_compare  category_literal
conditional_dependency_set
```

There is **no `multiply` and no `divide`.** Worksheet line 7 divides by
$15,000/$30,000; worksheet line 8 multiplies line 1 by line 7. Neither is
expressible today. `count` and `block` were added by the mortgage-interest
milestone, so operator extension has recent precedent, and ADR-0025
("Expression language extensions") is the established contract shape.

### Worksheet precedent

`rule.ss-benefits-worksheet.json` (from the SSA milestone) is the closest
precedent: a single rule citizen that folds a multi-step printed worksheet into
one declared expression, `requires` every component including declared-absence
facts, and blocks by naming every missing member. ADR-0038 (QDCG worksheet) and
ADR-0060 (Capital Loss Carryover Worksheet) are the accepted contracts for
"printed worksheet as declared rule content".

**Content-level reuse is therefore expected. No new worksheet substrate.**

### Package, registry, release, adoption at the base

| Layer | Tip at `b25562f` |
| --- | --- |
| Core package | `package.core-calculations.v29.json` |
| Published registry | `published-packages.v24.json` |
| Rule-artifact schema | through `rule-artifact.v4` |
| Attachment-rule schema | through `attachment-rule.v6` |
| Form-field schema | through `form-field.v3` |
| Fact-type schema | through `fact-type.v3` |
| Line-9 rule | `rule.form1040-line9.v7.json` |

**No version numbers are allocated by this plan.** Per owner direction,
allocation happens only after the final integration base is known — that is,
after PR #163 and PR #168 have merged and this branch has been rebased onto the
resulting ratified line.

## Official 2025 paper boundary

Grounded in current official sources, fetched and text-extracted 2026-08-09:

| Source | URL | What it settles |
| --- | --- | --- |
| 2025 Form 1040 (Created 9/5/25) | https://www.irs.gov/pub/irs-pdf/f1040.pdf | Line 10 = "Adjustments to income from Schedule 1, line 26"; line **11a** = "Subtract line 10 from line 9. This is your adjusted gross income"; line **11b** = "Amount from line 11a"; line 15 = "Subtract line 14 from line **11b**" |
| 2025 Schedule 1 | https://www.irs.gov/pub/irs-pdf/f1040s1.pdf | Part II lines 11–25; line 21 = "Student loan interest deduction"; line 22 = "Reserved for future use"; line **26** = "Add lines 11 through 23 **and 25**" |
| 2025 Form 1040 instructions | https://www.irs.gov/instructions/i1040gi | Schedule 1 line 21 eligibility conditions; the Exception; the Student Loan Interest Deduction Worksheet (p. 98) |
| 2025 Publication 970 | https://www.irs.gov/publications/p970 | $2,500 maximum; phaseout $85,000–$100,000 (single/HOH/QSS) and $170,000–$200,000 (MFJ); qualified student loan and eligible student definitions |
| 2025 Form 1098-E | https://www.irs.gov/pub/irs-prior/f1098e--2025.pdf | Complete field inventory (below) |
| About Form 1098-E | https://www.irs.gov/forms-pubs/about-form-1098-e | Lender reporting threshold and scope |

### The ordinary worksheet, verbatim structure (i1040gi p. 98)

> **Student Loan Interest Deduction Worksheet—Schedule 1, Line 21**
>
> *Before you begin:* If the instructions for Schedule 1, line 24z, have you
> enter a write-in adjustment on line 24z, figure that write-in before
> completing this worksheet. Be sure you have read the Exception in the
> instructions for this line to see if you can use this worksheet instead of
> Pub. 970 to figure your deduction.
>
> 1. Enter the total interest you paid in 2025 on qualified student loans.
>    **Don't enter more than $2,500.**
> 2. Enter the amount from Form 1040 or 1040-SR, **line 9**.
> 3. Enter the total of the amounts from **Schedule 1, lines 11 through 20, and 23 and 25**.
> 4. Subtract line 3 from line 2.
> 5. Enter the amount shown below for your filing status.
>    Single, head of household, or qualifying surviving spouse — **$85,000**;
>    Married filing jointly — **$170,000**.
> 6. Is the amount on line 4 more than the amount on line 5?
>    **No.** Skip lines 6 and 7, enter -0- on line 8, and go to line 9.
>    **Yes.** Subtract line 5 from line 4.
> 7. Divide line 6 by **$15,000 ($30,000 if married filing jointly)**. Enter the
>    result as a decimal (**rounded to at least three places**). If the result is
>    **1.000 or more, enter 1.000**.
> 8. Multiply line 1 by line 7.
> 9. **Student loan interest deduction.** Subtract line 8 from line 1. Enter the
>    result here and on Schedule 1, line 21. Don't include this amount in
>    figuring any other deduction on your return.

Three facts about this worksheet matter structurally:

1. **Worksheet line 3 is `lines 11 through 20, and 23 and 25`.** Line 21 is not
   in its own MAGI base, and neither is line 22 (reserved). Schedule 1 line 26
   is `lines 11 through 23 and 25` — the same set **plus** line 21. The engine
   must not build the worksheet's line 3 out of line 26.
2. **The $2,500 cap is applied at worksheet line 1, before the phaseout**, not
   after. The phaseout multiplies the *capped* amount.
3. **The rounding instruction is on the decimal at line 7, not on the result.**
   "At least three places" is a floor on precision, not an instruction to round
   to exactly three. Track 0 must settle the exact convention and pin it.

### Line 21 eligibility conditions (i1040gi p. 97)

> You can take this deduction only if **all** of the following apply.
> - You paid interest in 2025 on a qualified student loan.
> - Your filing status is any status **except married filing separately**.
> - Your modified AGI is less than $100,000 (single, HOH, QSS) or $200,000 (MFJ).
> - You, or your spouse if filing jointly, **aren't claimed as a dependent** on
>   someone else's 2025 tax return.
>
> Don't include any amount paid from a distribution of earnings made from a
> **qualified tuition program (QTP)** after 2018 to the extent the earnings are
> treated as tax free because they were used to pay student loan interest.
>
> **Exception.** Use Pub. 970 instead of the worksheet in these instructions if
> you file **Form 2555 or 4563**, or you **exclude income from sources within
> Puerto Rico**.
>
> **Qualified student loan.** A loan you took out to pay the qualified higher
> education expenses for … yourself or your spouse; any person who was your
> dependent when the loan was taken out; [or a person you could have claimed].
> However, a loan **isn't** a qualified student loan if (a) any of the proceeds
> were used for other purposes, or (b) the loan was from either a **related
> person** or a person who borrowed the proceeds under a **qualified employer
> plan**.

### Form 1098-E field inventory (2025 form, verbatim)

| Field | Classification (proposed; Track 0 confirms) | Reason |
| --- | --- | --- |
| **VOID** checkbox | **Guarded exclusion** | A voided statement is not a member; must not be silently absorbed |
| **CORRECTED** checkbox | **Required authority** | Drives correction/supersession lifecycle, per ADR-0015/ADR-0041 |
| RECIPIENT'S/LENDER'S name | **Required authority** (identity) | Lender identity component |
| RECIPIENT'S/LENDER'S street address, city, state, country, ZIP | Irrelevant to the bounded federal computation | Contact detail; no federal computational consequence and no identity role once TIN is present |
| RECIPIENT'S/LENDER'S telephone number | Irrelevant | Contact detail |
| **RECIPIENT'S TIN** | **Required authority** (identity) | Lender identity discriminator; distinguishes two lenders with similar names |
| **BORROWER'S TIN** | **Required authority** (identity) | Establishes that the taxpayer is the borrower on the statement |
| **BORROWER'S name** | **Required authority** (identity) | Borrower identity component |
| Borrower street address, city, state, country, ZIP | Irrelevant | Contact detail |
| **Account number** | **Required authority — conditionally mandatory** | Per the general instructions the account number is required when a filer has multiple accounts for a recipient. Track 0 must decide whether it is *unconditionally* required for identity when one lender issues multiple statements. See SLI-C1. |
| **Box 1 — Student loan interest received by lender** | **Required authority** (the only amount) | The sole computed input |
| **Box 2 — "Check if box 1 does not include loan origination fees and/or capitalized interest, and the loan was made before September 1, 2004"** | **Guarded exclusion** | Checked means box 1 is *knowingly incomplete*; the taxpayer may have additional deductible interest the engine cannot see. **Must block.** |
| (Form-level) tax year `2025` | **Required authority** (identity) | Year discriminator |

**Note on box 2 semantics.** Box 2 checked is not a statement about the
taxpayer's eligibility; it is the lender declaring that box 1 understates
deductible interest. That is why the narrow default requires box 2 **unchecked**
— unchecked means box 1 is the complete reported figure.

## Proposed supported class

Ground and refine during Track 0. Begin with taxpayers who:

- received one or more 2025 Forms 1098-E;
- are the borrowers identified on the statements;
- were legally obligated to pay the interest;
- actually paid the reported interest during 2025;
- incurred each loan solely to pay qualified higher-education expenses;
- incurred those expenses for the taxpayer, spouse, or a person who was the
  taxpayer's dependent when the loan was incurred;
- used the expenses for an eligible student enrolled at least half-time in a
  program leading to a degree, certificate, or other recognized educational
  credential;
- used an eligible educational institution;
- are **not** married filing separately;
- cannot be claimed as a dependent on another taxpayer's return;
- received no employer-paid educational assistance covering the claimed interest;
- used no tax-free QTP distribution to pay the claimed interest;
- claim no duplicate deduction or other tax benefit for the same interest;
- have no deductible student-loan interest outside Form 1098-E box 1;
- have no Form 2555, Form 4563, excluded Puerto Rico income, or other condition
  requiring Publication 970 Worksheet 4-1;
- have all other Schedule 1 Part II adjustments either computed or explicitly
  declared absent; and
- have every input to the ordinary worksheet closed.

For the first slice, statements must have **box 2 unchecked** and the taxpayer
must explicitly declare that no unreported pre-September-1-2004 origination fees
or capitalized interest exist.

## Non-goals

Excluded unless Track 0 establishes a smaller coherent inclusion:

- education credits; Form 1098-T; tuition-and-fees deductions;
- student-loan principal; cancellation or forgiveness of student debt;
- employer educational-assistance calculations;
- qualified-tuition-program distribution calculations;
- Coverdell or education-savings-account calculations;
- loans from related persons; qualified employer-plan loans;
- foreign or territorial-income worksheet variants (Pub. 970 Worksheet 4-1);
- Schedule 1 adjustments other than line 21 as computed sources;
- Form 1040-NR; married-filing-separately eligibility; itemized deductions;
- state tax treatment; filing or transmission; general education-benefit support;
- the Form 1040 line 13a/13b/14 spine gap.

## Track 0 charter

**Role:** Builder (paper track). **Author:** one owner-launched agent.
**Deep-reads action:** `paper`. **Output:** a Track 0 settlement section
appended to this plan, committed as one commit, plus any ADR drafts it
concludes are required.

**Posture: paper-first.** Prototype **only** if a genuine architecture choice
survives paper analysis. Do not create a spike merely because this is a new
source and a new worksheet — both have accepted precedent (ADR-0016 for source
families, ADR-0038/ADR-0060 for worksheets-as-rule-content). If you conclude a
prototype is needed, **stop and say so with the specific question it would
answer**; do not build it unasked.

Track 0 must settle the following ten items. For each, produce either a
confirmed contract or an escalation.

### T0-1 — Form 1098-E authority

Confirm, correct, or extend the field inventory above. Classify every field as
required authority, guarded exclusion, or irrelevant-with-a-stated-reason.
Specify the identity keys for borrower, lender/servicer, loan/account, tax year,
statement correction, duplicates, and multiple statements. **Decide whether
account identity is mandatory when a lender issues multiple statements** — and
if so, what happens to a statement that omits it.

### T0-2 — Eligibility authority

Form 1098-E reports interest received by the lender. It proves **none** of the
taxpayer-side conditions. Define component-level authority for: legal obligation
to pay; actual payment; qualified-student-loan status; use of proceeds solely
for qualified higher-education expenses; eligible student; eligible educational
institution; at-least-half-time enrollment; student–taxpayer relationship;
dependent status when the loan was incurred; current-year taxpayer dependency
eligibility; related-party loan exclusion; qualified-employer-plan loan
exclusion; absence of prohibited double benefits.

**Do not collapse these into an unexplained contributed `qualified=yes`** unless
you can demonstrate a precise evidence ceiling and auditable component meaning
for the collapsed assertion. Consolidation is permitted only where the resulting
authority stays precise and auditable; say which bullets you consolidated and
why the meaning survives.

### T0-3 — Reported-interest boundary

Decide whether the first milestone supports only box-1 interest. Explicitly
disposition: payments below the lender reporting threshold; interest from a
lender that failed to issue a statement; pre-September-1-2004 origination fees;
capitalized interest omitted when box 2 is checked; additional qualifying
interest not shown in box 1; multiple statements from one or more lenders.

The narrow default requires box 2 unchecked **and** an explicit declared absence
of deductible unreported interest.

### T0-4 — Student Loan Interest Deduction Worksheet

Model the ordinary worksheet as an auditable derived citizen. Settle:
aggregation of eligible interest; the $2,500 ceiling and the fact that it
applies **before** the phaseout; filing-status eligibility; the MAGI base; the
prescribed Schedule 1 adjustment inputs; the $85,000/$170,000 thresholds; the
$15,000/$30,000 denominator; the "rounded to at least three places" decimal
convention and the 1.000 clamp; final form-level rounding; zero and boundary
behavior; and the exact pin table.

**Expression-language finding to settle:** the base has no `multiply` and no
`divide`. Determine the minimal additive extension (operator names, argument
shapes, `Decimal` semantics, schema successor, `AccessLog` treatment) and
whether it warrants an ADR in the ADR-0025 line. Confirm whether the $2,500
ceiling needs a `min` operator or is expressible with the existing `choose` /
`compare` pair — prefer the existing pair if it reads honestly.

### T0-5 — MAGI completeness

Define an exact component boundary for: Schedule 1 lines 11 through 20; lines 23
and 25; foreign earned-income and housing exclusions; foreign housing deduction;
excluded Puerto Rico income; excluded American Samoa income; and any 2025
write-in adjustment that changes which worksheet must be used.

**Ensure line 21 is not subtracted from its own MAGI base.** Worksheet line 3 is
lines 11–20, 23, 25; Schedule 1 line 26 is lines 11–23 and 25. They are
different sets and must be different expressions.

**Settle the reuse-versus-mint decision** on `ss-benefits-scope.*`. That
vocabulary already carries the twelve Schedule 1 adjustment absences, plus
`no-form-2555`, `no-form-4563`, `no-puerto-rico-or-samoa-income`, and
`no-schedule1-line24z-writein`. Options, with the tradeoff stated:

- **Reuse in place** — one absence vocabulary, one contributed answer per
  concept, no divergence risk; but the fact-type ids are named for the Social
  Security worksheet and their titles describe *that* claim, so a reader of a
  student-loan explanation walk sees SSA-named authority.
- **Mint a parallel `slid-magi-scope` vocabulary** — clean naming and honest
  titles; but the taxpayer must answer the same question twice, and two
  vocabularies can silently disagree.
- **Rename/generalize into a shared `sch1-adjustment-scope` vocabulary** —
  correct long-term shape; but it touches the SSA milestone's content, which is
  unratified and on another branch, so it is a cross-milestone change.

Recommend one and say what it costs. This is the highest-leverage decision in
Track 0.

Unsupported components require **explicit absence authority, not optional
defaults.**

### T0-6 — Schedule 1 Part II completeness

The existing Schedule 1 work covers only Part I income. Define a **separate**
Part II adjustment-completeness boundary. Schedule 1 line 26 must be
composition-complete across every Part II adjustment: the new line-21 deduction
plus every supported or explicitly absent neighboring adjustment (lines 11–20,
23, 25; line 22 is reserved for future use and must be dispositioned as such,
not as an absence answer).

**Do not infer that "no other adjustments" follows from closure of the Form
1098-E family.** Family closure proves the statement set is complete; it proves
nothing about educator expenses or the HSA deduction.

### T0-7 — Schedule 1 attachment disposition

Settle each case:

| Case | Required disposition |
| --- | --- |
| Positive line-21 deduction, no Part I income | Schedule 1 **required** |
| Positive line-21 deduction alongside unemployment or another supported Part I source | **One** composition-complete Schedule 1 carrying both Parts |
| Deduction reduced to zero by the phaseout | Determine whether Schedule 1 is **not required**; justify against the printed form and ADR-0036 |
| Incomplete eligibility or adjustment authority | **Blocked**, never "not required" |
| Closed-empty Form 1098-E family | Line 21 absent/zero under the accepted semantics |
| Other Schedule 1 source or adjustment present but unsupported | **Blocked** |

The existing `rule.attachment.schedule-1` is `attachment-rule.v4` with a single
`strictly_greater_than` threshold trigger on the unemployment subtotal. A
Part II itemization changes the requirement predicate. Determine whether
`attachment-rule.v6` (already available at the base) accommodates a two-part
attachment with two requirement contributors, or whether an additive successor
schema is genuinely needed. **Prefer content-level reuse.**

### T0-8 — Form 1040 succession

Map the result through the actual 2025 form: Schedule 1 line 26 → Form 1040
line 10 → AGI on **line 11a** → carried to **line 11b** → taxable income →
regular tax.

The owner has dispositioned the spine question: **repair 10, 11a, and 11b in
this milestone.** The deduction spine (12e/13a/13b/14/15-v2) is already correct
at the base, so no other spine work is in scope. Settle:

- whether line 11a and line 11b are one symbol with two form-field citizens, or
  two symbols with a carry rule — and which reads honestly in an explanation
  walk. The printed line 11b is a pure carry-forward across the page break, so
  one symbol with two form-field citizens is the foreman's expectation; justify
  whichever you choose;
- what happens to the existing `form1040.line-11` form-field (`"line": "11"`)
  and `rule.form1040-line11` (v1, passthrough). They are published history: a
  successor is additive and the originals are never edited or removed;
- whether `rule.form1040-line15.v2` should be re-pinned from `income.agi` to an
  explicit line-11b symbol, or whether keeping `income.agi` as the single AGI
  symbol (bound by both the 11a and 11b form fields) is the honest shape. Note
  that line-15 v2 already consumes the correct `deductions.line-14`, so this is
  a provenance question, not an arithmetic one;
- the `line` attribute convention: `form1040.line-14.form-field.json` uses
  `"line": "1040-14"` while `form1040.line-12e.form-field.json` uses
  `"line": "12e"`. Pick one and say why; do not introduce a third.

### T0-9 — SSA interaction

The ordinary Social Security Benefits Worksheet subtracts specified Schedule 1
adjustments but **does not** include line 21 in that subtraction.

Confirm on paper and in tests that: student-loan interest reduces AGI; it does
**not** feed back into the supported Social Security taxable-benefits worksheet;
the merged SSA line-9 and downstream successors remain selected; no cycle is
introduced; and SSA, unemployment, IRA, interest, dividend, and capital-gain
components remain present **exactly once**.

Foreman's paper pre-finding, for Track 0 to verify rather than re-derive: the
worksheet's own MAGI subtraction set is lines 11–20, 23, 25 — the same set as
the student-loan worksheet's line 3, and it excludes line 21. `rule.ss-benefits-worksheet.json`
at the base already `requires` exactly that set and never names line 21.
Dependency direction is Schedule 1 line 21 → line 26 → Form 1040 line 10 →
line 11a, while the SS worksheet consumes Form 1040 line 9 and Schedule 1 line 10
(Part I). **No cycle is expected.** Prove it, do not assume it.

### T0-10 — Contract novelty

Determine whether existing statement-family, closure, worksheet, attachment,
rule-language, explanation, and presentation contracts suffice. Prefer
content-level reuse. **Stop and escalate any genuine need to interpret
governance or introduce generic substrate.**

State plainly which new ADRs, if any, this milestone requires. The foreman's
expectation is: **at most one** — an ADR-0025-line expression extension for
`multiply`/`divide` — plus plan-contract sections for everything else.

### Cases requiring explicit disposition

Track 0 must examine at minimum, and record a disposition for, each of:

multiple Forms 1098-E; corrected statements; duplicate statements; box 2
checked; interest paid below the reporting threshold; unreported interest;
capitalized interest; loan-origination fees; loans from related persons; loans
from qualified employer plans; mixed-use loans; refinancing or consolidation
loans; interest paid by someone other than the legally obligated borrower;
interest paid by an employer; interest paid with a tax-free QTP distribution;
married filing separately; taxpayer claimable as another person's dependent;
student who was not a qualifying dependent when the loan was incurred;
less-than-half-time enrollment; non-degree or noncredential study; ineligible
educational institutions; foreign-income or territorial-income modifications;
every MAGI phaseout boundary; any amount claimed under another deduction or
exclusion.

**These are decision targets, not instructions to support every case or to
create one declaration per bullet.** Consolidate only where the resulting
authority remains precise and auditable.

## Proposed contracts (Track 0 must confirm, refine, or replace)

These are the foreman's planning proposals. Track 0 owns them.

### SLI-C1 — Bounded Form 1098-E statement family

An independent 2025 Form 1098-E source family with identity over lender TIN,
borrower TIN, account number, and tax year; `CORRECTED` supersession; duplicate
rejection; late-member and closure behavior on the ADR-0016/ADR-0017 pattern
already used by `family.f1099g-1`. `VOID` and box-2-checked statements are
guarded exclusions that block, not members that are dropped.

### SLI-C2 — Component-level taxpayer eligibility authority

A declared vocabulary of contributed categorical components covering T0-2, with
no single collapsed `qualified` conclusion. Domain `{yes,no}`, no default,
presence-before-value, free supersession — matching the shape of
`schedule1-part1-scope` and `ss-benefits-scope`.

### SLI-C3 — Reported-interest boundary

Only Form 1098-E box-1 interest is deductible in this class. Box 2 checked
blocks. A declared absence of deductible unreported interest is required, and is
not implied by family closure.

### SLI-C4 — Ordinary worksheet as a derived citizen

One rule citizen implementing worksheet lines 1–9, on the
`rule.ss-benefits-worksheet` pattern: `requires` every component, blocks naming
every missing member, no contributed MAGI, no contributed final deduction. Cap
at $2,500 before phaseout. Filing-status-driven thresholds and denominator via
declared parameters, not literals.

### SLI-C5 — MAGI component boundary

MAGI = Form 1040 line 9 − (Schedule 1 lines 11–20, 23, 25), with every
unsupported component carrying explicit absence authority and the Exception
conditions (Form 2555, Form 4563, Puerto Rico) blocking. **Line 21 is excluded
from its own base.** The reuse-versus-mint decision from T0-5 is part of this
contract.

### SLI-C6 — Schedule 1 Part II completeness and line 26

A Part II completeness vocabulary distinct from Part I. Line 26 = lines 11–23
and 25, composition-complete, with line 22 dispositioned as reserved.

### SLI-C7 — One composition-complete Schedule 1

A single Schedule 1 attachment citizen carrying Part I and Part II itemizations
without losing the existing `line-7-unemployment` content, with the requirement
predicate and completeness answers extended per T0-7.

### SLI-C8 — Form 1040 line 10 / 11a / 11b succession

Additive line-10 and line-11a/11b citizens; AGI = line 9 − line 10; the existing
line-11 artifacts preserved as published history; taxable income and regular tax
recomputed through existing machinery.

### SLI-C9 — Expression extension

Additive `multiply` and `divide` operators with `Decimal` semantics, a schema
successor, and `AccessLog` treatment consistent with `round`. ADR in the
ADR-0025 line if Track 0 concludes one is warranted.

### SLI-C10 — Lifecycle, explanation, package, presentation

Correction and duplicate lifecycle; exact citation pins for line 21, line 26,
line 10, line 11a/11b; successor package built from the current selected graph;
production-shaped synthetic fixtures and presentation evidence.

## Dependencies and integration order

This milestone's branch is cut from `b25562f`, which contains two unratified
milestones. Therefore:

1. **PR #163 (SSA-1099 lines 6a/6b) must merge.** It supplies the Social
   Security Benefits Worksheet, the `ss-benefits-scope` vocabulary this
   milestone's MAGI boundary depends on, and line-9 v5–v7.
2. **PR #168 (Form 1098 mortgage interest, line 12e) must merge.** It supplies
   `form1040.line-12e`, the Schedule A attachment citizen, `rule-artifact.v4`,
   and the `count`/`block` operators.
3. **Rebase this milestone onto the resulting ratified line.**
4. **Rebuild all successors and generated publications from that base** —
   packages, registries, releases, adoptions, schema manifests.
5. **Verify the rebased semantic delta** before implementation review or
   publication.

Planning and paper-first Track 0 may proceed now, in parallel, on this base.

**No version numbers are allocated until step 3 completes.** Any number written
before then is a placeholder and must be regenerated.

### Semantic-ledger diagnostic (required, ephemeral)

Per `PROJECT_PLANNING.md#Owner-directed semantic ledger during final base
synchronization`, run the three-way semantic-ledger comparison **twice**: once
around the post-#163/#168 rebase, and once at the final pre-publication rebuild.

Blocking unless explicitly intended and justified in writing:

- lost upstream package members;
- changed selections;
- lost schema admissions;
- changed entrypoints;
- lost composition obligations.

The ledger is a local diagnostic. It is never committed.

## Tracks and independent review structure

| Track | Role | Unit |
| --- | --- | --- |
| **Track 0** | Builder (paper) | Paper eligibility, input authority, worksheet, MAGI completeness, Schedule 1 Part II, Form 1040 succession. Output: settlement section + any ADR draft. **Owner ratifies before Track 1.** |
| **Track 1** | Builder | Form 1098-E family, lifecycle, eligibility components, guards, expression extension, and the deduction worksheet. |
| **Track 2** | Builder | Schedule 1 Part II / line 26, attachment integration, Form 1040 line 10 / 11a / 11b succession, package, explanations, presentation, goldens. |
| **Review gate** | Reviewer | Author-independent review of each implementation track. |

Tracks 1 and 2 **may be combined** if Track 0 establishes that the
implementation remains one independently reviewable verification surface. Do not
split work by file type.

### Commit and PR discipline

One branch, one draft-to-final PR, curated track commits within that PR.

**Do not create separate PRs or permanent commits for:** spikes; provisional
evidence; charter amendments; review findings; repairs; regenerated
version-number corrections; mypy-only fixes; cleanup. Fold incidental fixes into
their owning track commits before final review.

Planned durable commits:

1. `plan: charter Form 1098-E student-loan interest milestone` (this commit)
2. `track-0: paper scope contract settlement` (+ ADR if warranted)
3. `track-1: Form 1098-E family, eligibility components, and deduction worksheet`
4. `track-2: Schedule 1 Part II, Form 1040 line 10/11a/11b, package, presentation`
5. `curate: prepare Form 1098-E milestone for final review`

## Evidence matrix

Focused positive, negative, boundary, and lifecycle cases required for:

| Group | Cases |
| --- | --- |
| Source family | one eligible Form 1098-E; multiple eligible statements; corrected-statement replacement; duplicate handling; late-member behavior; family closure; closed-empty family |
| Ceiling | interest below $2,500; interest exactly $2,500; interest above $2,500 |
| Phaseout | lower boundary (MAGI = $85,000 and $170,000); upper boundary (MAGI = $100,000 and $200,000); a midpoint; fully phased-out deduction; decimal ≥ 1.000 clamp |
| Filing status | single; head of household; qualifying surviving spouse; married filing jointly; **married filing separately blocks** |
| Blocking | taxpayer dependency; box 2 checked; each missing eligibility component; prohibited double benefit; foreign/territorial worksheet variant (Form 2555 / 4563 / Puerto Rico); missing Schedule 1 Part II completeness |
| Structural | line 21 excluded from its own MAGI base |
| Attachment | positive line 21 requires Schedule 1; zero deduction produces the accepted not-required disposition; coexistence with supported Part I unemployment in one Schedule 1 |
| SSA interaction | coexistence with SSA benefits without changing the SSA worksheet result; no cycle; each component present exactly once |
| Exact values | line 21, line 26, Form 1040 line 10, AGI (11a/11b), taxable income, and line 16 recomputation |
| Provenance | exact pins and explanations; package and schema-registry integrity |
| Regression | preservation of all existing regression fixtures |

All fixtures synthetic, `demo.*` / `demo-*` labelled, per `AGENTS.md#Fixture Rules`
and `AGENTS.md#Data Safety Rules`.

## Stop conditions

Stop and escalate to the owner — do not improvise — if any of the following holds.

1. **Governance interpretation.** The unit appears to require interpreting the
   Constitution, Ontology, or Engineering Constraints (`AGENTS.md`, "Stop when
   your unit turns on governance text").
2. **Generic substrate.** Honest implementation appears to require new generic
   substrate rather than content-level reuse — a new attachment ontology, a new
   worksheet mechanism, a new closure mechanism.
3. **Spine scope creep.** The owner scoped this milestone to Form 1040 lines 10,
   11a, and 11b. The deduction spine (12e/13a/13b/14 and line-15 v2) is already
   correct at the base. If honest implementation appears to require changing any
   of it, stop — that is a cross-milestone change to unratified mortgage-interest
   content, not a builder decision.
4. **Collapsed eligibility.** If T0-2 cannot produce component-level authority
   without a single opaque `qualified=yes` assertion, stop and present the
   evidence ceiling rather than shipping the collapse.
5. **Cross-milestone content change.** If T0-5 concludes that the correct answer
   is to rename or generalize `ss-benefits-scope` — content owned by the
   unratified SSA milestone — stop. That is an owner decision about two
   milestones, not one.
6. **Cycle detected.** If Schedule 1 line 21 turns out to feed the Social
   Security Benefits Worksheet, or any other cycle appears, stop.
7. **Semantic-ledger regression.** Any lost upstream member, changed selection,
   lost schema admission, changed entrypoint, or lost composition obligation
   that is not explicitly intended and justified.
8. **Prototype temptation.** If Track 0 believes a prototype is required, stop
   and state the specific architecture question it would answer. Do not build it
   unasked.
9. **Base moved.** If PR #163 or PR #168 changes shape materially, or either is
   abandoned, stop — the dependency chain and version allocation both change.

## Exit criteria

- Track 0 settlement ratified by the owner.
- Tracks 1 and 2 implemented, each with author-independent review.
- Every historical schema, rule, form-field, attachment, and package version
  preserved; all schema-manifest changes additive only.
- Schedule 1 attachment composes Parts I and II without losing prior content.
- SSA, unemployment, IRA, interest, dividend, Schedule A, and Schedule D
  citizens remain selected exactly once.
- Both semantic-ledger runs performed and every finding dispositioned.
- Worktree clean; no spikes, scratch output, superseded charters, transient
  review material, local ledgers, or obsolete generated versions retained.
- Single PR updated; **CI `verify` green on the exact candidate head** as the
  suite gate of record.

## Track 0a settlement — T0-1, T0-2, T0-3, T0-9, T0-10

Author: Track 0a builder (paper), owner-launched, base `eaee81d`.
Unit: charter items **T0-1, T0-2, T0-3, T0-9, T0-10** and the "Cases requiring
explicit disposition" entries falling under them. **T0-4 through T0-8 are not
settled here** and are owned by a separate unit (Track 0b). Where this
settlement constrains that unit, it says so under "Notes addressed to Track 0b"
and decides nothing on its behalf.

Every foreman pre-finding relied on below was verified against primary source or
against repository content at this commit, not inherited.

### Sources used, with exact locations

| Tag | Source | Where |
| --- | --- | --- |
| **[F1098E]** | 2025 Form 1098-E, Student Loan Interest Statement (Cat. No. 25088U) | `irs.gov/pub/irs-prior/f1098e--2025.pdf`, Copy A (PDF p. 2), Copy B (PDF p. 3), Instructions for Borrower (PDF p. 4) |
| **[I1098ET]** | 2025 Instructions for Forms 1098-E and 1098-T (Cat. No. 27990J, Nov 7 2024) | printed pp. 1–2 |
| **[I1040GI]** | 2025 Instructions for Form 1040 (i1040gi) | printed **p. 98** (Schedule 1 line 21 conditions, Exception, "Qualified student loan" 1) and **p. 99** (qualified student loan 2–3, qualified higher education expenses, line 22 reserved, **Student Loan Interest Deduction Worksheet**) |
| **[P970]** | 2025 Publication 970, chapter 4 | printed pp. 30, 31, 32, 33, 34, 35 |
| **[I1099GI]** | 2025 General Instructions for Certain Information Returns | printed p. 11 (part H CORRECTED checkbox / account number on corrections; **part I Void Returns**), printed p. 14 (**part L, Account Number Box**) |
| **[F1040S1]** | 2025 Schedule 1 (Form 1040) | page 2: line 21, line 22 "Reserved for future use", line 26 "Add lines 11 through 23 and 25 … Enter here and on Form 1040, 1040-SR, or 1040-NR, line 10" |

**Charter erratum (page numbers).** The charter attributes the line-21
eligibility conditions to i1040gi p. 97 and the worksheet to p. 98. Verified: the
conditions, the Exception, and the start of "Qualified student loan" are on
**p. 98**; the **Student Loan Interest Deduction Worksheet is on p. 99**, together
with the remainder of the qualified-student-loan definition and the "Line 22 has
been reserved for future use" instruction. Track 0b must pin **p. 99** for the
worksheet. The verbatim worksheet and condition text quoted in the charter is
otherwise accurate word for word.

---

### T0-1 — Form 1098-E authority and identity (settled)

#### Field inventory, confirmed and corrected

The charter's inventory is confirmed as to the field list. Copy A [F1098E p. 2]
carries exactly: VOID, CORRECTED, RECIPIENT'S/LENDER'S name+address+telephone
(one combined box), RECIPIENT'S TIN, BORROWER'S TIN, BORROWER'S name, borrower
street address, borrower city/state/country/ZIP, Account number, box 1, box 2.
There is no other field. Two classifications change.

| Field | Settled classification | Authority and reason |
| --- | --- | --- |
| VOID checkbox | **Guarded exclusion — blocks** | Confirmed, but on a narrower and stronger ground than the charter's. VOID is a **Copy-A-only, pre-submission filer control**: [I1099GI p. 11, part I] "If a completed or partially completed Form … is incorrect and you want to void it **before submission to the IRS** … The return will then be disregarded during processing", and "An 'X' in the 'VOID' box … will **not** correct a previously filed return." Decisively, **Copy B — the borrower's copy — has no VOID box at all** [F1098E p. 3, which carries only "CORRECTED (if checked)"]. A voided statement therefore cannot legitimately reach the taxpayer. A contributed statement bearing VOID is an authority anomaly, not a member and not a droppable duplicate: it blocks. |
| CORRECTED checkbox | **Required authority** | Confirmed. [I1099GI p. 11, part H]: "Enter an 'X' in the 'CORRECTED' checkbox only when correcting a form previously filed with the IRS or furnished to the recipient." Present on Copy B. Drives the ADR-0015 correction/supersession lifecycle. |
| RECIPIENT'S/LENDER'S name | **Required authority (identity)** | Confirmed. [I1098ET p. 2]: the box carries "the name, address, and telephone number of the **filer**". Note the filer is not necessarily the original lender: "If more than one person has a connection with the loan, only the **first person to receive the interest payment** must file … a loan service or collection agent receiving payments on behalf of the lender must file" [I1098ET p. 2]. The identity is therefore the **filer/servicer**, not the beneficial lender. |
| RECIPIENT'S TIN | **Required authority (identity)** | Confirmed. "A recipient's/lender's TIN **may not be truncated** on any form" [I1098ET p. 2], so it is a reliable discriminator. |
| BORROWER'S TIN | **Recorded authority — not an identity key; truncation-tolerant** | **Corrected.** [F1098E p. 4]: "For your protection, this form may show only the last four digits of your TIN". A truncated value cannot serve as an identity key. Its role is admission (see below), not individuation. |
| BORROWER'S name | **Recorded authority — not an identity key** | Same role as borrower TIN: admission, not individuation. |
| Lender/borrower street address, city, state, country, ZIP; lender telephone | **Irrelevant** | No federal computational consequence and no individuating role once the filer TIN and the statement instance exist. |
| **Account number** | **Not required authority; explicitly NOT an identity key** | **Corrected — this is the charter's open question, answered "no".** [I1098ET p. 2] and [I1099GI p. 14, part L]: "The account number is required **if you have multiple accounts for a recipient for whom you are filing more than one** information return of the same type"; otherwise the IRS merely "encourages" it. [F1098E p. 4]: "**May** show an account or other unique number the lender assigned". A lender may lawfully file **one** Form 1098-E covering all of a borrower's loans, or one per loan [I1098ET p. 1]; in the one-statement case the box is routinely blank. Making the account number an identity key would make a fully compliant statement unrecordable. See "Identity" below for what individuates instead. |
| Box 1 | **Required authority (the sole amount)** | Confirmed. [F1098E p. 4]: "Shows the **interest received by the lender** during the year on **one or more** student loans made to you." |
| Box 2 | **Guarded exclusion — blocks (via T0-3)** | Confirmed; semantics restated precisely in T0-3. |
| Form-level tax year 2025 | **Required authority (identity)** | Confirmed. |

#### Identity keys (settled)

Follow ADR-0011 §2–3, ADR-0015 §1–4, and the committed `f1099g-box1.bundle.json`
shape exactly. **No new identity mechanism.**

The box-1 fact is keyed by:

1. `filer` — entity, the Form 1098-E filer/servicer (a new entity kind in the
   `tax.us.*` line, peer to `tax.us.unemployment-payer`);
2. `statement` — entity, **one logical furnished Form 1098-E**, peer to evidence
   (ADR-0015 §2: file, upload, scan, document, and evidence ids are forbidden
   from fact identity);
3. `tax-year` — literal `"2025"`.

Consequences, each grounded:

- **Multiple statements from one filer** are distinct statement-instance
  citizens and therefore distinct facts (ADR-0015 §3). This is the ordinary
  case here, because a filer may issue one form per loan [I1098ET p. 1].
- **Account identity is not mandatory and does not appear in the key.** Two
  statements from one filer are individuated by their statement citizens, not by
  an account string. A statement that omits the account number is recorded
  normally; **nothing happens to it**, because nothing depended on the field.
  This answers T0-1's explicit question. The account number may be echoed as
  evidence detail in presentation; it must never be keyed on, required, or used
  to decide sameness.
- **A corrected statement** (CORRECTED checked) answers the **same** fact for the
  same statement citizen and supersedes its prior finding (ADR-0015 §4, ADR-0032
  §5: correction is supersession, never edit; the family horizon does **not**
  advance on a same-member value correction, ADR-0017 §4, so closure authority
  survives a corrected box-1 amount).
- **Duplicates** — the same physical statement contributed twice — are one
  statement citizen and one fact; the second contribution is a plain re-assertion
  that supersedes. A duplicate that the user individuates as a *second* statement
  citizen is, by construction, a second original and is summed. Deterministic
  sameness is therefore carried by the user's individuation of the statement
  citizen, exactly as the committed `f1099g` family already does, and is not
  inferred from evidence identity (ADR-0015 §5). **No new anti-duplication
  mechanism is authorized or needed.**
- **Borrower identity is an admission condition, not a key.** The supported class
  requires that the taxpayer (or the spouse on a joint return) is the borrower
  named on the statement; that assertion is carried by eligibility component
  **A1** (legal obligation) in T0-2, which is the condition tax law actually
  turns on [P970 p. 33]. Keying on a truncatable borrower TIN would be unsound.
- **Late members and closure** follow ADR-0016/ADR-0017 unchanged: a family
  declaration with an exact closure claim and canonical member predicate; a
  closure fact keyed on the family horizon current at attestation; a membership
  transition records a successor horizon and displaces the closure and every
  closure-backed result.

#### Family closure claim (settled wording constraint)

Per ADR-0016 §5, closure of a box-1 statement family may authorize **only** the
box-1 subtotal. The claim must state, and must not exceed:

> Every amount reported in box 1 of a Form 1098-E furnished to the taxpayer for
> tax year 2025 is recorded as a statement item as of the keyed horizon. This
> claim covers Form 1098-E box 1 only: it says nothing about deductible student
> loan interest not reported in box 1 (including interest below the $600
> reporting threshold, interest from a person not filing, and pre-September-1-2004
> loan origination fees or capitalized interest omitted under box 2), nothing
> about whether any reported amount is deductible by this taxpayer, and nothing
> about Schedule 1 line 21 or line 26 completeness. Closed with members
> authorizes the multi-filer sum of current members; closed-empty authorizes
> subtotal 0.

**Closed-empty is a valid state** and authorizes a box-1 subtotal of 0 — not a
zero line 21, which additionally requires the T0-2 and T0-3 authority.

---

### T0-2 — Component-level taxpayer eligibility authority (settled)

This is the item the charter singles out. It is settled **without** any collapsed
`qualified=yes`.

#### The evidence ceiling of Form 1098-E box 1

What box 1 **does** prove, at its highest: that a person, in the course of a
trade or business, received $600 or more of interest from an individual during
2025 on something that person treated as a reportable student loan [I1098ET
pp. 1–2].

What the lender's reportability test actually is [I1098ET p. 2]: the loan must be
either (a) "Subsidized, guaranteed, financed, or otherwise treated as a student
loan under a program of the federal, state, or local government, or of a
postsecondary educational institution", **or** (b) "**Certified by the borrower**
as a student loan incurred solely to pay qualified higher education expenses."

The decisive sentence, for revolving accounts and by extension for the
certification branch generally: "**You do not have to verify the borrower's
actual use of the funds.**" [I1098ET p. 2]

Therefore branch (b) reduces to *the same taxpayer assertion the engine would
otherwise collect directly*, laundered through a third party. Branch (a) proves a
program characteristic of the loan, not the taxpayer's §221 qualification. And
the form itself tells the borrower so: "you may **not** be able to deduct the
full amount of interest reported on this statement. Do not contact the
recipient/lender for explanations of the requirements for … any allowable
deduction" [F1098E p. 4].

**Conclusion: Form 1098-E is authority for an amount and for a statement's
existence. It is authority for none of the taxpayer-side conditions.** Accepting
a contributed `qualified=yes` would not merely be opaque; it would be *less*
informative than the components below, because the taxpayer certifying to a
lender under [I1098ET p. 2] is certifying to a narrower question (sole use for
qualified higher education expenses) than §221 asks.

#### Conditions that are CALCULATED, never contributed

Recorded here so no later unit mistakes them for components:

| Condition | Why it is calculated | Authority |
| --- | --- | --- |
| Modified AGI below $100,000 / $200,000 | The instruction itself directs computation: "Use **lines 2 through 4 of the worksheet** in these instructions to figure your modified AGI" [I1040GI p. 98]. The engine computes it. | [I1040GI p. 98]; [P970 p. 34] "MAGI is the AGI on **line 11a** of that form figured **without taking into account any amount on Schedule 1 line 21**" |
| Filing status ≠ married filing separately | Existing `filing_status` fact compared with `categorical_compare` / `category_literal` (ADR-0025 §5). Not a new component. | [I1040GI p. 98]; [P970 p. 33] |
| Total qualifying interest | The family box-1 subtotal (T0-1/T0-3). | [I1040GI p. 99] worksheet line 1 |
| $2,500 ceiling and the phaseout | Track 0b. | [I1040GI p. 99]; [P970 pp. 33–35] |

**A structural consequence worth pinning:** at MAGI ≥ $100,000 ($200,000 MFJ)
the worksheet's line-7 ratio clamps to 1.000 and line 9 is 0. The statutory
eligibility ceiling and the phaseout endpoint coincide exactly [P970 p. 34,
Table 4-2]. The engine therefore needs **no separate contributed MAGI-ceiling
guard** — the arithmetic already produces zero. Track 0b owns whether the rule
nonetheless states the ceiling explicitly for legibility; Track 0b must not add a
*contributed* MAGI answer either way.

#### Scope of the components: return-scoped, and why

**Finding (verified in code at this commit, not assumed):** the rule language
cannot fold a categorical or boolean condition across a variable-length family
membership. `packages/derivation/evaluator.py` line 118 `collect` returns
`[_as_decimal(v) for v in rows]` — it is a **numeric** collector only; `count`
(line 133) returns a length; there is no categorical or boolean aggregate. A
**per-statement** eligibility component is therefore **not expressible** at this
base.

Two candidate responses were considered:

- **Rejected — encode a per-statement eligibility flag as 1/0 and test
  `add(collect(flags)) == count(statements)`.** This re-introduces exactly the
  numeric-code representation of a categorical that ADR-0025 §5 retired
  ("Decimal `compare` remains numeric-only and gains no second interpretation");
  it also mints a second parallel source family whose closure would have to be
  kept coextensive with the statement family, contrary to ADR-0016 §4.
- **Rejected — mint a categorical aggregate operator.** That is new generic
  substrate for the rule language, i.e., milestone **stop condition 2**, and it
  is not needed: see below.

**Settled: every eligibility component is return-scoped**, keyed by the
`tax-year` literal `"2025"` alone, exactly like the committed
`schedule1-part1-scope` and `ss-benefits-scope` vocabularies (verified:
`schedule1-part1-scope.bundle.json`, `fact-type.v2`, `identity_keys` = a single
`tax-year` literal). Each component's **title carries the universal
quantifier explicitly** — "for every Form 1098-E box-1 amount recorded in the
2025 Form 1098-E source family" — so the collapsed scope is stated in the
authority itself and appears verbatim in the explanation walk. This is a
consolidation over statements, **not** over conditions: the thirteen distinct
legal conditions the charter enumerates remain thirteen separately authorized
answers. Meaning survives because a "no" on any component names the exact legal
condition that failed, and because the quantifier is written into the fact
type's own title rather than assumed by a reader.

#### The components

Shape for all of them (no novelty; matches `schedule1-part1-scope` exactly):
`fact-type.v2` in a `bundle.v2`, `nature: determinable`, `value_schema`
`{"enum": ["yes","no"]}`, `supersession: {"policy": "free"}`, **no
`optional_default`**, `identity_keys` = `[{kind: literal, name: tax-year,
values: ["2025"]}]`. Package binding `mode: "required"` (ADR-0025 §4) so absence
blocks `DEPENDENCY_ABSENT`; a declared default is forbidden here — these are
answers, not conveniences. `yes` asserts the named condition is satisfied for
every recorded statement; `no` blocks. They are contributed facts entering
through the ADR-0032 contribution boundary; no run request carries them.

**Group A — loan and student conditions (10 components).**

| # | Component (proposed id suffix) | Legal condition | Authority |
| --- | --- | --- | --- |
| A1 | `legally-obligated` | The taxpayer, or the spouse on a joint return, is legally obligated under the loan terms to make the interest payments covered by every recorded statement. | [P970 p. 33] "Can You Claim the Deduction?" bullet 3; [P970 p. 33] "Don't Include as Interest" bullet 1 ("Interest you paid on a loan if, under the terms of the loan, you aren't legally obligated to make interest payments") |
| A2 | `interest-paid-in-2025` | Every box-1 amount was paid during 2025 by the taxpayer, or on the taxpayer's behalf by another person while the taxpayer was the obligated borrower. | [P970 p. 33] "When Must Interest Be Paid?"; [P970 p. 33] "Interest paid by others" |
| A3 | `proceeds-solely-qualified-expenses` | Each loan was taken out **solely** to pay qualified education expenses; no proceeds were used for any other purpose; no refinancing or consolidation carries an excess amount used for other purposes. | [P970 p. 30] "Qualified Student Loan"; [P970 p. 32] "Interest on refinanced and consolidated student loans" + CAUTION; [I1040GI p. 99] "a loan isn't a qualified student loan if (a) any of the proceeds were used for other purposes" |
| A4 | `expenses-within-reasonable-period` | The expenses were paid or incurred within a reasonable period of time before or after the loan was taken out. | [P970 p. 30] second bullet; [P970 p. 31] "Reasonable period of time" |
| A5 | `student-relationship-when-incurred` | The student was the taxpayer, the taxpayer's spouse, or a person who was the taxpayer's dependent (as defined for this purpose) **when the loan was taken out**. | [P970 p. 30] "Qualified Student Loan" first bullet and "Your dependent"; [P970 p. 31] top (the three-part expanded dependent definition); [I1040GI pp. 98–99] items 1–3 |
| A6 | `eligible-student` | The student was enrolled **at least half-time** in a program leading to a degree, certificate, or other recognized educational credential. | [P970 p. 31] "Eligible student", "Enrolled at least half-time" |
| A7 | `eligible-educational-institution` | The education was provided by an eligible educational institution, judged during the academic period(s) for which the loan was incurred. | [P970 p. 31] "Eligible educational institution"; [I1040GI p. 99] |
| A8 | `lender-not-related-person` | No recorded statement's loan was from a related person. | [P970 p. 31] "Related person"; [I1040GI p. 99]; §221(d)(1) |
| A9 | `not-qualified-employer-plan-loan` | No recorded statement's loan was made under a qualified employer plan or under a contract purchased under such a plan. | [P970 p. 31] "Qualified employer plan"; [I1040GI p. 99]; §72(p)(4)–(5) via [I1098ET p. 2] |
| A10 | `expenses-not-reduced-below-loan` | Qualified education expenses, **after** the mandatory reduction for tax-free employer educational assistance, Coverdell distributions, QTP distributions, excluded savings-bond interest, tax-free scholarships and fellowship grants, veterans' educational assistance, and other nontaxable educational assistance, were not less than the loan proceeds. | [P970 p. 32] "Adjustments to Qualified Education Expenses" |

**Group B — taxpayer-status and double-benefit conditions (5 components).**

| # | Component | Legal condition | Authority |
| --- | --- | --- | --- |
| B1 | `not-claimed-as-dependent` | Neither the taxpayer nor, on a joint return, the spouse is claimed as a dependent on another taxpayer's 2025 return. | [I1040GI p. 98] fourth bullet; [P970 p. 33] "Claiming you as a dependent" and Example 2 |
| B2 | `no-qtp-tax-free-earnings-paid-interest` | No claimed interest was paid from a distribution of earnings made from a QTP after 2018 to the extent the earnings are treated as tax free because used to pay student loan interest. | [I1040GI p. 98]; [P970 p. 33] "No Double Benefit Allowed" ¶2 |
| B3 | `no-employer-educational-assistance-interest` | No claimed interest was paid by the taxpayer's employer after March 27, 2020 under an educational assistance program. | [P970 p. 30] Reminder; [P970 p. 33] "No Double Benefit Allowed" ¶3 |
| B4 | `no-other-provision-deduction` | No claimed amount is an allowable deduction under any other provision of the tax law, and no claimed amount is included in figuring any other deduction on the return. | [P970 p. 33] "No Double Benefit Allowed" ¶1; [I1040GI p. 99] worksheet line 9 ("Don't include this amount in figuring any other deduction on your return (such as on Schedule A, C, E, etc.)") |
| B5 | `no-loan-repayment-assistance-payments` | No claimed interest was paid through the taxpayer's participation in the NHSC Loan Repayment Program or a similar loan repayment assistance program. | [P970 p. 33] "Don't Include as Interest" bullet 3 |

#### Consolidations made, and why the meaning survives

The charter requires these be named. Four were made; each is a merge the
authority itself performs, not an engine convenience.

1. **"Eligible student" + "at-least-half-time enrollment" → A6.** [P970 p. 31]
   defines them as one thing: "An eligible student is a student who was enrolled
   at least half-time in a program leading to a degree, certificate, or other
   recognized educational credential." Splitting would create a fragment with no
   independent legal content.
2. **"Student–taxpayer relationship" + "dependent status when the loan was
   incurred" → A5.** [P970 p. 30] states them as a single conjunctive bullet;
   the relationship test is meaningless without its "when you took out the loan"
   timing, and the timing is meaningless without the relationship.
3. **"Related-party loan exclusion" and "qualified-employer-plan loan exclusion"
   were deliberately NOT merged** (A8, A9), despite being one sentence in
   [I1040GI p. 99]. They are distinct §221(d)(1) exclusions with distinct
   definitions [P970 p. 31] and distinct taxpayer knowledge; a merged "no" could
   not name which applied.
4. **"Non-interest loan origination fees" and "capitalized-interest timing" are
   NOT components.** [P970 p. 33] excludes origination fees that pay for property
   or services, and [P970 p. 32] makes capitalized interest deductible only as
   principal payments are made. Both are already discharged **by the lender's
   own reporting rule**: for loans made on or after September 1, 2004 the filer
   must include in box 1 only "payments of interest as described in Regulations
   section **1.221-1(f)** … interest includes capitalized interest and loan
   origination fees **that represent charges for the use or forbearance of
   money**" [I1098ET p. 2]; for loans made before that date box 1 contains only
   stated interest [P970 p. 34]. Box 1 is thus, by construction, amounts actually
   received in 2025 that are interest in the tax sense. This is the precise reason
   the box-1 boundary in T0-3 is safe rather than merely convenient, and it holds
   **only** while box 2 is unchecked.

#### Charter-stop check for this item

Milestone stop condition 4 ("collapsed eligibility") is **not** triggered:
component-level authority is achievable without any opaque `qualified=yes`. The
only collapse present is over *statements*, it is forced by a verified property
of the committed evaluator rather than chosen, it is written into each fact
type's title, and the alternatives were rejected on governance grounds (ADR-0025
§5, ADR-0016 §4) rather than on effort.

---

### T0-3 — The reported-interest boundary (settled)

**Settled: the first milestone supports Form 1098-E box-1 interest only.**

Box-2 semantics, restated precisely. Box 2 is checked when "loan origination
fees and/or capitalized interest are **not** reported in box 1 for loans made
before September 1, 2004" [I1098ET p. 2; F1098E p. 2 field text]. The borrower
instruction draws the consequence: "If your loan was made before September 1,
2004, you **may be able to deduct** loan origination fees and capitalized
interest not reported in box 1" [F1098E p. 4]; [P970 p. 34] adds "if you pay
qualifying interest that isn't included on Form 1098-E, you can **also** deduct
those amounts", pointing at the Pub 970 p. 32 allocation method, which requires
loan-level amortization data the engine does not have and this milestone does not
model.

The charter's reading is confirmed and can be stated more sharply: **box 2 is a
lender assertion that box 1 is knowingly incomplete.** It says nothing about
eligibility. It must **block**, never silently reduce the deduction to the box-1
figure.

#### Dispositions

| Case | Disposition | Ground |
| --- | --- | --- |
| Box 2 checked on any recorded statement | **Block.** Carried by component **C1** below. | [F1098E p. 4]; [P970 p. 32] allocation method out of scope |
| Interest paid below the $600 lender reporting threshold | **Deductible in law, unsupported here → must block unless declared absent.** | [I1098ET p. 1] "$600 or more"; [P970 p. 32] Example (a real deductible amount with no Form 1098-E). Carried by **C2**. |
| Qualifying interest paid to a person who filed no statement (not in a trade or business, or non-compliant) | Same as above → **C2**. | [I1098ET p. 1] "Who must file" is limited to trade-or-business recipients |
| Pre-September-1-2004 loan origination fees | **Block** via C1 when box 2 is checked; otherwise covered by C2. | [P970 p. 32] "Loan origination fee"; [I1098ET p. 2] |
| Capitalized interest omitted when box 2 is checked | **Block** via C1. | [P970 p. 32] "Capitalized interest" |
| Additional qualifying interest not shown in box 1 for any other reason | **Block** unless C2 is `yes`. | [P970 p. 34] |
| Multiple statements from one filer | **Supported.** Distinct statement citizens; summed by the family subtotal. | [I1098ET p. 1] "you may file a separate Form 1098-E for each student loan … or you may file one Form 1098-E for the interest from all student loans" |
| Multiple statements from several filers | **Supported.** Multi-filer sum, as the closure claim states. | Same |
| One statement covering several loans | **Supported**, and it is the reason the eligibility components must quantify over loans, not statements. | [F1098E p. 4] box 1 "on **one or more** student loans made to you" |
| Non-interest origination fees (commitment/processing) inside box 1 | **Cannot occur**; no guard needed. | [I1098ET p. 2] Reg. §1.221-1(f) limits box 1 to charges "for the use or forbearance of money" |

#### The two boundary components

Same shape and package binding as the T0-2 components (return-scoped,
`{"enum":["yes","no"]}`, `mode: "required"`, no default).

| # | Component | Assertion | Authority |
| --- | --- | --- | --- |
| C1 | `no-box-2-checked` | No 2025 Form 1098-E furnished to the taxpayer has box 2 checked. | [F1098E p. 2] box 2; [F1098E p. 4] Box 2 instruction; [I1098ET p. 2] |
| C2 | `no-unreported-deductible-interest` | The taxpayer has no deductible 2025 student loan interest other than the amounts reported in box 1 of the recorded Forms 1098-E — including interest below the $600 reporting threshold, interest paid to a person who filed no statement, and pre-September-1-2004 origination fees or capitalized interest. | [I1098ET p. 1]; [P970 pp. 32, 34] |

**C2 is not implied by family closure, and this is a governed consequence rather
than a preference.** ADR-0016 §5: closure of a box-1 statement family "may
authorize only the box-1 subtotal … It does not authorize … 'all taxable
interest complete.'" The same holds here: closure proves the *statement set* is
complete; C2 asserts the *deductible-interest universe* equals that set. The
charter's SLI-C3 is confirmed on that basis.

**Why C1 is separate from C2 even though C2 subsumes it.** C1 is a transcription
of a printed checkbox the taxpayer is holding — cheap, directly auditable, and it
lets the explanation name a form field. C2 is an attestation about the world.
Keeping them separate keeps the audit trail honest about which is which.

**Note.** C1 is deliberately a return-scoped attestation rather than a member
predicate on the family. Excluding box-2-checked statements from family
membership would let a family close *without* them, silently discarding a real
statement — the "silently absorbed" failure the charter forbids.

---

### T0-9 — SSA interaction (verified, no cycle)

The foreman's pre-finding is **confirmed on both halves**, by primary source and
by repository content at `eaee81d`. It was verified, not inherited.

**Half 1 — the paper.** The ordinary Social Security Benefits Worksheet's MAGI
subtraction is "the total of the amounts from Schedule 1, lines 11 through 20,
and 23 and 25" — the identical set the Student Loan Interest Deduction Worksheet
uses at its own line 3 [I1040GI p. 99, worksheet line 3]. Line 21 is in neither
set. Line 22 is "Reserved for future use" [F1040S1 p. 2; I1040GI p. 99]. Schedule
1 line 26 is "Add lines 11 through 23 **and 25**" [F1040S1 p. 2] — the same set
**plus line 21**. Independently corroborated by [P970 p. 34]: "your MAGI is the
AGI on line 11a of that form figured **without taking into account any amount on
Schedule 1 (Form 1040), line 21**", which is exactly what worksheet lines 2 − 3
compute, and which is only true because line 21 is the sole element of line 26
absent from worksheet line 3.

**Half 2 — the artifact.** `packages/content/tax/2025/rule.ss-benefits-worksheet.json`
(v1, `rule-artifact.v3`, publishes `tax.us.2025.social-security.line6b`) declares
31 `requires` entries. Its Schedule 1 adjustment absences are exactly
`no-sch1-line11-educator`, `-line12-business-expenses`, `-line13-hsa`,
`-line14-moving`, `-line15-deductible-se`, `-line16-se-retirement`,
`-line17-se-health`, `-line18-penalty`, `-line19-alimony-paid`,
`-line20-ira-deduction`, `-line23-archer-msa`, `-line25-other-adjustments` —
**twelve, with no line-21 and no line-22 entry.** It requires no AGI symbol, no
Schedule 1 line-26 symbol, and no Form 1040 line-10 symbol; none of those exist
at this base (verified: no artifact under `packages/content/tax/2025/`
references Schedule 1 line 21 or line 26; the only `line-21` matches in the tree
are Schedule D line 21).

**Half 2b — mechanical proof.** The 82 `computation` members of
`package.core-calculations.v29.json` were loaded, their `publishes`/`requires`
projected into a symbol graph (174 nodes), the four prospective milestone edges
added —

```
slid.line21              ← income.total-income, f1098e box-1 subtotal, filing_status
schedule1.line26         ← slid.line21
form1040.line10          ← schedule1.line26
income.agi(11a)          ← income.total-income, form1040.line10
```

— and the combined graph was depth-first searched. Results:

- **cycles: none;**
- the SS worksheet's transitive dependency closure is 93 symbols and contains
  **none** of `slid.line21`, `schedule1.line26`, `form1040.line10`,
  `income.agi(11a)`, or `income.agi`;
- `income.agi(11a)` **does** transitively depend on `social-security.line6b`,
  confirming the dependency is strictly one-directional
  (SS → line 9 → line 21 → line 26 → line 10 → line 11a);
- exactly one publisher per symbol across the selected computation set, with the
  single pre-existing exception of `tax.us.2025.schedule-a.total`
  (`rule.schedule-a-total.json` / `rule.schedule-a-total-closed-empty.json`), a
  guarded closed-empty alternate that predates this milestone and is untouched
  by it.

**Milestone stop condition 6 is not triggered.** The remaining half of T0-9 —
that the merged SSA line-9 and downstream successors stay selected and that each
component appears exactly once — is a *test* obligation on Tracks 1–2, listed in
the evidence matrix; the paper and structural preconditions for it are settled
here.

**One caution for the implementing tracks.** The SS worksheet consumes
`tax.us.2025.income.additional-income`, which `rule.form1040-line8.json` derives
from `tax.us.2025.schedule1.line10-additional-income` — Schedule 1 **Part I**.
Any Part II work that renames, re-versions, or re-points that Part I symbol would
create the cycle this item rules out. Part II must be additive to Part I, never a
re-pointing of it.

---

### T0-10 — Contract novelty (settled for T0-1, T0-2, T0-3, T0-9)

**No new ADR is required by any item in this unit.** Every settled position is a
content-level application of an already-ratified contract:

| Settlement | Governing contract | Nature |
| --- | --- | --- |
| Kernel fact types for the statement, closure, and every eligibility component | ADR-0011 §1, §4–5 | reuse |
| Statement-instance identity; corrections supersede; duplicates; evidence peer-hood | ADR-0015 §1–5 | reuse |
| Family declaration, exact closure claim, canonical member predicate, no broadening | ADR-0016 §1–5 | reuse |
| Family horizon, closure keyed on horizon, value correction does not advance it | ADR-0017 §1–5 | reuse |
| Categorical components with `categorical_compare` / `category_literal`; `mode: "required"`, no declared defaults | ADR-0025 §4–6 | reuse |
| Components arrive as contributed facts, never as run-request values | ADR-0032 §1, §3, §5 | reuse |
| Artifact shapes: `fact-type.v2` in `bundle.v2`, `source-family.v1`, `source-closure-mapping.v2` | committed `f1099g` / `schedule1-part1-scope` content | reuse |

No new generic substrate is implied: no new attachment ontology, no new closure
mechanism, no new worksheet mechanism, no new identity or anti-duplication
mechanism, and — given the return-scoped component decision in T0-2 — **no new
rule-language operator from this unit.** Milestone stop conditions 1, 2, and 8
are not triggered; no prototype is required or requested.

**Scope note.** Whether the milestone needs one ADR in the ADR-0025 line for
`multiply`/`divide` is a **T0-4** question and is neither confirmed nor denied
here. If Track 0b concludes it does, the milestone's total remains the foreman's
expected "at most one".

---

### Notes addressed to Track 0b (T0-4 – T0-8) — findings, not decisions

1. **Pin p. 99, not p. 98, for the worksheet** [I1040GI]. See the charter
   erratum above. The line-21 conditions and the Exception are on p. 98.
2. **The MAGI ceiling needs no contributed answer.** The $100,000/$200,000
   eligibility limit and the phaseout endpoint coincide exactly [P970 p. 34,
   Table 4-2]: at that MAGI the line-7 ratio clamps to 1.000 and line 9 is 0.
   Track 0b decides whether to state the ceiling explicitly for legibility; it
   must not introduce a contributed MAGI or a contributed eligibility flag for it.
3. **Worksheet line 1 receives the box-1 family subtotal, capped.** Under T0-2/T0-3
   the entire recorded box-1 subtotal is qualifying interest, because A1–A10, C1,
   and C2 are all `yes` before the rule fires. There is no partial-eligibility
   arithmetic in this class.
4. **The Pub 970 worked examples are usable as fixture oracles.** [P970 p. 34]
   Example 1: MFJ, $800 interest, MAGI $185,000 → $400. [P970 p. 35] Example 2:
   same facts with $2,750 paid → $2,500 capped, reduced by $1,250 → $1,250. Both
   exercise the cap-before-phaseout ordering.
5. **Two `Before you begin` conditions are paper preconditions, not arithmetic**
   [I1040GI p. 99]: the line-24z write-in must be figured first, and the
   Exception (Form 2555 / Form 4563 / excluded Puerto Rico income) routes to
   Pub 970 Worksheet 4-1. The corresponding absences already exist in
   `ss-benefits-scope` as `no-schedule1-line24z-writein`, `no-form-2555`,
   `no-form-4563`, `no-puerto-rico-or-samoa-income`; the reuse-versus-mint call
   on that vocabulary is **T0-5's**, untouched here.
6. **Pub 970 Worksheet 4-1 confirms the variant boundary** [P970 p. 35]: its
   lines 5–8 add back the foreign earned income/housing exclusions, the foreign
   housing deduction, and excluded Puerto Rico and American Samoa income. The
   ordinary worksheet has no such lines. This corroborates that the four
   Exception absences are the exact boundary between the two worksheets.
7. **Pub 970 states the 2025 Form 1040 AGI line as "line 11a"** [P970 p. 34],
   independently corroborating the T0-8 succession target.
8. **Part II must be additive to Part I.** See the caution at the end of T0-9:
   re-pointing `tax.us.2025.schedule1.line10-additional-income` would create the
   cycle T0-9 rules out.
9. **Attachment question (T0-7), for information only.** At MAGI ≥ $100,000
   ($200,000 MFJ) the taxpayer "can't claim the deduction" [P970 p. 30, p. 34],
   and line 21 is 0. Whether a zero line 21 makes Schedule 1 not-required is
   T0-7's call under ADR-0036; the paper here says the deduction is *eliminated*,
   not merely computed to zero.
10. **Boundary values for the evidence matrix.** [P970 p. 34, Table 4-2]:
    "not more than $85,000" is unaffected; "more than $85,000 but less than
    $100,000" is reduced; "$100,000 or more" is eliminated. So MAGI exactly
    $85,000 → no phaseout; exactly $100,000 → fully eliminated. Same with
    $170,000/$200,000 for MFJ.

---

### Cases requiring explicit disposition — those falling under this unit

| Case | Disposition | Where settled |
| --- | --- | --- |
| Multiple Forms 1098-E | Supported; distinct statement citizens, multi-filer sum | T0-1, T0-3 |
| Corrected statements | Supported; same fact, supersession; horizon does not advance | T0-1 |
| Duplicate statements | One statement citizen, one fact; re-assertion supersedes | T0-1 |
| VOID-checked statement | **Blocks**; Copy B has no VOID box, so it cannot legitimately reach the taxpayer | T0-1 |
| Statement omitting the account number | **Recorded normally**; the account number is not an identity key and not required | T0-1 |
| Box 2 checked | **Blocks** (C1) | T0-3 |
| Interest paid below the $600 reporting threshold | **Blocks** unless C2 is `yes` | T0-3 |
| Unreported interest generally | **Blocks** unless C2 is `yes` | T0-3 |
| Capitalized interest | In box 1 for post-9/1/2004 loans by Reg. §1.221-1(f); otherwise blocks via C1/C2 | T0-2 (consolidation 4), T0-3 |
| Loan origination fees | Same as capitalized interest; non-interest fees cannot appear in box 1 | T0-2 (consolidation 4), T0-3 |
| Loans from related persons | **Blocks** (A8) — guarded exclusion, not a supported case | T0-2 |
| Loans from qualified employer plans | **Blocks** (A9) — guarded exclusion | T0-2 |
| Mixed-use loans | **Blocks** (A3). Note: [I1098ET p. 2] instructs filers "Do not report interest on mixed use loans", so such a statement should not exist; A3 blocks it if one does | T0-2 |
| Refinancing or consolidation loans | **Supported** when solely refinancing qualified student loans of the same borrower; an excess amount used for other purposes **blocks** (A3) | T0-2; [P970 p. 32] |
| Interest paid by someone other than the legally obligated borrower | **Supported and deductible by the obligated borrower** — this is *not* a blocker. "If you are the person legally obligated to make interest payments and someone else makes a payment of interest on your behalf, you are treated as receiving the payments from the other person and, in turn, paying the interest" [P970 p. 33], with two worked examples. A1 (obligation) and A2 (payment) carry it | T0-2 |
| Interest paid by an employer | **Blocks** (B3) when paid after March 27 2020 under an educational assistance program. Note the contrast with the preceding row: [P970 p. 33] Example 1 allows an employer-adjacent payment that was *included in the borrower's W-2 box 1 as compensation*, which is not educational assistance. B3 is written to the educational-assistance program, not to the payer | T0-2 |
| Interest paid with a tax-free QTP distribution | **Blocks** (B2) | T0-2 |
| Taxpayer claimable as another person's dependent | **Blocks** (B1). [P970 p. 33] Example 2: in that case neither the student nor the parents may deduct | T0-2 |
| Student not a qualifying dependent when the loan was incurred | **Blocks** (A5) | T0-2 |
| Less-than-half-time enrollment | **Blocks** (A6) | T0-2 |
| Non-degree or non-credential study | **Blocks** (A6) | T0-2 |
| Ineligible educational institutions | **Blocks** (A7). Note the institution is judged only during the academic period(s) for which the loan was incurred; later loss of eligibility does not affect deductibility [P970 p. 31] | T0-2 |
| Amount claimed under another deduction or exclusion | **Blocks** (B4); loan-repayment-assistance payments blocked by B5 | T0-2 |
| Married filing separately | **Blocks** — computed from the existing `filing_status` categorical fact, not a new component | T0-2 |
| MAGI phaseout boundaries | **Computed**, never contributed; boundary values recorded in note 10 to Track 0b | T0-2 (out of unit for the arithmetic) |
| Foreign-income or territorial-income modifications | **Out of this unit** — T0-5 owns the Exception vocabulary; note 5/6 to Track 0b records the corroborating paper | — |
| Every Schedule 1 Part II adjustment other than line 21 | **Out of this unit** — T0-5/T0-6 | — |

---

### Open items and escalations from this unit

**None.** No milestone stop condition is triggered by T0-1, T0-2, T0-3, T0-9, or
T0-10; no new ADR is implied; no unratified-PR content was read or edited; no
prototype is requested; no sub-agent was used. T0-4 through T0-8 remain open and
are Track 0b's.

---

## Track 0b settlement — T0-4, T0-5, T0-6, T0-7, T0-8

Author: Track 0b builder (paper), owner-launched, base `f05dc6e`.
Unit: charter items **T0-4, T0-5, T0-6, T0-7, T0-8** and the "Cases requiring
explicit disposition" entries falling under them. **T0-1, T0-2, T0-3, T0-9, and
T0-10 are not re-settled here**; the Track 0a settlement above governs them and
is untouched.

Every carry-forward from Track 0a and every foreman pre-finding relied on below
was re-verified against primary source or against repository content at this
commit. Where verification changed the answer, it says so.

### Sources used, with exact locations

| Tag | Source | Where |
| --- | --- | --- |
| **[F1040]** | 2025 Form 1040 | page 1: line 9, line 10, line 11a; page 2: line 11b, line 15 |
| **[F1040S1]** | 2025 Schedule 1 (Form 1040) | page 2: Part II lines 11–25, line 26 |
| **[I1040GI]** | 2025 Instructions for Form 1040 | printed **p. 33** ("Total Income and Adjusted Gross Income", Line 10); printed **p. 88** (Instructions for Schedule 1, General Instructions); printed **p. 98** (line 21 conditions, Exception); printed **p. 99** (**Student Loan Interest Deduction Worksheet**) |
| **[P970]** | 2025 Publication 970, chapter 4 | printed **p. 34** (phaseout range, Table 4-2, MAGI definition, Example 1); printed **p. 35** (Example 2, Which Worksheet To Use, Worksheet 4-1) |

**Charter erratum re-verified independently.** The Student Loan Interest
Deduction Worksheet is on i1040gi **printed p. 99** (PDF page 99; the page
footer on that page reads `99`). Printed p. 98 carries the line-21 conditions
and the Exception. Track 0a's erratum is confirmed; the charter's p. 98 is
wrong for the worksheet. The charter's verbatim worksheet text was compared
word for word against the extracted page and is accurate, with one omission:
worksheet line 9's closing parenthetical is "**(such as on Schedule A, C, E,
etc.)**".

---

### T0-4 — The ordinary Student Loan Interest Deduction Worksheet (settled)

#### One rule citizen, on the accepted worksheet pattern

Worksheet lines 1–9 fold into **one** `computation` rule publishing
`tax.us.2025.schedule1.line21-student-loan-interest`, on the
`rule.ss-benefits-worksheet.json` pattern (ADR-0038 / ADR-0060 govern
"printed worksheet as declared rule content"). No new worksheet substrate.

#### The line-by-line mapping

Declared parameters, never literals, for every printed money constant:

| Parameter (proposed id) | Shape | Values | Authority |
| --- | --- | --- | --- |
| `…parameter.student-loan-interest-max` | scalar | `2500` | [I1040GI p. 99] worksheet line 1; [P970 p. 30] |
| `…parameter.student-loan-phaseout-start` | keyed by `filing_status` | `single`/`head_of_household`/`qualifying_surviving_spouse` → `85000`; `married_filing_jointly` → `170000` | [I1040GI p. 99] worksheet line 5 |
| `…parameter.student-loan-phaseout-range` | keyed by `filing_status` | same four keys → `15000`; `married_filing_jointly` → `30000` | [I1040GI p. 99] worksheet line 7 |

Both keyed tables **must omit `married_filing_separately`**. MFS is already
blocked by the T0-2 filing-status test; omitting the key means that even if that
test were removed, an MFS return cannot silently compute — the keyed `parameter`
op raises `LOOKUP_MISS` (verified: `packages/derivation/evaluator.py:152–155`).
That is a structural backstop, not a substitute for the explicit test.

The expression, worksheet line by worksheet line:

| Worksheet line | Expression at this base |
| --- | --- |
| 1 — capped qualifying interest | `choose(when: compare(f1098e box-1 subtotal, param(max), "gt"), then: param(max), else: subtotal)` |
| 2 — Form 1040 line 9 | `ref(tax.us.2025.income.total-income)` |
| 3 — Sch 1 lines 11–20, 23, 25 | literal `0`, gated (see T0-5) |
| 4 — MAGI | `subtract(L2, L3)` |
| 5 — threshold | `parameter(phaseout-start, key: ref(filing_status))` |
| 6 — excess over threshold | `choose(when: compare(L4, L5, "gt"), then: subtract(L4, L5), else: 0)` |
| 7 — phaseout ratio | `choose(when: compare(divide(L6, param(range, key: filing_status)), 1, "gte"), then: 1, else: divide(...))` |
| 8 — phased-out portion | `multiply(L1, L7)` |
| 9 — the deduction | `round(subtract(L1, L8), mode: ref("rounding.convention"))` |

Three notes on the mapping:

1. **Worksheet line 6's "No" branch is expressed as `0`, not as a skip.** The
   printed instruction says to skip lines 6 and 7 and enter -0- on line 8;
   setting L6 to 0 yields L7 = 0 and L8 = 0, which is the identical result and
   avoids a negative L6 producing a negative ratio. This is an arithmetic
   identity, not an interpretation.
2. **The 1.000 clamp is written with the existing `choose`/`compare` pair** and
   its constant is the literal `1`. JSON cannot carry the printed `1.000`
   trailing zeros, and it does not need to: the clamp value is exactly one and
   its precision cannot affect the product.
3. **Final rounding reuses the project convention.** `round` with
   `mode: ref("rounding.convention")`, exactly as `rule.ss-benefits-worksheet`
   already does. The `round` canon's `unit` is `"1"` (verified:
   `packages/canon/derivation/round.v1.json`), so line 21 rounds to whole
   dollars — the correct form-level treatment.

#### The three structural facts the foreman flagged, verified

**(a) The $2,500 cap applies at worksheet line 1, before the phaseout.**
Confirmed. [I1040GI p. 99] line 1: "Enter the total interest you paid in 2025 on
qualified student loans. **Don't enter more than $2,500**"; line 8 multiplies
**line 1** by line 7. Independently corroborated by [P970 p. 35] Example 2,
whose printed formula multiplies **$2,500** — not the $2,750 actually paid — by
the phaseout fraction. Capping after the phaseout would produce $2,750 − $1,375
= $1,375 instead of the published $1,250. The ordering is load-bearing.

**(b) "Rounded to at least three places" is a precision floor on the decimal.**
Confirmed: the instruction sits on worksheet line 7, the ratio, and nothing in
the worksheet rounds line 8 or line 9 before the final form-level rounding.
Rounding the *product* is a defect. Settled convention:

> Worksheet line 7 is computed as an exact quotient **quantized to exactly
> three decimal places, half-up**, then clamped to 1.

"At least three" permits more, and exact `Decimal` division would satisfy it.
Exactly three is chosen anyway, for one reason: it is the number a taxpayer
gets from the printed worksheet by hand, so the engine's line 21 is reproducible
against the paper form. Reproducibility-by-hand is the auditability property
this product optimizes for; a silently more precise engine answer that a filer
cannot reproduce is the wrong trade. This convention is declared in content
(the operator's `scale` and `mode`), not hidden, and is pinned.

**(c) `round` does not suffice, and this is the reason a new operator is
needed.** Verified in code, not assumed: `_round`
(`packages/derivation/evaluator.py:267–274`) takes its `unit` from
`env.canon["round"]["spec"]["unit"]`, and the published canon citizen
`packages/canon/derivation/round.v1.json` fixes that unit at `"1"`. The `round`
operator can therefore only round to whole dollars; it cannot express a
three-decimal-place quotient. `round` is **not** re-versionable either:
`load_canon` (`packages/derivation/loader.py:144–154`) keys canon citizens by
their `operation` field and raises on a duplicate, so a `round.v2.json` naming
operation `round` is rejected outright. `round` stays exactly as it is, and it
remains the right operator for worksheet line 9.

#### The minimal additive expression extension

Two operators, one canon citizen, one schema successor.

**`multiply`** — n-ary, exact, no canon.

```
{"op": "multiply", "args": [<expr>, <expr>, ...]}
```

It joins the existing `add`/`max`/`all`/`any` `args` branch shape in the
expression schema. Semantics: fold `Decimal.__mul__` over the coerced operands,
identity `1`. It gets **no** canon citizen and **no** `access.operations` entry,
matching `add`, `subtract`, and `max` — there is no convention to pin, because
multiplication of two exact decimals has no free parameter. It inherits exactly
the same ambient-`Decimal`-context property that `add` and `subtract` already
have and introduces no new one; with a money left operand and a three-place
right operand the product is exact well inside the default 28-digit context.

**`divide`** — binary, scaled, canon-governed.

```
{"op": "divide", "left": <expr>, "right": <expr>, "scale": 3, "mode": "half_up"}
```

Semantics: coerce both operands; if the divisor is zero, raise
`DEPENDENCY_INVALID` (never a Python `DivisionByZero`, never a NaN, never
silence); otherwise quantize the quotient to `scale` decimal places using
`mode`. `scale` and `mode` live in the **expression** so they are visible in the
rule and in the explanation walk; the permitted mode set, the tie-break, the
maximum admissible scale, and the zero-divisor disposition live in a new
**`packages/canon/derivation/divide.v1.json`** operation-semantics citizen,
mirroring `round.v1.json`. `divide` **does** add to `access.operations`, so
every derivation that uses it carries a `role: "operation-semantics"` pin at the
canon citizen's version (verified: `packages/derivation/runner.py:433–434`).
That is the correct treatment precisely because division here has a declared
convention that an auditor must be able to pin. `CANON_OPERATIONS`
(`packages/derivation/loader.py:103`) gains `"divide"`; this is a global loader
change, so Track 1 must confirm every existing canon-loading test still passes.

**Schema successor.** The expression definition is a closed `oneOf` with
`additionalProperties: false` on every branch (verified in
`packages/schemas/derivation/rule-artifact.v4.schema.json`, `$defs.expr`), so
the two operators require a new **`rule-artifact.v5`** with `$id`
`derivation/rule-artifact.v5` and discriminator const `rule-artifact.v5`. v4 is
untouched published history. Only the new line-21 rule needs v5; nothing else
migrates.

**No `min` operator.** Confirmed: the $2,500 ceiling and the 1.000 clamp are
both expressible with the existing `choose`/`compare` pair, which also reads
closer to the printed instructions ("Don't enter more than $2,500"; "If the
result is 1.000 or more, enter 1.000") than a `min` call would. This matches the
committed precedent — `rule.ss-benefits-worksheet.json`'s own notes record
"min uses choose".

**ADR.** This warrants **one** ADR in the ADR-0025 line
("Expression Language Extensions: Multiplication and Scaled Division"), because
it introduces two operators, a `Decimal` semantic decision with free parameters,
a new operation-semantics canon citizen, an addition to `CANON_OPERATIONS`, and
a schema successor. That is the milestone's **only** new ADR, and it is the one
the foreman anticipated. Together with Track 0a's zero, the milestone total is
one. **The ADR budget is not exceeded and no escalation is triggered.**

#### Eligibility and completeness gating: block, not guard-inapplicable

Track 0a settled that a component answering `no` **blocks**. The two nearest
precedents (`rule.ss-benefits-worksheet`, `rule.schedule1-line10`) put their
absence checks in `when: all(...)`, where a `no` makes the guard false and
yields a *guard-inapplicable* disposition rather than a block. That is the wrong
disposition here: a `no` on, say, the box-2 or related-person exclusion does not
mean the deduction is inapplicable, it means the engine cannot honestly compute
this return. Settled shape:

```
"when": true,
"value": {"op": "choose",
          "when": {"op": "all", "args": [<every component> eq yes]},
          "then": <worksheet lines 1-9>,
          "else": {"op": "block", "code": <an already-published code>}}
```

with **every** component named in `requires` and `pins`, so a *missing* answer
blocks `DEPENDENCY_ABSENT` naming it. The `block` op is committed and has a
committed precedent (`rule.schedule-a-line8a.json` uses
`{"op": "block", "code": "VALUE_INVALID"}` in a `choose` `else`). **Track 1 must
use an already-published block code; no new error vocabulary is authorized by
this settlement.**

**Known limitation, recorded rather than engineered around.** `block` carries no
`missing` list — `evaluator.py:143–144` raises `EvalBlocked(expr["code"], [])`.
The block therefore names the rule and the code, not *which* component answered
`no`. Distinguishing them is not expressible at this base without new error
vocabulary or a new operator, and neither is authorized. The diagnosis path is
the rule's pins: every component finding is pinned unconditionally whatever its
value, so a walker reads the answers directly. This limitation is stated here so
review does not mistake it for an oversight.

#### Zero and boundary behavior

| Case | Line 21 | Why |
| --- | --- | --- |
| Closed-empty Form 1098-E family | `0` | L1 = 0 ⇒ L9 = 0. Track 0a: closed-empty authorizes a box-1 subtotal of 0; the T0-2/T0-3 authority is still required |
| Interest below $2,500 | uncapped | L1 = subtotal |
| Interest exactly $2,500 | `2500` | "Don't enter **more than** $2,500" — exactly $2,500 is not more |
| Interest above $2,500 | capped at `2500` | before the phaseout |
| MAGI exactly $85,000 / $170,000 | no phaseout | [P970 p. 34, Table 4-2] "**not more than** $85,000 … not affected"; worksheet line 6 tests "**more than**" |
| MAGI strictly between the endpoints | reduced | phaseout applies |
| MAGI exactly $100,000 / $200,000 | `0` | L6 = the full range ⇒ L7 = 1.000 ⇒ L8 = L1 ⇒ L9 = 0. [P970 p. 34] "$100,000 or more … eliminated" |
| MAGI above $100,000 / $200,000 | `0` | ratio > 1 clamps to 1.000 |
| Married filing separately | blocked | T0-2, plus the omitted parameter key |

**The eligibility ceiling needs no separate test.** Track 0a's note 2 is
verified: [I1040GI p. 98] states the ceiling as "modified AGI is less than
$100,000 … $200,000", and [P970 p. 34] states the phaseout as ending at exactly
those figures. $85,000 + $15,000 = $100,000 and $170,000 + $30,000 = $200,000,
so the arithmetic already returns 0 at and above the ceiling for every filing
status. Adding a contributed eligibility flag would introduce a second, weaker
authority for a fact the computation already establishes. **No contributed MAGI
and no contributed eligibility ceiling.**

#### Fixture oracles from primary source

Both Pub 970 examples were read in full and are reproduced here from the source,
not inherited:

- [P970 p. 34] Example 1 — MFJ, $800 paid, MAGI $185,000. Printed formula:
  `$800 × ($185,000 − $170,000) / $30,000 = $400`; "reduced student loan
  interest deduction is $400". Engine: L1 = 800, L6 = 15,000, L7 = 0.500,
  L8 = 400, **L9 = 400**.
- [P970 p. 35] Example 2 — same facts, $2,750 paid. Printed formula:
  `$2,500 × ($185,000 − $170,000) / $30,000 = $1,250`; "reduced … deduction is
  $1,250". Engine: L1 = 2,500 (capped), L8 = 1,250, **L9 = 1,250**.

Example 2 is the cap-before-phaseout kill-test and belongs in the evidence
matrix as such.

#### Pin table for the line-21 rule

| Role | Pinned | Count |
| --- | --- | --- |
| `input` | `tax.us.2025.f1098e.box1-subtotal`; `tax.us.2025.income.total-income`; `filing_status`; every T0-2 eligibility component (A1–A10, B1–B5); every T0-3 boundary component (C1, C2); every T0-5 MAGI component | 1 + 1 + 1 + 15 + 2 + (T0-5) |
| `parameter` | the max, the phaseout start, the phaseout range | 3 |
| `operation-semantics` | `round` (canon `v1`), `divide` (canon `v1`) | 2 |
| `citation` | the worksheet at [I1040GI p. 99]; Schedule 1 line 21 at [F1040S1 p. 2] | 2 |
| `package`, `adoption`, `governance` | as the runner supplies | — |

`multiply` is deliberately absent from the operation-semantics pins; it has no
canon citizen, exactly like `add` and `subtract`.

#### Charter-stop check for this item

Milestone stop conditions 1, 2, and 8 are **not** triggered. The operator
extension is an additive instance of the ratified ADR-0025 contract line, not
new generic substrate: it adds no new dependency, closure, worksheet,
attachment, or identity mechanism. No prototype is required or requested — the
question the foreman flagged ("what must `multiply` and `divide` mean") was
answerable on paper against committed code, and it was.

---

### T0-5 — MAGI completeness, and line 21 excluded from its own base (settled)

#### The exact component boundary

Worksheet line 3 is "the total of the amounts from **Schedule 1, lines 11
through 20, and 23 and 25**" [I1040GI p. 99]. Read off the printed Schedule 1
Part II [F1040S1 p. 2], that set is exactly **twelve** amount lines:

| Line | Printed label |
| --- | --- |
| 11 | Educator expenses |
| 12 | Certain business expenses of reservists, performing artists, and fee-basis government officials |
| 13 | Health savings account deduction |
| 14 | Moving expenses for members of the Armed Forces |
| 15 | Deductible part of self-employment tax |
| 16 | Self-employed SEP, SIMPLE, and qualified plans |
| 17 | Self-employed health insurance deduction |
| 18 | Penalty on early withdrawal of savings |
| 19a | Alimony paid (19b and 19c are the recipient's SSN and the agreement date — identifiers, not amounts) |
| 20 | IRA deduction |
| 23 | Archer MSA deduction |
| 25 | Total other adjustments (itself the sum of lines 24a through 24z) |

Plus the boundary conditions that select which worksheet applies at all:

| Condition | Effect | Authority |
| --- | --- | --- |
| Form 2555 filed | Exception — Pub. 970 Worksheet 4-1, not this worksheet | [I1040GI p. 98]; [P970 p. 35] |
| Form 4563 filed | Exception | same |
| Income excluded from sources within Puerto Rico | Exception | same |
| Schedule 1 line 24z write-in adjustment | Sequencing precondition — must be figured **before** this worksheet | [I1040GI p. 99] "Before you begin" |

Two precise points the charter's list invites and the paper resolves:

- **The foreign housing deduction is not a separate component.** It is Schedule 1
  **line 24j** ("Housing deduction from Form 2555") [F1040S1 p. 2], which feeds
  line 25. It is therefore already inside `line 25`, and separately excluded by
  the Form 2555 Exception. Minting a component for it would double-count the
  question.
- **The 24z write-in condition is a sequencing precondition, not an Exception.**
  It does not route to Pub. 970; it orders the computation. It is also *entailed*
  by an absent line 25 (24z is one of 24a–24z). It is kept as a separate required
  answer anyway, because the printed worksheet names it as its own "Before you
  begin" condition and an explanation walk should show that precondition
  discharged rather than inferred. This redundancy is deliberate and is recorded
  so review does not read it as duplication.

#### Line 21 is excluded from its own MAGI base — the structural proof

Worksheet line 3 is lines 11–20, 23, 25. Schedule 1 line 26 is "Add lines 11
through 23 **and 25**" [F1040S1 p. 2] — the same twelve **plus line 21** (line 22
is "Reserved for future use" and is never an addend). Therefore, writing L*n* for
the worksheet lines:

```
MAGI  = L2 − L3 = line 9 − (11..20, 23, 25)
AGI   = line 9 − line 26 = line 9 − (11..20, 21, 23, 25)      [F1040 line 11a]
⇒  MAGI = AGI + line 21
```

which is exactly what [P970 p. 34] states independently: "your MAGI is the AGI
on line 11a of that form figured **without taking into account any amount on
Schedule 1 (Form 1040), line 21**". The two derivations agree, and they agree
*only* because line 21 is the single element of line 26 absent from worksheet
line 3.

**Consequence, binding on Tracks 1 and 2.** The worksheet's line 3 must be built
from the twelve-line set and **must never** be built from Schedule 1 line 26 or
from `tax.us.2025.income.agi`. The identity `MAGI = AGI + line 21` is a cheap
and decisive test and belongs in the evidence matrix under "Structural".

#### The encoding of worksheet line 3

Worksheet line 3 evaluates to the literal `0`, under the `all(...)` gate that
requires each of the twelve absences to answer `yes`.

This is the committed pattern, not an invention: `rule.schedule1-line10.json`
does the same thing for Part I, and its own notes state the reason —
"**Does not manufacture zero amounts for unimplemented producers.**" Summing
twelve declared-absent components is not expressible and should not be faked;
`collect` is numeric-only (Track 0a's verified finding at
`packages/derivation/evaluator.py:118`), and there is no producer publishing a
zero for "educator expenses" to collect.

Neither alternative Track 0a rejected is re-proposed here: this encoding uses no
numeric-coded categorical and no categorical aggregate operator. The components
are return-scoped contributed categoricals compared with
`categorical_compare` / `category_literal`, which is the ADR-0025 §4–6 shape
already in use.

#### Reuse versus mint — the decision, priced

The charter calls this the highest-leverage decision in Track 0. All three
options were priced against repository content read at this commit.

**Option 3 — rename or generalize into a shared `sch1-adjustment-scope` — is
foreclosed, and is not the recommendation.** `ss-benefits-scope.bundle.json` is
content contributed by the SSA-1099 milestone, whose review is open on PR #163.
Editing it on this branch would modify content inside an unratified PR. That is
this unit's stop condition and it is also milestone stop condition 5. It is
named here only to record that it was considered and why it cannot be taken.
Whether the vocabulary should eventually be generalized is an **owner
sequencing question for after both PRs are ratified**, not a conclusion of this
settlement.

**Option 2 — mint a parallel `slid-magi-scope` vocabulary — is rejected on
correctness, not on effort.** Verified: each of these fact types is keyed by a
single `tax-year` literal, so it is a return-scoped assertion with exactly one
true answer per return. Two vocabularies asking the same return-scoped question
can hold **contradictory** current findings, and nothing at this base detects it:
there is no cross-vocabulary consistency mechanism, and adding one would be new
generic substrate. A return carrying both Social Security benefits and student
loan interest could then publish a line 6b computed on "no HSA deduction" and a
line 21 computed on "HSA deduction present". That is a silent wrong answer, which
is strictly worse than a badly-titled right one.

**Option 1 — reuse `ss-benefits-scope` in place — is the recommendation.**

What it costs, stated exactly:

1. **The titles are SSA-framed and will appear verbatim in a student-loan
   explanation walk.** Verified by reading the bundle; every relevant title
   begins "Social Security Benefits Worksheet completeness component:" and ends
   "… for the bounded worksheet claim". For example:

   > Social Security Benefits Worksheet completeness component: No Schedule 1
   > line 11 educator expenses adjustment is present for the bounded worksheet
   > claim. Contributed categorical assertion, domain {yes, no}, no default. yes
   > asserts the named excluded class is absent; no asserts it is present and
   > blocks.

   The *proposition* is correct and return-scoped; only its framing names the
   wrong consumer.

2. **It couples this milestone to `tax.us.2025.ss-benefits-scope.vocabulary` v1.**
   That coupling is not new: "Dependencies and integration order" already makes
   this milestone depend on PR #163 landing, and lists the `ss-benefits-scope`
   vocabulary by name as the reason. Reuse consumes a dependency the plan has
   already accepted rather than creating one. If PR #163 renames or re-versions
   any of these sixteen fact types before merging, milestone stop condition 9
   ("Base moved") fires and version allocation is redone — which is already the
   declared procedure.

Why it wins: the divergence hazard in option 2 is a correctness hazard with no
mechanical guard, while the cost of option 1 is a legibility blemish with a
named mitigation. Reuse also keeps the eventual generalization cheap — one
rename across one owner-sequenced change — instead of a three-way
reconciliation between two vocabularies and a successor.

**Mitigation, owed to Track 2.** The line-21 rule's `notes` and its citation must
state which printed worksheet line each reused component discharges
([I1040GI p. 99] worksheet line 3, and p. 98 for the Exception), so the walk
carries the student-loan authority even where the fact-type title carries the
SSA framing. Track 2's presentation evidence must include a student-loan
explanation walk showing this.

#### Absence authority, not optional defaults

All sixteen are contributed answers with `mode: "required"` package binding and
**no `optional_default`** — verified present in the committed bundle
(`supersession: {"policy": "free"}`, `value_schema` `{"enum": ["yes","no"]}`, no
default field). An absent answer blocks `DEPENDENCY_ABSENT` naming it; a `no`
blocks through the T0-4 gate. The charter's requirement that unsupported
components carry explicit absence authority rather than optional defaults is
satisfied by the vocabulary as committed, with nothing added.

#### Charter-stop check for this item

Milestone stop condition 5 is **not** triggered: this settlement does not
conclude that `ss-benefits-scope` should be renamed or generalized, and it edits
no content owned by another milestone. No new fact type, bundle, or vocabulary is
minted by T0-5.

---

### T0-6 — Schedule 1 Part II completeness and line 26 (settled)

#### The finding that shapes this item: one vocabulary, not two

The charter treats T0-5 (the MAGI base) and T0-6 (Part II completeness) as two
boundaries. Read against the printed form they are almost the same boundary, and
saying so exactly is what keeps this milestone small.

```
worksheet line 3  =  Schedule 1 lines 11–20, 23, 25          (twelve amount lines)
Schedule 1 line 26 =  Schedule 1 lines 11–23 and 25
                   =  those same twelve  +  line 21  +  line 22 (reserved, never an addend)
```

So Part II completeness requires **exactly the twelve absences T0-5 already
requires**, plus the computed line 21, plus a disposition for line 22. There is
**no second absence vocabulary to mint.** The T0-5 reuse decision therefore
settles T0-6's vocabulary too, and the charter's "a Part II completeness
vocabulary distinct from Part I" is satisfied by the twelve Part II absences
being disjoint from `schedule1-part1-scope`'s ten Part I absences — which they
are, by inspection of the two id sets.

#### Line 26 as a citizen

A new `computation` rule publishing `tax.us.2025.schedule1.line26-adjustments`:

- `requires` — `tax.us.2025.schedule1.line21-student-loan-interest` **and** all
  twelve Part II absences;
- gate — `all(...)` over the twelve absences answering `yes`;
- value — `ref(tax.us.2025.schedule1.line21-student-loan-interest)`;
- citation — [F1040S1 p. 2] line 26, "Add lines 11 through 23 and 25. These are
  your adjustments to income."

This mirrors `rule.schedule1-line10.json` exactly, which likewise publishes a
`ref` to its single supported contributor under an absence gate.

**Why line 26 exists at all, given that it equals line 21 numerically.** Because
Form 1040 line 10 is defined as "Adjustments to income from **Schedule 1,
line 26**" [I1040GI p. 33; F1040 p. 1]. Publishing Form 1040 line 10 directly
from line 21 would produce the right number through a citation chain the printed
form does not have. The line-26 citizen is what makes the walk match the form.

#### Line 22 — dispositioned as reserved, never as an absence

[F1040S1 p. 2] prints line 22 as "Reserved for future use", and [I1040GI p. 99]
states "Line 22 has been reserved for future use."

Settled: **line 22 gets no fact type, no absence answer, and no addend.** A
reserved line is not a line the taxpayer can have an amount on, so there is no
question to ask; asking one would manufacture authority for a proposition with
no content. Its disposition is recorded in the line-26 rule's `notes` and is
visible in the citation, which is where a reader looking for "what happened to
line 22" will look. This is the charter's requirement ("must be dispositioned as
such, not as an absence answer") taken literally.

#### Completeness is contributed, never inferred from closure

The charter's warning is correct and is restated as a binding constraint.
Track 0a fixed the Form 1098-E family's closure claim to cover **box 1 only**,
in wording that says in terms that it says "nothing about Schedule 1 line 21 or
line 26 completeness". Closure of the statement family proves the statement set
is complete; it proves nothing about educator expenses or the HSA deduction.

Concretely: none of the twelve Part II absences may be derived from
`require_closed` on the Form 1098-E family, and the line-26 rule must not carry a
`require_closed` on that family as a stand-in for Part II completeness. It gets
its closure authority transitively through line 21, which is where the box-1
family belongs.

#### Part II is additive to Part I — verified, not assumed

Track 0a's caution (its note 8 and the tail of T0-9) is honoured and the check
was run rather than inherited. The two parts are structurally disjoint at this
base:

| | Part I | Part II |
| --- | --- | --- |
| Total symbol | `tax.us.2025.schedule1.line10-additional-income` | `tax.us.2025.schedule1.line26-adjustments` (new) |
| Consumed by | `rule.form1040-line8` → `income.additional-income` → the SS worksheet | Form 1040 line 10 (new, T0-8) |
| Absence vocabulary | `schedule1-part1-scope` (ten) | `ss-benefits-scope`, twelve of its members (T0-5) |

**Nothing in this settlement renames, re-versions, re-points, or republishes
`tax.us.2025.schedule1.line10-additional-income`, and nothing consumes it.** The
cycle Track 0a ruled out stays ruled out. Milestone stop condition 6 is not
triggered and the escalation this unit was warned about does not fire.

#### Charter-stop check for this item

No new generic substrate: line 26 is one more rule citizen of the shape already
committed for line 10, using operators that already exist. No new ADR. Stop
conditions 1, 2, and 6 are not triggered.

---

### T0-7 — Schedule 1 attachment disposition (settled)

#### The schema question, answered — and a provenance defect found on the way

The charter asks whether `attachment-rule.v6`, "already available at the base",
accommodates a two-part attachment. **It does not, and the reason is not the one
the charter supposed.** The finding below is stated in full because it changes
the answer.

`attachment-rule.v6` is **not a successor to `attachment-rule.v4`.** The two are
parallel, incompatible successors of `v3`, added by two different milestones on
the same day and neither reachable from the other:

| Added by | Schemas | What it adds to v3 |
| --- | --- | --- |
| `12770bd` "Implement Schedule B attachment and package schema gate" | v5, v6 | typed subtractive `adjustment_rows`; a tie-out declaring `operation`, `positive_subtotals`, `adjustment_subtotals`. Both are **required** on every itemization |
| `a62a9af` "Implement the final Track 2 Schedule D production route" | v4 | `required_answer` widened to a `oneOf` adding `check: "value"` with `equals` (ADR-0055); a `family_nonempty` requirement variant (ADR-0053) |

Neither contains the other. v6 **drops** both of v4's additions.

Proved mechanically rather than argued: the committed
`rule.attachment.schedule-1.json`, with nothing changed but its `schema`
discriminator, validates against `attachment-rule.v6` with **24 errors**, twenty
of which are its ten completeness answers being rejected —
`'presence' was expected` and `Additional properties are not allowed ('equals'
was unexpected)`. Moving Schedule 1 to v6 would silently discard the
value-checked completeness that the Part I attachment depends on, and would
additionally demand `adjustment_rows` that Schedule 1 has no use for.

**The provenance defect.** `packages/schemas/tax/attachment-rule.v5.schema.json`
is published (`packages/schemas/tax/published.json`, checksum `aecd3bf5…`) but
its `$id` is `tax/attachment-rule.v3` and its `properties.schema.const` is
`attachment-rule.v3`. `AGENTS.md#Schema Publication Protocol` requires a new
schema version to carry a "matching `$id` and `schema` discriminator"; v5 does
not. `attachment-rule.v6` is byte-for-byte that same document with only the
`$id` and the const corrected to v6 — that is, v5 looks like a mislabeled draft
that was superseded by v6 in the same commit and left published.

Its runtime effect is nil, and that was checked rather than assumed: the schema
registry keys documents by **filename** (`packages/kernel/schema_registry.py:117`)
and strips `$id` before building the validator (line 136), so there is no `$id`
collision with the real v3. But no citizen can ever lawfully use v5 — declaring
`"schema": "attachment-rule.v5"` fails the const — and no committed content does.
`packages/derivation/runner.py:833` lists `"attachment-rule.v5"` among accepted
attachment schemas; that branch is unreachable.

**Disposition: report, do not repair.** v5 is published history and immutable;
editing it is forbidden, and it belongs to the Schedule B milestone's records,
not this one. It is inert. This milestone must simply never select it. Recorded
here for the foreman as a records item, not as work.

#### The settled shape: content-level reuse on `attachment-rule.v4`

**No new attachment schema is needed.** A successor
`rule.attachment.schedule-1` **v2**, on the unchanged `attachment-rule.v4`,
carries both parts. Three properties of v4 were verified against the committed
schema and the committed runner:

1. **Two requirement contributors are already expressible.**
   `requirement.subtotals` is an array with `minItems: 1`, and the runner
   evaluates it as an **"any subtotal over threshold"** test that records a
   per-trigger outcome for each — never silence about which one crossed
   (`packages/derivation/runner.py:812–820`). The charter's "a Part II
   itemization changes the requirement predicate" turns out to need no predicate
   change at all: it needs a second entry in an array.
2. **Value-checked completeness is v4's own addition**, so the ten Part I
   answers stay exactly as committed and the twelve Part II answers (T0-5/T0-6)
   join them as ten-plus-twelve `check: "value"` entries — twenty-two in total.
3. **`itemizations` has no `minItems`**, so a Part II that contributes no
   itemization row is schema-valid and the runner's loop simply does not iterate
   over it.

The existing `line-7-unemployment` itemization is carried forward unchanged,
satisfying the charter's "without losing the existing Part I unemployment
itemization". The v1 title's claim "Part II adjustments are out of scope" is
corrected in the v2 title; v1 remains untouched published history.

#### Line 21 carries no itemization — and why that is correct, not a shortcut

Under v4 an itemization's rows must be `collect_members` over a source family,
and the tie-out invariant requires the row sum to equal the line's published
value (ADR-0036 decision 3; `ITEMIZATION_TIE_OUT_VIOLATION`).

Itemizing line 21 over the Form 1098-E family would therefore raise
`ITEMIZATION_TIE_OUT_VIOLATION` on **exactly the cases this milestone exists to
compute**: the box-1 members sum to the box-1 subtotal, which differs from line
21 whenever the $2,500 cap or the phaseout bites. It is also wrong on the paper:
printed Schedule 1 line 21 is a single entry box with no per-lender detail
[F1040S1 p. 2], so there is nothing on the form to itemize.

Settled: **Part II contributes no itemization row set.** Per-statement
provenance lives where it belongs — in the line-21 rule's own pins and
explanation walk, which pin every Form 1098-E box-1 member finding.

#### The requirement contributor must be the line-21 symbol, not the box-1 subtotal

This is a load-bearing implementation constraint, and it is what makes the
charter's "incomplete authority ⇒ blocked, never not-required" true by
construction rather than by luck.

The runner evaluates the requirement **before** completeness, and a
not-required outcome returns immediately without reading the completeness
answers (`runner.py:822–830`, completeness at line 883). A missing requirement
subtotal, by contrast, blocks `DEPENDENCY_ABSENT` naming it
(`runner.py:793–796`).

`tax.us.2025.schedule1.line21-student-loan-interest` exists **only** when every
eligibility component and all twelve Part II absences answer `yes` — that is the
T0-4 gate. So any incomplete or denied Part II authority makes the line-21
symbol absent, which makes the attachment **block**. Had the trigger instead read
`tax.us.2025.f1098e.box1-subtotal` — which the family publishes regardless of the
answers — a return with a denied component and no unemployment would have
reached the not-required path and reported "Schedule 1 not required" about a
return the engine cannot actually compute.

**Track 2 must use the gated line-21 symbol.** The two requirement subtotals are:

```
tax.us.2025.unemployment.box1-subtotal                 (Part I, unchanged)
tax.us.2025.schedule1.line21-student-loan-interest     (Part II, new)
```

with the existing `strictly_greater_than` comparison against the existing
`tax.us.2025.parameter.default-zero`, unchanged.

**Observation for review, on the Part I side.** The same ordering makes the
*committed* Part I trigger weaker than the Part II one: `unemployment.box1-subtotal`
is published by the closed Form 1099-G family independently of the
`schedule1-part1-scope` answers, so a return with zero unemployment and a `no` on
a Part I absence reaches the not-required path without its completeness being
read. That is **pre-existing at this base, is not introduced by this milestone,
and is not repaired by it** — repairing it would change committed Part I trigger
semantics, which is beyond this milestone's scope. It is named so that review
does not attribute it to the Part II extension, and so that a future Part I
milestone has it on record.

#### The six required case dispositions

| Case | Disposition | Mechanism |
| --- | --- | --- |
| Positive line-21 deduction, no Part I income | **Required** | line-21 subtotal > 0; the unemployment trigger records `over: false`, so the walk shows both outcomes |
| Positive line-21 alongside supported Part I unemployment | **One** composition-complete Schedule 1 carrying both parts | one attachment citizen, two requirement contributors, the Part I itemization retained, twenty-two completeness answers |
| Deduction reduced to zero by the phaseout | **Not required** (when Part I is also zero) | see the justification below |
| Incomplete eligibility or adjustment authority | **Blocked**, never not-required | the line-21 symbol is absent ⇒ `DEPENDENCY_ABSENT` on the requirement, which precedes and preempts the not-required path |
| Closed-empty Form 1098-E family | Line 21 = 0 ⇒ same as the phased-out case | Track 0a: closed-empty authorizes a box-1 subtotal of 0; the T0-2/T0-3 authority is still required, so this is a computed zero, not silence |
| Other Schedule 1 source or adjustment present but unsupported | **Blocked** | a `no` answer blocks the line-21 and line-26 gates, hence the attachment |

**Justification for "not required" at a zero deduction.** [I1040GI p. 88],
General Instructions for Schedule 1: "Use Schedule 1 to report income or
adjustments to income that can't be entered directly on Form 1040, 1040-SR, or
1040-NR… Adjustments to income are entered on Schedule 1, Part II. The amount on
line 26 is entered on Form 1040, 1040-SR, or 1040-NR, line 10." With line 26 = 0
and Part I = 0 there is nothing to report and nothing to enter on Form 1040
line 10. Under ADR-0036 decision 2 the boundary is strictly-greater-than the
cited threshold, which is the same rule the committed Part I trigger already
applies at zero. Under ADR-0036 decision 1 this is **not silence**: not-required
publishes a walkable inapplicability disposition carrying the inputs, the
threshold, the citation, and the per-trigger outcome.

Track 0a's note 9 observed that above the MAGI ceiling the deduction is
*eliminated*, not merely computed to zero. That distinction is real and it is
preserved — but it is carried by the **line-21 rule's** explanation walk, which
shows worksheet lines 4 through 8 and the 1.000 clamp, not by the attachment.
The attachment's own question is only "is there an amount to report", and the
answer at zero is no. Both facts are on the record, each where it belongs.

#### Charter-stop check for this item

Content-level reuse is achieved: **no new attachment schema, no new attachment
ontology, no new mechanism, no new ADR.** Milestone stop conditions 1 and 2 are
not triggered. No unratified-PR content is edited: `attachment-rule.v5` is
diagnosed and left exactly as published.

---

### T0-8 — Form 1040 succession: lines 10, 11a, and 11b (settled)

Owner disposition honoured: **the repair is narrow — add lines 10, 11a, and 11b
and nothing else.** The deduction spine (12e / 13a / 13b / 14 /
`rule.form1040-line15.v2`) is correct at this base and is not touched.

#### Primary source, re-verified for this item

Extracted from the 2025 Form 1040 PDF and the 2025 Instructions for Form 1040 at
authoring time, not inherited from the plan header:

| Where | Printed text, verbatim |
| --- | --- |
| [F1040] p. 1, line 10 | "Adjustments to income from Schedule 1, line 26" |
| [F1040] p. 1, line **11a** | "Subtract line 10 from line 9. This is your adjusted gross income" |
| [F1040] p. 2, line **11b** | "Amount from line 11a (adjusted gross income)" |
| [F1040] p. 2, line 15 | "Subtract line 14 from line 11b. If zero or less, enter -0-. This is your taxable income" |
| [I1040GI] printed p. 33 (footer reads `33`), heading "Total Income and Adjusted Gross Income" | "**Line 10.** Enter any adjustments to income from Schedule 1, line 26, on line 10." |

Two things this reading settles that the charter did not state:

1. **The instructions carry no "Line 11a" or "Line 11b" paragraph at all.** The
   whole "Total Income and Adjusted Gross Income" section of [I1040GI p. 33] is
   the single Line 10 sentence above. The authority for 11a and 11b is therefore
   the **printed form face**, not an instruction paragraph. That matters for the
   citation citizens: their `authority.family` must be the form, and the
   explanation walk must not imply an instruction passage that does not exist.
2. **Line 11b's printed text is a bare carry** — "Amount from line 11a" — with no
   arithmetic, no condition, and no second citation. This is the decisive fact
   for the one-symbol-versus-two-symbols question below.

---

#### The crux, settled first: what AGI does on a return with no Schedule 1

The previous attempt at this item identified the right question — if line 11a
subtracts a line 10 that sums Schedule 1 adjustments, does every existing return
with no Schedule 1 lose its AGI? It is settled here against committed artifacts,
before anything else, because every other T0-8 decision depends on the answer.

##### The finding that dissolves it: at this base there is no such return

**There is already no "return with no Schedule 1" in this engine, and there has
not been one since the Form 1099-G milestone.** Verified against committed
content, not reasoned from the plan:

```
rule.form1040-line9.v7   requires  tax.us.2025.income.additional-income   (hard requires, no guard)
rule.form1040-line8      requires  tax.us.2025.schedule1.line10-additional-income
                         value     ref(tax.us.2025.schedule1.line10-additional-income)
rule.schedule1-line10    requires  tax.us.2025.schedule1.line7-unemployment
                                   + the ten schedule1-part1-scope absences
```

So `tax.us.2025.income.total-income` — the input to today's passthrough AGI —
**already** cannot publish unless the taxpayer has closed the Form 1099-G family
and answered all ten Schedule 1 Part I absences. A return "with no Schedule 1"
is expressed today as a return that closes the family empty and declares the ten
absences, and it receives a **computed zero** at Schedule 1 line 10, at Form 1040
line 8, and hence a real number at line 9.

`rule.schedule1-line10`'s own `notes` state the governing posture in terms:
"Closed-empty unemployment with complete absences publishes explicit zero. **Does
not manufacture zero amounts for unimplemented producers.**"

Adding line 10 on the adjustment side is therefore **the same move the income
side already made**, on the same shape, with the same authority discipline. It is
not a new hazard class.

##### What line 10 evaluates to when the taxpayer has no Schedule 1 adjustments

`0` — a **computed zero**, published, walkable, and backed by declared authority.
Never an implicit zero and never a default.

The chain, using the already-settled T0-4/T0-5/T0-6 citizens:

```
F1098-E family closed empty        ⇒ box1-subtotal = 0                (T0-3, Track 0a)
+ the 17 T0-2/T0-3 components yes  ⇒ line 21 = 0                      (T0-4 gate, worksheet L1 = 0 ⇒ L9 = 0)
+ the 12 Part II absences yes      ⇒ line 26 = ref(line 21) = 0       (T0-6)
                                   ⇒ Form 1040 line 10 = ref(line 26) = 0
                                   ⇒ line 11a = line 9 − 0 = line 9
```

At a zero deduction AGI equals total income, so the *number* every existing
supported return produces is unchanged. What changes is that the number is now
**derived through a line-10 subtraction whose zero is authorized**, instead of
asserted by a passthrough that never asked the question.

##### Absence authority, not an implicit zero — and no new authority at line 10

Three shapes were considered for line 10 and only one survives the engine's own
committed posture.

| Candidate | Verdict |
| --- | --- |
| `optional_default` of 0 on the line-26 symbol, or a `choose` in line 11a falling back to 0 when line 10 is absent | **Rejected.** This is exactly "manufacture zero amounts for unimplemented producers", which `rule.schedule1-line10` forbids by name, and it would let a return with *unanswered* Part II authority publish an AGI as if the answer were known. It also contradicts T0-5's settled "absence authority, not optional defaults". |
| Line 10 carries its own absence vocabulary | **Rejected as redundant.** The Part II completeness question is answered exactly once, at line 26, by the twelve T0-5/T0-6 absences. A second gate at line 10 would re-ask a settled question and create two places for it to disagree. |
| **Line 10 = `ref(line 26)`, hard `requires`, no gate of its own** | **Settled.** Its authority is entirely upstream, which is precisely the committed shape of `rule.form1040-line8` — itself a bare `ref` of Schedule 1 line 10 with a hard `requires` and no absence checks, because line 10 already carries them. Line 10 is to Part II what line 8 is to Part I. |

So the answer to "does this require absence authority rather than an implicit
zero" is: **yes, absence authority — and it already exists.** T0-5 and T0-6
settled it, and T0-8 adds none.

##### How the committed T0-5 and T0-6 settlements bear on it

The load-bearing consequence, verified in content:

**The twelve MAGI absences are already mandatory for every return at this
milestone's integration base.** `rule.ss-benefits-worksheet.json` (v1) `requires`
all twenty-three `ss-benefits-scope` fact types, including the twelve
(`no-sch1-line11-educator` … `no-sch1-line25-other-adjustments`), and publishes
`tax.us.2025.social-security.line6b`, which `rule.form1040-line9.v7` `requires`.
Therefore, at the base, **no return can publish `income.total-income` without
already having answered all twelve.**

That is why T0-5's reuse decision matters here and not merely for naming: because
line 26 gates on the same twelve, **line 26 imposes no requirement on a return
that line 9 did not already impose.** Had T0-5 minted a parallel `slid-magi-scope`
vocabulary, every return reaching AGI would have had to answer the same twelve
questions a second time, and T0-8 would have doubled the entry burden of every
return in the engine as a side effect. The reuse decision is what makes this
repair cheap.

Likewise T0-6's "line 26 = `ref(line 21)` under the twelve-absence gate" means
line 26 inherits its closure authority transitively through line 21 and carries
no `require_closed` of its own — so line 10 inherits a single, already-audited
authority chain rather than a second one.

##### What is genuinely new, stated exactly

One thing, and it is a **fixture-corpus cost, not a semantic break**: a return
that wants an AGI from the successor package must now also carry the Form 1098-E
family (bundle adoption, horizon genesis, closure — closed-empty is fine) and
answer the **seventeen** T0-2/T0-3 components (A1–A10, B1–B5, C1, C2).

Sixteen of the seventeen are **vacuously true** for a taxpayer with no student
loans, and honestly so, because T0-2 wrote the universal quantifier into each
fact type's own title ("for every Form 1098-E box-1 amount recorded in the 2025
Form 1098-E source family"). A1–A10 quantify over recorded statements or their
loans; B2–B5 quantify over "claimed interest" / "claimed amount"; C1 quantifies
over furnished statements; C2 asserts the deductible-interest universe equals the
recorded set, which for a taxpayer with none is true. With zero statements each
is satisfied without asserting anything false.

**The one exception is B1** (`not-claimed-as-dependent`): "Neither the taxpayer
nor, on a joint return, the spouse is claimed as a dependent on another
taxpayer's 2025 return." That is an unquantified proposition about the taxpayer,
and it is a genuine question a no-student-loan return must now answer. A truthful
`no` blocks line 21, hence line 26, hence line 10, hence AGI.

This is recorded plainly rather than smoothed over, and two things bound it:

1. **It is the engine's existing convention, not a new one.** A truthful `no` on
   any of the twenty-three `ss-benefits-scope` answers already makes the SS
   worksheet's `when` guard false, so `social-security.line6b` does not publish,
   so `rule.form1040-line9.v7` blocks `DEPENDENCY_ABSENT` — the entire return's
   total income, today, at this base. "Outside the bounded supported class,
   block; never guess" is the committed posture, and T0-8 extends it without
   changing it.
2. **It is a bounded-class property with a named future exit.** Line 21 is 0
   whenever the family is closed-empty regardless of B1, so a future milestone
   could make the gate condition on a non-empty family. That is **not** proposed
   here: it would re-open T0-4's settled gate, which is out of this unit.

**Finding recorded for review (not a decision, and not a re-settlement):** T0-4's
gate blocks on a `no` in *all* cases, including the closed-empty case where the
deduction is 0 no matter what the answer is. Under T0-8 that propagates to AGI
for every return in the successor package. Track 0b's T0-4 settlement chose
`block` over guard-inapplicable deliberately and with reasons, and this
settlement does not disturb it. It is named here only so review sees the coupling
in one place and can price it as a whole.

##### Which existing fixtures and packaged computations change or break

**None.** Verified against the repository, not assumed.

Published packages are immutable, and every live-integration test pins its own
package version *and* its own registry:

| Test | Adoption | Registry |
| --- | --- | --- |
| `test_f1098_mortgage_interest_line12e_track2.py` | `adopt-core-v29-current.json` | `published-packages.v24.json` |
| `test_form1099r_ira_line4b_track2.py` | `adopt-core-v26-current.json` | its own |
| `test_form1099div_box7_direct_ftc.py` | `adopt-core-v21-current.json` | `published-packages.v16.json` |
| `test_form1099g_box1_schedule1_line7.py` | `adopt-core-v20-current.json` | `published-packages.v15.json` |
| `test_form1099int_box8_line2a.py` | `adopt-core-v19-current.json` | … |
| `test_f1098_mortgage_interest_lifecycle.py` | `adopt-core-v19-current.json` | `published-packages.v14.json` |
| … (every earlier milestone likewise) | its own | its own |

A repository-wide search for consumers of the current tip (`v29` /
`published-packages.v24`) returns exactly three files, all belonging to the
mortgage-interest milestone: its Track 2 test, its generator, and its adoption
fixture. **There is no "current package" pointer that older fixtures follow.**

Consequently:

- **No committed golden, expected report, or presentation model changes.** The
  static AGI values in `packages/sample_data/tax/scenarios/*/expected/report.json`
  and in the `tools/presentation_harness` citation-walk fixtures are computed
  under packages this milestone does not modify.
- `rule.form1040-line11` v1 and `form1040.line-11` v1 stay byte-identical and
  stay adopted in every package up to and including the current tip.
- **The only computations that change are the ones the successor package
  produces**, i.e. this milestone's own Track 2 fixtures — which must extend the
  SSA/IRA/mortgage base corpus with the Form 1098-E family and the seventeen
  components, exactly the additive pattern
  `test_f1098_mortgage_interest_line12e_track2.py` already documents in its own
  module docstring for the SSA corpus.

**Binding consequence for Track 2.** Because AGI now depends transitively on the
Form 1098-E family's closure, the new line-11a/11b form fields **must** declare
`SOURCE_SET_UNCLOSED` among their blocked codes. The published
`form1040.line-11` v1 is on `form-field.v2`, whose blocked-code enum does not
even contain that code (v2 carries the never-emitted `SOURCE_SET_OPEN`; `v3`
replaced it per ADR-0036 production condition 3). An unclosed Form 1098-E family
must render as a blocked AGI naming the closure, never as a silent gap. This is a
second, independent reason the new fields are new citizens on `form-field.v3`
rather than an edit to the old one.

---

#### Sub-question 1 — one AGI symbol, two form-field citizens

**Settled: one symbol (`tax.us.2025.income.agi`) bound by two form-field
citizens, one for line 11a and one for line 11b. No carry rule, no second
symbol.** The foreman's expectation is confirmed, with reasons rather than by
deference.

Why not two symbols with a carry rule:

- **A carry rule would publish a derived finding with no authority content.**
  Printed line 11b is "Amount from line 11a" — no arithmetic, no condition, no
  separate instruction paragraph ([I1040GI p. 33] has none). A rule citizen whose
  entire content is `ref(agi)` adds one node to every explanation walk that
  restates the previous node and answers no question.
- **It would force a re-pin of published history.** `rule.form1040-line15.v2`
  `requires` `tax.us.2025.income.agi`. A distinct line-11b symbol would leave
  line 15 consuming the 11a symbol while the printed form says line 11b, or
  demand a line-15 v3 whose only change is a name. Neither is an improvement;
  the second is out of scope under the owner's narrow disposition.
- **The page break is a presentation fact, and form-field citizens are exactly
  the presentation layer.** The engine's symbols name *meanings*; the form-field
  citizens name *boxes on paper*. One meaning printed in two boxes is the
  canonical case for one symbol and two fields.

**Verified expressible at this base, in code, not assumed.** Three properties of
the committed projector and validator were checked:

1. **Nothing forbids two fields binding one symbol.**
   `package_validation.py` §4 ("Form-field binds symbol closure") checks that the
   symbol is *produced or bound*, and flags `FORM_FIELD_PRODUCER_CONFLICT` only
   when one symbol has **multiple producers**. Two *consumers* are unconstrained.
2. **The projector handles it cleanly.** `presentation_projection.py` iterates
   fields and calls `_one_row(by_symbol.get(symbol, []))` per field; both fields
   resolve the same single row. Citation-site ids are `f"{section_id}-src-{index}"`,
   so they stay distinct per section. `pin_labels` is keyed by bare pin id and
   raises only on *conflicting* labels for one pin; both fields derive identical
   labels from the same finding, so no conflict arises.
3. **The section-id duplicate guard is satisfied.** `_section_id(field)` is
   `f"line-{field['line']}"` and the validator raises on duplicates. `11a` and
   `11b` yield `line-11a` and `line-11b`. Distinct.

**Implementation constraint Track 2 must honour, verified in code.**
`_require_declared_field_citation_chain` requires, for every field bound to a
rule that declares citations, that the field's citation appear **exactly once**
in the owning rule's `citations`. Because both fields join the same owning rule,
that rule must declare **both** the line-11a citation and the line-11b citation,
each exactly once. This is not a workaround: the rule's single publication is
presented at two printed boxes, so citing both is the honest declaration.
Precedent exists — `rule.form1040-line8` already declares two citations (its own
line 8 and Schedule 1 line 10).

#### Sub-question 2 — the existing line-11 artifacts: preserved, superseded by membership

**Settled: `rule.form1040-line11` v1, `form1040.line-11` v1, and
`citation.form1040.line-11` v1 are left byte-identical and are simply not members
of the successor package.** Nothing is edited and nothing is deleted.

This is not an invention; it is the **immediately preceding precedent on this
same spine**, verified by diffing package membership:

```
package.core-calculations.v28 :  form1040.line-12, citation.form1040.line-12, rule.form1040-line12   present
                                 form1040.line-12e, form1040.line-14                                  absent
package.core-calculations.v29 :  form1040.line-12, citation.form1040.line-12, rule.form1040-line12   ABSENT
                                 form1040.line-12e, citation.form1040.line-12e, form1040.line-14      present
```

The mortgage-interest milestone corrected the 2025 deduction line by **minting
new ids** (`form1040.line-12e`, `rule.form1040-line12e`) and **dropping the
mis-numbered trio from successor membership**, leaving the v1 citizens untouched
in the corpus and still adopted by every package up to v28. T0-8 does the same
thing one line higher.

**Therefore: new ids, not version bumps.**

| Citizen | Disposition |
| --- | --- |
| `tax.us.2025.rule.form1040-line11a` | **New id**, publishes `tax.us.2025.income.agi` = `subtract(total-income, line-10 symbol)` |
| `tax.us.2025.form1040.line-11a` | **New id**, `form-field.v3`, binds `income.agi`, `line: "11a"` |
| `tax.us.2025.form1040.line-11b` | **New id**, `form-field.v3`, binds `income.agi`, `line: "11b"` |
| `tax.us.2025.rule.form1040-line10` | **New id**, publishes the Form 1040 line-10 symbol = `ref(schedule1.line26-adjustments)` |
| `tax.us.2025.form1040.line-10` | **New id**, `form-field.v3`, `line: "10"` |
| `tax.us.2025.citation.form1040.line-10 / .line-11a / .line-11b` | **New ids** |
| `rule.form1040-line11` v1, `form1040.line-11` v1, `citation.form1040.line-11` v1 | **Untouched published history; not members of the successor package** |

Two reasons the version-bump alternative was rejected, since the corpus contains
both patterns and the difference is principled:

- The version-successor pattern (`rule.form1040-line9` v2–v7,
  `rule.form1040-line15` v2) is used when the **printed line number is unchanged**
  and only the derivation grows. Here the printed line number is the very thing
  being corrected: there is no line "11" on the 2025 form.
- Keeping the id `rule.form1040-line11` for a rule that computes printed line 11a
  would hide the correction inside a version number, where a reader chasing
  "line 11a" cannot find it. The v29 precedent puts the correction in the id.

**The symbol is deliberately *not* re-minted.** `tax.us.2025.income.agi` stays
the AGI symbol. The successor package therefore has exactly one producer of it
(the old rule is not a member), so **no `conflict_semantics` entry is needed** —
verified against the validator's `FORM_FIELD_PRODUCER_CONFLICT` condition, and
against v29, whose only `conflict_semantics` entry is for
`tax.us.2025.schedule-a.total`.

#### Sub-question 3 — `rule.form1040-line15.v2` is not re-pinned and not re-versioned

**Settled: line 15 is untouched.** It keeps `requires`
`tax.us.2025.income.agi` and `tax.us.2025.deductions.line-14`.

The charter framed this as a provenance question, and the provenance is already
correct once sub-question 1 is settled: `income.agi` **is** the line-11b amount,
because line 11b is definitionally the line-11a amount and both are the same
published finding. The printed "Subtract line 14 from line 11b" is honoured in
the walk by the `form1040.line-11b` field citizen, which shows the amount at its
printed box with its own citation.

Re-versioning line 15 to consume a distinct line-11b symbol would be arithmetic
churn on a rule the mortgage-interest milestone just repaired, would touch the
deduction spine the owner and the charter's non-goals both put out of scope, and
would buy provenance the form-field citizen already carries.

#### Sub-question 4 — the `line` attribute convention

The charter reports two rival conventions and asks for one. The corpus, read in
full (41 form-field citizens), shows the apparent conflict is not a conflict:

| Pattern | Examples |
| --- | --- |
| **Bare printed line, for Form 1040 fields** | `9`, `11`, `12`, `12e`, `13a`, `13b`, `15`, `16`, `1a`, `2a`, `2b`, `3a`, `3b`, `4b`, `6a`–`6d`, `7a`, `7b`, `8`, `20`, `22` |
| **Form-qualified prefix, for non-1040 forms** | `sch1-7`, `sch1-10`, `sch-d-13`, `sch-d-15`, `sch-d-16`, `Sch3-1`, `Sch3-8`, `1a-h`, `8a-h`, `1b-h`, `8b-h` |
| **One Form 1040 outlier** | `1040-14` |

`1040-14` is not a third convention; it is the documented **collision escape
hatch**, and the citizen says so in its own `description`: it disambiguates from
the already-published `tax.us.2025.schedule-d.line-14`, which renders bare `14`
and "would otherwise collide on the shared `line-{n}` section-id convention once
both are simultaneously adopted". That collision is real —
`_section_id(field)` is `f"line-{field['line']}"` and the projector raises
`duplicate section id` — and it is the whole reason for the prefix.

**Settled rule, which is what the corpus already follows:** a Form 1040 field
carries the **bare printed line**, unless the resulting `line-{n}` section id
would collide with another citizen adopted in the same package, in which case it
carries the `1040-` prefix and says why in its `description`.

Applied here, with the collision check actually run against all 41 citizens:

| New field | `line` | Section id | Collision? |
| --- | --- | --- | --- |
| `form1040.line-10` | `10` | `line-10` | **None.** `tax.us.2025.schedule1.line-10` carries `sch1-10`, so it renders `line-sch1-10`. Bare `10` is free. |
| `form1040.line-11a` | `11a` | `line-11a` | None. |
| `form1040.line-11b` | `11b` | `line-11b` | None — and free even if `form1040.line-11` (`line-11`) were ever co-adopted, which it is not. |

So all three take the bare printed line. **No third convention is introduced, and
the `1040-` prefix is not used** — using it here would be cargo-culting the
escape hatch in the absence of the collision that justifies it.

#### Case dispositions for this item

| Case | Line 10 | Line 11a / 11b | Line 15 |
| --- | --- | --- | --- |
| Supported return, positive line-21 deduction | published value | line 9 − line 10 | unchanged mechanics |
| Supported return, no Schedule 1 adjustments (F1098-E family closed empty, all authority `yes`) | **computed zero** | equals line 9 | unchanged |
| Deduction phased out to zero at or above the MAGI ceiling | computed zero | equals line 9 | unchanged |
| Any T0-2/T0-3/T0-5 component answered `no` | **blocked** (line 21 → line 26 → line 10) | blocked, `DEPENDENCY_ABSENT` | blocked |
| Any such component unanswered | **blocked** `DEPENDENCY_ABSENT` naming it | blocked | blocked |
| Form 1098-E family not closed | blocked | blocked; the field must declare **`SOURCE_SET_UNCLOSED`** | blocked |
| Schedule 1 not required (line 26 = 0 and Part I = 0) | still a **published computed zero** on Form 1040 line 10 | equals line 9 | unchanged |

The last row is worth stating explicitly because it is the one place where the
attachment disposition and the form line diverge: under T0-7 the Schedule 1
*attachment* is **not required** at a zero line 26, while Form 1040 **line 10
still publishes a computed zero**. These are consistent, not contradictory —
ADR-0036 decision 1 makes not-required a walkable inapplicability disposition of
the *attachment*, whereas line 10 is a form line whose value is 0. Track 2's
presentation evidence should show both in one walk so the pairing is on the
record.

#### Charter-stop check for this item

None of the milestone stop conditions is triggered by T0-8:

- **The narrow 10/11a/11b repair does not need broader form-spine work.** Line 15
  is untouched; line 9 is untouched; the 12e/13a/13b/14 spine is untouched. The
  only citizens introduced are the three lines the owner authorized, their
  citations, and their form fields.
- **No ADR is implied.** No new schema, operator, disposition, error code, or
  ontology. `form-field.v3`, `rule-artifact.v4`, and `citation.v1` are all
  already published and already used at this base; every mechanism relied on
  (two consumers of one symbol, dropping a superseded citizen from successor
  membership) was verified as existing behaviour of the committed validator,
  projector, and packages. The milestone's single allowed ADR remains spent on
  T0-4's multiply/divide extension.
- **No unratified-PR content is edited.** `ss-benefits-scope`, the SSA line-9
  successors, the Schedule A citizens, `rule-artifact.v4`, and
  `rule.form1040-line15.v2` are all read and none is modified.
- **`tax.us.2025.schedule1.line10-additional-income` is not re-pointed, not
  re-versioned, not renamed, and not consumed by anything this item introduces.**
  Form 1040 line 10 consumes `tax.us.2025.schedule1.line26-adjustments` only.
  The two Schedule 1 parts stay disjoint and Track 0a's no-cycle proof stands.
- **No version numbers are allocated**, consistent with the plan's rule that
  allocation waits until PR #163 and PR #168 land and this branch is rebased.
- No prototype is required or requested, and no sub-agent was used.

#### Open items and escalations from T0-8

**None blocking.** One coupling is recorded above for the foreman and for review,
without being decided here: T0-4's settled `block`-on-`no` gate means a truthful
`no` on B1 (`not-claimed-as-dependent`) removes AGI from a return that has no
student loans at all. That is the engine's existing bounded-class posture rather
than a new hazard, the alternative sits inside T0-4's settled scope, and this
unit does not re-open it.

## Track 0 reopened — owner review findings and dispositions (Track 0c charter)

**The Track 0 "settled" declaration recorded above is withdrawn.** Owner review
returned three findings, two at P1. All three are accepted as correct. This
section records the findings, the foreman's pricing of each against the
**rebased** base (`origin/main` after PR #163 and PR #168 merged), the required
dispositions, and the five mandatory Track 0 outputs that must exist before
Track 0 may be declared settled again.

Nothing in this section allocates a schema, rule, package, registry, attachment,
or form-field version number.

### Why this was missed — foreman process correction

The three findings were all predictable from the standing guidance in
`docs/roles/qualitative-review.md`. The failure was not intuition; it was that
the guidance was never forced into a concrete Track 0 *output*. The tell is in
the settlement's own prose: the phrases "known limitation, recorded rather than
engineered around", "existing bounded-class posture", and "none blocking" each
mark a place where a counterexample was owed and not demanded. Two of the three
findings were, in fact, already written down by the foreman as "open items
carried out of Track 0" — and a coupling recorded as an open item is a coupling
that has not been settled.

**Standing rule, adopted now:** Track 0 may not be marked settled while it
contains a known semantic coupling, unless the plan carries a counterexample
demonstrating that the coupling is correct. "Recorded" is not "settled".

### F1 (P1) — Statement-set-dependent authority is not bound to the statement set

**Finding.** The A/B/C eligibility facts are keyed by tax year alone while
asserting something about *every recorded statement*. Adding a Form 1098-E
invalidates family closure and the box-1 subtotal, but leaves the prior
eligibility answers current, so after re-closing they silently authorize a
statement they were never asserted about.

**Counterexample (accepted, and it does reproduce under the settled design).**
Attest A8 `lender-not-related-person` = `yes`; close a one-member horizon H1;
compute. Add a second statement whose lender *is* a related person; close H2.
The A8 fact is keyed `{tax-year: 2025}`, is unaffected by the horizon change,
remains current, and now covers a loan it was never asserted about.

**Required property.** Statement-set-dependent authority must be displaced, or
become unusable, whenever family membership changes.

**Pricing — the stop condition does not fire.** The charter's stop condition
asks whether this requires new substrate. It does not. The identity-key
vocabulary already admits `{"kind": "entity", "name": "family-horizon"}`, and
the ratified line already uses it **37 times** — every `*.source-closure` fact
type in the corpus is keyed `['family-horizon', 'tax-year']` (`f1098.bundle.json`,
`ssa1099.bundle.json`, the ten `f1099b-covered-*` bundles, and the rest). What is
novel here is only the *application*: horizon-binding has so far been used
exclusively for the closure attestation itself, never for a substantive
declaration. Extending it to substantive declarations is content-level reuse of
ratified substrate, needs no evaluator change, and needs no ADR. This matters,
because the alternative the finding names — per-statement authority plus a
genuine aggregate mechanism — *would* require new substrate: the evaluator has
no categorical or boolean aggregate at all (`collect` decimal-coerces every row,
`packages/derivation/evaluator.py:118`; `count` returns only a length).

**Disposition.** Re-key the statement-set-dependent components to
`['family-horizon', 'tax-year']`. The old attestation is then simply not current
for the new horizon, by exactly the mechanism that already invalidates closure,
and the counterexample resolves: A8@H1 does not answer for H2.

**Which components are statement-set-dependent — sixteen of seventeen.**
Track 0c must confirm this classification component by component, but the
foreman's reading of the settled roster is:

* **A1–A10 — statement-set-dependent.** Every one quantifies over the recorded
  set, explicitly or by construction (A1: "…covered by every recorded
  statement").
* **B2–B5 — statement-set-dependent.** Each quantifies over *claimed* interest
  ("No claimed interest was paid from…"), and the claimed interest is exactly
  the recorded box-1 set.
* **C1 — statement-set-dependent.** Quantifies over furnished Forms 1098-E.
* **C2 — statement-set-dependent, and most sharply so.** It names the recorded
  set in its own text: no deductible interest "other than the amounts reported
  in box 1 of the recorded Forms 1098-E".
* **B1 `not-claimed-as-dependent` — the sole exception.** It is a fact about the
  taxpayer's status on someone else's return. It is genuinely return-scoped and
  correctly keyed by tax year alone. It is invalidated only by correction.

That B1 is the one component that is *not* statement-set-dependent is not a
coincidence — it is the same fact that F2 shows must not gate the closed-empty
route. The two findings meet at the same component from opposite directions.

### F2 (P1) — A closed-empty family must not let eligibility control AGI

**Finding.** Under the settled design, `B1 = no` blocks line 21, line 26,
line 10, and therefore AGI, even when the Form 1098-E family is closed empty.
Calling that an existing bounded-class posture does not make it semantically
correct: with no deductible interest anywhere, dependent status cannot change
line 21 from zero. The prior settlement recorded this as an "open coupling"
rather than a defect — precisely the failure named above.

**Disposition — a real authority branch, with provenance.** A closed-empty
Form 1098-E family, together with C2 authority that there is no unreported
deductible interest, must produce a **canonical line 21 zero** without consulting
any loan-eligibility answer. The zero must carry closure and C2 provenance; it is
an authorized zero, not a manufactured one, and not a default.

Note what horizon-binding from F1 buys here for free: C2 keyed to the *empty*
horizon reads "the taxpayer has no deductible 2025 student loan interest other
than the amounts reported in box 1 of the recorded Forms 1098-E", of which there
are none — i.e. exactly "no deductible student loan interest at all". The empty
horizon makes C2 say the strongest true thing on its own. The two dispositions
compose rather than compete.

**A second correction this exposes, which Track 0c must settle.** `B1 = no` is
not an "unsupported, therefore block" condition even on a **non-empty** family.
Being claimed as another taxpayer's dependent makes the deduction zero as a
matter of law, not merely uncomputable by this engine. So B1 should never block:
it should *select* zero. That is a stronger and simpler result than the minimal
fix, and it distinguishes B1 from B3/B4/B5, which reduce the includible amount
and therefore genuinely do block. Track 0c must decide, for every component,
whether a `no` means **legal zero** or **unsupported → block**, and say why.
The prior settlement decided this uniformly and therefore decided it wrongly.

### F3 (P2) — Reopen the shared Schedule 1 absence decision

**Finding.** T0-5 chose to reuse `ss-benefits-scope`'s twelve Schedule 1
absences over minting a parallel vocabulary. That choice was priced against a
world in which the SSA content sat in an unratified PR #163. **PR #163 merged
2026-08-10.** Both dependencies are now ratified, so the constraint that drove
the decision no longer exists and the decision must be re-priced.

**The authority mismatch is confirmed in the rebased content, not merely
suspected.** The twelve fact types are named
`tax.us.2025.ss-benefits-scope.no-sch1-line11-educator` … `no-sch1-line25-other-adjustments`,
and each carries the declared title *"Social Security Benefits Worksheet
completeness component: … for the bounded Social Security worksheet claim."*
A tax-year-only identity key does not broaden that declared meaning; storage
shape cannot redefine meaning; and a note added by a downstream student-loan
consumer cannot retroactively widen an upstream declaration. Reuse as settled
fails the claim-reuse proof at the third leg — same proposition, same lifecycle,
but **not** the same declared authority scope.

**Pricing — the blast radius is three files.** Every reference to the twelve
lives in `packages/content/tax/2025/ss-benefits-scope.bundle.json` (12
declarations), `packages/content/tax/2025/rule.ss-benefits-worksheet.json` (60
references), and `tests/test_ssa1099_benefits_line6_track2.py`. Nothing else in
the corpus touches them.

**Disposition.** Adopt a **shared return-level successor**: neutral fact types
whose declared title states the proposition without naming a consuming
worksheet, required by both the Social Security worksheet and the student-loan
MAGI base. The SSA-scoped originals are superseded. A bridging rule that
republishes the SSA-scoped facts under a neutral symbol is **rejected** — it
leaves the mismatched declaration one hop upstream and repairs scope with a
downstream note, which the finding forbids by name. Track 0c must confirm this
against the supersession policy actually declared on the twelve (`free`) and
must price the resulting version churn, which now legitimately reaches ratified
SSA content.

### Mandatory Track 0 outputs — standing, and required before re-settlement

Track 0 is not settled until all five exist in this plan.

1. **Authority-lifecycle table.** For every contributed fact: meaning, scope,
   what it depends on, and *what invalidates it*. This is the output that would
   have exposed F1 — sixteen components depend on a changing statement set while
   keyed only by tax year.
2. **Empty/nonempty authority matrix.** At minimum the four rows: closed-empty
   with C2 present; closed-empty with C2 absent; non-empty and eligible;
   non-empty and ineligible. The first row is what makes F2 unmissable; the last
   row must be explicitly decided per component rather than uniformly.
3. **Late-authority counterexample.** Every aggregate declaration walked on paper
   through **attest → close → compute → add member → reclose → recompute**,
   naming exactly which prior facts become unusable at each transition. If any
   answer is "it remains current", Track 0 cannot close.
4. **Claim-reuse proof.** Reuse requires three independent matches: same
   real-world proposition, same identity and lifecycle, **and** same declared
   authority scope and explanation. The prior settlement checked the first two
   and treated the SSA-specific title as cosmetic.
5. **Neighboring-capability dependency diff.** What AGI requires on a return with
   *no* student-loan activity, before and after this design. The diff as settled
   reads: *before*, AGI does not depend on student-loan eligibility; *after*, AGI
   requires 1098-E closure plus seventeen student-loan answers including B1. Any
   new feature-specific prerequisite on a neighboring capability requires
   justification and triggers a blast-radius review.

### Track 0 adversarial closure — required declaration

This block must appear, fully discharged, in the re-settlement. Current status:

```
## Track 0 adversarial closure
- Late-member lifecycle:                    FAIL — F1, counterexample reproduces
- Closed-empty route:                       FAIL — F2, B1 suppresses AGI
- Neighboring capability dependency diff:   FAIL — F5 diff unjustified
- Reused-claim semantic/lifecycle equiv.:   FAIL — F3, declared scope mismatch
- Known limitations affecting correctness:  owner-disposition required
```

### Track 0c work items

* **T0c-1** — Authority-lifecycle table for all seventeen components plus
  closure and the subtotal; confirm or correct the sixteen-of-seventeen
  classification; re-key the statement-set-dependent components to
  `['family-horizon', 'tax-year']`; discharge output 3 on A8 and C2 explicitly.
* **T0c-2** — Empty/nonempty authority matrix; specify the closed-empty
  canonical-zero branch with closure and C2 provenance; decide **per component**
  whether `no` means legal zero or unsupported-block, and settle B1 as legal
  zero if the law supports it.
* **T0c-3** — Re-price the shared absence decision; specify the return-level
  successor, the supersession of the twelve SSA-scoped originals, and the
  version churn reaching ratified SSA content; discharge output 4.
* **T0c-4** — Neighboring-capability dependency diff, before and after, with the
  post-disposition figure; justify every remaining prerequisite AGI gains on a
  return with no student-loan activity.
* **T0c-5** — Restate the affected T0-2/T0-5/T0-8 settlements and the affected
  SLI-C2/C5/C6/C8 contracts; re-run the adversarial-closure declaration; confirm
  whether the ADR budget is still sufficient (F1 and F2 are expected to need no
  ADR; F3 may).

### Carried forward unchanged

The `attachment-rule.v5` provenance defect recorded by T0-7 remains open and is
untouched by these findings.

### Rebase record

Rebased `--onto origin/main` from `b25562f`; nine commits replayed, one conflict
in `docs/phase-state.md` resolved in favour of this milestone. The prior base was
**not** an ancestor of `origin/main` because the mortgage milestone was curated
before merge. Delta verified against the rebased base: the evaluator operator set
is unchanged (still no `multiply`, `divide`, or `min`, and still no categorical
or boolean aggregate); `rule.form1040-line11.json` is unchanged and still
publishes AGI as a bare `ref` passthrough of total income; the twelve
`ss-benefits-scope` absences are present and unchanged. Two changes on the
ratified line that Track 1 must respect and that post-date the settlement:
`CURRENT_RECORD_SCHEMA` advanced to **`derivation-record.v6`** (was v5), and
`packages/tax/ssa_benefits.py` was substantially reduced, its test-only
enforcement surface removed. Version tips on the rebased base: core-calculations
**v29**, published **v24**, release **v22**, `rule-artifact.v4`,
`attachment-rule.v6`, `form-field.v3`; highest **allocated** fact-type schema is
`fact-type.v3`, though all content still declares `fact-type.v2`.

---

## Track 0c settlement — T0c-1 (authority lifecycle and horizon re-keying)

This unit settles mandatory Track 0 output 1 (authority-lifecycle table) and
output 3 (late-authority counterexample), and settles the re-keying disposition
F1 requires. It allocates no version numbers and writes no content.

Everything below was verified against the worktree at `0ce6187`; file and line
references are to that commit.

### T0c-1.1 — Classification: confirmed sixteen of seventeen, with one ground corrected

The foreman's classification is **confirmed as to outcome for all seventeen
components**. One component (C1) is confirmed on a **different ground** than the
one offered; the offered ground, taken literally, would have made C1
return-scoped.

The controlling text is not only each component's legal condition but the T0-2
settlement's own scope constraint: *"Each component's title carries the
universal quantifier explicitly — 'for every Form 1098-E box-1 amount recorded
in the 2025 Form 1098-E source family'"*. A fact whose declared title names the
recorded family is, by its own declaration, an assertion about that family's
current membership. That declaration is the primary evidence for sixteen of the
rows below; the per-component text is the confirming evidence.

| # | What the settled definition text actually quantifies over | Class |
| --- | --- | --- |
| A1 | Explicit: "the interest payments covered by **every recorded statement**". | statement-set-dependent |
| A2 | Explicit: "**Every box-1 amount** was paid during 2025…". | statement-set-dependent |
| A3 | "**Each loan** was taken out solely…". The loans are reachable only through the recorded statements; the set of loans is a function of the recorded set. | statement-set-dependent |
| A4 | "**The expenses** were paid or incurred within a reasonable period…" — no quantifier in the sentence itself; "the expenses" are A3's expenses, i.e. those of the loans behind the recorded set. Dependent **by construction**, and made explicit by the mandated title. | statement-set-dependent |
| A5 | "**The student** was the taxpayer…" — per loan, therefore per recorded statement's loans, by the same construction as A4. | statement-set-dependent |
| A6 | Same construction as A5: a property of the student of each loan behind the recorded set. | statement-set-dependent |
| A7 | Same: a property of the institution for each loan behind the recorded set. | statement-set-dependent |
| A8 | Explicit: "**No recorded statement's** loan was from a related person". | statement-set-dependent |
| A9 | Explicit: "**No recorded statement's** loan was made under a qualified employer plan…". | statement-set-dependent |
| A10 | Per loan ("…were not less than **the loan proceeds**"), therefore per recorded statement's loans. | statement-set-dependent |
| B1 | "Neither the taxpayer nor, on a joint return, the spouse **is claimed as a dependent on another taxpayer's 2025 return**." The sentence names no loan, no statement, no interest, and no family. Its truth-maker is a *different return*. | **return-scoped — the sole exception** |
| B2 | "**No claimed interest** was paid from…" — the claimed interest is exactly the recorded box-1 set (T0-3: box 1 is the whole reported-interest boundary). | statement-set-dependent |
| B3 | "No **claimed interest** was paid by the taxpayer's employer…". Same. | statement-set-dependent |
| B4 | "**No claimed amount** is an allowable deduction under any other provision…". Same. | statement-set-dependent |
| B5 | "**No claimed interest** was paid through … the NHSC Loan Repayment Program…". Same. | statement-set-dependent |
| C1 | **Ground corrected.** C1's own text quantifies over forms *furnished* — "No 2025 Form 1098-E **furnished to the taxpayer** has box 2 checked" — not over forms *recorded*. Read on its face that universe does not move when the recorded set moves, and C1 would be return-scoped. It is nevertheless statement-set-dependent, for a stronger reason: the family closure claim asserts that the furnished set and the recorded set are coextensive as of the keyed horizon ("Every amount reported in box 1 of a Form 1098-E furnished to the taxpayer for tax year 2025 is recorded as a statement item as of the keyed horizon"). A membership addition is therefore precisely the event that says the taxpayer held a furnished form they had not accounted for when they answered C1. C1 is dependent **through closure**, not through its own quantifier. | statement-set-dependent |
| C2 | Explicit, and most sharply: "…other than the amounts reported in box 1 of **the recorded Forms 1098-E**". | statement-set-dependent |

**Settled: sixteen statement-set-dependent, B1 alone return-scoped.** No
component is reclassified. The C1 correction matters because it is the one row
whose dependence survives only as long as the closure claim's coextension
wording survives; if a later unit weakens that wording, C1 must be re-examined.

### T0c-1.2 — The re-keying, and the substrate it stands on

**Settled.** The sixteen statement-set-dependent components take identity keys

```
[ {kind: entity, name: family-horizon, entity_kind: kernel.family-horizon},
  {kind: literal, name: tax-year, values: ["2025"]} ]
```

B1 keeps `[{kind: literal, name: tax-year, values: ["2025"]}]` unchanged.

Verified as existing substrate, not proposed substrate:

* **The shape is in the ratified corpus.** `packages/content/tax/2025/f1098.bundle.json`
  declares `tax.us.2025.f1098.source-closure` with exactly
  `[{name: family-horizon, kind: entity, entity_kind: kernel.family-horizon},
  {name: tax-year, kind: literal, values: ["2025"]}]`, and
  `ssa1099.bundle.json` declares `tax.us.2025.ssa1099.source-closure` with the
  identical pair. `kernel.family-horizon` appears 44 times across
  `packages/content`.
* **The schema admits it, on both allocated surfaces.** `fact-type.v2`
  (`packages/schemas/kernel/fact-type.v2.schema.json`) types an entity key as
  `{name, kind: "entity", entity_kind: string minLength 1}` with no restriction
  on which entity kinds may appear and no coupling to `nature` or
  `value_schema`. A `determinable` component with `value_schema
  {"enum":["yes","no"]}` keyed on `kernel.family-horizon` is admissible.
  `fact-type.v3` narrows `entity_kind` to the dotted-id pattern
  `^[a-z][a-z0-9]*(\.[a-z0-9-]+)+$`, which `kernel.family-horizon` matches, so
  the re-keying does not become inadmissible if content later migrates. (Track 1
  should note that `fact-type.v3` is a *distinct, unrelated* surface — its own
  description says so — and drops `version`, `optional_default`, and
  `source_amount`; this settlement stays on `fact-type.v2`, as all content does.)
* **The displacement mechanism is generic in the kernel, not closure-specific.**
  This is the load-bearing verification and it was the open question. Fact
  individuation (`packages/kernel/facts.py:190–216`) walks *every* identity key
  of *every* fact type and, for entity keys, binds one fact per entity of that
  kind, recording `individuated_by`. Nothing there is aware of closure.
  `packages/kernel/findings.py:745–757` marks the predecessor horizon entity
  `status="superseded"` on every member transition.
  `packages/kernel/currency.py:151` adds every superseded entity id to the
  displacement roots, and `currency.py:117–134` builds individuation edges from
  the **full historical lattice** (`include_displaced=True`) so the edge from a
  now-superseded entity to the findings answering facts it individuates still
  exists. Therefore **any** fact keyed on `kernel.family-horizon` is displaced
  when that horizon is superseded — the closure fact has no privilege here, it
  is simply the only fact type that has so far used the key.
* **Marshalling honours it with no change.** `packages/derivation/marshal.py:222–226`
  builds the run context's inputs from `currency.current_finding_ids` alone; a
  displaced finding is never offered to a binding, and `marshal.py:236–241`
  leaves the binding unbound so the runner records `DEPENDENCY_ABSENT` rather
  than inventing a value. The legacy fallback path (`marshal.py:282–307`) also
  iterates `current_findings` and is likewise safe.

No evaluator change, no kernel change, no schema change, no ADR. The foreman's
pricing is confirmed: this is content-level reuse of ratified substrate.

**One substrate observation, recorded because it bounds the claim.**
`superseded_horizon_ids` (`packages/kernel/horizons.py:71`) is defined and has
**no caller anywhere in `packages/`**. Displacement does not run through it; it
runs through the entity lattice as traced above. The horizon-currency filter in
`packages/derivation/source_authority.py:141–163` (`record.horizon_id == current`)
is a *second*, closure-only mechanism reached through a
`source-closure-mapping.v2` citizen's `closure_horizon_key`. The sixteen
components get no such mapping and need none — they are protected by
displacement, which is the stronger of the two, because a displaced finding never
reaches the run at all.

### T0c-1.3 — Authority-lifecycle table (mandatory output 1)

Nineteen rows: the seventeen components, the family closure attestation, and the
box-1 subtotal. The member box-1 fact is included as a twentieth row because it
is contributed and its lifecycle is what the other rows react to. Scope is stated
as the settled identity key.

| Fact | Meaning | Scope (identity key) | Depends on | What invalidates it |
| --- | --- | --- | --- | --- |
| `f1098e.box1-interest` (member) | Box-1 interest on one furnished statement from one filer | `filer`, `statement`, `tax-year` | The statement citizen the taxpayer individuated | A later finding for the same fact (a CORRECTED statement, or a re-assertion); a member-transition `remove` withdrawing the fact. **Not** invalidated by other statements arriving |
| `f1098e.source-closure` | Every furnished 2025 Form 1098-E box-1 amount is recorded as of this horizon | `family-horizon`, `tax-year` | The membership of the 1098-E family at the keyed horizon | Any member transition on the family (add, remove, reclassify): the predecessor horizon entity is superseded and this finding is displaced |
| `f1098e.box1-subtotal` (derived, not contributed) | Multi-filer sum of current members, admitted only against current closure | derived publication over the family | Closure at the current horizon plus every current member finding | Displacement of the closure finding; displacement or correction of any member finding; any member transition |
| A1 `legally-obligated` | Taxpayer (or spouse, joint) is legally obligated for the interest covered by every recorded statement | `family-horizon`, `tax-year` | The recorded statement set | Member transition (horizon supersession); correction of the answer |
| A2 `interest-paid-in-2025` | Every box-1 amount was paid in 2025 by or for the taxpayer | `family-horizon`, `tax-year` | The recorded statement set | Member transition; correction |
| A3 `proceeds-solely-qualified-expenses` | Each loan behind the recorded set was taken out solely for qualified education expenses | `family-horizon`, `tax-year` | The recorded statement set (through its loans) | Member transition; correction |
| A4 `expenses-within-reasonable-period` | Those expenses fall within a reasonable period of each loan | `family-horizon`, `tax-year` | The recorded statement set (through its loans) | Member transition; correction |
| A5 `student-relationship-when-incurred` | For each loan, the student was the taxpayer, spouse, or dependent when the loan was taken out | `family-horizon`, `tax-year` | The recorded statement set (through its loans) | Member transition; correction |
| A6 `eligible-student` | For each loan, the student was an eligible student enrolled at least half-time | `family-horizon`, `tax-year` | The recorded statement set (through its loans) | Member transition; correction |
| A7 `eligible-educational-institution` | For each loan, the education was provided by an eligible educational institution | `family-horizon`, `tax-year` | The recorded statement set (through its loans) | Member transition; correction |
| A8 `lender-not-related-person` | No recorded statement's loan was from a related person | `family-horizon`, `tax-year` | The recorded statement set (through its lenders) | Member transition; correction |
| A9 `not-qualified-employer-plan-loan` | No recorded statement's loan was under a qualified employer plan | `family-horizon`, `tax-year` | The recorded statement set (through its loans) | Member transition; correction |
| A10 `expenses-not-reduced-below-loan` | For each loan, adjusted qualified expenses were not less than the proceeds | `family-horizon`, `tax-year` | The recorded statement set (through its loans) and the taxpayer's tax-free assistance | Member transition; correction |
| B1 `not-claimed-as-dependent` | Neither taxpayer nor spouse is claimed as a dependent on another taxpayer's 2025 return | `tax-year` **only** | Another taxpayer's return; nothing in this workspace | **Correction alone.** No 1098-E event invalidates it, and that is correct |
| B2 `no-qtp-tax-free-earnings-paid-interest` | No claimed interest came from tax-free QTP earnings | `family-horizon`, `tax-year` | The recorded box-1 set (what "claimed" denotes) | Member transition; correction |
| B3 `no-employer-educational-assistance-interest` | No claimed interest was paid by the employer under an educational assistance program after 2020-03-27 | `family-horizon`, `tax-year` | The recorded box-1 set | Member transition; correction |
| B4 `no-other-provision-deduction` | No claimed amount is deductible under another provision or used in another deduction | `family-horizon`, `tax-year` | The recorded box-1 set and the rest of the return | Member transition; correction |
| B5 `no-loan-repayment-assistance-payments` | No claimed interest was paid through NHSC or a similar LRAP | `family-horizon`, `tax-year` | The recorded box-1 set | Member transition; correction |
| C1 `no-box-2-checked` | No furnished 2025 Form 1098-E has box 2 checked | `family-horizon`, `tax-year` | The furnished set, held coextensive with the recorded set by the closure claim | Member transition; correction |
| C2 `no-unreported-deductible-interest` | No deductible 2025 student loan interest exists outside box 1 of the recorded statements | `family-horizon`, `tax-year` | The recorded statement set | Member transition; correction |

Two lifecycle facts the table makes visible and that later units must not undo:

1. **A same-member value correction does not advance the horizon** (ADR-0017 §4,
   already relied on by T0-1 for closure). A CORRECTED Form 1098-E that changes
   only an amount therefore does **not** invalidate any of the sixteen. This is
   semantically right: the loans and lenders the sixteen speak about are
   unchanged.
2. **A member `remove` does advance the horizon** and therefore does invalidate
   the sixteen, even though shrinking the recorded set can only make a universal
   assertion *weaker*, so the old answers would still be true. This settlement
   accepts the over-strictness rather than introducing a second, direction-aware
   invalidation rule. It is one rule, it never authorizes an unasserted
   statement, and it fails safe.

### T0c-1.4 — Late-authority counterexample (mandatory output 3), walked

Walked as **attest → close → compute → add member → reclose → recompute**, twice:
once under the withdrawn tax-year-only keying, once under the settled keying.
A8 and C2 are walked explicitly, as the charter requires; the paragraph after
states why the walk generalizes to the other fourteen without repetition.

Setup common to both walks: statement S1 from filer F1, box 1 = $900; horizon
genesis H1 on the 1098-E family; the second statement S2 from filer F2 is from a
**related person**, so the true A8 answer over {S1, S2} is `no`, and S2 also
carries $300 of interest the taxpayer never told the engine about, so the true
C2 answer over {S1} was false in retrospect.

**Walk 1 — tax-year-only keying (the withdrawn design).**

| Step | A8 | C2 | Other authority |
| --- | --- | --- | --- |
| attest | `A8|tax-year=2025` = yes, current | `C2|tax-year=2025` = yes, current | box-1 S1 current |
| close | unchanged | unchanged | `source-closure|family-horizon=H1,tax-year=2025` = true, current |
| compute | read, pinned | read, pinned | line 21 published over subtotal 900 |
| add member (S2) | **still current** — no individuation edge to H1, no later finding for the same fact | **still current** | H1 entity superseded ⇒ closure@H1 displaced ⇒ subtotal and the line-21 publication displaced along derivation edges |
| reclose | still current | still current | `source-closure|family-horizon=H2` = true |
| recompute | bound from the H1-era finding | bound from the H1-era finding | line 21 recomputed over subtotal 1200 |

Facts unusable at each transition, before the fix: **at "add member", exactly
three things** — the H1 closure finding, the box-1 subtotal, and the prior
line-21 publication. Nothing else. **A8 and C2 remain current**, and the
recomputation authorizes $1,200 of interest on attestations made about $900 of
it. The finding is confirmed: the counterexample reproduces exactly as stated,
and it reproduces for all sixteen, not only A8.

**Walk 2 — settled keying (`family-horizon`, `tax-year`).**

| Step | A8 | C2 | Other authority |
| --- | --- | --- | --- |
| attest | `A8|family-horizon=H1,tax-year=2025` = yes, current | `C2|family-horizon=H1,tax-year=2025` = yes, current | box-1 S1 current. **Ordering constraint:** horizon genesis must precede the attestation, since the key names H1 |
| close | unchanged | unchanged | closure@H1 = true |
| compute | read, pinned | read, pinned | line 21 published over subtotal 900 |
| add member (S2) | **displaced.** H1 entity → `status="superseded"` (`findings.py:745–757`); `currency.py:151` roots it; the individuation edge H1 → this finding exists because `facts.py:190–216` individuates A8 by its `family-horizon` entity key exactly as it individuates closure | **displaced**, by the same edge | closure@H1 displaced; subtotal and line-21 publication displaced |
| reclose | absent at H2 | absent at H2 | closure@H2 = true |
| recompute | binding finds no current finding (`marshal.py:233–241`) ⇒ **`DEPENDENCY_ABSENT` naming A8** | same ⇒ `DEPENDENCY_ABSENT` naming C2 | no line 21; the taxpayer is asked the sixteen questions again about {S1, S2} |

Facts unusable at "add member", after the fix: the H1 closure finding, the
subtotal, the line-21 publication, **and all sixteen statement-set-dependent
components**. B1 survives, correctly and by design.

**Nothing remains current that should not.** There is no residual "it remains
current" answer for any of the sixteen, so this output does not block Track 0
closure. The generalization to the other fourteen is not an argument by analogy:
displacement is driven by the identity key alone, and all sixteen carry the same
`family-horizon` key, so the walk is literally the same walk with a different
fact-type id. B1 is the only row with a different key and therefore the only row
with a different answer.

**One residual, recorded as a risk rather than a defect.** Nothing in the kernel
checks *which family's* horizon chain a contributed fact keys on.
`packages/kernel/contribution.py` performs no horizon validation, and fact
individuation binds a `family-horizon` key against every entity of kind
`kernel.family-horizon` in the workspace regardless of family. A component
mis-keyed to, say, the W-2 family's current horizon would be admissible and
would then never be displaced by 1098-E membership changes. The protection is
therefore only as good as the contribution boundary's choice of horizon. This is
a Track 1 obligation (the contribution path must key the sixteen to the 1098-E
family's current horizon) and a fixture obligation (a negative fixture asserting
a component against the wrong chain). It needs no new substrate and does not
reopen F1.

### T0c-1.5 — What the re-keying costs, and whether the burden is right

**The burden.** Every member transition on the 1098-E family — adding a
statement, removing one, reclassifying one — obliges the taxpayer to re-answer
**sixteen** questions before line 21, Schedule 1 line 26, Form 1040 line 10, and
AGI can be computed again. Before this settlement the same transition obliged
them to re-attest **one** thing (closure). The re-keying multiplies the
membership-change cost by sixteen, and it does so at the worst moment: the
taxpayer has just discovered a form they had forgotten.

**What softens it, factually.** A CORRECTED statement that changes only an amount
is not a member transition (ADR-0017 §4) and costs nothing. The burden falls only
on genuine membership change, which is the event that actually invalidates the
answers.

**Whether it is the right burden — settled: yes, at this base.** Three grounds.

1. *The answers really are about the new set.* Fourteen of the sixteen are
   universals over the recorded loans; adding a loan makes the previous answer
   an assertion about a different set. Re-asking is not friction, it is the
   question.
2. *The alternative is not cheaper, it is unavailable.* Per-statement authority
   would let the sixteen be asked once per new statement rather than sixteen
   times per transition — but it requires a categorical or boolean aggregate to
   fold per-statement answers across a variable-length family, and the evaluator
   has none (`evaluator.py:118` `collect` decimal-coerces every row;
   `count` returns only a length). That is milestone stop condition 2. The cost
   comparison is therefore against a design this milestone cannot build, not
   against a design it declined to build.
3. *The engine's existing posture already prices correctness above convenience
   here.* Closure itself imposes exactly this shape of burden and is ratified 44
   times over. The re-keying makes the sixteen behave like the one fact in the
   family that already behaved correctly.

**What is honestly wrong with it, stated rather than smoothed.** The burden is
blunt: a second statement from the *same* servicer for the *same* loans, which
changes nothing any of the sixteen assert, still costs sixteen re-attestations.
A future milestone with per-statement authority and a real aggregate would charge
one. This settlement records that as a known, correct-but-coarse cost, not as a
design virtue. Presentation should mitigate it by re-offering the previous
answers as defaults *to the taxpayer* — never as engine defaults, and never
carried forward without a fresh assertion.

### Notes addressed to T0c-3/4/5 — findings, not decisions

* **To T0c-4 (dependency diff).** B1's return scope is now load-bearing in a
  second way: since it is not displaced by 1098-E events, it is a *standing*
  return-level prerequisite once anything requires it. Whether AGI should acquire
  a standing dependent-status prerequisite is T0c-4's question; T0c-2 removes the
  worst version of it by making `B1 = no` a legal zero rather than a block, but
  it does not remove the requirement that B1 be *answered*.
* **To T0c-5 (restatement).** T0-2 must be restated: its heading *"Scope of the
  components: return-scoped, and why"* and its settled sentence *"every
  eligibility component is return-scoped, keyed by the `tax-year` literal
  `'2025'` alone"* are now wrong for sixteen of seventeen. The reasoning under
  that heading survives intact — the *collapse over statements* is still forced
  by the evaluator's missing aggregate, and the mandated universal quantifier in
  each title still stands. Only the identity key changes. T0-1's identity-key
  section needs no change.
* **To T0c-5.** SLI-C2's wording must gain the horizon binding. SLI-C1 is
  unaffected.
* **To T0c-3.** The twelve reused `ss-benefits-scope` absences are return-scoped
  in the same sense B1 is — they are not statement-set-dependent — so F1's
  re-keying does not touch them and does not change F3's pricing either way.

---

## Track 0c settlement — T0c-2 (empty/nonempty authority matrix and the closed-empty route)

This unit settles mandatory Track 0 output 2 (empty/nonempty authority matrix),
the F2 closed-empty canonical-zero branch, and the per-component
legal-zero-versus-block decision F2 exposes. It allocates no version numbers and
writes no content. Expression skeletons below are illustrative of *shape* only;
Track 1 owns the JSON.

Primary source re-read for this unit, not inherited:

* **[I1040GI p. 98], Schedule 1 line 21 instructions** — "You can take this
  deduction **only if** all of the following apply. • You paid interest in 2025
  on a qualified student loan… • Your filing status is any status except married
  filing separately. • Your modified adjusted gross income (AGI) is less than
  $100,000 … $200,000 … • You, or your spouse if filing jointly, **aren't
  claimed as a dependent** on someone else's (such as your parent's) 2025 tax
  return."
* **[P970 p. 33], "Can You Claim the Deduction?"** — the same four requirements,
  and **Example 2**: "During 2025, you paid $1,100 interest on your qualified
  student loan. Only you are legally obligated to make the payments. Your
  parents claimed you as a dependent on their 2025 tax return. **In this case,
  neither you nor your parents may deduct the student loan interest you paid in
  2025.**"
* **[P970 p. 33], "No Double Benefit Allowed"** — "You can't deduct as interest
  on a student loan **any amount** that is an allowable deduction under any
  other provision"; the QTP-earnings sentence; the post-2020-03-27
  employer-educational-assistance sentence.
* **[P970 p. 33], "Don't Include as Interest"** — the legal-obligation,
  origination-fee, and NHSC/LRAP bullets.
* **[P970 p. 34], "Form 1098-E"** — "if you pay qualifying interest that **isn't
  included** on Form 1098-E, you can **also** deduct those amounts."

### T0c-2.1 — The test that decides zero versus block

A `no` on a component is a **legal zero** when the law makes the *entire*
deduction zero on that fact alone, with no amount entering the determination.
A `no` is **unsupported → block** when the true line 21 is some amount the
engine cannot determine — either because the `no` removes an unknown *part* of
the claimed interest, or because it reveals an unknown *addition* outside box 1.

Two consequences of the test, both of which matter below:

* A component whose settled text is a **universal over the recorded set** can
  almost never yield a legal zero, because `no` on a universal is an existential
  failure: some loan fails, the others may still qualify, and the engine cannot
  split box 1 between them. This is not a limitation of the law but of the
  consolidation T0-2 was forced into.
* A block is warranted in **both** directions of error. The foreman's framing
  ("B3–B5 reduce the includible amount and therefore genuinely block") is correct
  as to outcome but incomplete as to ground: C1 and C2 block because the honest
  answer is *larger* than the box-1 subtotal, not smaller. Publishing the box-1
  figure there would understate the taxpayer's deduction, which is a real harm
  and exactly what T0-3 forbade ("It must block, never silently reduce the
  deduction to the box-1 figure").

### T0c-2.2 — Per-component decision (settled)

| # | `no` means | Disposition | Authority and reason |
| --- | --- | --- | --- |
| A1 `legally-obligated` | At least one recorded statement covers interest the taxpayer is not obligated to pay | **Block** | [P970 p. 33] "Don't Include as Interest" bullet 1 excludes *that interest*, not the deduction. The component is a universal over the recorded set, so `no` leaves an unknown obligated remainder. See the single-statement note below — even a one-statement family cannot collapse this to zero |
| A2 `interest-paid-in-2025` | Some box-1 amount was not paid in 2025 by or for the taxpayer | **Block** | Same structure; the timing failure is per-amount |
| A3 `proceeds-solely-qualified-expenses` | At least one loan is not a qualified student loan | **Block** | [I1040GI p. 99] "a loan isn't a qualified student loan if (a) any of the proceeds were used for other purposes" — disqualifies *that loan*. Other loans in box 1 remain deductible; split unknown |
| A4 `expenses-within-reasonable-period` | Same, for at least one loan | **Block** | [P970 p. 31] "Reasonable period of time"; per-loan |
| A5 `student-relationship-when-incurred` | Same, for at least one loan | **Block** | [P970 p. 30]; per-loan |
| A6 `eligible-student` | Same, for at least one loan | **Block** | [P970 p. 31]; per-loan |
| A7 `eligible-educational-institution` | Same, for at least one loan | **Block** | [P970 p. 31]; per-loan |
| A8 `lender-not-related-person` | At least one loan is from a related person | **Block** | [P970 p. 31]; §221(d)(1) excludes *that loan* from the definition of a qualified student loan |
| A9 `not-qualified-employer-plan-loan` | Same, for at least one loan | **Block** | [P970 p. 31]; §72(p)(4)–(5); per-loan |
| A10 `expenses-not-reduced-below-loan` | For at least one loan, adjusted expenses fell below the proceeds | **Block** | [P970 p. 32] "Adjustments to Qualified Education Expenses" — the excess disqualifies part of the loan; the allocation is the Pub 970 method the engine does not model |
| **B1** `not-claimed-as-dependent` | The taxpayer (or spouse on a joint return) is claimed as a dependent on another taxpayer's 2025 return | **Legal zero** | [I1040GI p. 98] "You can take this deduction **only if** … you … aren't claimed as a dependent". [P970 p. 33] Example 2 is decisive and quantifies nothing: a taxpayer who paid $1,100 of interest on a loan they alone are obligated on gets **no** deduction. The law returns a determinate answer — zero — and the engine can honestly publish it |
| B2 `no-qtp-tax-free-earnings-paid-interest` | Some claimed interest came from tax-free QTP earnings | **Block** | [P970 p. 33] ¶2 disallows *that amount*; the remainder is deductible; split unknown |
| B3 `no-employer-educational-assistance-interest` | Some claimed interest was paid by the employer under an educational assistance program | **Block** | [P970 p. 33] ¶3; per-amount |
| B4 `no-other-provision-deduction` | Some claimed amount is deductible under another provision, or is used in another deduction | **Block** | [P970 p. 33] ¶1 "any amount that is an allowable deduction under any other provision"; per-amount. [I1040GI p. 99] worksheet line 9 also forbids double-counting the *result*, which the engine cannot police |
| B5 `no-loan-repayment-assistance-payments` | Some claimed interest was paid through NHSC or a similar LRAP | **Block** | [P970 p. 33] "Don't Include as Interest" bullet 3; per-amount |
| C1 `no-box-2-checked` | A furnished statement asserts box 1 is knowingly incomplete | **Block — understatement direction** | [F1098E p. 4]; [P970 p. 34] "if you pay qualifying interest that isn't included on Form 1098-E, you can **also** deduct those amounts". The true deduction is ≥ the subtotal by an unknown amount requiring the [P970 p. 32] allocation method, which is out of scope |
| C2 `no-unreported-deductible-interest` | Deductible interest exists outside box 1 | **Block — understatement direction** | [I1098ET p. 1] ($600 threshold); [P970 pp. 32, 34]. Same reason as C1 |

**Settled: exactly one component — B1 — yields a legal zero. The other sixteen
block.** The prior settlement's uniform "a `no` blocks" was wrong at exactly one
place, and it is the place F2 named.

**Why no per-count special case is sound.** It is tempting to say that on a
one-statement family, `A3 = no` disqualifies the only loan and therefore yields a
legal zero. It does not: [F1098E p. 4] states box 1 shows interest "on **one or
more** student loans made to you", and [I1098ET p. 1] permits a filer to file one
Form 1098-E covering all of a borrower's loans. The engine cannot tell a
one-loan statement from a several-loan statement, so even a singleton family
leaves an unknown split. Block is correct at every cardinality, and Track 1 must
not add a cardinality shortcut.

**A consequence for a non-component condition, recorded not decided.** Filing
status *married filing separately* has the same structure as B1: [I1040GI p. 98]
denies the deduction outright, no amount enters. T0-4 settled MFS as **blocked**,
partly on the ground that the phaseout parameter has no MFS key. Under the test
settled here that is the wrong disposition — MFS should select zero and never
reach the parameter at all. This is a finding for T0c-5's restatement of T0-4,
not a decision of this unit; T0c-5 must dispose of it explicitly.

### T0c-2.3 — The closed-empty canonical-zero branch (settled)

**The guard is stated on the subtotal, not on membership, because that is what
the rule can see.** The rule has no membership-count symbol; what reaches it is
the closure-admitted box-1 subtotal. Settled guard:

> the closure-admitted box-1 subtotal equals 0 **and** C2 = `yes`.

Closed-empty is the case that motivates the guard and is its ordinary instance.
A closed non-empty family whose members all report box 1 = $0 takes the same
route, and that is correct for the same reason and not a loophole: with zero
claimed interest and C2 asserting no deductible interest outside box 1, the
deduction is zero whatever the answers to the other fifteen are.

**Why C1 is not in the guard, and why that is safe.** The worry is a furnished
statement with box 2 checked and no box-1 amount — a family that closes empty
while a real, deductible, unreported amount exists. C2 forecloses it by its own
enumerated text: the taxpayer has no deductible 2025 student loan interest other
than box-1 amounts of the recorded statements, "**including** interest below the
$600 reporting threshold, interest paid to a person who filed no statement, and
**pre-September-1-2004 origination fees or capitalized interest**". That last
clause is precisely the box-2 case. C2 = `yes` on an empty family is therefore
the strongest true statement available — "no deductible student loan interest at
all" — and C1 adds nothing to it.

**What it publishes.** Line 21 = `0`. This is an **authorized** zero. It is not a
default, not an `optional_default`, and not a fallback: it is selected by a guard
over two contributed authorities, and it is unavailable if either is missing.
It stands squarely inside the posture `rule.schedule1-line10` states in its own
notes — "Closed-empty unemployment with complete absences publishes explicit
zero. **Does not manufacture zero amounts for unimplemented producers**" — and
inside ADR-0038's declared-absence principle that "zero is never assumed, only
declared".

**Provenance, and where it lives.** On this route the rule reads exactly two
symbols, so its `pins` carry exactly two input authorities: the C2 finding and
the box-1 subtotal publication. **Closure provenance arrives transitively**,
through the subtotal: a closure-backed zero subtotal pins the family whose
closure authority the empty `collect` stood on (`AccessLog.closure_reads`,
ADR-0014 §5), so the walk from line 21 reaches the closure finding in one further
hop. Line 21 must **not** re-pin closure directly. That is the same reasoning
T0-8 used to reject a second absence gate at Form 1040 line 10: the authority
lives in one place, and duplicating it creates two places for it to disagree.
The resulting explanation walk reads: *line 21 is zero because the recorded
Form 1098-E family is closed with no box-1 amounts, and because the taxpayer
declared there is no deductible student loan interest outside box 1.*

**What must change in the T0-4 rule shape for this to be reachable.** T0-4 settled
"with **every** component named in `requires`". That cannot stand: the runner
checks `requires` before evaluating anything (`runner.py:482`), so seventeen hard
requirements would block a closed-empty return before the guard is ever reached —
which is F2's defect restated. Settled correction:

* `requires` carries the box-1 subtotal and **C2 only**.
* The other sixteen become **path dependencies**, in exactly the shape ADR-0038
  ratified for the QDCG worksheet's two declarations: "not unconditional
  `requires` on line 16; they are expression dependencies of the
  qualified-positive path only. A qualified-zero return never reads, names, or
  pins either declaration."

Illustrative shape (nesting only; not normative JSON):

```
when: true
value: choose(
  when: all( compare(box1-subtotal eq 0), categorical_compare(C2 eq yes) ),
  then: 0,                                     # canonical zero, closure + C2 provenance
  else: choose(
    when: all( conditional_dependency_set(condition: true, members: [ref B1]),
               categorical_compare(B1 eq no) ),
    then: 0,                                   # legal zero, B1 provenance
    else: choose(
      when: all( conditional_dependency_set(condition: true,
                                            members: [refs of A1-A10, B2-B5, C1]),
                 <all sixteen non-B1 components eq yes> ),
      then: <worksheet lines 1-9, T0-4>,
      else: block(<an already-published code>) )))
```

**Two verified properties of that shape, both load-bearing.**

1. *Absence is still named, and named completely.* `conditional_dependency_set`
   with a true condition evaluates **every** member, accumulates the
   `DEPENDENCY_ABSENT` misses, and raises once with the complete list
   (`evaluator.py:217–236`). So a return missing three components is told about
   all three, which is strictly better than the seventeen-hard-`requires` shape
   it replaces.
2. *It repairs a defect in T0-4's stated diagnosis path.* T0-4 recorded, as its
   mitigation for `block` carrying no `missing` list, that "every component
   finding is pinned unconditionally whatever its value, so a walker reads the
   answers directly." **That was not true at this base.** `all` is
   `all(bool(evaluate(a, ...)) for a in expr["args"])` (`evaluator.py:173–174`)
   over a Python generator, so it short-circuits at the first `no`; pins are
   built from `AccessLog.refs` (`runner.py:343–359`); therefore components after
   the first `no` were never read and never pinned. Placing the
   `conditional_dependency_set` node **first** in the guard fixes this as a side
   effect: it evaluates every member `ref`, each of which does
   `access.refs.add(...)` (`evaluator.py:108–110`), so all fifteen are pinned
   before the short-circuiting `all` runs. T0-4's claim becomes true only under
   this shape. T0c-5 must restate T0-4 accordingly.

**One cost, stated plainly.** Because the empty route is tested first, the B1
legal zero is reachable only after the subtotal and C2 are present. A taxpayer
claimed as someone else's dependent must therefore still close a Form 1098-E
family and answer C2 before receiving a zero the law grants unconditionally.
The alternative ordering — B1 first — would remove that cost but would make the
closed-empty route consult a loan-eligibility answer, which F2's disposition
forbids in terms ("without consulting any loan-eligibility answer"). This unit
takes F2 literally and accepts the cost. T0c-4 owns the dependency-diff argument
and may reopen the ordering; if it does, it must dispose of F2's wording.

### T0c-2.4 — Empty/nonempty authority matrix (mandatory output 2)

AGI here means Form 1040 line 11a via the T0-8 chain
(line 21 → Schedule 1 line 26 → Form 1040 line 10 → line 11a = line 9 − line 10).
"Not published" means the run records a disposition and no AGI exists — never a
zero.

| # | Family state | Interest universe | Eligibility answer | Expected line 21 | Expected AGI |
| --- | --- | --- | --- | --- | --- |
| 1 | Closed **empty** | none | C2 = `yes`; **B1 = `no`** | **`0`**, canonical zero. B1 is never read and never pinned | **Published**, = line 9. *This row is F2 discharged: dependent status no longer suppresses AGI* |
| 2 | Closed **empty** | none | C2 = `yes`; B1 = `yes`, or B1 absent | **`0`**, same route, same provenance | Published, = line 9 |
| 3 | Closed **empty** | none | **C2 absent** (any other answers) | **Not published** — `DEPENDENCY_ABSENT` naming C2, from the hard `requires` | **Not published.** Justified: without C2 the engine does not know whether deductible interest exists outside box 1, and a zero here would be manufactured. See the note to T0c-4 |
| 4 | Closed **empty** | none | C2 = `no`; B1 = `no` | **`0`**, legal zero on B1 (the empty guard fails on C2) | Published. Correct even though unreported interest exists: a claimed dependent may deduct none of it |
| 5 | Closed **empty** | none | C2 = `no`; B1 = `yes` | **Blocked** | Not published. Correct: real deductible interest exists that this milestone cannot quantify |
| 6 | Closed **non-empty** | box-1 subtotal > 0 | All seventeen `yes` | Worksheet L9 (T0-4): capped at $2,500, then phased out | Published, = line 9 − line 26 |
| 7 | Closed **non-empty**, all members box 1 = $0 | subtotal = 0 | C2 = `yes`, others any | **`0`**, same canonical-zero route as row 1 (guard is on the subtotal, not on emptiness) | Published |
| 8 | Closed **non-empty** | subtotal > 0 | **B1 = `no`** (any other answers) | **`0`**, legal zero | **Published.** The other sixteen are read for pinning but do not change the result |
| 9 | Closed **non-empty** | subtotal > 0 | any of **A1–A10** = `no`, B1 = `yes` | **Blocked** | Not published |
| 10 | Closed **non-empty** | subtotal > 0 | any of **B2–B5** = `no`, B1 = `yes` | **Blocked** | Not published |
| 11 | Closed **non-empty** | subtotal > 0 | **C1 = `no`**, B1 = `yes` | **Blocked** (understatement direction) | Not published |
| 12 | Closed **non-empty** | subtotal > 0 | **C2 = `no`**, B1 = `yes` | **Blocked** (understatement direction) | Not published |
| 13 | Closed **non-empty** | subtotal > 0 | one or more of the sixteen **absent**, B1 = `yes` | **Not published** — `DEPENDENCY_ABSENT` naming **every** absent component, via the `conditional_dependency_set` node | Not published |
| 14 | **Not closed** (no closure finding at the current horizon) | unknown | any | **Not published** — the subtotal cannot publish; `SOURCE_SET_UNCLOSED` | Not published |
| 15 | Closed at H1, then a member added (H2), not yet re-answered | subtotal recomputed over {S1, S2} | the sixteen displaced by T0c-1's re-keying; B1 survives | **Not published** — `DEPENDENCY_ABSENT` naming C2 (hard `requires`) and, on the non-empty path, the other fifteen | Not published. *This row is F1 discharged* |

Row 8 is the sharpest reading of the second correction F2 exposed: a taxpayer
with $1,100 of genuinely paid interest, claimed as a dependent, gets a published
zero and a published AGI — [P970 p. 33] Example 2 exactly — where the withdrawn
settlement gave them no AGI at all.

### T0c-2.5 — What this does and does not close

* **F2 is discharged** for the closed-empty route (rows 1–5) and, more broadly
  than the finding asked, for every family state, because B1 never blocks
  (rows 8 and 4).
* **The adversarial-closure line "Closed-empty route: FAIL — B1 suppresses AGI"
  can be re-declared PASS** once T0c-5 restates T0-4 and SLI-C2 to match. This
  unit does not itself re-run the declaration.
* **No stop condition fires.** Every operator this settlement relies on is
  committed: `choose`, `all`, `compare`, `categorical_compare`,
  `category_literal`, `block`, and `conditional_dependency_set`. The last is the
  only one T0-4 did not already name, and it is ratified content-level substrate
  (ADR-0037/ADR-0038, in production at `rule.form1040-line16`). No new error
  vocabulary, no new operator, no ADR.

### Notes addressed to T0c-3/4/5 — findings, not decisions

* **To T0c-4.** The post-disposition dependency figure for AGI on a return with
  no student-loan activity is now **two** contributed prerequisites plus one
  closure — the 1098-E family closed (empty), C2 = `yes`, and nothing else —
  down from seventeen components plus closure. Row 3 of the matrix is the
  remaining cost and the one T0c-4 must justify: a taxpayer who has never had a
  student loan must still close an empty 1098-E family and answer C2 before AGI
  exists. That is the same shape of prerequisite the income side already imposes
  through `rule.schedule1-line10` (closed-empty 1099-G plus ten declared
  absences), which is the strongest available justification and is offered here
  as evidence, not as a decision.
* **To T0c-5.** Three restatements are forced by this unit: (a) T0-4's
  "every component named in `requires`" becomes "the subtotal and C2 in
  `requires`; the other sixteen as `conditional_dependency_set` path
  dependencies"; (b) T0-4's "Known limitation" paragraph must be corrected — its
  claim that every component is pinned unconditionally was false at this base and
  becomes true only under the corrected shape; (c) T0-4's zero-and-boundary table
  row "Married filing separately | blocked" must be re-decided against T0c-2.2's
  test.
* **To T0c-5.** SLI-C2 must state that a `no` blocks for sixteen components and
  selects zero for B1; SLI-C6 and SLI-C8 are unaffected in substance but their
  "line 21 is required" wording should be read against rows 3 and 14.
* **To T0c-3.** Nothing in this unit changes the pricing of the twelve shared
  Schedule 1 absences. It does, however, supply a precedent T0c-3 may want: the
  `conditional_dependency_set` shape is a ratified way to make declared absences
  path-conditional rather than unconditional, should the return-level successor
  need it.

## Foreman record — T0c-1/T0c-2 acceptance, source availability, and open dispositions

### Source availability defect (process, not correctness)

`p970-2025.pdf` and `i1040gi-2025.pdf` are **not present in this worktree and not
tracked anywhere on this branch**. Every Track 0 unit that cited them re-obtained
them into an ephemeral scratchpad. The milestone's page citations are therefore
not reproducible from the repository alone.

The foreman spot-checked five load-bearing Track 0a/0b citations against freshly
obtained 2025 editions. **All five verify at the cited page**: P970 p. 32
"Adjustments to Qualified Education Expenses"; P970 p. 33 "Can You Claim the
Deduction?"; P970 p. 33 "Don't Include as Interest" including the A1 obligation
bullet (a literal search fails only because the source hyphenates "pay-ments"
across a line break); I1040GI p. 98 "aren't claimed as a dependent" and "You can
take this deduction only if"; and I1040GI p. 99 for the Student Loan Interest
Deduction Worksheet, independently reconfirming the p. 98 → p. 99 erratum. This
is an availability and reproducibility defect, not an evidence-integrity one.

Track 1 obligation: settle how cited federal sources are made durably available
to a reviewer, without violating ADR-0031's real-data residency boundary.

### T0c-1 and T0c-2 accepted, with three corrections to foreman pricing

Accepted at `46583f2` (T0c-1) and `6506125` (T0c-2). The sixteen-of-seventeen
classification and the B1-alone-is-a-legal-zero result are confirmed. Three
places where the builder corrected the foreman's stated grounds while reaching
the same outcome, all of which govern over the foreman's wording above:

* **C1's dependence is contingent, not textual.** The foreman said C1 quantifies
  over *furnished* forms; read literally that would make C1 return-scoped, since
  the furnished universe does not move when the recorded set moves. C1 is
  statement-set-dependent only because the closure claim asserts furnished and
  recorded are coextensive at the keyed horizon. If a later unit weakens that
  wording, **C1 must be re-examined**.
* **C1/C2 block for the opposite reason from B2–B5.** The foreman's ground
  ("reduce the includible amount") is right for B2–B5 and wrong for C1/C2, which
  block because the honest answer is *larger* than box 1.
* **A1–A10 are not legal zeros.** Each is a universal over the recorded set, so
  a `no` is an existential failure leaving an unknown obligated remainder — it
  blocks. No cardinality shortcut rescues a legal zero even for a singleton
  family, because [F1098E p. 4] box 1 covers "one or more student loans".

The substrate claim underpinning F1's pricing is **verified in the kernel, not
assumed**: horizon displacement is generic, not closure-specific
(`packages/kernel/facts.py:190-216`, `findings.py:745-757`, `currency.py:127,151`,
`marshal.py:222-226`). The counterexample fully resolves after re-keying; no
fact remains current that should not.

### Defect found in the already-settled T0-4 text

T0-4 recorded, as its mitigation for `block` carrying no `missing` list, that
"every component finding is pinned unconditionally whatever its value." **That
was false at this base.** `all` short-circuits (`evaluator.py:173-174`) and pins
derive from `AccessLog.refs` (`runner.py:343-359`), so components after the first
`no` were never read and never pinned. The repair falls out of the change F2
already forces: seventeen hard `requires` cannot stand, because `runner.py:482`
checks `requires` before evaluating anything and a closed-empty return would
block before reaching the guard. The sixteen become `conditional_dependency_set`
path dependencies — the shape ADR-0038 already ratified for the QDCG
declarations — which evaluates every member, accumulates a complete absence
list, and restores the pin completeness T0-4 claimed. No new operator, no new
error code, no ADR.

### Open dispositions carried to T0c-5

* **MFS.** T0-4 settled married-filing-separately as "blocked". Under the test
  settled in T0c-2 it has B1's structure and should **select zero**. T0c-5 must
  dispose of this.
* **Branch ordering.** Because the empty route is tested first, a taxpayer
  claimed as a dependent must still close a 1098-E family and answer C2 before
  receiving a zero the law grants unconditionally. T0c-2 took F2's "without
  consulting any loan-eligibility answer" literally and accepted the cost.
  T0c-4 may reopen the ordering, but must then dispose of F2's wording.

### New residual risk — recorded, does not reopen F1

Nothing validates *which family's* horizon a contributed fact keys on.
`packages/kernel/contribution.py` has no horizon check, and individuation binds
against every `kernel.family-horizon` entity in the workspace, so a component
mis-keyed to (say) the W-2 horizon would be admissible and never displaced by
1098-E changes. Track 1 obligation plus a negative fixture; no new substrate.

Separately, `superseded_horizon_ids` (`packages/kernel/horizons.py:71`) has **no
caller anywhere in `packages/`**. Displacement does not run through it. Harmless,
but a reviewer who assumes it is the mechanism would be wrong.

### T0c-4 input, already established

The post-disposition AGI prerequisite on a return with no student-loan activity
is **closure (empty) plus C2 alone**, down from seventeen components plus
closure. Matrix row 3 is the remaining cost for T0c-4 to justify.

### T0c-3 is held

T0c-3 (the shared Schedule 1 absence renormalization) modifies content ratified
by PR #163 and is **held pending owner decision**. It is the only Track 0c item
that expands the milestone past its original charter.

## Owner dispositions — Track 0c (governing)

The owner disposed of the three findings as follows. These govern over any
foreman or builder wording above.

### D1 — Horizon re-keying: approved, bounded

Re-key the sixteen statement-set-dependent declarations to the **current Form
1098-E family horizon plus tax year**. Re-attestation after family membership
changes is **accepted for this milestone**. **Do not expand into per-loan
boolean aggregation.**

Required evidence, explicitly, for each of: **add**, **remove**, **reclose**,
**same-member correction**, and **rejection or non-use of an answer keyed to the
wrong family's horizon**. That last one converts the residual risk T0c-1
recorded into a discharged obligation rather than a Track 1 note.

### D2 — Legal zero: approved, and branch ordering is reopened

A closed-empty Form 1098-E family plus C2 may produce a canonical zero without
reading loan-eligibility declarations.

**Branch ordering must be settled explicitly, not inherited.** Where B1 or
filing status establishes an *unconditional* legal zero, determine whether that
zero must publish **before** requiring Form 1098-E closure or C2. A legally
unconditional zero must not be left dependent on irrelevant student-loan
authority merely because of expression ordering. This supersedes T0c-2's
acceptance of the ordering cost, and it subsumes the open MFS disposition.

### D3 — Shared vocabulary: approved in principle, bounded by an inventory

A neutral, shared **return-level successor vocabulary** for the twelve Schedule 1
absence propositions is approved **in principle**. Three shapes are ruled out by
name:

* **Do not rewrite ratified SSA citizens in place.**
* **Do not duplicate the twelve declarations.**
* **Do not bridge SSA-scoped claims into broader claims.**

The permitted shape is succession: the SSA-scoped facts **may be superseded by
new neutral citizens**, and both the Social Security worksheet and the
student-loan route may consume the successors. This is additive content
succession, not editing.

**Item 3 is not bounded within this milestone until T0c-3 delivers a full
semantic and publication impact inventory — not a count of direct reference
files.** The foreman's earlier "three files" pricing is withdrawn as
category-inadequate. The inventory must enumerate:

* every new or successor fact and rule citizen;
* every package, published-package, release, registry, fixture, and golden
  version affected;
* all existing consumers and user attestations displaced;
* the exact SSA compatibility tests and live-route evidence;
* whether any generic evaluator, contribution, schema, or migration mechanism
  must change.

**Keep the repair in this milestone** if it remains additive content succession,
package publication, and bounded SSA regression proof. **Stop and propose a
separate prerequisite milestone** if the inventory reveals generic substrate,
migration machinery, additional consumers, or broader changes to SSA semantics.

### D4 — ADR budget

**Do not create a second ADR merely to satisfy an allowance.** Use another ADR
only if Track 0c identifies a **new durable product contract** not already
governed by the existing fact-meaning, lifecycle, succession, and claim-reuse
contracts.

### D5 — Track 1 gate

Complete T0c-4 and T0c-5, including the newly discovered **pin-completeness
repair**, the **wrong-family-horizon negative fixture obligation**, the
**no-activity dependency diff**, and all remaining PASS/FAIL entries.

**Track 1 may not be chartered until the adversarial-closure declaration carries
no unresolved FAIL and the final implementation boundary is stated as an
explicit allowed-impact envelope.**

### Standing consequence — milestone entry gate

The allowed-impact envelope required by D5 is the same instrument this milestone
lacked at entry. Reach was bounded in tax-domain language, which cannot express
it. Five entry questions are to be answered before a future charter is written,
and their answers carried in it: (1) what existing artifacts will be created,
versioned, or **modified in place while already merged** — the third bucket
empty by default and an explicit owner decision to fill; (2) what already works
that could change behaviour, stated as before/after for a return that does not
use the new feature; (3) which needed facts already exist and whether their
**declared meaning** is neutral or owner-scoped; (4) for every new fact, whether
staleness is caused by correction or by the paperwork changing; (5) what
substrate the engine lacks. Question 5 is the one this charter did ask, and it
is the one thing that never surprised the milestone.
