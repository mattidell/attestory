# Contract Synthesis Charter — Covered Long-Term Gains, Schedule D Line 8a

Audience: Builder

Date: 2026-08-01. Track 0 of Covered Long-Term Gains, Schedule D Line 8a.

## Context Capsule

- **Source ref and resolved launch commit:** use the current local
  `decisions/schedule-d-covered-ltcg-8a` branch and verify its commit at
  launch.
- **Exact object:** synthesize the owner-selected and independently confirmed
  Rung-1 evidence into one proposed successor contract.
- **Role:** Contract Synthesis Builder, High capability / high effort.
- **Scope:** proposed ADR-0052, its advisory index entry, and the evidence
  analysis that makes every ADR clause traceable. No production artifacts.
- **Stop conditions:** any unresolved conflict in the selected evidence;
  governance interpretation; an attempt to edit accepted ADR text (including
  ADR-0036 or ADR-0050) or published history; a new proposition, source
  family, evaluator feature, real data, production code, or owner
  ratification.
- **Full reads before acting:** this charter; `round-1-triage.md`; the topic
  `plan.md`; `it2/design.md` and `it2/examination.md` (the selected rival);
  `it1/design.md` and `it1/examination.md` (rejected incumbent, cited only
  for the Alternatives Considered section); `reviews/contract-adversary.md`;
  `reviews/expressiveness.md`; `repair1/design.md`; `repair1/examination.md`;
  `reviews/repair1-confirmation.md`; the milestone plan's Supported Source
  Class, Completeness Boundary, Contracts, Published-schema and migration
  posture, Fixtures, and Data Safety sections; ADR-0010, ADR-0011, ADR-0012,
  ADR-0014 through ADR-0017, ADR-0023, ADR-0027, ADR-0029, ADR-0032, ADR-0036,
  ADR-0038, ADR-0046, and ADR-0050; `docs/adr/INDEX.md`; and
  `PROJECT_PLANNING.md` sections "Prototype-Driven Decisions" and
  "Architecture Decision Records" (or their current equivalents).

## Assignment

Draft a plain-language Tier-2 (or Tier-3 if the evidence chain's
contract-foundational reach warrants it — state which and why) successor
contract from the selected evidence. Do not reopen the topology comparison
and do not copy the prototype's example identifiers (`demo.*`) into
normative contract names unless the evidence explicitly selects them as the
production shape.

The ADR must settle, citing the exact selected `it2`/`repair1` evidence for
each clause:

1. **Transaction source family and identity (P1).** The independent,
   anchor-keyed statement family and transaction member identity: the
   contributed broker-and-statement anchor fact, the transaction member
   keyed to it, correction/supersession behavior preserving logical
   transaction identity, multi-transaction and multi-broker sums, and the
   non-covered/adjustment-code/non-gain-only exclusion predicate — stated as
   a contributed/attested source-class assertion, never derived from
   proceeds minus basis.
2. **Completeness boundary (P2).** The nine direct authorities: the two
   `require_closed` reads (eligible long-term family, box-2a family) and the
   seven independently presence-checked absence declarations, with the
   adopted P2-S5A successor stating box-2a must be closed (not
   closed-empty), closed-empty contributing zero, and closed-nonempty
   contributing once via Schedule D line 13. State the presence-before-value
   discipline and exact missing/violated-component naming.
3. **Schedule D content (P3).** Line 8a columns (d)/(e)/(h), Part II line 15,
   Part III line 16, and the Schedule D required/not-required/incomplete
   disposition, as an ADR-0036 instantiation — content only, no new
   attachment ontology. Name the `attachment-rule.v2` threshold-only
   requirement-block gap (CA-05) as a production condition requiring an
   additive `attachment-rule.v3` (or equivalent) successor, not resolved by
   this ADR's evidence.
4. **Shared selected-preferential-base publication and line-16 successor
   (P3).** The `P` symbol, its two mutually exclusive producer signatures
   (direct, Schedule-D), the exact pin contract from the repair (P3-S8): the
   `COMMON16` set, the four-row ADR-0050 Decision 7 pin table rewritten in
   terms of `P` for the direct producer, and the empty pin addition for the
   Schedule-D producer. State explicitly that no route tag is added to `P`'s
   payload because the producer signature is recoverable from disjoint
   direct-pin lineage, and that generic exactly-one-producer mechanical
   enforcement (CA-06) is a named, separately tracked production condition,
   not resolved here.
5. **Line 7a, line 7b, and line 9.** Schedule D line 16 carried to line 7a
   exactly once; line 7b not affirmatively checked for this class; a
   versioned line-9 successor consuming the selected line-7a value exactly
   once regardless of which route produced it.
6. **Relationship to ADR-0036 and ADR-0050.** Both remain immutable history.
   State the exact named clauses this ADR supersedes only for the versioned
   successor graph (ADR-0050 Decision 5's line-7a source and Decision 7's
   line-16 pin table, rewritten in terms of `P`), and state that ADR-0036 is
   instantiated with content only, no ontology change.
7. **Pins, citations, presentation, and production kill tests.** The measured
   direct graph per producer signature; the exact 2025 Schedule D and Form
   1099-B citation pins; presentation of the Schedule D attachment, line 7a,
   and line 16 states under ADR-0046; and the kill-test set drawn from the
   eleven shared prototype cases (identity/closure lifecycle, each of the
   nine completeness components missing/violated, both-gain and
   Schedule-D-only routing, forward/reverse correction, double-count and
   reach-around rejection, non-covered exclusion).

Record: the rejected incumbent topology and why (CA-01/CA-03, corroborated
box-2a data loss); the two committee reviews and their one recorded dissent
(CA-04, resolved by the repair and independently confirmed); the one repair
cycle and its confirmation (`READY`); and the two named production
conditions carried forward as owed, not resolved (CA-05: categorical
attachment requirement schema; CA-06: exactly-one-producer generic
representation).

## Outputs

Create or modify exactly:

- `docs/prototypes/schedule-d-covered-ltcg-8a/evaluation-analysis.md`
- `docs/adr/0052-covered-long-term-gains-schedule-d-line-8a.md`
- `docs/adr/INDEX.md` (append one advisory row for ADR-0052; do not edit any
  other row)

The ADR status is **proposed** and inert. The index row must likewise say
`proposed` and provide only an advisory digest. `evaluation-analysis.md`
routes each adopted clause, rejected alternative, dissent/cost, production
condition, and unresolved non-blocking observation to the evidence chain
without retelling every case.

Do not modify a prototype exhibit, review, disposition, plan, phase state,
SEAT, accepted ADR, schema, manifest, content, fixture, test, production
file, or other documentation.

## Completion

Before writing, echo the selected contract boundary, evidence chain, three
outputs, proposed/inert status, and stop conditions.

Commit only the three outputs on the assigned branch and stop. Do not push,
merge, ratify the ADR, begin production, perform ADR review, or advance the
pointer. Return the commit SHA and a clause-to-evidence summary.

## Data safety

All examples and citations remain synthetic and publishable. No personal
values, identities, dispositions, refusal reasons, workspace locations,
documents, screenshots, or private artifacts may enter the contract unit.
