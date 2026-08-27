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

> Interest that had accrued at the time of purchase is not the purchaser's
> income when it is subsequently paid to them; such payments are returns of
> capital that reduce the purchaser's remaining cost basis.

Subject: the relation between P1 and P2. Support: **Treasury Regulation
§ 1.61-7(c)**, headed *"Obligations bought at a discount; bonds bought when
interest defaulted or accrued."* The paragraph opens *"If a taxpayer purchases
bonds when interest has been defaulted or when the interest has accrued but has
not been paid,"* and provides that *"any interest which is in arrears but has
accrued at the time of purchase is not income and is not taxable as interest
if subsequently paid. Such payments are returns of capital which reduce the
remaining cost basis."*

The statutory frame is IRC § 61(a)(4), which places interest in gross income.
§ 61 is what makes the default answer *includible*; § 1.61-7(c) is what
displaces the default for this amount. Neither alone is sufficient: the statute
without the regulation gets the wrong answer, and the regulation without the
statute has nothing to displace.

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

That sentence is worth reading carefully, because it is the closest the form
instructions come to substance and it still falls short of P3. It asserts a
fact about **the seller's** tax position. It does not say the amount is not
income to the buyer, it does not say the payment is a return of capital, and it
says nothing about basis. The reporting instruction is a legitimate and
sufficient authority for the disclosure mechanics of P4. It is not a sufficient
authority for P3.

That asymmetry is the point of separating the two layers. A model that cites
the Schedule B instructions for the subtraction has cited an authority that
does not establish the subtraction is required — only where to write it down.

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
| Authority | Treas. Reg. § 1.61-7(c), against IRC § 61(a)(4) |
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

One condition is a genuine dependency and is stated rather than modeled: the
treatment described assumes the interest in question had accrued and was unpaid
at the time of purchase. An obligation that does not pay interest periodically
in arrears is outside this account.
