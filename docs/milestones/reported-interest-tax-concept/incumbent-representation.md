# What the Engine Represents Today

## What this document is

The engine already subtracts accrued interest when it computes Form 1040 line
2b. The presence of that subtraction is easily mistaken for evidence that the
engine models the accrued-interest circumstance. This document reads the
artifacts to find out what is actually represented.

The finding is that the subtraction exists and the circumstance does not. The
engine represents a **row on a return** whose amount happens to be right,
supported by an authority that does not establish the subtraction is required,
identified in a namespace that cannot say which item it reduces.

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

## Six things the artifacts show

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
authority of family `irs-instructions`, form `1040-SCH-B`, tax year 2025. That
is the correct authority for the disclosure mechanics. It is not an authority
for the substantive proposition that the amount is not the purchaser's income.

The engine has therefore attached a *where to write it* authority to a *whether
it happens* question. Read forwards: the artifact that decides a taxpayer's
income is supported by a document that only explains form layout.

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
`us-code`. Regulatory authority is not. Treas. Reg. § 1.61-7(c) — the authority
that actually establishes the treatment in this case — has no family and no
locator shape, so it cannot be recorded at all.

The gap is therefore specific: **a missing regulation authority family and
locator**, not an inability to cite substantive law in general. `citation.v1`
is a published schema, so closing it is a contract question rather than a
content change. It is recorded here as a production condition and is outside
this milestone's scope.

Separately, and as an observation about content practice rather than about
capability: of the 74 citation artifacts for 2025, 71 are `irs-instructions`,
2 are `irs-publication`, 1 is `irs-form`, and none is `us-code`. The existing
statutory family has gone unused. That count alone does not establish why —
whether substantive authority was never needed, never sought, or recorded
elsewhere — and no inference about the engine's history is drawn from it here.

### 5. The circumstance is typed as a reported amount of the same quantity as the income it reduces

The accrued-interest fact type carries `source_amount: true`, which marks it as
an amount reported by a source. No source reports it; the taxpayer supplies it
from knowledge of their own transaction.

It also carries `quantity: tax.us.2025.quantity.taxable-interest` — the same
quantity as the box-1 income it reduces. The purchase-price component and the
income are declared to be the same kind of quantity. The quantity vocabulary
being referred to is, in its entirety, the list `["taxable-interest",
"wages"]`, so the declaration carries no discriminating content in either
direction.

### 6. The completeness question asks the user for a tax classification

Alongside the amount, the family declares
`tax.us.2025.scheduleb.adjustment.accrued-interest.source-closure`: a
user-attested closure of "the 2025 Accrued Interest adjustment class."

To answer it, a user must already know what a Schedule B accrued-interest
adjustment is, and must decide whether they have any. That is the legal
classification, put to the person least equipped to make it. The ordinary form
of the same question — *did you buy any bonds partway through an interest
period?* — is not asked, because the model has no place to put the answer.

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

There is no bond, no obligation, no account, no purchase, no disposition — no
entity that exists in the world rather than on paper. The nearest thing,
`f1099b-transaction`, is a row on a broker's statement.

This is why the accrued-interest circumstance has no home. It is a fact about
an economic object, and the ontology has no economic objects. The circumstance
was therefore filed where there *was* a home for it: on the return form that
discloses its effect.

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

The engine gets $900 for the right arithmetic and the wrong reasons. It holds
the reported amount and the includible total, and between them it holds a form
row rather than a determination. The reason the amounts differ is not recorded
anywhere, the authority that makes them differ cannot be cited, and the fact
that produces the difference cannot be asked for in terms the taxpayer would
recognise.
