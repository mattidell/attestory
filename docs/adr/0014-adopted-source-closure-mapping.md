# ADR 0014 - Adopted Source-Closure Mapping

- Status: accepted (ratified 2026-07-12)
- Tier: 2
- Date: 2026-07-12

## Context

ADR-0011 requires affirmative-only source closure but deliberately leaves the
closure-finding-to-`collect` mapping undecided. Source Completeness Track 0
tested a reusable mapping citizen against an embedded-rule parameter and then
exercised false, absent, displaced, ambiguous, caller-injected, fabricated, and
alternate-entry failures through a copied calculation path.

Evidence: `docs/prototypes/source-completeness/evaluation-analysis.md`, C1–C3.

## Decision

1. Source closure enters calculation through an independently versioned and
   adopted mapping citizen, reusable across collecting rules.
2. A mapping declares source-family identity/scope, member fact type, closure
   fact type/identity, and the affirmative admission condition. The adopted
   mapping version is pinned by the run.
3. Exactly one matching current closure finding whose value is literal boolean
   `true` authorizes empty-source publication. False, absent, displaced,
   truthy-non-boolean, ambiguous, or duplicate authority blocks.
4. The runner exposes one supported dispatch path that resolves mapping and
   findings internally. Caller-supplied closed sets or authority carriers are
   not accepted inputs and cannot augment membership.
5. A closure-backed zero pins the exact mapping version and exact current
   closure finding used. Present-source aggregation does not consult or pin
   closure authority.

## Not Decided

- natural-language closure claim and source-family/coverage universe (SC-P3);
- coverage read-model presentation;
- production schema ids/bytes;
- citation resolution; or
- persisted implementation details beyond the required observable contract.

## Consequences

- `RunContext.closed_sets` must be removed, not renamed or retained as a second
  writer.
- Production must audit every environment construction and dispatch route.
- Mapping adoption, pins, computed-zero distinction, and closure-withdrawal
  displacement become required contract tests.
- Prototype code is reimplemented, never promoted by similarity.

## Alternatives Considered

- Caller-supplied sets: rejected as unpinned authority.
- Embedded mapping per rule: rejected for duplication/divergence and tested
  same-family rule-addition outage.
- Presence-only projection: rejected by false-closure mutation evidence.

## Links

- Analysis: `docs/prototypes/source-completeness/evaluation-analysis.md`
- Exhibits: `exhibits/source-completeness/it1`, `it2`, `repair1`–`repair4`
- Milestone: `docs/phases/foundation/milestones/source-completeness-and-interest-slice.md`
- Precedents: ADR-0005, ADR-0010, ADR-0011, ADR-0013
