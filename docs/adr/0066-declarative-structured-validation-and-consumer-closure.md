# ADR 0066 — Declarative Structured Validation and Consumer Closure

- Status: **accepted** (ratified by the owner 2026-08-14)
- Tier: 2 — versioned source-family validation, cross-family identity,
  dependency synthesis, and fail-loud package/presentation boundaries that
  future content and consumers are written against.
- Date: 2026-08-14

## Context

The ratified engine implements Form 8949 code-W row checks and Form 1099-B
identity collision policy in tax-specific branches inside generic derivation
and package-validation modules. The same row policy is repeated in attachment,
line-rule, and finalize-unreached paths. A consumer can also omit a validation
dependency while still looking structurally complete.

The declarative-validation-substrate milestone compared two rival contracts.
Candidate B's family-attached shape converged after Synthesis Repair 2. The
evidence demonstrates a closed single-member predicate grammar, per-member
masking isolation, declared identity bindings, content-addressed correction and
removal, reachability-derived consumer prerequisites, package mutations,
late-member displacement, identical dispositions under both schedulers, and
real-projector disposition/cardinality models. The independent repair review
returned `READY FOR OWNER RATIFICATION DECISION`; its three documentation
findings were then independently closed.

The same evidence also exposed an existing boundary defect: a schema-valid
attachment successor unknown to `presentation_projection.py` is silently
filtered out, producing a valid model with no attachment. A corresponding
package member can be schema-valid yet inert when its schema is absent from the
validator's semantic dispatch. Adoption cannot precede a fail-loud boundary.

## Decision

1. **Structured-member constraints belong to versioned source-family
   content.** A source family may declare a separately identified and versioned
   constraint set. Each constraint has an id, a block code, an explanation
   meaning, and one predicate evaluated against exactly one current member.
   Generic code may not select behavior by Form 8949, Schedule D, Form 1099-B,
   box-1g, wash-sale, consumer id, or tax-name substring.

   The bounded Form 8949 migration declares four independently blockable
   meanings: `box-1g-flag-without-amount`,
   `box-1g-amount-without-flag`, `code-w-on-gain`, and
   `adjustment-exceeds-loss`. The latter two preserve ADR-0062 Decision 2's
   arithmetic meanings; every meaning is evaluated against one transaction,
   never against a netted subtotal.

2. **The predicate language is closed and bounded.** Its term forms are
   `field`, `literal`, binary `add`, binary `subtract`, and `floor_zero`. Its
   predicate forms are `field_present`, `field_absent`, `field_equals`,
   `field_not_equals`, `compare` with `gt/ge/lt/le/eq/ne`, `all`, and `any`.
   There is no `not`, binding, function definition, iteration, cross-member
   read, run-state read, parameter read, or symbol read. Resolver admission
   rejects predicate depth greater than six; JSON Schema is not claimed to
   enforce recursive depth by itself. An absent field is handled only by
   `field_absent` or an explicit term default: `field_not_equals` is false when
   the field is absent, and no global closed-world negation is inferred.

3. **Validation results are current, citable engine publications.** A member
   result is content-addressed over the member fact id, member-value pin, and
   semantic constraint-set version. A family validation publication depends on
   the current member-result set, family horizon, and closure authority. Member
   correction, removal, identity change, constraint-version change, or horizon
   succession displaces stale results. These publications are internal engine
   facts, not taxpayer-facing presentation rows.

4. **Cross-family identity is declared, not inferred.** Source-family content
   may declare mutually exclusive families and named identity components. Each
   component binds explicitly either to a named ADR-0011 fact-id bound key or
   to a member-field path. Generic code follows only those bindings and never
   parses a fact-type prefix or tax-name substring.

5. **Reachability creates validation dependencies.** For each constrained
   family reached by a consumer, resolution synthesizes that family's
   validation prerequisite. Consumer `accounts_for` declarations use the
   closed relationships `composes_line`, `itemizes_members`, and
   `reads_subtotal`; they record author intent and must exactly agree with the
   reachability-derived constrained-family set. They do not create or remove
   graph edges. Schedule D attachment inherits W validation when it reaches W
   proceeds; lines 1a/8a remain outside W dependencies.

6. **The production package boundary owns mechanical closure.** Every
   synthesized validation symbol has exactly one producer and every affected
   consumer has its synthesized edge. Production package validation rejects a
   missing or ambiguous producer, a removed synthesized edge, and missing or
   extra `accounts_for` declarations with named generic issues before a run can
   start. Both schedulers remain fail closed as defense in depth.

7. **Unknown semantic schema versions fail loudly.** A package member whose
   declared schema validates in the registry but is not supported by the
   package resolver's semantic dispatch is rejected with an issue naming the
   member and schema. Presentation projection rejects unknown form-field and
   attachment schema successors with an error naming the citizen and schema;
   it never filters them into an otherwise-valid incomplete model. This
   boundary ships before any schema successor adopted by this ADR.

8. **Domain completeness stays in migration acceptance.** Generic machinery
   does not know that a particular tax family must declare C1-C5. The bounded
   2025 migration must prove that all four row constraints, both ST/LT identity
   relationships with broker/statement/transaction/tax-year bound keys, and
   every measured family/consumer relationship exist. Each of the ten
   one-at-a-time removal mutants must fail. This is distinct from Decision 6's
   package closure over declarations that are present.

9. **ADR-0061 Decision 5 remains binding.** Its line-1a/8a non-confusion
   requirement and current kill-test remain an explicit residual. This ADR
   neither replaces that invariant nor authorizes deletion of its current
   implementation. A future accepted contract may supersede it separately.

10. **Publication is additive and post-ratification.** Candidate B's
    provisional discriminators reserve nothing. Before the first schema edit,
    the milestone selects new unused additive versions and records current
    intent in the schema-intent ledger. The source-family, rule/attachment, and
    package successor surfaces are an inseparable adoption set. Published
    predecessors remain byte-identical.

## Supersession and preservation

This ADR supersedes only the following implementation mechanisms while
preserving their product requirements:

- ADR-0061 Decision 2's literal identity-collision pair-table kill-test is
  replaced by declared `identity_exclusivity` and explicit component binding.
- ADR-0062 Decision 2's hard-coded generic-runner guard mechanism is replaced
  by declared structured-member constraints with the same two arithmetic
  meanings on the admitted corpus, plus the two independently contributable
  flag/amount consistency meanings required by ADR-0061 Decision 1.

ADR-0061's separate families, independent contribution, correction, and
completeness requirements remain binding. ADR-0062's attachment, arithmetic,
line composition, threshold, explanation, and presentation requirements remain
binding. Accepted ADR text is not edited in place.

## Consequences

- Tax policy moves from generic Python branches into versioned content while
  the evaluator and resolver remain domain-neutral.
- A bad package is rejected before scheduling instead of relying on eventual
  non-publication.
- Per-member findings preserve the exact defective transaction and prevent
  aggregate masking.
- Schema evolution costs an explicit dispatch update at both package and
  presentation boundaries; an unknown successor cannot disappear silently.
- The current Decision 5 substring check remains honestly visible until a
  separate contract replaces it.
- Prototype code is not adopted. Production is reimplemented against this ADR
  and focused tests.

## Alternatives considered

- **Candidate A validation citizens with authored `requires[]`.** Rejected:
  the expression shape remained schema-open and the parallel consumer list was
  incomplete, including Schedule D/subtotal paths.
- **Make generic code know mandatory Form 8949 declarations.** Rejected: that
  recreates tax-class policy in the resolver. Migration acceptance owns domain
  completeness.
- **Use `accounts_for` as the edge source.** Rejected: authoring declarations
  can be incomplete. Reachability derives edges; `accounts_for` checks intent.
- **Rely on scheduler failure for missing producers.** Rejected: fail-closed
  execution is defense in depth, not package validity.
- **Widen known-version lists without rejecting future unknown versions.**
  Rejected: it preserves the silent-drop hazard for the next successor.

## Links

- Plan:
  `docs/phases/engine-breadth/milestones/declarative-validation-substrate.md`
- Owner ratification:
  `docs/prototypes/declarative-validation-substrate/ratification-packet.md`
- Comparison and dissent:
  `docs/prototypes/declarative-validation-substrate/evaluation-analysis.md`
- Candidate B evidence:
  `docs/prototypes/declarative-validation-substrate/rival/README.md`
- Final reviews:
  `docs/prototypes/declarative-validation-substrate/reviews/synthesis-repair-2.md`
  and
  `docs/prototypes/declarative-validation-substrate/reviews/synthesis-repair-2-closure.md`
- Supersedes mechanisms in: ADR-0061 Decision 2 and ADR-0062 Decision 2
- Preserves and builds on: ADR-0003, ADR-0006, ADR-0010, ADR-0020, ADR-0023,
  ADR-0027, ADR-0028, ADR-0029, ADR-0033, ADR-0036, ADR-0046, ADR-0055,
  ADR-0056, ADR-0061, ADR-0062
