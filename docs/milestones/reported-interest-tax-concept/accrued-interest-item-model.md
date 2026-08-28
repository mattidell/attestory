# One Interest Item, Five Propositions

## What this document establishes

A taxpayer buys a bond partway through an interest period and pays the seller
for the interest that had already accrued. At the next coupon date the issuer
pays the whole period's interest to the new owner, and the payer's Form
1099-INT reports the whole amount to that new owner.

The reported amount is right. The taxpayer's income is smaller.

This document separates the propositions that produce that outcome, names the
official source behind each, and says which layer each belongs to. It covers
US-federal individual income tax for 2025 and one obligation whose interest is
payable periodically in arrears. It establishes nothing about any other
interest category.

## The five propositions

The whole point of the exercise is that these are five different assertions,
about four different subjects, resting on four different kinds of support.
Collapsing any adjacent pair produces a model that computes the right number
for the wrong reason.

### P1 — What the statement reports

> Logical Form 1099-INT statement S, furnished by payer P for tax year 2025,
> reports $1,200 in box 1.

Subject: the statement. Support: the statement itself. This proposition is
true whatever the taxpayer's tax position turns out to be, and it stays true
after every subsequent step. Nothing downstream may rewrite it.

### P2 — What happened

> On 2025-05-15 the taxpayer purchased obligation B and paid the seller $300
> for interest that had accrued on B before that date.

Subject: the taxpayer's purchase. Support: the taxpayer's own knowledge of
their transaction, corroborable by a trade confirmation.

This is an ordinary fact about a purchase. It is not a tax classification, and
the taxpayer can answer it without knowing any tax law: *did you buy a bond
between its interest payment dates, and did you pay the seller for interest
that had built up before you bought it?*

**No box on any Form 1099-INT reports this.** Payer P has no way to know it and
no obligation to report it. A model that can only ingest what a payer reports
cannot obtain P2 at all.

### P3 — What the law makes of it

> Interest that had accrued before the purchase is not the purchaser's income
> when it is subsequently paid to them; it is a return of the purchaser's
> capital investment and reduces their basis in the obligation.

Subject: the relation between P1 and P2.

The statutory frame is **IRC § 61(a)(4)**, which places interest in gross
income. § 61 is what makes the default answer *includible*, so something must
displace it.

What displaces it, for this exact fact pattern, is weaker than one might
expect, and the nearby authorities that look like they govern do not. The
distinctions below are load-bearing.

**Treasury Regulation § 1.61-7(d)** covers sales between interest dates and
addresses only the seller: *"When bonds are sold between interest dates, part
of the sales price represents interest accrued to the date of the sale and must
be reported as interest income."* It says nothing about the purchaser.

**Treasury Regulation § 1.61-7(c)** is the nearest regulation that speaks to a
purchaser, and it is a different transaction. It is headed *"Obligations bought
at a discount; bonds bought when interest defaulted or accrued,"* and its
operative sentence concerns *"any interest which is in arrears but has accrued
at the time of purchase."* That is the **traded-flat** pattern: a bond in
default or with unpaid accrued interest, bought at a discount, where the
overdue interest is embedded in the price. Publication 550 treats it under its
own heading, *"Bonds Traded Flat."*

Our taxpayer's purchase is the opposite economics. The bond is current, and the
buyer pays the seller a **separate** accrued-interest component on top of the
price. Reading § 1.61-7(c) onto that transaction stretches it, and the stretch
is easy to make because both patterns end in the same words — return of
capital, reduced basis.

The authority actually on point is **IRS Publication 550**, under *"Bonds Sold
Between Interest Dates"*: where a buyer purchases a bond between interest
payment dates and part of the purchase price represents interest accrued before
the purchase, that interest, when paid to the buyer, is *"a return of your
capital investment, rather than interest income,"* reducing basis in the bond.
The **Instructions for Schedule B (Form 1040)** state the income half more
briefly: the accrued interest is taxable to the seller, *not you*.

**This is a finding about the strength of the authority, not only its
location.** For the ordinary between-interest-dates purchaser, there appears to
be no regulation directly on point. The best available support is an IRS
publication, corroborated by a form instruction and by the seller-side
regulation — which establishes that the amount is *someone else's* income, and
so cannot also be this taxpayer's. That is adequate support for a modeled
method, and it is a materially different kind of support from a statute or a
regulation. A model that records where its propositions come from should be
able to show that difference rather than flatten it.

Note that P3 has **two** consequences, not one. The amount is not income, *and*
it reduces basis in the obligation. The second consequence is dormant this year
and material in the year the obligation is sold or redeemed.

### P4 — Where the subtraction is disclosed

> Report the full box-1 amount on Schedule B, Part I, line 1. Under the last
> line-1 entry, enter a subtotal; below the subtotal, identify the amount to be
> subtracted as "Accrued Interest"; subtract it and enter the result on line 2.

Subject: the return document. Support: **Instructions for Schedule B (Form
1040), line 1**, which direct the taxpayer to follow the mechanics given under
*Nominees* and to *"identify the amount to be subtracted as 'Accrued
Interest.'"*

The same instructions state that *"When you buy bonds between interest payment
dates and pay accrued interest to the seller, this interest is taxable to the
seller."*

How much substance that carries is worth being exact about, because it is easy
to dismiss too quickly. Line 1 of the same instructions directs the taxpayer to
report *"all of your taxable interest"* there. Directing the **buyer** to then
subtract this amount from that total is not layout advice; operationally it
says the amount is not the buyer's taxable interest. The instructions do
establish the **income half** of P3.

What they do not establish is the other half. They never say the payment is a
return of capital and never mention basis. A taxpayer who followed the
instructions exactly would file a correct return this year and would have no
record of the basis reduction that matters when the bond is sold.

So the layers separate on a narrower seam than "mechanics versus substance."
The reporting instruction is sufficient authority for the disclosure mechanics
*and* for the current-year income conclusion. It is not sufficient for the
complete proposition, and it is not the source that explains **why** the
subtraction is right — only that it is required.

### P5 — What the return says

> Form 1040 line 2b is $900.

Subject: the return line. Support: P4 applied to the result of P3, plus the
correspondence between the concept the line names and the concept computed.

P5 is a *projection*. It asserts that the amount belongs in that position on
that form. It does not define what taxable interest is, and if P3 were absent
the line would be wrong no matter how faithfully P4 were followed.

## The determination the propositions imply

Between P1 and P5 sits a conclusion that none of the five propositions is:

> Of the $1,200 that statement S reports for 2025, $900 is includible in the
> taxpayer's gross income as interest; $300 is not includible, and reduces the
> taxpayer's basis in obligation B.

This is the item-level tax determination. It is about **one item**, it names
both amounts, and it carries the reason. Its identity is the taxpayer, the tax
year, the jurisdiction, the regime, and the item — not the form on which the
result is later disclosed.

Setting it out this way describes the content of the conclusion. It does not
establish that the conclusion must be represented as a single recoverable
object; the cases built for this milestone do not show that, and the README says
so. What the table does establish is the **constituent list** — anything that
claims to carry this conclusion has to carry these parts, in whatever shape.

Its constituents:

| | |
| --- | --- |
| Subject | The return subject (taxpayer) |
| Period | Tax year 2025 |
| Jurisdiction | US-federal |
| Regime | Individual income tax |
| Quantity | A money amount in US dollars |
| Reported amount | $1,200, from P1, unmodified |
| Includible amount | $900 |
| Non-includible amount | $300, with its basis consequence |
| Operative facts | P1 and P2 |
| Authority | Pub. 550, *Bonds Sold Between Interest Dates*, and the Schedule B line-1 instructions, against IRC § 61(a)(4); Treas. Reg. § 1.61-7(d) for the seller's side |
| Reporting consumer | Schedule B Part I; Form 1040 line 2b |

## What this model does not establish

The declared coverage of this account is **one** obligation, purchased between
interest dates, whose interest is payable periodically in arrears, held
directly by one person, with no election in force.

It says nothing about original issue discount, market discount, bond premium
amortization, savings-bond education exclusion, nominee ownership, previously
reported interest, tax-exempt interest, or any interest not reported in box 1
of a Form 1099-INT. Those are not "not yet done"; they are outside what these
sources were read to support.

The basis consequence in P3 is **stated but not modeled** here. Naming it is
necessary because a model that carries only the income half of the regulation's
proposition has silently discarded the other half, and the discard is
undetectable in the year it happens.

Two conditions are genuine dependencies and are stated rather than modeled.

The obligation must pay interest periodically in arrears, and the accrued
amount must have been paid to the seller as a separate component of the
purchase. An obligation that does not work this way is outside this account.

The bond must be **current**, not in default and not carrying overdue unpaid
interest. That neighbouring pattern — a bond traded flat, bought at a discount
with the arrears embedded in the price — reaches the same words about return of
capital by a different route and under different authority (Treas. Reg.
§ 1.61-7(c); Pub. 550, *Bonds Traded Flat*). It is not covered here, and the
resemblance between the two is close enough that treating one account as
covering both would be a mistake.
