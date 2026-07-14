# ADR 0018 - Member Assertion and Transition Boundaries

- Status: proposed
- Tier: 2
- Date: 2026-07-13

## Context

Reconciliation review `docs/reviews/2026-07-13-source-completeness-reconciliation.md` exposed two defects in the admission boundary:
1. **SC-R1**: A predicate-matching member fact for an adopted family could be asserted directly through a plain `assertion`, bypassing the `member-transition` chain. This allowed the family's closure finding and closure-backed zeros to remain current despite a new member being introduced.
2. **SC-R2**: A same-member value correction could be submitted as a `member-transition`, advancing the horizon and invalidating current closure authority unnecessarily, when it should have been routed through the ordinary assertion path instead.

These defects violate Constitution Articles 7, 12, and 13. While ADR-0017 decision 3 requires membership changes to advance the horizon and rejects malformed transitions, the exact boundary between plain assertions and member transitions was not enforced by the kernel.

## Decision

1. **Rejection at Admission for New Member Assertions**: A plain `assertion` act for a fact whose type matches the member predicate of any adopted source family is rejected at admission with `FindingModelError` if the fact is not already currently a member of that family. This directs new member insertions exclusively to the `member-transition path`.
2. **Rejection of Same-Member transitions**: A `member-transition` asserting a member fact that is already currently in the family (i.e. a same-member value correction) is rejected at admission with `FindingModelError`. Such value corrections must use the ordinary `assertion` path.
3. **Registry-Carried Predicates**: The `SchemaRegistry` maintains the set of registered family member predicates. The consuming layer's registry builder (e.g. `tax_registry`) populates this set during initialization by loading the adopted source family declarations. This keeps the kernel generic and content-agnostic.

## Consequences

- Stale closure findings and closure-backed zeros are guaranteed to be displaced or invalidated when a late member is introduced, as the insertion must go through a horizon-advancing member-transition.
- Value corrections for existing family members do not advance the horizon or displace current closure authority.
- The generic kernel package remains independent of specific source-family schemas and directories, but is configurable by consuming layers.
- Valid-transition lifecycle guarantees are preserved.

## Alternatives Considered

- **Atomic Routing**: Atomically advancing the horizon on a plain member assertion. Rejected because it blurs the boundary between ordinary acts (non-horizon-advancing) and transition acts, introducing complex composite semantics.
- **Tolerant / Post-Fact Validation**: Validating this constraint during calculation/coverage rather than at kernel admission. Rejected because it allows inconsistent or invalid state sequences to accumulate in the act log.

## Links

- Charter: [charter-2026-07-13-source-completeness-patch.md](file:///Users/mattidell/git/personal/finances/docs/reviews/charter-2026-07-13-source-completeness-patch.md)
- Review: [2026-07-13-source-completeness-reconciliation.md](file:///Users/mattidell/git/personal/finances/docs/reviews/2026-07-13-source-completeness-reconciliation.md)
- Precedents: [ADR-0016](file:///Users/mattidell/git/personal/finances/docs/adr/0016-source-family-claim-and-composition.md), [ADR-0017](file:///Users/mattidell/git/personal/finances/docs/adr/0017-recorded-family-horizons-for-closure-freshness.md)
