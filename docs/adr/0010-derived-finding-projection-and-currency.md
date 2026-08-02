# ADR 0010 — Derived Findings in the Projection and Currency

- Status: accepted (ratified 2026-07-11)
- Tier: 2
- Date: 2026-07-11

## Context

Derivation Machinery (merge `e1608bf`) publishes derived values but does not
close the correction cascade: superseding an input finding does not displace the
derived findings that depend on it (`docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-11-derivation-cascade-
reconciliation.md`). Two seams are unfinished:

1. **Act-log admission.** ADR-0008 decision 2 places publication acts in the act
   log. The runner produces and validates `derived-publication` act payloads but
   does not append them as `act.v1` envelopes, because the kernel `ActLog`'s
   `SchemaRegistry` spans only the kernel schema directory, not the derivation
   act schema.
2. **Currency.** `packages/kernel/currency.py` folds `finding.v1` citizens and
   reads derivation edges from `finding.pins.finding_ids`. Derived values are
   `derived-finding.v1` (ADR-0009) with role-bearing pins `[{role,id,version}]`;
   they are a different citizen family and are not folded.

This ADR settles how derived findings enter the workspace projection and the
displacement computation. It does not touch the reserved T1 derived-finding-
authority entry: displacement is mechanical (Article 7 edges), and currency is
already computed without authority doctrine.

## Decision (proposed)

1. **The workspace act log admits `derived-publication` envelopes.** The act
   log's registry spans all published act kinds a workspace may store — kernel
   plus derivation. A combined registry (both schema directories) is the
   mechanism; the two-step validation pattern is unchanged (envelope schema, then
   the payload's declared schema, then the embedded `derived-finding.v1`).

2. **Derived findings enter the projection from the act log.** Applying a
   `derived-publication` act adds its `derived-finding.v1` to workspace state,
   alongside kernel findings but as a distinct family (human and machine findings
   stay separate citizen kinds, per ADR-0009).

3. **Currency composes over the kernel, it does not absorb the derivation family
   (the one real decision).** A derivation-currency layer contributes derivation
   edges from each derived finding's `input`/`choice` pins; `currency.py` keeps
   folding kernel findings and remains unaware of `derived-finding.v1`. The
   displacement roots (superseded inputs, individuated entities) and the
   `displacement_closure` walk are reused unchanged — the derivation layer only
   supplies additional edges into that walk.

4. **Edge extraction.** For each derived finding, each pin with role `input` or
   `choice` that names a finding id yields a derivation edge `pinned_finding →
   derived_finding`. Edges chain through derived-on-derived (a derived input pin
   points at another derived finding). Parameter/operation-semantics/adoption/
   governance pins are provenance, never displacement edges.

5. **Derived findings are displacement targets, never roots.** A derived finding
   carries a `symbol`, not a `fact_id`, and never participates in `currency.py`'s
   correction-root detection (`_finding_corrections`, which keys on `fact_id`
   sameness among kernel findings). A derived value is not *corrected* in place —
   it is *re-derived*, producing a new content-addressed finding — so its
   predecessor leaves current state by displacement along the derivation edge,
   not by same-fact correction. This is why compose-over needs no `fact_id` on
   derived findings and why the kernel's correction machinery stays untouched:
   the derivation layer contributes edges into the closure walk and nothing else.

6. **Displacement propagation only; re-derivation is out of scope.** A displaced
   derived value with no replacement is a valid incomplete-but-true state
   (Article 6). Auto-re-derivation is a later trigger/orchestration decision.

## Consequences

- The correction cascade closes end to end: supersede an input → the input
  displaces → derivation edges propagate → dependent derived findings displace,
  as a consequence of the record (Article 7), not a caller-supplied fan-out.
- First Tax Slice can carry a supersession golden as a first-class acceptance
  test of the signature move.
- The kernel projection and `currency.py` are unchanged in what they know about;
  the derivation family lives in a composing layer, so a future currency change
  in one family does not entangle the other.
- The combined registry is the seam every future act family will use; this ADR
  sets that precedent (workspace act log = all published act kinds).

## Alternatives considered

- **Extend `currency.py` to fold `derived-finding.v1` directly.** Rejected:
  teaches the kernel projection about the derivation family, coupling two citizen
  families in the module the whole record-integrity story rests on. Compose-over
  keeps the kernel pure and the coupling one-directional.
- **Keep publication acts out of the act log; project from a side stream.**
  Rejected: contradicts ADR-0008 decision 2 (publication acts land in the act
  log; records are the separate stream) and would split the workspace's
  authoritative store.
- **Close re-derivation now too.** Rejected as scope: correctness is satisfied by
  displacement (Article 6); re-derivation is convenience and a separate decision.

## Links

- Charter: `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-11-derivation-cascade-reconciliation.md`
- Precedent: Workspace Kernel review Finding 1 (`docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-10-workspace-kernel-tracks-4-7.md`) — same class, individuation layer; fixed by `patch-kernel-reconciliation`.
- Companions: ADR-0002 (act log), ADR-0007 (publication act), ADR-0008 (record placement), ADR-0009 (derived-finding shape).
- Affected: `packages/kernel/act_log.py` (registry), `packages/kernel/currency.py` (composed-over), new derivation-currency layer under `packages/derivation/`.
