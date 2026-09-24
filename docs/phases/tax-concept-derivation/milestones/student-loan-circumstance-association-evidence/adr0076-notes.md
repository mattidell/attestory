# ADR 0076 notes — authority quotations and case workings

Working evidence for `temp/a4-pass2/adr0076-draft.md`. Not a decision. Not authority over the draft's Parts 1 and 2, and not a selection of Part 3.

Read at branch `milestone/student-loan-circumstance-association`, HEAD `f0f1dd7630c330f5f1c6c840b8270152641eb8d2`. The probe write-up `g2-binding-and-scheduling.md` records itself at `b558da4e097367319816568f41091d4fbab5d0b5`. This pass did not re-run `tests/test_sli_g2_binding_probe.py`. "Executed" below means that write-up's named test called the existing hand-dispatch or the existing runners. "Traced" means read off source and not run on this chain.

Identities in the probes are synthetic `demo.*`.

## What was read

- `docs/adr/0075-link-coverage-operation.md` (accepted). The operator is not a binding proof. A result, including a returned parameter, does not support a statement-specific claim until the binding ADR 0076 is for exists.
- `g2-binding-and-scheduling.md` — the hand-dispatched probe results.
- `g2-path-investigation.md` Question 1 — how production schedules today, and why a subject declaration sits on the rule. Question 2 (the reader) is not this record.
- `a0-tax-concept-facts.md` F5, F6, F9. F5 is the qualified-education-loan classification, behind the box-1 route. F6 is eligible-student for the academic period the loan financed, behind F5. F9's three outcomes that matter here: a supported adverse determination; no adverse determination, so the bounded calculation proceeds; a favourable value from the default, recorded as default-supported. Independently proving every constituent is not a product outcome. F6's favourable value is the default, not a favourable ordinary answer. An adverse ordinary account is adequate to support failure of the test. It is not proof the person was ineligible.
- `a5-stage2-circumstances-and-keying.md` tests 1–3 and "the adverse case." Test 1 is two schooling situations in one period, one borrowing: separate identities, not a correction, and not an adverse pair. The à-la-carte Metro enrolment was withdrawn as an adverse account. Test 2 separates the schooling circumstance from the financing claim. Test 3 keys load on the course of study and withdraws an adverse reading of a combined credit total. The traced adverse case is a different period in which no credential programme anywhere confers the status.
- `whose-deduction-model.md`. Qualification is taxpayer-relative and dated. Interest the filer paid stays an event when a qualification condition fails; the treatment changes, the payment does not. Not the set-of-statuses question, and not re-decided here.

Primary text fetched this pass: 26 U.S.C. § 221 and § 25A from the Legal Information Institute; 26 CFR § 1.221-1 from the eCFR (title 26 displayed as of 2026-09-22). IRS Publication 970 (2025) is secondary only, and only the chapter 4 passages the search returned.

Not fetched as a primary quotation: 20 U.S.C. § 1091(a)(1) as in effect on 5 August 1997. § 25A(b)(3)(A) incorporates that historical sentence. This pass does not pretend a later compilation, the regulation's parenthetical, or Publication 970 is that sentence.

## Authority — 26 U.S.C. § 221

§ 221(a):

> In the case of an individual, there shall be allowed as a deduction for the taxable year an amount equal to the interest paid by the taxpayer during the taxable year on any qualified education loan.

§ 221(d)(1), the operative definition (related-person and employer-plan exclusions included because they are part of the same term, not because these cases turn on them):

> The term "qualified education loan" means any indebtedness incurred by the taxpayer solely to pay qualified higher education expenses—
>
> (A) which are incurred on behalf of the taxpayer, the taxpayer's spouse, or any dependent of the taxpayer as of the time the indebtedness was incurred,
>
> (B) which are paid or incurred within a reasonable period of time before or after the indebtedness is incurred, and
>
> (C) which are attributable to education furnished during a period during which the recipient was an eligible student.
>
> Such term includes indebtedness used to refinance indebtedness which qualifies as a qualified education loan. The term "qualified education loan" shall not include any indebtedness owed to a person who is related (within the meaning of section 267(b) or 707(b)(1)) to the taxpayer or to any person by reason of a loan under any qualified employer plan (as defined in section 72(p)(4)) or under any contract referred to in section 72(p)(5).

"Solely" is in the chapeau. It qualifies the indebtedness: incurred solely to pay qualified higher education expenses. (A), (B), and (C) qualify those expenses. (C) is a condition on the expenses — attributable to education furnished during a period during which the recipient was an eligible student — not a sentence that says "any adverse status disqualifies the loan."

§ 221(d)(2):

> The term "qualified higher education expenses" means the cost of attendance (as defined in section 472 of the Higher Education Act of 1965, 20 U.S.C. 1087ll, as in effect on the day before the date of the enactment of the Taxpayer Relief Act of 1997) at an eligible educational institution, reduced by the sum of—
>
> (A) the amount excluded from gross income under section 127, 135, 529, or 530 by reason of such expenses, and
>
> (B) the amount of any scholarship, allowance, or payment described in section 25A(g)(2).

(d)(2) does not mention the eligible student and does not split an indebtedness across academic periods. Eligible student is (d)(1)(C) plus (d)(3).

§ 221(d)(3):

> The term "eligible student" has the meaning given such term by section 25A(b)(3).

(A)'s dependency timing ("as of the time the indebtedness was incurred") is not (C)'s timing. (C) is the period the education was furnished.

Nothing in § 221(a) or § 221(d) allocates a fraction of the interest when some but not all of the proceeds paid expenses that fail (C). The allowance is interest paid on any qualified education loan. If the indebtedness is not within the term, (a) does not allow the interest paid on it.

## Authority — 26 U.S.C. § 25A(b)(3)

§ 221(d)(3) pulls this definition in. It is "for purposes of this subsection" inside § 25A(b), which is the American Opportunity credit subsection. § 221 adopts the term as (b)(3) defines it, not the credit limits in § 25A(b)(2).

> For purposes of this subsection, the term "eligible student" means, with respect to any academic period, a student who—
>
> (A) meets the requirements of section 484(a)(1) of the Higher Education Act of 1965 (20 U.S.C. 1091(a)(1)), as in effect on the date of the enactment of this section, and
>
> (B) is carrying at least ½ the normal full-time work load for the course of study the student is pursuing.

The status is of the student with respect to an academic period. (B) attaches the half-time standard to "the course of study the student is pursuing." The historical HEA § 484(a)(1) sentence is the content of (A) and was not quoted from a primary source in this pass. The date of enactment of § 25A is 5 August 1997.

## Authority — 26 CFR § 1.221-1

eCFR text, title 26 displayed as of 2026-09-22. The applicability paragraphs are quoted because they are still in that text. This pass does not resolve whether the 2010 condition they recite is spent.

§ 1.221-1(a)(1) (applicability, first two sentences and the sunset sentence):

> Under section 221, an individual taxpayer may deduct from gross income certain interest paid by the taxpayer during the taxable year on a qualified education loan. [...] The rules of this section are applicable to periods governed by section 221 as amended in 2001, which relates to deductions for interest paid on qualified education loans after December 31, 2001, in taxable years ending after December 31, 2001, and on or before December 31, 2010. [...] To the extent that the effective date limitation (sunset) of the 2001 amendment remains in force unchanged, section 221 before amendment in 2001, to which § 1.221-2 relates, also applies to interest due and paid on qualified education loans in taxable years beginning after December 31, 2010.

§ 1.221-1(h) repeats that applicability limit. The definitional workings below use paragraph (e) as the regulation's statement of the term. They do not decide that paragraph (h) makes (e) inapplicable to interest paid in 2024 or 2025.

§ 1.221-1(e)(2)(i) (qualified higher education expenses):

> Qualified higher education expenses means the cost of attendance (as defined in section 472 of the Higher Education Act of 1965, 20 U.S.C. 1087ll, as in effect on August 4, 1997), at an eligible educational institution, reduced by the amounts described in paragraph (e)(2)(ii) of this section. Consistent with section 472 of the Higher Education Act of 1965, a student's cost of attendance is determined by the eligible educational institution and includes tuition and fees normally assessed a student carrying the same academic workload as the student, an allowance for room and board, and an allowance for books, supplies, transportation, and miscellaneous expenses of the student.

§ 1.221-1(e)(3)(i) (qualified education loan):

> A qualified education loan means indebtedness incurred by a taxpayer solely to pay qualified higher education expenses that are—
>
> (A) Incurred on behalf of a student who is the taxpayer, the taxpayer's spouse, or a dependent (as defined in section 152) of the taxpayer at the time the taxpayer incurs the indebtedness;
>
> (B) Attributable to education provided during an academic period, as described in section 25A and the regulations thereunder, when the student is an eligible student as defined in section 25A(b)(3) (requiring that the student be a degree candidate carrying at least half the normal full-time workload); and
>
> (C) Paid or incurred within a reasonable period of time before or after the taxpayer incurs the indebtedness.

The parenthetical in (e)(3)(i)(B) — "a degree candidate carrying at least half the normal full-time workload" — is the regulation's gloss on § 25A(b)(3). It is not the text of HEA § 484(a)(1). "Degree candidate" is not the same words as Publication 970's "degree, certificate, or other recognized educational credential." This pass does not choose between them. Where the brief stipulates that the person was not an eligible student, the workings apply § 221(d)(1)(C) to that stipulation and do not re-derive the status from the gloss.

§ 1.221-1(e)(3)(ii) (reasonable period):

> Except as otherwise provided in this paragraph (e)(3)(ii), what constitutes a reasonable period of time for purposes of paragraph (e)(3)(i)(C) of this section generally is determined based on all the relevant facts and circumstances. However, qualified higher education expenses are treated as paid or incurred within a reasonable period of time before or after the taxpayer incurs the indebtedness if—
>
> (A) The expenses are paid with the proceeds of education loans that are part of a Federal postsecondary education loan program; or
>
> (B) The expenses relate to a particular academic period and the loan proceeds used to pay the expenses are disbursed within a period that begins 90 days prior to the start of that academic period and ends 90 days after the end of that academic period.

(B) is per academic period. It is a timing safe harbor for expenses, not a rule that the indebtedness is qualified only in part, and not a rule that one note becomes two loans.

§ 1.221-1(e)(3)(v):

> (A) A qualified education loan includes indebtedness incurred solely to refinance a qualified education loan. A qualified education loan includes a single, consolidated indebtedness incurred solely to refinance two or more qualified education loans of a borrower.
>
> (B) Treatment of refinanced and consolidated indebtedness. [Reserved]

(B) is reserved. It does not supply a portion rule, and it does not say how two loans that are later consolidated are treated. None of the five cases is a refinancing.

§ 1.221-1(e)(4), Example 4 (one note, two semesters, reasonable period — both semesters treated as qualified; eligibility does not differ):

> Student I signs a promissory note for a loan on August 15, 2003, to pay for qualified higher education expenses for the 2003 fall and 2004 spring semesters. On August 20, 2003, the lender disburses loan proceeds to Student I's college. The college credits them to Student I's account to pay qualified higher education expenses for the 2003 fall semester, which begins on August 25, 2003. On January 26, 2004, the lender disburses additional loan proceeds to Student I's college. The college credits them to Student I's account to pay qualified higher education expenses for the 2004 spring semester, which began on January 12, 2004. Student I's qualified higher education expenses for the two semesters are paid within a reasonable period of time, as the first loan disbursement occurred within the 90 days prior to the start of the fall 2003 semester and the second loan disbursement occurred during the spring 2004 semester.

One promissory note covers two academic periods. The example holds the reasonable-period condition met, disbursement by disbursement. It does not split the note into a qualified part and an unqualified part. It does not discuss a semester in which the student was not an eligible student.

§ 1.221-1(e)(4), Example 5, is the same loan after the college later loses eligibility. Later loss of institutional eligibility does not undo the loan. That is not an eligible-student holding, and it is not used below except to avoid reading it as one.

§ 1.221-1(e)(4), Example 6 (mixed-use loans):

> Student J signs a promissory note for a loan secured by Student J's personal residence. Student J will use part of the loan proceeds to pay for certain improvements to Student J's residence and part of the loan proceeds to pay qualified higher education expenses of Student J's spouse. Because Student J obtains the loan not solely to pay qualified higher education expenses, the loan is not a qualified education loan.

This is the regulation's only mixed-use decision. The other use is home improvement, not an ineligible academic period. The conclusion is about the loan, not a portion of the interest: the loan is not a qualified education loan. There is no tracing fraction.

§ 1.221-1(f)(1):

> Amounts paid on a qualified education loan are deductible under section 221 if the amounts are interest for Federal income tax purposes.

§ 1.221-1(f)(3):

> See §§ 1.446-2(e) and 1.1275-2(a) for rules on allocating payments between interest and principal. In general, these rules treat a payment first as a payment of interest to the extent of the interest that has accrued and remains unpaid as of the date the payment is due, and second as a payment of principal.

That allocation is interest versus principal on a loan. It is not qualified-use proceeds versus other proceeds, and it is not one academic period versus another.

§ 1.221-1(g)(1):

> Payments of interest on a qualified education loan to which this section is applicable are deductible even if the payments are made during a period when interest payments are not required because, for example, the loan has not yet entered repayment status or is in a period of deferment or forbearance.

The year the interest is paid is not the year of the eligible-student test. The test stays on the academic period the education was furnished.

## Authority — Publication 970 (2025), secondary

Chapter 4, as returned by search against irs.gov. Not controlling. It restates the statute's "solely" and the regulation's reasonable-period safe harbors. The passages retrieved do not state an allocation of interest when only part of the proceeds paid qualified expenses, and they do not discuss one loan across an eligible term and an ineligible term.

> This is a loan you took out solely to pay qualified education expenses (defined later) that were:
>
> For you, your spouse, or a person who was your dependent (as defined later for this purpose) when you took out the loan;
> Paid or incurred within a reasonable period of time before or after you took out the loan; and
> For education provided during an academic period for an eligible student.

Eligible student, student-loan-interest row of the publication's glossary, same secondary source:

> A student who was enrolled at least half-time in a program leading to a postsecondary degree, certificate, or other recognized educational credential at an eligible educational institution.

That glossary sentence is wider than the regulation's "degree candidate" parenthetical and is not HEA § 484(a)(1) as of 5 August 1997. It is not used to decide any case below. It is recorded so the difference stays visible.

## How the quoted text is used

Four distinctions the cases keep:

1. **The indebtedness is one thing.** § 221(d)(1) is "any indebtedness." A later consolidation is a different indebtedness, and its treatment is reserved. Two loans are two tests.
2. **"Solely" is about that indebtedness.** The regulation's mixed-use example applies it to the note: part of the proceeds not used for qualified higher education expenses, the loan is not a qualified education loan. No sentence then deducts the interest "on the qualified part."
3. **(C) is about the expenses and the period, not about every programme in the period.** The recipient was or was not an eligible student during the period the education was furnished. § 25A(b)(3) defines that status with respect to an academic period. A second enrolment in the same period is not, on these words, a subtraction from the status.
4. **Unknown is not a status the text deems.** (C) requires that the recipient was an eligible student. The text does not say a missing account is eligibility, and it does not say a missing account is ineligibility.

None of the five cases gives disbursement dates, a federal-loan-program fact, or the reductions in § 221(d)(2)(A) and (B). The reasonable-period condition is therefore not determined for any of them. The cost-of-attendance reductions are not determined either. The workings say what (C) and "solely" do with the facts the brief states, and they mark the rest silent.

"Any adverse status disqualifies the loan" is not derived here from `subject_dispatch._scope`, from `test_two_statuses_for_one_borrowing_disagree_and_block`, or from the spring-2025 example. Those are recorded in the engine section below so they are not mistaken for this text.

## Case (a) — one loan, autumn 2024 eligible, spring 2025 not an eligible student

Facts taken from the brief, not from a return: one indebtedness finances autumn 2024, in which the recipient was an eligible student, and spring 2025, in which the recipient was not an eligible student because there was no credential-programme enrolment anywhere that term. No amounts. No disbursement dates. No fact about whose education, relatedness of the lender, or employer-plan proceeds.

(C) applied to the spring expenses: the education was furnished during a period during which the recipient was not an eligible student. Those expenses do not satisfy (C). They are not within the class of expenses the indebtedness must have been incurred solely to pay.

(C) applied to the autumn expenses: the brief stipulates the recipient was an eligible student during that period, so (C) does not fail for education furnished then. (A), (B), and § 221(d)(2) are not stipulated. "Can satisfy (C)" is not "is a qualified education loan."

The indebtedness, on the facts that are stipulated, paid at least one set of expenses that fail (C) and at least one set that do not fail (C) on eligible-student grounds. The chapeau requires the indebtedness to have been incurred solely to pay qualified higher education expenses meeting (A), (B), and (C). Example 6 is the regulation's decision when part of the proceeds pay qualified higher education expenses and part do not: the loan is not a qualified education loan. Example 6's other use is home improvement. Applying it to an ineligible academic period is applying "solely" plus (C), not reading a two-term example. There is no two-term example. Example 4 is the closest, and both of its semesters are inside the qualified class; it treats the note as one loan and holds only the reasonable-period condition.

If that application of "solely" is right, the loan is not a qualified education loan at all. It is not a qualified loan in part. § 221(a) then allows none of the interest paid on it. § 1.221-1(f)(1) deducts interest paid on a qualified education loan. (f)(3) does not save a portion: it splits a payment into interest and principal.

If that application is not right — if an ineligible term is a different kind of mixed use from home improvement, and the regulation's silence on academic periods is a real gap — then the text does not say the autumn portion's interest is deductible either. It simply does not address the split. That gap is why unresolved-blocks is on the candidate list. It is not a second holding.

What the text does not say: that the spring status "spoils" the autumn status by being adverse; that the interest is deductible in the ratio of autumn proceeds to total proceeds; that the reasonable-period safe harbor fails (no disbursement facts; the safe harbor is per period and Example 4 shows one note can cover two periods); that the year the interest is paid changes (C) (see (g)(1)).

## Case (b) — one loan, one period, degree programme at one school and non-credential classes at another

This is the shape of A5 test 1, which that write-up refused to treat as adverse, plus the brief's stipulation that one side is a degree programme and the other is non-credential classes. Same period. One indebtedness finances both. Workload is not stated. Whether either institution is an eligible educational institution is not stated. Half of whose normal full-time load is not stated.

§ 221(d)(1)(C) asks whether the expenses are attributable to education furnished during a period during which the recipient was an eligible student. § 25A(b)(3) defines eligible student with respect to an academic period: HEA § 484(a)(1) as of 5 August 1997, and at least half the normal full-time workload for the course of study pursued. The regulation's gloss adds "degree candidate" and the same half-time condition, and it places that status on the academic period ("when the student is an eligible student").

On those words, a person enrolled in a degree programme during the period can be an eligible student for that period. Nothing in (C), (d)(3), or (e)(3)(i)(B) says a second, non-credential enrolment in the same period revokes that status or subtracts from it. A5's withdrawn reading is the same observation, and it is not upgraded here into a rule: it is what the quoted sentences do not say.

What remains open, and is not answered by "the period status was met":

- Whether the non-credential expenses are qualified higher education expenses under § 221(d)(2) and § 1.221-1(e)(2). That is cost of attendance at an eligible educational institution, as the institution determines it, reduced by (d)(2)(A) and (B). Non-credential is not, by itself, "not cost of attendance." Institutional eligibility and the institution's cost of attendance are not in the facts.
- If those expenses are not qualified higher education expenses, "solely" and Example 6 are back in the same posture as case (a): part of the proceeds may have paid something outside the class. The text does not determine that they did.
- § 25A(b)(3)(B) can still fail if the person was not carrying half the workload for the course of study pursued. The facts do not say. A0 places that standard with the person, not with a calculation that compares credit counts. This pass does not run the comparison.
- The regulation's "degree candidate" gloss and Publication 970's "certificate or other recognized credential" are not reconciled here. The brief's "non-credential" might or might not fail HEA § 484(a)(1) as of 1997. That sentence was not quoted. It does not matter for the period if the degree programme independently meets (A); it would matter if someone claimed the non-credential classes were what made the person an eligible student. Nobody needs to claim that on these facts.

So the loan is not shown to fail (C) for the period. It is also not shown to be a qualified education loan: "solely," (d)(2), (A), (B), and the half-time fact are all unstated. Deductible interest is not a number. Treating the non-credential classes as an adverse status that disqualifies the loan, or as a portion to carve out, is an addition to the text.

## Case (c) — one loan financing only an ineligible period

The only education the indebtedness paid for was furnished during a period the recipient was not an eligible student. (C) fails for those expenses. The indebtedness was not incurred solely to pay qualified higher education expenses meeting (C). It is not a qualified education loan. § 221(a) allows no deduction for the interest paid on it.

This is not a qualified loan whose deductible portion is zero. The term does not include it. Portion-based language reaches a zero deduction only by describing a loan the statute has already left outside the term.

Unresolved-blocks is the wrong posture. The classification is determined by (C) and the chapeau. Refusing to say "not a qualified education loan" treats a stipulated failure as an unknown.

Nothing in the text makes this loan's failure depend on some other loan, some other period, or on how many status rows a join returned.

## Case (d) — two loans, each financing one period

Two indebtednesses. Each is its own "any indebtedness" under § 221(d)(1). § 221(a) allows the interest paid on any qualified education loan, which is per loan, not per filer and not per borrowing-id shared across loans.

Take the brief's contrast with (a) seriously: each loan finances one period. Then each loan is case (c) or the single-period eligible case, not case (a).

- The loan that financed only a period in which the recipient was an eligible student is a qualified education loan only if it was incurred solely to pay expenses that also meet (A), (B), and § 221(d)(2). (C) does not fail. Its interest, if it is a qualified education loan, is interest paid on a qualified education loan. The cap and the phase-out are outside this question.
- The loan that financed only an ineligible period is case (c). Not a qualified education loan. None of its interest is allowed under § 221(a).

The failure of the second does not move to the first. No sentence aggregates a filer's loans for the eligible-student test. § 1.221-1(e)(3)(v)(A) includes a consolidation only when the consolidation itself was incurred solely to refinance qualified education loans. (v)(B) reserves the treatment. These two loans are not, on the stated facts, a consolidation. The reserved paragraph is not a reason to blend them, and it is not a portion rule for either one.

A set-level rule that collects every status the filer has and disqualifies every loan gets this case wrong. A rule that collects every status of one borrowing gets this case right only because each loan has one period. That is per-indebtedness classification, which is what the statute already does. It is not evidence for a set rule.

## Case (e) — one loan, a period with no status

Some period the loan financed has no status. No enrolment account, not an account that says "not an eligible student." The other facts of case (a) or (c) are not stipulated; the brief isolates the unknown.

(C) is true only if the expenses are attributable to education furnished during a period during which the recipient was an eligible student. An absent account does not make that sentence true. It also does not make it false. Example 6 does not fire, because it is not known that part of the proceeds paid expenses outside the class. The reasonable-period safe harbors do not fire, because disbursement is not known.

§ 221 does not contain a default. The product's F6/F9 posture is a different artifact: where no enumerated disqualifier is supported, a favourable value is produced and the record has to say the basis is the default; a supported adverse account fails the constituent; absence of adverse information is not the same as adverse information of unresolved scope (A5, citing A3). A missing status for a period this loan financed can be read as either of those last two. The statute does not say which. This pass does not extend the default to (e) and does not withdraw it.

Consequences that follow without inventing a status:

- Whole-loan disqualification reaches "not a qualified education loan" only by treating the unknown as a failed (C). That treatment is not in the text.
- A portion cannot be computed. There is no qualified fraction to multiply by the interest, and (f)(3) would not be that multiplication even if there were.
- Leaving the interest treatment undetermined matches the silence. It is a response to the text, not a sentence in the text. It blocks a deduction the statute has not allowed and has not denied.

If the unknown period sits beside a known failure, the case is (a) or (c), not (e): a stipulated failure of (C) is enough for the "solely" question, and the unknown is surplus. If the unknown period sits beside a known eligible period and no known failure, the case is the open one.

## Candidates, scored against the text

"Gets right" means the option's result is one the quoted text requires, not one the text merely fails to forbid.

**Whole-loan disqualification.** If the indebtedness was not incurred solely to pay expenses meeting (A), (B), and (C), it is not a qualified education loan, and § 221(a) allows none of the interest paid on it.

- (a) gets right only by treating expenses that fail (C) as a non-qualified use in the sense of Example 6. The chapeau supports that step. Example 6's facts do not. No period-splitting example contradicts it. Deductible interest, if the step is taken: none.
- (b) does not get right if "non-credential classes" are treated as the failing use. (C) is not shown to fail for the period. The option does not disqualify on the facts given, and it must not be stretched until it does.
- (c) gets right. Not a qualified education loan. No interest allowed.
- (d) gets right when applied to each indebtedness separately. It gets wrong when one loan's failure is assigned to the other.
- (e) gets right only if unknown counts as failure. It does not.

**Portion-based.** The indebtedness is a qualified education loan to the extent of the proceeds that paid expenses meeting (A), (B), and (C), and only a corresponding part of the interest is deductible.

- (a) does not get right. No sentence states the fraction. Example 6 decides the loan, not a part of the interest. (f)(3) allocates interest and principal.
- (b) does not get right. Carving out the non-credential classes assumes they are outside the class. The text does not say that.
- (c) reaches a zero deduction and describes the loan as partly qualified. The text describes it as outside the term. The amount coincides; the classification does not.
- (d) is not the rule that separates the two loans. Each loan is entire. A portion rule is idle if it is not also wrong.
- (e) cannot be computed.

**Unresolved-blocks.** Where the statuses do not determine whether the indebtedness was incurred solely to pay expenses meeting (C), the interest treatment for that indebtedness is not determined, and no deduction proceeds on it.

- (a) gets right only as a refusal to extend Example 6 from home improvement to an ineligible term. If that extension is accepted, the classification is determined and blocking over-refuses it. Both descriptions of the gap belong in front of the owner. This option does not dissolve the gap.
- (b) matches the silence that is actually there: institutional eligibility, cost of attendance, half-time, and therefore "solely" are undetermined. It does not match a silence about whether the second programme revokes the period's status. That revocation is not in the text; it is not an open fact.
- (c) gets wrong. The text determines "not a qualified education loan."
- (d) gets wrong for the ineligible loan, and wrong if the eligible loan is blocked because the other loan failed.
- (e) matches the silence. It does not claim the statute ordered a block. The statute neither allows nor denies the interest while (C) is unknown.

**Any adverse status in the set disqualifies the borrowing.** Not offered as a co-equal reading. Scored because the join suggests it and one example can be mistaken for it.

- It is not (C). (C) asks whether the recipient was an eligible student during the period the education was furnished.
- It is not "solely." "Solely" asks what the indebtedness was incurred to pay, after (A), (B), and (C) have classified the expenses.
- (a) coincides in result with whole-loan disqualification and gives the wrong reason.
- (b) is the reading A5 withdrew. The text does not support it.
- (c) coincides in result with the statute for a single ineligible loan. One loan with one failing period does not make a set rule.
- (d) gets wrong as soon as the set crosses loans.
- (e) gets wrong whether absence is treated as non-adverse (the deduction proceeds without (C)) or as adverse (absence is relabeled failure).

**Default-supported favourable value** (A0 F6/F9, already a product posture, not a sentence in § 221). Where no enumerated disqualifier is supported, the application produces a favourable eligible-student value and the record says the basis is the default. A supported adverse account fails the constituent.

- It is not applied here to (a) or (c). Those are supported failures of (C), not empty accounts.
- It is a candidate answer to (e) only if a missing status on a financed period is "no enumerated disqualifier," rather than adverse information of unresolved scope. A0's own sources distinguish those. This pass does not reclassify (e) as either one.
- It does not answer (b). The non-credential classes are not a supported disqualifier on the quoted text, and the default is not what makes them qualified expenses under (d)(2).

No candidate gets every case right on the text alone. Whole-loan disqualification is the one that tracks "solely" and Example 6 for a known non-qualified use, and it is the one that decides (c) and the separate loans in (d). It does not decide (b) or (e), and its step from (C) to Example 6 in (a) is an application across a factual gap the regulation does not bridge. Portion-based allocation is not in the quoted text. Unresolved-blocks is the honest response to (e) and to what (b) leaves open, and it is too weak for (c) and, if Example 6 is applied, for (a). The owner selects. This record does not.

## Engine behaviour that is not this text

Hand-dispatched, `tests/test_sli_g2_binding_probe.py`. Not a production scheduling result. Not a reading of § 221.

`test_two_statuses_for_one_borrowing_disagree_and_block`: two financing claims, one borrowing, two periods, two enrolments, reduction values 100 and 40. The reduction blocks `DEPENDENCY_INVALID` and names both financing fact ids. The statement blocks uncovered on that link.

`test_two_statuses_for_one_borrowing_agree_and_sort_first_publishes`: both values 100. The reduction publishes the sort-first status by finding id and does not pin the other. The statement publishes 1400 (1500 − 100).

Disagreeing duplicates block. Agreeing duplicates publish one and drop the other from the pins. The shared name is `borrowing` alone. That is the shape the owner rejected as a binding. It is also not "any adverse status disqualifies," because the agreeing pair does not disqualify anything. It must not be cited as evidence for a set-level tax rule in either direction.

The link identity (lender + statement + tax-year + borrowing) and the financing identity (borrowing + period + institution + programme) do not contain each other. Neither containment direction validates this edge. One shared name, `borrowing`, is the relationship Part 2 rejects everywhere else. Two loans that share a borrowing id are one identity under a borrowing-only join, which is a different defect from case (d)'s two indebtednesses.

## Probe inventory used by Parts 1 and 2

Coverage figures in the write-up: box 1 of 1000 and 400, reductions 100 and 40, each reduction keyed like its link. A cross-join publishes 860 and 260. A one-link join publishes 900 and 360.

Executed joins:

| Test | What happened |
| --- | --- |
| `test_tax_year_and_borrowing_joins_both_statements` | Only shared name is tax year. Both statements publish the sum, 860 and 260. |
| `test_shared_statement_id_joins_both_lenders` | Shared statement id. Same cross-join, 860 and 260. |
| `test_full_statement_identity_joins_only_its_statement` | Lender + statement + tax-year + borrowing. Each link joins only its statement. 900 and 360. `joined_contains_subject` accepts; `subject_contains_joined` rejects because borrowing is not a statement key. `row_binding` returns `join` for that statement and `disagree` for the other. |
| `test_lender_and_tax_year_splits_these_two_lenders` | Looks like the full-identity split, 900 and 360, because the lenders differ. Statement is not in the key. |
| `test_lender_and_tax_year_collides_for_one_lender` | Same key names, one lender, two statement ids. Cross-join, 860 and 260. |
| `test_full_enrolment_reaches_both_borrowings_of_one_situation` | Enrolment keyed period + institution + programme. Both borrowings of that situation publish `not-adverse`. The third borrowing publishes `adverse` from its own enrolment. `subject_contains_joined` is the direction that accepts this; `joined_contains_subject` rejects it because the enrolment has no borrowing key. |
| `test_period_only_enrolment_reaches_every_financing_in_that_period` | One enrolment keyed period only. All three financings publish `not-adverse`. `subject_contains_joined` accepts, and that acceptance is wrong for a full situation. `row_binding` of Z's full financing keys against the period-only row, required names period + institution + programme, returns `missing`. |
| `test_narrow_link_is_dropped_when_a_wide_link_widens_shared_names` | Today's `_scope` drops the narrow link. S1 publishes 900 and does not pin it. S2 publishes 400, the no-link parameter, and does not pin it. `row_binding` of the narrow row against the statement identity returns `missing`. |
| `test_period_only_row_is_dropped_when_a_full_row_widens_shared_names` | Same drop on the enrolment side. The financing publishes the full row. Nothing blocks. |
| `test_identical_statement_keys_join_both_facts` | Two statement facts, same lender, statement id, and tax year, different fact ids. One fully keyed link joins both. They publish 900 and 300. Containment of names accepts this because the values agree. |

The package-validation fact-surface walk (bare `fact-type.v2` members are on the validation surface and in `fact_types_by_key`) was read, not executed. Stated in the probe write-up.

Scheduling, executed against the current runners, which do not dispatch these rules:

| Test | What happened |
| --- | --- |
| `test_status_blocked_for_one_financing_blocks_that_link_and_the_statement` | Status rule id is in `resolved`. The other financing's reduction is `DEPENDENCY_ABSENT` / missing the status. The statement is `DEPENDENCY_INVALID` / missing that link. It does not publish 1500 − 100 and does not take the parameter. After the one keyed status publication, `is_eligible` on the reduction is false: the unsuffixed status symbol is absent and the keyed symbol is present. |
| `test_status_blocked_for_every_financing_blocks_every_link` | Rule id resolved. Both reductions absent. The statement blocks both link findings, sorted. Not the parameter. |
| `test_status_inapplicable_for_one_financing_leaves_no_source` | No status source for the inapplicable financing. Its reduction is `DEPENDENCY_ABSENT`. The statement blocks that link. From the successor, inapplicable and blocked are the same: no keyed source. |
| `test_skipping_status_makes_every_reduction_absent` | Executed as data, not as a scheduler. Status rule id not resolved. Both reductions absent. The statement is uncovered on both links. |
| `test_amount_before_reduction_blocks_uncovered_and_stays_resolved` | Amount rule runs with both links present and no reduction yet. Statement blocks `DEPENDENCY_INVALID` with both link finding ids. The amount rule id is resolved. The later reduction does not reopen that row. An empty reduction slot is an uncovered link. |
| `test_both_runners_record_ordinary_absence_and_agree` | `run` and `run_reference` record the same three unsuffixed `DEPENDENCY_ABSENT` rows and no keyed publication. |
| `test_attempt_blocks_scope_unbound_when_box1_is_a_symbol` | Box 1 in `symbols`, so `is_eligible` is true. `attempt` evaluates the amount rule once and blocks `link-coverage-scope-unbound`. No keyed symbol. |
| `test_finalize_unreached_evaluates_coverage_once_when_requires_are_met` | The same unsuffixed block from `finalize_unreached` alone. The ordinary fallback evaluates; it does not call `attempt`. |

Traced only: a predecessor rule absent from the package. `consequence_eligibility` returns eligible when the supportability rule id is not among `run.ctx.rules`, and waits on that id when it is present (`packages/tax/pairing_consequences.py`). The same don't-wait posture is not what `is_eligible` does today for an ordinary `requires` entry, and it was not executed on the status → reduction → amount chain. `g2-path-investigation.md` Question 1's description of production (`live.live_coordinate_run` → `_execute`; nothing in rule content selects `evaluate_subject_scoped_rule`; keyed publication stores `publishes|fact_id` and does not insert the unsuffixed name) was read at the investigation's commit and not re-traced line by line at `f0f1dd76`. The three functions as they stand at this HEAD still match that account: `is_eligible` ends at `all(req in self.symbols for req in self._requires(rule))` after the pairing and nominee id tests; `attempt` returns at the pairing intercept before any per-subject call; `finalize_unreached` evaluates an ordinary rule's guard and value itself; `run_reference` calls `is_eligible`, `attempt`, and `finalize_unreached`, returns early when the unsuffixed symbol is already in `state.symbols`, and skips a rule id already in `resolved`.
