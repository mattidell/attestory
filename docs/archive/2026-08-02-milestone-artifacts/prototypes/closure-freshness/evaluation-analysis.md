# Prototype Evaluation Analysis — Closure Freshness

Foreman, 2026-07-12. Status: complete for Tier-3 owner disposition and ADR
drafting.

## Decision under evidence

How can a later family-member change make prior closure authority and dependent
closure-backed results noncurrent without manual closure withdrawal, derived
closure authority, stored staleness, or a third standing-affecting edge?

## Evidence

| Evidence | Contribution |
|---|---|
| `exhibits/closure-freshness/it1` (`3f98725`) | Incumbent computed-divergence/horizon paper shape |
| `exhibits/closure-freshness/it2` (`32e1312`) | Clean-room ordinary horizon-citizen successor shape |
| Round 1 reviews/triage | Reject incumbent unrecorded root; retain rival conditionally |
| `exhibits/closure-freshness/repair1` (`111579f`) | Atomic-transition contract and ordered act-log reducer |
| Round 2 reviews/triage | Two-edge/rebuild convergence; bounded validation/encapsulation conditions |

## Supported conclusions

### C1 — Closure freshness is relative to a recorded family horizon

Each source-family declaration/version and scope has an ordinary membership-
horizon citizen with a succession history. A closure fact is keyed on the
specific horizon current when the user attests completeness. The true finding
remains user-attested; the horizon does not compute closure truth.

### C2 — Membership-changing transitions atomically advance the horizon

Adding/removing a relevant member or changing whether an existing member
satisfies the canonical family predicate must, in the same accepted recorded
transition, create exactly one successor horizon for the same family/scope and
name the current predecessor. Missing, replayed, future, global, mis-scoped, or
wrong-predecessor successors make the whole transition invalid.

A same-member value correction that leaves predicate membership unchanged does
not advance the horizon; its dependent subtotal currency follows the known
member finding's ordinary derivation edge.

### C3 — Currency uses only individuation then derivation

Recorded horizon succession is an ADR-0010 individuation root. Because the
closure fact is keyed on the predecessor horizon, succession displaces that fact
and its current finding through individuation. A closure-backed zero pins the
exact closure finding and becomes noncurrent through its existing derivation
edge. There is no member→zero edge, listener, computed root, stored stale flag,
manual closure withdrawal, or derived closure finding.

The clean-room rival states this structure more completely than the incumbent;
round-1 adversary rejects the incumbent's comparison-derived root.

### C4 — Currency is record-derived, monotonic, rebuildable, and isolated

The repair reducer accepts an ordered synthetic act log and exposes recorded
superseded-horizon roots plus individuation/derivation maps. Incremental currency
equals full replay after every accepted act. Later removal cannot erase roots or
resurrect an old zero. Only new true re-attestation and explicit rerun may
publish a successor. Horizon identity includes exact family declaration and
scope, so changing one family does not affect another.

Repair tests pass; all round-2 reviewers reproduce the core result. Governance
finds no third edge or reserved T1 authority. Adversary finds no admitted-log
bypass. Expressiveness finds ordinary validation gaps, preserved below.

## Rejected alternatives

- Manual closure withdrawal: correctness cannot depend on optional follow-up.
- Derive `closure=false`: computation cannot replace user attestation.
- Compare current membership and inject a stale root: disguised third edge.
- Stored staleness/current flags or side listeners: violates record-derived
  currency and E7.1/E7.2.
- Direct member→zero dependency: undeclared third relation.
- Global horizon: breaks family isolation.

## Production conditions and exclusions

Production must define schema/version identity, actor-bearing atomic act,
transaction revision/order, strict nonempty ids, current-horizon validation,
family-declaration/predicate binding, immutable/encapsulated projection state,
and replay/idempotence. It must repeat all malformed-transition, rebuild,
resurrection, and isolation tests against registered act kinds.

The prototype does not adopt schema bytes, edit governance text, implement tax
content, or approve caller-created horizon authority. Prototype code is evidence
only.

## Dissent

Round-1 adversary correctly withholds convergence until the horizon producer and
replay mechanism are executable. Repair1 supplies that bounded evidence.
Round-2 expressiveness dissent on `None`/empty ids and validation completeness is
upheld as a production condition; no conclusion claims bulletproof input
validation.
