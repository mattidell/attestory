# Whose student-loan interest deduction is this?

A bounded model. Authority is statute and regulation; IRS publications are explanatory
and never controlling.

## Three conditions, none of them the whole test

**Who is legally obligated.** 26 CFR § 1.221-1(b)(1): a taxpayer is entitled to the
deduction *only if* the taxpayer has a legal obligation to make interest payments under
the terms of the loan. A co-signer has one. More than one person can have one on the
same loan.

**Who actually paid.** § 221(a) allows "the interest paid by the taxpayer during the
taxable year". Obligation without payment yields nothing to deduct.

**Who is treated as paying.** § 1.221-1(b)(4)(i): where a third party **not** legally
obligated pays on behalf of a taxpayer who **is** obligated, the taxpayer is treated as
receiving the payment and in turn paying the interest. This moves the *payment*, not the
obligation, and it runs only in that direction.

**Whether the loan qualifies for this taxpayer.** § 221(d)(1)(A): the expenses must have
been incurred on behalf of the taxpayer, their spouse, or **their dependent as of the
time the indebtedness was incurred**. Qualification is therefore *taxpayer-relative* and
dated at origination — the same loan can be a qualified education loan for one person and
not for another.

**How they combine.** All of obligation, payment and taxpayer-relative qualification must
hold, for that person, on that loan. Each is necessary; none is sufficient; and the
amount deducted is the interest *that person* paid.

## The five cases

| Case | Obligated | Paid | Qualifies for them | Result |
| --- | --- | --- | --- | --- |
| Obligated borrower pays | yes | yes | normally yes — own education | Deducts what they paid |
| Obligated co-signer pays nothing | yes | **no** | — | **Nothing.** Obligation alone deducts nothing |
| Obligated co-signer pays some or all | yes | yes | **the open one** | Deducts only if the education was for them, their spouse, or their dependent *at origination*. A paying parent whose child was not their dependent then gets nothing |
| Non-obligated person pays for the borrower | payer: **no** | payer: yes | — | Payer deducts nothing. The borrower is *treated as* paying and deducts, if obligated and qualifying |
| Borrower and co-signer each pay part | each: yes | each: partly | tested separately for each | Each may deduct the part **they** paid, on their own return, if all three hold for them |

Two errors these cases exist to block: **a paying co-signer does not automatically
qualify**, and **whoever sends the money does not automatically own the deduction**.

## Where the incumbent applies a loan-level condition return-wide

Checked against committed content, and this is a real defect rather than a modelling
preference.

- `sli-scope.legally-obligated-for-interest` is keyed on **tax-year only**. Obligation
  holds per loan. Someone obligated on one loan and not another cannot be represented by
  a single return-level yes/no.
- The related-person exclusion is a relation between the taxpayer and **the creditor on
  that indebtedness**. Our authority record says so directly: it is not a fact about the
  return, and not about a statement except where a statement happens to name a lender.
  The incumbent witness is per-statement, and a statement may aggregate a related-person
  loan with an unrelated one.

Neither is this milestone's to fix in the incumbent. Both bound what a *new* consumer may
key its facts on.

## The smallest coherent implementation boundary

**Represent now:** that obligation and payment are separate conditions; that the amount
is the interest *this taxpayer* paid; and that qualification is taxpayer-relative. Enough
to stop a payment statement being read as an obligation statement, and to stop one
person's circumstances deciding another's deduction.

**Defer, named not designed:** allocation between two payers on one loan; determining
dependency *at origination*; the case where a paying co-signer has no Form 1098-E of
their own; and any household or payment-allocation framework, which is explicitly not
wanted.

## Consequential owner decision

**Does this milestone represent the payer at all, or only the filer's own obligation and
payment?** Representing the payer opens multi-person cases — two returns, one loan — and
the deferred items above. Not representing it means the product cannot yet distinguish
"I pay it" from "I'm obligated on it" in what it records, only in what it asks.

*Depends on it:* whether A5 needs a payer concept, whether the interest amount needs a
per-payer dimension, and whether case 5 is testable at all in A6.

## Remaining limitations

Dependency-at-origination has no producer and is not asked. The third-party deeming rule
is represented nowhere. Whether two people each deducting part of one loan's interest is
in scope for this vertical is unsettled. And none of this is executed — it is a model, at
`read` level against statute, regulation and committed content.
