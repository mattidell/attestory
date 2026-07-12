# Closure Freshness Round 2 — Adversary Review

Date: 2026-07-12

Seat: adversary reviewer. Evidence reviewed: the repair1 contract, reducer,
tests, and examination, plus the recorded-horizon exhibit. This review is
independent and does not rely on peer reviews.

## Independent execution

I extracted the tagged `exhibits/closure-freshness/repair1` reducer and ran:

```text
python3 -m unittest discover -s /tmp/cf-repair1/docs/prototypes/closure-freshness/repair1 -p 'test_*.py' -v
Ran 5 tests ... OK
```

I also replayed the scenario with an independent attack harness. It compared
incremental currency with a fresh rebuild after every accepted act, checked
the root and both edge maps, and exercised the negative cases below.

## Attack results

### Malformed, fabricated, future, replayed, and mis-scoped transitions

- **Missing successor on `add`.** Rejected with “membership-changing
  transition requires exactly one horizon successor”; no member is entered.
  The supplied mutant is killed.
- **Half transition with a bad predecessor.** Rejected before membership or
  horizon mutation. After the rejection the current horizon remains `H0` and
  member `M1` is absent. This resists a half-committed transition.
- **Future closure reference (`H99`).** Rejected because closure must name the
  current family-scoped horizon. A closure cannot establish a future horizon.
- **Fabricated successor identity.** A new opaque ID is accepted only when it
  is created as the exact successor in the current family/scope and names the
  current predecessor. An ID cannot be referenced ahead of recording, reused,
  or supplied with a different predecessor. The reducer has no external ID
  provenance to validate; within this synthetic contract, creation in the
  admitted transition is the producer of the ordinary horizon citizen.
- **Replay of a successor/member transition.** Rejected: the horizon ID is no
  longer new (and the member precondition also fails).
- **Replay using an old predecessor.** Rejected because `previous` must equal
  the current family/scope horizon.
- **Mis-scoped successor.** Rejected because the successor must preserve the
  member-change family and scope.
- **Global successor.** Rejected by `_pair`; a `GLOBAL` horizon cannot enter
  the record.
- **Unknown operation, member shape, extra transition fields, and bad
  relevance values.** Rejected by the operation, member, `_only`, and
  operation-specific preconditions. No alternate caller-supplied transition
  channel is admitted.

### Correction classification and resurrection

- **Same-member value correction.** Accepted only when the member already
  exists and its boolean relevance is unchanged. It creates no successor,
  root, closure displacement, or zero effect. Replaying this no-standing-effect
  act is accepted, because it has no act identity or standing mutation; this is
  harmless for currency but remains a small replay-detection limitation if
  value-correction history itself is meant to be uniquely recorded.
- **Predicate-changing correction.** Requires an existing member, a changed
  boolean predicate, and one exact horizon successor. It creates a new
  recorded root and does not leave the prior zero current.
- **Removal.** Requires an existing member, no relevance value, and a successor.
  Successors accumulate roots; removal does not delete a root or traverse
  backward to resurrect an old zero.
- **Resurrection attempt.** In the complete scenario, `Z0` remains displaced
  after the add, predicate change, second-member add, and removal. Only a new
  current closure finding `K4` followed by an explicit `run_zero` produces the
  distinct current `Z4`. The old `K0 → Z0` chain never becomes current again.

### Rebuild and atomicity

`replay_check` passed at every accepted prefix. Incremental currency and full
ordered rebuild were equal after each act, including the transitions that
create multiple predecessor roots and the later re-attestation. Invalid acts
are rejected during the fold; rebuild does not silently repair them.

The successor is validated before member mutation. A rejected successor thus
cannot leave the member present with no horizon or the horizon advanced with
no member transition.

### Isolation and edge inventory

The final independent inventory was:

```text
roots: H0, H1, H2, H3
individuation: H0 -> K0; G0 -> KG0; H4 -> K4
derivation:    K0 -> Z0; KG0 -> ZG0; K4 -> Z4
```

F roots do not reach G edges. `ZG0` remains current while F changes, and the
F roots do not affect `KG0` or `ZG0`. No member-to-zero edge, listener,
comparison-derived root, or cross-family/global edge is used.

### Closure and authority attacks

- **Derived closure.** `derived_closure` is rejected. Closure authority enters
  only through `closure_attested` with literal `True`.
- **False or truthy-non-boolean closure substitution.** Both are rejected;
  `False` and `1` do not establish affirmative closure.
- **Stale closure used for a zero.** `run_zero` checks the closure fact’s
  horizon against the current family horizon and rejects stale authority.
- **Caller staleness flag or injected root argument.** Extra `stale` input is
  rejected, and `currency` accepts only `state`, so the public act/currency
  path has no caller-supplied root or staleness flag. The supplied direct-root
  mutation test passes.
- **Manual withdrawal.** There is no withdrawal act. Displacement occurs only
  when a recorded successor makes the predecessor an individuation root, and
  then follows the declared closure-finding derivation edge.
- **Third-edge or derived authority substitution.** The exposed currency
  result contains exactly `individuation` and `derivation` maps. Closure facts,
  horizons, and zeroes are not made current by a hidden freshness bit or a
  derived authority citizen.

## Adversarial boundary finding

The reducer’s `State` dataclass and its sets/dictionaries are publicly mutable.
As an out-of-contract in-memory tamper, adding `H0` directly to
`state.superseded_horizons` makes `currency(state)` displace `K0` and `Z0`
without a recorded successor. This is not reachable through an admitted act,
and the supplied API-level injection mutant is correctly killed, but it means
the prototype does not itself enforce the authoritative-record boundary
against a caller with direct object access. A production implementation must
encapsulate state or rebuild roots solely from immutable recorded transitions.

## Recommendation

**Recommend conditional pass for the bounded repair1 evidence.** Every
recorded-log attack required by the round brief is resisted, including
malformed transitions, rebuild divergence, resurrection, cross-family
contamination, fabricated/future references, and authority substitution. The
evidence supports the two-edge recorded-horizon shape for CF-P1/CF-P2 only.
Do not treat the result as production adoption: resolve state encapsulation,
value-correction act identity if replay uniqueness matters, and the remaining
Tier-3 production contract questions in a later decision process.
