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

**How they combine.** Obligation, payment **or deemed payment**, and taxpayer-relative
qualification must all hold, for that person, on that loan. Each is necessary; none is
sufficient; and what they establish together is that an amount is **attributable to that
filer** — not that any deduction follows. The remaining conditions and limits still
apply: dependent status, filing status, the cap, the MAGI phase-out, and the rest.

## The five cases

Written from the filer's side: each row says what is attributable to **the filer**, not
what anyone else's return does.

| Case | Obligated | Paid, or deemed paid | Qualifies for them | What is established |
| --- | --- | --- | --- | --- |
| The filer is the obligated borrower and pays | yes | yes | normally yes — own education | The interest they paid is attributable to them. Whether a deduction follows depends on the remaining conditions and limits |
| The filer is an obligated co-signer who pays nothing | yes | **no** | — | **No attributable amount.** Obligation alone attributes nothing |
| The filer is an obligated co-signer who pays some or all | yes | yes | **the open one** | Attributable only if the education was for them, their spouse, or their dependent *at origination*. A paying parent whose child was not their dependent then has no attributable amount |
| Someone not obligated pays for the filer | filer: yes | filer: **deemed** yes | — | The filer is treated as paying, so the amount is attributable to them. The payer's own position is not modelled and does not need to be |
| The filer and another obligor each pay part | filer: yes | filer: partly | tested for the filer | The part **the filer** paid is attributable to them. What the other person's return does is outside this model |

Two errors these cases exist to block: **a paying co-signer does not automatically
qualify**, and **whoever sends the money does not automatically own the deduction**.

## The actual open question: obtaining the filer-attributable amount

Three different things that an earlier version of this work ran together:

- **The reported total** — what a Form 1098-E box 1 says.
- **The amount attributable to the filer** — the interest they paid or are treated as
  paying, on borrowing they are obligated on and that qualifies for them.
- **The final deduction** — after the cap, the phase-out and every other condition.

In the ordinary case the first two coincide. In a shared-payment case they do not, and
**the reported total must not be used silently as the attributable amount.**

Four candidate paths for obtaining it, none selected here:

1. **From evidence** — something in the workspace distinguishes the filer's payments.
2. **From an ordinary statement** — the filer says what they paid.
3. **Derived** — from other facts already held.
4. **Unresolved** — the amount is not determinable, which is A3's blocked state and an
   honest outcome.

**What A6 can test within this boundary.** One filer's treatment in a shared-payment
scenario, with no second return and no payer identity. If the fixture simply supplies
the filer-attributable amount, that proves the consumer uses an attributable amount
rather than the reported total — and proves **nothing** about how such an amount is
obtained, which is exactly what paths 1 to 4 leave open.

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

**Filer-centered.** No second person's identity, no per-payer ledger, no two-return
coordination. Everything below is about the filer.

**Represent now** — as conceptual distinctions, not as three prescribed fields; A5
selects the representation:

- the filer's legal obligation concerning the relevant borrowing;
- interest the filer actually paid;
- interest **treated as paid** by the filer under an applicable rule, where supported.

That is enough to stop a payment statement being read as an obligation statement, and to
stop the reported total standing in for an attributable amount.

**Defer, named not designed:** how a shared-payment amount is obtained, where paths 1–4
above are the options; determining dependency *at origination*; the case where a paying
co-signer has no Form 1098-E of their own. No household or payment-allocation framework.

## Resolved: filer-centered

The owner's direction of 2026-09-22. No other payer's identity is represented unless a
concrete supported case demonstrates that identity is necessary — and none of the five
cases above does. Each is expressible from the filer's side alone.

An earlier version of this section posed a choice between representing the payer and
recording payment separately from obligation. That was false: obligation, payment and
deemed payment are three things about **one** person, and keeping them distinct needs no
second identity.

## Remaining limitations

Dependency-at-origination has no producer and is not asked. The third-party deeming rule
is represented nowhere. Whether two people each deducting part of one loan's interest is
in scope for this vertical is unsettled. And none of this is executed — it is a model, at
`read` level against statute, regulation and committed content.
