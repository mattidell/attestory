# Reported Interest to Tax Concept

## The question

A Form 1099-INT reports $1,200. The taxpayer's income is $900, because they
bought the bond partway through an interest period and paid the seller for
interest that had already accrued. The reported amount is not wrong; it is
simply not the same thing as the taxpayer's income.

**Does the engine need a separately recoverable item-level tax determination
between what the document reports and what reaches the return?**

The engine already produces $900 for this case. So the question is not whether
the arithmetic works. It is whether anything in the model holds the reason.

## What the evidence shows

The determination is missing, and the reason it is missing is more specific
than "not built yet."

Every entity kind the engine declares is a document, the issuer of a document,
a row within a document, or engine infrastructure. There is no obligation, no
account, no purchase — no entity that exists in the world rather than on paper.
The accrued-interest circumstance is a fact about a purchase, so it had nowhere
to live, and it was filed instead as a **row on Schedule B**: an amount whose
identity is a return-form instance, cited to the form instructions, unlinked to
the item it reduces.

The consequences follow from that one displacement:

- the engine cannot be given the ordinary fact, only the classified conclusion;
- it cannot ask the taxpayer the ordinary question, only the Schedule B one;
- it cannot say which reported item an adjustment reduces, so it cannot detect
  an adjustment larger than its item;
- it cannot cite the authority that governs, because the citation vocabulary
  has no Treasury Regulation family; and
- it carries only half the governing proposition — the income effect — and
  drops the basis effect without trace.

## Reading order

1. [accrued-interest-item-model.md](accrued-interest-item-model.md) — the five
   propositions the case actually contains, what supports each, and the
   determination they imply. Establishes the treatment from official sources
   and separates substantive authority from reporting authority.
2. [incumbent-representation.md](incumbent-representation.md) — what the
   existing artifacts represent, read from the artifacts themselves rather than
   from the correctness of the output.
3. [synthetic-case-specification.md](synthetic-case-specification.md) — six
   cases holding the reported amount constant, and which of them actually
   discriminate between the two paths.

## Scope

US-federal individual income tax, tax year 2025, one synthetic taxpayer, one
logical Form 1099-INT, one box-1 amount, one obligation purchased between
interest payment dates. All identities and amounts are demonstration values.

This slice establishes nothing about original issue discount, market discount,
bond premium, the savings-bond education exclusion, nominee ownership,
previously reported interest, tax-exempt interest, elections, joint-return
subject identity, or any interest not reported in box 1. One case is included
from outside the slice for the sole purpose of bounding what the others may be
taken to prove.

The work selects no schema, citizen kind, field shape, or production contract.
