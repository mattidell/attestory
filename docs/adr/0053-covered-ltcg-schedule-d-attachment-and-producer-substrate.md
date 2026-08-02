# ADR 0053 — Categorical Attachment Requirement and Selected-Producer Substrate

- Status: **accepted** (owner ratification recorded by merging PR #143;
  foreman-run paper spike, Gate 1 scores below the prototype-eligible band)
- Tier: 2 — narrow, additive schema/representation questions; not a
  product-thesis or rival-topology decision (Gate 1 scores 4 and 5, below
  the prototype-eligible band).
- Date: 2026-08-02

## Context

ADR-0052 (Covered Long-Term Gains, Schedule D Line 8a) named two production
conditions it deliberately left open rather than resolving inline: CA-05
(`attachment-rule.v2`'s `requirement` block is threshold-only, but Schedule
D's required/not-required disposition for this bounded class is
categorical) and CA-06 (whether two mutually exclusive rule citizens may
both `publish` the shared `selected-preferential-base` symbol, or a
dedicated selection mechanism is needed). Per `PROJECT_PLANNING.md` Gate 2,
a missing substrate surfaced mid-prototype routes to its own decision
rather than silent absorption into the next implementation track.

Both questions are narrow schema/representation choices, not competing
product topologies, so this ADR is grounded in a foreman-run paper spike
(`docs/prototypes/schedule-d-covered-ltcg-8a/ca05-ca06-paper-spike.md`) —
Rung 1 only, no Builder charter, no committee review — rather than a full
incumbent/rival prototype round.

## Decision

1. **Categorical attachment requirement (CA-05).** Publish
   `attachment-rule.v3` as an additive successor to `attachment-rule.v2`
   (unused version; `.v2` untouched, immutable history). Its `requirement`
   block becomes a `oneOf` between the existing threshold shape
   (`subtotals`/`threshold_parameter`/`comparison`/`citation`, unchanged)
   and a new categorical shape:

   ```
   requirement.categorical = {
     kind: "family_nonempty",
     source_family: <pin>,
     citation: <pin>
   }
   ```

   For this bounded class, Schedule D is required when the eligible
   long-term transaction source family (ADR-0052 Decision 1) is current and
   closed with at least one member; not required when it is current and
   closed-empty; the trigger is `blocked` (not `not-required`) when the
   family is unclosed, mirroring the existing threshold branch's honest
   block on an unclosed subtotal. This trigger is driven solely by the
   eligible-family's own presence — none of Decision 2's seven absence
   declarations independently triggers the requirement; their role remains
   completeness authority once the family already triggers it.

2. **No new substrate for the selected-preferential-base producer
   (CA-06).** Two separate rule citizens may not both declare `publishes`
   for one symbol — current package validation (ADR-0027 Decision 5) and
   ADR-0038 Decision 2's foreclosure of a dynamic `conflict_semantics`
   selector already establish that, read together. The resolution is not a
   new selection mechanism: model the selected preferential base as **one**
   rule citizen, pinning both the direct-route inputs (box-2a subtotal,
   C1-C4, the checked conclusion) and the Schedule-D inputs (Schedule D
   line 16, its attachment disposition, the nine completeness authorities),
   with a top-level `choose` expression (the existing evaluator operator,
   `packages/derivation/evaluator.py`) keyed on whether the eligible
   long-term family is current and closed-nonempty:

   - closed-nonempty selects the Schedule-D branch, which requires
     Decision 2's boundary and publishes Schedule D line 16's value; the
     untaken direct branch's inputs are never evaluated and therefore never
     named as missing;
   - otherwise selects the direct branch, which requires the checked
     conclusion and box-2a subtotal; the untaken Schedule-D branch's inputs
     are never evaluated.

   This is the same single-rule, internal-`choose` pattern already
   accepted and in production for `rule.form1040-line7a.json` and the
   current `rule.form1040-line16` successor — no new evaluator operation,
   schema, or generic substrate. ADR-0052 Decision 4's exact pin-signature
   table is unchanged by this decision; it is now understood as exactly
   which `choose` branch was taken, recoverable from the rule's own access
   log.

3. **Relationship to ADR-0052 and other accepted history.** This is an
   additive addendum to ADR-0052, not an edit to it — Decisions 3 and 4's
   text stands unchanged; this ADR discharges the two production
   conditions those decisions named as owed. ADR-0027, ADR-0036, and
   ADR-0038 remain immutable history; nothing here edits their accepted
   text. `attachment-rule.v2` and every other published schema/content
   citizen remain byte-unchanged.

## Production conditions (owed to Track 2; never allowlisted)

- The exact `attachment-rule.v3` JSON Schema text, its schema-registry
  publication, and Schedule D's `attachment.schedule-d.v1` citizen
  instantiating the categorical requirement shape.
- The exact `selected-preferential-base` rule citizen: its `choose`
  expression tree, both branches' pin sets (matching ADR-0052 Decision 4's
  table exactly), and its `publishes` identifier.
- Coordinator-from-facts goldens proving both branches, the family-presence
  trigger's blocked/not-required/required states, and that the untaken
  branch's absence never surfaces as a missing dependency.

## Consequences

- Schedule D's requirement disposition is categorical and honest: no
  numeric-threshold misfit, no fabricated attachment from a thin assertion.
- The selected preferential base has exactly one producer by construction
  (one rule citizen), not by a new generic multi-producer mechanism —
  keeping the accepted single-producer-per-symbol invariant (ADR-0027
  Decision 5) intact rather than carving an exception into it.
- Both resolutions are additive; no accepted ADR, schema, or content
  citizen changes.

## Alternatives Considered

- **A dedicated selected-binding citizen naming candidate producers with
  priority/guard semantics.** Rejected: would be new generic substrate for
  a case the existing single-rule/`choose` pattern already covers; adds a
  mechanism ADR-0038 Decision 2 already leaned away from (dynamic
  conflict-selection patterns) without a demonstrated need.
- **A boolean-flag route tag on the selected preferential base's payload.**
  Considered and rejected in ADR-0052 Decision 4 itself (the producer
  signature is already recoverable from disjoint pin lineage); this ADR
  does not reopen that question.
- **Leaving `attachment-rule.v2`'s threshold-only shape and forcing
  Schedule D's requirement into a synthetic numeric comparison** (e.g., a
  member-count "threshold" of zero). Rejected: misrepresents a categorical
  presence check as a numeric one, and the existing schema's
  `comparison: strictly_greater_than` const would need to be relaxed
  either way — no cheaper than the categorical `oneOf`.

## Links

- Paper spike: `docs/prototypes/schedule-d-covered-ltcg-8a/ca05-ca06-paper-spike.md`
- Builds on: ADR-0027 (package manifests, single-producer-per-symbol),
  ADR-0036 (attachment ontology), **ADR-0038** (dual-producer
  foreclosure), **ADR-0052** (the milestone contract this addendum
  discharges two named production conditions for)
- Consumed by: Covered Long-Term Gains, Schedule D Line 8a production
  Track 2 (only after ratification and merge)
