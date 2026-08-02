# Prototype Evaluation Analysis — Source-Family Semantics

Foreman, 2026-07-12. Status: complete for owner disposition and bounded ADR
drafting. SFS-P1/P2 are supported; SFS-P3 is explicitly excluded.

## Decision under evidence

This analysis asks:

1. what content carries a source family's closure meaning;
2. when a closed narrow family may feed a broader tax result.

It does not decide how a later previously unknown member makes closure authority
and an existing closure-backed zero noncurrent.

## Evidence

| Evidence | Contribution |
|---|---|
| `exhibits/source-family-semantics/it1` (`5ef3435`) | Five-part versioned B1 declaration; narrow subtotal outcome |
| `exhibits/source-family-semantics/it2` (`f48a102`) | Clean-room closure-domain/composition rival |
| Round 1 reviews/triage | Shared mislabel and late-trigger failures |
| `exhibits/source-family-semantics/repair1` (`b38f131`) | Exact claim+predicate authority; explicit composition; late-state table |
| Round 2 reviews/triage | SFS-P1/P2 convergence; SFS-P3 reserved-boundary escalation |

The rival requirement is satisfied: separate builders independently exercise
the same six cases at paper depth.

## Supported conclusions

### C1 — Family meaning is a versioned exact claim plus canonical predicate

A source-family declaration carries the exact closure claim and canonical
member predicate. Its opaque id, title, shorthand, rule symbol, or UI label is
not semantic authority. Mapping, calculation, and coverage reference/pin the
declaration. Coverage presents the exact claim or an explicit reference to it;
shortened wording cannot broaden completion.

Evidence: both rivals keep B1 distinct from taxable interest; round-1 adversary
defeats their original narrative naming defenses; repair1 makes claim+predicate
jointly authoritative; both round-2 reviewers find the consistent-mislabel and
rollup substitutions resisted at paper level.

### C2 — Narrow closure authorizes only its matching subtotal

A derived subtotal carries its source-family declaration/predicate. A broader
final result declares its required universe and accepts only an identical
universe or an explicit composition whose component predicates are established
as coextensive with that required universe. Labels and symbols cannot substitute
for universe compatibility.

Therefore closure of 1099-INT box-1 statement items may authorize only the B1
subtotal, including an empty subtotal zero. It cannot directly authorize Form
1040 line 2b zero. Non-form taxable interest and box 3 are concrete
counterexamples.

Evidence: all six cases in both rivals; repair1 composition contract; unanimous
round-2 SFS-P2 disposition.

## Rejected alternatives

- Treat all 1099-INT documents as one taxable-interest family: box 3 and other
  boxes defeat the member predicate.
- Treat B1 as coextensive with taxable interest: non-form taxable interest
  defeats it.
- Let ids, labels, or symbols carry family meaning: consistent mislabeling
  defeats internal alignment.
- Let a downstream rule implicitly promote a subtotal: it hides an open broader
  universe and can falsely publish line 2b zero.

## Excluded Tier-3 boundary — late-member freshness

The required observable result is clear: a relevant later member makes the old
closure stale, the closure-backed zero noncurrent, and coverage open until
re-attestation and explicit rerun. Existing ADR-0010 derivation edges cannot
produce that result because the old empty zero cannot pin a future member.

A record-derived family frontier/horizon may touch the Ontology's reserved T1
derived-finding authority construction or require a new standing-affecting
relation contrary to Article 7's “no third edge” constraint. This analysis does
not select or authorize that machinery. It requires a separate Tier-3 prototype
and ADR before closure-backed zero ships.

## Production conditions

- Publish schema-first family declarations and structural negatives.
- Validate exact-claim/predicate binding across mapping, subtotal, coverage, and
  final-result composition.
- Present or reference the exact coverage claim; shorthand is non-authoritative.
- Keep statement identity peer to evidence under ADR-0015.
- Do not implement closure-backed interest zero until the Tier-3 freshness
  boundary is ratified.

Prototype ids/content are evidence only.
