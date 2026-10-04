# Track 0e — what supports the favorable conclusion

Paper only. No rule, package, schema, or test was changed.
Read on the milestone branch at the start of Track 0e.

This note traces the fact the new path replaces, then says how the decided
design supports each condition of that fact. The result's name and the route
map follow from the table. They are not settled by calling the result
`qualified`.

Authorities actually read:

- 26 U.S.C. § 221, as displayed by the Legal Information Institute at
  `https://www.law.cornell.edu/uscode/text/26/221`, read 2026-10-01.
- 26 CFR § 1.221-1, as displayed by the eCFR (unofficial; the page said title
  26 was current as of 2026-09-30), T.D. 9125, 69 FR 25492 (May 7, 2004).
- IRS Publication 970 (2025), *Tax Benefits for Education*, chapter 4,
  printed pages 30–35, from the PDF at `https://www.irs.gov/pub/irs-pdf/p970.pdf`
  (created 2026-01-29, for use in preparing 2025 returns).

Anything not in that list is unverified. Cross-references those three texts
name, and that this unit did not open, are collected at the end of section 1.

The eCFR text of § 1.221-1(a)(1) and (h) says the regulation applies to
interest paid on a qualified education loan after December 31, 2001, in
taxable years ending after that date and on or before December 31, 2010, and
that if the 2001 sunset stays in force the pre-2001 statute applies after
2010. Whether a later act removed that sunset was not read. Publication 970
(2025), chapter 4, states the deduction for 2025 returns without a 60-month
limit and with the 2025 income limits. The loan conditions below are taken
from § 221(d), from § 1.221-1(e), and from chapter 4. The regulation's sunset
sentence is not treated as a 2025 operating rule, and it is not treated as
repealed.

## 1. The replaced proposition, traced

The fact the new path replaces is
`tax.us.2025.f1098e.no-non-qualified-loan-component`, in
`packages/content/tax/2025/f1098e.bundle.json`. Its title says one yes/no
answer stands in for the student-status, qualified-education-expense, and
reasonable-period-of-time sub-questions, and that Publication 970 gives no
per-return signal to separate them. `yes` means that excluded class is absent
from this statement's box 1. `no` means it is present. There is no default.
The title cites Publication 970 pages 30–31. Those pages were read for this
note. The title is the bundle's summary of them, not a second statute.

The owner decision of 2026-10-01 keeps the other four statement answers as
asked questions. This note still lists the lender-relationship and
legal-obligation conditions, because they sit on the same statutory
definition or on the same deduction, and it says where they are already
asked. It does not fold them back into the replaced fact.

A qualified education loan, for this deduction, is the following. Each row
is a condition that bears on the replaced fact. The basis table in section 2
says what the design does with it.

**The loan is indebtedness the taxpayer incurred.** Section 221(d)(1) defines
a qualified education loan as indebtedness incurred by the taxpayer.
Section 1.221-1(e)(3)(i) uses the same words. Publication 970, page 30, says
it is a loan you took out.

**The loan was taken out solely to pay qualified education expenses.**
Section 221(d)(1) requires that the indebtedness be incurred solely to pay
qualified higher education expenses. Section 1.221-1(e)(3)(i) repeats
"solely." Example 6 of § 1.221-1(e)(4) says a loan used partly for home
improvements and partly for a spouse's qualified higher education expenses is
not a qualified education loan, because it was not obtained solely for those
expenses. Publication 970, page 30, says the loan must have been taken out
solely to pay qualified education expenses. Page 32 says interest on a
revolving line of credit is student loan interest only if the line is used
only to pay qualified education expenses, and says that if a refinance is for
more than the original loan and the extra is used for anything other than
qualified education expenses, none of the interest on the refinanced loan is
deductible.

**The expenses are qualified higher education expenses.** Section 221(d)(2)
defines them as the cost of attendance, as defined in section 472 of the
Higher Education Act of 1965 as in effect on the day before the Taxpayer
Relief Act of 1997 was enacted, at an eligible educational institution,
reduced by amounts excluded under sections 127, 135, 529, or 530 by reason of
those expenses, and by any scholarship, allowance, or payment described in
section 25A(g)(2). The term "eligible educational institution" has the
meaning in section 25A(f)(2), and also includes an institution conducting an
internship or residency program leading to a degree or certificate awarded by
an institution of higher education, a hospital, or a health care facility
that offers postgraduate training. Section 472, section 25A(f)(2), and
section 25A(g)(2) were not opened.

Section 1.221-1(e)(2)(i) restates cost of attendance and says, consistent
with that Higher Education Act section, that the eligible educational
institution determines it and that it includes tuition and fees normally
assessed a student carrying the same academic workload, an allowance for room
and board, and an allowance for books, supplies, transportation, and
miscellaneous expenses. Paragraph (e)(2)(ii) lists the reductions: a
section 117 scholarship, specified veterans' and armed-forces educational
allowances, section 127 employer-provided educational assistance, other
section 25A(g)(2)(C) educational assistance, excluded savings-bond interest
under section 135, excluded Coverdell distributions under section 530(d)(2),
and excluded qualified-tuition-program distributions under
section 529(c)(3)(B). Section 1.221-1(e)(1) says an eligible educational
institution is, in general, a college, university, vocational school, or
other postsecondary institution described in section 481 of the Higher
Education Act as in effect on August 5, 1997, and certified by the Department
of Education to participate in its student-aid programs, as described in
section 25A(f)(2) and § 1.25A-2(b), plus the same internship and residency
extension. Section 481 and § 1.25A-2(b) were not opened. Example 5 of
§ 1.221-1(e)(4) says a later loss of that eligibility does not undo a loan
used for periods when the institution still had it.

Publication 970, pages 31–32, describes the same expenses as the total costs
of attending an eligible educational institution, including tuition and fees,
room and board, books, supplies, equipment, and other necessary expenses such
as transportation. Room and board qualifies only up to the institution's
allowance in the cost of attendance for that period and living arrangement,
or, if greater, the actual charge for housing the institution owns or
operates. The institution is generally one eligible to participate in a
Department of Education student-aid program, including some institutions
outside the United States, and it includes the internship and residency case.
It must meet that test only for the academic period or periods for which the
loan was incurred. Pages 31–32 then require the expenses to be reduced by
employer-provided educational assistance, tax-free Coverdell earnings,
tax-free qualified-tuition-program earnings, excluded U.S. savings-bond
interest, the tax-free part of scholarships and fellowship grants, veterans'
educational assistance, and any other nontaxable educational assistance other
than gifts or inheritances.

**Whose education, and when.** Section 221(d)(1)(A) requires the expenses to
be incurred on behalf of the taxpayer, the taxpayer's spouse, or a dependent
of the taxpayer as of the time the indebtedness was incurred. Dependent has
the meaning in section 152, determined without regard to subsections (b)(1),
(b)(2), and (d)(1)(B). Section 152 was not opened. Section 1.221-1(e)(3)(i)(A)
states the same person and the same timing, and points at section 152 for
dependent. Publication 970, page 30, says the expenses were for you, your
spouse, or a person who was your dependent when you took out the loan, and
pages 30–31 widen "dependent" for this purpose beyond the usual claim rules,
including a person you could have claimed except for the joint-return,
gross-income, or you-yourself-are-a-dependent limits. The dollar figure it
gives for that gross-income limit for 2025 is $5,200. The usual dependent
tests in Publication 501 were not opened.

**A reasonable period.** Section 221(d)(1)(B) requires the expenses to be
paid or incurred within a reasonable period of time before or after the
indebtedness is incurred. Section 1.221-1(e)(3)(i)(C) and (e)(3)(ii) say
that period is generally all the relevant facts and circumstances, and that
the expenses are treated as inside it if they are paid with loans that are
part of a federal postsecondary education loan program, or if they relate to
a particular academic period and the proceeds are disbursed in a window that
begins 90 days before that period starts and ends 90 days after it ends.
Publication 970, pages 30–31, states the same two safe harbors and the same
facts-and-circumstances fallback. Page 31 defines an academic period as a
semester, trimester, quarter, or other period of study, such as a summer
session, as the institution reasonably determines, or a payment period where
the institution uses credit or clock hours and has no terms.

**The student was an eligible student for that education.** Section
221(d)(1)(C) requires the expenses to be attributable to education furnished
during a period when the recipient was an eligible student. Section 221(d)(3)
says eligible student has the meaning in section 25A(b)(3). Section 25A(b)(3)
was not opened. Section 1.221-1(e)(3)(i)(B) requires the expenses to be
attributable to education provided during an academic period, as described in
section 25A and the regulations under it, when the student is an eligible
student as defined in section 25A(b)(3), and it adds in parentheses that this
requires the student to be a degree candidate carrying at least half the
normal full-time workload. The section 25A regulations were not opened.
Publication 970, page 31, says an eligible student was enrolled at least
half-time in a program leading to a degree, certificate, or other recognized
educational credential. Half-time means at least half the normal full-time
workload for that course of study. The institution determines that standard,
and the standard may not be lower than any standard the Department of
Education has set under the Higher Education Act of 1965. That Act's
half-time standard was not opened. Page 30's glance table states the same
enrollment test and adds that it is at an eligible educational institution.

**Refinancing.** The flush language of section 221(d)(1) says the term
includes indebtedness used to refinance indebtedness that qualifies as a
qualified education loan. Section 1.221-1(e)(3)(v) says a qualified education
loan includes indebtedness incurred solely to refinance one, and a single
consolidation incurred solely to refinance two or more qualified education
loans of the same borrower. The paragraph headed "Treatment of refinanced and
consolidated indebtedness" is reserved. Publication 970, page 32, includes
interest on a loan used solely to refinance a qualified student loan of the
same borrower, and on one consolidation of two or more such loans of that
borrower. The caution on that page, quoted above, denies the deduction for
the whole refinanced loan when extra proceeds are used for anything else.

**Not a related person, and not an employer plan.** The same flush language
of section 221(d)(1) excludes indebtedness owed to a person who is related,
within the meaning of section 267(b) or 707(b)(1), to the taxpayer, and
indebtedness to any person by reason of a loan under a qualified employer
plan defined in section 72(p)(4) or under a contract referred to in section
72(p)(5). Those four sections were not opened. Section 1.221-1(e)(3)(iii)
repeats both exclusions and gives a parent or grandparent as an example of a
related person. Publication 970, pages 30–31, says the loan cannot be from a
related person or made under a qualified employer plan, and lists related
persons as the taxpayer's spouse, brothers and sisters, half brothers and
half sisters, ancestors, lineal descendants, and certain corporations,
partnerships, trusts, and exempt organizations. A federal guarantee is not
required: § 1.221-1(e)(3)(iv) says a loan does not have to be issued or
guaranteed under a federal postsecondary education loan program. Publication
970 does not add a federal-loan requirement. Example 3 of § 1.221-1(e)(4) is
a commercial bank loan that is still a qualified education loan.

**The taxpayer's obligation to pay the interest.** This is a condition of the
deduction, and it is not one of the three sub-questions named in the replaced
fact's title. Section 221(a) allows the deduction for interest paid by the
taxpayer during the year on a qualified education loan. Section 1.221-1(b)(1)
allows it only if the taxpayer has a legal obligation to make interest
payments under the terms of the loan. Publication 970, page 33, requires that
the taxpayer be legally obligated to pay interest on a qualified student
loan, and page 32 says interest the taxpayer is not obligated to pay under
the loan's terms is not included. Page 33 treats a payment by someone else,
on a loan the taxpayer is obligated to pay, as the taxpayer's payment.
Section 1.221-1(b)(4) is the same third-party rule.

**What paid the interest, as distinct from what the loan paid for.** Section
221(e)(1) denies the deduction for an amount deductible under another
provision of chapter 1, and for an amount for which an exclusion is allowable
under section 127 because the taxpayer's employer paid indebtedness on the
taxpayer's qualified education loan. It also reduces the deduction, before
the dollar cap, by qualified-tuition-program distributions treated as paying
the taxpayer's loans under section 529(c)(9), to the extent those earnings
would have been included in income under section 529(c)(3)(A) but for that
treatment. Sections 127 and 529 were not opened. Section 1.221-1(g)(2), which
is the 2004 regulation, denies a deduction for an amount deductible elsewhere
in chapter 1 and for an amount excludable under section 108(f). It does not
contain the section 127 employer-payment sentence or the section 529(c)(9)
reduction; those appear in the statute as read and in Publication 970.
Publication 970, page 33, says the taxpayer cannot deduct student-loan
interest that is deductible under another provision, cannot deduct earnings
from a qualified tuition program distributed after 2018 to the extent those
earnings are tax free because they paid student-loan interest, and, for
payments after March 27, 2020, cannot deduct interest the employer paid under
an educational assistance program. These are conditions on the interest, not
on whether the loan itself is a qualified education loan. The other two
statement answers already ask them. They are listed so they are not mistaken
for part of the replaced fact.

The dollar cap, the income phaseout, married filing separately, and the rule
that a claimed dependent cannot take the deduction are conditions of the
amount or of the taxpayer. They are sections 221(b), 221(c), and 221(e)(2),
§ 1.221-1(b)(2), (b)(3), (c), and (d), and Publication 970, pages 30 and
33–35. They are not conditions of the replaced fact. The worksheet already
applies them. Publication 970's 2025 phaseout band is $85,000 to $100,000
($170,000 to $200,000 for a joint return). The statute's unadjusted band in
section 221(b)(2) is the older $50,000 / $15,000 pair, indexed by section
221(f). Reconciling those dollar figures to a revenue procedure was not part
of this reading.

### Unverified

Not opened, so not cited for their own text:

- 26 U.S.C. § 25A(b)(3), § 25A(f)(2), and § 25A(g)(2), and the regulations
  under section 25A, including § 1.25A-2(b). The eligible-student sentence
  used above is the parenthetical in § 1.221-1(e)(3)(i)(B) and Publication
  970, page 31, not the text of section 25A.
- Section 472 and section 481 of the Higher Education Act of 1965, and any
  Department of Education half-time standard under that Act.
- Sections 152, 267(b), 707(b)(1), 72(p)(4), 72(p)(5), 108(f), 117, 127, 135,
  529, and 530, except where § 221 or § 1.221-1 restates a consequence.
- Publication 501.
- Any act that may have changed the effective-date sentence in
  § 1.221-1(a)(1) and (h).
- The citation record `tax.us.2025.citation.form1040.sli-worksheet`. The
  route map already said that citation text was not opened. It still has not
  been opened.

## 2. Basis table

The design that this table classifies is the one the owner approved on
2026-10-01, plus the two answer keys already stated in the Track 0b
evidence. Two ordinary answers are asked. The loan-cost answer is
`tax.us.2025.sli.loan-paid-only-school-costs`, keyed only by `borrowing`
(`tax.us.student-loan-borrowing-reference`). The enrollment answer is
`tax.us.2025.sli.enrolled-at-least-half-time`, keyed by `period`,
`institution`, and `programme`, the same three keys as the schooling
situation. Each allows `yes`, `no`, and `cannot-tell`. Only `yes` supports a
favorable result. The two links are the financing relationship and the
statement-inclusion relationship. The two counts are one current affirmed
financing for that borrowing, and one current affirmed inclusion on that
statement. The plain case deducts the whole box 1. Old and new inputs are
exclusive. There is no institutional catalog and no allocation.

The classes are the five the charter names. An adopted favorable assumption
is the A0 direction carried into this design: where no supported disqualifier
is recorded, the product may proceed on a default, and the record has to say
that the default is the basis. An assumption is not an answer the person
gave and not a conclusion the engine derived. An inspectable responsibility
is a condition the product keeps and does not establish. The favorable result
does not wait on a finding that the responsibility is satisfied.

| Condition | Class | What the design has |
| --- | --- | --- |
| The named statement includes interest on one identified borrowing. | Recorded ordinary fact | The person's inclusion answer, value `sli.statement-inclusion.affirmed`, for that statement and that borrowing. The link's own title does not assert a portion, exclusivity, or the whole statement. |
| That statement has exactly one current affirmed inclusion. | Rule conclusion | A count of the current affirmed inclusion rows for that statement. The count is derived from those rows. It is the design's stand-in for "no second recorded loan." |
| Box 1 contains no loan the person never recorded. The whole box 1 follows the one recorded loan. | Adopted favorable assumption | Owner decision: do not ask, and do not hunt. An unmentioned loan is invisible. The inclusion count does not see it. The product treats the whole box 1 as that one loan's interest. |
| That borrowing financed one identified schooling. | Recorded ordinary fact | The person's financing answer, value `sli.financing.affirmed`. The link's own title does not assert sole use, qualified expenses, or an amount. |
| That borrowing has exactly one current affirmed financing. | Rule conclusion | A count of the current affirmed financing rows for that borrowing. Two rows block. The count refuses a second schooling. It does not decide what two periods do to the interest. |
| The borrowing's proceeds paid only for school costs. | Recorded ordinary fact | `loan-paid-only-school-costs` = `yes` for that borrowing. The words are the person's. They are an ordinary use answer. |
| Those costs are qualified higher education expenses, after the required reductions for scholarships and other tax-free assistance. | Adopted favorable assumption | Nothing asks the cost-of-attendance list or those reductions. No disqualifier is recorded, so the product proceeds. The school-costs answer is not this conclusion. |
| The school is an eligible educational institution, and the cost of attendance is the figure that institution determines. | Inspectable responsibility | Kept, and not established. No catalog and no institutional lookup. The result does not contain a finding that either is true, and it does not block while they stay unestablished. |
| The expenses were for the taxpayer, a spouse, or a dependent, as of the time the loan was incurred. | Adopted favorable assumption | Not asked. A schooling recorded on this return is not that statement, and it does not fix the dependent test at the time of the loan. |
| The identified borrowing is indebtedness the taxpayer incurred. | Adopted favorable assumption | The person names a borrowing. Naming it does not establish that the taxpayer incurred the indebtedness. |
| The expenses fall within a reasonable period before or after the loan, including either safe harbor. | Adopted favorable assumption | Not asked. The schooling period key is an identifier. It is not a judgment that the period was reasonable, and neither the federal-program harbor nor the 90-day window is checked. Nothing adverse is recorded, so the product proceeds. |
| During that schooling, the student was enrolled at least half-time in a degree or certificate program. | Recorded ordinary fact | `enrolled-at-least-half-time` = `yes` for that period, institution, and programme. This is the person's answer to that sentence. |
| That enrollment meets the institution's half-time standard, and the program leads to a recognized educational credential. | Inspectable responsibility | The answer uses the words "at least half-time" and "degree or certificate." The standard is the institution's, and recognition of the credential is not established. A program that is only an "other recognized educational credential," and not a degree or a certificate, is outside the question. A yes does not cover it. |
| The loan is not owed to a related person. | Covered elsewhere | `tax.us.2025.f1098e.no-related-person-interest` stays an asked yes/no answer on the statement. |
| The loan is not under a qualified employer plan or a section 72(p)(5) contract. | Covered elsewhere | `tax.us.2025.f1098e.no-qualified-employer-plan-interest` stays an asked yes/no answer. The text of section 72(p) was not read. |
| The taxpayer is legally obligated to pay the interest. | Covered elsewhere | The worksheet's existing `legally-obligated-for-interest` answer. It is a condition of who may deduct the interest. It is not one of the three sub-questions folded into the replaced fact. |
| Employer educational assistance did not pay this interest, and qualified-tuition-program earnings were not used to pay it. | Covered elsewhere | `no-employer-educational-assistance-interest` and `no-qtp-earnings-used` stay asked. They bear on what paid the interest. They do not classify the loan. |
| The indebtedness was used solely to refinance a qualified education loan. | None of the five | The two questions do not ask it. The product does not assume a refinance qualifies. The plain-case result does not rest on refinance treatment. A person who answers that the proceeds paid only for school costs has made that use statement. The answer is not a conclusion that a refinance meets the flush language of section 221(d)(1). |

`no` or `cannot-tell` on either ordinary answer, or a missing answer, does
not support the favorable result. A missing answer is not the old fact's
`no`, and it is not the number 0.

The plain case still requires the schooling and the box 1 named by the links
to be current. That check is not classified here as a rule conclusion. Track
0b found that the derivation path does not call `current_claim_applicability`.
Track 0d owns that gap. This table does not treat a stale target as
favorable support, and it does not invent a derivation that has not run.

Filing status, the claimed-dependent rule, the income phaseout, and the
$2,500 cap stay on the worksheet. They are not rows of this replaced fact.

Read against the table, the two answers, two links, and two counts support a
favorable result only together with the assumptions and the responsibilities.
They do not establish every condition of a qualified education loan. Calling
that result `qualified` would say they do.

## 3. What the result says

The favorable value is `plain-case-supported`. The other value is
`not-supported`. The symbol proposed for the later fact is
`tax.us.2025.sli.statement-loan-support`, one row per box 1 statement.

`plain-case-supported` means all of the following hold for that statement:
exactly one current affirmed inclusion; the borrowing on that inclusion has
exactly one current affirmed financing; `loan-paid-only-school-costs` is
`yes` for that borrowing; and `enrolled-at-least-half-time` is `yes` for that
schooling. On that basis the worksheet may run its existing arithmetic on the
whole box 1, once the other four statement answers and the return-level gates
also pass. The value does not mean the loan is a qualified education loan
under section 221(d)(1).

`not-supported` means this statement is outside that case. It does not mean a
non-qualified loan is present. It is not the replaced fact's `no`, and it is
not zero.

The name `qualified`, and the symbol `qualified-loan-for-statement` from the
route map's section 6, claim the statutory conclusion. Section 2 does not
support that claim, so both are retired for this design. The route map's
sections 6, 7, and 8 are corrected to the new value in the same unit.

A reader of the result has to be able to see four groups. Pins of the inputs
can carry the first two, because those inputs exist. They cannot carry the
last two, because an assumption that was never asked and a responsibility
that was never established are not findings the rule read.

**Said.** The loan-cost answer `yes` for the named borrowing. The enrollment
answer `yes` for the named period, institution, and programme. The financing
affirmation naming that borrowing and that schooling. The inclusion
affirmation naming that statement and that borrowing.

**Derived.** The inclusion count is 1. The financing count is 1. Both are
counts of current rows, not answers the person gave. Currency of the schooling
and of the box 1 the links name is not in this list. Track 0d still owns that
check.

**Assumed, in the person's favor, with no answer recorded.** The expenses
fall in a reasonable period. The school costs stand in for qualified higher
education expenses, and no reduction is applied for scholarships or other
tax-free assistance. The schooling was for the taxpayer, a spouse, or a
dependent when the loan was incurred. The named borrowing is indebtedness the
taxpayer incurred. Box 1 holds no loan the person did not record, so the whole
box 1 is this loan's interest.

**Left with the person.** The institution is an eligible educational
institution. The enrollment meets that institution's half-time standard. The
program leads to a recognized educational credential. The cost of attendance
is the figure that institution determines. None of these is a finding, and
none is consumed as an input. The result names them so the person can see
they still apply to this statement's interest.

The stated basis is part of what the result says. Choosing a stored field for
it is later work. This paper does not add a schema. A value with no stated
basis would hide the assumptions inside `plain-case-supported`.

The result is not the deduction. The other four statement answers, the legal
obligation, the claimed-dependent rule, filing status, and the phaseout stay
in front of the arithmetic. If the old non-qualified-loan answer is also
current anywhere on the return, the worksheet blocks and does not use
`plain-case-supported`. A return with only the old answers never reads this
result. A refinance is not given this value by a separate rule. The
conditions that fit none of the five classes stay outside the favorable
result.
