# P0: how many rounds of questions a return takes, and why

Builder unit on `milestone/all-questions-at-once-2025`. Core v75. Evidence only.
No production, test, content, or schema edit.

## Scope

A filer who answers every question a blocked return shows should not then be shown a new question the engine could already have asked. This unit measures, on core v75 through `live_coordinate_run`, how many answer rounds six starting returns take, and for every question first shown after round one, which rule hid it, by which mechanism, and whether it was knowable without an earlier answer. The smallest change that would show the knowable questions in round one is designed and counted on a scratch prototype. A question that truly depends on an earlier answer stays conditional.

Understood non-goals: no change to a computed amount once its inputs are present; no new question wording; no recording-surface or entry-loop change; no edit to a published schema, an adopted package, or an adopted rule version.

## Evidence ceiling

`live_coordinate_run` on `package.core-calculations.v75.json`, release `demo.release.sli-worksheet-integration.2025.v73.json`, and registry `published-packages.v73.json`. Question sentences are the presentation reasons on blocked lines. The answer key for each return is a complete synthetic `demo.*` persona already used by the current-core helpers. The prototype, when run, patches the in-process runner only and writes `prototype-output.json`. It does not edit package content.

## Stop conditions

Stop without a content or engine edit if the change needs a schema, an expression operation, a runner change, an evaluator change, or a projection change. Report that and do not implement it. No production, test, content, or schema edits in this unit.

## Method

`probe.py` reads core v75. An input question maps its sentence to a fact type, and through the package input bindings to the symbol the rules read. A closure mapping maps its sentence to a family id. Numeric input questions are amount answers. Every other input question is a scope answer, including filing status and the Form 1098 boolean.

The answer key for each return is a complete synthetic persona. Answering a shown sentence copies the persona acts that record that sentence and no others. Scope and amount sentences restore those facts. A closure sentence restores that family's closure attestation. Statement members are not questions, so they are not removed and not treated as answers.

The six starts:

| Start | Persona | What is withheld |
| --- | --- | --- |
| scope-withheld | publishing W-2 base | every categorical input question |
| amounts-open | publishing W-2 base | every numeric input question, and every source-closure attestation |
| mortgage-empty | base plus one Form 1098, box 1 interest 8400 | every input question and every closure; the statement and its companions stay |
| form-1099b-empty | base, with the "only box 2a" answer set to no, plus one covered short-term sale (proceeds 1000, basis 800) | every input question and every closure; the sale stays |
| dependent-empty | three qualifying children, W-2 boxes 4 and 6 | every input question and every closure; the children stay |
| foreign-tax-empty | base plus Form 1099-DIV box 7 of 30, direct credit elected | every input question and every closure; the statement stays |

Each round is `live_coordinate_run`. The probe collects the reason sentences on every blocked form line, answers exactly those sentences, and runs again. It stops when a round shows no filer question, when a round shows no sentence that was not already shown, when a shown sentence has no persona act, or at eight rounds. The persona itself is run once so a finished loop can be compared on scalar published amounts.

A question first shown after round one is classified from the rule that names it. The class is knowable when the rule demands it without depending on the value of an earlier answer, and conditional when it sits only where an earlier answer selects the branch. The contexts recorded with each question are the classifier's evidence. The note corrects a label when those contexts disagree with it.

## 1. Rounds

A round is one that showed at least one question sentence. The run that follows, with no new sentence, is the stop. `probe-output.json` holds every sentence. No round had a generic blocked line (a blocked line whose reasons were empty).

| Start | Rounds | Stop | Last run |
| --- | --- | --- | --- |
| scope-withheld | 2 | no filer question | round 3, 0 blocked rules |
| amounts-open | 4 | no filer question | round 5, 4 blocked rules, 0 question lines |
| mortgage-empty | 4 | no filer question | round 5, 4 blocked rules, 0 question lines |
| form-1099b-empty | 4 | no filer question | round 5, 4 blocked rules, 0 question lines |
| dependent-empty | 6 | no filer question | round 7, 4 blocked rules, 0 question lines |
| foreign-tax-empty | 6 | nothing new | round 6 still shows one question |

What each round asked:

- **scope-withheld.** Round 1 showed 25 sentences (49 question lines, 142 blocked rules) and restored 57 persona acts. Round 2 showed one new sentence, the Form 1098 question (19 lines, 55 rules). Round 3 was clear.
- **amounts-open.** Round 1 showed 35 sentences, all closures and the one withheld amount the open families ask up front (57 lines, 184 rules). Round 2 showed 9 sentences: the covered short-term and long-term sale closures, the six wash-sale basis, proceeds and adjustment closures, and the wage closure. Round 3 showed the Form W-2 box 2 withholding amount. Round 4 showed the overpayment to apply to next year. Round 5 had no question.
- **mortgage-empty.** Round 1 showed 61 sentences (69 lines, 217 rules). Rounds 2 through 5 match amounts-open, including the same 9, then box 2, then the overpayment. The Form 1098 question did not appear: the mortgage statement is already on the return.
- **form-1099b-empty.** Round 1 showed 60 sentences (68 lines, 215 rules). Round 2 showed the same 9 plus the Form 1098 question. Rounds 3 and 4 are box 2, then the overpayment.
- **dependent-empty.** Round 1 showed 60 sentences. Round 2 showed the 9, the Form 1098 question, and the Social Security number question for the child tax credit. Round 3 showed the W-2 box 2 amount, the qualifying-child-of-another question, and the nonresident-alien question. Round 4 showed the Form W-2 box 4 closure. Round 5 showed the box 6 closure. Round 6 showed the overpayment.
- **foreign-tax-empty.** Round 1 showed 59 sentences. Round 2 showed the same 9, the Form 1098 question, and the Form 1099-DIV box 4 withholding amount. One of those 11 sentences had no persona act. Round 3 showed the W-2 box 2 amount and the Form 1099-DIV box 7 closure. Round 4 showed nine foreign-tax-credit questions, and the box 4 amount was still on the return. Round 5 showed the $300 / Form 1116 question, with box 4 still shown. Round 6 showed only the box 4 amount, which had already been shown, so the loop stopped. The persona itself, run complete, has 7 blocked rules and 6 question lines on this return.

Published headlines match the persona on every start.

| Start | AGI | Taxable income | Notable lines |
| --- | --- | --- | --- |
| scope-withheld, amounts-open, mortgage-empty | 50000 | 34250 | withholding 4500, refund 625, Schedule D 0, foreign tax credit 0 |
| form-1099b-empty | 50200 | 34450 | Schedule D line 1a and line 7 are 200, refund 601 |
| dependent-empty | 15000 | 0 | Schedule 8812 line 21 is 500, payments line 33 and the refund are 8636 |
| foreign-tax-empty | 50100 | 34350 | foreign tax credit 30. Withholding and the refund are unpublished on both the loop and the persona, because the return stays blocked |

scope-withheld matches the persona on every scalar publication. The other five starts match these headlines and differ on four symbols: `interest.b8-tax-exempt-subtotal`, `interest.scheduleb-nominee-subtotal`, `odc.child-count`, and `odc.relative-count`. The questions that would close those families never appeared, and the confirming run still has four blocked rules. Section 5 names that limit. The probe did not store those four artifact ids.

## 2. Questions first shown after round one

The same questions recur across the starts. Each row is the rule that first records the question, the mechanism in that rule, and whether the question was knowable in round one. Knowable means the return would ask it whatever the earlier answers were: the statements already on the return determine it, and the delay is only that the rule recorded a different cause first. Conditional means an earlier answer selects the branch, and the question stays on that branch.

The classifier's raw label is in `probe-output.json`. Two of those labels are corrected here. The wage closure was marked unknown because the family id occurs as a `count` source set, which the classifier did not name. The Form W-2 box 4 and box 6 closures were marked knowable; they are asked only after the additional child tax credit path is selected.

### Knowable

| Question | First shown | Rule | Mechanism |
| --- | --- | --- | --- |
| Have you recorded every covered short-term sale (basis reported, held a year or less)? | round 2 on every start except scope-withheld | `rule.schedule-d-line1a-gain` v2 | guard |
| The same question for a covered long-term sale | round 2, same starts | `rule.schedule-d-line8a-gain` v3 | guard |
| Have you recorded the basis, the proceeds, and the wash-sale adjustment of every covered short-term wash sale, and the same three for long-term (six questions) | round 2, same starts | the six `rule.f1099b-covered-w-*-subtotal` v3 rules | guard |
| Have you recorded every wage amount in box 1 of every Form W-2? | round 2, same starts | `rule.form1040-line25a` v1 | guard |
| Enter the federal income tax withheld in box 2 of each Form W-2. If box 2 is blank, enter $0. | round 3, or round 2 on the dependent and foreign starts where round 3 is shared with other questions | `rule.form1040-line25a` v1 | raised ref |
| Enter the federal income tax withheld in box 4 of each Form 1099-DIV. If box 4 is blank, enter $0. | round 2 on foreign-tax-empty, and still shown through round 6 | `rule.form1040-line25b` v4 | raised ref |
| Have you recorded every foreign tax paid amount in box 7 of every Form 1099-DIV? | round 3 on foreign-tax-empty. On amounts-open, where the scope answers are already present, this closure is in round 1 | `rule.schedule3-line1-direct-ftc` v4 | static requires checked before the guard |

Why each one waits:

- **Schedule D lines 1a and 8a.** `requires` names the proceeds and basis subtotals, so the runner records those and does not evaluate `when`. `when` is `all` of three `require_closed` calls, and the parent sale family is the first. The basis and proceeds closures are asked in round 1 by their own subtotal rules. The parent family is asked only after those subtotals exist. The parent family does not depend on an answer.
- **Wash-sale basis, proceeds, and adjustment.** Each subtotal's `when` is a single `require_closed` of that companion family. The rule also accounts for the parent wash-sale family, and the run records that family's member-validation symbol first. The parent wash-sale closure is in round 1. The companion closures are the next cause. They do not depend on an answer.
- **Wage closure.** Line 25a `when` is `any` of a `compare` of two `count`s (box 2, then wages) and a `ref` of the box 2 amount. `count` raises on the first unclosed family, so box 2's closure is round 1 and the wage closure is round 2. A `collect` of wages, on the wages line, does not ask this: `collect` sums members that are already present and raises only when the set is empty. The wage statement is already on these returns. The closure does not depend on an answer.
- **W-2 box 2 amount.** The same `any` reaches the `ref` only when the count comparison is false. With a W-2 on the return and no box 2 amount, the comparison is false once both families are confirmed, so the amount is asked next. It is knowable from the statement already on the return. Showing it in the same round as the closures means recording that `ref` while the earlier `count` is blocked. Section 3 says why that part is an evaluator change.
- **Form 1099-DIV box 4 amount.** Line 25b `when` is `all` of five `require_closed` calls and, for each form, `any` of a count comparison and a `ref` of the withholding amount. The box 4 closure is asked first. The amount is the later `ref`, same shape as W-2 box 2. The foreign-tax persona never records this amount, so answering the shown sentences cannot clear it. The complete persona stays blocked on the same question.
- **Form 1099-DIV box 7 closure, on the empty foreign return.** The credit rule `requires` the box 7 subtotal, filing status, and the tax total before it evaluates `when`, which begins with `require_closed` of the box 7 family. While filing status is unanswered, that line's recorded causes are not all filer questions, and the projection shows none of them. Once filing status is answered and the tax total exists, the closure is the cause that remains. The Form 1099-DIV is already on the return, so the closure does not depend on which way filing status was answered.

### Conditional, and left as they are

| Question | First shown | Rule | Mechanism |
| --- | --- | --- | --- |
| Did you receive a Form 1098 mortgage interest statement for 2025? | round 2 on scope-withheld, form-1099b-empty, dependent-empty, foreign-tax-empty | `rule.form1040-line12e` v4 | choose branch |
| Enter how much of your 2025 overpayment you want applied to your 2026 estimated tax. | the last question round on every start except scope-withheld and foreign-tax-empty | `rule.form1040-line36` v1 | choose branch |
| Does your Social Security number allow you to work in the United States? | round 2 on dependent-empty | `rule.ctc-filer-ssn-gate` v1 | choose branch |
| Could you be a qualifying child of another person for 2025? | round 3 on dependent-empty | `rule.eic-answer.not-qualifying-child-of-another` v2 | choose branch |
| Were you, or was your spouse, a nonresident alien for any part of 2025? | round 3 on dependent-empty | `rule.ctc-filer-gate` v1 | choose branch |
| Have you recorded every Social Security tax withheld amount in box 4 of every Form W-2? | round 4 on dependent-empty | `rule.w2-box4-total` v2 | choose branch |
| Have you recorded every Medicare tax withheld amount in box 6 of every Form W-2? | round 5 on dependent-empty | `rule.w2-box6-total` v2 | raised ref |
| Nine foreign-tax-credit questions (the election, the 16-day holding period, passive income, other foreign income, the credit-or-deduction choice, carryback, and the Schedule 2 gates) | round 4 on foreign-tax-empty | `rule.schedule3-line1-direct-ftc` v4 | guard |
| Is your total foreign tax more than $300 ($600 if joint), or must you file Form 1116? | round 5 on foreign-tax-empty | `rule.schedule3-line1-direct-ftc` v4 | guard |

What a truly conditional question looks like to the filer: it appears only after an earlier answer has opened a part of the return. The mortgage question is inside the `choose` on line 12e, read once the standard deduction is known and only on the branch that still needs the statement. The overpayment question is inside the `choose` on line 36, and the applied-amount `ref` sits in a `conditional_dependency_set` whose condition is that line 34 is an overpayment. The child-credit and earned-income questions are `choose` branches after the child count and the filer gates. Box 4 and box 6 are asked only when Schedule 8812 line 21 takes the branch `part-ii-b-needed` equals 1; line 21 then `ref`s the box 4 total before the box 6 total, so box 6 is one round later even after that branch is open. The foreign-tax worksheet questions are the members of a `conditional_dependency_set` whose condition is that the box 7 subtotal is positive, so they are asked only once that credit is in play. A filer who answered the other way is not asked. Those questions stay.

## 3. Design

Two changes, and only the first is content.

**Content successors for the unconditional closures.** The runner already records every missing `requires` entry, and it does so before it evaluates `when`, including for a rule that becomes eligible only at the end of the run. What it does not record is a `require_closed` or a sibling `count` that sits in the guard. The successor shape is one closure-check rule per family, whose `when` is that single `require_closed` and which publishes a symbol, and a successor of the consumer that lists every such symbol in `requires`. The families this covers are the parent covered-sale families on Schedule D lines 1a and 8a, the six wash-sale companion families, and the wage family on line 25a. Each of those questions was asked on the next round only because a different cause was recorded first. None of them depends on the value of an earlier answer.

**The withholding amount stays one round later unless the evaluator keeps a later ref.** Line 25a asks for Form W-2 box 2, and line 25b asks for Form 1099-DIV box 4, from a `ref` in the second arm of `any`. The first arm compares two `count`s and raises on the first unclosed family, so the `ref` is never named in that pass. On these returns the comparison is false once the families are confirmed, because the statement is already present and the amount is not, so the amount is knowable. A static `requires` entry would ask it of a return that has no such statement. Recording the `ref` while the `count` is blocked, and only when one of the compared sets already has a member, is evaluator behavior. The same gap keeps the Form 1099-DIV box 4 amount one round later when line 25b is still blocked on its subtotal `requires` and the `when` has not run.

The conditional questions in section 2 stay where they are. A successor does not pull a `choose` branch or a `conditional_dependency_set` forward.

This unit stops before that evaluator change. No schema, expression operation, runner, evaluator, or projection edit is in this commit.

## 4. Prototype counts

`prototype.py` patches the in-process runner and writes `prototype-output.json`. It does not edit package content. The closures layer records the unconditional families. The full layer also records the later withholding `ref` when the expression actually runs and a compared set has a member. Complete personas were run with the patch off and on. Scalar publications were identical for the base, mortgage, Form 1099-B, dependent, and foreign-tax personas: no symbol differed.

Question rounds are runs that showed a sentence. Before is section 1. After is the full patch.

| Start | Before | After, full patch | What the later rounds still ask |
| --- | --- | --- | --- |
| scope-withheld | 2 | 2 | the Form 1098 question, then clear |
| amounts-open | 4 | 2 | the overpayment amount, then four blocked rules and no question |
| mortgage-empty | 4 | 2 | the overpayment amount, then the same four rules |
| form-1099b-empty | 4 | 3 | the Form 1098 question, then the overpayment |
| dependent-empty | 6 | 5 | the credit and Form 1098 questions, then box 4, then box 6, then the overpayment |
| foreign-tax-empty | 6 | 6 | the Form 1098 question and the Form 1099-DIV box 4 amount, then the box 7 closure, then the credit worksheet, and the box 4 amount stays |

Headlines after the patch match section 1 on every start, including Schedule D line 1a of 200 on the Form 1099-B return, Schedule 8812 line 21 of 500 on the dependent return, and the foreign tax credit of 30.

A closures-only run of amounts-open, with the later-ref layer off, took 3 question rounds. Round 1 held the 44 sentences that include every closure section 2 marks knowable, including the wage closure and both Schedule D parent families. Round 2 was the Form W-2 box 2 amount. Round 3 was the overpayment. The full patch is what moves that box 2 amount into round 1.

## 5. Limitations

The confirming run of every start except scope-withheld still has four blocked rules, and the same four published symbols differ from the persona: `interest.b8-tax-exempt-subtotal`, `interest.scheduleb-nominee-subtotal`, `odc.child-count`, and `odc.relative-count`. The rules are `rule.f1099int-b8-subtotal`, `rule.scheduleb-adjustment.nominee-subtotal`, `rule.odc-child-count`, and `rule.odc-relative-count`, each blocked `SOURCE_SET_UNCLOSED` on its family. Those closure questions never appeared on a blocked line, so the loop could not confirm the families. The persona confirms them and publishes the symbols. The headlines in section 1 still match.

The foreign-tax persona does not record Form 1099-DIV box 4 withholding. The question is shown from round 2 and never cleared. The complete persona itself has 7 blocked rules and 6 question lines, and it publishes the same headlines the loop does, with withholding and the refund unpublished.

The Form 1099-DIV box 7 closure on the empty foreign return is still round 3. The credit rule's other requires include the tax total, and the line shows the closure once those requires exist. The scratch patch adds no form line, so it did not give that closure a line of its own in round 1.

The closures-only count is amounts-open only. The other five starts were counted with the full patch.

No production, test, content, or schema file was edited.
