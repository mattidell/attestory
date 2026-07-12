# Examination — Source-Family Semantics, repair 1

Paper/table examination; 2026-07-12. No code or production contract was built.

## SFS-P1 — settled at paper

The authoritative semantic content is a versioned family declaration: exact
closure claim plus canonical member predicate, with mapping, subtotal, and
coverage bound to it. The id/title/label is non-authoritative. Consumers must
pin/reference the declaration and present the exact claim or a separately
declared composition. Thus a box-1 predicate cannot gain taxable-interest
meaning through a consistent-but-misleading id, coverage rollup, or downstream
wiring.

The required shared mislabel attack now fails: a family called
`taxable-interest` with box-1-only members must either display the box-1 claim
or fail authoring because “all taxable interest” is not coextensive.

## SFS-P2 — settled at paper

A family subtotal carries its declaration/predicate. A final taxable-interest
result declares a required universe and accepts only an identical universe or
an explicit, proven-coextensive composition. Validation rejects a narrow
subtotal substituted for a broader final input merely by label or symbol.

The six original cases still hold:

| Case | Result |
|---|---|
| 1. No forms/no interest | B1 closure may publish only its empty subtotal zero. |
| 2. Two one-payer box-1 statements | Two logical statement instances remain two subtotal members. |
| 3. Non-form taxable interest | B1 is not the final universe; line 2b remains open. |
| 4. One form, boxes 1 and 3 | B1 selects only box 1; box 3 defeats document/final-universe substitution. |
| 5. Late statement after zero | The required result is stale closure/open coverage/noncurrent zero. |
| 6. Narrow closed, broad open | Exact B1 coverage may close while the final universe remains open. |

## SFS-P3 — unresolved at static-table depth

The ordered table establishes: true empty closure → current zero → relevant
late member assertion → stale closure/noncurrent zero/open coverage → new true
closure → explicit rerun; member correction displaces a present-member result;
member displacement/removal reopens the family.

ADR-0010 can displace a derived result when it pins a known input, including a
closure after that closure is superseded. It cannot displace an empty zero from
a later, previously unknown member: no pin or declared edge reaches it. Manual
closure withdrawal is therefore not an adequate production condition.

The smallest next decision is a record-derived closure-freshness currency
mechanism: a family membership frontier/horizon whose succession reaches
closure authority and closure-backed zeros through existing derivation or
individuation edges, with rebuildable currency and exact horizon pins. This
repair does not select its citizen, edge expression, schema, or implementation.

## Stop

No resolver/currency mutation is authorized or supplied. Statement
deduplication, full interest taxonomy, UI design, persistence, and production
implementation remain deferred.
