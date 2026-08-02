# SC-P3 — Source Family Definition (incumbent design, it1)

Rung 1, paper. Stated once, exercised by the SC-P1 and SC-P2 instances; no
separate fixtures (plan Gate 2).

## Definition

A **source family** is a named scope over a member fact type:

```
source_family := (member_fact_type, scope)
identified by an opaque string name, e.g. "tax.us.2025.interest"
```

- The name is *exactly* the string a `collect` node carries as `source_set`
  (`evaluator.py:115`, `rule.wages-line1a.json` `"source_set":"tax.us.2025.w2"`),
  *exactly* the `source_family` key of a `source-closure-mapping.v1` entry
  (SC-P1), and the unit the coverage read model reports over (milestone Track 4).
  One string, three consumers — no second definition, no second store
  (Article 5).
- **Membership is derived, never stored:** the current findings of
  `member_fact_type` within `scope`. A family with zero current members is still
  a well-defined family — that is what makes a closure-backed *empty* zero
  meaningful (SC-P1 (a)). Coverage (open vs. closed) is computed fresh from
  records (Article 14: "coverage available now is computed fresh").

## Why it is compatible with the SC-P2 identity key

The family is defined by `(member_fact_type, scope)`, **not** by any member's
identity key. So:

- `tax.us.2025.interest` = (`tax.us.2025.interest.box1`, {tax_year 2025, …}).
  Its members are individuated by payer+account+tax-year (SC-P2), but the family
  itself names none of them. Adding a second account adds a member; it does not
  change the family.
- `tax.us.2025.w2` = (`tax.us.2025.w2.box1-wages`, {tax_year 2025, …}); members
  keyed by employer+slip+tax-year (ADR-0011).

The closure fact type keys on the family's scope only (tax-year), never on a
member — so closure and per-instance identity never collide, and a closure
finding is authority over the *family*, admitted into `closed_sets` under that
one name by the SC-P1 mapping.

## Disposition intent

SC-P3 produces no artifact of its own. It ratifies as a **definition inside**
the SC-P1 (mapping) ADR — the mapping's `source_family` field *is* this name —
rather than as its own ADR (plan Gate 6). It is stated here so both the mapping
and the coverage read model consume one word for one thing.
