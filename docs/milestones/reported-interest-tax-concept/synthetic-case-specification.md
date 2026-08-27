# Six Cases, One Reported Amount

## Purpose and reading

Six synthetic cases hold the source report constant and vary everything else.
Their job is to make visible which distinctions a model must carry, by finding
places where two situations that must produce different results are
indistinguishable to the model.

All identities are demonstration identities and all amounts are obviously
synthetic. Nothing here is a real taxpayer, payer, obligation, or transaction.

The propositions P1–P5 and the item-level determination are defined in
[accrued-interest-item-model.md](accrued-interest-item-model.md). The incumbent
artifacts referred to are described in
[incumbent-representation.md](incumbent-representation.md).

## Common fixture

| | |
| --- | --- |
| Subject | `demo.subject.filer-1` |
| Jurisdiction and regime | US-federal individual income tax |
| Period | Tax year 2025 |
| Payer | `demo.payer.harbor-bank` |
| Logical statement | `demo.stmt.1099int.harbor-2025-a` |
| Box 1 reported amount | $1,200 |
| Obligation (where relevant) | `demo.obligation.orchard-note-2031`, interest payable periodically in arrears |
| Purchase (where relevant) | 2025-05-15, accrued interest paid to seller $300 |

Every case below holds P1 — *statement `harbor-2025-a` reports $1,200 in box 1*
— unchanged unless the case is explicitly about correcting it.

## TI-B1 — Ordinary reported interest

**Facts entering.** P1 only. The taxpayer did not acquire the obligation
partway through an interest period, so P2 is absent rather than unknown.

**Who supplies what.** The statement supplies P1. The taxpayer supplies the
answer *no* to the ordinary purchase question.

**Rule and authority.** IRC § 61(a)(4) places the interest in gross income. No
displacing provision applies.

**Determination.** Of the $1,200 reported, $1,200 is includible. Reported and
includible coincide, and the case records *why* they coincide — no accrued
interest was purchased — rather than leaving the coincidence unexplained.

**Reporting consumer.** Schedule B Part I line 1 and line 2; Form 1040 line 2b
= $1,200.

**What the case establishes.** That equality of the reported and includible
amounts is a *result*, not an assumption. A model that cannot produce TI-B1 and
TI-B2 as different determinations is treating this equality as a definition.

**Incumbent behaviour.** Correct number. The equality is unexplained, because
nothing represents the absent circumstance; the accrued-interest family is
simply closed with no members.

## TI-B2 — The accrued-interest contrast

**Facts entering.** P1 and P2.

**Who supplies what.** The statement supplies P1: $1,200. The taxpayer supplies
P2: *on 2025-05-15 I bought `orchard-note-2031` and paid the seller $300 for
interest that had accrued before I bought it.* No payer reports P2.

**Rule and authority.** Treas. Reg. § 1.61-7(c) displaces the § 61(a)(4)
default for the accrued portion: it is not income, and it reduces basis.

**Determination.** Of the $1,200 reported, $900 is includible; $300 is not
includible and reduces the taxpayer's basis in `orchard-note-2031`.

**Reporting consumer.** Schedule B Part I: $1,200 on line 1, subtotal, then
"Accrued Interest" $300 subtracted, $900 to line 2. Form 1040 line 2b = $900.

**What the case establishes.** The statement still says $1,200 and the return
still says $900, and both are true at once. The determination is the thing
that holds them together, and it is separately recoverable from either.

**Incumbent behaviour.** Correct number, by a different route: a Schedule B
adjustment instance of $300 exists and is subtracted at the aggregate. The
obligation, the purchase date, the seller, the regulation, and the basis
consequence are all absent. Critically, **the incumbent cannot be given P2**.
It can only be given the already-classified figure "$300 of accrued-interest
adjustment," which is the output of the classification, not its input.

## TI-N1 — The circumstance is material and unanswered

**Facts entering.** P1. The taxpayer has confirmed that they bought an
obligation partway through an interest period, but has not yet supplied the
amount paid to the seller.

**Who supplies what.** The taxpayer has answered the ordinary question *yes*
and has not answered the follow-up.

**Required behaviour.** No determination is produced for that item. The product
does not fall back to $1,200 and does not guess $0. It states the outstanding
ordinary question — *how much did you pay the seller for interest accrued
before your purchase?* — and continues to report P1 unchanged.

**What the case establishes.** The difference between a gap that blocks and a
gap that silently resolves to one branch. Both produce no visible complaint;
only one produces a wrong answer.

**Incumbent behaviour.** The state is not representable. The incumbent's only
relevant question is whether the "Accrued Interest adjustment class" is closed,
which the taxpayer must answer in Schedule B vocabulary. A taxpayer who does
not recognise the category answers *closed, with no members*, and the model
silently takes the $1,200 branch with no indication that a branch was taken.
This is the case the incumbent fails outright.

## TI-L1 — The source report is corrected

**Facts entering.** TI-B2, then payer `demo.payer.harbor-bank` furnishes a
corrected Form 1099-INT for the same logical statement showing $1,000 in box 1.
P2 is unchanged.

**Required behaviour.** P1 supersedes: the statement now reports $1,000, and
the prior reported figure is superseded rather than deleted. The prior
determination is no longer current. The circumstance is **not** rewritten — the
taxpayer still paid the seller $300, and no source correction can change what
the taxpayer paid. A new determination follows: $700 includible, $300 not.

**What the case establishes.** Correcting a document must not silently
re-author a fact about the world.

**Incumbent behaviour.** The correction supersedes the box-1 finding and the
adjustment is untouched. The behaviour is nominally right, but for a reason
that carries no information: the two facts are in disjoint identity spaces, so
they are independent by unrelatedness rather than by design. Nothing is marked
stale, because there is no determination to mark. The engine simply recomputes
an aggregate.

Note that at $1,000 box 1 with $300 accrued, the numbers remain coherent. Had
the correction been to $200, the incumbent would subtract $300 from an item
worth $200 and detect nothing, because its only guard compares total positive
interest against total adjustments across all families.

## TI-L2 — The circumstance is corrected

**Facts entering.** TI-B2, then the taxpayer corrects P2: the amount paid to
the seller was $250, not $300. P1 is unchanged at $1,200.

**Required behaviour.** P2 supersedes. The statement still reports $1,200 and
is not touched. The prior determination is no longer current; a new one gives
$950 includible, $250 not includible.

**What the case establishes.** The mirror of TI-L1. A correction to the
taxpayer's own account of their transaction must not appear to revise what the
payer reported.

**Incumbent behaviour.** Again nominally right and again uninformative, for the
same reason. Taken together, TI-L1 and TI-L2 **do not discriminate** between
the incumbent and an item-level determination. They are recorded as a case pair
that was expected to discriminate and does not.

## TI-A1 — Outside the slice

**Facts entering.** A different synthetic taxpayer redeemed Series EE savings
bonds in 2025, reported in box 3 of a Form 1099-INT, and paid qualified higher
education expenses in the same year.

**Why it is here.** IRC § 135(a) provides that no amount is includible in gross
income for qualifying redeemed savings bonds. That is a substantive exclusion
of the same structural kind as the accrued-interest rule: an ordinary
circumstance the payer cannot see, displacing the § 61 default.

**Required behaviour.** The case is not modeled and must not appear to be. A
model that succeeds on TI-B1 and TI-B2 has established nothing about TI-A1, and
must not present a computed line 2b as though it had.

**Incumbent behaviour.** The box-3 amount flows through the `b3` family into
the positive total and is included in full. The result is silently wrong for
this taxpayer, and it is wrong in exactly the way TI-B2 would have been wrong
had the accrued-interest adjustment never been built — which is the point.
Building the accrued-interest path did not build a way to *notice* TI-A1.

**Scope boundary.** No implementation of § 135 follows from this case. It is
here to bound the conclusion, not to extend the work.

## What the six cases jointly show

| Case | Does it discriminate incumbent from item determination? |
| --- | --- |
| TI-B1 | No — same number, but the incumbent cannot say why |
| TI-B2 | Yes — the incumbent cannot accept the circumstance, only the conclusion |
| TI-N1 | Yes, decisively — the incumbent cannot represent the unanswered state |
| TI-L1 | No — independent, but by unrelatedness rather than design |
| TI-L2 | No — same |
| TI-A1 | Neither path detects it; it bounds what either result may claim |

The discriminating cases are TI-B2 and TI-N1, and they discriminate on the same
axis: whether the model can hold an **ordinary fact about a transaction** as
distinct from the **tax conclusion drawn from it**. The lifecycle cases, which
were expected to carry weight, turn out not to.
