# Governance Review — Closure Freshness Round 1

Date: 2026-07-12
Seat: governance reviewer
Scope: CF-P1 and CF-P2, measured against `round-1.md`, the governance set,
and ADR-0009/0010/0011/0014/0016. This review does not authorize a reducer or
production implementation.

## Determination

Horizon succession is legitimate individuation in both paper designs, but
only under the designs' explicit, still-to-be-contracted condition: a relevant
member-change act must atomically create/advance a declared, family-scoped
horizon citizen and thereby supersede the prior horizon. The old closure fact
is keyed on that horizon; its finding is then displaced as an individuated
dependent, and the zero is displaced through the already declared derivation
pin from the closure finding.

That is not a third edge. It is an instance of the Ontology's existing
individuation semantics and ADR-0010's existing root class, followed by the
ordinary derivation edge. The horizon is not itself a derived authority and
must not be a hidden freshness bit, listener target, reverse-invalidation
record, or direct member-to-zero dependency.

The distinction is load-bearing. A reducer that merely compares a current
membership observation with a stored horizon and marks the old zero stale
would be a disguised third standing mechanism unless that comparison is only
the record-derived way of discovering the already declared horizon
individuation root. The reducer may compute currency; it may not introduce a
new relation or mutate standing state.

CF-P1 is settled semantically at paper. CF-P2 is structurally legitimate but
not yet evidenced as rebuildable currency: it requires the bounded reducer
probe specified by the examinations. Closure-backed zero remains blocked until
that probe and the later contract work pass.

## Governance basis

- Article 7 permits displacement only along derivation and individuation edges
  and requires currency to be derived from the record. E7.1 forbids stored
  current/stale flags; E7.2 requires every cascade path to map to a declared
  edge.
- The Ontology defines a fact as an enduring question identity, allows facts
  to be individuated by keyed-on citizens, and distinguishes correction of an
  answer from succession that changes the questions. Its cascade semantics
  explicitly allow an individuating citizen's succession to displace the
  facts, findings, and derived outputs that depend on it.
- ADR-0010 makes superseded inputs and individuated entities displacement roots,
  keeps derived findings as targets rather than roots, and permits a composed
  currency layer to contribute only declared derivation edges.
- ADR-0011 keeps closure an affirmative, user-attested determinable fact.
  ADR-0014 requires exactly one current literal-`true` closure finding for a
  pinned adopted mapping. ADR-0016 expressly leaves late-member freshness as
  a separate Tier-3 boundary and forbids a frontier, derived authority citizen,
  or new standing-affecting edge.

## Rival measurements

| Measurement | Incumbent it1 | Clean-room rival it2 | Governance result |
|---|---|---|---|
| Empty family, true closure, zero | `C@H0` supports `Z0`; `Z0` pins the exact closure finding. | Same, with explicit `H0`, `C0`, `K0`, `Z0`. | Passes; authority remains the user's attestation plus adopted mapping/rule. |
| Later relevant member | The family horizon advances; divergence displaces `C`, then `C→Z`. | The member-change act must establish `H1`; `H0` supersedes and cascades through `C0/K0→Z0`. | Passes on paper; the successor act is mandatory, not optional metadata. |
| Same-member correction | Member value derivation displaces the subtotal only; membership horizon does not advance. | `V1→V2` displaces only subtotals pinning `V1`; no horizon change. | Passes; no unnecessary family reopening. |
| Removal/displacement | Monotonic horizon keeps the old zero noncurrent even if the set becomes empty again. | `H2` supersedes `H1`; the old closure and zero remain historical. | Passes; no resurrection. |
| Re-attestation and rerun | New `C'` at the later horizon and explicit rerun publish `Z1`; old `Z0` stays displaced. | New `K2/C2` and rerun publish `Z2`; no cascade-based resurrection. | Passes; fresh authority is an assertion, not computation. |
| Rebuild equality | Claimed from folding acts and recomputing divergence; examination identifies this as reducer work. | Claimed from ordered replay; examination requires a reducer. | Unproven for both; required CF-P2 evidence. |
| Family isolation | Roots are keyed per family. | Horizon identity is `(family declaration, scope)`; no global horizon. | Passes on paper; global/shared horizon would fail. |

The exact explanation shape is also sound: the zero names the exact true
closure finding, which names the closure fact and its horizon; the horizon's
member-change provenance explains why the old closure is displaced. Family
declaration, mapping, rule, adoption, and governance pins remain provenance,
not currency edges. Neither design pins an absence or an unknown future member.

## Edge classification

The legitimate path is:

`member-change act → successor horizon citizen`

`successor horizon supersedes/individuates prior closure fact → prior closure finding`
`closure finding → closure-backed zero` (ordinary derivation pin)

The first two lines are one declared individuation structure, not a new
membership-to-result edge. The last line is the already accepted derivation
edge. Same-member value correction remains an ordinary derivation path to a
present-member subtotal and is not allowed to advance the family horizon.

The it2 design is the clearer governance expression because it makes the
horizon a first-class ordinary citizen, gives the closure fact an identity key
over it, and requires the member-change transition to publish the successor.
The it1 design reaches the same legitimate result, but its notation
`F-membership(F)@H` and its instruction to the reducer to “treat divergence as
the individuation root” leave a contract risk: if no horizon citizen and
supersession act exist, that instruction is direct computed invalidation, not
individuation. The reducer must discover the root from the act record, never
invent it from a side comparison.

## Authority and reserved-boundary checks

Both designs preserve user-attested closure. Neither re-derives closure to
`false` when a member appears, which would make computation resolve or
withdraw the user's assertion and violate Articles 2 and 3. A later member
change makes the old attestation inapplicable by succession of what it was
attested over; it does not alter the old finding or fabricate a contrary one.

Neither design needs T1 derived-finding authority. The horizon must be an
ordinary asserted/recorded citizen or an ordinary citizen whose existence is
established by the complete member-change act; it cannot be a derived finding
that authoritatively says the family has changed. Derived zeroes remain
displacement targets, never roots, as required by ADR-0010.

## Required reducer evidence

The next evidence step is the small synthetic reducer, not a production runner.
It must rebuild horizons, closure facts/findings, zeroes, and both edge closures
from the ordered act log, and compare that result with incremental projection
after each act. At minimum it must prove:

1. `H0/K0/Z0` is current after empty true closure.
2. A member-change act with `H1` displaces the old closure and zero without an
   explicit withdrawal or false closure act.
3. Same-member correction leaves the horizon unchanged.
4. Removal creates a later horizon and cannot restore `Z0`.
5. Family B remains current when only family A advances.
6. A relevant member change lacking its required horizon successor is rejected
   as an invalid transition, rather than repaired by a listener or staleness
   flag.

The reducer must expose the root and edge classification in its result so that
E7.2 can inspect cascade equality. Failure of any of these checks means the
paper proposal has not established CF-P2; it does not justify adding a third
edge or reserved authority doctrine.

## Recommendation

Accept CF-P1 as the semantic direction: closure is fresh only relative to a
declared family-scoped membership horizon, and re-attestation is required
after any later relevant member act. Carry CF-P2 forward only as a conditional
structure pending the reducer evidence and an explicit Tier-3 contract for the
horizon citizen, its identity, and the atomic member-change transition. Do not
ship closure-backed zero, amend governance text, or treat either paper exhibit
as production schema until those conditions are met.
