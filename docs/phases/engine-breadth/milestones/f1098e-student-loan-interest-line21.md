<!-- foreman-context-v1
{
  "version": 1,
  "topic": "f1098e-student-loan-interest-line21",
  "milestone_state": "planned",
  "retrospective": null,
  "status": "PLANNED. Track 0 (paper-first scope contract) is chartered and not yet performed. Base is milestone/f1098-mortgage-interest-line12e @ b25562f, selected by the owner so version allocation sees the true highest allocated numbers. No schema, rule, package, registry, attachment, or form-field version numbers are allocated by this plan. No dispatch: owner-launch only.",
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
  }
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
