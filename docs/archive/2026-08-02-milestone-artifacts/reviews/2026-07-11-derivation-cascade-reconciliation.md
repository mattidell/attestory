# Review: Derivation Machinery — the correction cascade is not closed

- Date: 2026-07-11
- Reviewer: builder of the Derivation Machinery milestone (self-review of merged work)
- Scope: merge `e1608bf` (Derivation Machinery) and its disclosed follow-ups
- Status: advisory. The owner decides whether to act, ignore, or snapshot-and-reset.
- Verification observed: `python3 -m unittest` 168 OK; mypy strict clean; governance lint conformant.

## Verdict

**Keep, and patch before First Tax Slice.** The milestone is faithful to ADRs
0006–0009 and the §5 conditions are discharged. But two items the retrospective
disclosed as separate follow-ups are, read together, a single hole under the
product's center of gravity: **the correction cascade does not close through the
machinery.** This is the same class of defect as Finding 1 of the Workspace
Kernel review (`docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-10-workspace-kernel-tracks-4-7.md`) —
"displacement is not drivable from the record" — one layer up. That one was
fixed by a reconciliation patch before the next milestone; this one should be too.

## The gap, precisely

Supersede an input finding and nothing downstream moves. Mechanism:

- `packages/kernel/currency.py` computes displacement by folding `state.findings`
  (kernel `finding.v1` citizens) and reads derivation edges from
  `finding.pins.finding_ids` — the old shim shape.
- Derived values are `derived-finding.v1` citizens (ADR-0009) with *role-bearing*
  pins `[{role,id,version}]`, and they live in publication-act payloads that are
  produced and validated but **never appended into the act log** — so they are
  neither in the projection nor edge-shaped for the fold.

Result: superseding a W-2 input correctly displaces the *input* finding, and the
derived `line1a` / `line9` that depend on it do not displace — because they are
not in the graph and their dependency edges were never extracted. Article 7 (two
declared cascade edges; displacement is a consequence of the record) and Ontology
§2 supersession propagation are asserted in doctrine and unrealized in the
machinery. The signature product move — supersede an input, watch derived values
displace — does not run end to end.

## Why it must precede First Tax Slice

First Tax Slice is where this commitment earns its acceptance test: the slice
should carry a supersession fixture (amend a W-2, assert the derived 1040 lines
displace) as a first-class golden. If the cascade is open when the slice is
authored, that fixture cannot exist or must encode the broken behavior, and the
slice quietly proves a weaker thesis than the product claims. Closing the cascade
first turns the patch from cleanup into the precondition for the slice to prove
the signature move on content.

## Scope

**In — displacement propagation (patch-sized):**
- The act log admits `derived-publication` act envelopes (combined registry over
  kernel + derivation act schemas).
- Derived findings enter the workspace projection from the act log.
- Derived-finding `input`/`choice` pins contribute derivation edges (pinned
  finding → derived finding); the existing `displacement_closure` walk then
  propagates displacement, chaining through derived-on-derived (W-2 → line1a →
  line9).

**Out — re-derivation orchestration:** auto-re-running derivation to produce the
*corrected* value after a supersession. A displaced derived value with no
replacement yet is a valid workspace state (Article 6, incomplete-but-true), so
displacement-only fully discharges the constitutional propagation commitment;
re-derivation is convenience, not correctness, and belongs to a later trigger/
orchestration decision. Bounding the patch here is a decision on the record, not
a place scope leaks.

## The one real decision → ADR-0010

The patch carries one genuine architecture choice, proposed in
`docs/adr/0010-derived-finding-projection-and-currency.md`: whether derived-
finding currency **extends `currency.py`** or is a **derivation layer composing
over it**. Recommendation: compose-over, so the kernel projection stays unaware
of the derivation family. The registry mechanism (act log admits the new
envelope) is the ADR's other, mechanical, half.

## No reserved-entry entanglement

Displacement is mechanical (Article 7 edges); `currency.py` already propagates
without any authority doctrine. Folding derived findings needs no resolution of
the reserved T1 derived-finding-authority entry, and does not re-open ADR-0009.

## Acceptance

- A supersession fixture: adopt → derive (W-2 → line1a → line9) → supersede the
  W-2 input finding → the derived findings are displaced from current state,
  attributable along the derivation edge.
- `derived-publication` act envelopes round-trip through the act log (append,
  read, project) under the combined registry.
- Kernel suite and derivation suite stay green; the E7.x displacement detections
  cover the derivation edge, not only individuation.

## Resolution (2026-07-11)

Addressed by the Derivation Cascade Reconciliation patch (merge `18ce073`), on
the `patch-kernel-reconciliation` precedent, in the ADR-0010 order:

- Combined schema registry (`SchemaRegistry` spans kernel + derivation dirs;
  `workspace_registry()`).
- Act log admits `derived-publication` envelopes (`append_publications`); the
  kernel projection scopes to `KERNEL_ACT_KINDS` and passes over the rest
  (compose-over).
- Derivation-currency layer (`packages/derivation/projection.py`) contributes
  derived-finding pin edges into the kernel's `displacement_closure`;
  `currency.py` unchanged.

Acceptance met: `tests/derivation/test_cascade.py` proves adopt → assert W-2 →
derive line1a/line9 → supersede W-2 → both derived findings displace, and an
unrelated correction displaces nothing. Full suite 179 green. Re-derivation
remains out of scope as chartered.
