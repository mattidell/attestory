# A5 stage 2 — representing the ordinary circumstances, and what they are keyed on

Provisional where it depends on stages 3 and 4. Filer-centered. No implementation.

## What each circumstance is actually about

The key follows the subject of the proposition, not the document it arrived with.

| A0 F9 circumstance | What the proposition is about | Provisional key |
| --- | --- | --- |
| What the borrowed money paid for, and whether only that | The **borrowing** | borrowing |
| Whose education it paid for | The **borrowing**, at origination | borrowing |
| Who lent the money | The **borrowing** — the creditor on that indebtedness | borrowing |
| Borrowing against an employer's plan | The **borrowing** | borrowing |
| An employer paid interest under an educational assistance programme | § 221(e)(1) **first sentence** — see below | **not selected** |
| Qualified-tuition-programme earnings used to pay this interest | § 221(e)(1) **second sentence**, a different object — see below | **not selected** |
| Attendance at an identified institution for an identified period | Attendance **at that institution** in that period | period + institution |
| Enrolment in an identified programme | Enrolment **in that programme** | period + institution + programme |
| Course load for that period | A load **in that course of study** in that period | period + institution + programme |
| *(not an F9 circumstance)* What the borrowed money paid for at an identified course of study — *"this loan paid my tuition and housing for the Riverside BSc that autumn"* | The **pair** — that borrowing and that schooling situation | borrowing + period + institution + programme |

**No borrowing appears in a schooling circumstance's key**, and the last row is why: the
connection to a borrowing is its own claim rather than part of the circumstance's identity.
The two sections below are the tests that forced that.

**None of these *circumstances* is about a statement.** A statement is where an amount is
reported; it is not what any of these propositions says. The incumbent keys its witnesses per
statement, and A0 records why that is wrong for at least the related-person case: relatedness
is between the taxpayer and the creditor on an indebtedness, and a statement may aggregate a
related-person loan with an unrelated one.

**That is not a ban on statement-scoped representation**, and an earlier version of this stage
came close to one. What a person says a circumstance *applies to* is a separate thing from what
the circumstance is about, and a statement is a perfectly good population to apply something
to. Whether some claim is keyed on a statement stays genuinely open — see the scope section
below.

## Test 1 — one borrowing, two schooling situations in one period

An earlier version of this stage keyed the schooling circumstances on **borrowing + period**
and assumed that pair picked out one account. It does not, and the case is ordinary.

**The case.** The filer takes one loan in autumn 2024. It pays for a degree programme at
Riverside College *and* for two individual classes at Metro Community College, both in that
same period. Two attendances, two enrolments, two loads — one borrowing, one period.

On a `borrowing + period` key, the second account collides with the first, and a
representation that displaces it would record the Metro records **as a correction of** the
Riverside ones. That is false in either direction and independently of which account is more
favourable: nobody corrected anything, and the two situations both obtain.

**The accommodation, and it is not an addition.** The propositions already name the missing
discriminators: attendance is *at an identified institution*, enrolment is *in an identified
programme*. Dropping those from the key was the same error as keying on a statement —
under-keying against what the proposition is actually about. Once the institution and the
programme are in the key the two situations are distinct, and — as test 2 shows — the
borrowing is then doing no work in the key at all.

**What this does not need:** no other-person identity, and no general model of education.
Only the identifiers the propositions already carry.

**What it does not license.** The Metro classes are not adverse because they are two classes,
or evening ones. A3 settled that: an irrelevant description of a schedule derives no canonical
circumstance, and reading one out of it manufactures an adverse circumstance from a neutral
one. Nor does this test need an adverse account at all: it is about two identities, not about
a favourable one and an unfavourable one. Where this stage does need an adverse account, it
traces one — see "the adverse case" below.

## Test 2 — two borrowings, one schooling situation, and a correction

**The case.** Autumn 2024, one course of study: the BSc at Riverside. Two borrowings finance
it — an institutional loan and a private one, two lenders, two 1098-Es. The filer first says
full-time, then corrects it: they withdrew from all but one class.

**On borrowing-keyed schooling facts there are two load records**, one under each borrowing,
and correcting one leaves the other saying full-time. Nothing in the representation says the
two were ever the same load, so nothing detects the disagreement: one statement's interest is
defeated and the other's is deducted, on the same schooling, in the same period, for the same
student.

**That is a state the world cannot be in.** The eligible-student test in § 25A(b)(3), which
§ 221(d)(3) adopts, is a fact about the student in an academic period. Two loans cannot
disagree about whether the filer carried half the normal full-time load at Riverside in autumn
2024. A representation that permits the disagreement is admitting states the subject matter
excludes — the same objection this stage raised against keying a relatedness circumstance on a
statement.

**The distinction the case forces.** Two different claims were being carried in one record:

- **The schooling circumstance** — *the filer was enrolled in the Riverside BSc in autumn 2024
  and carried this load.* Its subject is the course of study in that period. It has one truth
  value however many loans exist, and none if no loan exists.
- **The financing claim** — *this borrowing paid for that course of study*, in the ordinary
  terms a person would use: tuition, fees, housing, books, or simply "my studies there". Its
  subject is the **pair**. It is per borrowing, it is about origination, and it is the claim
  that can differ between two loans while the schooling does not.

**What the financing claim must not assert.** An earlier wording had the person saying the
borrowing paid *qualified education expenses*. That is a conclusion, not an ordinary telling:
qualified higher education expenses are defined at § 221(d)(2) as the cost of attendance under
HEA § 472 at an eligible educational institution, reduced by the amounts § 221(d)(2)(A) and
(B) name. Whether what the filer describes meets that definition is the rule's to reach, and
putting it in the person's mouth would repeat the defect A0 names for F5 — a composite
presented as something a person can be asked. The filer says what the money went to. The rule
says whether those are qualified.

This is the per-situation form of F9's existing use-of-proceeds row, not a rival to it. The
borrowing-level row keeps the part that is about the whole borrowing — **whether the proceeds
went *solely* to such expenses**, which § 221(d)(1) requires of the indebtedness and which no
single situation can answer.

**Selected: the smallest representation that keeps them apart.** The circumstance is keyed on
the schooling situation and nothing else; the financing claim is a separate record keyed on
the borrowing together with that situation. Two borrowings financing one course of study are
two financing claims naming **one** circumstance record.

**Correction behaviour.** A correction to enrolment or load edits the one record its key
addresses. Both borrowings' financing claims name that record, so both use the corrected
value on the next derivation, and there is no second copy to reconcile or leave stale. The
contradictory state above is not merely detected — it is unrepresentable.

**Two smaller-looking alternatives, and why neither is taken.**

*Keep the duplicate records and propagate a correction to every copy of the same load.* To do
that the engine must recognise two records as the same load, which means computing the very
identity — period, institution, programme — this selection names. Reconstructing an identity
implicitly to repair the consequences of having left it out is larger, not smaller, and it is
larger in the part that is easy to get wrong.

*Make the financing claim one record per borrowing whose value is the **set** of situations
that borrowing financed.* This is genuinely fewer records than one per pair, and it does keep
the circumstance separate, so it is a real alternative rather than a straw one. Two reasons it
is not selected, the second decisive:

- A set loses independent grounds and independent correction per situation. "This borrowing
  financed the BSc" and "this borrowing financed the certificate" then cannot be supported,
  corrected or refused separately, and stage 1's route (b) — a *known portion* concerning an
  identified borrowing — is exactly where they need to be.
- **No demonstrated consumer can reach a member.** D7 is `read` and negative for
  `collect_categorical_all_equal`, which returns one Boolean; the one per-item mechanism A4
  marks `run` is pairing dispatch, and it resolves a single pinned `left_fact_id` and
  `right_fact_id` per record — the pair *is* the record. D7's cell is careful that this limits
  what an expression reads rather than what a record may keep, so the set-valued form is not
  impossible; it is undemonstrated, and selecting it would rest this stage on a behaviour A4
  has not seen. The per-pair record is the shape the demonstrated mechanism already has.

**What this does not settle, and it is the one that stays owed.** A single shared record
removes the inconsistent copies. It does not by itself establish that correcting it *reaches*
every statement whose figure depended on it — that is `a4-bounds.md`'s first owed row, which
D8 does not demonstrate, and this selection makes it the milestone's central owed behaviour
rather than a peripheral one. G2 is where it is seen.

**Route (a) is unaffected.** A whole-statement scope claim names no borrowing, so it has no
financing claim; the circumstance it applies is still keyed on its own situation. Stage 1's
routes concern what a *reported amount* covers, and the borrowing named in (b) and (c) is the
one whose financing claim carries the schooling. Two relations, deliberately not merged.

## Test 3 — two programmes at one institution, and what a recorded load means

The previous key for course load named the institution and not the programme, while the
workload test is about the course of study. That gap is not cosmetic.

**The case.** Autumn 2024 at Riverside. The filer is enrolled in a BSc *and* in a separate
certificate programme, and takes five credits in the first and four in the second. Riverside's
normal full-time load is twelve credits for each.

**Withdrawn: that the statute answers this case adversely.** An earlier version compared nine
credits to a twelve-credit standard, found it clears half, compared five and four to the same
standard, found neither does, and concluded the institution-level key produces a favourable
answer where the statute is adverse. That conclusion is not established, for two reasons.

- **Whether credits in a second programme count toward the first programme's standard is the
  institution's determination**, and nothing traced here settles it. A school may well certify
  a student's enrolment status on their total registration. A0 already places the half-time
  standard among the conditions the person is responsible for, which the application does not
  establish and no calculation consumes — so the application is in no position to run the
  comparison either way.
- **No course-load telling produces a favourable value in the first place.** A0's R6a supports
  an adverse determination and nothing favourable; the favourable eligible-student value comes
  from the **default**, on a default-supported basis. So the coarse record cannot "produce the
  favourable answer" — that answer arrives the same way at either grain.

**What the case does show, which is the reason to keep it.** § 25A(b)(3)(**B**) — *"is carrying
at least ½ the normal full-time work load for the course of study the student is pursuing"* —
attaches the standard to a course of study. An adverse telling therefore has a course of study
as its subject: *"I dropped below half-time in the BSc."* A school-wide total has no course of
study to attach to, so it loses the very subject an adverse telling needs. That is an
information loss about **what can be said**, not a determination about what is true.

**Selected:** course load is keyed on period, institution and programme, the same grain as
enrolment, because that is the grain at which the person's account can be adverse at all.

**And what a combined total means when that is all the filer said — reconciled with A0 and
A3.** It means what it says: nine credits at Riverside. It supports no adverse determination
about the work load in either course of study, and an earlier version of this section then
called the constituent **unresolved**, which was wrong and is withdrawn. A3 is explicit that no
adverse information and adverse information of unresolved scope are opposite in consequence,
and that the first is the normal condition of every return: **the consumer proceeds.** Holding
the calculation on a combined total would manufacture an adverse circumstance out of an
absence — the same error as reading adversity out of a class schedule.

So the calculation proceeds, on F6's default, and what the grain protects is the **basis**: the
favourable value must record that it came from the default and not from the filer's nine-credit
telling, which said nothing either way about the § 25A(b)(3)(B) standard.

**What would justify holding it** is supported adverse information, and only that: the filer
saying they were below half-time in the course of study they were pursuing, or an adverse
account of enrolment for the period of the kind traced below. A combined total is neither.

## The adverse case, and one that was withdrawn

**Withdrawn: the à la carte Metro enrolment as an adverse account.** An earlier version added
one circumstance to test 1 — that the Metro classes led to no degree, certificate or other
recognised credential — and concluded that the Metro situation was adverse while Riverside's
was not. Tracing it does not support that conclusion.

§ 221(d)(1)(C) requires the expenses to be attributable to education furnished during **a
period during which the recipient was an eligible student**. § 221(d)(3) sends "eligible
student" to § 25A(b)(3), which is a status of *the student in that period*: (A) meeting HEA
§ 484(a)(1), and (B) carrying at least half the normal full-time work load for the course of
study pursued. In test 1 the filer is enrolled in the Riverside degree programme in that same
autumn. Whatever the Metro classes are, the person was an eligible student during the period,
so (C) is not defeated for education furnished in it. Nothing traced establishes that a
second, non-credential enrolment subtracts from a status the first one confers.

**A keying consequence worth carrying, and it is what the test actually found.** Eligible
student is keyed on **the student and the period** — the circumstances that feed it are per
course of study, but the status they feed is not. Test 1 therefore stands as what it was
before the variant was bolted on: two schooling situations in one period keep **separate
identities**, and neither is a correction of the other. It is a cardinality test, and it does
not need an adverse party.

**The adverse case, traced.** Take a different period. In spring 2025 the loan pays for a
short Metro course, and in that term the filer is enrolled in no programme leading to a
degree, certificate or other recognised credential — at Metro or anywhere else — and carries
no qualifying work load. Now § 25A(b)(3)(A) fails through HEA § 484(a)(1) with nothing else in
the period to confer the status, so the recipient was not an eligible student during the
period that education was furnished, and § 221(d)(1)(C) fails for expenses attributable to it.

That is the shape A0's R6a accepts: an ordinary account of one's schooling that supports an
**adverse** determination. It is adverse because of what the person was enrolled in across the
whole period, not because of what any one class was.

## Whose education does not identify a unique student, and this milestone's student is the filer

A second assumption is withdrawn. I wrote that the borrowing carries whose education it
financed and therefore identifies which student's situation is described. It does not:
§ 221(d)(1)(A) admits expenses for the taxpayer, a spouse, **or any dependent**, and one
borrowing may have paid expenses for more than one of them.

**This milestone's scope is the filer as the student.** That is where the bounded consumer
works, and keying the schooling circumstances on the borrowing, period, institution and
programme is sufficient there. The broader possibilities — a spouse's or a dependent's
education — are in A0's domain model as facts of the matter and are **not represented here**,
which is a scope bound and not a claim that they do not arise.

Filer-as-student is also what keeps the earlier point true in its narrow form: no second
person's identity is needed, because within this scope there is no second person.

**How that row and the financing claim differ**, since both are per borrowing and about
origination. Whose-education carries *which person* the expenses were for; the financing claim
carries *which course of study* they were for. In this milestone's scope the first is constant
— the filer — which is exactly why the second has to be recorded separately rather than read
off it. A later milestone widening the student would give the first row work to do; it would
not remove the second.

## Whole-statement scope, without a placeholder borrowing

Route (a) — *"this applies to everything on this statement"* — needs no borrowing, and an
earlier version of this stage mis-described it as a circumstance about **one unidentified
borrowing**. It is not. Such a statement may cover several borrowings while naming none of
them, and inventing a singular subject to hold it would be exactly the "make reality fit the
identifier" move this stage exists to avoid.

**What separates cleanly:** what the circumstance *says* — a proposition with its own subject
— and the **population or portion** the person says it applies to. Route (a) supplies the
second without the first being individuated. The circumstance is what it is; the scope claim
says it reaches everything this statement reports.

So no placeholder borrowing, and no requirement that route (a) resolve to one. **Whether the
scope claim is itself keyed on the statement is left open** — it is the natural reading, and
stage 4 settles it alongside the lifecycle question of what a correction to such a claim
reaches, which differs from what a correction to a circumstance reaches.

## What this milestone's consumer depends on, and what it does not

The milestone connects schooling circumstances to reported interest. That fixes the boundary.

**Depended on:** use of proceeds, whose education, and the three schooling circumstances.
These are the path the bounded consumer exercises.

**Represented by the same shapes, not depended on here:** who lent the money, and borrowing
against an employer's plan. **Not because they would test nothing new** — each defeats a
different constituent and each would be worth exercising eventually. They are simply not
needed for the selected demonstration, which is the schooling path, and including them would
widen the consumer past what this milestone set out to show.

**Not this milestone's, and deliberately not redesigned:** the two double-benefit
circumstances. They are § 221(e)(1) amount operations about what paid the interest, not
schooling circumstances, and the milestone's purpose does not reach them.

**They are also two different objects, and an earlier version of this stage keyed them as one.**
That compression is a defect our own authority record already identified and corrected, and it
was reintroduced here by writing "same" against the second row:

- **Employer-paid interest — § 221(e)(1) first sentence.** An *amount* for which a § 127
  exclusion is allowable, by reason of the employer's payment of indebtedness on a qualified
  education loan of the taxpayer. The employer's payment is the *reason*, not the identity of
  the fact. Not a classification of the borrowing, and not a statement. **Key not selected.**
- **Qualified-tuition-programme earnings — § 221(e)(1) second sentence.** A reduction, for the
  taxable year, of the deduction otherwise allowable under § 221(a) before § 221(b), by the
  earnings on § 529(c)(9) distributions with respect to **loans** of the taxpayer. One
  year-level amount measured across loans, not a payment on one borrowing. **Key not
  selected.**

This milestone adopts neither as a dependency and changes neither incumbent per-statement
witness. A later milestone may treat either as an amount fact. **That key is not chosen here,
and borrowing-plus-year is not a default it inherits** — withdrawing the statement key was
right, and putting both sentences on the borrowing was not.

## The boundary, stated in one place

The plan gives this stage the double-benefit rows and asks it to select their handling. It has:
**no key is selected and neither is adopted as a dependency.** Stated as four things so the
deferral does not read as something else.

| | |
| --- | --- |
| **Circumstances represented** | Use of proceeds and whose education (filer-as-student), keyed on the borrowing; attendance keyed on period and institution; enrolment and course load keyed on period, institution and programme; and, joining them, a financing claim — what the money paid for, in ordinary terms — keyed on the borrowing together with a schooling situation. Who lent and the employer-plan circumstance are representable by the borrowing-keyed shape |
| **What the bounded consumer evaluates** | The schooling path only: whether a supported, enumerated adverse schooling circumstance defeats a constituent, and what that does to the interest on a statement |
| **Deferred** | Both § 221(e)(1) double-benefit conditions; the related-person and employer-plan constituents; legal obligation, whose key stage 3 selects but which nothing here consumes; what the filer paid, which stage 5 specifies and nothing here consumes; origination dating for whose-education; a student other than the filer |
| **What the output does *not* establish** | That any deferred condition is **satisfied**. The consumer does not evaluate them, and not evaluating a condition is not a finding that it holds |

**That last row is the one that matters.** A figure this consumer publishes has not been
checked against employer-paid interest, against qualified-tuition-programme earnings, against
the related-person exclusion, against the employer-plan exclusion, against legal obligation
on any particular loan, or against whether anyone other than the filer paid the reported
interest. Absence of
implementation must never read as a determination — which is the same discipline A0 applies to
a default-supported value, and the same reason the responsibility category exists.

Deferral here creates no production dependency and commissions no broader tax implementation.
It does oblige whatever consumes this output to carry the limit with it.

## Storage shape

**Provisional, and it follows the keys rather than preceding them.** A circumstance about a
borrowing, a circumstance about a schooling situation, and a claim about the pair have three
different identities, so they are separately addressable. Whether that means separate fact
types, or one type keyed by subject, is left to stage 3's basis work — a value's basis and its
key are chosen together, and choosing the shape first would prejudge that.

What is fixed by the three tests:

- A *circumstance* is not keyed on the statement its amount was reported on, because that is
  not what a circumstance is about.
- A *schooling* circumstance is not keyed on a borrowing either, because it is about a course
  of study in a period and would otherwise exist in as many copies as there are loans.
- What a borrowing paid for at a particular course of study is a **separate record about the
  pair**, stated in ordinary terms, and it is the record that legitimately varies per
  borrowing. Whether those payments were *qualified* expenses is not part of it.
- Correcting a circumstance must not silently rewrite another, and must not leave a second copy
  of the same circumstance saying something else.

What is **not** fixed is whether a *scope claim* is keyed on a statement — that stays open for
stage 4.

## Dependence on A4

| Depends on | Level |
| --- | --- |
| A consumer requiring a fact conditionally | `run` — D4 |
| Per-item dispatch resolving a named subject and refusing by name when it is gone | `run` — D1, D2 |
| **A rule expression reading a per-member value from `collect_categorical_all_equal`** | `read`, and the answer is **no** — D7. Any shape needing a per-member branch through that operator is barred |
| Telling "still resolvable" from "still supported" | **untested** — D9 |
| Holding A3's states apart | **untested** — D11 |

| **One corrected schooling circumstance reaching every statement its financing claims bear on** | **untested** — `a4-bounds.md`'s first owed row. D8 corrects one nominee report and checks the current finding is used; it exercises no shared subject reached from several statements. Test 2's selection makes this the milestone's central owed behaviour |

D7 matters here specifically: keying a circumstance away from the statement means a consumer
may need to read a particular member's answer, and that operator cannot supply one. Whether
per-item dispatch covers it instead is D1's territory, and D1 is `run` only for the dispatch
path — and the path now has two hops, borrowing to schooling situation, where the demonstrated
dispatch has one. That second hop is part of what G2 has to see.

## Handoff to stage 3

What stage 3 receives as selected, and must give a basis to:

| Record | Key | Stage 3 owes |
| --- | --- | --- |
| Use of proceeds — including whether the proceeds went *solely* to such expenses; whose education; who lent; employer-plan borrowing | borrowing | Basis of each, and whether a default-supported value is distinguishable from a stated one |
| Attendance | period + institution | Same |
| Enrolment; course load | period + institution + programme | Same, plus test 3's case: where only a combined institution total is known, nothing adverse is supported, the calculation **proceeds on F6's default**, and the basis must record that the value came from the default rather than from the total the filer gave |
| What the borrowed money paid for at an identified course of study | borrowing + period + institution + programme | Whether the pair's own basis can differ from the basis of the circumstance it names — a well-grounded financing claim pointing at a default-supported enrolment, and the reverse |
| Legal obligation (a tax-concept fact, not an F9 row) | not selected here — stage 3's | — |

**The ordinary/derived boundary this table must hold**, which is the distinction test 2's
repair turned on. The filer's record says what the money paid for. Three further things are
the rule's to reach, each with its own basis and none of them assertable by the person:

| Derived, not told | Reached from | Authority |
| --- | --- | --- |
| That what the money paid for were **qualified higher education expenses** | The financing claim, plus what the expenses were | § 221(d)(2) → HEA § 472, less § 221(d)(2)(A) and (B) |
| That the recipient was an **eligible student** during the period the education was furnished | The period's schooling circumstances, taken together across situations | § 221(d)(1)(C) → § 221(d)(3) → § 25A(b)(3) |
| That the indebtedness was incurred **solely** to pay such expenses | The borrowing-level use-of-proceeds row, not any single situation | § 221(d)(1), flush language |

The second row carries test 1's finding and stage 3 should not lose it: the **circumstances**
are keyed per course of study, but the **status** they feed is keyed on the student and the
period. A second enrolment in a period does not subtract from a status another enrolment in
that period confers, and a representation that keyed the status per situation would let it.

Stage 3 also inherits the question test 2 raised and did not answer: whether a correction to a
shared record reaching every dependent statement needs anything carried on the record itself,
or is entirely a matter of re-derivation. Stage 2 takes no position.

## Deferred, named not designed

Origination dating for whose-education. Whether a *scope claim* is keyed on a statement, and
what a correction to one reaches — stage 4 owns both, along with the lifecycle of a
route-(a) claim that names no borrowing.
