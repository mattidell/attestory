# Recorded Family-Horizon Contract (Reducer Evidence Only)

This is a synthetic prototype contract, not an adopted schema or production
API.  It makes the selected rival's paper shape executable enough to test
CF-P1/CF-P2.

## Citizens and identity

A `horizon` is an ordinary recorded citizen.  Its identity is
`(family_declaration, scope)` plus its immutable successor occurrence; it is
not a finding, a derived finding, a current/stale flag, or an authority about
whether closure is true.  For each `(family, scope)`, one recorded horizon is
current.  Its successor retains the same pair and records the current horizon
as `previous`.

A closure fact has identity `(family_declaration, scope, horizon_id)`.  A true
closure finding is an asserted, affirmative answer to that fact.  A zero is a
derived result which pins that exact closure finding.  Mapping, declaration,
rule, adoption, and run references are provenance in a real system; this
reducer only gives them stable synthetic names and never treats them as edges.

## Admitted transitions

`open_family` records the initial horizon.  A `member_change` is one complete
ordered transition.  It has one member operation and one valid successor
horizon whenever membership changes:

| Operation | Member precondition | Relevant membership after act | Horizon |
| --- | --- | --- | --- |
| `add` | member absent | present | required successor |
| `value_correction` | member present | unchanged | forbidden |
| `predicate_change` | member present | changed | required successor |
| `remove` | member present | absent | required successor |

The successor must be new, have the act's exact `(family, scope)`, and name the
current horizon for that pair as `previous`.  Thus it cannot be fabricated,
future, replayed, or mis-scoped.  A half transition, global horizon, or unknown
act field is rejected.  A closure is only `closure_attested` with literal
`true`; `derived_closure` is rejected.  A run publishes zero only for a current
true closure with no current relevant members; caller staleness flags/roots are
not accepted.

## Standing effects

When a successor is recorded, its predecessor is a record-derived
individuation root.  The predecessor horizon has an individuation edge to each
closure finding whose closure fact is keyed on it.  Each zero has a derivation
edge from the closure finding it pins.  Currency walks only these two declared
edge maps.  A same-member value correction has neither a horizon successor nor
a closure/zero effect.  No listener, comparison-derived root, manual closure
withdrawal, or derived authority participates.

Rebuild is the fold of the ordered acts under these admission rules.  It may
recompute currency but may not repair an invalid historical act.
