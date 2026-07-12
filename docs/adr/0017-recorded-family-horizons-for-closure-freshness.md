# ADR 0017 - Recorded Family Horizons for Closure Freshness

- Status: proposed
- Tier: 3
- Date: 2026-07-12

## Context

A closure-backed empty result pins a closure finding but cannot pin a future
member. Existing ADR-0010 edges therefore cannot make the old result noncurrent
when a previously unknown relevant member is later recorded. Manual closure
withdrawal, derived closure, stored staleness, and a third edge are unacceptable.

Evidence: `docs/prototypes/closure-freshness/evaluation-analysis.md`.

## Decision

1. Each versioned source-family declaration and scope has an ordinary recorded
   membership-horizon citizen with explicit succession.
2. A closure fact is keyed on the family horizon current at attestation. Closure
   remains a user-attested determinable fact; the horizon does not compute or
   negate closure truth.
3. Every accepted membership-changing transition—add, remove, or change across
   the canonical member predicate—atomically records exactly one successor
   horizon for the same family/scope and current predecessor. A malformed or
   missing successor rejects the entire transition.
4. A same-member value correction that does not change predicate membership
   does not advance the horizon.
5. Horizon succession is an individuation root. It displaces closure facts and
   findings keyed on the predecessor horizon; existing derivation edges from
   the closure finding displace closure-backed results. No third edge or derived
   authority is introduced.
6. Currency is derived from immutable accepted acts. Incremental projection and
   full rebuild must agree. Supersession roots accumulate, so removal cannot
   resurrect an old result.
7. After a horizon change, new true closure attestation and explicit rerun are
   required before a successor closure-backed result may publish.

## Consequences

- Late members invalidate old closure authority without manual withdrawal.
- Closure truth stays user-attested; computation affects applicability/currency,
  not the historical assertion.
- Horizon identity must bind exact family declaration/version and scope.
- Production admission, replay, and currency tests are contract requirements.
- This ADR extends ADR-0010's use of individuation roots; it does not amend
  Article 7 or authorize reserved derived-finding authority construction.

## Not Decided

- Production schema ids/bytes and act-kind names;
- UI/presentation of stale closure;
- extraction/import workflow;
- transaction storage implementation; or
- tax-family content beyond accepted ADR-0016 semantics.

## Alternatives Considered

- Manual withdrawal: rejected as optional correctness.
- Derived false closure: rejected because it replaces attested authority.
- Computed divergence injected as root: rejected as a disguised third edge.
- Stored stale flag/listener: rejected by record-derived currency constraints.
- Direct member-to-zero edge: rejected by Article 7.

## Links

- Analysis: `docs/prototypes/closure-freshness/evaluation-analysis.md`
- Exhibits: `exhibits/closure-freshness/it1`, `it2`, `repair1`
- Milestone: `docs/phases/foundation/milestones/source-completeness-and-interest-slice.md`
- Precedents: ADR-0009, ADR-0010, ADR-0011, ADR-0014, ADR-0016
