# Downstream, and Premature: Representation Reconnaissance

## What this document is, and what it is not

> **This is reconnaissance, not design.** It is the furthest-downstream
> document in the milestone and the least authoritative. It was written before
> the architecture upstream of it was settled, and it is retained because the
> legibility test it applies is durable evidence — not because the shapes it
> compares are the right shapes.

Read it as a record of what was looked at. Do not read it as a menu.

**No representation may be selected from this milestone.** Choosing a citizen
kind, a schema, a field shape, or a contract requires the conceptual
architecture and the authority policy to be settled first, and neither is. A
representation chosen now would encode whichever open question it happened to
resolve by accident.

With that stated: an evaluation of whether the engine's existing structure can
declare a derived tax concept, tested against one worked concept
(`tax.us.2025.interest.taxable-total`), and a comparison of two conceptual
alternatives.

This document selects nothing. It proposes no schema, no bytes, no field
names, no version numbers, and no implementation. It identifies what each
shape buys, what it duplicates, and what it risks, and it lists the contract
questions that would have to be answered before either could be ratified.

Concept semantics: [taxable-interest-concept.md](taxable-interest-concept.md).
Evidence for the current-state claims:
[current-engine-assessment.md](current-engine-assessment.md).

## The test

Can a reader — with no private convention, no access to project history, and
no ability to read Python — recover the following from committed content?

| # | Question | Recoverable today? |
| --- | --- | --- |
| 1 | What does the result mean? | **No** |
| 2 | Who is its subject, and what is its identity? | Partially — scope only |
| 3 | What jurisdiction and tax year? | Yes |
| 4 | What quantity and unit? | Partially — a quantity id, with no unit or direction |
| 5 | What is its authority basis? | **No** |
| 6 | What is its modeled universe? | Partially — recoverable by reading the rule body, declared by no composition |
| 7 | What are its exclusions and known unsupported categories? | **No** |
| 8 | Which rule derives it? | Yes |
| 9 | What are its presentation bindings? | Yes |
| 10 | Is it eligible for an official form line? | **No** |

**Three clear passes** (3, 8, 9), **three partials** (2, 4, 6), and **four
clear failures** (1, 5, 7, 10). The passes are what the *derivation* machinery
needs in order to run. The failures are what a *reader* needs in order to
trust the result.

Question 4 is graded partial rather than failed because
`tax.us.2025.quantity.taxable-interest` does exist and is referenced by the
fact types: a reader can recover *that the amounts are commensurable* and
which pool they belong to. What they cannot recover is a unit or a direction,
because the quantity vocabulary is a list of bare strings — which is why
signed constituents have nowhere to express themselves.

The split between what execution needs and what a reader needs is the finding,
and question 6 is its clearest instance: the universe is present in content but
only as an operational detail of the rule that consumes it, never as a
declaration a reader could rely on.

## Evaluation of the current distributed declaration

The concept is currently declared, to the extent it is declared at all,
across seven places.

### Output symbol — `tax.us.2025.interest.taxable-total`

A string. It appears in the rule's `publishes`, the form field's
`binds_symbol`, the Schedule B tie-out's `line_symbol`, and the package's
`composition_obligations`. It has no declaration of its own: there is no
artifact whose subject is this symbol.

The name asserts more than the model supports. "Taxable total" reads as the
exhaustive concept; the thing it names is a bounded ten-slot arithmetic.

### Rule artifact — `rule.form1040-line2b.v4`

Carries `publishes`, `requires`, `value`, `when`, `blocked`, `pins`,
`citations`, `composition`, `scope`, and a free-text `notes`.

This is where most real information lives, and it is well-formed for
execution. But its subject is *how to compute*, not *what is computed*. The
`notes` field carries the only prose account of the model's boundary, and
notes are not a contract.

### Rule scope

`{family: individual-income-tax, jurisdiction: US-federal, tax_year: 2025}`.
Correct, and genuinely useful — this is the one place the concept's
jurisdiction and year are structurally declared. It does not identify the
subject (the taxpayer), which is supplied by the workspace at run time.

### Quantity vocabulary — `quantity.taxable-interest` v1

```
{"quantities": ["taxable-interest", "wages"]}
```

A list of two bare strings. No unit, no currency, no dimension, no
definition, no jurisdiction, no year. It groups `wages` with
`taxable-interest` in one citizen, so the artifact's own name does not
describe its contents.

Critically, the same quantity types both the seven inclusions and the three
subtractive adjustments. A quantity that cannot distinguish an addition from
a subtraction is not carrying semantics; it is carrying a de-duplication key.
Its real function in the engine is to trigger the "aggregates multiple inputs
of the same quantity" check that forces a composition obligation to be
declared — a structural role, not a semantic one.

### Composition — `interest-composition.v4`

Declares seven slots, `coextensiveness: "slot-bijection"`, `publishes:
"tax.us.2025.interest.positive-total"`, and a `required_universe.claim`.

Two observations.

**It is honest and it is about a different symbol.** Its claim — "Seven
declared positive taxable-interest families forming the gross Schedule B Part
I line-1 basis, without subtractive adjustments" — is accurate, and it
describes `positive-total`, not `taxable-total`. The concept under
examination has no composition of its own.

**`required_universe.claim` is unread prose.**
`packages/schemas/derivation/taxable-interest-composition.v1.schema.json`
requires it as a non-empty string with no further constraint. No code reads
it; the only occurrences outside content are in the generator tools that
write it. It is the project's existing example of an honesty gate implemented
as a caption, and it is the cautionary case for any new shape.

### Citations

`citation.form1040.line-2b` v1 resolves to `{family: irs-instructions,
form_id: 1040, tax_year: 2025}`. The `irs-instructions` authority variant in
`packages/schemas/derivation/citation.v1.schema.json` has no locator field, so
the citation names an entire instruction document. The `us-code` variant
exists in the schema and is used by none of the 74 citation citizens in
`packages/content/tax/2025/`.

A concept declaration that cited this citation would inherit its
imprecision. Any shape chosen below is capped by the citation vocabulary.

### Form-field binding — `form1040.line-2b` v5

`packages/schemas/tax/form-field.v3.schema.json` describes itself as
"Presentation-only." The field carries the accurate narrowing in a free-text
`description`, and a `dispositions` block that is genuinely expressive —
`blocked`, `guard_inapplicable`, `closure_backed_zero`, `computed_zero`,
`published_value`, each with its own `explain` and `render`.

The dispositions block is the strongest existing precedent for "occupy a form
line conditionally and explain why," and any shape should preserve it.

### Derived-finding provenance

The rule pins every input subtotal and every closure read, so a finding
carries its derivation edges. Provenance of *computation* is good. Provenance
of *meaning* is absent: nothing in the finding says what the number is a
number of.

### Summary of the current shape

The distributed declaration is adequate for execution and inadequate for
trust.

The modeled universe *is* in content, and this must be stated precisely
because it is easy to get wrong. `rule.form1040-line2b.v4` names all ten slots
four times over — in its input `pins`, its `requires`, its `value` refs, and
its `when.require_closed` branches — and Schedule B's `tie_out` repeats the
surface. What is missing is not the information but its *owner*: no
composition citizen declares the universe of the published symbol, so the
universe is recoverable only from the artifact that computes the result and
from an attachment that is produced conditionally. A reader who wants to know
what `taxable-total` covers must reverse-engineer a rule body.

The known-unsupported categories are the genuinely absent half. Nothing in
content records that the § 135 education exclusion, Form 1099-OID boxes 2 and
8, § 454 previously-reported interest, or seller-financed mortgage interest
are materially relevant and unmodelled. That information exists only in
documentation.

## Shape A — Strengthen the existing distributed declaration

Keep the current artifact kinds. Make the missing information declarable
within them.

The essential moves would be: give the composition the ability to express
subtractive constituents so that `taxable-total` can have a composition of
its own rather than borrowing one that publishes a different symbol; give
`required_universe` a machine-readable structure and an actual consumer;
enrich the quantity vocabulary so a quantity carries a unit and a direction;
and add a locator to the citation authority families.

### What it buys

- **No new citizen kind.** The shape works within the existing artifact kinds:
  nothing here requires inventing a new one, and the package membership and
  reachability rules keep operating on the same kinds of citizen they operate
  on now. This is a statement about the *kinds*, not a claim that no consumer
  or validator changes — adding structured semantics and giving
  `required_universe` an actual consumer necessarily changes validation
  behaviour somewhere. What that costs was not measured here and should not
  be assumed small.
- **It removes the validator exemption at its root.** If a composition can
  express a subtractive slot, `_V11_ADJUSTMENT_SLOTS` and the named-artifact
  gate at `packages/derivation/package_validation.py:1168-1188` and
  `:1213-1216` become unnecessary. The general contract in ADR-0026 decision
  2 — exact bijection, no extras — is restored rather than exempted, and the
  brittleness of a route granted to one literal artifact identity goes with
  it.
- **It gives the universe an owner.** The ten-slot surface gains a composition
  citizen that declares it, so the universe stops being something a reader
  infers from a rule body and stops being duplicated in a Schedule B `tie_out`
  that is produced only when Schedule B is required. The duplication becomes a
  check against a declaration rather than a second source of truth.
- **The moves are separable in principle.** A composition able to express
  subtraction is worth having even if the quantity and citation changes never
  happen. Whether they are separately *shippable* depends on how the existing
  validators respond to each move in isolation, which this document did not
  establish and does not assert.

### What it duplicates

- **Scope, three times over.** Rule scope, composition scope, and form scope
  would all continue to assert jurisdiction and tax year, with nothing
  declaring which is authoritative.
- **Boundary prose in at least three places.** Family `closure_claim`s,
  `required_universe.claim`, and the form field `description` all describe the
  concept's edges in overlapping, independently-authored English. They are
  already inconsistent: `family.non-form-interest.json`'s closure claim says
  "without a Form 1099-INT statement instance" while its own fact type says
  "without a Form 1099-INT/OID statement instance."

### What it risks

- **The concept still has no home.** Strengthening the parts does not create
  a thing whose subject is the concept. Questions 1, 5, 7, and 10 of the test
  above — meaning, authority basis, known-unsupported categories,
  official-line eligibility — have no natural owner among the existing kinds.
  Composition is about constituents; rule is about computation; form field is
  presentation-only by its own declaration.
- **Known-unsupported categories have no plausible location.** This is the
  sharpest limitation. A composition declares what it *includes*. There is no
  existing citizen whose job is to record "the Series EE/I education
  exclusion is materially relevant, is not modelled, and would change this
  result." Under Shape A that information stays in documentation, which is
  exactly where it is now.
- **Prose gates recur.** Making `required_universe` structured without giving
  it a consumer reproduces the current failure in a new syntax.

## Shape B — A first-class derived-tax-concept declaration

Introduce a citizen whose subject is the tax concept itself. Rules publish
*into* it; form fields bind *to* it; the concept declares its own meaning,
authority basis, modeled universe, exclusions, known gaps, and official-line
eligibility.

### What it buys

- **A subject for the questions that currently have no owner.** Meaning,
  authority basis, known-unsupported categories, and official-line
  eligibility get a declared home. This is the only substantive advantage,
  and it is the one that matters: it is the difference between a model that
  can state its own bound and one that can only be described as bounded by a
  document alongside it.
- **Machine-readable eligibility.** Whether a bounded result may occupy an
  official line becomes a declared, checkable property rather than a judgment
  a reader makes from prose. A form field could be validated against the
  concept's eligibility instead of trusting its own caption.
- **The bound travels with the symbol.** Every downstream consumer of
  `taxable-total` could reach the concept, so the narrowing survives one
  derivation hop. This directly addresses the strongest argument in the
  official-line-binding debate — that a field description constrains no
  consumer.
- **One authoritative scope.** Jurisdiction, tax year, regime, and subject
  are declared once, and rule and form scope become checks against it rather
  than independent assertions.
- **Bounded-claim presentation becomes principled.** The claim ladder in
  [taxable-interest-concept.md](taxable-interest-concept.md) becomes
  expressible: a concept that declares itself level-3-supported can be
  rendered as such everywhere it appears, without each surface re-deciding.

### What it duplicates

- **Scope and citations, unless the existing carriers give them up.** If rule
  scope, composition scope, and form scope all persist alongside a concept
  scope, the shape has added a fourth assertion of the same facts and made
  the authority question worse rather than better.
- **Universe declaration, against composition.** A composition already
  declares constituents. If a concept also declares a universe, the two must
  be reconciled — and if they are reconciled by requiring exact agreement,
  the concept's universe is derived and arguably redundant.

### What it risks

- **A new citizen kind is a large contract.** It needs identity, versioning,
  supersession, currency, package membership, adoption, reachability, and
  marshalling — every obligation the existing kinds carry. That is a
  substantial ratification, not a schema addition.
- **It can become a second place to be wrong.** A concept declaring "modeled
  universe: seven positive families and three adjustments" is a claim that
  must be kept true as content changes. Without a validator binding it to the
  actual composition, it becomes a third unread prose gate — the failure mode
  of `required_universe.claim`, reproduced at higher cost.
- **Known-unsupported categories are unbounded by nature.** A field for
  "categories materially relevant but not modelled" invites an ever-growing
  list that no validator can check for completeness, and whose emptiness
  proves nothing. The absence of a counterexample is not evidence of
  coverage. Whatever this field means, it must not be readable as "everything
  not listed here is covered."
- **It may be the right answer at the wrong time.** The engine has one worked
  derived concept. Generalising from one instance is how the current
  distributed shape came to fit line 2b and nothing else.

## Information both shapes must preserve

Whatever is chosen, the following must survive, because each is load-bearing
today:

1. **Slot bijection as a validated property**, not a documented intention.
   The mechanism works; the objection is only to its named-artifact
   exemption.
2. **The distinction between internal coextensiveness and external
   sufficiency.** They must remain separately declarable and separately
   checkable. Collapsing them is the defect this milestone exists to name.
3. **Per-constituent closure reads and their pins.** Constituent-scoped
   blocking is what keeps the bottom-left quadrant of the support matrix
   non-empty.
4. **The `dispositions` vocabulary.** `blocked`, `guard_inapplicable`,
   `closure_backed_zero`, `computed_zero`, and `published_value` are a real
   and useful distinction set, and `guard_inapplicable` in particular is
   working precedent for conditional non-occupation of a form line.
5. **Statement identity independent of evidence.** The statement-backed
   interest fact types are keyed on a *logical statement* alongside the payer
   and tax year — `payer`/`statement`/`tax-year` for the Form 1099-INT and
   1099-OID types, `partnership`/`k1-statement`/`tax-year` for the K-1 type —
   with no file, upload, scan, document, or evidence key anywhere. That
   property is correct and must not be weakened.

   It is a bounded property, not a universal one, and the exceptions are the
   fact types that have no statement to be backed by: `non-form-interest` is
   keyed `payer`/`tax-year` (see A14, where that under-specification collapses
   two arrangements into one), and the three Schedule B adjustment types are
   keyed `tax-year`/`adjustment-instance` (see A13, where the absence of a link
   to the adjusted statement is the defect). Both exceptions are places where
   identity is *too weak*, which is the opposite failure from evidence leaking
   into identity.
6. **The tax-exempt routing.** The distinct `quantity.tax-exempt-interest`
   typing and the box-9 hard block keep Form 1099-INT box 8 structurally out
   of line 2b. That structural separation is what was verified, and it is
   worth preserving. It is not a finding that the tax-exempt boundary is
   substantively correct: § 103 was not read, so which amounts *belong* on
   that side of the line remains unassessed here.
7. **Honest self-description where it already exists.** The market-discount
   families' closure claims and `interest-composition.v4`'s
   `required_universe.claim` are accurate. The problem is that nothing reads
   them, not that they are wrong.

## Contract questions requiring later ratification

Neither shape can be adopted without answering these. They are listed as
questions, not proposals.

1. **Is a derived tax concept a citizen?** If yes, what are its identity
   keys, its versioning and supersession policy, its currency semantics, and
   its package-membership and adoption obligations?
2. **Can a composition express a subtractive constituent?** If yes, does
   `coextensiveness: slot-bijection` still mean bijection over a flat slot
   set, or over a signed one? If no, what licenses a rule to consume inputs
   its composition does not declare?
3. **What reads `required_universe.claim`, or its successor?** A gate with no
   consumer is a caption. If the answer is "a human reviewer," that should be
   stated as the contract rather than implied by structure.
4. **Does a quantity carry a unit and a direction?** The present vocabulary
   carries neither, and types inclusions and reductions identically.
5. **Must a tax claim cite controlling law?** The `us-code` authority family
   exists and is unused. If the answer is yes, essentially every existing
   citation is incomplete; if no, the product should say plainly what its
   citations are for.
6. **Can a citation name a line or section?** The `irs-instructions` variant
   cannot. Adding a locator is a vocabulary change with corpus-wide
   consequences.
7. **Which artifact kind carries the § 135 exclusion?** § 135(a) operates on
   includibility in gross income, so the exclusion is part of the taxable-
   interest concept and not an artefact of Schedule B; that much is settled by
   statute rather than by this project. What is genuinely open is the
   structure that implements it — a signed constituent of a composition, a
   separate rule the concept consumes, or a declared adjustment class — and
   whether a pre-exclusion intermediate is also modelled. The § 454
   previously-reported amount raises the identical structural question.
8. **What is the subject of a derived tax concept on a joint return?**
9. **How does a declared "known unsupported category" avoid being read as a
   completeness claim about everything omitted from it?**
10. **Do rule scope, composition scope, and form scope become checks against
    a single authoritative scope, or do they remain independent assertions?**

## A note on sequencing

These two shapes are not exclusive, and the comparison above suggests they
are not really alternatives. Shape A's moves — a composition that can express
subtraction, a quantity that carries a unit and a direction, a citation that
can name a line — are prerequisites for Shape B being able to say anything
precise. Shape B without them would declare a concept whose universe it
cannot check, whose amounts it cannot type, and whose authority it cannot
locate.

The genuine decision is therefore narrower than "A or B": it is whether the
distributed shape is the destination or the foundation. That question is put
to the owner as D3 in
[current-engine-assessment.md](current-engine-assessment.md).
