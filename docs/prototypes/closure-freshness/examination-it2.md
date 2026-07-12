# Examination — Closure Freshness, Iteration 2

Status: clean-room rival paper examination.  This review measures the charter's
seven cases against Article 7's two declared displacement relations and the T1
boundary.  It does not approve implementation.

## Result

CF-P1 is settled in paper: a closure claim is current only at its declared,
current source-family horizon.  CF-P2 is structurally expressible but needs a
tiny reducer before it can be treated as evidence of rebuildable currency.

The design places the closure fact's horizon in fact identity.  A member-change
act supersedes that horizon; Article 7 individuation displaces the old closure
fact and its true closure finding; the existing derivation pin from that finding
displaces the old closure-backed zero.  This is a two-hop cascade, not a new
edge.  It does not use derived authority: the horizon is an ordinary asserted
citizen and the zero's authority remains the attested closure plus adopted
artifacts.

## Measurements

| Charter case | Paper result | Relation exercised |
| --- | --- | --- |
| fresh empty zero | true current closure at `H0` supports `Z0=0` | derivation |
| later new member | `H0 → H1` displaces `C0/K0`, then `Z0` | individuation → derivation |
| same-member correction | `V1 → V2` displaces only outputs that pin `V1` | derivation |
| removal / no resurrection | `H1 → H2` leaves old closure/zero historical; `C2` is open | individuation → derivation |
| re-attestation / rerun | true `K2` permits a distinct `Z2` | new derivation, no cascade-based resurrection |
| rebuild = incremental | expected from the ordered act walk | requires reducer proof |
| two-family isolation | different `(family, scope)` horizons have no path | absence of edge |

## Required reducer probe

Use synthetic acts only.  It must project horizons, closure facts/findings, and
zeroes from an ordered log; compute the complete closure of both edge kinds; and
compare incremental projection with a fresh rebuild after each act.  Assert:

1. `H0/K0/Z0` are current after an empty true closure.
2. A member-change act creating `H1` makes all three noncurrent without an
   explicit false/withdrawal closure act.
3. A same-member value correction does not advance `H1`.
4. A removal successor `H2` cannot restore `Z0`.
5. Family B remains current while only family A advances.
6. Reject a relevant-member act that omits its family-horizon successor.

## Boundary finding

No governance conflict is identified on paper.  The only material new contract
is the member-change act's obligation to supersede the relevant family horizon.
If that obligation cannot be expressed as one complete recorded transition, the
design fails: a side listener, stored staleness bit, or reverse invalidation
would violate E7.2; a derived membership authority would cross reserved T1.

The prototype stops here.  A reducer, if commissioned, is evidence only and
does not authorize schema, runner, persistence, or governance changes.
