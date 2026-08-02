# Charter: Repair Pass 1 — Claim Authority and Late-Member Freshness

Date: 2026-07-12. Foreman-authorized after round-1 triage.

- **Branch:** `prototypes/source-family-semantics/repair1`
- **Builder:** incumbent it1 builder, deliberate continuity, High/high.
- **Scope:** SFS-P1/P2 semantic repair plus SFS-P3 late-member freshness.
- **Evidence by question:** SFS-P1/P2 remain paper; SFS-P3 gets a static
  state/currency table. No code, evaluator, production schema, UI, or persistence.

## Questions

1. What declaration is authoritative for a family's claim and member predicate,
   so a narrow box-1 family cannot gain broader meaning through its id, label,
   coverage rollup, or downstream wiring?
2. What explicit composition contract distinguishes a closed subtotal from a
   final taxable-interest result?
3. When a relevant member is asserted after a true closure and closure-backed
   zero, what makes closure stale and the old zero noncurrent—without assuming a
   human happens to withdraw closure?

## Required evidence

- Repair both paper rivals' shared mislabel attack: consistently box-1 members/
  mapping/coverage under a misleading “taxable interest” name.
- State which field/content is semantic authority and what consumers must
  present verbatim or reference; names and UI shorthand cannot broaden it.
- Declare subtotal versus final-result composition and the validator failure
  when a narrow family is substituted for a broader input universe.
- Static ordered table for: true closure on empty family → zero; later member
  assertion; state before user re-attestation; re-attestation true; member
  correction; member displacement/removal. For every state show effective
  closure, zero currency, coverage, and required act/edge.
- Identify whether existing ADR-0010 derivation edges can make the old zero
  noncurrent. If not, name the smallest separate machinery decision rather than
  pretending the semantic contract implements it.
- Re-run all six original cases and report SFS-P1, SFS-P2, and SFS-P3
  independently.

## Outputs

- `docs/archive/2026-08-02-milestone-artifacts/prototypes/source-family-semantics/repair1/design.md`
- `docs/archive/2026-08-02-milestone-artifacts/prototypes/source-family-semantics/examination-repair1.md` (≤120 lines)

## Stop

Stop after paper/table evidence. A need for a resolver or currency mutation is a
finding and possible next depth for SFS-P3 only. Do not absorb statement
deduplication, full interest taxonomy, UI design, or production implementation.
