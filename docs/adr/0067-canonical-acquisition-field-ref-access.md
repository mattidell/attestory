# ADR 0067 — Direct Per-Item Field-Ref Access for Canonical Object-Valued Facts

- Status: **accepted**
- Tier: 2 — resolves Seam 1 of the Document and Ordinary-Fact Translation
  Vertical milestone; sets the extraction pattern every downstream seam of
  that milestone (identity association, relationship constraints, rule-owned
  consequences) reads a canonical scalar through, but is not a
  product-thesis or governance-meaning decision.
- Date: 2026-08-28

## Context

Seam 1 of `milestone/document-ordinary-fact-translation-seams`
(`docs/phases/tax-concept-derivation/milestones/document-ordinary-fact-translation.md#Seam 1`)
asked how a tax rule obtains a scalar amount —
`accrued_interest_paid_to_seller` — that lives on an object-valued
acquisition fact, without inventing an unnecessary generic substrate. This
mirrors, but is not identical to, the fan-in problem ADR-0054 resolved for
Schedule D covered-LTCG (twin scalar collectible companions for a
multi-member *sum*); Seam 1 is fan-out from a single per-rule-binding fact,
not aggregation across a member set, so ADR-0054's rejection of a generic
field-projection substrate does not automatically transfer, and the seam
was chartered as a genuine rival comparison rather than assumed settled.

**Process.** `docs/prototypes/canonical-value-extraction/plan.md` (Gates
0-8). Two independent builders ran the same charter: an incumbent-informed
builder (`prototypes/canonical-value-extraction/it1`,
`examination-it1.md`) with access to the prior single-track milestone
attempt as reference evidence, and a clean-room rival dispatched via Grok
CLI with no access to that attempt or to `it1`
(`prototypes/canonical-value-extraction/it2`, `examination-it2.md`). Both
independently recommended the same mechanism for the same reason. A
three-seat committee reviewed both (`docs/prototypes/canonical-value-extraction/reviews/clean-room-r1.md`,
`adversary-r1.md`, `eligibility-r1.md`): the convergence is genuine, not
same-label-different-meaning, but the rival's account was more accurate —
it, not the incumbent-informed builder, correctly identified that today's
schema shape blocks the mechanism outright regardless of spelling. The one
paper-unsettled question (case 6: does a misspelled field fail closed) was
closed by a rung-2 spike
(`docs/prototypes/canonical-value-extraction/case6-rung2-spike.md`,
`spike/case6_spike.py`) exercising the real, unmodified
`packages/kernel/schema_registry.py` `SchemaRegistry` against a draft
successor schema — independently re-run and confirmed by the foreman.

## Decision

1. **No new evaluator op, no new collectible family, no second published
   finding.** `packages/derivation/evaluator.py`'s `ref`/`collect` ops and
   `packages/derivation/marshal.py`'s scalar-symbol resolution are extended,
   not replaced. Neither "runtime projection into a scalar collection"
   (Candidate A) nor "an explicit rule-produced numeric finding" (Candidate
   B) is adopted.
2. **A `field` selector on `ref_expr`.** A rule's `ref` node may carry an
   optional `field: string` alongside its existing `name`, naming a
   property on the bound fact type's `value_schema`. When present, the
   marshalled symbol resolves to `finding.value[field]` off the currently
   bound finding (the same finding `ref` already resolves against),
   flowing through the existing scalar path unchanged from that point
   forward — no new symbol kind, no new dependency-tuple shape beyond
   naming the field.
3. **A `rule-artifact.v7` schema successor is required — this is not free.**
   The current `rule-artifact.v6` schema's `ref_expr` shape
   (`{"op":"ref","name":string}`, `additionalProperties:false`) rejects any
   `field` key outright, correctly spelled or not
   (`case6-rung2-spike.md`, assertion 1). `v7` widens `ref_expr` to
   `{"op":"ref","name":string,"field"?:string}`, preserving
   `additionalProperties:false`. This is bounded, additive growth to one
   schema's one node shape — not the excessive expression-language
   broadening the milestone plan's decision rule warned against — but it is
   real schema growth, not a marshal-layer-only change, and must not be
   described as free.
4. **Fail-closed field validation is a load-time obligation, not a
   convenience.** Package validation
   (`packages/derivation/package_validation.py`) must reject, at load time,
   any `field` naming a property absent from the bound fact type's
   `value_schema.properties`, with a distinct, citable error (the spike's
   `FIELD_REF_UNKNOWN_FIELD`) — never a silent `None`/zero flowing through
   evaluation. This is the case-6 guarantee and is the one piece of this
   decision with direct executable evidence
   (`spike/case6_spike.py`, assertions 3-4, independently re-run by the
   foreman with the same pass/fail result).
5. **Provenance follows the real `pins_for` shape, not an invented one.**
   `it1`'s proposed pin shape (`{fact_type_id, identity, finding_id,
   field}`) is not grounded in `packages/derivation/runner.py`'s actual
   `pins_for` tuple (`{role, id, version, origin}`, resolving to finding
   ids only); `it2`'s account, deriving the field reference as part of the
   existing expression-tree dependency walk rather than inventing a new pin
   member, is the one this ADR adopts. A citation/explanation walk that
   reaches a field-ref-derived value must terminate at the same finding-id
   pin any other `ref` produces, with the field name recoverable from the
   rule artifact's own declared `ref_expr`, not from a new provenance
   field.
6. **Hostile-scalar and correction behavior inherit unchanged.** Because
   resolution reads whichever finding is currently bound (the same binding
   `ref` already uses), an independently asserted, unrelated scalar fact
   cannot be picked up by this mechanism — there is no second collection to
   prefer from — and a correction to the acquisition fact's value is
   visible the next time the same binding is marshalled, with no separate
   cache to invalidate. Both are inherited properties of the existing
   `ref`/marshal path, not new guarantees this ADR adds.

## Production conditions (owed to Seam 1's production implementation; never allowlisted)

- The real `rule-artifact.v6` → `v7` schema successor, checksum-published
  per the existing package-versioning discipline, with hand-written
  positive instances (a correctly-spelled field-ref) and named negatives (a
  misspelled field; a `field` on a `ref` bound to a fact type with no
  `value_schema.properties` at all; a `field` combined with a bound scalar
  fact type, which should be rejected as a category error, not silently
  ignored).
- The real `check_field_ref_bindings`-equivalent check, integrated into
  `package_validation.py`'s existing validation pass rather than left as
  spike-local code, with the exact `FIELD_REF_UNKNOWN_FIELD` (or renamed
  equivalent) error surfaced through the same channel other package
  validation errors use.
- Multi-acquisition scale evidence: both examinations' fixtures assumed
  exactly one acquisition per rule binding; `adversary-r1.md` named this as
  untested. Before production adoption, exercise a binding that could
  resolve against more than one live acquisition finding and confirm
  `marshal.py`'s existing "one current finding per binding, refuse on
  disagreement" behavior extends correctly to the field-ref case.
- The `it2`-identified "legacy fallback" binding path in `marshal.py`
  (symbol equals fact-type id) was not traced against case 2 (hostile
  scalar) by either examination (`adversary-r1.md`); confirm the field-ref
  extension does not reopen that path to a hostile substitution before
  adoption.

## Consequences

- Seam 2 (identity association) and Seam 5 (rule-owned consequences) can
  now charter against a real, evidence-backed value-extraction mechanism
  instead of an assumed one.
- A future object-valued canonical fact with a single scalar member a rule
  needs to read repeats this same field-ref pattern rather than reaching
  for a projected-scalar-family or explicit-derived-finding substrate,
  unless a source needs more than field-level access (e.g. computing over
  multiple fields, or fan-in aggregation across a member set — ADR-0054's
  domain) — a future decision, not resolved here.
- `rule-artifact.v6` remains valid, immutable history; `v7` is additive.
  No existing rule artifact is edited or reinterpreted by this decision.

## Alternatives Considered

- **Candidate A, runtime projection into a scalar collection.** Rejected:
  requires a new collectible family and closure mapping per object-valued
  source (the `it2` account is explicit that this repeats ADR-0054's
  rejected Option A pattern one level down), disproportionate to a
  single-field read, and produces a second, derived scalar fact whose
  relationship to the original object-valued fact would itself need a
  provenance story this ADR gets for free from the existing `ref`/pin path.
- **Candidate B, an explicit rule-produced numeric finding.** Rejected:
  publishes a second finding purely to re-expose a value the object-valued
  fact already carries: doubles the correction-and-supersession surface for
  no case in the milestone's T1-T9 set that Candidate C cannot already
  satisfy.
- **Treating the schema change as unnecessary ("marshal-layer only").**
  Rejected: disproven directly by `case6-rung2-spike.md` assertion 1 — the
  real, unmodified `v6` schema rejects the widened `ref_expr` shape outright
  before any marshal-layer code would ever run. `it1`'s original framing is
  not adopted; `it2`'s is.
