# ADR 0041 — Correction-Authority Policy

- Status: **accepted** (owner ratification 2026-07-22, PR #50 merge)
- Tier: 2
- Date: 2026-07-22

## Context

`packages/kernel/findings.py` already consults a per-fact-type correction gate
at the exact point it is needed. In `_validate_finding`:

```python
already_answered = any(
    existing["fact_id"] == finding["fact_id"]
    for existing in state.findings.values()
)
if already_answered:
    policy = fact_type["supersession"]["policy"]
    if policy != "free":
        raise FindingModelError(
            f"finding {finding['id']}: fact {fact.fact_id} is governed by "
            f"supersession policy '{policy}', which does not permit correction here"
        )
```

The comment immediately above this block already anticipates this ADR:
"Only the `free` policy is published today, but the declaration is consulted,
not decorative: restricted policies arrive with rule artifacts and bind
here." That prediction is correct and nothing about the dispatch site is
broken or needs to change shape.

The gap is entirely upstream. `packages/schemas/kernel/fact-type.v1.schema.json`
closes the policy enum to a single value:

```json
"supersession": {
  "type": "object",
  "properties": { "policy": { "enum": ["free"] } },
  ...
}
```

and every fact-type citizen in the repo declares exactly that value. A grep
of `"supersession"` across `packages/content/tax/2025/*.json` turns up ten
bundles and every declared policy is `"free"` — W-2, both 1099 forms,
Schedule B, QDCG, and core calculations alike. No fact type has ever
declared anything else, and no other policy value has ever been given
meaning. The gate is real but permanently a no-op; this is deferral-ledger
entry 13 (Dividends and Schedule B Slice ledger, and re-affirmed in the
First Real Return Slice ledger as entry 10): "any actor supersedes any
finding without restriction; a real correction-authority policy is
undesigned."

**On "actor."** The deferral entries and this milestone's decision summary
use the word "actor" colloquially — "any actor supersedes any finding" reads
naturally as "whoever submits a correction." It is not a designed concept.
Findings carry no notion of who supplied them: `packages/schemas/kernel/finding.v2.schema.json`'s
property set is `schema`, `id`, `fact_id`, `value`, `basis`, `evidence_ids`,
`capture`, `pins`, `contribution_id` — `basis` is an epistemic classification
of *how* a value was obtained (`documentary` / `attested` / `elective`), not
*who* supplied it, and `contribution_id` is Article-14 batch provenance, not
identity. A grep of `packages/kernel/*.py` for `actor` or `contributor` turns
up nothing. Building a real actor/role concept — one that could be trusted at
a validation gate rather than merely asserted — is a materially bigger,
un-narrow change (session/authentication concept, a place to record it
durably, a way to keep it from being spoofed by whoever holds the workspace)
that this milestone's Non-goals correctly keep out of scope. This ADR
therefore settles the vocabulary in terms of **existing recorded state** —
horizons, closure claims, fact nature, the fact's own answer history — never
in terms of who is asking. See Alternatives Considered for why this still
serves the named need.

ADR-0011 (§4, "Closure authority is affirmative-only") and ADR-0016/0017
already establish the shape this ADR reuses: a closure fact is an ordinary
`fact-type.v1` citizen, `nature: determinable`, keyed to a family-horizon
citizen (ADR-0017); its current value being `true` is the recorded,
attested, individuation-rooted signal that a scope is closed. That is the
one piece of "has something authoritative happened yet" state this codebase
already has, and it is exactly the kind of condition a correction-authority
policy should be able to gate on without inventing anything new.

## Decision

1. **The supersession-policy vocabulary is closed to three values:** `free`,
   `locked`, and `closed-on-attestation`. Each is a state predicate over data
   the kernel already tracks — never an identity check. **Correction to this
   ADR (post-Track-1-review, 2026-07-22): this vocabulary ships as a new
   `fact-type.v3` schema version, not an in-place widening of `fact-type.v1`.**
   ADR-0003/Canon Article 9 makes a published schema version immutable,
   enforced by the checksum manifest (`packages/kernel/schema_registry.py`);
   widening `fact-type.v1`'s enum in place — this ADR's original wording —
   would mutate a published schema, exactly what that registry exists to
   refuse. (`fact-type.v2` is unrelated pre-existing content — ADR-0025/0028's
   versioned fact-identity surface — so the next free version is v3, not v2.)
   `fact-type.v1` is untouched, byte-for-byte; every existing `free`-policy
   fact type is unaffected and needs no migration; only new fact-type content
   that wants `locked` or `closed-on-attestation` declares `"schema":
   "fact-type.v3"`. This is the same historical-coexistence pattern ADR-0028
   already established for `form-field.v2`/`v3`. The widening itself, plus the
   two policies' own predicates below, is Track 1's schema and content work.
   **The dispatch site in `findings.py` does not change shape** — it still
   reads `fact_type["supersession"]["policy"]` at the same `already_answered`
   check and still raises `FindingModelError` on rejection, regardless of
   which schema version the fact type declares. What changes is what the
   `if policy != "free"` branch does for each non-`free` value.

2. **`free`** — unrestricted, unchanged. A new finding for an already-answered
   `fact_id` is always accepted. This remains the default and stays what
   every existing fact type declares; ratifying this ADR does not, by
   itself, restrict a single fact today. Restriction only takes effect where
   a fact type's own content is deliberately changed to declare `locked` or
   `closed-on-attestation`.

3. **`locked`** — correction forbidden unconditionally once any finding for
   that `fact_id` exists. Predicate: identical to the existing
   `already_answered` test already computed at the dispatch site — no
   additional state read. This is for fact types where a second answer to
   the same question is never legitimate (single-shot facts), and it is the
   cheapest policy to implement because it needs no new state access, only
   an unconditional raise in that branch.

4. **`closed-on-attestation`** — correction forbidden once a *named* closure
   fact is currently true; permitted otherwise. The supersession declaration
   carries a reference to which closure fact type gates it:

   ```json
   "supersession": {
     "policy": "closed-on-attestation",
     "gate": { "fact_type": "<closure-fact-type-id>" }
   }
   ```

   The named fact type must itself be `nature: determinable` with a boolean
   `value_schema` — the same shape ADR-0011 §4 and ADR-0016/0017 already
   require of a closure-claim fact. The dispatch site resolves the current
   finding for that fact type at the scope the gated fact and the closure
   fact share (their common identity-key names), the same scope-projection
   ADR-0016's family-subtotal/closure-claim pattern already performs. If
   that current finding's value is `true`, correction is rejected; if it is
   `false`, absent, or the referenced fact type carries no current finding,
   correction is permitted. This mirrors ADR-0011 §5's affirmative-only
   posture: only a current `true` closes anything, and horizon succession
   (ADR-0017) — which supersedes the closure finding itself — reopens
   correction exactly as it already reopens closure-backed derived results.
   Exact schema bytes for the `gate` object and exact scope-matching
   mechanics are Track 1's implementation, not decided further here (see Not
   Decided).

5. **No new act kind, no new entity kind, no new edge.** All three policies
   read state the kernel already carries (`state.findings`, the closure
   fact's current value via existing horizon/closure machinery). This is
   pure content declaration plus one new predicate branch at an existing
   dispatch site — consistent with the milestone's framing of this as a
   bounded Tier-2 contract needing no rival-prototype cycle.

## Consequences

- Track 1 (enforcement) must: publish `fact-type.v3` with the widened enum
  (`fact-type.v1` untouched); add the
  `gate` property (required iff `policy == "closed-on-attestation"`,
  forbidden otherwise — schema-enforced, not just convention); publish
  `bundle.v3` alongside it, since `bundle.v1`'s own schema pins nested
  `fact_types[].schema` to `const: "fact-type.v1"` and would otherwise reject
  any bundle carrying a `fact-type.v3` member before that member's own
  schema is even consulted (`bundle.v1` stays untouched; a bundle carrying
  only `fact-type.v1` members still declares `bundle.v1`, unaffected);
  implement the
  `locked` and `closed-on-attestation` branches in `findings.py`'s dispatch;
  and produce regression goldens proving rejection of an unauthorized
  correction and success of an authorized one across at least two fact
  families (per the milestone's exit criteria), including one exercising
  each non-`free` policy and one exercising horizon succession reopening a
  `closed-on-attestation` fact.
- Every fact type currently declaring `"free"` is unaffected; no content
  bundle needs to change for this ADR to ratify. Choosing `locked` or
  `closed-on-attestation` for any specific fact type is a separate content
  decision, not compelled by this ADR.
- The word "actor" in deferral-ledger entries 10/13 should be read, after
  this ADR, as resolved by state-gating rather than by an actor/role
  concept; if a future need genuinely requires knowing *who* is correcting a
  fact (not just *whether* a state condition holds), that is a new,
  separately-chartered identity/trust-boundary decision, not an extension of
  this vocabulary.

## Alternatives Considered

- **Actor/role-scoped supersession** (e.g., "only the original contributor
  may correct this fact," or "only a preparer role may correct a filed
  fact") — this is the literal reading of the milestone's Tier-2 summary
  ("which actor/role may supersede"). Rejected for this ADR: findings carry
  no actor/contributor identity today (confirmed by schema and kernel grep,
  Context above), and the concrete pain recorded in the deferral ledger is
  "any actor supersedes any finding without restriction" — read most
  charitably, the problem is the *absence of any restriction at all*, not a
  specifically role-shaped one. A state-gated vocabulary (closed once an
  attested condition holds, or closed unconditionally after one answer)
  honestly addresses that recorded need without inventing an identity
  system. Had the recorded need instead been something like "a preparer must
  be able to override a taxpayer's closed election," no state predicate
  could honestly express that, and this ADR would need to stop and escalate
  rather than force a role concept into fact-type content — but no such need
  is recorded anywhere in this milestone's inputs, so this ADR proceeds on
  the state-gated design.
- **A single new restricted value (`locked` only, no attestation gate)** —
  rejected as too coarse: it cannot express "open until closure, then shut,"
  which is the shape ADR-0011/0016/0017 already use for closure claims
  themselves and the shape most likely to recur in real fact types (an
  election is free to revise until some determinable condition is attested,
  then it should stop moving).
- **Open/free-text policy strings interpreted by ad hoc code at each call
  site** — rejected by the same reasoning ADR-0006 used to close the pin-role
  vocabulary: an open vocabulary invites divergent, silently-incompatible
  meanings across fact types and defeats schema-level enforcement.
- **Deriving closure from computation rather than gating on an attested
  fact** — rejected by ADR-0011 §5 and ADR-0017 §2: closure/attestation truth
  is user-attested authority, not a derived value: a `closed-on-attestation`
  policy must gate on the same attested fact, not recompute it.

## Not Decided

- Exact JSON Schema bytes for the `gate` object beyond the shape shown in
  Decision §4 (e.g., whether it names one closure fact type or a small
  ordered list).
- The precise scope-matching algorithm used to project the gated fact's
  identity-key values onto the named closure fact type's identity keys when
  they are not identically named.
- Which specific existing or future fact types should adopt `locked` or
  `closed-on-attestation` — this ADR settles the vocabulary and predicates,
  not which content uses them.
- Any actor/role/identity concept — explicitly out of scope; see Alternatives
  Considered.

## Links

- Enforcement mechanism: `packages/kernel/findings.py` (`_validate_finding`,
  the `already_answered` / `supersession.policy` dispatch).
- Schema: `packages/schemas/kernel/fact-type.v3.schema.json` (`fact-type.v1.schema.json` untouched),
  `packages/schemas/kernel/finding.v2.schema.json`.
- Precedents: ADR-0006 (closed pin-role vocabulary + predicate pattern),
  ADR-0011 §§3–6 (same-fact correction, affirmative-only closure), ADR-0016
  (closure claim / family subtotal declaration pattern), ADR-0017 (recorded
  family horizons, closure freshness, horizon succession reopening closure).
- Milestone: `docs/phases/real-return/milestones/correction-authority-and-marshaller-simplification.md`
  (Track 0); deferral ledgers:
  `docs/phases/real-return/milestones/dividends-schedule-b-slice-deferral-ledger.md`
  (entry 13), `docs/phases/real-return/milestones/first-real-return-slice-deferral-ledger.md`
  (entry 10).
