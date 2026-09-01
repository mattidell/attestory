# ADR 0071 — Rule-Owned Current-Year Adjustment and Basis Consequence via Two Pairing-Scoped Rules

- Status: **accepted**
- Tier: 2 — the last seam before production integration. Not a
  product-thesis or governance-meaning decision.
- Date: 2026-08-29

## Context

Once a pairing's supportability verdict passes, an adopted rule must
publish both the current-year interest adjustment and the item-level
basis consequence. The incumbent mechanism for this treatment
(`rule.scheduleb-adjustment.accrued-interest-subtotal`) is a real,
checksum-published adopted rule, but its fact type's identity is keyed to
a Schedule B form-row entity structurally disjoint from any acquisition
or report identity, with the adjustment amount directly user-attested
rather than rule-derived at all. The real discriminator against the
incumbent is dependency and association provenance, where it is
structurally incapable, not merely harder to trace — the incumbent's
identity cannot name the reported item it reduces.

## Decision

1. **The declared mechanism replaces the incumbent in function, not in
   place.** An adopted rule whose fact-type identity cannot name the
   reported item it reduces is replaced by two adopted rules whose
   identity is the acquisition/report pairing itself. The existing
   `rule.scheduleb-adjustment.accrued-interest-subtotal` artifact and its
   fact type are not edited or reinterpreted by this decision.
2. **Two separate pairing-scoped rule artifacts, not one rule publishing
   two findings.** One rule publishes the current-year interest
   adjustment; a second, independent rule publishes the item-level basis
   consequence. Each applies the same per-pairing dispatch pattern on its
   own, gated on the supportability verdict passing for the same pairing
   finding. Ordinary rule dispatch publishes exactly one finding per rule
   id; no dispatch loop anywhere in the runner appends twice within one
   iteration, so two separate rule artifacts — not one rule producing two
   findings — is the only shape ordinary dispatch actually supports.
3. **Each rule's own declared `value` expression genuinely controls what
   is published.** Dispatch builds a pairing-local `Environment` whose
   symbols bind the acquisition and report fact-type ids to *this specific
   pairing's own* resolved left/right values — never the run-wide
   "current" binding a global `ref` lookup would otherwise return — and
   evaluates the adopted rule's actual `value` field through the same
   closed-vocabulary expression evaluator every ordinary (non-pairing-
   scoped) rule's `value`/`when` already uses. No second evaluator is
   invented. A genuinely different declared `value` on a successor rule
   changes what gets published; this is what makes rule succession real
   rather than a pin-shape claim only.
4. **The expression's dynamic dependencies are truthfully pinned.**
   Evaluating a rule's declared `value` builds an access log of every
   parameter, table, operation-semantics citizen, ref, and closure read
   the expression actually touched. That access log is converted into the
   same dependency-pin classes ordinary (non-pairing-scoped) rule
   evaluation already produces, composed with — never replacing — the
   pairing-specific left/right/pairing/supportability pins dispatch
   assembles unconditionally. Parameter and operation-semantics pins
   remain provenance only, never displacement roots, matching the
   unchanged design ordinary rule evaluation already uses for those pin
   classes; what a successor's declared dependency actually is, is now
   truthfully recorded, never silently omitted.
5. **Independent rule succession is a real advantage of the two-rule
   shape.** Because the two consequences are separate rule artifacts,
   superseding one (a future basis-consequence rule revision, say) does
   not require touching or re-superseding the other — the
   current-year-adjustment finding, including its own rule-version pin,
   is untouched by a basis-rule successor.
6. **Correction displacement follows from shared pins, with no new
   machinery.** Both findings pin the same upstream dependencies
   (acquisition amount, report amount, the pairing finding, the
   supportability verdict). A correction to the acquisition or the
   pairing displaces both consequences directly, one hop. A correction to
   the report displaces the supportability finding first, which then
   displaces both consequences, two hops — the supportability verdict is
   never itself a correction root; it only displaces as a consequence of
   what it depends on.
7. **Exact rule identity, dependencies, association, and citation are
   pinned, not asserted.** Both published findings carry: their own
   rule-artifact pin (distinct per rule, satisfying independent
   succession); the acquisition and report source-fact pins; the pairing
   finding's pin (association support); and a citation pin supporting the
   treatment.

## Production conditions (owed to production implementation; never allowlisted)

- Name and select the item-level basis consequence's consumer: this
  decision establishes that the basis finding is published with correct
  provenance and independent succession; it does not yet name what
  later-year disposition path consumes it.

## Consequences

- Production integration charters against a real, evidence-backed
  consequence-publication mechanism. The current-year adjustment's exact
  line-2b aggregator successor is `rule.form1040-line2b.v6` (ADR-0072
  Decision 4), reached only through a real migration-adoption act.
  `tests/test_pairing_consequences.py` and
  `tests/derivation/test_pairing_dispatch.py` cover both rule citizens'
  positive and negative payload instances: one pairing, independent
  succession of each rule, both the one-hop and two-hop
  correction-displacement cases, and a parameter and an
  operation-semantics dependency proving both the number and the exact
  pins/displacement.
- A future tax concept needing two independently supersedable published
  consequences from one supported relationship repeats this two-rule,
  per-pairing-dispatch-twice pattern, rather than assuming one rule
  evaluation can publish multiple independently cited findings — it
  cannot, given the runner's own dispatch discipline.
- `rule.scheduleb-adjustment.accrued-interest-subtotal` and its fact type
  are untouched; this decision does not edit, migrate, or deprecate them
  in place. Coexistence with the legacy path during migration is a named
  production condition.
- A future pairing-scoped consequence rule built on this same primitive
  inherits real declared-expression control and real dependency pinning
  without needing to re-litigate whether the rule or the runner owns the
  arithmetic, or re-derive how to convert an access log into pins.

## Alternatives Considered

- **One rule publishing two findings per pairing.** Rejected: no real
  dispatch loop in the runner has ever appended twice within one
  iteration; this shape would require genuinely new, unbuilt dispatch
  machinery for no case the two-rule shape cannot already satisfy.
- **Continuing to patch the incumbent fact type/rule.** Rejected: its
  identity is structurally incapable of naming the reported item it
  reduces — not a traceability gap patching could close without changing
  the fact type's identity, which schema immutability forbids in place.
- **A single merged finding carrying both the current-year adjustment and
  the basis consequence.** Rejected: a merged finding would defeat the
  independent-succession property that is a real, demonstrated advantage
  of the two-rule shape.
- **Leaving dynamic dependencies unpinned once the declared expression
  controls execution.** Rejected: a checksum-published successor could
  then change behavior through a parameter, table, or operation-semantics
  citizen while its published result omitted the authority that actually
  determined the value, letting explanation, correction, and currency
  disagree with what execution actually did.
