# ADR 0075 — Link coverage on the rule artifact

- Status: **proposed**. Written for Track 3 stage B1; repaired 2026-09-23 on
  the owner's review. `PROJECT_PLANNING.md` "Decision Records" binds only
  `accepted`, so this record does not bind until the owner accepts it, and
  the owner's choice below is taken first.
- Tier: 2 — a rule-language operation and the runner behaviour later rules are
  written against. Not a product-thesis or governance-meaning decision.
- Date: 2026-09-23

## Context

A Form 1098-E statement reports one amount. Recorded links connect that
statement to borrowings, and each link may carry a reduction derived earlier in
the same run. The P3 probes showed an engine that could not tell three
situations apart: nothing linked; every link resolved to a reduction; a link
recorded whose reduction never resolved. It read the third as the first, and
published a figure with the unresolved link missing from its dependency chain.

The evidence is the P3 measurements in
`tests/test_sli_circumstance_association_a4_pass2.py`
(`ObservedMechanismLimits`, and `UnresolvedLinkBlocksTheStatement`, formerly
`ObservedUnresolvedLinkDefect`) and the accepted contract
`docs/phases/tax-concept-derivation/milestones/student-loan-circumstance-association-evidence/track3-coverage-contract.md`.
Gate 1 on the contract scores 2, 1, 1, 0, total 4: paper plus this ADR, not a
prototype.

## Decision

**`link_coverage` is an operator over one bound subject.** It is an expression
alternative in `rule-artifact.v10`. It names a link fact type, a reduction
symbol, and a parameter pin, and it returns **a reduction total** — one decimal
— or blocks. What a rule does with that total is the rule's own expression; the
worked example subtracts it from a statement's box 1, but that subtraction is
not the operator's meaning.

It is evaluated for one subject at a time, over two lists the per-subject
dispatch supplies for that subject: the **joined current links for this subject**
and the **joined reductions for this subject**. A link and a reduction match
when the name-to-value maps of their structured keys are equal. Rendered fact
ids and symbols are never compared.

It returns exactly one of three results, and falls through to none of them:

1. **The declared parameter** — only when the subject's scope is bound, the
   identity keys of both lists are available, the link fact type is joinable to
   the subject (below), **and both joined lists are empty**. The result pins the
   parameter. It pins no link, no reduction, and no source-family closure, and it
   does not claim that the set of links is complete.
2. **The sum of the matched reductions** — only when every joined link has
   **exactly one** matching reduction, every reduction matches a joined link, and
   every matched value is a number. The result pins every joined link and every
   joined reduction, and not the parameter.
3. **Block `DEPENDENCY_INVALID`** — in every other case. An unbound scope, missing
   keys, an orphan reduction, duplicate link maps, a link with more than one
   reduction, a non-numeric reduction, and a link with no reduction all block;
   **none of them can fall through to the parameter**. For an uncovered link,
   `missing` is exactly the uncovered links' finding ids, sorted, and those links
   are pinned; the other cases carry the identifiers the contract's section 3
   table names.

**Joinability.** A link fact type whose declared identity keys share no key name
with the subject cannot be joined to it. That is not "no link": it blocks. The
check reads the declared fact type, so it holds when no link row exists.

Ordinary `collect` and `count`, source families, and closure admission are
unchanged. An empty collection that was not declared closed still blocks. No
new record code: an uncovered link and the other failures share
`DEPENDENCY_INVALID`, and P4 decides from the durable reader whether a distinct
code is needed.

## Three layers, kept distinct

1. **Schema validity.** A `rule-artifact.v10` rule containing the node validates.
2. **Package acceptance.** An `artifact-package.v31` package containing it passes
   package validation (section "Name confinement" below applies here).
3. **Executable per-subject binding.** The rule is evaluated by per-subject
   dispatch with the statement as the subject. **Nothing in rule content selects
   that, and production scheduling is open at G2.** Outside per-subject dispatch
   the operator blocks `link-coverage-scope-unbound`.

A package that is schema-valid and accepted has **not** established statement
coverage. Coverage is established only by a run in which the operator was
evaluated for the statement with its links joined — and a returned parameter is
evidence of coverage only where the link type was joinable to that statement.
G2 must prove or enforce that binding. Two candidate means, neither selected
here: the runtime joinability check above, which refuses an unjoinable link
type; and, when G2's scheduler names a rule's subject type, a static check that
the link fact type's identity keys include the subject type's.

## Name confinement — a cost, and the owner's choice

To load the link facts as sources, the implementation registers the operator's
`links` name on the collect list marshal shares with every rule. That list also
decides which fact types marshal will **not** bind as a scalar, so registering a
name silently changes any other rule that reads it. Stage B1 contained that side
effect by **package validation**: in a v31 package using the operator, no other
rule may name the link or reduction string at all
(`LINK_COVERAGE_NAME_REUSED`), except the reduction rule's `ref` of the link.

**That restriction is not a tax requirement, and it is not free.** In such a
package, a rule that legitimately needs the canonical statement-to-borrowing
links — for example, a later per-loan legal-obligation consumer — cannot read
them. The restriction exists only to contain a side effect of how names are
admitted.

The owner chooses between:

- **A — keep confinement as an explicit, bounded v10 limitation.** Nothing more
  to build now. Consequence: the first consumer that needs to read the link facts
  in the same package forces a change of admission then, and an amendment to this
  ADR. The restriction lives in validation code, not in the published schema, so
  it can be lifted without a schema version.
- **B — change source admission so the facts are reusable.** The operator's names
  are admitted as sources through a channel marshal does **not** consult when
  deciding scalar bindings, so no other rule's binding changes and confinement is
  dropped. Consequence: a signature change to `marshal_run_context` and to
  `live._resolved_run_material`, a contract amendment, and tests re-cut. A rule that
  `collect`s the link type would then see its rows, which is what a reader of
  those facts needs.

**Foreman's recommendation: B**, because this ADR is a general grammar contract and
A ratifies a restriction whose only reason is an implementation shortcut. A is
acceptable if the owner prefers to defer the admission change until a consumer
exists.

## Consequences

- `rule-artifact.v10` and `artifact-package.v31` are published schemas on the
  milestone branch (checksums appended); any change to v10's shape is a new
  version. The joinability check and either confinement choice need no schema
  change.
- The Decision above requires one change to the accepted contract and the built
  runtime: an **unjoinable** link type currently installs an empty list and takes
  the parameter, because `subject_dispatch._scope` returns `[]` when no key names
  are shared. That must block. This is recorded as a required follow-up, not made
  in this ADR edit.
- Registering the **reduction** name on the collect list appears unnecessary:
  reductions are derived, never marshalled, and their same-run sources are
  appended regardless of that list. If so, its registration — and its
  confinement — can be dropped under either choice. To be confirmed by test
  before the contract is amended.
- `records.CURRENT_RECORD_SCHEMA` stays `"derivation-record.v9"`.

## Alternatives considered

The contract's section 1 compared four homes against the same measurements. A
field on the rule needs the same schema successor and splits the total from the
expression that uses it. A binding mode cannot name one link's finding id, and a
default on an empty reduction symbol does not run when one of two reductions
published. A separate citizen adds a declaration no second rule was shown to
need. The operator is selected.

## Not decided

- Whether an uncovered link needs its own record code (P4).
- How a production run schedules rules onto per-subject dispatch, and how G2
  proves the statement binding (G2).
- Confinement A or B (the owner's choice above).

## Links

- Contract:
  `docs/phases/tax-concept-derivation/milestones/student-loan-circumstance-association-evidence/track3-coverage-contract.md`
- Evidence: `tests/test_sli_circumstance_association_a4_pass2.py`,
  `tests/derivation/test_link_coverage_contract.py`,
  `tests/derivation/test_link_coverage_runtime.py`
- Schemas: `packages/schemas/derivation/rule-artifact.v10.schema.json`,
  `packages/schemas/derivation/artifact-package.v31.schema.json`
- Same class of decision: ADR-0064 (`multiply` / `divide`), ADR-0074
  (`bound_sources`). General grammar, not an id gate.
