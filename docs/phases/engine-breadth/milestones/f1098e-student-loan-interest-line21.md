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
