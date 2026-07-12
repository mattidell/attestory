# Closure Freshness — Round 1 Adversary Review

Date: 2026-07-12. Seat: adversary reviewer. Evidence rung: paper only.

## Disposition

**CF-P1 and CF-P2 do not converge for production adoption in either paper.**
Both papers state the required observable lifecycle, but neither supplies the
record-level contract and replay evidence needed to demonstrate it. The
incumbent paper has a decision-blocking Article 7 problem as written: its
currency reducer makes a `current(F) > H` comparison a displacement root
without identifying a later act that supersedes a citizen on which a closure
*fact* is keyed. Renaming that comparison `F-membership(F) @ H'` does not make
it an individuation edge.

The clean-room rival has the more promising edge shape: a closure fact keyed on
an actual family/scope horizon could be displaced when that keyed horizon is
superseded, and its pinned closure finding could then displace the zero by the
ordinary derivation edge. But the paper leaves the producer, identity,
same-fact/succession rule, and atomic admission validation for that horizon as
future contract work. Consequently its advertised protection is conditional on
the very mechanism under test. It must not be treated as a settled answer to
CF-P1 or CF-P2 yet.

These are paper findings, not a request to add a listener, a stored freshness
bit, manual closure withdrawal, or a derived closure value.

## Equal attack matrix

| Attack | CF-it1 incumbent outcome | CF-it2 clean-room rival outcome |
| --- | --- | --- |
| Late relevant member without a horizon successor | A member act advancing the family log is supposed to make `current(F) > H`, then the proposed reducer displaces `C` and `Z0`. No successor citizen or declared keyed fact is produced; this is an unproved standing dependency and `Z0` remains current in any implementation that lacks the new reducer. **Not resisted.** | The paper expressly says a relevant member admitted without `H1` leaves the prior zero current. It calls that a future validation failure, but supplies no present validation. **Not resisted; correctly exposed.** |
| Same-member value correction | The table resists a correction only when the undeclared “membership card” is unchanged; then the subtotal, not the family, is displaced. It gives no testable rule separating value correction from a predicate/reclassification correction. **Conditionally resisted only.** | `V1 -> V2` is a derivation-only correction and does not advance `H1`; a reclassification is separately said to require a successor. This is the intended result, but no admission rule proves the classification. **Conditionally resisted only.** |
| Removal followed by restored emptiness (resurrection) | A monotonic log position would keep `Z0` noncurrent after removal. The conclusion depends on the same unimplemented divergence root, so replay has not shown that an empty current set cannot refresh `C` or `Z0`. **Claimed, not demonstrated.** | `H1 -> H2` would individuate `C1/K1` and cannot revive `C0/K0/Z0`; a new `K2` and run are required for `Z2`. This resists resurrection if the successor is atomically admitted. **Conditional; no reducer evidence.** |
| Out-of-order delivery and full rebuild | “Position” and a fold are named, but neither a total ordering rule nor projection/replay algorithm is declared. The row labelled rebuild merely asserts equality. **Not demonstrated.** | The table expects a replay of acts 1–8 to reach `H2/C2/K2/Z2`, but it defines neither ordering/conflict handling nor the horizon successor validation. **Not demonstrated.** |
| Change family F while family G stays current | The paper says roots are per-family, but `F-membership(F)` has no declared identity/scope contract or validation against a wrong family target. **Claimed, not structurally established.** | `(family declaration, scope)` is the stated horizon identity, which is the right isolation boundary; the paper nevertheless defers enforcement that a successor preserves it. **Conditional; an altered/global horizon remains possible.** |
| Fabricated, future, or wrong-family horizon | `C` declares `H`, but no rule binds that value to the family-scoped act-log position at the same revision. A future fabricated `H` makes later member acts compare `<= H`, leaving old authority fresh; computing the value instead creates the unclassified reducer dependency. **Not resisted.** | `H` is called an ordinary asserted citizen, but no schema, producer, or validation prevents a fabricated/mis-scoped successor or a closure keyed to it. The promised rejection is explicitly future work. **Not resisted.** |
| Manual closure withdrawal or computed/derived closure substitution | No manual withdrawal is required, which is correct. But reducer-derived staleness is made to displace an attested closure through a newly named root; it is neither an asserted closure successor nor a demonstrated keyed-citizen cascade. Treating `F-membership` as derived authority would also enter reserved T1. **Not resisted under the two-edge rule.** | No manual withdrawal or computed closure is proposed: `K0`/`K2` remain asserted closure findings. This attack is resisted only if `Hn` is an asserted, declared citizen rather than a derived membership authority; the paper has not established that contract. **Conditionally resisted.** |

## Attack details and exhibits

### 1. Late member / missing successor

**Attack.** Start with an empty family, true closure, and current `Z0`. Admit a
previously unknown relevant member but omit the purported horizon update.

**Incumbent outcome.** The design has no separately recorded horizon successor
to omit. It instead says the member act changes a log comparison and that a
currency reducer treats divergence as an individuation root. Thus the proposed
result is unavailable until a new standing-affecting computation is installed;
without it, no existing ADR-0010 input pin reaches the old zero. This is exactly
the late-member defect, not a resistance to it.

**Rival outcome.** Its own failure map reaches the same result: absent `H1`,
`Z0` stays current. Calling the omitted transition invalid is useful, but a
future validator cannot count as evidence that the required complete act exists.

**Exhibits.** CF-it1 `it1/design.md`, “The one piece of machinery this needs”
and table row 2; CF-it2 `it2/design.md`, table row 5 and failure map.

### 2. Same-member correction

**Attack.** Correct a member amount while retaining membership, then correct an
attribute that moves that same member across the declared predicate.

**Incumbent outcome.** The first case is intended to displace only the subtotal.
The second is called a “membership-changing correction,” but no producer or
identity rule says how that distinction is recorded. The design cannot be
tested for the boundary case until it defines it.

**Rival outcome.** The first case is intended to be `V1 -> V2` only; the second
is listed as reclassification and should create a successor. That is a coherent
desired split, but the required reject/accept rule remains deferred.

**Exhibits.** CF-it1 `it1/design.md`, table row 3 and first bullet under
CF-P1; CF-it2 `it2/design.md`, table rows 6–7 and opening claim.

### 3. Removal and resurrection

**Attack.** Add a member after `Z0`, remove it, and inspect currency before any
new true closure assertion or run.

**Incumbent outcome.** Its monotonic-horizon assertion is the right negative
expectation, but it shares the unimplemented comparison-root mechanism. There
is no replay evidence that removal cannot make a set-based freshness check or
an accidentally recomputed closure restore `Z0`.

**Rival outcome.** If `H2` genuinely supersedes `H1`, `C0/K0/Z0` remain
downstream of displaced `H0`; `C2` is open until `K2` is asserted. This is a
valid two-edge *shape*, conditional on the missing horizon contract.

**Exhibits.** CF-it1 `it1/design.md`, table rows 4–5; CF-it2 `it2/design.md`,
table rows 7–8 and “Required cases and checks”.

### 4. Rebuild and ordering

**Attack.** Replay the same complete act log from empty state after every act;
also attempt arrivals whose transport order differs from the authoritative
act-log order.

**Outcome for both.** Neither design gives an ordering/atomicity rule sufficient
to run this attack. The incumbent says its horizon is an act-log position; the
rival says a member-change act is one complete transition. Neither says how the
position is fixed at the transition revision, how an invalid half-transition is
rejected, or how replay forms the identical displacement closure. Both rebuild
claims are predictions, not measurements.

**Exhibits.** CF-it1 `it1/design.md`, definition of `H` and table row 6;
CF-it2 `it2/design.md`, opening “Member-change act” paragraph and table row 9.

### 5. Family isolation

**Attack.** Create equally named or neighboring families; advance only F and
verify that G's closure and zero remain current. Then attempt a successor whose
scope is changed from F to G.

**Incumbent outcome.** The paper relies on “per-family” roots but does not
declare the membership citizen's identity or the validation that binds every
act to exactly one family/scope. It therefore has no structural answer to the
wrong-target case.

**Rival outcome.** Its `(family declaration, scope)` identity is an explicit
and appropriate defense. But it says successor identity retention *must* be
validated later, so the attack is only conditionally resisted.

**Exhibits.** CF-it1 `it1/design.md`, table row 7 and edge inventory; CF-it2
`it2/design.md`, “Required cases and checks”, check 2.

### 6. Fabricated horizon

**Attack.** Attach a horizon after a member already exists, choose a future
position, or manufacture a successor not coupled to the membership transition;
then attest a true closure and test whether a zero can be made current.

**Incumbent outcome.** The attestation itself declares H, but the design gives
no atomic check that H equals the family log position at that act's workspace
revision. A future H defeats its `latest <= H` freshness predicate. If the
runner supplies H, H is no longer the user's presented assertion, and the
paper must explain how its construction avoids a new authority citizen.

**Rival outcome.** It reserves exactly the validation that should reject this
attack. Until the horizon's kind, identity, supersession rule, and atomic
producer are declared, this is an open authority injection path rather than a
passed negative.

**Exhibits.** CF-it1 `it1/design.md`, CF-P1 definition and exact pins;
CF-it2 `it2/design.md`, opening claim and failure condition.

### 7. Authority and edge audit

**Attack.** Prohibit manual closure withdrawal and prohibit a rule from
asserting/negating closure. Require every effect making `Z0` noncurrent to be
one existing derivation or individuation edge.

**Incumbent outcome.** The paper correctly rejects a rule that derives
`closure=false`. Its substitute nevertheless makes a computed divergence
displace `C`. Article 7 individuation requires a superseded citizen keyed by a
fact; the paper names no closure fact keyed on a versioned `F-membership`
citizen, and its reducer instead injects divergence into the root set. That is
a third standing-affecting dependency unless the missing
citizen/fact/successor contract is supplied. Making that membership object a
derived authority would also collide with reserved T1. This is decision-blocking.

**Rival outcome.** The proposed `H0 -> C0` relation can be an individuation
edge if `C0` is a closure *fact* keyed on the superseded, asserted `H0`; the
paper's subsequent `K0 -> Z0` is then the ordinary derivation edge. It must
still prove that the member-change act asserts the valid successor rather than
using a listener, a stored flag, or a derived authority. This remains a
decision-blocking missing contract, not a demonstrated Article 7 violation.

**Exhibits.** Constitution Articles 2, 3, 6, 7, and 12; Ontology §7 “The two
edges” and “Cascade semantics”; ADR-0010 decisions 3–6; ADR-0016 “Not Decided”;
CF-it1 `it1/design.md`, CF-P2 machinery paragraph; CF-it2 `it2/design.md`,
edge inventory and CF-P1/CF-P2 disposition.

## Required next evidence

Before either design can support a Tier-3 decision, a bounded reducer/contract
probe must use a single ordered synthetic act log and, after each accepted act,
compare incremental currency with full rebuild. It must make the following
pass/fail, not merely narrative:

1. A relevant member transition cannot be admitted without the one declared,
   family/scope-preserving horizon successor.
2. The closure fact is actually keyed on that successor, and the closure
   finding and zero are displaced by complete individuation then derivation
   closure—no separately injected staleness root.
3. Same-member value corrections, membership-predicate changes, removal, and
   re-attestation have distinct admitted transitions and the stated currency.
4. A fabricated/future/mis-scoped horizon is rejected at the transition's
   workspace revision.
5. Removal never resurrects an old zero; only a new asserted true closure and
   explicit run may publish a successor.
6. A change to F cannot affect G, including through malformed successor input.
7. No currency flag, side listener, caller-supplied authority, derived closure,
   or derived T1 authority citizen is used.

This is evidence gathering only. It does not authorize production schema,
runner, persistence, or governance changes.
