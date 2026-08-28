# What the Engine Represents Today

## What this document is

The engine already subtracts accrued interest when it computes Form 1040 line
2b. The presence of that subtraction is easily mistaken for evidence that the
engine models the accrued-interest circumstance. This document reads the
artifacts to find out what is actually represented.

The finding is that the subtraction exists and the circumstance does not. The
engine represents a **row on a return**: an amount whose identity is a return
form instance, cited to the authority for the disclosure rather than to the
authority for the treatment, and held in a namespace that cannot say which item
it reduces.

## The subtraction as it exists

Four artifacts carry it.

**The fact type** is `tax.us.2025.scheduleb.adjustment.accrued-interest.amount`.
Its identity keys are the tax year and an entity of kind
`tax.us.scheduleb-adjustment-instance`. Its declared title describes "an
accrued-interest-paid-to-seller adjustment reported for one logical Schedule B
interest-adjustment instance."

**The source family** `tax.us.2025.scheduleb.adjustment.accrued-interest` groups
those instances and carries a closure claim about "every contributed accrued
interest amount within the bounded Schedule B interest-adjustment surface."

**The rule** `tax.us.2025.rule.scheduleb-adjustment.accrued-interest-subtotal`
sums the family and publishes
`tax.us.2025.interest.scheduleb-accrued-interest-subtotal`.

**The line-2b rule** `tax.us.2025.rule.form1040-line2b` v4 subtracts that
subtotal, alongside the nominee and ABP subtotals, from the sum of seven
positive-interest subtotals.

The arithmetic is correct, and this is demonstrated by committed execution
rather than assumed. `tests/test_schedule_b_interest_adjustments.py` runs the
production content against synthetic acts and establishes three results
directly relevant here: with $2,000 of box-1 interest and a $100
accrued-interest adjustment, line 2b resolves to $1,900; with the adjustment
family closed and empty, it resolves to $2,000; and correcting an adjustment
amount from $100 to $140 moves the line to $1,860. Those are the structural
analogues of the two principal cases and of a circumstance correction, at
different amounts, with the correction exercised on the sibling nominee class.

Everything below concerns what the arithmetic is about.

## Six readings of the artifacts

Six things were examined. Four are findings, one is a content gap rather than a
capability gap, and one is a place where an expected finding was looked for and
not found. They are kept in one list because the null result is as much a part
of the record as the others.

### 1. The subject of the fact is a return row, not a purchase

The identity of an accrued-interest amount is *the tax year plus a Schedule B
adjustment instance*. A Schedule B adjustment instance is a line on a form the
product generates. So the recorded proposition is, in substance, *"a Schedule B
adjustment row exists in the amount of $300."*

That is not proposition P2. P2 is about a purchase of an obligation on a date
from a seller. Nothing in the artifact graph is about a purchase.

The consequence is not cosmetic. Because the subject is a form row, the only
question the model can put to the user is a question about the form row.

### 2. There is no key linking the adjustment to the item it adjusts

The reported amount is identified by payer, statement, and tax year. The
adjustment is identified by adjustment instance and tax year. The two identity
spaces are disjoint: no key of one appears in the other.

The two quantities meet in exactly one place, `rule.form1040-line2b` v4, and
they meet there as two of ten sibling scalar subtotals fed into one add and one
subtract. At that point both have already lost their item identity.

With one statement and one adjustment this is invisible, because the aggregate
and the item coincide. With two statements it is not merely invisible but
unanswerable: the model has no way to express which statement's interest the
$300 reduces, and no way to detect an adjustment larger than the item it
belongs to. The rule's only guard is a comparison of the total positive basis
against the total adjustments, which is an aggregate check. An item-level
incoherence passes it.

### 3. The authority cited is a reporting instruction

`tax.us.2025.citation.scheduleb-adjustment.accrued-interest` records an
authority of family `irs-instructions`, form `1040-SCH-B`, tax year 2025.

That is the right authority for the disclosure mechanics, and it carries more
than mechanics: because line 1 of the same instructions calls for *all* of the
taxpayer's taxable interest, directing the buyer to subtract this amount from
that total operationally establishes that the amount is not the buyer's taxable
interest. The citation is not empty, and calling it mere layout advice would be
unfair to it.

What it does not reach is the rest of the proposition. The instructions never
say the payment is a return of capital and never mention basis, and they are not
the source that explains *why* the subtraction is right. The substantive
authority — Pub. 550, *Bonds Sold Between Interest Dates*, against
IRC § 61(a)(4) — is not attached to the artifact, although both could be cited
in the existing vocabulary. So the gap here is a content gap, not a schema gap:
one citation is present where the proposition needs a stack.

### 4. The citation vocabulary has no Treasury Regulation family

`citation.v1` admits exactly four authority families, as a closed `oneOf` with
`additionalProperties: false`:

| Family | Locator fields |
| --- | --- |
| `us-code` | title, section |
| `irs-form` | form_id, tax_year |
| `irs-instructions` | form_id, tax_year |
| `irs-publication` | publication, revision |

Statutory authority is representable: IRC § 61(a)(4) can be cited through
`us-code`. Regulatory authority is not: no Treasury Regulation has a family or
a locator shape, so § 1.61-7 in any of its paragraphs cannot be recorded at all.

**For this slice the gap is real but not blocking.** The authority actually on
point for the between-interest-dates purchaser is Publication 550, *Bonds Sold
Between Interest Dates* — and `irs-publication` exists. The full authority stack
this case needs is IRC § 61(a)(4) via `us-code`, Pub. 550 via `irs-publication`,
and the Schedule B instructions via `irs-instructions`. All three are citable
today. What is not citable is the seller-side corroboration in
Treas. Reg. § 1.61-7(d), and the traded-flat neighbour § 1.61-7(c) that has to
be distinguished to bound the account.

So the gap is specific and narrower than it first appeared: **a missing
regulation authority family and locator**, which bites on any tax proposition
whose best support is regulatory, and which here costs corroboration rather than
the citation itself. `citation.v1` is a published schema, so closing it is a
contract question rather than a content change. It is recorded as a production
condition and is outside this milestone's scope.

Separately, and as an observation about content practice rather than about
capability: of the 74 citation artifacts for 2025, 71 are `irs-instructions`,
2 are `irs-publication`, 1 is `irs-form`, and none is `us-code`. The existing
statutory family has gone unused. That count alone does not establish why —
whether substantive authority was never needed, never sought, or recorded
elsewhere — and no inference about the engine's history is drawn from it here.

### 5. The typing fields carry no economic claim, in either direction

It is tempting to read the accrued-interest fact type's `source_amount: true`
and `quantity: tax.us.2025.quantity.taxable-interest` as economic assertions —
that the amount is *reported by a source*, and that the purchase-price component
is *the same kind of thing* as the income it reduces. Neither reading is
correct, and the correction matters because both would have been evidence.

`source_amount: true` is the aggregation marker. Under ADR-0028 decision 7 it
identifies a fact type as a collectible member of a family that a rule sums, and
it is what makes the `quantity` pin mandatory. It says nothing about who
supplied the value. The nominee, ABP, and non-form interest fact types all carry
it, and the taxpayer supplies those too.

The `quantity` pin is likewise the composition force-declare mechanism of
ADR-0028 decisions 7–8: it makes a rule's summands declare a common unit-bearing
symbol so that composition can be checked, and 23 quantity citizens exist to
serve that check. It is not an economic-kind tag, and sharing one between an
income amount and a subtraction from that income is exactly what a checkable
subtraction requires.

So this is a place where the artifacts were examined for an implicit economic
commitment and none was found. The fields do their declared jobs. **What follows
is only that the fact type does not carry economic kind anywhere** — not that it
mis-states it. That is consistent with finding 1 rather than additional to it.

### 6. The only question the user is asked is phrased in return vocabulary

Alongside the amount, the family declares
`tax.us.2025.scheduleb.adjustment.accrued-interest.source-closure`: a
user-attested closure of "the 2025 Accrued Interest adjustment class."

What that fact *asserts* is completeness, not classification. ADR-0011 decision
4 is explicit: the assertion reports completeness; it does not constitute a
tax-law choice. Decision 5 makes it affirmative-only, so the absence of a
closure finding is unknown and blocks rather than defaulting. The semantics are
sound, and reading this fact as asking the user to decide a point of law would
be wrong.

The problem is the **name of the class the user must recognise**. To attest
completeness over "the 2025 Accrued Interest adjustment class," a user must know
what belongs in that class — which is Schedule B vocabulary, and which is the
classification. The ordinary form of the same question, *did you buy any bonds
partway through an interest period and pay the seller for interest that had
already built up?*, is not asked, because there is no fact type whose subject is
a purchase.

This is finding 1 seen from the user's side. It is a vocabulary consequence of
where the fact lives, not a defect in the closure mechanism.

## The shape underneath all six

Every entity kind declared in the 2025 content package is a document, the
issuer of a document, a row within a document, or engine infrastructure:

> `1098-statement`, `1098e-statement`, `1099div-statement`, `1099g-statement`,
> `1099int-statement`, `1099oid-statement`, `1099r-statement`,
> `form1065-k1-statement`, `ssa1099-statement`, `w2-slip`,
> `f1099b-statement`, `f1099b-transaction`, `f1099b-broker`,
> `scheduleb-adjustment-instance`, `dividend-payer`, `interest-payer`,
> `ira-payer`, `unemployment-payer`, `mortgage-lender`, `student-loan-lender`,
> `employer`, `partnership`, `family-horizon`

Two qualifications keep this from being said too broadly.

The payer, lender, employer, and partnership kinds *are* real-world parties.
They exist independently of any document. But every one of them is declared and
used in the role of **issuer of a statement**, and the content package gives
them no other function; none participates in a transaction, holds an
obligation, or has a counterparty relation to the subject. So the accurate claim
is not "nothing here is real" but that the only real-world entities are the
parties on the document, in their document-issuing role.

And there is genuinely no bond, no obligation, no account, no purchase, no
disposition. The nearest candidate, `f1099b-transaction`, is identified as a row
of a broker statement rather than as an acquisition or a sale.

This is why the accrued-interest circumstance has no home. It is a fact about an
economic object, and this content package declares no economic objects. The
circumstance was therefore filed where there *was* a home for it: on the return
form that discloses its effect.

The evidence for this is the 2025 US-federal content package. It is not evidence
about the kernel, which does not fix a domain vocabulary, nor about what the
engine could declare. What it establishes is that the modelled domain as built
so far is a domain of documents.

## What the composition declares, and what it does not

`tax.us.2025.interest-composition` v4 declares
`coextensiveness: "slot-bijection"` over seven positive families, and a
required universe of *"seven declared positive taxable-interest families
forming the gross Schedule B Part I line-1 basis, without subtractive
adjustments."*

Slot bijection is a real and checkable property: the rule consumes exactly the
families the composition declares. It is a statement about the artifacts. It
says nothing about whether those families are the legally relevant ones, and
the required-universe text defines the universe by reference to a **form line**
— the gross Schedule B line-1 basis — rather than by reference to what the law
counts as interest income.

The taxable-interest concept is not declared anywhere. What exists is a rule
that publishes the symbol `tax.us.2025.interest.taxable-total` and a form field
`tax.us.2025.form1040.line-2b` that binds the symbol to a line and describes it
as *"exact seven-family positive taxable interest less the three separately
closed Schedule B adjustment classes."* The description enumerates the
implementation. A reader can recover what the engine computed; they cannot
recover what it was trying to compute, because no artifact says.

## Summary

The engine gets $900, and it gets it by a route that holds the reported amount
and the includible total with a form row between them rather than a
determination.

It is worth being precise about how much of the reason survives in the
artifacts, because "nothing is recorded" would overstate it. A reader with only
the committed content can recover the **reporting category**: the fact type's
title names an "accrued-interest-paid-to-seller adjustment," and the line-2b
form field describes itself as the seven positive families less the three
separately closed adjustment classes. Someone who already knows the tax
treatment can read the artifacts and see which treatment was applied.

What is not recoverable is the **proposition** — that interest accrued before
purchase is not the purchaser's income because it is a return of their capital,
that this reduces basis, and on what authority. The title states a category; it
does not assert anything, nothing depends on it, and nothing checks it. So the
distinction is preserved as a label on a subtraction, not as a claim the model
holds.

Alongside that: the substantive authority is citable in the existing vocabulary
but is not attached, the regulatory corroboration is not citable at all, and the
ordinary fact that produces the difference cannot be asked for in terms the
taxpayer would recognise.
