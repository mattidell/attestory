# Examination: Iteration 1 — Incumbent Closure-Freshness Design

Date: 2026-07-12. Incumbent builder, paper only, under `charter-it1.md` /
approved Tier-3 `plan.md`. Branch `prototypes/closure-freshness/it1`; design at
`it1/design.md`.

## What was built

One record-derived paper design in which a later relevant family-member act makes
prior closure authority stale and every closure-backed zero that used it
noncurrent, **without manual closure withdrawal**, classifying every standing
effect as an existing derivation or individuation relation:

- **Membership horizon** (CF-P1): a closure attestation declares `H`, the
  family-scoped act-log position at attestation; it is fresh only while
  `current(F) ⪯ H`. Any later member assert/membership-correction/removal
  advances F past `H` → stale until re-attestation.
- **Two-edge currency** (CF-P2): member act → `F-membership(F)@H'` supersedes the
  attested `@H` (**individuation** root, an existing ADR-0010 root class) → `C`
  displaced → `C → Z` (**derivation** edge, `Z` pins `C`). No member→`Z` edge is
  needed.

Grounded on Article 7 (no third edge), ADR-0010 (roots = superseded inputs +
individuated entities; derived findings are targets), and the ratified
source-family contract.

## Required cases — all six/seven resolved (design.md table)

1 publish fresh zero; 2 new member → zero **noncurrent** (no withdrawal);
3 same-member correction displaces only the subtotal, **no family reopen**;
4 removal → **no resurrection** (monotonic horizon keeps it stale); 5 re-attest →
fresh, rerun publishes successor `Z1` pinning `C'`; 6 act-log rebuild equals
incremental currency; 7 two families isolated (roots are per-family).

## Negatives and the rejected rival

- **New member with no manual withdrawal** (neg 1): horizon divergence displaces
  `C` by individuation; `Z0` noncurrent via `C→Z0`.
- **Removal does not resurrect** (neg 2): horizon is a monotonic position, not a
  set-equality test, so restoring emptiness does not refresh `C`; `Z0` stays
  displaced (Article 6/7 — history accumulates).
- **Rival worked to failure:** "re-derive closure to `false` when members appear"
  fails on Article 2/3 — closure is a user attestation; a rule cannot make its
  negation operative by computation. This forecloses the derivation-only route
  and shows the individuation horizon is load-bearing, not decorative.

## Pins, edges, map

Exact pins recorded (design.md): `Z0` pins `C@v1`; when stale its walk reaches
`C@v1` shown displaced by `F-membership(F)@pos1`; `Z1` pins `C'`, never the stale
`C`. Full derivation/individuation edge inventory and the
producer→authority→edge→currency-consumer→failure map are in design.md; every
standing effect is one of the two edges.

## CF-P1 — reported independently

**Settled at paper.** Horizon-relative freshness is observable and rebuildable
from acts (`fresh(C) ⇔ latest F-member-act ⪯ H`); ids/labels/coverage cannot
widen or reset it; re-attestation is the only fresh-making act. No governance
conflict: it displaces an attestation by individuation of what it was attested
over, never re-authoring the user's claim.

## CF-P2 — reported independently

**Structure settled at paper; needs a tiny reducer (Gate-3 depth 1) — not a
third edge, not reserved authority.** The propagation to `Z` uses only the
existing individuation and derivation edges. The one real requirement: because a
bare absence cannot be a displacement root, currency must **positively compute**
per-family horizon divergence (`current(F) ≻ H`) and feed it to the existing
individuation-root set. That is a small act-log/currency reducer — the authorized
next depth for CF-P2. It adds **no** third standing-affecting edge and asserts
**no** reserved T1 derived-finding authority, so the design does **not** fail; it
concludes with a scoped reducer finding.

Single open question that alone would justify the climb: *does a reducer that
flags `current(F) ≻ H` as an individuation root reproduce the table's currency
verdicts on rebuild, with no resurrection and per-family isolation?* — the exact
CF-P2 depth-1 charter, if the owner authorizes it.

## Disposition / handoff

CF-P1 settled at paper; CF-P2 settled in structure with a named tiny-reducer
finding. Stop condition honored — no reducer, schema, runner, or persistence
built; the reducer is a finding, not taken. Recommend: a clean-room rival on the
same seven cases (per Gate 4) before any committee, then decide the CF-P2 reducer
depth. Excluded matter (statement dedup, interest taxonomy, UI, coverage display,
production ids) untouched. Committed on this branch only; integration, exhibit
tagging, and rival dispatch are the foreman/owner's.
