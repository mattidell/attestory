# P0 — 2025 earned income credit law and scope

Sources (downloaded, ignored, under `temp/tax-on-taxable-income/sources/`):
`i1040gi-2025` (Form 1040 instructions), `rp-2024-40` (Rev. Proc. 2024-40),
`f1040-2025`. Citations are text lines of the `.txt` extract unless noted.
Pub. 596 was not needed. Where a source is silent, this file says so.

## 1. Law table

Form 1040 line 27a is the earned income credit. Line 27b is the clergy
Schedule SE checkbox. Line 27c is checked when the filer does not take the
credit. Line 32 is lines 27a through 31 (`f1040-2025.txt` l.123-131).

### All filers (Step 1)

| Test | Rule | Citation |
| --- | --- | --- |
| AGI ceiling | Line 11b must be **less than** the completed phaseout amount for the number of qualifying children who have valid SSNs and the filing status. At the amount, stop. | `i1040gi-2025.txt` l.2644-2659 |
| Filer and spouse SSN | Filer, and spouse if a joint return, must have an SSN issued on or before the due date of the 2025 return (including extensions) that is valid for EIC purposes. Otherwise stop and check line 27c. | l.2662-2666, l.2967-3001 |
| Form 2555 | Filing Form 2555: stop. | l.2608-2614 |
| Nonresident alien | A nonresident alien for any part of 2025 stops, unless the filer checked the box to treat a nonresident or dual-status alien spouse as a U.S. resident for the whole year. | l.2617-2619, l.2937-2941 |
| Prior disallowance | Form 8862 is required if the EIC for a year after 1996 was reduced or disallowed for a reason other than a math or clerical error, with the stated exceptions (a later allowed year; a no-child claim disallowed only because a Schedule EIC child was not a qualifying child). A reckless or fraud determination bars the credit for 2 or 10 years. | l.2630-2636, l.2871-2889 |

### Investment income (Step 2)

| Item | Rule | Citation |
| --- | --- | --- |
| Sum | Line 2a + line 2b + line 3b + line 7a. If line 7a is a loss, enter 0. | l.2627-2636 |
| Limit | More than **$11,950** is the question. At $11,950 the answer is no. | l.2641; `rp-2024-40.txt` l.327-332 |
| Over the limit, no Form 4797 | Stop. No credit. | l.2645-2651 |
| Over the limit, Form 4797 in line 7a | Must use Worksheet 1 in Pub. 596. Otherwise stop. | l.2645-2651, l.2866-2870 |
| At or under the limit | Skip the Form 4797 question. If the filer has Schedule E, rental of personal property not used in a business, Form 8814, or passive-activity income or loss, Worksheet 1 is still required. If none of those apply, go to Step 3. | l.2641-2662 |

The instructions do not define a fifth investment-income addend inside Step 2's sum. Worksheet 1 is the source for anything those four items add, and this file does not restate Pub. 596.

### Qualifying child (Step 3)

A qualifying child for the EIC is all of the following (`i1040gi-2025.txt` l.2669-2728):

- Relationship: son, daughter, stepchild, foster child, brother, sister, stepbrother, stepsister, half brother, half sister, or a descendant of any of them.
- Age: under 19 at the end of 2025 and younger than the filer (or the spouse, if joint); or under 24, a full-time student, and younger than the filer (or spouse); or any age and permanently and totally disabled.
- Return: not filing a joint return, or filing a joint return only to claim a refund of withheld income tax or estimated tax.
- Residency: lived with the filer in the United States for more than half of 2025. Temporary absence, birth, death, foster or adoption placement, and kidnapping have exceptions (l.2733-2736, l.2849-2864). United States is the 50 states and the District of Columbia (l.3002-3003).

| Test | Rule | Citation |
| --- | --- | --- |
| No such child | Skip to Step 4. | l.2672-2673 |
| Joint return | Skip the rest of Step 3 and Step 4. Go to Step 5. | l.2676-2678 |
| Married, filing MFS or head of household | Must meet the separated-spouse rule below. An unmarried head of household answers this question no. | l.2681-2684 |
| Not married MFS or HOH | Skip the separated-spouse questions. Still answer whether the filer could be a qualifying child of another person. | l.2681-2684, l.2706-2728 |
| Filer could be a qualifying child of another person | Stop, unless that other person is not required to file and is not filing, or is filing only to claim a refund of withheld or estimated tax. | l.2706-2716 |
| Child of more than one person | Only one person can claim the child for the five listed benefits. Order: the parent; then the parents' joint return; then the parent with the longer residency, or the higher 2025 AGI if time is equal; if no parent can claim, the person with the highest AGI; if a parent can claim but does not, another person only if that person's AGI is higher than every parent's who can claim. | l.2913-2964 |
| Child without a valid SSN | Not counted in the number of children. The filer still attaches Schedule EIC. A child who meets the four conditions above is still a qualifying child, so Step 4 does not apply. | l.2619-2625, l.2999-3001 |
| Married child | A qualifying child only if the filer can claim the child as a dependent, or could except for the divorced-or-separated-parents rule. | l.2919-2927 |

### Filers without a qualifying child (Step 4)

| Test | Rule | Citation |
| --- | --- | --- |
| MFS or head of household | Stop. No credit. | l.2737-2746 |
| Age | At least 25 but under 65 at the end of 2025. The instruction says to check yes if the filer, or the spouse on a joint return, was born after December 31, 1960, and before January 2, 2001. A spouse who died in 2025 is referred to Pub. 596; these sources do not state that case. | l.2748-2758 |
| Main home | Filer's main home, and the spouse's if joint, in the United States for more than half of 2025. Extended active duty outside the United States counts as the home being in the United States. | l.2763-2778, l.2930-2936 |
| Joint return | Skip the next two questions. | l.2781-2783 |
| Filer could be a qualifying child of another person | Stop, with the same not-required-to-file proviso as Step 3. | l.2787-2797 |
| Can be claimed as a dependent | Stop, with the same proviso. | l.2799-2807 |

### Earned income and the worksheet (Steps 5 and 6)

Worksheet A applies when Step 5 question 2 is no. Worksheet B applies to self-employment, clergy, church-employee income, and statutory employees (`i1040gi-2025.txt` l.2799-2805, l.3011-3013, l.3075-3077). Worksheet B is not restated here; the milestone does not compute it.

Earned income on Worksheet A (`l.2756-2794`):

1. Form 1040 line 1z.
2. Subtract Medicaid waiver payments excluded on Schedule 1 line 8s, unless the filer chooses to include them (then enter 0).
3. Add nontaxable combat pay the filer elects to include (also entered on line 1i). Each spouse elects separately.

Clergy and church employees replace line 1z or line 1a with a Schedule SE subtraction before that worksheet (`l.2858-2886`). That is Worksheet B's path.

Step 5 question 3: earned income must be **less than** the same completed phaseout amount as Step 1 (`l.2808-2821`).

Worksheet A (`l.3015-3058`):

| Line | Rule |
| --- | --- |
| 1 | Earned income from Step 5. |
| 2 | EIC Table credit for line 1, using filing status and the number of qualifying children who have valid SSNs. If 0, stop. |
| 3 | Line 11b. |
| 4 | If line 3 equals line 1, line 6 is line 2. |
| 5 | If line 3 is less than the threshold phaseout amount ($10,620, or $17,730 if joint, with no qualifying child who has a valid SSN; $23,350, or $30,470 if joint, with one or more), leave line 5 blank and keep line 2. Otherwise look up line 3 and enter the smaller of that credit and line 2 on line 6. |
| 6 | The credit. Enter on line 27a. |

Line 11b is "Amount from line 11a (adjusted gross income)" (`f1040-2025.txt` l.82-86). These sources show no difference between 11a and 11b. The worksheet compares line 11b.

The compared AGI is the greater of earned income and AGI only in the Rev. Proc.'s description of the phaseout amounts (`rp-2024-40.txt` l.287-293). The worksheet implements that by taking the smaller table credit.

### Married filing separately, 2025

MFS is not barred outright.

- No qualifying child: Step 4 stops. Credit is $0 (`i1040gi-2025.txt` l.2737-2746). The same stop applies to head of household with no qualifying child.
- With a qualifying child: a married filer whose status is MFS or head of household can take the credit under the separated-spouse rule (l.2950-2963): the child lived with the filer in the United States for more than half of 2025, and either the filer lived apart from the spouse for the last 6 months of 2025, or the filer is legally separated under a written separation agreement or a decree of separate maintenance and did not live in the same household at the end of 2025.
- Those filers use the single / head of household / qualifying surviving spouse column of the table (star note, l.3544). Rev. Proc. 2024-40 §2.06(1) says the non-joint threshold and completed amounts also apply to married taxpayers who do not file jointly and who meet §32(d) (`rp-2024-40.txt` l.303-307).

Qualifying surviving spouse uses the non-joint column (table header, l.3226-3228).

### SSN

For the EIC, a valid SSN is a number issued by the Social Security Administration, unless "Not Valid for Employment" is printed on the card and the number was issued solely to apply for or receive a federally funded benefit. A card that says "Valid for Work Only With DHS Authorization" is valid for the EIC only while that authorization is still valid. The SSN must have been issued on or before the due date of the 2025 return, including extensions. This applies to the filer, the spouse on a joint return, and each child who is counted. A child without such an SSN is not counted on an original or an amended return (`i1040gi-2025.txt` l.2662-2666, l.2967-3001).

### 2025 amounts

Rev. Proc. 2024-40 §2.06 (`rp-2024-40.txt` l.279-332). "Other" is every status except married filing jointly, including MFS filers who meet the separated-spouse rule.

| Children | Earned income amount | Maximum credit | Phaseout starts, other | Completed, other | Phaseout starts, MFJ | Completed, MFJ |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | $8,490 | $649 | $10,620 | $19,104 | $17,730 | $26,214 |
| 1 | $12,730 | $4,328 | $23,350 | $50,434 | $30,470 | $57,554 |
| 2 | $17,880 | $7,152 | $23,350 | $57,310 | $30,470 | $64,430 |
| 3 or more | $17,880 | $8,046 | $23,350 | $61,555 | $30,470 | $68,675 |

The earned income amount is the earned income at or above which the maximum credit is allowed. The threshold phaseout amount is the AGI (or, if greater, earned income) above which the maximum begins to phase out. The completed phaseout amount is where no credit is allowed (`rp-2024-40.txt` l.283-293).

The instructions use the same dollars. Step 1 and Step 5 say "less than" each completed amount (`i1040gi-2025.txt` l.2644-2656, l.2808-2819). Worksheet A line 5 says "less than" each threshold amount (l.3038-3043). The investment-income limit is $11,950 in both (l.2641; `rp-2024-40.txt` l.327-332).

The Rev. Proc. and the instructions do not state the credit or phaseout percentages. Section 3 records the rates that reproduce these maximums and the table.

## 2. Classification

Symbols are published findings the v52 rules already produce. A new question is a new fact type. "Outside" means the slice cannot compute the credit and must not publish $0.

| Test | Class | Where it lives |
| --- | --- | --- |
| Filing status, including the MFS and head-of-household stops when there is no qualifying child, and which table column applies | Computed | `tax.us.2025.filing-status` (`single`, `married_filing_jointly`, `married_filing_separately`, `head_of_household`, `qualifying_surviving_spouse`) |
| Line 11b / AGI ceiling and Worksheet A lines 3-6 | Computed | `tax.us.2025.income.agi`, published by `tax.us.2025.rule.form1040-line11` v2, which cites line 11a and line 11b. The form defines 11b as the amount from 11a. |
| Investment-income sum | Computed, after the Worksheet 1 question below is answered no | `tax.us.2025.tax-exempt-interest.line2a-total` + `tax.us.2025.interest.taxable-total` + `tax.us.2025.dividends.ordinary-total` + the positive part of `tax.us.2025.capital-gains.line7a-total`. A loss on line 7a contributes 0. |
| Earned income for this class | Computed, after the Worksheet B and earned-income-adjustment questions below are answered no | `tax.us.2025.wages.total-w2-box1`, the W-2 box 1 total published by `tax.us.2025.rule.w2-box1-to-line1a` v2 and used as the wage term of line 9. The engine has no line 1b-1h, line 1i, or Schedule 1 line 8s amount. On this class line 1z is that total. |
| Joint return skips Step 4 questions 5 and 6, and Step 3 questions 3-6 | Computed | Same filing-status fact |
| Filer SSN valid for the EIC | New question | Draft: "Was your social security number issued by the Social Security Administration on or before the due date of your 2025 return, including extensions, and is it valid for the earned income credit? Answer no if the card says 'Not Valid for Employment' and the number was issued only so you could apply for or receive a federally funded benefit. If the card says 'Valid for Work Only With DHS Authorization,' answer yes only while that authorization is still valid." No means the credit is $0. |
| Spouse SSN, joint return only | New question | Same wording, for the spouse. Asked only when filing status is married filing jointly. |
| Form 2555 | New question | Draft: "Are you filing Form 2555 for 2025?" Yes blocks this route. |
| Nonresident alien | New question | Draft: "Were you, or your spouse, a nonresident alien for any part of 2025? Answer no if you checked the box to treat a nonresident or dual-status alien spouse as a U.S. resident for the entire year." Yes means the credit is $0. |
| At least one EIC qualifying child | New question for slice (a); per-child facts for slice (b) | Draft for slice (a): "Do you have at least one child who meets the relationship, age, residency, and joint-return conditions to be your qualifying child for the earned income credit, whether or not that child has a valid social security number?" Yes is outside slice (a). It is not a $0 credit. |
| Age 25 through 64, no qualifying child | New question | Draft: "Were you, or your spouse if you are filing a joint return, born after December 31, 1960, and before January 2, 2001?" No means the credit is $0. A spouse who died in 2025 is outside this slice; Pub. 596 is the source the instructions point to and it was not used here. |
| Main home in the United States | New question | Draft: "Was your main home, and your spouse's if you are filing a joint return, in the United States for more than half of 2025? If you were on extended active duty outside the United States, treat that duty as time your main home was in the United States." No means the credit is $0. |
| Filer could be a qualifying child of another person | New question, not asked on a joint return | Draft: "Could you be a qualifying child of another person for 2025? Answer no if that person is not required to file a 2025 return, and is not filing one, or is filing only to claim a refund of withheld income tax or estimated tax." Yes means the credit is $0. |
| Filer can be claimed as a dependent | New question, not asked on a joint return | Draft: "Can you be claimed as a dependent on someone else's 2025 return? Answer no if the person who could claim you is not required to file, and is not filing, or is filing only to claim a refund of withheld income tax or estimated tax." Yes means the credit is $0. |
| Form 8862 or a 2-year or 10-year bar | New question | Draft: "For a year after 1996, was your earned income credit reduced or disallowed for a reason other than a math or clerical error, so that you must file Form 8862 or are in a 2-year or 10-year period in which you cannot take the credit?" Yes is outside this slice. The milestone does not compute Form 8862. |
| Worksheet B | New question | Draft: "Were you self-employed at any time in 2025, filing Schedule SE because you were a member of the clergy or had church employee income of $108.28 or more, or filing Schedule C as a statutory employee?" Yes is outside. Worksheet B is not computed. |
| Combat pay election, Medicaid waiver exclusion | New questions | Draft: "Are you electing to include nontaxable combat pay in earned income?" and "Did you exclude Medicaid waiver payments on Schedule 1, line 8s, that Worksheet A would subtract?" Yes on either is outside. The engine does not compute those amounts. |
| Schedule E, Form 4797, Form 8814, personal-property rental, passive activity | New question | Draft: "For 2025, are you filing Schedule E, Form 4797, or Form 8814, reporting income from renting out personal property that is not used in a business, or reporting income or loss from a passive activity?" Yes is outside. Worksheet 1 is not computed. No leaves the four-line sum as the whole investment-income test. |
| Qualifying-child elements, tie-breaker, separated-spouse rule | Outside slice (a). Slice (b) asks them. | See section 4. |
| Decline the credit (line 27c) | Not an eligibility test | The instructions let a filer check line 27c and not claim an otherwise available credit. This slice does not add that election. |

### Senior-deduction SSN facts

`tax.us.2025.senior-deduction.taxpayer-valid-ssn` and `tax.us.2025.senior-deduction.spouse-valid-ssn` are not the EIC test.

Their published titles say the person has a social security number valid for employment, issued before the due date of the 2025 return including extensions, for Schedule 1-A Part V. The EIC instructions add two conditions those titles do not state: the "Not Valid for Employment" card is invalid only when it was issued solely for a federally funded benefit, and a "Valid for Work Only With DHS Authorization" card is valid for the EIC only while the authorization lasts (`i1040gi-2025.txt` l.2967-2989).

The senior facts are also the wrong population. They are required only for a person recorded as 65 or older on a return that is not married filing separately. The EIC question is for every filer, and for the spouse on every joint return, including filers under 65.

Reusing the recorded answer would give the EIC a yes/no that was made for Part V. Widening the published title so one question served both statutes would edit a published fact and would change what a senior-deduction "yes" means. The same split was already made for Form 2555: `tax.us.2025.sli-scope.no-form-2555` was minted new rather than reusing `tax.us.2025.ss-benefits-scope.no-form-2555`. The EIC gets its own questions.

`tax.us.2025.taxpayer-over-65` is "Taxpayer is over 65 years of age for 2025." It is not the EIC birth-date test. The EIC parenthetical includes a person born on January 1, 1961. The standard-deduction convention treats a person born on that day as age 65 (born before January 2, 1961). One fact cannot be both. The under-25 end of the parenthetical is a different fact the engine does not have.

`tax.us.2025.standard-deduction.can-be-claimed-as-dependent` is one return-level answer: someone can claim the taxpayer, or the spouse on a joint return. The EIC asks only the filer, only when the return is not joint, and it tells the filer to answer no when the other person is not required to file. That published title does not say the proviso. It stays the standard-deduction fact.

## 3. The EIC Table

The table is $50 bands (`i1040gi-2025.txt` l.3232 onward). The first printed row is "at least $1 but less than $50," the $0–$50 band with $0 omitted. A $0 lookup is not a row; the credit is $0. Every later row is $50 wide, through "at least $68,650 but less than $68,700."

The cell is the statutory credit at one point in the band, rounded half up to the nearest dollar. The point is the midpoint, $25 above the band floor, except at three corners:

- The band contains the completed phaseout amount. The point is the halfway point between the band floor and that amount. The printed cell is a star. The footnote gives that one credit for every dollar from the band floor up to, but not including, the completed amount. At the completed amount and above, the credit is $0 and Step 1 has already stopped.
- The band contains the earned income amount and the midpoint is still below it. The point is the earned income amount, so the cell is the maximum credit. The band $8,450–$8,500 contains $8,490; round($8,475 × 7.65%) is $648, and the cell is $649.
- The band floor is below the phaseout threshold and the midpoint is above it. The point is the threshold, so the cell is still the maximum. The band $30,450–$30,500 contains the joint $30,470 threshold; the midpoint credit would be $1 under the maximum for one, two, and three children, and the cells are the maximums. A band that starts exactly on the threshold uses the midpoint. $23,350–$23,400 is $4,324 for one child, other statuses.

Credit at that point, for child count *n* and status (joint, or other):

- If the point is at or above the earned income amount, the phase-in result is the maximum credit.
- Otherwise the phase-in result is the half-up rounding of point × credit rate, not above the maximum.
- If the point is at or below the phaseout threshold, that phase-in result is the credit.
- Otherwise the credit is the half-up rounding of maximum − phaseout rate × (point − threshold), and not below $0.

Rounding is applied to the credit. It is not applied to the reduction first. $25 × 15.98% = $3.995; $4,328 − $3.995 = $4,324.005, which rounds to $4,324, the other-status one-child cell for $23,350–$23,400 (l.3513).

The Rev. Proc. and the instructions do not state the percentages. These rates reproduce each maximum and every table cell:

| Children | Credit rate | Phaseout rate | Maximum check |
| --- | --- | --- | --- |
| 0 | 7.65% | 7.65% | $8,490 × 7.65% = $649.485 → $649 |
| 1 | 34% | 15.98% | $12,730 × 34% = $4,328.20 → $4,328 |
| 2 | 40% | 21.06% | $17,880 × 40% = $7,152 |
| 3 or more | 45% | 21.06% | $17,880 × 45% = $8,046 |

The expression operations are the ones `rule.qdcg-worksheet.line-24` already uses for the Tax Table midpoint, which `rule.form1040-line16` v6 reads: `divide` rounded down to a whole number of $50 bands, `multiply` by 50, `add` 25. The corners are `compare` and `choose`. The partial midpoint divides by 2 and keeps one decimal place, because $61,555 and $68,675 are odd. `multiply` by the rate, then `round` with mode `half_up`. There is no `min` operation; the cap at the maximum is `choose`. A negative phaseout result uses `max` with 0. `rounding.convention` has `half_up` as its only value; the table rule can carry `half_up` as a literal so it does not depend on that assertion. No new operation.

`probe.py` beside this file parses the instruction text and checks the formula. It matched all 1,374 bands, 10,984 numeric cells, and all 8 footnote bands. Checked rows include the first band, the $2,455 example (one child, $842, l.3221-3223), the earned-income-amount bands, both phaseout-threshold bands, and each column's last nonzero band.

Footnote credits, for an amount still below the completed phaseout: other/0 $0 (l.3545); joint/0 $1 (l.3632); other/1 $3 (l.3974); other/2 $1 (l.4047); joint/1 $0 (l.4051); other/3 $1 (l.4055); joint/2 $3 (l.4142); joint/3 $3 (l.4175).

## 4. Slice recommendation

Recommend slice (a): filers with no qualifying child.

Slice (a) uses the questions in section 2 and Worksheet A on `tax.us.2025.wages.total-w2-box1`, with the 0-child column. Joint wages are already one total. Single and qualifying surviving spouse use the other column. Married filing jointly uses the joint column. Married filing separately and head of household, with no qualifying child, are a computed $0 from filing status.

It publishes $0, and can say why, when the SSN, age, main-home, qualifying-child-of-another, or dependent answer fails; when the filer was a nonresident alien; when the four-line investment sum is over $11,950; when AGI or earned income is at or above the completed amount; or when the table credit is $0.

It rejects, and does not publish $0, when:

- the filer has a qualifying child, including a child who meets the four conditions and has no valid SSN (that filer is not on Step 4, and the 0-child column is not the childless age test);
- Worksheet B applies;
- the filer elects combat pay or has a Medicaid waiver exclusion Worksheet A would subtract;
- Schedule E, Form 4797, Form 8814, personal-property rental, or a passive activity is present;
- Form 8862 or a disallowance bar applies;
- a spouse died in 2025 and the age answer depends on Pub. 596.

No tie-breaker arises. There is no child to assign.

Slice (b) adds, for each child, relationship, the age branch (under 19, or under 24 and a full-time student, or any age and permanently and totally disabled) including younger than the filer or the spouse, residency, the child's joint return, and an EIC-valid SSN. `fact-type.v2` already allows an entity identity key, so a child does not by itself need a new fact-type schema. A child with no valid SSN is not counted, and the filer still does not take Step 4. Married filing separately or head of household with a qualifying child also needs the separated-spouse questions, and then uses the other column. Schedule EIC has to be attached; the credit figure is not that schedule.

The tie-breaker is the rejection. If another person can also claim the child, the engine does not have that person's AGI, the days the child lived with each person, or whether the other person claims the child. Slice (b) should refuse that case rather than pick a parent.

Cost. Slice (a) is about 14 new fact types (the section 2 questions, counting combat pay and the Medicaid waiver separately, plus the lines 28–31 absence in section 5), one parameter for the limit and the 0-child amounts and rates, and about 12 rules: investment income, the eligibility gate, Worksheet A lines 1 through 6, line 27a, the lines 28–31 zero, the successor 27a–31 total, and the successor line 32. The case list in section 6 is the path test set. No schema successor, no new expression operation, no engine change.

Slice (b) adds about eight fact types on a child entity, two separated-spouse facts, the other child-count rows of the same parameter (the formula already covers them), and about six more rules. The cases multiply: one, two, and three children, across phase-in, plateau, and phase-out, plus the tie-breaker refusal, the child with no SSN, and the separated spouse. That is the larger slice. It can follow (a). It should not be first.

## 5. Absence split

`tax.us.2025.lines27-31-scope.no-refundable-credits-or-other-payments` says the return claims none of lines 27a–31: the earned income credit, the additional child tax credit, the American opportunity credit, the refundable adoption credit, and Schedule 3 Part II. Its only consumer is `tax.us.2025.rule.form1040-lines27-31-total` v1, which publishes `tax.us.2025.payments.lines27-31-total` as 0 when the answer is yes, and blocks otherwise. `tax.us.2025.rule.form1040-line32` adds that total.

The successor needs a new fact whose only meaning is lines 28–31. Yes publishes those four lines as 0. No blocks. Line 27a comes from Worksheet A line 6, including a real $0 when a test in section 4 fails. A successor of the lines 27–31 total adds line 27a to that lines 28–31 zero. A successor of line 32 reads the new total. The v52 fact and rules stay as they are. Packages and goldens on v52 keep them.

A workspace that already answered the v52 question keeps that finding on the old fact. The successor package does not read it. The old yes is not line 27a, and it is not the new lines 28–31 fact. The run blocks with the new facts named. It does not keep a silent $0, and it does not compute a credit from the old answer. Someone eligible today could only stay in the class by answering yes, so that yes does not mean the worksheet credit is $0. A workspace that stays on the v52 package is unchanged.

## 6. Case table

No qualifying child. Investment income is $0 and AGI equals earned income unless the row says otherwise. Table cells are the printed rows cited. Ages are inside the parenthetical unless the row says otherwise.

| Case | Worksheet | Credit |
| --- | --- | --- |
| Single, wages $5,000 | Line 2 is the $5,000–$5,050 cell, $384 (l.3276). Line 3 equals line 1. | $384 |
| Single, wages $9,000, plateau | $9,000–$9,050 is $649 (l.3312). $8,490 is the earned income amount; $10,620 is the threshold. | $649 |
| Single, wages $15,000, phase-out | $15,000–$15,050 is $312 (l.3453). | $312 |
| Single, wages $19,050 | Last positive other/0 band, $19,050–$19,100, is $2 (l.3491). | $2 |
| Single, wages $19,100 through $19,103 | Starred band. Footnote credit $0 (l.3545). | $0 |
| Single, wages $19,104 | Step 1 stops. Not less than $19,104. | $0 |
| Single, wages $9,000, born on or before December 31, 1960, or on or after January 2, 2001 | Step 4 age question is no. The table cell would be $649. | $0 |
| Single, wages $5,000, taxable interest $11,950 | Investment income is not more than $11,950. Earned-income credit $384. AGI $16,950 is not under $10,620. The $16,950–$17,000 cell is $163 (l.3428). Line 6 is the smaller. | $163 |
| Single, wages $5,000, taxable interest $11,951 | Step 2 stops. The worksheet is not reached. | $0 |
| Single, wages $9,000, taxable interest $11,950 | Investment income is at the limit, so Step 2 does not stop. AGI $20,950 is not less than $19,104. Step 1 stops. | $0 |
| Single, wages $9,000, taxable interest $6,000 | Investment income $6,000. Earned-income credit $649. AGI $15,000 looks up to $312. Line 6 is the smaller. | $312 |
| Single, wages $5,000, taxable interest $2,000 | Investment income $2,000. AGI $7,000 is less than $10,620, so line 5 stays blank. Line 6 is the earned-income credit. The $7,000 cell is $537 (l.3336), which is larger, so the smaller-of step would not have changed it. | $384 |
| Single, wages $9,000, line 7a a $3,000 loss | The loss enters the investment-income sum as $0. AGI $6,000 is under $10,620. | $649 |
| Joint, one spouse's wages $4,000 and the other's $4,000 | Line 1z is $8,000. The $8,000–$8,050 cell is $614 on the joint column too (l.3356). Under the joint $17,730 threshold. | $614 |
| Joint, combined wages $20,000 | Under the joint completed amount $26,214. The $20,000–$20,050 joint/0 cell is $473 (l.3510). The same wages on a single return are past $19,104 and are $0. | $473 |
| Joint, combined wages $26,200 through $26,213 | Footnote credit $1 (l.3632). | $1 |
| Joint, combined wages $26,214 | Step 1 stops. | $0 |
| Married filing separately, or head of household, wages $9,000, no qualifying child | Step 4 question 1 stops. | $0 |

## 7. Change list

Proposed ids only. Nothing here is created. Parameters and rules are successors; no published version is edited.

Facts, each domain yes/no, no default:

| Id | Role |
| --- | --- |
| `tax.us.2025.eic.taxpayer-valid-ssn` | Section 2 SSN question |
| `tax.us.2025.eic.spouse-valid-ssn` | Spouse, joint only |
| `tax.us.2025.eic.no-form-2555` | Yes means not filing Form 2555 |
| `tax.us.2025.eic.not-nonresident-alien` | The section 2 question, including the full-year resident election |
| `tax.us.2025.eic.no-qualifying-child` | Yes means slice (a). No rejects |
| `tax.us.2025.eic.age-25-under-65` | The birth-date parenthetical |
| `tax.us.2025.eic.main-home-in-us` | Includes the military sentence |
| `tax.us.2025.eic.not-qualifying-child-of-another` | Not asked on a joint return |
| `tax.us.2025.eic.not-claimable-as-dependent` | Not asked on a joint return |
| `tax.us.2025.eic.no-form-8862` | Yes means no Form 8862 and no bar. No rejects |
| `tax.us.2025.eic.no-worksheet-b` | Yes means Worksheet A. No rejects |
| `tax.us.2025.eic.no-combat-pay-election` | No rejects |
| `tax.us.2025.eic.no-medicaid-waiver-exclusion` | No rejects |
| `tax.us.2025.eic.no-worksheet-1-items` | Schedule E, Form 4797, Form 8814, personal-property rental, passive activity. No rejects |
| `tax.us.2025.lines28-31-scope.no-other-refundable-credits` | Lines 28–31 only |

Parameter:

- `tax.us.2025.parameter.eic-2025` — $11,950; for each child count and for joint versus other, the earned income amount, maximum, credit rate, phaseout rate, phaseout threshold, and completed amount. Slice (a) reads the 0-child rows. The other rows are the verified table, stored so a later child count does not need a new formula.

Rules, one worksheet line each, plus the form lines:

| Id | Publishes |
| --- | --- |
| `tax.us.2025.rule.eic-investment-income` | The four-line sum, line 7a floored at 0, compared with $11,950 |
| `tax.us.2025.rule.eic-eligibility` | $0 with the failing test named, or blocked when a rejecting question is no |
| `tax.us.2025.rule.eic-worksheet-a.line-1` | Earned income, the W-2 box 1 total on this class |
| `tax.us.2025.rule.eic-worksheet-a.line-2` | Table credit at line 1 |
| `tax.us.2025.rule.eic-worksheet-a.line-3` | `tax.us.2025.income.agi` |
| `tax.us.2025.rule.eic-worksheet-a.line-5` | Table credit at AGI when AGI is not below the threshold; blank otherwise |
| `tax.us.2025.rule.eic-worksheet-a.line-6` | Line 2, or the smaller of line 2 and line 5 |
| `tax.us.2025.rule.form1040-line27a` v1 | Line 27a from line 6 |
| `tax.us.2025.rule.form1040-lines28-31` v1 | 0 from the new absence fact |
| `tax.us.2025.rule.form1040-lines27-31-total` v2 | Line 27a plus lines 28–31. v1 stays the combined absence |
| `tax.us.2025.rule.form1040-line32` v2 | Reads the v2 total. v1 stays |

Line 4 of Worksheet A is the branch inside line 6, not a separate published amount.

Scope for the contract that follows this file: the first build is slice (a). It does not need a schema successor, a new expression operation, or an engine change. Qualifying children, the tie-breaker, Worksheet B, Form 8862, combat pay, the Medicaid waiver exclusion, and Worksheet 1 stay out. Existing v52 packages and goldens stay on the old absence fact.

Open:

- A person born on January 1, 1961 is inside the EIC parenthetical and is age 65 under the standard-deduction convention. The draft age question follows the parenthetical.
- The v52 lines 27a–31 yes is not copied onto the new lines 28–31 fact. A later prompt could offer it as something to re-answer. This file does not.
- A spouse who died in 2025, for the age test, is Pub. 596 and is outside the slice.
- Line 27c lets a filer decline a credit the tests allow. This slice does not ask that.
- A later child slice can use an entity identity key. Whether a new child entity kind needs any recording work is not settled, and slice (a) does not depend on it.
