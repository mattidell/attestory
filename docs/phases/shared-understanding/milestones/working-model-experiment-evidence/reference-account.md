# Reference account: joint return, both spouses with Form 1098-E interest

Prepared by the grounding agent for the facilitator. It records what the law requires and
what the application does today, with sources, so a planner's statement can be checked
against the evidence that was available. It is not an answer key and proposes no mechanism.

**Source tags.** [IRC] 26 U.S.C. § 221, Cornell LII text (amendment notes end at Pub. L.
117-2). [Reg] 26 CFR § 1.221-1, eCFR current. [Pub970] IRS Publication 970 (2025), chapter
4, irs.gov HTML. [i1040] 2025 Instructions for Form 1040, Schedule 1 line 21 and its
worksheet, irs.gov HTML. [i1098] Instructions for Forms 1098-E and 1098-T, **2026** revision
(the 2025 revision was not fetched). [R6050S] 26 CFR § 1.6050S-3. [repo] a committed file in
this repository. [probe] a scratch run by the grounding agent, not committed and not
available to a planner. **V** = verified by reading the source or running it. **I** =
inferred by the grounding agent.

## Part A — the law (tax year 2025)

**A1. The $2,500 limit is per return.**
- Text: "the deduction allowed by subsection (a) for the taxable year shall not exceed
  $2,500" [IRC (b)(1)]; "may not exceed $2,500" [Reg (c)]. Unlike the phase-out, the statute
  gives no larger figure "in the case of a joint return". The worksheet's line 1 is "the
  total interest you paid in 2025 on qualified student loans … Don't enter more than $2,500"
  [i1040; Pub970 Worksheet 4-1].
- Joint return, both spouses with loans: the interest of both spouses is added and the total
  is capped once at $2,500. The cap does not become $5,000. (V for the wording. I for "per
  return", which follows from the joint return being one return with one worksheet. I did
  not fetch § 6013.)
- Confidence: high.

**A2. The phase-out reads one joint MAGI.**
- Text: the reduction ratio uses "the taxpayer's modified adjusted gross income … over
  $50,000 ($100,000 in the case of a joint return)" to "$15,000 ($30,000 in the case of a
  joint return)" [IRC (b)(2)(B)]. The two threshold amounts are indexed for inflation after
  2001 and rounded down to a multiple of $5,000 [IRC (f)]. The range amounts are not
  indexed. The regulation repeats the unindexed $50,000–$65,000 ($100,000–$130,000 joint)
  figures [Reg (d)(1), (d)(3)].
- 2025 amounts: married filing jointly, the phase-out starts at $170,000, has a $30,000
  range and ends at $200,000. Other statuses: $85,000, $15,000 and $100,000 [i1040 worksheet
  lines 5 and 7; Pub970 Table 4-2]. Worksheet MAGI is Form 1040 line 9 minus Schedule 1
  lines 11–20, 23 and 25 [i1040 lines 2–4]. Pub970 adds back the foreign and possession
  exclusions. When those apply, i1040 sends the filer to Pub970 instead of its own
  worksheet.
- Joint return: one MAGI figure, from the joint return's AGI, read against the joint
  amounts. (V)
- Discrepancy: Pub970 prints "$170,00" twice, a typo; its tables and worksheet say $170,000.
  I did not fetch Rev. Proc. 2024-40.
- Confidence: high.

**A3. The dependency bar: whose status matters.**
- Text: "No deduction shall be allowed by this section to an individual for the taxable year
  if a deduction under section 151 with respect to such individual is allowed to another
  taxpayer" [IRC (c)]. Reg (b)(2)(i) says the same: "is a dependent … for whom another
  taxpayer is allowed a deduction under section 151".
- The publications go beyond the text, and differ from each other in wording. i1040 makes it
  a condition that "You, or your spouse if filing jointly, aren't claimed as a dependent on
  someone else's … 2025 tax return". Pub970 says "No one else is claiming you as a
  dependent" and defines claiming as listing the person on page 1 of a return. The statute's
  word is "allowed". The publications use "claimed".
- Joint return: i1040 tests both spouses, and either one being claimed defeats the return's
  deduction. The statute bars "an individual". It does not say whether one spouse's bar
  removes interest the other spouse paid on a joint return. (V for the texts. The reach on a
  joint return is unresolved in the text.)
- Practical narrowing (I, not verified): a person who files a joint return generally cannot
  be anyone's dependent under § 152(b)(2), except for a refund-only return. A repo document
  mentions the same exception
  (`…/student-loan-interest-deduction-translation-evidence/p1-obligation-and-amounts.md:366`).
  So the case is rare, but it is not impossible.
- Confidence: medium.

**A4. Legal obligation and who paid.**
- Text: "A taxpayer is entitled to a deduction under section 221 only if the taxpayer has a
  legal obligation to make interest payments under the terms of the qualified education
  loan" [Reg (b)(1)]. Third-party payment: "If a third party who is not legally obligated …
  makes a payment of interest on behalf of a taxpayer who is legally obligated …, then the
  taxpayer is treated as receiving the payment … and, in turn, paying the interest" [Reg
  (b)(4)(i)]. Reg Example 2 under (b)(2): a parent who is not obligated cannot deduct.
  Pub970: "You can't claim … [i]nterest you paid on a loan if … you aren't legally
  obligated".
- Joint return: obligation is tested loan by loan. It is satisfied if a spouse on the return
  is obligated on that loan. Interest that spouse A pays on a loan only spouse B owes is
  treated as B's payment under (b)(4), so it is deductible on the joint return (I,
  medium-high). A parent or other third party paying an obligated spouse's loan is treated
  the same way (V, from (b)(4) and Pub970 "Interest paid by others"). A loan neither spouse
  is obligated on, such as a parent's own Parent PLUS loan for a child, gives the couple
  nothing (I).
- The statute itself has no obligation test. The obligation test is in the regulation and
  Pub970.

**A5. Qualified education loan: whose expenses, and when that is tested.**
- Text: "indebtedness incurred by the taxpayer solely to pay qualified higher education
  expenses — (A) which are incurred on behalf of the taxpayer, the taxpayer's spouse, or any
  dependent of the taxpayer as of the time the indebtedness was incurred" [IRC (d)(1)(A)].
  The regulation reads: "on behalf of a student who is the taxpayer, the taxpayer's spouse,
  or a dependent … of the taxpayer at the time the taxpayer incurs the indebtedness" [Reg
  (e)(3)(i)(A)]. Pub970 reads: "For you, your spouse, or a person who was your dependent …
  when you took out the loan". i1040 reads: "Yourself or your spouse. Any person who was
  your dependent when the loan was taken out."
- A loan taken out before marriage, for one's own education: the expenses were for "the
  taxpayer", so the later marriage does not matter (V, high).
- A loan taken out before marriage, for the person later married: this is **unresolved in
  the text**. The statute and regulation can be read to test every relationship at the time
  the debt was incurred. On that reading, a fiancé was not then a spouse, and was a
  dependent only if the § 152 tests were met, so the loan does not qualify. The publications
  attach the time only to "dependent", which suggests the spouse relationship might be read
  at present. This is a real divergence of wording. I found no example that settles it. A
  variation (I): if the future spouse was a co-borrower, then for that spouse the expenses
  were their own, and the loan can qualify as to them.
- Eligible student: the expenses must be "attributable to education furnished during a
  period during which the recipient was an eligible student" [IRC (d)(1)(C); Reg
  (e)(3)(i)(B), at least half the normal full-time workload]. The half-time test applies to
  the **student**, not the filer. On a joint return it applies to whichever spouse, or
  dependent, was educated (V).
- Sole purpose: Reg Example 6 under (e): a loan used partly for home improvements and partly
  for the borrower's **spouse's** education is not a qualified education loan (V).

**A6. Married filing separately.**
- Text: "If the taxpayer is married at the close of the taxable year, the deduction shall be
  allowed … only if the taxpayer and the taxpayer's spouse file a joint return" [IRC (e)(2);
  Reg (b)(3)]. Marital status is determined under § 7703 [IRC (e)(3)]. i1040 and Pub970 say
  the deduction is available for "any filing status except married filing separately" (V).
  The result for married filing separately is no deduction.
- Inferred, not verified: § 7703(b) treats some married people living apart as unmarried.
  Such a person may file as head of household and claim the deduction.

**A7. Other points that matter for two people's loans on one return.**
- Related person: a loan owed to a person related under § 267(b) or § 707(b)(1) is excluded
  [IRC (d)(1); Reg (e)(3)(iii)]. Pub970 lists "Your spouse" first. A loan from one spouse to
  the other is not qualified (V for the wording).
- Each loan's status is its own: the qualified-loan tests, the obligation test and the
  related-person test apply loan by loan. A non-qualifying loan of one spouse removes that
  loan's interest, not the other spouse's interest. (I, from the definitional structure. No
  text addresses the two-spouse mix directly.)
- Loan held jointly by both spouses: both are obligated. The interest is still paid once and
  counted once on the joint return (I).
- Form 1098-E goes to one person per loan: the "Payor means the individual … carried on the
  books … as the borrower …. If there are multiple borrowers, the principal borrower … is
  treated as the payor" [R6050S (b)(2)]. The $600 threshold "applies to each borrower"
  [i1098]. So one spouse may get no 1098-E, and a co-borrowed loan's form names only the
  principal borrower. The deduction does not depend on the form: "if you pay qualifying
  interest that isn't included on Form 1098-E, you can also deduct those amounts" [Pub970]
  (V).
- Double benefit: interest paid by employer educational assistance, or with tax-free § 529
  earnings, is excluded per payment [IRC (e)(1); Pub970], so it can affect one spouse's loan
  and not the other's (I).

**Not verified in Part A.** Whether Pub. L. 119-21 (2025) amended § 221: the Cornell notes
stop at 2021, the House U.S. Code page did not load, and the 2025 IRS publications state the
same rules. Also not fetched: Rev. Proc. 2024-40 and §§ 6013, 152(b)(2) and 7703. Reg §
1.221-1(a)(1) and (h) still describe applicability through 2010 under a repealed sunset. I
treated the regulation as current.

## Part B — the application today

**B1. Married filing jointly: does the calculation run, and what does it read?**
- The current core package `package.core-calculations.v42.json` pins
  `tax.us.2025.rule.sli-worksheet` **v5** [repo, V].
- v5 reads `filing_status` [repo `rule.sli-worksheet.v5.json:100`, `:270`]. The cap is
  `parameter.sli-interest-cap` = 2500, a single value with no key by status (`:326`,
  `:352`). The threshold is `parameter.sli-magi-threshold`, keyed by filing status (`:381`,
  `:423`): married filing jointly 170000, the others
  85000. The range is `parameter.sli-magi-phase-range` (`:396`, `:438`): married filing
         jointly 30000, the others 15000 [repo parameter files, V].
- Line 1 is the uncapped sum of **every** current Form 1098-E box 1 in the family [repo
  `rule.sli-worksheet-line1-subtotal.json`, `collect` over `tax.us.2025.f1098e.1`]. v5 caps
  that sum once at 2,500. MAGI is `tax.us.2025.income.total-income` minus a literal 0
  (`:368`, `:410`). The other Schedule 1 adjustments are asserted absent through
  `schedule1-adjustments-scope.no-line*` facts, and the route blocks
  (`SLI_SCHEDULE1_PART_II_OUT_OF_SCOPE`, `:494`) if any is not yes (V).
- Married filing separately blocks with `SLI_MFS_INELIGIBLE` (`:831`–`:847`). The
  application does not publish a zero for it (V).
- Runs [probe, V]: the harness in `tests/test_sli_track1_combined_standing.py`, case K0a
  (two statements, $3,000 + $1,800, adopting v42), changing only filing status and wages.
  MFJ at 180,000 gives line 21 = 1,668 (4,800 capped to 2,500; 10,000 / 30,000 = 0.333;
  2,500 − 832.5, rounded). MFJ at 50,000 gives 2,500. MFJ at 200,000 and single at 180,000
  give a computed zero. The v1 rule gives the same. The married-filing-jointly arithmetic
  runs and follows the 2025 worksheet.
- **No committed test exercises married filing jointly with student-loan interest** (V,
  grep). The student-loan tests use `single` and `married_filing_separately`.
  `tests/test_sli_worksheet_line21_track3.py` defaults to single, and its only other status
  is the MFS test at `:318`. `tests/derivation/adr0077_worksheet_fixture.py:118` lists
  married filing jointly only as a value the filing-status fact can take. Every
  `sli_correction_t1` workspace asserts `single`
  (`tools/generate_sli_correction_t1_fixtures.py:401`).

**B2. How the filer-level conditions are worded and keyed.**
- `sli-scope.bundle.json` declares five facts, **each keyed on `tax-year` only**, so there
  is one answer per return (`:9`, `:30`, `:51`, `:72`, `:93`; identity keys at `:13`–`:99`).
  Their titles say "Filer-level". Dependency (`:72`): "the filer is not claimed as a
  dependent by another taxpayer". Obligation (`:93`): "the filer is legally obligated to pay
  interest on the loan(s) claimed". A "no" to either gives a **literal 0 for the whole line
  21** [repo v5 `:455`–`:490`, the `any(... == "no")` branch] (V).
- Per-statement witnesses (related person, qualified employer plan, non-qualified component,
  employer assistance, § 529 earnings) are keyed on lender, statement and tax-year [repo
  `f1098e.bundle.json`]. v5 requires every statement to be "yes". A single "no" blocks the
  whole route with `SLI_UNIVERSAL_COMPONENT_VIOLATION` [v5 `:721`,
  `collect_categorical_all_equal`] (V).
- Spouse in the student-loan path: **none** (V, grep). The only spouse facts in the package
  are `spouse_blind` and `spouse_over_65`, for the standard deduction [repo
  `package.core-calculations.v42.json`], plus the line 6d "lived with spouse" fields.
- A committed analysis already names the obligation keying as a defect: it is "keyed on
  **tax-year only**. Obligation holds per loan" [repo
  `…/student-loan-circumstance-association-evidence/whose-deduction-model.md:115`–`:121`].

**B3. Do statements, borrowings or schooling carry a person?**
- Form 1098-E box 1 identity is lender + statement + tax-year. It has **no borrower or
  recipient key** [repo `f1098e.bundle.json`] (V).
- A borrowing is an entity, `tax.us.student-loan-borrowing-reference`, with an opaque id and
  a description the person supplies. It has no borrower field [repo
  `packages/tax/sli_relationship_recording.py:705`–`:730`] (V).
- A schooling situation is keyed on period, institution and programme. It has **no student
  key** [repo `sli-relationship-source.bundle.v2.json`] (V). The enrollment answer is keyed
  by borrowing, and its wording is "the student" [repo
  `packages/tax/sli_relationship_review.py:83`–`:88`].
- The rule's assumption list includes "The schooling was for the taxpayer, a spouse, or a
  dependent when the loan was incurred." This is listed as assumed, and the application does
  not ask about it [repo `rule.sli-statement-loan-support.json:185`;
  `…/student-loan-deduction-completion-evidence/track0e-conclusion-basis.md:302` calls it an
  "Adopted favorable assumption"] (V).

**B4. Person-facing wording.**
- Messages address "you": for example, "You said you cannot tell which student loan this
  statement covers." [repo `sli-combined-standing.bundle.json:134`,
  `sli-worksheet-inputs.bundle.json:289`]. The correction page's groups are titled "What you
  told us" and "Conditions left with you" [repo
  `packages/sample_data/sli_correction_t1/surface/content/app/index.html:280`–`:282`].
- Fact titles and the blocked explanation say "the filer". The explanation reads "… the
  filer is married filing separately …" [repo `schedule1.line-21.form-field.json:16`].
- The borrowing questions are impersonal: "This loan paid only for school costs." and "… the
  student was enrolled at least half-time …" [repo `sli_relationship_review.py:83`–`:88`].
  No wording distinguishes "you" from "your spouse" (V, grep).

**B5. Explicit scope statements.**
- These scope the work to one filer [repo, V]: "**Filer-centered.** No second person's
  identity, no per-payer ledger, no two-return coordination"
  (`…/whose-deduction-model.md:134`); "This milestone's scope is the filer as the student. …
  within this scope there is no second person"
  (`…/a5-stage2-circumstances-and-keying.md:244`–`:258`); premise X4, "The student is the
  tax-return filer"
  (`…/student-loan-interest-bounded-method-transfer-evidence/p1-bounded-executable-comparison.md:127`);
  "The model is filer-centered" (`student-loan-circumstance-association.md:86`).
- No committed document claims joint returns are supported (V, grep over the student-loan
  and f1098e plans and evidence). The f1098e plan specifies the married-filing-jointly
  threshold and range as worksheet arithmetic
  (`docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-agi.md:561`–`:565`).
  Its non-goals do not mention spouses. A reader could take the parameter values as support
  (I).
- A committed analysis records the instruction "You, or your spouse if filing jointly,
  aren't claimed" and calls the bar return-scoped
  (`…/p1-obligation-and-amounts.md:384`–`:390`).

## Part C — where present behavior and the law diverge or are untested

1. **Untested.** No committed test runs married filing jointly with 1098-E interest (B1).
   The arithmetic matches the 2025 worksheet in the uncommitted probe only.
2. **Spouse dependency.** The law, as i1040 states it, tests both spouses (A3). The app's
   one fact is worded "the filer" (B2). Whether one answer covers both spouses is not
   specified. This is low-frequency because of § 152(b)(2) (I).
3. **Obligation keyed per return.** The law tests obligation loan by loan, against either
   spouse, and counts a non-obligated spouse's payment toward the obligated spouse (A4). The
   app has one "the filer is legally obligated" yes/no, and a "no" zeroes the whole line
   (B2). If B is obligated only on B's own loan and A only on A's, the question has no clear
   answer. This defect was already recorded for one filer (`whose-deduction-model.md:115`).
4. **Whose education.** The law accepts the taxpayer, the spouse or a then-dependent, with
   timing that is unresolved for a loan made before marriage to a future spouse (A5). The
   app records no student and assumes the condition favorably (B3). The eligible-student
   test belongs to the student (A5). The app's enrollment answer is per borrowing, which
   fits, but it does not say who the student is (B3).
5. **No person on statements or borrowings.** In law, 1098-E goes to the principal borrower,
   and interest without a form still counts (A7). The app cannot tell which spouse a
   statement or borrowing belongs to (B3). It counts only box 1 amounts, and it assumes "Box
   1 holds no loan the person did not record" (`rule.sli-statement-loan-support.json:187`).
6. **One bad loan blocks all.** In law, a related-person or other non-qualifying loan
   removes only that loan's interest (A7, I). The app blocks the whole route when any
   statement witness is "no" (B2, v5 `:721`). The two-spouse case makes this more likely
   because there are more statements.
7. **Consistent with the law.** The single $2,500 cap per return over both spouses'
   statements (A1/B1). One joint MAGI with $170,000 and $30,000 (A2/B1). Married filing
   separately excluded (A6/B1), although the app blocks where the law gives a zero.
