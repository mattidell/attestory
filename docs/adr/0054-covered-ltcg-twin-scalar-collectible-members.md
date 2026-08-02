# ADR 0054 — Twin Scalar Collectible Companions for Multi-Field Members

- Status: **accepted** (owner ratification recorded by merging this
  decision unit's PR; foreman-run paper spike, Gate 1 scores in the
  prototype-eligible band but the owner directed lightweight treatment)
- Tier: 2 — resolves a Track-2 charter-stop; sets a reusable template for
  future multi-scalar-member sources, but is not a product-thesis or
  governance-meaning decision.
- Date: 2026-08-02

## Context

Track 2's Builder filed a charter-stop against
`docs/reviews/charter-2026-08-02-schedule-d-covered-ltcg-8a-track2.md`:
Track 1's eligible-transaction member fact type
(`tax.us.2025.f1099b.covered-ltcg-txn`) is object-valued, carrying
`proceeds`, `basis`, `gain_only`, and eight other predicate fields on one
finding — exactly what ADR-0052 Decision 1 requires, and correct, immutable
Track-1 content. Schedule D line 8a (ADR-0052 Decision 3) needs two
independent numeric sums across the eligible-member set (proceeds, basis;
gain is `(d)-(e)`, not a third summed field), but every existing collection
path in the engine (`packages/derivation/evaluator.py`'s `collect` op,
`packages/derivation/marshal.py`'s `marshal_run_context`,
`packages/derivation/runner.py`'s `SourceFact.value: str`) assumes a single
scalar member value, matching every prior `collect_members` precedent
(1099-INT, K-1, 1099-DIV, market discount). Neither of the two paths that
would unblock this — editing Track 1's citizen shape, or adding new
evaluator/marshal field-projection substrate — is available inside Track
2's charter; both are named stop conditions.

Foreman-run paper spike:
`docs/prototypes/schedule-d-covered-ltcg-8a/track2-multi-scalar-member-paper-spike.md`.
Gate 1 scores the underlying question (generic field-projection substrate
vs. a scoped additive companion-citizen shape) at approximately 6 — the
prototype-eligible band — because whichever mechanism is chosen becomes the
template for future multi-scalar-member sources. The owner directed the
same lightweight, foreman-authored-paper-plus-short-ADR treatment already
used for CA-05/CA-06 (ADR-0053) rather than a full incumbent/rival
committee round.

## Decision

1. **No new generic evaluator or marshal substrate.** `collect`,
   `collect_members`, `marshal_run_context`, and `SourceFact` remain
   unchanged. The object-valued field-projection extension considered in
   the paper spike (Option A) is not adopted — it is more general than
   this milestone's two-scalar case requires, and its blast radius is the
   whole engine's evaluation core, not just this milestone.
2. **Twin scalar collectible companions.** Track 1's object-valued
   eligible-transaction member fact type is untouched — no edit, no new
   version. It continues to gate admission and serve as the audit record
   of the full contributed predicate. Two new, purely additive sibling
   fact types are published at the same identity `(tax-year, subject,
   statement-anchor-ref, logical-transaction-ref)`:

   - `tax.us.2025.f1099b.covered-ltcg-txn.proceeds` — scalar `proceeds`,
     its own new source family and closure mapping;
   - `tax.us.2025.f1099b.covered-ltcg-txn.basis` — scalar `basis`, its own
     new source family and closure mapping.

   Both are unconditionally admitted, exactly matching every existing
   `collect_members` precedent's scalar shape (`source_amount: true` on a
   scalar member). The contribution act that admits an eligible
   transaction writes the object finding and both scalar findings
   together at one identity, keeping them in lockstep; a correction to a
   transaction's amounts corrects all three findings at the same identity,
   closed under the same horizon-advance discipline Track 1 already
   established for the object family. Two sales from one broker, or one
   corrected transaction, follow Track 1's existing identity/correction
   rules unchanged — this ADR adds no new identity behavior.

3. **Schedule D line 8a arithmetic.** Column (d) is `collect_members` over
   the proceeds family; column (e) is `collect_members` over the basis
   family; column (h) is `(d)-(e)`, per ADR-0052 Decision 3 — no third
   scalar family. The tie-out invariant (`ITEMIZATION_TIE_OUT_VIOLATION`,
   ADR-0036 Decision 3) applies to this row set exactly as it applies to
   every other attachment content Track 2 publishes.
4. **Completeness authority unchanged.** ADR-0052 Decision 2's first
   completeness authority ("the eligible long-term family closed")
   continues to read the *original* object-valued family's closure. The
   two new scalar families' closures are additional required authorities
   for Schedule D's line-8a/13/15/16 computation specifically, not a new
   completeness-boundary category, and not a substitute for the object
   family's own closure requirement.
5. **Relationship to ADR-0052, ADR-0053, ADR-0036, and Track 1.** This is
   an additive addendum to ADR-0052 — it settles the collection mechanism
   Decision 3 left unspecified, without editing any Decision text. ADR-0053
   is unaffected (its `attachment-rule.v3` and selected-preferential-base
   decisions are orthogonal to how line 8a's sums are collected). ADR-0036
   remains immutable history; nothing here changes the attachment ontology.
   No Track-1 citizen — schema, content, or checksum — is edited, reformatted,
   or version-bumped by this decision.

## Production conditions (owed to Track 2; never allowlisted)

- The exact fact-type/family/closure-mapping schema/content citizens for
  both new scalar companions, with hand-written positive instances
  (Payload Instantiation Gate) and named negatives (a scalar family
  missing its sibling object/companion at the same identity; a proceeds or
  basis value asserted without the object finding; mismatched identities
  across the three sibling findings).
- The exact contribution-act shape that writes all three findings
  atomically at one identity (a Track-2 implementation detail this ADR
  does not choreograph).
- Coordinator-from-facts goldens proving: both scalar sums tie out to the
  object family's member count; a correction to one transaction updates
  all three sibling findings and displaces every downstream Schedule D
  publication; and the two new families' closures are required
  independently of the object family's closure for Schedule D content to
  publish.

## Consequences

- Track 2 can resume under its existing charter (`charter-2026-08-02-schedule-d-covered-ltcg-8a-track2.md`)
  without a rewrite — this ADR settles how deliverable 2 (Schedule D
  content) sources its column sums; the charter's other deliverables are
  unaffected.
- A future multi-scalar-member source repeats this same additive-companion
  pattern rather than reaching for generic field-projection substrate,
  unless a source needs three or more scalar quantities or conditional
  projection, at which point Option A's cost may become worth paying — a
  future decision, not resolved here.
- Track 1's committed citizens remain byte-for-byte unchanged; this
  milestone's identity discipline (no evidence/document identity, distinct
  transactions, correction preserving sibling identity) is unaffected.

## Alternatives Considered

- **Option A, generic field-projection substrate.** Rejected for this
  milestone: touches core derivation machinery (`evaluator.py`,
  `marshal.py`, `SourceFact`) used by every existing rule, a blast radius
  disproportionate to a two-scalar need; more general than required. Not
  ruled out permanently — a future source with three or more scalar
  quantities, or a need for conditional field projection, may justify it.
- **Editing Track 1's member fact type to carry scalar fields directly.**
  Rejected: forbidden by schema immutability (ADR-0003) and this
  milestone's own Track-2 charter boundary; would also require a version
  bump touching every existing consumer of the v1 shape (none yet exist in
  production, but the discipline holds regardless).
- **A single merged scalar (e.g., only `gain`) instead of twin
  proceeds/basis companions.** Rejected: ADR-0052 Decision 3 requires
  separate column (d) and (e) sums, not only column (h); a single merged
  scalar cannot supply both.

## Links

- Paper spike: `docs/prototypes/schedule-d-covered-ltcg-8a/track2-multi-scalar-member-paper-spike.md`
- Builds on: ADR-0003 (schema immutability), ADR-0010 (currency), ADR-0011
  (closure / presence-before-value), ADR-0014-0017 (mapping, identity,
  family, horizon), ADR-0023 (member transitions), ADR-0032 (contribution
  boundary), **ADR-0036** (attachment ontology, tie-out), **ADR-0052**
  (the milestone contract this addendum discharges Decision 3's
  unspecified collection mechanism for)
- Consumed by: Covered Long-Term Gains, Schedule D Line 8a production
  Track 2 (resumes under its existing charter after ratification and
  merge)
