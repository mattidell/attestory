# ADR 0037 — Conditional Multi-Dependency Non-Publication

- Status: **accepted** (owner ratification 2026-07-18)
- Tier: 2
- Date: 2026-07-18
- Plain-language companion:
  [0037-conditional-multi-dependency-nonpublication](analyses/0037-conditional-multi-dependency-nonpublication.md)

## Context

Some declared rules need several factual dependencies only when a declared
condition is active. Existing evaluation stops at the first absent reference,
so it cannot name every current gap in one non-publication walk. Making all
dependencies unconditional blocks inactive returns; collecting names in a tax
runner, UI, or post-processing list puts rule meaning outside declared
artifacts.

D2 is the immediate consumer: qualified dividends require two
declared-absence facts, while qualified-zero returns owe neither. This ADR
defines a generic rule-language substrate, not a D2 exception.

Prototype evidence is the CMDN evaluation analysis. Two paper rivals ran the
same six cases. Governance found both schema-declared; Adversary rejected the
top-level conditional-requires rival because it allowed a conditionally
demanded but unpinned member to escape supersession. The evaluator-node
candidate converged at Rung 1.

## Decision

1. **Declared expression.** A new rule-artifact schema version admits
   conditional_dependency_set as a boolean guard expression carrying:

   - a declared condition expression; and
   - a non-empty ordered array of declared ref member expressions.

   It is declared eligibility logic, never a runner-private list,
   tax-specific branch, UI repair, or post-processing convention.

2. **Evaluation.** The evaluator reads the condition first. If false, the node
   succeeds and evaluates no member. If true, it evaluates each member once and
   accumulates every dependency-absence result. Any absence stops evaluation of
   that rule with the existing dependency-absent category and the complete
   ordered absent-member list. Non-absence errors retain their ordinary
   behavior. If all members are present, the node succeeds.

3. **Pins and currency.** Every evaluated condition and member enters the
   normal access log. A published finding pins the condition and all active
   members through existing derivation edges. Inactive members are neither
   evaluated nor pinned. Supersession uses only existing
   derivation/individuation edges; contribution resolving a blocked absence is
   observed by a new run and creates no third edge.

4. **Explanation.** The record and NPE walk carry all and only accumulated
   missing members through the existing dependency-absence and missing-list
   surfaces unless implementation proves a versioned schema change necessary.
   This ADR adopts no opaque multi-missing error code.

## Production conditions

1. Publish the schema version; members must be non-empty and ref-only.
2. Implement all-member accumulation and access logging; preserve ordinary
   non-absence failure propagation.
3. Prove all-missing and partial-missing record/NPE walks; no present member
   may appear as missing.
4. Supply coordinator-from-facts goldens for the six paper cases, including
   inactive isolation and condition/member supersession.
5. Prove portability with a second runner and reject mutations that bypass
   member pinning or introduce a tax-specific missing-list path.

## Consequences

- D2 can require both capital-gain declarations only on its qualified path and
  explain both absent facts honestly in one walk.
- Future rules gain generic conditional completeness without hidden runner
  policy.
- The rule schema and evaluator grow together and must preserve the closed,
  portable language contract.

## Alternatives considered

- **Top-level conditional-requires gate (IT2).** Rejected: a member can control
  eligibility without being an evaluated pinned input, so its supersession can
  leave a stale result current.
- **Unconditional requires.** Rejected: demands inactive members.
- **First-missing reporting.** Rejected by the owner's D2 requirement.
- **Runner/UI aggregation.** Rejected by Articles 11 and 15 because rule
  meaning and explanation would depend on code-private behavior.

## Links

- Prototype evidence:
  docs/archive/2026-08-02-milestone-artifacts/prototypes/conditional-multi-dependency-nonpublication/
- Builds on: ADR-0006, ADR-0010, ADR-0020, ADR-0024, ADR-0025, ADR-0034
- Consumed by: D2 QDCG worksheet; a prerequisite production track before D2
  adoption
