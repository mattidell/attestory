# Examination — Iteration 1 (Incumbent-Informed Design)

Rung: 1 (static documents; illustrative snippets only). Fixtures synthetic:
workspace `W-001`, taxpayers `T-001`/`T-002`, tax years `2025`/`2026`, package
boundary `PKG-2025-r3`.

## Why not extend per-family horizons

`packages/kernel/horizons.py` chains are keyed on `(family, version, scope)`
and *every* `member-transition` act computes a new successor
(`findings.apply_member_transition` calls `horizons.apply_transition`
unconditionally). Coupling authorization to that chain would make it expire
on every ordinary add/remove — the exact defect Seam 4's spike found. The
successor must be an **uncoupled** citizen: its own entity kind, own act
kinds, never touched by `member-transition`, `bundle-adoption`, or any
fact-lattice applier. That decoupling structurally delivers property (b); it
is an absence of wiring, not a guard that could be forgotten.

## Citizen shape

New kernel entity kind `authorization.standing-workspace`, admitted the way
`horizons.py` admits `kernel.family-horizon` citizens: a chain keyed on a
scope tuple, not a bare entity id, so re-grant after withdrawal is possible
without id collision.

```json
{
  "schema": "entity.v1",
  "id": "authorization.standing-workspace|workspace=W-001,taxpayer=T-001,tax_year=2025,package_boundary=PKG-2025-r3#g1",
  "kind": "authorization.standing-workspace",
  "label": "Standing calculation authorization — T-001, TY2025, PKG-2025-r3",
  "scope": {"workspace_id": "W-001", "taxpayer_id": "T-001", "tax_year": 2025, "package_boundary_id": "PKG-2025-r3"},
  "status": "current"
}
```

The chain key is `(workspace_id, taxpayer_id, tax_year, package_boundary_id)`,
mirroring `horizons.chain_key`'s `(family, version, scope)` shape. The
trailing `#g1` is a grant sequence number, not part of the chain key, so a
later re-grant after withdrawal gets a fresh entity id (`#g2`) without
violating `entity-introduced`'s duplicate-id rejection, while chain lookup
(by scope tuple) still finds "the current authorization for this scope," as
`current_by_chain` does for horizons.

New act kinds, new appliers, no change to existing ones:

| Act kind | Effect | Reversible? |
|---|---|---|
| `authorization-granted` | genesis/re-grant; status → `current` | — |
| `authorization-suspended` | current → `suspended`, reason recorded | yes |
| `authorization-reinstated` | suspended → `current` | — |
| `authorization-withdrawn` | current/suspended → `withdrawn` | no; re-grant is a new chain entry |

Each act payload carries `actor`, `scope`, and (for suspend/withdraw) a
`reason`. Ordinary `member-transition`, `assertion`, and `bundle-adoption`
acts carry none of these fields and never reference this chain — the same
non-coupling argument as above.

## Consumer check (fail-closed)

A calculation reader (successor to
`marshal.marshal_closure_authority`/`source_authority.resolve_closure_admissions`)
computes its own scope tuple from the run request — `(workspace_id,
taxpayer_id, tax_year, package_boundary_id)`, the last derived from the
content actually governing the run (SA-P2 below) — and looks up *exactly*
that chain key. No fallback widens workspace, taxpayer, year, or boundary;
absence of a matching key is refusal, never reuse of another chain.

```python
def resolve_standing_authorization(chains, scope: AuthorizationScope) -> Resolution:
    key = chain_key(scope)  # (workspace_id, taxpayer_id, tax_year, package_boundary_id)
    lifecycle = chains.current_by_chain.get(key)
    if lifecycle is None:
        # diagnostic-only relaxed lookup; never an admission path
        near = _find_same_workspace_and_boundary(chains, scope)
        if near and near.scope["taxpayer_id"] != scope.taxpayer_id:
            return Resolution.refused("authorization_scope_mismatch:taxpayer")
        if near and near.scope["tax_year"] != scope.tax_year:
            return Resolution.refused("authorization_scope_mismatch:tax_year")
        return Resolution.refused("not_authorized")
    if lifecycle.status == "suspended":
        return Resolution.refused("authorization_suspended")
    if lifecycle.status == "withdrawn":
        return Resolution.refused("authorization_withdrawn")
    return Resolution.admitted(lifecycle)
```

The diagnostic-only relaxed lookup never admits; it only selects which
refusal reason to surface. Admission is always the exact-key match.

## Six cases

**1. Correct taxpayer and year.** Scope `(W-001, T-001, 2025, PKG-2025-r3)`
matches a `current` chain entry exactly. `Resolution.admitted`. The
calculation treats the current workspace as the exhaustive universe.
Settled at paper — the lookup is a dict-key match, no ambiguity.

**2. Wrong taxpayer.** Calculation scope `(W-001, T-002, 2025,
PKG-2025-r3)`; only `(W-001, T-001, 2025, PKG-2025-r3)` exists. No exact
match. Diagnostic lookup finds a chain for the same workspace+boundary with
a different taxpayer → `authorization_scope_mismatch:taxpayer`, not the
generic `not_authorized`. Settled at paper for the state machine;
needs-rung-2 to confirm the diagnostic lookup stays cheap against a real
chain index, not just a paper single-entry example.

**3. Wrong year.** Scope `(W-001, T-001, 2026, PKG-2025-r3)`; same
mechanism keyed on `tax_year` → `authorization_scope_mismatch:tax_year`.
Settled at paper, same caveat as case 2.

**4. Ordinary additions and removals.** A `member-transition` act adds a
1099-INT statement to the interest family; `findings.apply_member_transition`
advances that family's horizon chain and touches only `findings`,
`withdrawn_fact_ids`, and `fact_state.entities` for `kernel.family-horizon`.
No payload field names an authorization chain key; no code path calls the
authorization applier. The authorization entry for
`(W-001, T-001, 2025, PKG-2025-r3)` is unread and unwritten; status stays
`current`. The next calculation resolves the same key and is admitted
without any new act. Settled at paper — an absence-of-call argument,
verifiable by reading `findings.py`'s applier dispatch table today.

**5. Suspension or withdrawal.** An `authorization-suspended` act moves the
chain entry to `status: "suspended"` with a recorded `reason`/`actor`. The
next lookup finds the entry (not absent) but `status != "current"`, and
returns `authorization_suspended` — a distinct code from `not_authorized`,
carrying reason and actor. `authorization-withdrawn` behaves identically but
is terminal: no `authorization-reinstated` is admitted once
`status == "withdrawn"` (rejected the way
`findings.apply_evidence_replaced` rejects a non-`current` predecessor). A
later grant produces a fresh `#g2` entity under the same chain key. Settled
at paper for the state machine and distinct codes; needs-rung-2 for the
actual admission-time rejection of reinstate-after-withdrawal against a real
act log (the analogous `evidence-replaced` guard is proven at rung ≥2, but
this is a new applier).

**6. No renewed per-family confirmation (stale scope must be inert).**
`package_boundary_id` is part of the chain key, not a mutable field on an
existing entry. If the content governing the calculation's referenced-input
footprint changes (SA-P2 below), the calculation's own computed
`package_boundary_id` changes, so its scope tuple no longer matches the old
chain's key — no "same chain, more permissive boundary" state exists. The
old entry is never read, superseded, or partially matched; a fresh
`authorization-granted` under the new key is the only admission path. Same
non-relaxation property `horizons.apply_transition` already gets right for
family chains (wrong/future/replayed predecessor all reject), applied to
boundary change instead of membership change. Settled at paper — same
dict-key-match argument as case 1, negated.

## Producer → authority → consumer → failure map

- **Producer:** the interaction `completeness-support-decision.md` names —
  "first requests a return-level generation or derivation that requires an
  exhaustive total" — issues `authorization-granted`. The same surface (or
  the taxpayer directly) issues `authorization-suspended` /
  `authorization-withdrawn` / `authorization-reinstated` on request.
- **Authority:** a new pure fold module, `authorization_chains.py`, parallel
  to `horizons.py` — `AuthorizationState`, `chain_key`, `apply_granted`,
  `apply_suspended`, `apply_reinstated`, `apply_withdrawn`,
  `current_authorization(state, scope)`; four new act kinds registered into
  `findings.KERNEL_ACT_KINDS`/`_APPLIERS`, touching no existing applier.
- **Consumer:** the marshal/runner step that today calls
  `marshal_closure_authority`/`resolve_closure_admissions`
  (`packages/derivation/marshal.py`, `packages/derivation/source_authority.py`)
  gains a sibling call, `resolve_standing_authorization`, exposed on
  `Environment` (alongside `closed_sets`) and copied into run-record
  provenance — meeting the decision doc's requirement that the authorization
  "remain visible in run explanation provenance."
- **Failure modes:** `not_authorized` (narrow per-family confirmation
  fallback offered instead), `authorization_scope_mismatch:taxpayer` /
  `:tax_year` (diagnostic refinement of `not_authorized`),
  `authorization_suspended`, `authorization_withdrawn`, and
  `authorization_boundary_superseded` (SA-P2). Each is a distinct
  disposition code in the run record, never collapsed into one "closure
  missing" code the way the incumbent mechanism collapses
  suspension/withdrawal into absence.

## SA-P2: the re-authorization boundary rule

**Checkable rule:** `package_boundary_id` is a content hash (or monotonic
tag equivalent to one) computed over the sorted set of `{bundle id+version,
family declaration id+version, rule id+version, quantity-symbol
declaration id+version}` that are **reachable from the specific rule(s) the
authorized calculation actually composes** — not the full adopted content
set. Recompute this hash at every content-adoption act; if it differs from
the value stored on the authorization chain the calculation resolves,
resolution returns `authorization_boundary_superseded` (case 6's mechanism).

This makes the rule mechanical rather than taste-based: a new bundle,
family, or rule the composition does not reference (an unrelated form, a
different tax year's content) does not change the hash and does not force
re-authorization; a change to any declaration inside the referenced closure
— a new box on an already-referenced family, a revised rule version, a
redefined quantity symbol the composition consumes — changes the hash and
forces it. This answers `completeness-support-decision.md`'s framing:
"which changes alter the meaning of the calculation universe itself" is
exactly "which declarations are inside the referenced-input dependency
closure of the composition the authorization covers." Needs-rung-2: whether
the adopted-content graph already exposes a stable, cheap "dependency
closure of a rule composition," or whether that closure computation is
itself new machinery this successor must add.
