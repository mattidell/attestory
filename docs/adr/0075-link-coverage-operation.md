# ADR 0075 — Link coverage on the rule artifact

- Status: **proposed** (written for Track 3 stage B1 and reviewed with it;
  `PROJECT_PLANNING.md` "Decision Records" binds only `accepted`, so this
  record does not bind until the owner accepts it.)
- Tier: 2 — a rule-language schema and the runner behaviour later rules are
  written against. Not a product-thesis or governance-meaning decision.
- Date: 2026-09-23

## Context

A Form 1098-E statement has a box 1 amount. A recorded link says that
statement is connected to a borrowing. Each current link is supposed to
contribute its own numeric reduction, published earlier in the same run and
pinned to that link. The statement's reported amount is box 1 minus those
reductions.

Three outcomes are different, and the probes showed the engine treating two
of them as the same. Nothing was linked: the amount is box 1 minus a
declared parameter, and that default does not claim the set of links is
complete. Every current link has its own numeric reduction: publish box 1
minus those reductions, and pin every reduction and every link. A link is
recorded and its reduction never became a number: that statement blocks, the
block names that link, and the missing reduction is not zero. Another
statement in the same run is left alone.

An ordinary collection that is empty and was not declared closed still
blocks. This decision does not give that collection a default.

The evidence is the P3 measurements in
`tests/test_sli_circumstance_association_a4_pass2.py`
(`ObservedUnresolvedLinkDefect`, `ObservedMechanismLimits`) and the accepted
contract
`docs/phases/tax-concept-derivation/milestones/student-loan-circumstance-association-evidence/track3-coverage-contract.md`
(reviewed at `df1abb02`; the review disposition is in that document). Gate 1
on the contract scores 2, 1, 1, 0, total 4: paper plus this ADR, not a
prototype. Tier 2 status does not raise the evidence rung.

## Decision

A statement amount subtracts, from box 1, the reduction total declared by the `link_coverage` operation on `rule-artifact.v10`; earlier rule schemas stay as published. The operation matches each current link to its reduction by equality of the structured key tuples those sources already carry, never by a rendered fact id. No current link produces box 1 minus the value of a named parameter, and that publication pins the parameter and not a source-family closure. Every current link with exactly one numeric reduction produces box 1 minus the sum of those reductions, and the publication pins each of those reductions and each of those links. Any current link without that reduction blocks `DEPENDENCY_INVALID`, and the disposition's missing list is those links' finding ids. That code does not distinguish an uncovered link from an orphan reduction, a duplicate link map, or a non-numeric reduction on the same subject; a distinct code, if the durable reader needs one, is a later charter and not this decision. Ordinary `collect` and `count` arms, source families, and closure admission are unchanged, and an empty collection that was not declared closed still blocks. Package validation accepts the operation only when no other member names the link or reduction string, except the reduction rule, which publishes the reduction and reads the link by `ref` as its per-subject subject. Any other such use is `LINK_COVERAGE_NAME_REUSED`. `marshal_run_context` does not change. How a production run schedules either rule onto per-subject dispatch is not this decision. It is open for G2.

## Consequences

- `rule-artifact.v10` and `artifact-package.v31` are new published schemas.
  `rule-artifact.v1` through `v9` and `artifact-package.v1` through `v30`
  stay as published. v10 is the ordinary guarded clause: `value` is required,
  and `selection` and `aggregation` are not properties. `citations`,
  `composition`, and `notes` stay optional, as on v9's value branch.
- There is no `derivation-record.v10` and no `LINK_UNCOVERED` code. An
  uncovered link blocks `DEPENDENCY_INVALID`. `missing` is exactly those
  links' finding ids, sorted. `records.CURRENT_RECORD_SCHEMA` stays
  `"derivation-record.v9"`. The same code, with finding ids in `missing`,
  is also what an orphan reduction, a duplicate link map, and a non-numeric
  reduction use. P4 decides, from what a durable reader sees, whether a
  distinct code is needed. If it is, the record bump is chartered then.
- Package validation rejects a node in `when`, a node that is not exactly
  once in `value`, identical `links` and `reductions` strings, a `links`
  string that is not a package fact type, a `reductions` string that is not
  one other rule's `publishes`, and an `empty.parameter` pin that is not an
  exact parameter member. The contract requires those rejections and does
  not name their code. This implementation uses `LINK_COVERAGE_INVALID`.
  That label is not part of the decision paragraph.
- `live._resolved_run_material` registers each node's `links` and
  `reductions` as collect names. That registration is not a source-family
  edge and not a closure read. `marshal_run_context` does not change, so a
  sibling fact type's scalar binding stays on today's branch.
- The evaluator, the per-subject slot, and the sentinel are not this
  record's implementation. They are stage B2.

## Alternatives considered

The contract's section 1 compared four homes against the same measurements.
A field on the rule needs the same new schema and the same admission lists,
and it splits the reduction total from the expression that subtracts it.
A new binding mode cannot name one link's finding id, and a default on an
empty reduction symbol does not run when one of two reductions published.
A separate content citizen adds an adopted declaration no second rule was
shown to need. None of those homes is selected.

## Not decided

- Whether a distinct disposition code is required. P4 decides that from the
  durable reader. This ADR does not open `derivation-record.v10`.
- How a production run schedules the reduction rule or the coverage rule
  onto per-subject dispatch. Nothing in the rule selects that dispatch.
  Ordinary `attempt` does not perform the per-subject outcomes. The limit
  is open for G2.

## Links

- Contract:
  `docs/phases/tax-concept-derivation/milestones/student-loan-circumstance-association-evidence/track3-coverage-contract.md`
- P3 evidence: `tests/test_sli_circumstance_association_a4_pass2.py`
- Schemas: `packages/schemas/derivation/rule-artifact.v10.schema.json`,
  `packages/schemas/derivation/artifact-package.v31.schema.json`
- Same class of decision: ADR-0064 (`multiply` / `divide`), ADR-0074
  (`bound_sources`). This operation is general grammar. It is not an id gate.
