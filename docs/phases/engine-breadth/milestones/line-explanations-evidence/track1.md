# Track 1 evidence

Core v78 replaces explain text only. Values, dispositions, rules, and questions are unchanged. v77 and earlier field files are untouched.

31 fields succeeded. 74 texts changed. Five of the 36 stay on the v77 pin because the bound rule cannot select their generic texts: Form 1098 unresolved and Form 1099-K unresolved only block, and the guards on Form 1040 lines 3a and 3b and Schedule D line 8a are `require_closed`, which is true or blocked and never false. That is the same rule as Decision 1's three exclusions.

A closure sentence stays on its v77 bytes when the publication always pins a real answer (a categorical, filing status, or a dependency that always has one). The rule then cannot select closure-backed zero.

## Changed texts

| Field | Disposition | v77 | v78 |
| --- | --- | --- | --- |
| `form1040.line-1a` | published_value | A current derived finding publishes this nonzero amount. | Line 1a is the total of box 1 wages, tips, and other compensation on your Forms W-2. |
| `form1040.line-1a` | computed_zero | A current derived finding publishes a numeric zero. | Line 1a is zero because your Form W-2 box 1 amounts round to zero. |
| `form1040.line-1a` | blocked | No published value exists because required state is absent. | Line 1a has no value yet. It is waiting for a Form W-2 box 1 amount or confirmation that the wage record is complete. |
| `form1040.line-4b` | published_value | published fully taxable IRA distributions on Form 1040 line 4b | Your taxable IRA distributions are the total of box 1 on Forms 1099-R for traditional, SEP, and SIMPLE IRAs that are fully taxable. |
| `form1040.line-6a` | published_value | published Social Security benefits on Form 1040 line 6a | Line 6a is your total Social Security benefits from box 5 of your Forms SSA-1099. |
| `form1040.line-6b` | published_value | published Taxable Social Security benefits on Form 1040 line 6b | Line 6b is the taxable amount of your Social Security benefits from the Social Security Benefits Worksheet. |
| `form1040.line-8` | computed_zero | A current derived finding publishes a computed zero under complete authority. | Your additional income is zero because Schedule 1 line 10 is zero. |
| `form1040.line-9` | published_value | published total income | Your total income: lines 1a, 2b, 3b, 4b, 6b, 7, and 8 added together. |
| `form1040.line-9` | computed_zero | computed zero | Your total income is zero because lines 1a, 2b, 3b, 4b, 6b, 7, and 8 add to zero. |
| `form1040.line-9` | blocked | blocked | Your total income has no value yet. It is waiting for whichever of lines 1a, 2b, 3b, 4b, 6b, 7, and 8 is still open. |
| `form1040.line-10` | computed_zero | A current derived finding publishes a computed zero under complete authority. | Your adjustments to income are zero because Schedule 1 line 26 is zero. |
| `form1040.line-11a` | computed_zero | A current derived finding publishes a computed zero under complete authority. | Your adjusted gross income is zero because your total income equals your adjustments on Schedule 1 line 26. |
| `form1040.line-11b` | computed_zero | A current derived finding publishes a computed zero under complete authority. | Line 11b is zero because line 11a, your adjusted gross income, is zero. |
| `form1040.line-12e` | published_value | published standard-or-itemized deduction | Line 12e is the larger of your standard deduction and your itemized deductions. |
| `form1040.line-12e` | computed_zero | computed zero | Line 12e is zero because neither your standard deduction nor your itemized deductions is above zero. |
| `form1040.line-12e` | blocked | blocked | Line 12e has no value yet. It is waiting for your standard deduction and your itemized deductions. |
| `form1040.line-13a` | computed_zero | computed zero | Your qualified business income deduction is zero because you said you have none. |
| `form1040.line-13a` | blocked | blocked | Your qualified business income deduction has no value yet. It is waiting for whether you have a qualified business income deduction. |
| `form1040.line-13a` | guard_inapplicable | guard false | This line is computed only when you have no qualified business income, qualified REIT dividends, or publicly traded partnership income. You have not answered that question, or you said you have one. |
| `form1040.line-13b` | computed_zero | computed zero | Schedule 1-A line 37 is zero, so line 13b is zero. |
| `form1040.line-13b` | blocked | blocked | Line 13b has no value yet. It is waiting for your Schedule 1-A deduction and for whether you have tips, overtime, or car-loan interest to deduct. |
| `form1040.line-13b` | guard_inapplicable | guard false | This line is computed only when you have no qualified tips, overtime, or new-car-loan interest to deduct. You have not answered that question, or you said you have one. |
| `form1040.line-14` | published_value | published line 14 total | Line 14 adds lines 12e, 13a, and 13b. |
| `form1040.line-14` | computed_zero | computed zero | Line 14 is zero because lines 12e, 13a, and 13b add to zero. |
| `form1040.line-14` | blocked | blocked | Line 14 has no value yet. It is waiting for lines 12e, 13a, and 13b. |
| `form1040.line-15` | published_value | published taxable income | Your taxable income is line 11a minus line 14, and not below zero. |
| `form1040.line-15` | computed_zero | computed zero | Your taxable income is zero because line 11a is not more than line 14. |
| `form1040.line-15` | blocked | blocked | Your taxable income has no value yet. It is waiting for your adjusted gross income and your line 14 deductions. |
| `form1040.line-16` | published_value | published tax | Your tax is the tax on your taxable income when you have no qualified dividends and no preferential capital gain. Otherwise it is the tax from the Qualified Dividends and Capital Gain Tax Worksheet. |
| `form1040.line-16` | computed_zero | computed zero | Your tax is zero because the tax on your taxable income is zero when you have no qualified dividends and no preferential capital gain, or the qualified dividends and capital gain tax is zero. |
| `form1040.line-16` | blocked | blocked | Your tax has no value yet. It is waiting for your taxable income, your filing status, your qualified dividends and capital gain, or your covered sale proceeds. |
| `form1040.line-16` | guard_inapplicable | guard false | Line 16 is computed here only when you sold covered securities, or when Schedule D is not required and your qualified dividends and capital gain fit your capital gain distributions answer. Neither is true on this return. |
| `form1040.line-20` | computed_zero | A current derived finding publishes a computed zero. | Your other nonrefundable credits are zero because Schedule 3 line 8 is zero. |
| `form1040.tax-after-credits` | computed_zero | A current derived finding publishes a computed zero. | Your tax after credits is zero because line 16 is not more than your nonrefundable credits on lines 19 and 20. |
| `form1040.tax-after-credits` | guard_inapplicable | No value is published because a scope, election, threshold, or creditability component is not satisfied for the bounded class. | This line is computed only when you have no Form 4972 tax on line 16 and no additional tax from Schedule 2. You have not answered that question, or you said you have one. |
| `schedule-d.line-1a` | published_value | Current derived finding publishes this line. | Schedule D line 1a, column (h), is short-term proceeds minus basis for the sales you report directly on Schedule D. |
| `schedule-d.line-1a` | computed_zero | Computed zero. | Schedule D line 1a, column (h), is zero because your short-term proceeds equal your basis. |
| `schedule-d.line-1a` | closure_backed_zero | Closure-backed zero. | You said you have no short-term sales reported directly on Schedule D, so line 1a, column (h), is zero. |
| `schedule-d.line-1a` | blocked | Blocked. | Schedule D line 1a, column (h), has no value yet. It is waiting for your short-term proceeds and basis. |
| `schedule-d.line-1b` | published_value | Current derived finding publishes this line. | Schedule D line 1b, column (h), is your short-term gain or loss from Form 8949, proceeds minus basis plus adjustments. |
| `schedule-d.line-1b` | computed_zero | Computed zero. | Schedule D line 1b, column (h), is zero because your Form 8949 short-term proceeds, basis, and adjustments net to zero. |
| `schedule-d.line-1b` | closure_backed_zero | Closure-backed zero. | You said you have no short-term Form 8949 sales, so Schedule D line 1b, column (h), is zero. |
| `schedule-d.line-1b` | blocked | Blocked. | Schedule D line 1b, column (h), has no value yet. It is waiting for your Form 8949 short-term proceeds, basis, and adjustments. |
| `schedule-d.line-6` | published_value | Current derived finding publishes this line. | Schedule D line 6 is your short-term capital loss carryover from last year, as a loss. |
| `schedule-d.line-6` | computed_zero | Computed zero. | Schedule D line 6 is zero because your short-term capital loss carryover is zero. |
| `schedule-d.line-6` | closure_backed_zero | Closure-backed zero. | You said you have no short-term capital loss carryover, so Schedule D line 6 is zero. |
| `schedule-d.line-6` | blocked | Blocked. | Schedule D line 6 has no value yet. It is waiting for your short-term capital loss carryover. |
| `schedule-d.line-7` | published_value | Current derived finding publishes this line. | Schedule D line 7 adds lines 1a, 1b, and 6. |
| `schedule-d.line-7` | computed_zero | Computed zero. | Schedule D line 7 is zero because lines 1a, 1b, and 6 add to zero. |
| `schedule-d.line-7` | closure_backed_zero | Closure-backed zero. | You said you have no short-term capital gain or loss, so Schedule D line 7 is zero. |
| `schedule-d.line-7` | blocked | Blocked. | Schedule D line 7 has no value yet. It is waiting for whichever of lines 1a, 1b, and 6 is still open. |
| `schedule-d.line-8b` | published_value | Current derived finding publishes this line. | Schedule D line 8b, column (h), is your long-term gain or loss from Form 8949, proceeds minus basis plus adjustments. |
| `schedule-d.line-8b` | computed_zero | Computed zero. | Schedule D line 8b, column (h), is zero because your Form 8949 long-term proceeds, basis, and adjustments net to zero. |
| `schedule-d.line-8b` | closure_backed_zero | Closure-backed zero. | You said you have no long-term Form 8949 sales, so Schedule D line 8b, column (h), is zero. |
| `schedule-d.line-8b` | blocked | Blocked. | Schedule D line 8b, column (h), has no value yet. It is waiting for your Form 8949 long-term proceeds, basis, and adjustments. |
| `schedule-d.line-14` | published_value | Current derived finding publishes this line. | Schedule D line 14 is your long-term capital loss carryover from last year, as a loss. |
| `schedule-d.line-14` | computed_zero | Computed zero. | Schedule D line 14 is zero because your long-term capital loss carryover is zero. |
| `schedule-d.line-14` | closure_backed_zero | Closure-backed zero. | You said you have no long-term capital loss carryover, so Schedule D line 14 is zero. |
| `schedule-d.line-14` | blocked | Blocked. | Schedule D line 14 has no value yet. It is waiting for your long-term capital loss carryover. |
| `schedule-d.line-15` | computed_zero | A current derived finding publishes a computed zero from present inputs that net to zero. | Schedule D line 15 is zero because lines 8a, 8b, 13, and 14 add to zero. |
| `schedule-d.line-15` | closure_backed_zero | A current derived finding publishes a zero from closure-backed inputs with no recorded members. | You said you have no long-term capital gain or loss, so Schedule D line 15 is zero. |
| `schedule-d.line-16` | computed_zero | A current derived finding publishes a computed zero from present inputs that net to zero. | Schedule D line 16 is zero because lines 7 and 15 add to zero. |
| `schedule-d.line-16` | blocked | Line 16 is blocked because line 15 is unavailable. | Schedule D line 16 has no value yet. It is waiting for line 7 or line 15. |
| `schedule-d.line-16` | closure_backed_zero | A current derived finding publishes a zero from closure-backed inputs with no recorded members. | You said you have no capital gain or loss, so Schedule D line 16 is zero. |
| `schedule-d.line-21` | published_value | Current derived finding publishes this line. | Schedule D line 21 is the capital loss you can deduct this year, after the yearly limit. |
| `schedule-d.line-21` | computed_zero | Computed zero. | Schedule D line 21 is zero because line 16 is zero or a gain. |
| `schedule-d.line-21` | blocked | Blocked. | Schedule D line 21 has no value yet. It is waiting for your total gain or loss on line 16. |
| `schedule1.line-7` | computed_zero | A current derived finding publishes a computed zero under complete authority. | Your unemployment compensation is zero because your Form 1099-G box 1 amounts round to zero. |
| `schedule1.line-8b` | computed_zero | A current derived finding publishes a computed zero under complete authority. | Your gambling winnings are zero because your Form W-2G box 1 amounts round to zero. |
| `schedule1.line-10` | computed_zero | A current derived finding publishes a computed zero under complete authority. | Schedule 1 line 10 is zero because your unemployment compensation and your Form W-2G gambling winnings add to zero. |
| `schedule3.line-1` | computed_zero | A current derived finding publishes a computed zero. | Your foreign tax credit is zero because the smaller of your Form 1099-DIV foreign tax and your tax rounds to zero. |
| `schedule3.line-1` | guard_inapplicable | No value is published because a scope, election, threshold, or creditability component is not satisfied for the bounded class. | Schedule 3 line 1 shows no value because this return is not one where the foreign tax credit can be claimed without Form 1116. The questions on that page say which condition is not met. |
| `schedule3.line-8` | computed_zero | A current derived finding publishes a computed zero. | Schedule 3 line 8 is zero because your foreign tax credit on line 1 is zero. |
| `schedule3.line-8` | guard_inapplicable | No value is published because a scope, election, threshold, or creditability component is not satisfied for the bounded class. | This line is computed only when you have no other nonrefundable credit on lines 2 through 6. You have not answered that question, or you said you have one. |

## Cases

Every run uses `live_coordinate_run` and the presentation projection. Every section value and disposition on v78 equals v77 on the same acts. v77 still shows its own sentences.

| Case | What it shows |
| --- | --- |
| Wages-only | Line 9 publishes 50000 and says the lines it adds. |
| Closed-empty family | Schedule D line 1a, column (h), is a closure-backed zero and names the empty short-term sales. |
| Schedule D | The same wages return publishes Schedule D with no sale statements. Line 7 is a computed zero and names lines 1a, 1b, and 6. |
| Unanswered input | With the qualified-business-income answer removed, line 13a is blocked and names that answer. |
| Guard that does not apply | With that answer set to no, line 13a is guard-inapplicable. The sentence says the line is computed only when the filer has no qualified business income, and that the filer has not answered or said they have some. |
| Rounded wages | One W-2 box 1 of 0.40. Line 1a is a computed zero and says the amounts round to zero. |
| Rounded unemployment | One Form 1099-G box 1 of 0.40. Schedule 1 line 7 is a computed zero and says the amounts round to zero. |
| Rounded gambling | One Form W-2G box 1 of 0.40. Schedule 1 line 8b is a computed zero and says the amounts round to zero. |
| Open wage record | The W-2 box 1 member and the wage-record closure are removed. Line 1a is blocked and names a box 1 amount or confirmation that the wage record is complete. |
| Open covered proceeds | The covered short-term proceeds closure is removed. Line 16 and Schedule D line 16 are blocked. Line 9 and Schedule D line 7 say they are waiting for whichever listed line is still open. |
| Tips guard | The tips, overtime, and car-loan answer is no. Line 13b is guard-inapplicable and says the line is computed only when the filer has none of those. |
| Line 22 guard | The line 17 answer is no. Line 22 is guard-inapplicable and names Form 4972 and Schedule 2. |
| Schedule 3 line 8 guard | The line 2 credit answer is no. Line 8 is guard-inapplicable and says the line is computed only when the filer claims no other credit on lines 2 through 6. |
| Schedule 3 line 1 guard | Form 1099-DIV foreign tax is 601 and the election is yes. Line 1 is guard-inapplicable. The sentence says this is not a return where the credit can be claimed without Form 1116, and that the questions on that page say which condition is not met. |

## Suite

mypy on `packages/tax/loader.py`, `tests/test_line_explanation_wording.py`, and `tests/test_line_explanations.py`: Success, no issues in 3 source files.

Fast lane (`pytest -m "not live"`): 1651 passed, 8 skipped, 3975 subtests passed in 17.50s.

Full suite (`pytest`): 4316 passed, 24 skipped, 8165 subtests passed in 1300.76s (0:21:40).

These are local runs. The `verify` check on the pull request is the gate of record.

The repair re-ran mypy on the two wording tests: Success, no issues in 2 source files. Fast lane: 1651 passed, 8 skipped, 3975 subtests passed in 17.43s. The case file: 10 passed in 49.09s. The full suite was not re-run.

## Limits

The wording check rejects a v77 generic sentence on any explain the bound rule can select. The banned words, the internal-id check, the two-sentence limit, and the pattern "not say that you have no" apply to replaced explains. Kept specific sentences still contain words such as "derived finding". Decision 2 keeps those bytes.

Schedule 3 line 1's guard does not list every compare in the rule. It says the return is not one where the credit can be claimed without Form 1116, and that the questions on that page say which condition is not met.

The blocked sentence is on the section. The page still hides a blocked line's own text when it shows questions. That page behavior is parked.
