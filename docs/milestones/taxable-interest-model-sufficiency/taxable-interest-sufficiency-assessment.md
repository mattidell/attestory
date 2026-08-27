# Tax-Model Sufficiency Assessment: `tax.us.2025.interest.taxable-total`

## The question

May the engine honestly publish `tax.us.2025.interest.taxable-total` as *the*
US-federal taxable-interest result reported on Form 1040 line 2b, or only as
the output of the currently declared interest model?

Concept semantics: [taxable-interest-concept.md](taxable-interest-concept.md).
Authority and category evidence:
[taxable-interest-authority-and-coverage.md](taxable-interest-authority-and-coverage.md).

## Verdict

**Not sufficient.** The current model may honestly publish a claim at level 3
of the ladder — *a result over the model's declared categories* — and may not
publish a level-4 derived tax-concept result or a level-5 official-line
binding.

The strongest single piece of evidence is a missing subtraction rather than a
missing addition, and it is best stated narrowly:

> In the § 135 education-exclusion fact pattern — assuming the modeled
> positive families and the three modeled adjustment classes otherwise
> reproduce the correct pre-line-3 amount — the engine publishes that
> pre-line-3 amount as `tax.us.2025.interest.taxable-total`. The official
> line-2b route requires Schedule B line 4, which is line 2 **less** line 3,
> and the § 135 exclusion has no representation anywhere on the interest
> route.

Two qualifications keep that statement honest.

**It is not a general identity.** The model does not necessarily compute
Schedule B line 2 either. Form 1099-OID box 2 and box 8, savings-bond interest
previously reported under a § 454 election, seller-financed mortgage interest,
and the OID adjustment class all feed line 2 and are unrepresented; and
acquisition premium, payer-netted bond premium, frozen-deposit timing, and
contingent-payment debt instruments can each make a *modeled* amount wrong —
in the contingent-payment case because the box 1 figure the model faithfully
records may not be the amount the noncontingent bond method requires be
included. The claim above is about the *missing subtraction*, not about the
model reproducing line 2.

**§ 135 is substantive, not presentational.** § 135(a) provides that "no
amount shall be includible in gross income by reason of the redemption during
such year of any qualified United States savings bond." Schedule B line 3 is
where that exclusion is reported; it is not what creates it. So this is a
tax-model defect, and it would remain one even if the product never generated
a Schedule B.

Everything else below either compounds that or is independent of it.

## Examined package and artifact boundary

### There is no repository-wide "current" package

`packages/content/tax/2025/published-packages.v28.json` — the highest-numbered
publication registry — lists `tax.us.2025.package.core-calculations` at
versions v1 through v33 **simultaneously**, each with its own checksum. The
registry is a monotone accumulating record of what has been published. It
carries no adoption pointer, no "current" marker, and no ordering beyond
version number.

"The current package" is therefore not expressible in committed state, and no
conclusion in this document rests on calling the highest-numbered artifact
current.

### The bounded examination candidate

This assessment examines exactly:

| Artifact | Version | Schema |
| --- | --- | --- |
| `tax.us.2025.package.core-calculations` | v33 | `artifact-package.v25` |
| `tax.us.2025.interest-composition` | v4 | `taxable-interest-composition.v1` |
| `tax.us.2025.rule.form1040-line2b` | v4 | `rule-artifact.v3` |
| `tax.us.2025.rule.interest-positive-total` | v1 | `rule-artifact.v3` |
| `tax.us.2025.form1040.line-2b` | v5 | `form-field.v3` |
| `tax.us.2025.rule.attachment.schedule-b` | v4 | `attachment-rule.v6` |
| `tax.us.2025.quantity.taxable-interest` | v1 | `quantity-vocabulary.v1` |
| `tax.us.2025.parameter.schedule-b-threshold` | v1 | `parameter-declaration.v1` |
| `tax.us.2025.citation.form1040.line-2b` | v1 | `citation.v1` |

Package v33 declares `scope` `{family: individual-income-tax, jurisdiction:
US-federal, tax_year: 2025}` and `composition_obligations`
`["tax.us.2025.interest.positive-total",
"tax.us.2025.interest.taxable-total"]`.

**This interest artifact graph is identical in every package version from v24
through v33.** The choice of v33 as the candidate is therefore not
load-bearing: any conclusion here holds for all ten. That was verified by
reading the member pins of each `package.core-calculations.v*.json` in
`packages/content/tax/2025/`.

## Current internal coextensiveness

### What is declared, and where

`packages/content/tax/2025/interest-composition.v4.json` declares
`coextensiveness: "slot-bijection"`, seven constituents, and:

```
"publishes": "tax.us.2025.interest.positive-total"
"required_universe": {
  "claim": "Seven declared positive taxable-interest families forming the
            gross Schedule B Part I line-1 basis, without subtractive
            adjustments."
}
```

That claim is honest and accurate. The composition says exactly what it is:
the gross line-1 basis, without adjustments.

`packages/content/tax/2025/rule.form1040-line2b.v4.json` publishes a
**different symbol** — `tax.us.2025.interest.taxable-total` — and `requires`
**ten** symbols: the composition's seven, plus
`interest.scheduleb-nominee-subtotal`,
`interest.scheduleb-accrued-interest-subtotal`, and
`interest.scheduleb-abp-adjustment-subtotal`. Its `composition` pin resolves
to `interest-composition` v4, the artifact that publishes `positive-total`.

### Where the ten-slot surface is declared

**The rule declares all ten slots, in content.**
`packages/content/tax/2025/rule.form1040-line2b.v4.json` names every one of
the ten in four independent, consumer-bearing structures: its ten input
`pins`; its ten-entry `requires` list; its `value` node, whose `subtract`
takes an `add` of the seven positive subtotal refs less an `add` of the three
adjustment subtotal refs; and its `when` guard, which is an `all` of ten
`require_closed` branches naming the ten source families. The full surface of
the derived concept is therefore recoverable from committed content by reading
one artifact.

`packages/content/tax/2025/rule.attachment.schedule-b.v4.json`, part
`part-i-interest`, independently repeats the surface in a `tie_out` block
naming `line_symbol: "tax.us.2025.interest.taxable-total"`, seven
`positive_subtotals`, three `adjustment_subtotals`, and `operation:
"subtract"`.

**No composition declares them.** This is the real gap.
`interest-composition.v4` declares seven constituents and publishes
`positive-total`. There is no composition citizen whose declared universe is
the ten-slot surface, and none that publishes `taxable-total`. The concept's
universe is declared by the artifact that *computes* it and by the attachment
that *displays* it, but not by the citizen kind whose job is to declare a
universe.

**The validator admits the three extras through a named special case.**
`packages/derivation/package_validation.py:217-221` defines
`_V11_ADJUSTMENT_SLOTS` as a hardcoded tuple of the three
`(source_family, subtotal)` pairs. The slot-bijection check at
`packages/derivation/package_validation.py:1154-1272` reaches it only through
a literal-identity gate:

```
v11_adjustment_route = (
    rule_pin["id"] == "tax.us.2025.rule.form1040-line2b"
    and rule_pin["version"] == "v4"
)
```

(`packages/derivation/package_validation.py:1213-1216`.) A second named
special case at `packages/derivation/package_validation.py:1168-1188` resolves
the composition for the obligated symbol `taxable-total` by walking through
that same specific rule id and version to a composition publishing
`positive-total`.

### What this means

Internal coextensiveness for `taxable-total` **is** enforced — the validator
does check an exact ten-slot bijection across `requires`, `value` refs,
`require_closed` reads, and input pins. The mechanism works, and it works
against a surface that content does declare.

The defects are narrower than "the universe lives in Python," and they are
three:

- **The composition citizen does not cover the published concept.** The
  artifact kind whose declared purpose is to state a universe states the wrong
  one — seven slots, for a different symbol. The ten-slot universe exists in
  content only as an implementation detail of a rule and as a display detail
  of an attachment.
- **The bijection is gated on a literal id and version.** It is a property of
  `rule.form1040-line2b@v4` specifically rather than a general contract. The
  gate **fails closed**, not open: an otherwise unchanged v5 loses both named
  special cases, so the composition-resolution walk at
  `packages/derivation/package_validation.py:1168-1188` finds no member and
  package validation reports `COMPOSITION_MEMBER_MISSING` before the package
  is accepted. The defect is therefore brittleness rather than escape — the
  subtractive route is available to exactly one artifact identity, and any
  successor version must be accompanied by a matching edit to Python. A
  contract that must be re-granted by code for each new version is not a
  contract the content layer owns.
- **The accepted contract for subtractive adjustments is unresolved**, so the
  special case has nothing to be an exception *to*. See below.

The layering point survives in a weaker and more precise form. Schedule B's
`tie_out` is a *second* declaration of the concept's arithmetic living in
presentation machinery whose own existence is conditional on a threshold; when
Schedule B is not required, that copy is simply not produced, and the two
declarations can drift apart with no artifact obliged to reconcile them. That
is a duplication-and-drift hazard, not an absence.

### Departure from the ratified contract

ADR-0026 (accepted, 2026-07-14) decision 2 states that package validation
"rejects unless the line-2b rule's constituent set is an exact bijection with
the universe's slots — no omission, duplication, substitution, **or extra**."
The current rule carries three extras relative to its pinned composition. The
validator permits them by named exemption.

ADR-0026 decision 7 explicitly deferred "the *subtractive adjustment*
mechanism (nominee interest, accrued interest paid at purchase, bond-premium
amortization), which a sum-of-positive-subtotals composition structurally
cannot express and **which requires its own contract decision**."

No such decision exists. The strings `nominee`, `ABP Adjustment`, and
`accrued interest` appear in exactly one file under `docs/adr/` — ADR-0026
itself, where they are named as deferred. No ADR mentions `adjustment_rows`
or `tie_out`.

The subtractive-adjustment mechanism therefore ships in content, in a schema
(`attachment-rule.v6`), and in a validator exemption, on an unratified
contract. ADR-0026 anticipated the exact structural problem — "a
sum-of-positive-subtotals composition structurally cannot express it" — and
the implementation resolved it by routing around the composition rather than
by extending it.

## Current external sufficiency assessment

Internal closure is established. External sufficiency fails on five
independent grounds, any one of which is disqualifying for a level-4 claim.

**E1 — A gross-income exclusion is unrepresented, so a required subtraction
is missing.** § 135(a) excludes qualifying redeemed savings-bond interest from
gross income; Schedule B reports it at line 3 and sends line 4 — line 2 less
line 3 — to Form 1040 line 2b. Nothing on the interest route represents the
exclusion, the qualifying expenses, the redemption proceeds the exclusion is
rationed against, or the subtraction itself: the engine's tie-out goes from the
line-1 rows and the three modeled adjustments directly to `taxable-total`. See
coverage map C13.

**This defect lands at level 4, not level 5.** Because § 135(a) governs
includibility in gross income, a taxable-interest result that has not applied
the exclusion is already wrong as a statement about the taxpayer's tax
position — before any question of which form line it occupies. Schedule B's
line 2 / line 3 / line 4 sequence is where the subtraction is *reported*, not
where it becomes true. The consequence matters for remediation: no change
confined to presentation, field prose, or attachment rendering can fix E1.

**E2 — Adjustment classes are missing, and the rule's shape forecloses
adding them.** Two subtractive needs are absent. The OID adjustment (C10) is
one of the four adjustment labels the Schedule B instructions name, and the
only one of those four the model does not carry. Publication 1212 directs that
it may "subtract or add accordingly" — but the
rule's `value` is a single `subtract` node with three fixed operands and all
three adjustment fact types are constrained nonnegative, so an upward
adjustment cannot be represented even in principle. Savings-bond interest
previously reported under a § 454 election (C18) is a further subtractive
class, and its omission overstates the total by the entire prior-year accrual
for a taxpayer who took an election the Code expressly offers. Both repairs
require changing the rule's shape, not only adding content.

**E2b — Two of the three reportable OID boxes have no representation.**
Publication 1212 directs the recipient to "[i]nclude all OID and qualified
stated interest shown on any Form 1099-OID, boxes 1, 2, and 8." The committed
content declares fact types for box 1 and box 5 only. Box 2 (qualified stated
interest) and box 8 (Treasury OID) are unrepresentable, and the residual
`non-form-interest` family cannot absorb them because its own predicate
excludes amounts accompanied by a Form 1099-OID statement. See C16, C17.

**E3 — A category that independently triggers the attachment is absent.**
Seller-financed mortgage interest is includible, must be listed first on
Schedule B Part I with the buyer's name, address, and SSN, and independently
requires Schedule B. It has no representation, and the residual family that
would absorb it is keyed `payer` + `tax-year` with no place for the required
disclosure. See C11.

**E4 — Reported amounts are treated as includible amounts.** Acquisition
premium (Pub 1212) routinely makes 1099-OID box 1 larger than the holder's
includible OID; payer-netted bond premium makes an ABP adjustment a
double-reduction. Neither circumstance is representable, so neither can be
detected or asked about. See C1, C3, C9.

**E5 — Nothing in the model carries the concept's meaning.** The quantity
vocabulary that types every interest amount,
`packages/content/tax/2025/quantity.taxable-interest.json`, is:

```
{"schema": "quantity-vocabulary.v1",
 "id": "tax.us.2025.quantity.taxable-interest",
 "version": "v1",
 "quantities": ["taxable-interest", "wages"]}
```

Two bare strings, one of which is `wages`. There is no unit, no currency, no
jurisdiction, no tax year, no definition, and no distinction between an
inclusion and a reduction — the three subtractive adjustment fact types carry
this same quantity as the seven inclusions they reduce. Direction exists only
as the position of an operand in the rule's `subtract` node.

The form field is explicitly presentation-only:
`packages/schemas/tax/form-field.v3.schema.json` describes itself as
"Presentation-only official field with at most one exact structured citation
pin." Its narrowing lives in a free-text `description`.

And the citations in the corpus do not reach controlling law or a specific
line — see the *Limitations of the authority corpus* section of the coverage
document. These two limitations are different in kind and should not be merged.

**Citing controlling law is possible and unused.** The `us-code` authority
family already exists in
`packages/schemas/derivation/citation.v1.schema.json`. Of the 74 citation
citizens in `packages/content/tax/2025/`, **zero** use it. So the accurate
statement is that *current artifacts are not cited to controlling authority* —
not that they could not be. Every statutory section this assessment relies on
could be expressed as a citation citizen today, with no schema change.

**Citing a specific line is not currently possible.** The `irs-instructions`
authority variant has no locator field, so "line 2b" cannot be recorded even
in principle. That one is a genuine vocabulary limit.

So there is no artifact anywhere whose subject is "US-federal taxable
interest for 2025"; and if one were written, it could be cited to statute
today but could not point at the form line it occupies.

## Model-support versus global-authorization matrix

Three distinct things have to be kept apart, because they license different
claims and only some of them exist:

- **Family-scoped closure** — a confirmation that one source family is
  complete, in the terms that family's own `closure_claim` states. This is
  **committed machinery**: it is what `require_closed` reads, and it is what
  the engine actually has. It supports a *family-scoped subtotal*.
- **Global workspace authorization** — a standing act by which the user
  authorizes the application to treat the facts currently in the workspace as
  the exhaustive input universe. This is what an *exhaustive total* would
  need. It is **selected product direction and not committed machinery**: no
  user act performs it, no marshaller accepts it, and no evaluator consumes
  it.
- **Model support** — external tax-model sufficiency for the exhaustive
  concept. This is the product's burden and no user attestation touches it.

Family-scoped closure does not aggregate into global authorization. Ten closed
families affirm ten declared propositions; the categories the model does not
represent are outside all ten, so the conjunction still falls short of "this
workspace holds everything." That gap is the subject of A15.

The matrix below is indexed by the second and third of these: its columns are
the global authorization, so the right-hand column is **prospective
throughout**, and its rows are model support. The matrix shows what may be
presented in each quadrant.

| | **Global authorization absent** *(all committed behavior lives here)* | **Global authorization present** *(prospective — machinery not built)* |
| --- | --- | --- |
| **Model support absent** *(current model)* | **Where the engine stands today.** Levels 1–2, plus level 3 for any family whose own closure is confirmed. With all ten families closed the engine does publish a value — but the strongest honest claim over it is level 3, a result over the model's declared categories, and the declared categories must be legible to the reader. Levels 4–6 unavailable. | Level 3 only, on the same reasoning: the authorization would settle the record question and leave the model question untouched. Levels 4–6 still unavailable. |
| **Model support present** *(hypothetical)* | Levels 1–2, plus level 3 for any family whose own closure is confirmed. The exhaustive total blocks on the specific unclosed families, and unrelated calculations remain available. | Levels 4–5 available. Level 6 requires a separate filing act. |

Three properties of this matrix are worth stating explicitly.

**The current engine occupies the top-left cell.** Not the top-right one: the
engine cannot be in a column defined by machinery that does not exist. What it
has is ten family-scoped closures, which is a real and useful thing and is not
the same thing.

**The left column is not empty.** Absent the global authorization, the model
still supports every source-report claim and every family-scoped subtotal
whose own family is confirmed. Blocking is constituent-scoped, not global —
which is why family-scoped closure has to be tracked separately from the
authorization that would license an exhaustive claim.

**The whole top row is where the danger lives, and building the authorization
would not move the engine out of it.** A user who has closed every family has
done everything asked of them and has every reason to believe the result is
complete. Nothing in their experience distinguishes the top row from the
bottom row. Only the product can make that distinction, and at present nothing
in the artifact graph carries the information needed to make it. The reason
this is worth stating precisely: adding global authorization is a plausible
next product step, and it would make the completeness impression *stronger*
while changing model sufficiency not at all.

## Permitted and prohibited product claims, as the model stands

### Permitted

- "This 2025 Form 1099-INT from *payer* reports $X in box 1."
- "The interest amounts recorded in this workspace sum to $X."
- "Over the seven interest categories this model covers, less the three
  Schedule B adjustment classes it covers, the 2025 total is $X" — provided
  the ten categories are named where the reader can see them.
- "This total does not account for the Series EE/I education exclusion,
  seller-financed mortgage interest, OID adjustments, or acquisition
  premium." Naming known gaps is always permitted and is the honest
  companion to the bounded claim.
- Blocking, with a reason, when a constituent family is unclosed.

### Prohibited

- "Your 2025 taxable interest is $X."
- "Form 1040 line 2b: $X", presented as the form line's value.
- Any presentation in which the bounded result occupies a position whose
  meaning is supplied by the official form rather than by the product.
- Any presentation that treats the user's workspace-completeness
  authorization as evidence of model coverage.
- A zero presented as an exhaustive total. A closure-backed zero over seven
  families is a true statement about seven families; as "your taxable
  interest is zero" it is a level-4 claim and fails for the same reasons a
  nonzero one does.

### What the engine currently does

`packages/content/tax/2025/form1040.line-2b.form-field.v5.json` binds
`tax.us.2025.interest.taxable-total`, carries `label: "Taxable interest"`,
`form.authority: "IRS"`, `form_id: "1040"`, `line: "2b"`, and a `description`
that narrows accurately: "exact seven-family positive taxable interest less
the three separately closed Schedule B adjustment classes: Nominee
Distribution, Accrued Interest, and ABP Adjustment."

Its `published_value` disposition renders `{value}`.

So the engine renders a level-3 result in a level-5 position, with the
narrowing carried in field prose. Whether that is honest is the decision
below.

## The central product question

> Binding a value to an official form line adopts that line's official
> meaning. A calculation known to cover only a bounded internal model must not
> silently occupy that line as though it were the complete tax concept.

### The strongest case for the rule

**User expectation is set by the form, not by the product.** "Form 1040, line
2b, Taxable interest" is a phrase with a fixed public meaning, printed by the
IRS on a document the user may sign under penalty of perjury. A user reading
a filled-in line 2b is not reading a product's output; they are reading their
tax return. No amount of adjacent prose changes what the numeral in that box
asserts, because the box's meaning is supplied by its author and the product
is not its author.

**Official-looking output is a claim about competence, not just content.** The
rendering carries `authority: "IRS"`. It borrows institutional credibility it
did not earn and cannot underwrite. The narrowing text is the product's; the
authority is the IRS's; a reader has no reason to weigh the former against
the latter.

**Downstream derivations do not read prose.** This is the decisive practical
argument. `tax.us.2025.interest.taxable-total` is not consumed only by a
rendering. Once published it is a symbol available to any rule. A field
description is not a guard: it is transported into the presentation projection
object, but nothing consumes it as a semantic contract, no validator checks it,
the committed citation-walk template does not render it, and it travels with no
derivation edge. The moment a
`total-income` rule consumes `taxable-total`, the bound is gone and the
downstream result carries an unqualified error. The narrowing exists exactly
one layer away from where it would need to be enforced.

**Defensibility.** If the amount is later found wrong, the product's position
is that it published a bounded model result and described the bound in a
field caption. That is a weak position when the output was rendered as a
federal tax return line, and it is weakest in precisely the case the coverage
map identifies: the Series EE/I taxpayer, for whom the published figure is
overstated, unqualified, and carries a `published_value` disposition
indistinguishable from a correct one.

**The gap is not a corner case in the model's own terms.** Whatever its
incidence among filers, which was not measured, E1 is not a subtlety within a
represented category — it is a whole line of the form with no representation
at all.

### The strongest case against the rule

**Incremental coverage is the only way coverage ever happens.** No model
begins complete. A rule that forbids occupying a form line until the concept
is fully modelled forbids shipping any form line at all, and therefore
forbids the incremental route by which sufficiency is actually reached. Taken
literally it is a rule against having a product.

**A bounded calculation is genuinely useful — on an assumption this project
did not test.** For a taxpayer with bank interest and no bond activity, the
current seven-family model computes exactly the right answer, and withholding
it imposes a real cost to prevent an error that taxpayer will not encounter.

The force of this argument depends entirely on how the affected and unaffected
populations compare in size, and **no prevalence evidence was examined here.**
Whether such taxpayers are most filers or few is an unmeasured hypothesis, and
it is stated as one. It is recorded because it is the honest form of the
strongest objection to the rule proposed above — not because the publication
has grounds to assert it. Anyone who wants to rest a product decision on this
argument has to go and measure the distribution first; nothing below relies on
it.

**Qualifications can be made visible, and the engine already does this
elsewhere.** The form field's `dispositions` block is not decoration: it
carries `blocked`, `guard_inapplicable`, `closure_backed_zero`,
`computed_zero`, and `published_value`, each with distinct `explain` text and
distinct `render` behaviour. `guard_inapplicable` already refuses to render a
value when the adjustments exceed the positive basis. The machinery for
"occupy the line conditionally, and explain" exists and is in use.

**A form-field description may be the honest place for the narrowing.** The
form field is the boundary between the product's concept and the
authority's presentation. If the narrowing must live somewhere, arguably it
belongs precisely at the point where the product's symbol meets the
government's label. Putting it deeper — in the rule or the composition —
would not make it more visible to a reader.

**"Silently" is doing the work.** The proposed rule prohibits *silently*
occupying the line. The current field is not silent: it names its seven
families and three adjustment classes explicitly. If the objection is that
the narrowing is not enforced on downstream consumers, that is an argument
for a stronger declaration mechanism, not for refusing to render.

### Where the two cases actually diverge

They agree that a bounded result is worth computing and worth showing. They
diverge on one question: **is the form-field description a claim-narrowing
instrument, or only a caption?**

The evidence in this milestone favours "only a caption," for a structural
reason rather than a rhetorical one. `form-field.v3` is declared
presentation-only. Its `description` is a free-text string that is carried
into the projection object but consumed by nothing as a semantic contract,
checked by no validator, rendered by no committed template, and attached to no
derivation edge — the same structural position as `required_universe.claim`,
which `packages/schemas/derivation/taxable-interest-composition.v1.schema.json`
requires to exist as a non-empty string and which no production code reads for
meaning. The
project already has one honesty gate implemented as unread prose. The
question before the owner is whether to add a second.

## Recommendation for owner disposition

1. **Adopt the rule, with the qualification that it governs the *symbol*, not
   the rendering.** The defect is not that a bounded number is displayed. It
   is that a bounded number is published under a symbol named
   `taxable-total`, bound to an IRS-authority field, and made available to
   every downstream consumer without its bound. Renaming and re-scoping the
   published symbol addresses the real hazard; refusing to render addresses
   the appearance of it.

2. **Do not leave the narrowing in prose.** Whatever shape is chosen, the
   declared universe and the known-unsupported categories must be machine-
   readable and reachable by a consumer, or the same failure recurs. Two
   candidate shapes are compared in
   [derived-tax-concept-declaration.md](derived-tax-concept-declaration.md).

3. **Treat E1 as the near-term correctness item, and treat it as a level-4
   defect.** The § 135 exclusion is a gross-income exclusion with no
   representation, so the published total omits a subtraction the statute
   requires — and it is wrong as a statement of taxable interest before any
   question of form-line binding arises. No presentation change can repair it.

   It is the sharpest of several findings that produce a specific wrong number
   for a specific identifiable taxpayer — C18 (§ 454 previously reported) and
   C16/C17 (Form 1099-OID boxes 2 and 8) do so as well, and C18's error can be
   larger. E1 ranks first because the omission is a whole line of the form and
   the affected taxpayer is identifiable from facts the workspace could hold.

   Scoping note for whoever takes it: the exclusion is rationed by the ratio
   of net qualified expenses to **total redemption proceeds**, so representing
   it means representing the proceeds, the interest within them, nontaxable
   educational benefits, modified AGI, and the ownership and age-at-issue
   conditions — not merely an expense figure. Where net qualified expenses
   equal or exceed proceeds the whole interest amount is excluded, which is
   the case in which the current engine's error is largest.

4. **Ratify or retire the subtractive-adjustment contract.** It ships today
   on a validator exemption keyed to one artifact id and version, against an
   ADR that deferred it pending its own decision. Either decision is
   defensible; the current state is that neither was made.

5. **Do not ask the user to close this gap.** Nothing in the workspace
   authorization can supply tax-model sufficiency, and any interface that
   invites the user to confirm coverage converts a statement they can make
   into one they cannot.

## Owner decisions required

| # | Decision | Consequence of deferral |
| --- | --- | --- |
| D1 | Does binding to an official form line require external tax-model sufficiency? | The current level-3-in-a-level-5-position rendering continues. |
| D2 | Should `taxable-total` be renamed and re-scoped to its actual bounded meaning, with a separate symbol reserved for the sufficient concept? | Downstream consumers keep inheriting an unqualified bound. |
| D3 | Is a derived tax concept a first-class declared citizen, or a strengthening of the existing distributed declaration? | The concept's universe stays declared by the rule that computes it and duplicated in a conditional Schedule B tie-out, with no composition citizen covering the published symbol and the bijection check gated on one artifact id and version. |
| D4 | Where is the § 135 exclusion implemented — a signed constituent of the composition, a separate rule feeding the concept, or a value the concept consumes — and does the model also name a pre-exclusion intermediate? Whether the exclusion belongs to current-year taxable interest is settled by § 135(a) and is not in scope for this decision. | E1 stays unaddressed; the published total omits a subtraction the statute requires, so the engine remains wrong at claim level 4 regardless of how line 2b is bound. |
| D5 | Ratify, revise, or retire the subtractive-adjustment mechanism deferred by ADR-0026 decision 7(b). | Production content continues on an unratified contract with a named validator exemption. |
| D6 | Should the citation vocabulary gain a line/section locator, and should tax claims be required to cite controlling law? | Current artifacts stay uncited to controlling authority, and the `us-code` family the schema already offers stays unused. |
| D7 | Should the Schedule B requirement rule test the seven non-threshold filing conditions? | Sub-threshold taxpayers with adjustments get a reduced line 2b and no Schedule B disclosing the reduction. |
