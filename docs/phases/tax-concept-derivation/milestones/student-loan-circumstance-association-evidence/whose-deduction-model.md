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
sufficient; and what they establish together is **how the interest the filer paid is
treated** — not that any deduction follows. The remaining conditions and limits still
apply: dependent status, filing status, the cap, the MAGI phase-out, and the rest.

## The five cases

Written from the filer's side: each row says what **the filer** paid and how it is treated, not
what anyone else's return does.

| Case | Obligated | Paid, or deemed paid | Qualifies for them | What is established |
| --- | --- | --- | --- | --- |
| The filer is the obligated borrower and pays | yes | yes | normally yes — own education | They paid that interest. Whether it counts, and what deduction follows, depends on the remaining conditions and limits |
| The filer is an obligated co-signer who pays nothing | yes | **no** | — | **Nothing was paid**, so there is no payment to treat. Obligation alone supplies one condition and no quantity |
| The filer is an obligated co-signer who pays some or all | yes | yes | **the open one** | **They paid that interest, and that stays true.** Whether it counts depends on whether the education was for them, their spouse, or their dependent *at origination*. A paying parent whose child was not their dependent then still paid — the payment is preserved and excluded by a named condition, not erased |
| Someone not obligated pays for the filer | filer: yes | filer: **deemed** yes | — | The filer is treated as paying that interest. The payer's own position is not modelled and does not need to be |
| The filer and another obligor each pay part | filer: yes | filer: partly | tested for the filer | **The filer paid their part.** How that part is obtained is the open question below. What the other person's return does is outside this model |

Two errors these cases exist to block: **a paying co-signer does not automatically
qualify**, and **whoever sends the money does not automatically own the deduction**.

## Four things to keep apart

An earlier version of this work used "attributable amount" for two of these at once —
what happened, and how the rules treat it. They are separate:

1. **The reported amount** — what a Form 1098-E box 1 says.
2. **Interest the filer paid**, or is treated as paying under § 1.221-1(b)(4)(i). A fact
   about what happened. It does not depend on any tax condition holding.
3. **How that interest is treated** under the loan and deduction conditions — whether it
   counts, and if not, which condition excludes it.
4. **The deduction** — after the cap, the phase-out and the rest.

These are distinctions to preserve, not four fields or four mandatory processing stages.
A5 decides the representation.

**Worked small case.** The filer paid **$400**, and the borrowing fails a qualification
condition — say the education was not for them, their spouse or their dependent at
origination. Then: the reported amount is whatever the form says; **the filer paid $400,
and that stays true**; the treatment is that the $400 does not count, *because* that
condition failed; the deduction reflects none of it.

The point of keeping (2) and (3) apart is that **changing the qualification later must not
require pretending the payment changed.** If the condition turns out to hold after all,
the $400 was always $400 and only its treatment moves.

**And what an ordinary answer supplies is only (2).** "I paid $400" is a payment
statement. It establishes nothing about obligation, nothing about qualification, and
nothing about the deduction — those come from defaults, from other circumstances, and
from rules. A definition that packs the conditions into the amount cannot be satisfied by
that answer.

In the ordinary case (1) and (2) coincide. In a shared-payment case they do not, and
**the reported amount must not silently stand in for what the filer paid.**

Four candidate paths for obtaining what the filer paid, none selected here:

1. **From evidence** — something in the workspace distinguishes the filer's payments.
2. **From an ordinary statement** — the filer says what they paid.
3. **Derived** — from other facts already held.
4. **Unresolved** — the amount is not determinable, which is A3's blocked state and an
   honest outcome.

**What A6 can test within this boundary.** One filer's treatment in a shared-payment
scenario, with no second return and no payer identity. If the fixture simply supplies what
the filer paid, that demonstrates **downstream handling** — that the consumer works from
what the filer paid rather than from the reported amount — and demonstrates **nothing**
about acquisition or translation. How such an amount is obtained is what paths 1 to 4
leave open.

**A5 either selects a supported route or leaves this case explicitly unresolved.** Both
are acceptable outcomes; what is not acceptable is proceeding as though a fixture had
settled it.

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
- interest the filer actually paid, **or is treated as paying** under
  § 1.221-1(b)(4)(i) where supported;
- how that interest is **treated** under the applicable conditions, kept separate from
  the payment itself.

That is enough to stop a payment statement being read as an obligation statement, to stop
the reported amount standing in for what the filer paid, and to stop an excluded payment
being recorded as though it never happened.

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
