# Reported Interest to Tax Concept

## The question

A Form 1099-INT reports $1,200. The taxpayer's income is $900, because they
bought the bond partway through an interest period and paid the seller for
interest that had already accrued. The reported amount is not wrong; it is
simply not the same thing as the taxpayer's income.

**Does the engine need a separately recoverable item-level tax determination
between what the document reports and what reaches the return?**

The engine already computes a subtraction of this shape — committed tests run
the production content and resolve line 2b to $1,900 from $2,000 of box-1
interest less a $100 accrued-interest adjustment, a structural analogue at
different amounts. But the $100 is supplied to the engine *already classified*
as an accrued-interest adjustment. That establishes working arithmetic, not
derivation from ordinary facts. So the question is not whether the arithmetic
works. It is whether anything in the model holds the reason.

## The answer, stated plainly

**A separately recoverable item-level determination is warranted, on a narrow
executed ground.** Two representation shapes were built on the same six cases
and run through the engine's real expression evaluator: a **distributed** shape,
in which ordinary facts and a tax rule derive an item-linked result with no
durable determination object, and an **explicit determination** shape. The
executed comparison is recorded in
[`docs/prototypes/reported-interest-tax-concept/examination.md`](../../prototypes/reported-interest-tax-concept/examination.md).

**Arithmetic does not discriminate.** Both shapes produce every required number
on all six cases, including the two designed to break the weaker one. Any
argument from the displayed number is unsupported in either direction.

The static rubric does not discriminate either, once the distributed shape is
repaired. As first built it failed one requirement — no authority was
recoverable from a bare amount. Attaching the item, the rule, the authority, and
provenance to each symbol clears every one of the ten requirements.

What discriminates is two dynamic probes:

- **The distributed shape can go silently incoherent.** After the circumstance
  correction $300 → $250, refreshing only the includible symbol leaves it
  asserting $950 includible — implying $250 non-includible — while its basis
  symbol still reads $300. It does not detect the disagreement, because
  coherence is an external observer's arithmetic rather than something the
  result carries. The determination shape cannot reach that state.
- **A carried consequence cannot check itself in a later year.** The
  distributed shape carries a bare $300 against an item and can state neither
  the reported nor the includible amount it is consistent with. In the year of
  disposition there is no re-run to perform: the producing facts belong to a
  prior year's workspace. The determination shape carries all four amounts and
  can.

The honest counter-case is recorded with the recommendation: the distributed
shape's lifecycle displacement is genuinely more precise, and the first probe
alone would prove nothing if the system always re-ran every symbol from current
facts. The recommendation rests on the second probe.

Two earlier claims are **withdrawn and must not be re-asserted.** First, that
the incumbent produces the correct number in all six cases — it does not; see
TI-A1 below. Second, that a tax-year `{yes, no}` fact plus a guard clause in the
line-2b rule passes the cases. That design was never built or executed, and the
claim does not follow: TI-B2 requires the ordinary circumstance, its amount, and
item linkage, not merely yes/no, and TI-N1 must distinguish "yes, amount
supplied" from "yes, amount missing," which a guard reading only yes/no cannot
do.

**The incumbent is silently wrong on TI-A1.** The 2025 package contains no
§ 135 or Form 8815 content, verified by search. For a taxpayer with qualifying
savings-bond education expenses, box 1 flows to line 2b unreduced and the
incumbent's ordinary line-2b result is not correct for that taxpayer. Both
prototype shapes block explicitly instead.

Alongside the comparison, a narrower set of requirements is established.

**The modelled domain is a domain of documents.** In the 2025 US-federal content
package, every declared entity kind is a document, a party in its role as issuer
of a document, a row within a document, or engine infrastructure. There is no
obligation, no account, no purchase, no disposition. The accrued-interest
circumstance is a fact about a purchase, so it had nowhere to live and was filed
as a **row on Schedule B** — an amount whose identity is a return-form instance,
unlinked to the item it reduces.

Three consequences follow, and each is a requirement on whatever comes next:

- **The ordinary fact cannot be supplied, only the classified conclusion.** The
  engine can be told "$300 of accrued-interest adjustment." It cannot be told
  "I bought this bond on 15 May and paid the seller $300 for interest that had
  already built up." The user is asked to attest completeness over "the 2025
  Accrued Interest adjustment class," which requires them to recognise a
  Schedule B category.
- **An adjustment cannot name the item it reduces.** The reported amount is
  keyed by payer and statement; the adjustment by adjustment instance. The two
  meet only as scalar subtotals inside the line-2b rule, by which point both
  have lost item identity. The only coherence guard is an aggregate comparison,
  which an item-level incoherence passes.
- **The proposition is labelled, not asserted.** A reader of the committed
  artifacts can recover the reporting *category* — the fact type is titled an
  accrued-interest-paid-to-seller adjustment. They cannot recover the claim that
  such interest is not the purchaser's income because it is a return of capital,
  nor that it reduces basis, nor on what authority. The substantive authority is
  citable in the existing vocabulary and simply is not attached.

Two further findings are bounded and recorded rather than acted on: the citation
vocabulary cannot express a Treasury Regulation (below), and the basis
consequence of the treatment is carried by no artifact and is invisible in the
year it is dropped.

## What this milestone is and is not

It is a **completed executable vertical slice**: the six cases were built and
run end to end, under two rival representation shapes, through the engine's real
expression evaluator. It establishes semantic and representation requirements
and produces a recommendation from executed evidence.

It is **not** a production selection. The shapes are prototype evidence. No
schema, citizen kind, field shape, storage mechanism, ADR, or migration is
selected here, and none should be inferred from the recommendation. The
recommendation itself turns on one unresolved product question, named in the
examination.

An earlier version of this document recorded that no candidate implementation
was exercised and that the necessity claim had been defeated on paper. Both are
superseded. Paper analysis was not sufficient in either direction; the executed
comparison is.

Claims about incumbent behaviour are graded. Some rest on exact execution of a
committed test, some on a structural analogue at different amounts, and some on
artifact inspection. The examination separates the three, and nothing here
should be read as an execution of the six cases against the incumbent — that was
not possible, because the incumbent has no representation of the ordinary
purchase question.

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
4. [`docs/prototypes/reported-interest-tax-concept/examination.md`](../../prototypes/reported-interest-tax-concept/examination.md)
   — the executed comparison of the two shapes: case outcomes, rubric results,
   the two deciding probes, the recommendation, and the case against it. The
   [charter](../../prototypes/reported-interest-tax-concept/charter.md) states
   what the round set out to decide before it ran.

## Two production conditions, recorded and not addressed

The second is the dropped basis consequence, described above and classified
below. The first is the citation vocabulary.

`citation.v1` admits four authority families — U.S. Code, IRS form, IRS
instructions, IRS publication — as a closed set, and it is a published schema.
No Treasury Regulation can be cited.

For *this* slice that costs less than it first appeared. The authority on point
for the between-interest-dates purchaser is Publication 550, and the statute is
IRC § 61(a)(4); both are citable today. What cannot be recorded is the
seller-side corroboration in Treas. Reg. § 1.61-7(d), or the traded-flat
neighbour in § 1.61-7(c) that has to be distinguished to bound the account.

It remains a **condition on production use** for any proposition whose best
support is regulatory, which is a large share of them. Closing a published
closed set is a contract question, not a content change. It is a substrate
question about the citation citizen rather than a taxable-interest question, and
a candidate for a separate milestone. No citation schema is designed, versioned,
or proposed here.

## What is unresolved, and of what kind

Not everything open here is the same kind of open, and treating it as one list
would be misleading.

**Decision-blocking — must be settled before a representation is chosen.**
Whether a consequence that outlives the tax year must be **self-checkable**. If
a carried basis reduction has to be able to state, in the year of disposition,
the reported and includible amounts it is consistent with, the determination
shape is warranted and the distributed shape is out. If a bare amount keyed to
an item suffices — because the broker reports the reduced basis, or because the
user reconciles — the distributed shape is cheaper and the deciding probe loses
its force. This is a product question about what the year-of-disposition
experience owes the user, and no representation experiment can answer it.

**Production conditions — do not block the decision, do block shipping.** The
missing Treasury Regulation authority family in `citation.v1`. The absence of
any artifact carrying the basis consequence, which is silently correct in the
year it is dropped and wrong in the year of disposition.

**Separate decisions — real, but about something else.** Whether the substantive
authority stack should be attached to content that already has an
`irs-instructions` citation, which is a content-practice question and not a
schema one. Whether `f1099b-transaction` should be an economic event rather than
a statement row.

**Deferred breadth — deliberately out, not overlooked.** Every interest family
other than box 1; § 135, OID, market discount, bond premium, nominee ownership,
elections; the traded-flat pattern; joint-return subject identity; full line-2b
coverage.

## The smallest questions for the next milestone

The Tax Concept Representation Contract milestone should not open with "design
the determination citizen." The smallest questions that would decide whether one
is needed are:

0. **Where does a consequence that outlives the tax year live, and must it be
   self-checkable?** This is now the load-bearing question, and the
   recommendation depends on it. The basis reduction is the concrete instance.
   Ask it in its smallest form first: the covered-lot 1099-B fact types already
   carry a required `basis` field on a statement row, keyed by broker,
   statement, transaction and tax year, so if the broker reports the reduced
   basis in the year of disposition the engine may not need to carry the drop at
   all. Only one tax year is packaged, so this is an inference from the shape
   rather than an observed cross-year path — but it is cheap to settle, and
   settling it decides the representation.
1. **What does the product owe the user in the blocked state?** Detection is
   settled: the prototype executed TI-N1 and the evaluator distinguished "yes,
   amount supplied" from "yes, amount missing," blocking and naming the missing
   fact. Two things remain, and neither is an expressiveness question. The
   recorded blocked-code set is a closed enum in a published schema, so an
   honest new code means publishing a successor record schema, and reusing an
   old one misstates which condition fired. And a blocked disposition does not
   by itself put the outstanding ordinary question in front of the user.
2. **What is the cheapest representation that lets an adjustment name the item
   it reduces?** Re-keying to the statement identity is sufficient for
   *naming* and is compatible with the existing rule and composition checks. It
   does **not** by itself produce a per-item comparison; nothing joins two
   families on a shared identity. So the open part is the guard, not the key.
3. **What criterion does "explainable" have?** The prototype attached authority
   to a result and checked that it was recoverable, which is a criterion for the
   *shape* but not for the *product*. The committed explanation surface explains
   the subtraction, not the legal reason for it. Until there is a standard for
   what an explanation must let a reader recover, the explanation requirement
   can be satisfied trivially.
4. **Is an ordinary-question fact type distinct from its classified amount a
   general pattern or a one-off?** The package already asks ordinary questions:
   Schedule B Part III asks whether the taxpayer had a financial account in a
   foreign country, and the student-loan route asks whether the filer is legally
   obligated on the loan. Both are `{yes, no}` categorical assertions about the
   world rather than about a tax category. But both are keyed to the tax year
   and neither is attached to an item, and neither is followed by an amount the
   answer makes mandatory. So the precedent covers the *ordinary* half of the
   question and not the *per-item* half, which is exactly the half this slice
   needs.

Question 0 first: it is cheap, and it is the one the recommendation rests on.
Questions 1 and 3 are product questions rather than representation questions,
and both were mistaken for representation questions earlier in this milestone.
None is answerable on paper alone — which is the lesson of this milestone, not
an aside.

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
