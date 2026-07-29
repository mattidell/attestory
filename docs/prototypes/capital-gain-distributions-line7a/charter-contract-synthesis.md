# Contract Synthesis Charter — Capital-Gain Distributions to Line 7a

Audience: Builder

Date: 2026-07-28. Track 0 of Capital-Gain Distributions and Form 1040
Line 7a.

## Context Capsule

- **Source ref and resolved launch commit:** use the current local
  `decisions/capital-gain-distributions-line7a` branch and verify its commit at
  launch.
- **Exact object:** synthesize the owner-selected and independently confirmed
  component-backed Rung-1 evidence into one proposed successor contract.
- **Role:** Contract Synthesis Builder, High capability / high effort.
- **Scope:** proposed ADR-0050, its advisory index entry, and the evidence
  analysis that makes every ADR clause traceable. No production artifacts.
- **Stop conditions:** any unresolved conflict in the selected evidence;
  governance interpretation; an attempt to edit accepted ADR text or published
  history; a new proposition, source family, evaluator feature, Schedule D
  implementation, real data, production code, or owner ratification.
- **Full reads before acting:** this charter; `final-disposition.md`; the topic
  `plan.md`; `round-1-triage.md`;
  `repair1-confirmation-disposition.md`; both exhibit designs and
  examinations; both committee reviews; both repair designs/examinations and
  confirmations; the milestone plan's Contracts, Published-schema and
  migration posture, Fixtures, and Data Safety sections; ADR-0010, ADR-0011,
  ADR-0012, ADR-0014 through ADR-0017, ADR-0023 through ADR-0025, ADR-0027,
  ADR-0029, ADR-0032, ADR-0035, ADR-0037, and ADR-0038; `docs/adr/INDEX.md`;
  and `PROJECT_PLANNING.md` sections “Prototype Before Ratification” and
  “Architecture Decision Records.”

## Assignment

Draft a plain-language Tier-2 successor contract from the selected evidence.
Do not reopen the topology comparison and do not copy the prototype's example
identifiers into normative contract names unless the evidence explicitly
selects them.

The ADR must settle:

1. the four contributed Exception-1 component assertions, their categorical
   and correction semantics, predicate E, and the checked
   Schedule-D-required conclusion;
2. the successor box-2a statement/member identity, independent family,
   horizon, closure, closed-empty meaning, multi-payer sum, non-null presence
   signal, and correction/removal behavior;
3. successor/historical exclusivity and the versioned dividend-universe
   transition without modifying any published schema, manifest, content, or
   accepted ADR;
4. contradiction behavior in both temporal orders and one batch;
5. line 7a and line 7b as distinct form-field dispositions, including blocked
   and guard-inapplicable states;
6. line 9 consuming line 7a exactly once and the declared downstream
   displacement chain;
7. the line-16 successor's typed state partition, QDCG selection when
   qualified dividends or applicable direct-route line 7a are positive,
   worksheet-line-3 binding, both-zero reduction, and no raw-source or
   assumed-zero path;
8. pins, citation obligations, presentation consequences, and production kill
   tests; and
9. the exact relationship to ADR-0035 and ADR-0038: accepted history remains
   immutable, while named clauses are superseded only for the versioned
   successor graph.

Record the component topology's additional contribution and correction costs,
the rejected conclusion-level alternative, the two repair cycles, the final
confirmation, and the final review's two non-blocking observations.

Every central decision clause must cite a named evidence file or exhibit. Do
not cite unmerged commits by SHA. Do not claim implementation or acceptance.

## Outputs

Create or modify exactly:

- `docs/prototypes/capital-gain-distributions-line7a/evaluation-analysis.md`
- `docs/adr/0050-capital-gain-distributions-and-line-7a.md`
- `docs/adr/INDEX.md`

The ADR status is **proposed** and inert. The index row must likewise say
`proposed` and provide only an advisory digest. `evaluation-analysis.md`
routes each adopted clause, rejected alternative, dissent/cost, production
condition, and unresolved non-blocking observation to the evidence chain
without retelling every case.

Do not modify a prototype exhibit, review, disposition, plan, phase state,
SEAT, accepted ADR, schema, manifest, content, fixture, test, production file,
or other documentation.

## Completion

Before writing, echo the selected contract boundary, evidence chain, three
outputs, proposed/inert status, and stop conditions.

Commit only the three outputs locally and stop. Do not push, merge, ratify the
ADR, begin production, perform ADR review, or advance the pointer. Return the
commit SHA and a clause-to-evidence summary.

## Data safety

All examples and citations remain synthetic and publishable. No personal
values, identities, dispositions, refusal reasons, workspace locations,
documents, screenshots, or private artifacts may enter the contract unit.
