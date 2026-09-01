# ADR 0070 — Accrued-Amount Supportability, Per-Pairing and Aggregate

- Status: **accepted**
- Tier: 2 — the consumer, rule-owned consequences, builds on this; not a
  product-thesis or governance-meaning decision.
- Date: 2026-08-29

## Context

Once an acquisition and a report are associated (ADR-0068), a further
question is where the return of capital claim's own physical
constraint — the accrued amount cannot exceed the associated report's own
amount — is enforced. This is kept deliberately separate from the
identity question (already decided) and from what the current-year
consequence and basis publication actually compute (a downstream,
consuming question).

A single pairing's own comparison is not the whole of the constraint. A
Form 1099-INT statement can be legitimately associated with more than one
acquisition (ADR-0068 Decision 6); each pairing can individually pass its
own report-amount comparison while the group's *combined* claim against
that one shared report still exceeds what the report actually supports.
Detecting that requires a second, aggregate check, layered after the
per-pairing one — a report-group failing that check is not evidence that
no adjustment applies at all, only that the claimed adjustment set, taken
together, is internally inconsistent with the report it depends on.

## Decision

1. **Tax-rule machinery, not association machinery, not a generic
   mechanism.** The supportability check is an adopted tax rule consuming
   the field-ref-extracted accrued amount and the published pairing
   finding. It is not attached to the pairing record itself, which would
   mix structural identity with substantive treatment.
2. **Per-pairing dispatch resolves the report by dereferencing the
   pairing's own pinned fact id, never by generic "current" binding.**
   An ordinary rule fires once per rule id into a single-value-per-symbol
   table; per-pairing dispatch is a distinct mechanism, firing once per
   runtime-discovered pairing finding (via the pairing type's own
   collect-source registration), each pin naming only its own acquisition
   and its own dereferenced report. This is structural, not conventional,
   masking prevention: an unrelated report of the same type — however
   large — is never bound, never read, and cannot numerically mask a
   real violation the way an ordinary `ref` binding on the report's fact
   type would (which leaves the symbol unbound and blocks with the wrong
   diagnosis whenever two disagreeing current reports exist).
3. **Multiple acquisitions sharing one report evaluate individually at
   this tier, never cumulatively.** Two acquisitions independently paired
   with the same report each receive their own independent supportability
   finding, evaluated against the full reported amount, with no
   cross-contamination between the two evaluations. This holds even where
   the sum of two individually-supportable amounts would exceed the
   report if compared cumulatively — that combined question is answered
   by Decision 6 below, deliberately kept separate from this per-item
   check.
4. **A named, distinct per-pairing failure disposition.** The rule blocks
   with `ACCRUED_EXCEEDS_ASSOCIATED_REPORT` when the per-pairing
   constraint fails, via the evaluator's `compare`/`choose`/`block`
   grammar — never a silent clamp, never a pass.
5. **Correction re-evaluates.** A correction to the reported amount (or
   the acquisition's accrued amount) is visible the next time the pairing
   is dispatched, with no separate invalidation step.
6. **A second, aggregate check groups every current-year-adjustment
   publication in one run by the specific report fact id its pairing
   names, sums the claims per report, and compares the sum to that
   report's own amount.** This is layered after per-pairing dispatch, a
   distinct rule (`rule.interest.current-year-adjustment.aggregate-
   supportability`) rather than a cumulative rewrite of Decision 3 — the
   per-item and aggregate questions stay separate.
7. **Named, scoped blocking — not a whole-run halt.** A report-group
   whose combined claim exceeds its report blocks with a distinct
   disposition code, `AGGREGATE_ACCRUED_EXCEEDS_REPORT`, naming the
   report fact id. Only that report-group's contribution is excluded;
   unrelated report-groups and every individual per-pairing verdict are
   unaffected — the same pairing-scoped dispatch convention this
   mechanism already establishes at the per-item tier: a specific thing
   being wrong does not halt everything else that is right.
8. **No allocation policy, at either tier.** This decision detects and
   excludes an over-claimed individual pairing or report-group; it does
   not decide how much of a report an acquisition, or a group of
   acquisitions, is "really" entitled to.
9. **An aggregate block retracts the individual claims that composed it
   — it does not leave them published alongside the block.** When a
   report-group's combined claim exceeds its report, that group's
   individual current-year-adjustment and basis findings are retracted
   from the run's publications and their disposition rows are rewritten
   from `published` to `blocked`. An individually-plausible finding that
   was only plausible as part of an aggregate set that failed is not
   available downstream as an ordinarily-supported input to any other
   consumer.
10. **The current-year subtotal blocks entirely rather than excluding the
    failed group and publishing the remainder as a settled, differently-
    scoped number.** The aggregate check establishes only that the
    report-group's combined claim is internally inconsistent with that
    report's own amount — it does not establish that no adjustment
    applies, nor that the unadjusted gross figure is the ordinarily
    correct one. The subtotal therefore blocks entirely when any
    report-group is blocked, propagating through the existing
    dependency-absence mechanism. The affected return result carries an
    explicit unsupported/blocked standing; it is never offered as an
    ordinarily-computed total under a different, unstated confidence.

## Production conditions (owed to production implementation; never allowlisted)

- No allocation policy exists, at either tier, for an over-claimed
  pairing or report-group where the product might eventually want to
  admit a partial, allocated amount rather than block. Not decided here;
  full retraction and block propagation is the safe default until a
  product decision says otherwise.
- The same obligation entered twice with a mismatched amount is
  orthogonal to both checks and remains a named residual risk (see
  ADR-0068).

## Consequences

- Rule-owned consequences charter against a real, evidence-backed
  supportability verdict at both the individual and aggregate scope,
  instead of an assumed one. `tests/test_supportability.py` and
  `tests/test_aggregate_supportability_live.py` cover both rule citizens'
  positive and negative payload instances: one pairing, masking,
  multiple acquisitions sharing one report both within and beyond its
  combined amount, and correction.
- A future per-pairing evaluation need (anywhere a rule must fire once
  per a runtime-discovered relationship rather than once per rule id)
  repeats this dispatch pattern — driven by the actual pairing findings a
  run has, resolving a peer fact id by dereference rather than generic
  type binding.
- A future pairing-scoped consequence that shares a source across
  multiple pairings repeats this same two-tier pattern: a per-pairing
  check for the individual question, plus a separate aggregate check
  grouped by the shared source, with an aggregate failure retracting the
  individual claims that composed it and blocking propagation to any
  dependent total — rather than assuming per-pairing correctness composes
  into aggregate correctness, or excluding the failed contribution and
  presenting the remainder as a settled, differently-scoped number.
- `_evaluate_family_validation` is untouched by either check; only its
  per-instance iteration shape is reused as a template.

## Alternatives Considered

- **A constraint attached to the association record.** Rejected:
  conflates structural identity with substantive treatment, which the
  identity mechanism deliberately keeps separate.
- **A generic relationship-validation mechanism.** Rejected: no code
  path validates a relationship across two independently-pinned findings;
  building one generically would be disproportionate to this one need.
- **Ordinary rule dispatch without dedicated per-pairing machinery.**
  Rejected: an ordinary rule cannot express "once per pairing finding"
  without a synthesized per-instance dispatch; a naive `ref` binding on
  the report's fact type leaves the symbol unbound and blocks with the
  wrong diagnosis whenever two disagreeing current reports exist.
- **Cumulative comparison across multiple acquisitions sharing one
  report, folded into the per-pairing rule itself.** Rejected: would
  require the per-pairing rule to see every other pairing sharing its
  report at evaluation time, conflating a per-item check with an
  aggregate one for no case that a separate aggregate check cannot
  already answer.
- **Halt the entire run on any aggregate over-claim.** Rejected:
  inconsistent with the established pairing-scoped dispatch convention,
  and would block unrelated, entirely correct pairings for an unrelated
  report's defect.
- **Silently cap the subtotal at each report's amount instead of
  blocking.** Rejected: an unstated allocation policy hidden inside an
  aggregation step.
- **Exclude the blocked group's contribution and publish the remainder as
  a settled, differently-scoped gross total.** Rejected: the aggregate
  check establishes only that the claimed adjustment set is internally
  inconsistent, not that the unadjusted gross figure is ordinarily
  correct.
- **Leave the individually-plausible findings published and only block
  the subtotal.** Rejected: findings that were only plausible as part of
  a failed aggregate set would remain available to any other consumer as
  if independently supported.
- **Publish the excluded-group subtotal as a distinct, lower-confidence
  figure instead of blocking.** Rejected: no established mechanism exists
  for a distinguishable confidence tier on a published amount; blocking
  reuses the existing dependency-absence mechanism instead of introducing
  new, undecided scope.
