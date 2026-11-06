# Review: P0 and Track 1 of line explanations

Fresh-reader review of `github/main..HEAD` on `milestone/line-explanations-2025`.

Reviewed commit: the Track 1 build plus the review charter (removed at closeout).
Ratified line: `origin/main`. At that commit the branch was 0 behind and 15 ahead. Draft PR #260 is open. No merged PR for this branch. The tree is not spent. Later commits on this branch are this review.

Object: core v78 explain text, the P0 and Track 1 evidence, and the two wording tests. No production, test, or content edit in this review.

Live comparisons used `live_coordinate_run` on core v77 (package v77, registry v75, release v75) and core v78 (package v78, registry v76, release v76). Each case had 73 sections, the same section ids, and 0 value or disposition mismatches. Cases: interest 250 and ordinary dividends 100; a joint return; itemized mortgage interest of 20000; Form 1099-DIV foreign tax of 40 and of 601; the covered short-term proceeds closure removed; one W-2 box 1 of 0.40; one Form W-2G box 1 of 0.40; one Form 1099-G box 1 of 0.40. All of those amounts are synthetic.

## Required

1. **A rounded zero is described as amounts that add to zero.** Form 1040 line 1a, Schedule 1 line 7, and Schedule 1 line 8b. The computed-zero sentences say the box 1 amounts add to zero. Each bound rule rounds to the dollar after the sum. `packages/canon/derivation/round.v1.json` sets that unit to `1`. The three box 1 fact types admit a number with a minimum of 0, so cents are a real input.

   On a return whose only W-2 box 1 is 0.40, line 1a is `computed_zero` with value 0 and the sentence "Line 1a is zero because the box 1 amounts on your Forms W-2 add to zero." The bound rule `rule.wages-line1a` v2 is `round(add(collect box 1))`. The amounts add to 0.40. The zero is the rounding.

   Schedule 1 line 7 and line 8b have the same shape. `rule.f1099g-1-subtotal` v3 and `rule.w2g-b1-subtotal` v3 publish the box 1 sum with cents, and `rule.schedule1-line7` v3 and `rule.schedule1-line8b` v2 round that sum. A return with Form 1099-G box 1 of 0.40, and a return with Form W-2G box 1 of 0.40, each show the matching line as `computed_zero` 0 and the "add to zero" sentence. The W-2G return also blocks Schedule A on the gambling-loss subtotal, which the return with no W-2G does not, so the statement is in the return.

   Replacement for line 1a: "Line 1a is zero because your Form W-2 box 1 amounts round to zero." Use the same shape for the unemployment and gambling lines, naming the form and box.

2. **Line 1a, blocked, names an input the filer cannot supply.** The sentence is "Line 1a has no value yet. It is waiting for a Form W-2 box 1 amount, confirmation that the wage record is complete, or the dollar-rounding rule." `rule.wages-line1a` v2 lists `rounding.convention` as its missing input. That convention is an engine parameter. The cents return above did not block, so this sentence is the one the field shows whenever the line does block.

   Replacement: "Line 1a has no value yet. It is waiting for a Form W-2 box 1 amount or confirmation that the wage record is complete."

3. **Form 1040 line 16, blocked, names filing status and omits the open input.** The sentence is "Your tax has no value yet. It is waiting for your taxable income, your filing status, and your qualified dividends and capital gain." On the return with the covered short-term proceeds closure removed, the line is blocked. The rule `form1040-line16` reports missing taxable income, the preferential base, the covered short-term proceeds subtotal, and worksheet lines 24 and 25. Filing status is not missing. Covered sale proceeds are missing, and the sentence does not name them. `rule.form1040-line16` v6 also lists those proceeds subtotals in `blocked.missing`.

   Replacement: "Your tax has no value yet. It is waiting for your taxable income, your filing status, your qualified dividends and capital gain, or your covered sale proceeds."

4. **Schedule D line 16, blocked, names the wrong line.** The successor kept the previous sentence "Line 16 is blocked because line 15 is unavailable." On the same proceeds return, line 15 is `computed_zero` 0 and `rule.schedule-d-line16` reports missing line 7 only. Line 7 is the blocked one. The rule's own `blocked.missing` is line 7 and line 15.

   Replacement: "Schedule D line 16 has no value yet. It is waiting for line 7 or line 15."

5. **Line 13a, guard, answers a different question than the one the filer was asked.** The sentence is "Line 13a shows no value because you did not say that you have no qualified business income deduction." `rule.form1040-line13a` publishes 0 only when `no-qbi-deduction-declared` is `yes`. The question asks whether the filer had qualified business income, qualified REIT dividends, or publicly traded partnership income. That fact is an absence fact: the question's yes records `no`, and its no records `yes`. The recorded `no` is the guard. The scope-answer probe shows that recorded `no` leaves line 13a not computed. The sentence does not say that the filer said they had that income. The computed-zero sentence "you said you have none" matches the recorded `yes`, which is the question's no, and the base returns showed that sentence.

   Replacement: "Line 13a shows no value because you said you had qualified business income, qualified REIT dividends, or publicly traded partnership income."

6. **Line 13b, guard, has the same inversion.** The sentence is "Line 13b shows no value because you did not say that you have no tips, overtime, or car-loan interest deduction." `rule.form1040-line13b` v2 publishes Schedule 1-A line 37 only when `no-parts-ii-iv-deductions-declared` is `yes`. Its note says a recorded `no` means the return does have a Parts II through IV deduction and the rule is inapplicable. The question asks whether the filer received qualified tips or overtime, or paid interest on a new personal vehicle. Question yes records `no`. The probe shows that recorded `no` leaves line 13b not computed. The base returns showed the computed-zero sentence, which is true when line 37 is the value and it is zero.

   Replacement: "Line 13b shows no value because you said you received tips or overtime, or paid interest on a new car loan, that could be deducted."

7. **Line 22, guard, drops Form 4972 and keeps the double negative.** The sentence is "Line 22 shows no value because you did not say that line 17 has no additional tax from Schedule 2." `rule.form1040-tax-after-credits` v2 applies only when `no-line17-schedule2-additional` is `yes`. The question the filer answers also asks whether line 16 includes Form 4972 tax. The probe shows a recorded `no` on the line 17 fact leaves line 22 not computed. The sentence does not mention Form 4972.

   Replacement: "Line 22 shows no value because you said line 16 includes Form 4972 tax or line 17 has additional tax from Schedule 2."

8. **Schedule 3 line 8, guard, uses the same inverted double negative.** The sentence is "Schedule 3 line 8 shows no value because you did not say that you have no credit on line 2, line 3, line 4, line 5, or line 6." `rule.schedule3-line8` applies only when all five absence facts are `yes`. Those five facts share one question: whether the filer claims any other nonrefundable credit on lines 2 through 6. The probe shows a recorded `no` on any one of them leaves line 8 not computed.

   Replacement: "Schedule 3 line 8 shows no value because you said you claim another nonrefundable credit on lines 2 through 6."

9. **Schedule 3 line 1, guard, states reasons that are false on the return that shows it.** With Form 1099-DIV foreign tax of 601, the election set to yes, and line 16 at 3887, the line is `guard_inapplicable`. The sentence says the foreign tax is not zero and the credit does not apply, which matches this return, and then says "The tax is not above zero, you did not elect the credit, it is over 600 dollars when you file jointly or 300 dollars otherwise, or you did not say yes to every condition..." On this return the election is yes and both the foreign tax and the income tax are above zero. The condition that fails is the 300 dollar cap. The sibling return with foreign tax of 40 publishes line 1 as 40, so the election and the credit path do apply when the amount is under the cap.

   A two-sentence list cannot also name every compare in that guard. The repair should not pretend to. Replacement: "Schedule 3 line 1 shows no value because your Form 1099-DIV foreign tax is not zero and a condition for this credit is not met."

## Recommended

1. **Form 1040 line 16, guard, is not two short sentences.** The second sentence is "Schedule D is required, or your qualified dividends or preferential capital gain is below zero, or those amounts are not both zero and do not fit your capital gain distributions answer." The first sentence, "you have no covered sale proceeds above zero," is the condition that begins the guard. The proceeds return blocked the line instead of taking this guard, so this text was not shown in these cases. It is the sentence the field uses when the guard does select. Replacement for the second sentence: "Schedule D is required, or your qualified dividends or capital gain is below zero, or your capital gain distributions answer does not match those amounts."

2. **Form 1040 line 9, blocked, names lines that are already filled in.** On the proceeds return, line 1a is 50000 and line 9 is blocked with "It is waiting for lines 1a, 2b, 3b, 4b, 6b, 7, and 8." Line 7 is the open one. The same return's Schedule D line 7 says it is waiting for lines 1a, 1b, and 6 while line 6 is already a computed zero. Both sentences name the whole sum. Replacement for line 9: "Your total income has no value yet. It is waiting for whichever of lines 1a, 2b, 3b, 4b, 6b, 7, and 8 is still open." Use the same shape for Schedule D line 7.

3. **The wording test would accept every required finding above.** `tests/test_line_explanation_wording.py` rejects a replaced sentence that contains a banned word, an internal id, or one of the 37 generic sentences. It does not count sentences, and it does not check that a sentence is true. "Add to zero" after a round, and the inverted guard sentences, contain none of the banned words. A regression of those sentences would still pass the test. The test does enforce the 37 generic sentences and the five fields that stay on the previous version. Those two checks hold: this review counted 73 changed explain texts across the 31 successors, and the five stayed pins are unchanged.

## Notes

The five fields that stayed on the previous pin still have generic text, and that text is not a disposition the bound rule can select. The Form 1098 unresolved field and the Form 1099-K unresolved field publish through a default path whose `when` is false and whose value is false, so the "does not publish a value" and "Not used." sentences are not a numeric result. Their blocked and guard sentences are specific. Lines 3a and 3b and Schedule D line 8a use `require_closed` as the guard. `require_closed` returns true or blocks. It does not return false, so the generic guard sentences on those three fields do not show. Their other sentences stay as they were, including "derived finding," which Decision 2 keeps.

On the complete returns, Schedule D lines 7, 15, and 16 were `computed_zero`, so the closure sentences on those lines were not the ones shown. Line 9's closure sentence and its guard sentence were not shown either. Line 11a and line 11b carried the same value on every complete return. Schedule D line 21 was `computed_zero` with "line 16 is zero or a gain" where line 16 was zero.

The interest return published line 9 as 50350, which is the wages, the 250 of interest, and the 100 of dividends. The joint return used the joint standard deduction, 31500. The itemized return published line 12e as 20000. Foreign tax of 40 published Schedule 3 line 1 as 40.

For the Schedule 3 line 8 and line 22 guards, the scope-answer table marks a question yes on those absence groups as not determined. The sentence is what the field shows when the recorded fact is `no`. The probe reached that state. A question yes on the group is outside the supported recording.

The Form W-2G return of 0.40 also blocked Schedule A because the gambling-loss subtotal was absent. That return is not a finished return. Line 8b still resolved, and its sentence is the one in required finding 1.

On the foreign-tax return of 601, Schedule 3 line 8 is blocked while line 1 is `guard_inapplicable`. The blocked sentence, kept from the previous field, says line 1 is blocked or another Part I absence is incomplete. This review did not record which dependency line 8 named, so that sentence is not a finding.

`packages/tax/loader.py` maps core v78 to the same companion declaration object as core v77. That is the source. This review did not execute the loader.

The builder's suite counts are a local report. The `verify` check on PR #260 is the gate. This review did not re-run the suite. The page behavior parked in the plan, hiding a blocked sentence when a question exists, is outside this charter.

No personal return, no absolute path, and no real identifier is in this record. The live cases used synthetic demo amounts.

## Checks

1. True sentences. The nine required findings are sentences v78 shows that are false or misleading on a return that selects them. Required finding 4 kept a previous sentence; the successor still shows it. The published sentences exercised here matched the values: line 9 on the interest return, line 12e on the itemized return, Schedule 3 line 1 at 40, and the computed-zero sentences for lines 13a and 13b on the base returns. Line 9's computed zero on the 0.40 wage return is about the already rounded lines, so that sentence is not in the rounding finding.

2. The wording standard. The changed sentences do not contain the banned words or an internal id. The failures are the double negatives in required findings 5 through 8, the false clauses and the length of the Schedule 3 line 1 guard, and the Form 1040 line 16 guard in the recommended list. A single pair of parentheses for a column, such as column (h), is not nested.

3. Generic text still selectable on v78. The five stayed fields are the ones named in the wording test, and their pins match v77. The generic sentences on those fields are not selectable, for the reasons in the notes. No other generic from the v77 stock was selected on the nine live returns. Several kept specific sentences still say "derived finding." That is the Decision 2 keep.

4. Values and dispositions unchanged, and publication is add-only. All nine cases matched v77 on every section's disposition and value. Package v77 and package v78 each have 851 members. The 31 members that differ are form-field version swaps, and each successor differs only in version and explain text. There are 73 such text changes. The only other package fields that differ are `version`, `package_checksum`, and six entrypoints that retarget a succeeded field. Registry v76 has 1234 citizens against 1203 in v75: 31 added, none removed, and no shared citizen changed. Both release files record the sha256 of their registry file. The only modified path from `github/main` to the reviewed commit is `packages/tax/loader.py`. No schema file is in that diff.

5. The account and the wording test. The plan's counts of 31 fields and 73 texts match the packages. The wording test's generic count and its five stayed pins are real checks, and they would not catch the required findings. See the recommended list.
