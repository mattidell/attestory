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

**Necessity is not established. No representation is recommended on necessity
grounds.** Four packagings were run on the same six cases through the engine's
real expression evaluator. The comparison is
[`docs/prototypes/reported-interest-tax-concept/examination.md`](../../prototypes/reported-interest-tax-concept/examination.md),
exhibit `exhibits/reported-interest-tax-concept/it6`.

- **A — artifact-alone.** Independent artifacts, payload `{amount}` only.
  Includible and basis are separate evaluator runs.
- **C — embedded-composite.** Same two evaluations; the carried basis artifact
  also holds copied `reported` and `includible` amounts, each with the
  provenance of the evaluation that produced it.
- **E — relationship-edge.** The carried artifact holds `sibling` and
  `reported_key` pointers, not partition amounts. Following them requires an
  object store whose targets match self-key, item, kind, and exact producing
  rule id/version. Object-store access recovers the recorded partition; it
  does not establish currentness.
- **B — explicit determination.** One item-level result holding the amounts
  together.

Arithmetic does not discriminate. All four produce every required number, or
the same explicit refusal, on all six cases.

A later-year consumer performs six recovery tasks under four in-memory object
grants (artifact-object-only; currentness; object-store access; full-workspace).
The exhibit does not execute serialization or persistence. Artifact-object-only
never detects an amendment. Task 5 recovers the recorded partition explanation.
Task 6 is `fact_version_current` of the dependencies actually used; it does not
decide general usability, nor rule, authority, coverage, or reporting
succession. Task 5 true with task 6 unknown means a recorded explanation is
recoverable but currentness is unknown. Task 5 true and task 6 false means the
recoverable explanation is historical. Both are required before this
publication calls the result a current explanation under the prototype's
bounded assumptions. An unamended fixture is harness knowledge, not a consumer
capability.

A copied or referenced partition cannot support a current explanation after a
producing evaluation is displaced. That is settled. After a reported-amount
correction, C's basis amount can remain current while its copies are a
historical recorded explanation; B is wholly displaced. C and B with
artifact-object-only recover the recorded partition but cannot establish
currentness. E recovers the recorded partition through object-store access to
targets whose self-key, item, kind, and producing rule id/version match; that
access does not establish currentness. A recovers the recorded partition only
with the full source-year workspace.

Those differences do not establish that a new citizen kind is necessary.
Production cost was not measured. The source report is independent of
tax-slice coverage and of tax authority: its support is the exact statement
reads; tax authority and accrued-interest coverage are omitted. On TI-A1 the
treatment refuses and the reported $840 remains.

## What else is established

**The modelled domain is a domain of documents.** In the 2025 US-federal content
package, every declared entity kind is a document, a party in its role as issuer
of a document, a row within a document, or engine infrastructure. There is no
obligation, no account, no purchase, no disposition. The accrued-interest
circumstance is a fact about a purchase, so it had nowhere to live and was filed
as a **row on Schedule B**.

Three consequences follow:

- **The ordinary fact cannot be supplied, only the classified conclusion.** The
  engine can be told "$300 of accrued-interest adjustment." It cannot be told
  "I bought this bond on 15 May and paid the seller $300 for interest that had
  already built up."
- **An adjustment cannot name the item it reduces.** Reported amount and
  adjustment meet only as scalar subtotals inside the line-2b rule.
- **The proposition is labelled, not asserted.** A reader can recover the
  reporting category. They cannot recover the claim that such interest is not
  the purchaser's income because it is a return of capital, nor that it reduces
  basis, nor on what authority.

On TI-N1 the evaluator blocked with `DEPENDENCY_ABSENT` and named the missing
accrued-amount fact. Source and circumstance corrections displace exactly the
artifacts whose provenance reads the corrected fact. Rule, authority,
coverage-declaration, and reporting-artifact succession were not executed.

**TI-A1 is an outside-slice coverage probe**, not a proof that the incumbent's
published number is wrong for that taxpayer. The fixture records box-3 Series
EE interest and an education-expense answer. That is enough for the prototype
to refuse coverage. It is not a complete § 135 pattern. The incumbent's
selected line-2b v4 takes box 3 as an addend and does not pin Form 8815 or
§ 135; no committed rule computes the exclusion. So the incumbent cannot
determine whether an exclusion applies and may publish full inclusion without
representing the statutory conditions. `tax.us.2025.ss-benefits-scope.no-form-8815`
exists as a Social Security Benefits Worksheet completeness fact, not a line-2b
consumer.

Claims about incumbent behaviour are graded: exact execution of committed
tests; a structural analogue at different amounts; artifact inspection. The six
semantic cases were not posed to the incumbent.

## What this milestone is and is not

It is a completed executable vertical slice whose current evidence is exhibit
`it6`. It does not select a production representation, schema, citizen kind,
field shape, storage mechanism, ADR, or migration.

## Reading order

1. [accrued-interest-item-model.md](accrued-interest-item-model.md) — the five
   propositions, official-source treatment (Pub. 550 against IRC § 61(a)(4)),
   and the reporting/basis split.
2. [incumbent-representation.md](incumbent-representation.md) — what the
   existing artifacts represent.
3. [synthetic-case-specification.md](synthetic-case-specification.md) — six
   cases holding the reported amount constant.
4. [`examination.md`](../../prototypes/reported-interest-tax-concept/examination.md)
   — the executed comparison. The
   [charter](../../prototypes/reported-interest-tax-concept/charter.md) states
   what the round set out to decide.

## Two production conditions, recorded and not addressed

`citation.v1` admits four authority families and cannot cite a Treasury
Regulation. For this slice the authority on point is Publication 550 and
IRC § 61(a)(4), both citable. The missing regulation family remains a
condition on production use for propositions whose best support is regulatory.

No committed artifact carries the basis consequence into a later year.

## What is unresolved

**Decision-blocking.** A copied or referenced partition cannot support a
current explanation after a producing evaluation is displaced. Remaining
product questions concern the split state: recompute, retain as historical,
withhold, or decide whether an independently current basis amount supports a
named later-year task. The exhibit measured in-memory object grants, not
durable storage. Rule, authority, coverage, and reporting succession remain
outside the executed currentness service.

**Production conditions.** Missing Treasury Regulation family in `citation.v1`.
No artifact carrying the basis drop into the year of disposition.

**Open and unexecuted.** Rule, authority, coverage-declaration, and
reporting-artifact succession.

**Deferred.** Every interest family other than the box-1 slice; a § 135
computation; OID, market discount, bond premium, nominee, elections; joint
return subject identity.

## The smallest questions for the next milestone

0. **Which later-year capabilities does the product grant?** Ask first whether
   a covered-lot 1099-B already carries reduced basis as a statement field; if
   the broker reports it, the engine may not need to retain the drop.
1. **What does the product owe the user in the blocked state?** TI-N1 named the
   missing fact. Putting that question in front of the user, and whether a new
   blocked-code is a published-schema successor, remain product questions.
2. **What lets an adjustment name the item it reduces?** Re-keying can name; it
   does not by itself produce a per-item comparison.
3. **What must an explanation recover?** Until there is a product standard, the
   explanation requirement can be satisfied trivially.

## Scope

US-federal individual income tax, tax year 2025, one synthetic taxpayer, one
logical Form 1099-INT box-1 amount, one obligation purchased between interest
payment dates. A second synthetic statement carrying a box-3 savings-bond
amount exists solely as an out-of-slice coverage probe. All identities and
amounts are demonstration values.
