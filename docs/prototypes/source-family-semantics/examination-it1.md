# Examination — Source-Family Semantics, iteration 1

Paper examination; 2026-07-12. This examines the incumbent design only.

## SFS-P1 — settled at paper

The design declares one narrow family, `2025 1099-INT box-1 statement items`,
once across its claim, member universe, adopted mapping, calculation consumer,
and coverage consumer. A closure says only that every member in that declared
universe has been accounted for. The mapped calculation is a box-1 subtotal;
coverage reports that same narrow completion. A closure cannot silently widen
to the taxable-interest concept or Form 1040 line 2b.

Case evidence:

| Case | Result |
|---|---|
| 1, no forms/no interest | Narrow true closure authorizes only the empty box-1 subtotal zero. |
| 2, two one-payer box-1 statements | ADR-0015 statement instances remain two members; current aggregation is positive `$20`. |
| 3, non-1099 taxable interest | The `$9` item proves the narrow closure is not coverage of taxable interest or authority for line-2b zero. |
| 4, one form boxes 1 and 3 | `$7` box 1 is a subtotal member; `$5` box 3 prevents any claim that the subtotal is all taxable interest. |
| 5, late statement after zero | Withdrawal/displacement removes the pinned zero; explicit rerun publishes present-source result and coverage reopens. |
| 6, narrow closed/broad open | “Box-1 statement items complete” is valid; “taxable interest complete” is not. |

The positive outcomes are empty narrow subtotal zero and two-statement
aggregation. The required negatives are non-form interest and box-3/broad-line
substitution. The rejected `taxable-interest = box-1 members = line 2b` rival
fails both negatives because its claim and result are broader than its members.

## SFS-P2 — settled at paper, bounded

Box-1 statement items, the full taxable-interest concept, and line 2b are
explicitly distinct universes. Official IRS materials say line 2b is total
taxable interest, direct taxpayers to include other taxable interest even
without Form 1099-INT, and generally add box 3 to other taxable interest.
See [2025 Form 1040 instructions](https://www.irs.gov/instructions/i1040gi)
and [Publication 550](https://www.irs.gov/publications/p550).

Accordingly, a closed box-1 family may authorize a **subtotal zero only**; it
may not directly authorize a Form 1040 line-2b zero. This is a semantic result,
not a claim to have designed all taxable-interest content.

## Boundary and unresolved questions

No resolver table is needed: the six static cases make the universes
extensionally clear. A tiny resolver table would be needed only to test a
future composition rule that combines a closed narrow subtotal with other
families while deciding line-2b publication.

Deferred: full taxable-interest member taxonomy; other 1099-INT boxes beyond
the case-4 counterexample; manual-entry product design; coverage persistence;
UI copy; Schedule B; production ids/schemas; and any implementation. The cited
IRS sources motivate the distinctions but do not select production artifacts.
