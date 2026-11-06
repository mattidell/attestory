# P0: inventory and draft for line explanations

Core v77 (`package.core-calculations.v77.json`, registry
`published-packages.v75.json`, release
`demo.release.sli-worksheet-integration.2025.v75.json`), through
`live_coordinate_run` only. Synthetic `demo.*` findings. This file is the
record. The probe and its JSON output, and the scratch prototype and its
output, sit beside it. Nothing under `packages/` is edited.

## Inventory

Core v77 pins 73 form-field members: 69 use `form-field.v3` and 4 use `form-field.v2`. The four v2 fields are Form 1040 lines 1a, 9, 15, and 16, each at version v1. Every member has the five disposition texts, so the inventory is 365 texts. `probe-output.json` has each id, version, form, line, label, and the five texts.

A text is generic when it is a stock phrase that does not say what this line adds, why this zero, or why this line shows no value (`blocked`, `guard false`, `closure zero`, `computed zero`, `Current derived finding publishes this line.`, and the longer "A current derived finding publishes…" sentences of that kind), or the same sentence is used on two different lines, or it is only the word "published" plus a label, or it only says "No line N value exists for this route." The other texts are specific. Of the 365, 239 are specific and 126 are generic. The 126 generics are 37 distinct sentences. 114 are stock phrases, 8 are bare "published …" labels, and 4 are the unnamed-route sentence.

39 fields have at least one generic text. 36 of those have a generic text the page can select. The other three are generic only on a guard the rule never selects: Schedule D line 13, Schedule 1 line 21, and the Schedule 1 top entry.

Specific / generic by disposition:

| Disposition | Specific | Generic |
| --- | ---: | ---: |
| published_value | 55 | 18 |
| computed_zero | 43 | 30 |
| closure_backed_zero | 44 | 29 |
| blocked | 58 | 15 |
| guard_inapplicable | 39 | 34 |

Specific / generic by form. Each cell is specific/generic.

| Form | Fields | Published | Computed zero | Closure zero | Blocked | Guard |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Form 1040 | 41 | 32/9 | 27/14 | 28/13 | 33/8 | 25/16 |
| Schedule D | 11 | 4/7 | 2/9 | 2/9 | 4/7 | 0/11 |
| Schedule 8812 | 7 | 7/0 | 7/0 | 7/0 | 7/0 | 7/0 |
| Schedule 1 | 6 | 5/1 | 2/4 | 2/4 | 6/0 | 1/5 |
| EIC Worksheet A | 5 | 5/0 | 5/0 | 5/0 | 5/0 | 5/0 |
| Schedule 3 | 2 | 2/0 | 0/2 | 0/2 | 2/0 | 0/2 |
| Schedule A | 1 | 0/1 | 0/1 | 0/1 | 1/0 | 1/0 |

Schedule 8812 and EIC Worksheet A are already specific on every disposition. Credit lines 19 and 28 are in the Form 1040 specific count.

Class of each text, in package member order. `s` is specific and `g` is generic.

| Form | Line | Version | Published | Zero | Closure | Blocked | Guard | Label |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1040-EIC-WS-A | eic-a-1 | v1 | s | s | s | s | s | Worksheet A line 1 |
| 1040-EIC-WS-A | eic-a-2 | v1 | s | s | s | s | s | Worksheet A line 2 |
| 1040-EIC-WS-A | eic-a-3 | v1 | s | s | s | s | s | Worksheet A line 3 |
| 1040-EIC-WS-A | eic-a-5 | v1 | s | s | s | s | s | Worksheet A line 5 |
| 1040-EIC-WS-A | eic-a-6 | v1 | s | s | s | s | s | Worksheet A line 6 |
| 1040-SCH-A | f1098-unresolved | v1 | g | g | g | s | s | Open condition on the home mortgage interest statement |
| 1040-SCH-1 | f1099k-unresolved | v1 | g | g | g | s | s | Unresolved Form 1099-K condition |
| 1040 | 10 | v1 | s | g | g | s | g | Adjustments to income from Schedule 1 |
| 1040 | 11a | v1 | s | g | g | s | g | Adjusted gross income |
| 1040 | 11b | v1 | s | g | g | s | g | Amount from line 11a (adjusted gross income) |
| 1040 | 12e | v1 | g | g | g | g | g | Standard deduction or itemized deductions |
| 1040 | 13a | v1 | s | g | g | g | g | Qualified business income deduction |
| 1040 | 13b | v1 | s | g | g | g | g | Schedule 1-A deductions |
| 1040 | 1040-14 | v1 | g | g | g | g | g | Add lines 12e, 13a, and 13b |
| 1040 | 15 | v1 | g | g | g | g | g | Taxable income |
| 1040 | 16 | v1 | g | g | g | g | g | Tax |
| 1040 | 1a | v1 | g | g | s | g | g | Total amount from Form(s) W-2, box 1 (see instructions) |
| 1040 | 20 | v1 | s | g | g | s | g | Other nonrefundable credits from Schedule 3 |
| 1040 | 24 | v1 | s | s | s | s | s | Total tax |
| 1040 | 25a | v1 | s | s | s | s | s | Federal income tax withheld from Form(s) W-2 |
| 1040 | 25b | v3 | s | s | s | s | s | Federal income tax withheld from Form(s) 1099 |
| 1040 | 25c | v2 | s | s | s | s | s | Federal income tax withheld from other forms |
| 1040 | 25d | v1 | s | s | s | s | s | Total federal income tax withheld |
| 1040 | 26 | v1 | s | s | s | s | s | 2025 estimated tax payments |
| 1040 | 27a | v1 | s | s | s | s | s | Earned income credit |
| 1040 | 2a | v2 | s | s | s | s | s | Tax-exempt interest |
| 1040 | 2b | v6 | s | s | s | s | s | Taxable interest |
| 1040 | 32 | v1 | s | s | s | s | s | Total other payments and refundable credits |
| 1040 | 33 | v1 | s | s | s | s | s | Total payments |
| 1040 | 34 | v1 | s | s | s | s | s | Overpayment |
| 1040 | 35a | v1 | s | s | s | s | s | Refund |
| 1040 | 37 | v1 | s | s | s | s | s | Amount you owe |
| 1040 | 38 | v1 | s | s | s | s | s | Estimated tax penalty |
| 1040 | 3a | v1 | s | s | s | s | g | Qualified dividends |
| 1040 | 3b | v1 | s | s | s | s | g | Ordinary dividends |
| 1040 | 4b | v1 | g | s | s | s | s | Taxable IRA distributions |
| 1040 | 6a | v1 | g | s | s | s | s | Social Security benefits |
| 1040 | 6b | v1 | g | s | s | s | s | Taxable Social Security benefits |
| 1040 | 6c | v1 | s | s | s | s | s | Lump-sum election |
| 1040 | 6d | v1 | s | s | s | s | s | MFS lived apart all year |
| 1040 | 6d-not-checked | v1 | s | s | s | s | s | MFS lived with spouse (line 6d not checked) |
| 1040 | 7a | v1 | s | s | s | s | s | Capital gain or (loss) |
| 1040 | 7b | v2 | s | s | s | s | s | Schedule D not required |
| 1040 | 8 | v2 | s | g | g | s | g | Additional income from Schedule 1 |
| 1040 | 9 | v1 | g | g | g | g | g | Total income |
| 1040 | 22 | v1 | s | g | g | s | g | Tax after nonrefundable credits |
| 1040-SCH-D | sch-d-13 | v2 | s | s | s | s | g | Line 13: capital gain distributions |
| 1040-SCH-D | 14 | v1 | g | g | g | g | g | Line 14 long-term capital loss carryover |
| 1040-SCH-D | sch-d-15 | v1 | s | g | g | s | g | Line 15: net long-term capital gain |
| 1040-SCH-D | sch-d-16 | v1 | s | g | g | s | g | Line 16: total gain |
| 1040-SCH-D | 1a-h | v1 | g | g | g | g | g | Line 1a column (h) |
| 1040-SCH-D | 1b-h | v1 | g | g | g | g | g | Line 1b column (h) |
| 1040-SCH-D | 21 | v1 | g | g | g | g | g | Line 21 limited loss |
| 1040-SCH-D | 6 | v1 | g | g | g | g | g | Line 6 short-term capital loss carryover |
| 1040-SCH-D | 7 | v1 | g | g | g | g | g | Line 7 net short-term |
| 1040-SCH-D | 8a-h | v1 | s | s | s | s | g | Line 8a, column (h): gain |
| 1040-SCH-D | 8b-h | v1 | g | g | g | g | g | Line 8b column (h) |
| 1040-SCH-1 | sch1-10 | v3 | s | g | g | s | g | Additional income |
| 1040-SCH-1 | sch1-21 | v1 | s | s | s | s | g | Student loan interest deduction |
| 1040-SCH-1 | sch1-7 | v1 | s | g | g | s | g | Unemployment compensation |
| 1040-SCH-1 | sch1-top | v1 | s | s | s | s | g | Form 1099-K personal item sale loss gross payment amount (Schedule 1 top entry) |
| 1040-Schedule-3 | Sch3-1 | v1 | s | g | g | s | g | Foreign tax credit |
| 1040-Schedule-3 | Sch3-8 | v1 | s | g | g | s | g | Total other nonrefundable credits |
| 1040 | 19 | v2 | s | s | s | s | s | Child tax credit and credit for other dependents |
| 1040 | 28 | v2 | s | s | s | s | s | Additional child tax credit |
| Schedule 8812 | 8812-4 | v2 | s | s | s | s | s | Qualifying children under 17 with a valid SSN |
| Schedule 8812 | 8812-14 | v2 | s | s | s | s | s | Child tax credit and credit for other dependents |
| Schedule 8812 | 8812-17 | v2 | s | s | s | s | s | Smaller of unused credit and the refundable cap |
| Schedule 8812 | 8812-20 | v2 | s | s | s | s | s | 15 percent of earned income over $2,500 |
| Schedule 8812 | 8812-wa-5 | v2 | s | s | s | s | s | Credit Limit Worksheet A line 5 |
| Schedule 8812 | 8812-6 | v1 | s | s | s | s | s | Other dependents |
| Schedule 8812 | 8812-7 | v1 | s | s | s | s | s | Credit for other dependents amount |
| 1040-SCH-1 | sch1-8b | v1 | s | g | g | s | g | Gambling |

Seventy citations name an instructions or form family, a form, and tax year 2025. The citation schema has no line, page, or quoted instruction. Three fields have no citation: the home-mortgage open condition, the Form 1099-K open condition, and the Schedule 1 top entry.

## Where a filer reads it

Both cases are synthetic returns finished onto core v77 and run through `live_coordinate_run`. The presentation page was rendered in headless Chrome. Both runs produced 73 sections and no duplicate section ids. The browser was available, and the rendered section text was read back from the page.

The page puts the active explain in the line row for a published value, a computed zero, a closure-backed zero, and a guard. A guard row also says "Not applicable." A blocked row says "No value published — cannot compute." and, when the line has reason sentences, shows those sentences and the missing-dependency code. In that case the field's blocked explain is left out. The closed "Trace recorded support" block is in the same section and lists pin ids. It does not repeat the disposition sentence. None of the active explain strings appear in the saved explanation graph.

A numeric line with no citation is replaced by "This line published a value with no citation attached. No value can be shown safely." The amount and the explain are not shown. That happened to the Schedule 1 top entry. The two open-condition lines have no citation either, but they were guards, and a guard row does not take that citation path, so their explains did show.

### Wages-only return

`demo.le.p0.wages` is the shared wages return. Census: 19 published values, 41 computed zeros, 7 closure-backed zeros, 4 guards, 2 categorical "checked" lines. Nothing was blocked.

There is no field whose line is exactly 11. Lines 11a and 11b are the adjusted-gross-income lines. What the row shows:

| Line | Amount | Sentence beside it |
| --- | ---: | --- |
| 1a | 50000 | A current derived finding publishes this nonzero amount. |
| 9 | 50000 | published total income |
| 11a | 50000 | A current derived finding publishes Form 1040 line 11a, adjusted gross income, as total income minus Schedule 1 line 26. |
| 11b | 50000 | A current derived finding publishes Form 1040 line 11b, carried forward from line 11a's adjusted gross income. |
| 12e | 15750 | published standard-or-itemized deduction |
| 13a | 0 | computed zero |
| 13b | 0 | computed zero |
| 14 | 15750 | published line 14 total |
| 15 | 34250 | published taxable income |
| 16 | 3875 | published tax |

Each of those sentences is in the rendered row. Lines 11a and 11b name the line. The others are the generic labels from the inventory.

Schedule D on this return is not a set of guards. There are no capital transactions, and the lines are zeros of two kinds. Computed zero, sentence in the row: line 13 (a sentence about box 2a findings that sum to zero), lines 15 and 16 (a sentence about present inputs that net to zero), and lines 6, 7, 14, and 21 ("Computed zero."). Closure-backed zero, sentence in the row: lines 1a, 1b, and 8b ("Closure-backed zero."), and line 8a (a sentence that the proceeds and basis families are closed with no recorded members).

The four guards, each with "Not applicable." and its own sentence: the Schedule A home-mortgage open condition ("No open condition: the statement has a completed result, or no statement is present."), the Schedule 1 Form 1099-K open condition ("No open condition: statements resolved or no statement received."), and the two line 6d filing-status lines.

The seven closure-backed zeros are Schedule 8812 line 4 ("Schedule 8812 line 4 publishes zero through an honest closed-empty source family."), the four Schedule D lines above, Schedule 1 line 21 (the Form 1098-E box 1 family is closed and empty), and the Schedule 1 top entry ("No Form 1099-K statements were received for 2025."). The first six are in the row. The top entry is the no-citation case, so that sentence is not on the page. Line 2b is 0 and is not one of these seven, so it is a computed zero.

### Unanswered wage record

`demo.le.p0.wages-closure-unanswered` is the same return with the W-2 source-closure attestation removed. Line 1a and line 9 stay published at 50000 with the same sentences. They do not block. Line 1a collects the box 1 amounts already on the return, and its rule guard is true, so dropping the closure attestation leaves the wage total in place. Line 9 adds that total.

What does block is the payment side. The derivation report has 8 blocked rule rows. The page has 6 blocked form lines: 25a, 25d, 33, 34, 35a, and 37. Each is `DEPENDENCY_ABSENT`. Beside each one the page shows "No value published — cannot compute.", that code, and one question: "Have you recorded every wage amount in box 1 of every Form W-2 you or your spouse received for 2025?" The field's blocked explain is not in the row. Line 25a is the line that counts W-2 box 1 against box 2 and requires each family's closure, so the open wage record stops there and on the payment lines that depend on it.

### Texts a filer does not see

The four dispositions that are not the line's current one. A guard sentence on a rule whose `when` is true (20 of the drafted guards). The zero sentences on a checkbox line, which uses the published-value sentence for "checked". The blocked sentence whenever the line already has reason questions, which is the case observed here. The Schedule 1 top entry's closure sentence, because the page will not show a number from a field with no citation. The disposition sentences are not in the explanation graph.

## Draft wording

Each generic text gets one plain replacement. The words come from the line's label, a description sentence that adds something the label does not already say, the rule's own notes when those notes are already a filer sentence, and the labels of the amounts the rule adds. Citations cannot name a line or quote an instruction page, and there is no quoted instruction corpus in the package, so the draft does not pretend to quote one.

A published line that adds two or more labeled amounts says what it adds. A published line whose value is adjusted gross income minus the deduction total, and not below zero, says that. Where the rule notes are engine notes rather than a filer sentence, the draft uses a short sentence written for that line: lines 12e, 15, 16, and 1a, Schedule D lines 1a, 1b, 6, 8b, 14, and 21, and the two open-condition lines. A computed zero says those amounts come to zero, or that the subtraction is not above zero, or that the calculation comes to zero. A closure-backed zero says nothing was recorded and that record is complete. A blocked line says it is waiting for the amounts it adds, or for the labeled inputs the rule names, or for an answer it needs. Lines 1a, 12e, and 16 name the kind of input in their own words.

A rule with one guard says its condition does not hold. A rule with several guards says one of its conditions does not hold, and that one sentence cannot say which. That is the honest limit of a single static text. A rule whose guard is simply true never selects the guard sentence; those 20 drafts say so, and they are not proposed as filer copy. A checkbox line does not select its zero sentences; those drafts are kept so the field text is still honest if a later package selects them.

106 of the 126 drafts are sentences the page can select. 20 are the never-selected guard sentences.

| Form | Line | Disposition | Page can show it | Replacement |
| --- | --- | --- | --- | --- |
| 1040-SCH-A | f1098-unresolved | published | yes | This line names an open condition on the home mortgage interest statement. It does not show an amount. |
| 1040-SCH-A | f1098-unresolved | computed zero | yes | Schedule A, open condition on the home mortgage interest statement is zero because the calculation comes to zero. |
| 1040-SCH-A | f1098-unresolved | closure zero | yes | Schedule A, open condition on the home mortgage interest statement is zero because nothing was recorded and that record is complete. |
| 1040-SCH-1 | f1099k-unresolved | published | yes | This line names an open condition on a Form 1099-K. It does not show an amount. |
| 1040-SCH-1 | f1099k-unresolved | computed zero | yes | Schedule 1, unresolved Form 1099-K condition is zero because the calculation comes to zero. |
| 1040-SCH-1 | f1099k-unresolved | closure zero | yes | Schedule 1, unresolved Form 1099-K condition is zero because nothing was recorded and that record is complete. |
| 1040 | 10 | computed zero | yes | Form 1040 line 10 (Adjustments to income from Schedule 1) is zero because the calculation comes to zero. |
| 1040 | 10 | closure zero | yes | Form 1040 line 10 (Adjustments to income from Schedule 1) is zero because nothing was recorded and that record is complete. |
| 1040 | 10 | guard | no | Form 1040 line 10 (Adjustments to income from Schedule 1) has no condition that turns it off, so this sentence is not shown. |
| 1040 | 11a | computed zero | yes | Form 1040 line 11a (Adjusted gross income) is zero because the calculation comes to zero. |
| 1040 | 11a | closure zero | yes | Form 1040 line 11a (Adjusted gross income) is zero because nothing was recorded and that record is complete. |
| 1040 | 11a | guard | no | Form 1040 line 11a (Adjusted gross income) has no condition that turns it off, so this sentence is not shown. |
| 1040 | 11b | computed zero | yes | Form 1040 line 11b (Amount from line 11a (adjusted gross income)) is zero because the calculation comes to zero. |
| 1040 | 11b | closure zero | yes | Form 1040 line 11b (Amount from line 11a (adjusted gross income)) is zero because nothing was recorded and that record is complete. |
| 1040 | 11b | guard | no | Form 1040 line 11b (Amount from line 11a (adjusted gross income)) has no condition that turns it off, so this sentence is not shown. |
| 1040 | 12e | published | yes | Form 1040 line 12e is the larger of the standard deduction and the itemized deductions. |
| 1040 | 12e | computed zero | yes | Form 1040 line 12e (Standard deduction or itemized deductions) is zero because the calculation comes to zero. |
| 1040 | 12e | closure zero | yes | Form 1040 line 12e (Standard deduction or itemized deductions) is zero because nothing was recorded and that record is complete. |
| 1040 | 12e | blocked | yes | Form 1040 line 12e has no value yet. It is waiting for the standard deduction or the itemized deductions. |
| 1040 | 12e | guard | yes | Form 1040 line 12e (Standard deduction or itemized deductions) shows no value because its condition does not hold. |
| 1040 | 13a | computed zero | yes | Form 1040 line 13a (Qualified business income deduction) is zero because the calculation comes to zero. |
| 1040 | 13a | closure zero | yes | Form 1040 line 13a (Qualified business income deduction) is zero because nothing was recorded and that record is complete. |
| 1040 | 13a | blocked | yes | Form 1040 line 13a (Qualified business income deduction) has no value yet. It is waiting for an answer it needs. |
| 1040 | 13a | guard | yes | Form 1040 line 13a (Qualified business income deduction) shows no value because its condition does not hold. |
| 1040 | 13b | computed zero | yes | Form 1040 line 13b (Schedule 1-A deductions) is zero because the calculation comes to zero. |
| 1040 | 13b | closure zero | yes | Form 1040 line 13b (Schedule 1-A deductions) is zero because nothing was recorded and that record is complete. |
| 1040 | 13b | blocked | yes | Form 1040 line 13b (Schedule 1-A deductions) has no value yet. It is waiting for an answer it needs. |
| 1040 | 13b | guard | yes | Form 1040 line 13b (Schedule 1-A deductions) shows no value because its condition does not hold. |
| 1040 | 1040-14 | published | yes | Form 1040 line 14 (Add lines 12e, 13a, and 13b) adds Standard deduction or itemized deductions, Qualified business income deduction, and Schedule 1-A deductions. |
| 1040 | 1040-14 | computed zero | yes | Form 1040 line 14 (Add lines 12e, 13a, and 13b) is zero because those amounts come to zero. |
| 1040 | 1040-14 | closure zero | yes | Form 1040 line 14 (Add lines 12e, 13a, and 13b) is zero because nothing was recorded and that record is complete. |
| 1040 | 1040-14 | blocked | yes | Form 1040 line 14 (Add lines 12e, 13a, and 13b) has no value yet. It is waiting for the amounts it adds. |
| 1040 | 1040-14 | guard | no | Form 1040 line 14 (Add lines 12e, 13a, and 13b) has no condition that turns it off, so this sentence is not shown. |
| 1040 | 15 | published | yes | Form 1040 line 15 is taxable income: adjusted gross income minus the line 14 deduction total, and not below zero. |
| 1040 | 15 | computed zero | yes | Form 1040 line 15 (Taxable income) is zero because that subtraction is not above zero. |
| 1040 | 15 | closure zero | yes | Form 1040 line 15 (Taxable income) is zero because nothing was recorded and that record is complete. |
| 1040 | 15 | blocked | yes | Form 1040 line 15 (Taxable income) has no value yet. It is waiting for Amount from line 11a (adjusted gross income) and Add lines 12e, 13a, and 13b. |
| 1040 | 15 | guard | no | Form 1040 line 15 (Taxable income) has no condition that turns it off, so this sentence is not shown. |
| 1040 | 16 | published | yes | Form 1040 line 16 is the tax. With no qualified dividends and no preferential gain, it is the tax on taxable income. Otherwise it is the tax from the qualified dividends and capital gain worksheet. |
| 1040 | 16 | computed zero | yes | Form 1040 line 16 (Tax) is zero because the calculation comes to zero. |
| 1040 | 16 | closure zero | yes | Form 1040 line 16 (Tax) is zero because nothing was recorded and that record is complete. |
| 1040 | 16 | blocked | yes | Form 1040 line 16 has no value yet. It is waiting for taxable income and the facts the tax worksheet needs. |
| 1040 | 16 | guard | yes | Form 1040 line 16 (Tax) shows no value because one of its conditions does not hold. One sentence cannot say which condition. |
| 1040 | 1a | published | yes | Form 1040 line 1a is the total of box 1 wages, tips, and other compensation on Forms W-2. |
| 1040 | 1a | computed zero | yes | Form 1040 line 1a (Total amount from Form(s) W-2, box 1 (see instructions)) is zero because the calculation comes to zero. |
| 1040 | 1a | blocked | yes | Form 1040 line 1a has no value yet. It is waiting for the box 1 wage amounts, or for that wage record to be confirmed complete. |
| 1040 | 1a | guard | no | Form 1040 line 1a (Total amount from Form(s) W-2, box 1 (see instructions)) has no condition that turns it off, so this sentence is not shown. |
| 1040 | 20 | computed zero | yes | Form 1040 line 20 (Other nonrefundable credits from Schedule 3) is zero because the calculation comes to zero. |
| 1040 | 20 | closure zero | yes | Form 1040 line 20 (Other nonrefundable credits from Schedule 3) is zero because nothing was recorded and that record is complete. |
| 1040 | 20 | guard | no | Form 1040 line 20 (Other nonrefundable credits from Schedule 3) has no condition that turns it off, so this sentence is not shown. |
| 1040 | 3a | guard | yes | Form 1040 line 3a (Qualified dividends) shows no value because its condition does not hold. |
| 1040 | 3b | guard | yes | Form 1040 line 3b (Ordinary dividends) shows no value because its condition does not hold. |
| 1040 | 4b | published | yes | Fully taxable 2025 traditional, SEP, and SIMPLE IRA distributions from Form 1099-R box 1 and box 2a equality. |
| 1040 | 6a | published | yes | Total Social Security benefits from ordinary Form SSA-1099 box 5. |
| 1040 | 6b | published | yes | Taxable Social Security benefits from the standard Social Security Benefits Worksheet. |
| 1040 | 8 | computed zero | yes | Form 1040 line 8 (Additional income from Schedule 1) is zero because the calculation comes to zero. |
| 1040 | 8 | closure zero | yes | Form 1040 line 8 (Additional income from Schedule 1) is zero because nothing was recorded and that record is complete. |
| 1040 | 8 | guard | no | Form 1040 line 8 (Additional income from Schedule 1) has no condition that turns it off, so this sentence is not shown. |
| 1040 | 9 | published | yes | Form 1040 line 9 (Total income) adds Total amount from Form(s) W-2, box 1, Taxable interest, Ordinary dividends, Capital gain or (loss), Additional income from Schedule 1, Taxable IRA distributions, and Taxable Social Security benefits. |
| 1040 | 9 | computed zero | yes | Form 1040 line 9 (Total income) is zero because those amounts come to zero. |
| 1040 | 9 | closure zero | yes | Form 1040 line 9 (Total income) is zero because nothing was recorded and that record is complete. |
| 1040 | 9 | blocked | yes | Form 1040 line 9 (Total income) has no value yet. It is waiting for the amounts it adds. |
| 1040 | 9 | guard | no | Form 1040 line 9 (Total income) has no condition that turns it off, so this sentence is not shown. |
| 1040 | 22 | computed zero | yes | Form 1040 line 22 (Tax after nonrefundable credits) is zero because the calculation comes to zero. |
| 1040 | 22 | closure zero | yes | Form 1040 line 22 (Tax after nonrefundable credits) is zero because nothing was recorded and that record is complete. |
| 1040 | 22 | guard | yes | Form 1040 line 22 (Tax after nonrefundable credits) shows no value because its condition does not hold. |
| 1040-SCH-D | sch-d-13 | guard | no | Line 13: capital gain distributions has no condition that turns it off, so this sentence is not shown. |
| 1040-SCH-D | 14 | published | yes | Schedule D line 14 is the long-term capital loss carryover. |
| 1040-SCH-D | 14 | computed zero | yes | Line 14 long-term capital loss carryover is zero because the calculation comes to zero. |
| 1040-SCH-D | 14 | closure zero | yes | Line 14 long-term capital loss carryover is zero because nothing was recorded and that record is complete. |
| 1040-SCH-D | 14 | blocked | yes | Line 14 long-term capital loss carryover has no value yet. It is waiting for an answer it needs. |
| 1040-SCH-D | 14 | guard | no | Line 14 long-term capital loss carryover has no condition that turns it off, so this sentence is not shown. |
| 1040-SCH-D | sch-d-15 | computed zero | yes | Line 15: net long-term capital gain is zero because those amounts come to zero. |
| 1040-SCH-D | sch-d-15 | closure zero | yes | Line 15: net long-term capital gain is zero because nothing was recorded and that record is complete. |
| 1040-SCH-D | sch-d-15 | guard | no | Line 15: net long-term capital gain has no condition that turns it off, so this sentence is not shown. |
| 1040-SCH-D | sch-d-16 | computed zero | yes | Line 16: total gain is zero because those amounts come to zero. |
| 1040-SCH-D | sch-d-16 | closure zero | yes | Line 16: total gain is zero because nothing was recorded and that record is complete. |
| 1040-SCH-D | sch-d-16 | guard | no | Line 16: total gain has no condition that turns it off, so this sentence is not shown. |
| 1040-SCH-D | 1a-h | published | yes | Schedule D line 1a, column (h), is short-term proceeds minus basis for the transactions reported directly on Schedule D. |
| 1040-SCH-D | 1a-h | computed zero | yes | Line 1a column (h) is zero because the calculation comes to zero. |
| 1040-SCH-D | 1a-h | closure zero | yes | Line 1a column (h) is zero because nothing was recorded and that record is complete. |
| 1040-SCH-D | 1a-h | blocked | yes | Line 1a column (h) has no value yet. It is waiting for an answer it needs. |
| 1040-SCH-D | 1a-h | guard | yes | Line 1a column (h) shows no value because one of its conditions does not hold. One sentence cannot say which condition. |
| 1040-SCH-D | 1b-h | published | yes | Schedule D line 1b, column (h), is the short-term gain or loss from Form 8949. |
| 1040-SCH-D | 1b-h | computed zero | yes | Line 1b column (h) is zero because the calculation comes to zero. |
| 1040-SCH-D | 1b-h | closure zero | yes | Line 1b column (h) is zero because nothing was recorded and that record is complete. |
| 1040-SCH-D | 1b-h | blocked | yes | Line 1b column (h) has no value yet. It is waiting for an answer it needs. |
| 1040-SCH-D | 1b-h | guard | yes | Line 1b column (h) shows no value because one of its conditions does not hold. One sentence cannot say which condition. |
| 1040-SCH-D | 21 | published | yes | Schedule D line 21 is the capital loss allowed this year, after the yearly limit. |
| 1040-SCH-D | 21 | computed zero | yes | Line 21 limited loss is zero because the calculation comes to zero. |
| 1040-SCH-D | 21 | closure zero | yes | Line 21 limited loss is zero because nothing was recorded and that record is complete. |
| 1040-SCH-D | 21 | blocked | yes | Line 21 limited loss has no value yet. It is waiting for Line 16: total gain. |
| 1040-SCH-D | 21 | guard | no | Line 21 limited loss has no condition that turns it off, so this sentence is not shown. |
| 1040-SCH-D | 6 | published | yes | Schedule D line 6 is the short-term capital loss carryover. |
| 1040-SCH-D | 6 | computed zero | yes | Line 6 short-term capital loss carryover is zero because the calculation comes to zero. |
| 1040-SCH-D | 6 | closure zero | yes | Line 6 short-term capital loss carryover is zero because nothing was recorded and that record is complete. |
| 1040-SCH-D | 6 | blocked | yes | Line 6 short-term capital loss carryover has no value yet. It is waiting for an answer it needs. |
| 1040-SCH-D | 6 | guard | no | Line 6 short-term capital loss carryover has no condition that turns it off, so this sentence is not shown. |
| 1040-SCH-D | 7 | published | yes | Line 7 net short-term adds Line 1a column (h), Line 1b column (h), and Line 6 short-term capital loss carryover. |
| 1040-SCH-D | 7 | computed zero | yes | Line 7 net short-term is zero because those amounts come to zero. |
| 1040-SCH-D | 7 | closure zero | yes | Line 7 net short-term is zero because nothing was recorded and that record is complete. |
| 1040-SCH-D | 7 | blocked | yes | Line 7 net short-term has no value yet. It is waiting for the amounts it adds. |
| 1040-SCH-D | 7 | guard | no | Line 7 net short-term has no condition that turns it off, so this sentence is not shown. |
| 1040-SCH-D | 8a-h | guard | yes | Line 8a, column (h): gain shows no value because one of its conditions does not hold. One sentence cannot say which condition. |
| 1040-SCH-D | 8b-h | published | yes | Schedule D line 8b, column (h), is the long-term gain or loss from Form 8949. |
| 1040-SCH-D | 8b-h | computed zero | yes | Line 8b column (h) is zero because the calculation comes to zero. |
| 1040-SCH-D | 8b-h | closure zero | yes | Line 8b column (h) is zero because nothing was recorded and that record is complete. |
| 1040-SCH-D | 8b-h | blocked | yes | Line 8b column (h) has no value yet. It is waiting for an answer it needs. |
| 1040-SCH-D | 8b-h | guard | yes | Line 8b column (h) shows no value because one of its conditions does not hold. One sentence cannot say which condition. |
| 1040-SCH-1 | sch1-10 | computed zero | yes | Schedule 1 line 10 (Additional income) is zero because the calculation comes to zero. |
| 1040-SCH-1 | sch1-10 | closure zero | yes | Schedule 1 line 10 (Additional income) is zero because nothing was recorded and that record is complete. |
| 1040-SCH-1 | sch1-10 | guard | no | Schedule 1 line 10 (Additional income) has no condition that turns it off, so this sentence is not shown. |
| 1040-SCH-1 | sch1-21 | guard | no | Schedule 1 line 21 (Student loan interest deduction) has no condition that turns it off, so this sentence is not shown. |
| 1040-SCH-1 | sch1-7 | computed zero | yes | Schedule 1 line 7 (Unemployment compensation) is zero because the calculation comes to zero. |
| 1040-SCH-1 | sch1-7 | closure zero | yes | Schedule 1 line 7 (Unemployment compensation) is zero because nothing was recorded and that record is complete. |
| 1040-SCH-1 | sch1-7 | guard | yes | Schedule 1 line 7 (Unemployment compensation) shows no value because its condition does not hold. |
| 1040-SCH-1 | sch1-top | guard | no | Schedule 1, form 1099-K personal item sale loss gross payment amount (Schedule 1 top entry) has no condition that turns it off, so this sentence is not shown. |
| 1040-Schedule-3 | Sch3-1 | computed zero | yes | Schedule 3 line 1 (Foreign tax credit) is zero because the calculation comes to zero. |
| 1040-Schedule-3 | Sch3-1 | closure zero | yes | Schedule 3 line 1 (Foreign tax credit) is zero because nothing was recorded and that record is complete. |
| 1040-Schedule-3 | Sch3-1 | guard | yes | Schedule 3 line 1 (Foreign tax credit) shows no value because one of its conditions does not hold. One sentence cannot say which condition. |
| 1040-Schedule-3 | Sch3-8 | computed zero | yes | Schedule 3 line 8 (Total other nonrefundable credits) is zero because the calculation comes to zero. |
| 1040-Schedule-3 | Sch3-8 | closure zero | yes | Schedule 3 line 8 (Total other nonrefundable credits) is zero because nothing was recorded and that record is complete. |
| 1040-Schedule-3 | Sch3-8 | guard | yes | Schedule 3 line 8 (Total other nonrefundable credits) shows no value because one of its conditions does not hold. One sentence cannot say which condition. |
| 1040-SCH-1 | sch1-8b | computed zero | yes | Schedule 1 line 8b (Gambling) is zero because the calculation comes to zero. |
| 1040-SCH-1 | sch1-8b | closure zero | yes | Schedule 1 line 8b (Gambling) is zero because nothing was recorded and that record is complete. |
| 1040-SCH-1 | sch1-8b | guard | no | Schedule 1 line 8b (Gambling) has no condition that turns it off, so this sentence is not shown. |

## Mechanics

The current sentences are the `explain` strings on the form-field citizen the package pins. `form-field.v2` and `form-field.v3` both require `explain` to be a string of at least one character. Neither sets a max length or a pattern on `explain`. `render` is a string and may be empty. The only pattern in those schemas is on version strings (`v` plus digits). Nothing in the schema, the projection, or the page checks that a sentence names the line.

All 37 distinct generic sentences also appear outside `packages/content`, in 50 files among the 796 tests and sample-data files scanned. The scan looks for the explain string as a JSON `"explain"` value, and for a sentence longer than 40 characters as raw text. The hits are presentation-model goldens and tests that copied those sentences. They pin the bytes of the versions they name. A successor adds a version. It does not edit a published form-field file, so those goldens stay valid for v77 and earlier. `load_form_fields` keeps the highest version of an id. A test that loads fields that way, rather than through the package pin, would see the new sentence once the new file is in the corpus.

A new field version and a package successor are enough to change the words. The projection copies the package-pinned citizen into the section, and the page prints `instruction.explain`. No schema change, no projection change, and no engine change is required to replace a sentence. The page's choice to hide the blocked sentence when questions exist is a page behavior. Putting that sentence beside the questions would be a change in `renderLine` of `citation-walk.v1.html`. This unit does not make it. The no-citation refusal on a numeric line is the same kind of page behavior.

The next free identities are package v78, registry `published-packages.v76.json`, and release `demo.release.sli-worksheet-integration.2025.v76.json`. Succeeding the 36 fields that have a selectable generic text adds 36 form-field files (32 `form-field.v3`, 4 `form-field.v2`) plus the package, the registry, and the release: 39 new files. Eight of those fields are also entrypoints, so their pins update inside the package and do not add files. Succeeding every field that has any generic text, including the three whose only generic text is a guard the rule never selects, adds 39 field files plus the same three package files: 42. The old version files stay.

A live run of v78 needs `packages/tax/loader.py` to share v77's companion declaration. Without that entry the loader falls back to the global maps and refuses amounts v77 admits. The closure-question switch is already on for any core at v75 or later, and the later-arm switch for any core at v76 or later, so v78 inherits both by version rank. The prototype shares the declaration in-process and does not edit the loader. That handshake is the established package-version step, not a schema, engine, or projection change.

## Recommendation

Succeed the 36 fields that have a selectable generic text, as new form-field versions on package v78, registry v76, and release v76, and leave every published v77 byte in place. That is 39 new files. The three fields whose only generic text is a guard the rule never selects can stay. A scratch v78 with three of those successors (Form 1040 lines 9 and 12e, and Schedule D line 7) published the same 73 values and dispositions as v77 on the wages return; the three new sentences appeared on the page, and line 16, which was not succeeded, still said "published tax." Track 1 adds the loader companion share for v78. No schema, engine, or projection change is required. The page already hides a blocked sentence when questions exist, and it refuses a numeric line that has no citation; those are page findings, and this wording change does not depend on them.
