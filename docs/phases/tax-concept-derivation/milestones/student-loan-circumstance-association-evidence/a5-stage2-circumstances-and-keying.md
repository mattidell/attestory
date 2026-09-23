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
| *(not an F9 circumstance)* A borrowing financed education this circumstance is about | The **pair** — that borrowing and that schooling situation | borrowing + period + institution + programme |

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
one. Where this stage needs an adverse account it states the ordinary circumstance that makes
it so — see the adverse variant below.

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
- **The financing claim** — *this borrowing paid qualified education expenses for that course
  of study.* Its subject is the **pair**. It is per borrowing, it is about origination, and it
  is the claim that can differ between two loans while the schooling does not.

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

**What an institution-keyed record would say:** *nine credits at Riverside.* Evaluated against
a normal full-time load of twelve, nine clears half, and the eligible-student constituent
publishes a favourable value. Per course of study, five of twelve and four of twelve clear
half in **neither**. The institution-keyed key does not merely lose precision; it produces the
favourable answer in a case the statute answers adversely.

**Why:** the workload clause is § 25A(b)(3)(**B**) — *"is carrying at least ½ the normal
full-time work load for the course of study the student is pursuing"*. It measures the load
against a standard belonging to a course of study. With two courses of study there is no single
standard for an institution total to be compared to, so the institution-level figure is not an
under-specified answer to the workload question — it is not an answer to it.

**Selected:** course load is keyed on period, institution and programme, the same grain as
enrolment, which is the grain § 25A(b)(3)(B) actually speaks at.

**And what an institution total means when that is all the filer said.** It means what it says
— nine credits at Riverside — and the workload constituent is **unresolved**, not favourable.
That is detectable rather than silent: the enrolment records at that institution and period
say there are two courses of study, so the condition for the total being evaluable fails
observably. It matters because the favourable value would otherwise arrive from F6's default
rather than from anything the filer said, which A0 requires be distinguishable.

**The adverse variant test 1 needs.** Add one ordinary circumstance to the Metro account: the
filer took those two classes **not as part of any programme leading to a degree, certificate
or other recognised credential** — an à la carte enrolment. That defeats the *other*
subparagraph, § 25A(b)(3)(**A**), which requires meeting HEA § 484(a)(1), and it does so before
any workload question arises, so the Metro situation
carries an adverse enrolment while Riverside's remains favourable. The adverse quality is
traced from what the filer was enrolled in. Nothing about the class schedule contributes to
it.

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
| **Circumstances represented** | Use of proceeds and whose education (filer-as-student), keyed on the borrowing; attendance keyed on period and institution; enrolment and course load keyed on period, institution and programme; and, joining them, a financing claim keyed on the borrowing together with a schooling situation. Who lent and the employer-plan circumstance are representable by the borrowing-keyed shape |
| **What the bounded consumer evaluates** | The schooling path only: whether a supported, enumerated adverse schooling circumstance defeats a constituent, and what that does to the interest on a statement |
| **Deferred** | Both § 221(e)(1) double-benefit conditions; the related-person and employer-plan constituents; origination dating for whose-education; a student other than the filer |
| **What the output does *not* establish** | That any deferred condition is **satisfied**. The consumer does not evaluate them, and not evaluating a condition is not a finding that it holds |

**That last row is the one that matters.** A figure this consumer publishes has not been
checked against employer-paid interest, against qualified-tuition-programme earnings, against
the related-person exclusion, or against the employer-plan exclusion. Absence of
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
- Whether a borrowing financed that schooling is a **separate record about the pair**, and it
  is the record that legitimately varies per borrowing.
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
| Use of proceeds; whose education; who lent; employer-plan borrowing | borrowing | Basis of each, and whether a default-supported value is distinguishable from a stated one |
| Attendance | period + institution | Same |
| Enrolment; course load | period + institution + programme | Same, plus the unresolved case from test 3: an institution total with two courses of study is not a favourable answer, and its basis must not read as one |
| A borrowing financed that schooling | borrowing + period + institution + programme | Whether the pair's own basis can differ from the basis of the circumstance it names — a well-grounded financing claim pointing at a default-supported enrolment, and the reverse |
| Legal obligation (a tax-concept fact, not an F9 row) | not selected here — stage 3's | — |

Stage 3 also inherits the question test 2 raised and did not answer: whether a correction to a
shared record reaching every dependent statement needs anything carried on the record itself,
or is entirely a matter of re-derivation. Stage 2 takes no position.

## Deferred, named not designed

Origination dating for whose-education. Whether a *scope claim* is keyed on a statement, and
what a correction to one reaches — stage 4 owns both, along with the lifecycle of a
route-(a) claim that names no borrowing.
