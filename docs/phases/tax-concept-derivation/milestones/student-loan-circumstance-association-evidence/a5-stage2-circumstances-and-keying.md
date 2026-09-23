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
| An employer paid interest under an educational assistance programme | A **payment** on a borrowing, in a tax year | borrowing + tax year |
| Qualified-tuition-programme earnings used to pay this interest | Same | borrowing + tax year |
| Attendance at an identified institution for an identified period | The **student's situation at a period** | borrowing + period |
| Enrolment in an identified programme | Same | borrowing + period |
| Course load for that period | Same | borrowing + period |

**None of these is keyed on a statement.** A statement is where an amount is reported; it is
not what any of these propositions is about. The incumbent keys its witnesses per statement,
and A0 records why that is wrong for at least the related-person case: relatedness is between
the taxpayer and the creditor on an indebtedness, and a statement may aggregate a
related-person loan with an unrelated one.

## The schooling circumstances need no second person's identity

Enrolment is about a student, and the student may be a spouse or a dependent rather than the
filer. That does **not** require modelling that person.

The selection: key the schooling circumstances on **borrowing plus period**. The borrowing
already carries whose education it financed — that is the second row of the table — so the
borrowing identifies which student's situation is being described without naming them. What
is needed is the information and its relation to the borrowing, not an identity.

This is the same move the deeming rule got: a rule turning on another person's relationship
to something does not require creating that person.

## A tension stage 1's routes create, named rather than dissolved

Stage 1 selected three scope routes, and route **(a)** asserts a circumstance over a whole
statement with **no borrowing identified**. But every circumstance above is keyed on a
borrowing. Those cannot both be satisfied by one shape.

Two ways out, and this stage does not choose:

- **The circumstance keys on its subject and route (a) is a separate claim.** The person's
  whole-statement assertion is a scope claim over that statement, and the circumstance it
  carries is still about a borrowing — an unidentified one. The scope claim is what attaches
  to the statement.
- **The circumstance's subject varies by route.** The same circumstance type keys on a
  borrowing where one is identified and on a statement where none is.

The first keeps one subject per proposition and adds a claim; the second keeps one claim and
admits two subjects. **Stage 4's lifecycle work decides it**, because the two differ in what a
correction reaches: correcting a circumstance about an unidentified borrowing, versus
correcting a statement-scoped claim, are not the same event.

## What this milestone's consumer depends on, and what it does not

The milestone connects schooling circumstances to reported interest. That fixes the boundary.

**Depended on:** use of proceeds, whose education, and the three schooling circumstances.
These are the path the bounded consumer exercises.

**Represented by the same shapes, not depended on here:** who lent the money, and borrowing
against an employer's plan. They defeat different constituents by the same mechanism, and
adding them would widen the consumer without testing anything the schooling path does not
already test.

**Not this milestone's, and deliberately not redesigned:** the two double-benefit
circumstances. They are § 221(e)(1) **amount** operations about what paid the interest, not
schooling circumstances, and the milestone's purpose does not reach them. The incumbent holds
them as per-statement categorical witnesses that block the whole route; this milestone neither
adopts them as dependencies nor changes them. Treating them as amount-bearing facts keyed on
borrowing and year remains available to a later milestone, and would need an amount nobody
collects today — which is A1's question and is not asked.

## Storage shape

**Provisional, and it follows the keys rather than preceding them.** A circumstance about a
borrowing and a circumstance about a borrowing at a period have different identities, so they
are separately addressable. Whether that means separate fact types, or one type keyed by
subject, is left to stage 3's basis work — a value's basis and its key are chosen together,
and choosing the shape first would prejudge that.

What is fixed: circumstances are **not** keyed on the statement their amount was reported on,
and correcting one must not silently rewrite another.

## Dependence on A4

| Depends on | Level |
| --- | --- |
| A consumer requiring a fact conditionally | `run` — D4 |
| Per-item dispatch resolving a named subject and refusing by name when it is gone | `run` — D1, D2 |
| **A rule expression reading a per-member value from `collect_categorical_all_equal`** | `read`, and the answer is **no** — D7. Any shape needing a per-member branch through that operator is barred |
| Telling "still resolvable" from "still supported" | **untested** — D9 |
| Holding A3's states apart | **untested** — D11 |

D7 matters here specifically: keying a circumstance on a borrowing rather than a statement
means a consumer may need to read a particular member's answer, and that operator cannot
supply one. Whether per-item dispatch covers it instead is D1's territory, and D1 is `run`
only for the dispatch path.

## Deferred, named not designed

Origination dating for whose-education. How a circumstance about an unidentified borrowing is
addressed at all — that is the tension above, and stage 4 owns it.
