# Examination — Recorded Horizon Reducer Repair 1

Status: bounded synthetic reducer evidence, not production approval.

## Result

The selected rival shape passes the reducer probe.  An ordinary recorded
family/scope horizon successor is a valid individuation root: it displaces the
closure finding on the fact keyed by its predecessor horizon, and the existing
closure-finding derivation pin then displaces the zero.  Incremental currency
equals full replay after every accepted synthetic act.

## What was measured

`python3 -m unittest test_reducer.py` runs the reducer's ordered synthetic log.
It establishes fresh F and G zeroes; adds an F member; performs a same-member
value correction; performs a predicate-changing correction; adds/removes a
second member; and re-attests/reruns F.  Each prefix compares incremental
currency to full rebuild.

| Required case | Measured result |
| --- | --- |
| Fresh zero | `K0 → Z0` is current at `H0`. |
| Late member | `H0` is a record-derived root; `H0 -individuation→ K0 -derivation→ Z0`. |
| Value correction | no successor; horizon/currency unchanged. |
| Predicate correction | required `H1 → H2` successor; old authority stays displaced. |
| Removal/no resurrection | later successors never remove roots; `Z0` remains displaced. |
| Re-attestation/rerun | only `K4` plus explicit `run_zero` publishes `Z4`. |
| Two-family isolation | F successors do not affect current `KG0/ZG0`. |

## Negative and mutation evidence

The suite rejects: missing successor; fabricated future closure horizon;
mis-scoped and global horizons; replayed successor; half removal; derived
closure; and caller staleness fields.  Two test-local mutants are killed:

1. An add with its horizon successor omitted is rejected before it can enter
   the log.
2. Direct root injection is impossible because `currency` accepts only state;
   a caller stale flag is rejected as an unknown authority field.

## Edge audit and residual question

The reducer exposes only roots from recorded superseded horizons and two maps:
`individuation` from horizon to closure finding, and `derivation` from closure
finding to zero.  It has no member-to-zero map, listener, stored freshness bit,
or derived closure/horizon authority.  Thus CF-P1 and CF-P2 are evidenced for
this bounded synthetic model.

The residual Tier-3 question is whether a future adopted production contract
may introduce the ordinary horizon citizen and require the atomic
member-change transition with these semantics.  This prototype neither adopts
that citizen nor settles its production schema, actor/presentation form, or
integration with existing act families.
