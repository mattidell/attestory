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
   identity keys of both lists are available, no present link row is unjoinable
   to the subject (below), **and both joined lists are empty**. The result pins the
   parameter. It pins no link, no reduction, and no source-family closure, and it
   does not claim that the set of links is complete.
2. **The sum of the matched reductions** — only when every joined link has
   **exactly one** matching reduction, every reduction matches a joined link, and
   every matched value is a number. The result pins every joined link and every
   joined reduction, and not the parameter.
3. **Block** — in every other case, and **none can fall through to the
   parameter**. An unbound scope, missing keys, an unjoinable present link type,
   an orphan reduction, duplicate link maps, a link with more than one reduction,
   a non-numeric reduction, and a link with no reduction block
   `DEPENDENCY_INVALID`. For an uncovered link, `missing` is exactly the uncovered
   links' finding ids, sorted, and those links are pinned; the other cases carry
   the identifiers the contract's section 3 table names. On the no-link path, an
   **absent parameter** blocks `DEPENDENCY_ABSENT` and a **version mismatch** blocks
   `DEPENDENCY_INVALID`, each with `missing` the parameter id (contract section 6).

**Joinability.** Link rows that are present but share no key name with the
subject cannot be joined to it. That is not "no link": it blocks
`DEPENDENCY_INVALID` with `missing` of `["link-coverage-unjoinable"]`, checked before
the no-link default. **This runtime check covers only present rows.** With no link row in the run, the dispatch cannot
tell a joinable type from an unjoinable one: `_scope` returns an empty list before
reading any key, the subject's keys may be absent, and a bare `fact-type.v2` link
declaration — the contract's admitted shape — is not on the run context, which
copies fact types only from bundles. So at zero rows **joinability is a property
of the binding, which G2 must establish statically**, not something a returned
parameter can show. Zero link rows with the subject's keys absent also takes the
parameter today, as the contract's section 3 specifies; that case is likewise G2's.

Ordinary `collect` and `count`, source families, and closure admission are
unchanged. An empty collection that was not declared closed still blocks. No
new record code: an uncovered link and the other failures share
`DEPENDENCY_INVALID`, and P4 decides from the durable reader whether a distinct
code is needed.

## Three layers, kept distinct

1. **Schema validity.** A `rule-artifact.v10` rule containing the node validates.
2. **Package acceptance.** An `artifact-package.v31` package containing it passes
   package validation — the section 2 shape checks; name confinement is dropped
   under the owner's choice of B (below).
3. **Executable per-subject binding.** The rule is evaluated by per-subject
   dispatch with the statement as the subject. **Nothing in rule content selects
   that, and production scheduling is open at G2.** Outside per-subject dispatch
   the operator blocks `link-coverage-scope-unbound`.

A package that is schema-valid and accepted has **not** established statement
coverage. Coverage is established only by a run in which the operator was
evaluated for the statement with its links joined — and a returned parameter is
evidence of coverage only where the link type was joinable to that statement.
G2 must prove or enforce that binding. The runtime check above refuses present
rows that cannot join, but cannot see an unjoinable type with no rows; so G2 needs
a static check, once its scheduler names a rule's subject type, that the link fact
type's identity keys include every identity key of the subject type — and the run
context must carry bare fact-type declarations for any runtime use of them.

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
- **B — change source admission so the names can be reused.** The link type is
  emitted as sources through a channel marshal does **not** consult when deciding
  scalar bindings, and confinement is dropped. What that buys, stated exactly:
  another rule may name the link type — in `requires`, a binding, a `ref`, or as
  the subject of its own per-subject dispatch — without the package being
  rejected, and no **other** symbol's scalar binding changes. That holds only if
  the coverage emission does **not** mark the emitted finding ids as used:
  marshal's legacy fallback skips used ids before anything else, so marking them
  would keep the scalar loss confinement was written to contain. What it does
  **not** buy: a sibling `collect` returns the link values as decimals (or blocks on a
  non-number), not their key maps, so a consumer that needs the canonical links
  reads them per subject — by per-subject or pairing dispatch — not by `collect`;
  and a plain `ref` of the link type outside dispatch binds a run-wide scalar only
  through the legacy fallback, when the current link values agree — the
  behaviour before registration, not a per-statement read. `count` and
  `collect_categorical_all_equal` would see the rows too, and a sibling that
  collects the type pins every row it read, across statements — its own read,
  not the operator's.

**The owner chose B (2026-09-24).** This ADR is a general grammar contract, and A
would have ratified a restriction whose only reason is an implementation shortcut.
B's benefit is the narrower one stated above — the names become usable, not
readable by `collect` as canonical links; an earlier draft overstated it.
The admission change, the contract amendment and the removal of
`LINK_COVERAGE_NAME_REUSED` follow as a bounded track; this record stays
`proposed` until that change and this wording are independently reviewed.

## Consequences

- `rule-artifact.v10` and `artifact-package.v31` are published schemas on the
  milestone branch (checksums appended); any change to v10's shape is a new
  version. The joinability check and either confinement choice need no schema
  change.
- **Changes to the accepted contract and the built code this ADR requires**, none
  made in this edit:
  1. **Present-but-unjoinable link rows must block.** Today `_scope` returns `[]`
     when link rows share no key name with the subject, and the arm then returns
     the parameter **if the reductions slot is also empty** (a joined reduction is
     reported as an orphan first). `subject_dispatch.evaluate_subject_scoped_rule`,
     where it fills the coverage slot, must block instead with
     `["link-coverage-unjoinable"]`; `_scope` itself is unchanged, so joins for
     rules without the operator stay as they are. Contract passages amended: the
     section 3 table (a new row before the default), section 5 "No current link",
     and section 8 item 3, plus an obligation for present unjoinable rows.
  2. **Option B.** `marshal.marshal_run_context` gains an emission-only name set,
     default empty: emission walks it with the existing set; the input-binding
     branch and the legacy fallback keep consulting only the existing set; and
     findings emitted only because of the new set are **not** added to the used
     ids. Forwarded through `marshal.marshal_live_run_context` and `live.live_run`
     (optional, default empty); `live._resolved_run_material` returns the link type
     in that set instead of `collect_names`; `live.live_coordinate_run` passes it;
     `package_validation._link_coverage_issues` drops the confinement walk and
     `LINK_COVERAGE_NAME_REUSED`, keeping the shape checks. Contract passages
     amended: section 1.1 (admission); section 2 (confinement, and its four effect
     bullets); section 5 "Undeclared empty collection"; section 7's first two
     bullets; section 8 items 14 and 17; section 9's Gate 1 blast-radius sentence
     and its prescribed decision paragraph.
  3. **The reduction name is not registered at all.** Reductions are derived and
     never marshalled, and their same-run sources reach `run.sources` regardless of
     that list; nothing depends on the registration. (Dropping registration does not
     by itself drop confinement — the rows are in `run.sources` either way; B drops
     confinement.)
- Zero-row joinability is **not** closed by any of these; it is G2's.
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
- ~~Confinement A or B~~ — decided: **B** (owner, 2026-09-24).

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
