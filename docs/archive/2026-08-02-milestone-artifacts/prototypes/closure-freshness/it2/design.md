# Closure Freshness — Clean-Room Rival Design

## Claim

Use a successive **source-family horizon** citizen.  A horizon is the current
membership-revision citizen for one declared source-family scope.  It is neither
a finding nor derived authority: it is an ordinary, versioned citizen whose
successor is asserted by every act that changes that family's relevant member
set.  The closure fact is keyed on `(family declaration, scope, horizon)`.

Consequently a closure attestation is only an attestation of the named family at
that horizon.  A closure-backed zero pins that closure finding.  A later
relevant-member addition, removal, or reclassification supersedes the horizon;
the old closure fact and all its findings leave current state by an
**individuation edge**; the zero then leaves current state by its ordinary
**derivation edge** from the displaced closure finding.  No act withdraws the
old closure, and no result purports to pin a member not yet known.

This is a paper design, not a schema or reducer proposal.  “Member-change act”
means one complete, recordable transition which both admits/corrects/removes the
member as applicable and creates the successor horizon.  It must not be a
background repair, a stored freshness flag, or a caller trigger.  The act's
validity rule is future contract work: it must reject a relevant member change
that leaves the family's horizon unchanged.

## Edge classification and inventory

Every standing effect is one of Article 7's two relations.

| Standing effect | Relation | Declared source → target | Why it is not another edge |
| --- | --- | --- | --- |
| A closure question stops being current after a membership change | individuation | superseded horizon citizen → closure fact keyed on it, then that fact's findings | The closure fact's identity includes the horizon; it is exactly a keyed-on-citizen cascade. |
| An old zero stops being current | derivation | closure finding pin → derived zero | The zero names the exact closure finding it used. |
| A member-value correction invalidates a subtotal that used it | derivation | corrected member finding pin → derived subtotal | Ordinary ADR-0010 input currency. |
| A member removal makes prior closure stale | individuation, then derivation | superseded horizon → old closure fact/finding → zero | Removal produces a successor horizon; it does not delete or withdraw history. |
| Re-attestation makes a new zero eligible | no standing cascade | new assertion answers the already-current closure fact; a later run publishes a successor | Publication is lazy work, not a standing effect. |
| Family A change leaves family B alone | no edge exists | different horizon citizens and closure facts | There is intentionally no cross-family source or target. |

Complete inventory: `(horizon → closure fact)` is the only new individuation
edge; `(closure finding → closure-backed zero)` is the closure-specific
derivation edge; `(member finding → present-member subtotal)` and downstream
derived-output pins are ordinary derivation edges.  Rule, mapping, adoption,
family-declaration, and horizon provenance pins are not currency edges.  The
horizon is not an input pin to the zero, because Article 7 defines derivation
edges through findings/rules; it acts through the closure fact's identity.

## Ordered act/state table

Synthetic identifiers: family `F-B1-2025`; horizons `H0`, `H1`, `H2`; closure
facts `C0`, `C1`, `C2`; closure findings `K0`, `K2`; zeroes `Z0`, `Z2`; member
facts/findings `M1/V1`, `M1/V2`.  “Current” is derived by a complete record
walk, never stored.

| Order | Recorded act | Current horizon / closure fact | Current relevant members | Currency result |
| ---: | --- | --- | --- | --- |
| 1 | adopt family declaration, mapping, and rule | — | none | no closure authority; empty subtotal blocked |
| 2 | establish `H0` for `F-B1-2025` | `H0` / `C0` open | none | blocked |
| 3 | assert true closure `K0` on `C0` | `H0` / `C0=K0(true)` | none | eligible, not yet published |
| 4 | run; publish `Z0=0` | same | none | `Z0` current; pins below |
| 5 | assert newly discovered relevant member `M1/V1` and successor `H1` | `H1` / new `C1` open | `M1/V1` | `H0` superseded; `C0`, `K0`, and `Z0` displaced; blocked, never stale zero |
| 6 | correct same member `V1 → V2`; no membership change | `H1` / `C1` open | `M1/V2` | any subtotal pinned to `V1` displaces; no horizon or closure effect |
| 7 | remove/reclassify `M1` as nonmember and successor `H2` | `H2` / new `C2` open | none | `C1` remains open but displaced with `H1`; no old closure or zero resurrects |
| 8 | re-attest true `K2` on `C2`; run | `H2` / `C2=K2(true)` | none | publish current `Z2=0`; `Z0` remains history only |
| 9 | rebuild record from acts 1–8 | same as row 8 | none | exactly `H2`, `C2`, `K2`, `Z2` current |

For a present-member case, a run after row 5 may publish a positive subtotal
pinned to `V1`; row 6 displaces that subtotal through its input derivation edge
and rerun may publish its `V2` successor.  It does not create or revive a zero.

## Producer → authority → edge → consumer → failure map

| Producer | Authority it records | Edge to currency consumer | Currency consumer | Failure prevented |
| --- | --- | --- | --- | --- |
| member-change act | successor horizon `Hn` for exactly one family/scope | individuation: `H(n-1) → C(n-1)` | prior closure finding | late member cannot leave old closure current |
| current true closure assertion | `Kn` on `Cn` | derivation: `Kn → Zn` | closure-backed zero | zero cannot exist on absent/false/open closure |
| same-member correction | `V2` answers `M1` again | derivation: `V1 →` any subtotal that pinned it | present-member subtotal | corrected amount cannot leave old subtotal current |
| removal/reclassification act | `H(n+1)` | individuation then derivation as above | prior closure / zero | removal does not delete history or resurrect `Zn` |
| re-attestation and run | `K(n+1)` then `Z(n+1)` | new derivation edge only | new zero | replacement occurs only through an explicit fresh authority |

The failure condition for the mechanism itself is narrow and checkable: if a
relevant-member act is admitted without a successor horizon, the prior zero
remains current.  That is a contract-validation failure, not a third edge or a
manual correction path.

## Exact pins and explanation walk

`Z0` pins: (1) `input: K0`, the exact true closure finding; (2) the adopted
mapping version; (3) source-family declaration/predicate version; (4) rule and
operation-semantics versions; (5) adoption and run/revision provenance required
by the existing derived-finding contract.  `Z0` does **not** pin `H0` as a
derivation input, any nonexistent future member, or a record.

An explanation for `Z0` is: `Z0` → `K0(true)` → `C0` whose identity names
`H0` → `H0`'s member-change provenance → adopted family declaration and mapping.
The last two are explanation/provenance references, not added currency edges.
After row 5 the same walk explicitly reports: `Z0` displaced because its pinned
`K0` is displaced; `K0` displaced because `C0` was individuated by superseded
`H0`.  For `Z2`, substitute `K2/C2/H2`.

## Required cases and checks

Positive checks:

1. Fresh empty: `H0`, true `K0`, no members, and a run yield current `Z0=0`.
2. Re-attested empty: after the member-add/remove sequence, only true `K2` can
   yield current `Z2=0`; rebuilding produces the same state.

Negative checks:

1. A later relevant member with `H1` displaces `Z0` immediately, before rerun;
   a false or absent `K1` blocks rather than publishes zero.
2. Changing family A's horizon cannot displace family B's closure or zero;
   a member removal cannot make `Z0` current again.

Two-family isolation follows from the horizon identity being exactly
`(family declaration, scope)`.  A horizon successor must retain that identity;
using a global horizon would fail this check by invalidating unrelated families.

## Rejected alternative

**Pin a frozen member list (or an observed-members frontier) directly on the
zero.**  It cannot invalidate the zero on a later unknown member: no old pin
points to the new finding.  Adding a “member arrived” listener, freshness flag,
or reverse-membership invalidation would be a third standing-affecting edge;
making the list a derived authority also crosses reserved T1.  This alternative
therefore fails Article 7 even if its incremental implementation looks simple.

## CF-P1 / CF-P2 disposition

- **CF-P1 — settled at paper.** Closure is fresh relative to an explicit,
  current family horizon, not timelessly fresh.  Relevant membership change
  makes the old horizon—and therefore its closure—noncurrent until a new
  attestation.
- **CF-P2 — requires a tiny reducer.** The edge path is expressible without a
  third edge: horizon individuation followed by the existing closure-pin
  derivation edge.  A throwaway reducer must nevertheless prove record-order
  replay, complete cascade, required horizon advancement, and no resurrection.
  Until it does, this is not production authorization.
