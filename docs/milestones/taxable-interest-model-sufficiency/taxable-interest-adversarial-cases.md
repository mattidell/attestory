# Adversarial Cases: Testing the Modeling Requirements

## What this document is

Bounded synthetic cases that test the **modeling requirements** proposed in
[tax-modeling-foundation.md](tax-modeling-foundation.md) and
[concept-coverage-and-claims.md](concept-coverage-and-claims.md), using the
taxable-interest specimen as the medium.

This is not a category census. A census of missing features cannot terminate,
and it cannot tell you what it is missing. These cases are organised by
**failure class** — the distinct ways a layer collapse produces a wrong or
overstated result. A case is admitted only if it tests a distinct modeling
requirement, materially changes the support envelope, or invalidates an
existing conclusion.

Each case names the defect it targets, the result the current model would
produce, and the artifact or future test that could operationalize it.

These are **conceptual and traceable scenarios, not production fixtures.**
Every payer, amount, and circumstance is invented. No case uses or implies
personal data, and none is authorized for use as a real-run fixture.

## How to read "current model result"

None of these cases was executed against the engine. Each "current model
result" is derived by reading the committed artifacts and the code paths that
consume them, and each is labelled with what kind of statement it is:

- **Executable** — the stated outcome follows from the committed artifacts
  given the stated preconditions, and could be demonstrated by a test written
  against current content without any contract change.
- **Conditional** — the stated outcome follows only if additional
  preconditions hold that the setup must state explicitly. For
  `tax.us.2025.interest.taxable-total`, publication requires **all ten**
  `require_closed` branches in `rule.form1040-line2b.v4.json`'s `when` guard
  to pass, plus the `gte` guard refusing a negative result. A case that closes
  one family establishes nothing about publication unless it closes the other
  nine.
- **Conceptual** — the case depends on product machinery that does not exist
  in committed state. Its consequence is a design consequence, not an
  observation.

**Block codes.** The engine has two, defined at
`packages/derivation/evaluator.py:24-26`: `SOURCE_SET_UNCLOSED`
(`BLOCK_CLOSURE`), raised by `require_closed` when a source set is not in
`closed_sets`; and `DEPENDENCY_ABSENT` (`BLOCK_ABSENT`), raised when a
required symbol was never published. `OPEN_DEPENDENCY` is **not** a code the
runner emits. It appears as the declared `blocked.code` inside
`rule.form1040-line2b.v4.json` itself, but no consumer reads that field — the
form field's own `blocked.codes` enum lists `DEPENDENCY_ABSENT`,
`DEPENDENCY_INVALID`, `CATEGORICAL_DOMAIN_MISMATCH`, and
`SOURCE_SET_UNCLOSED`, and the record and presentation layers both carry
comments noting `SOURCE_SET_UNCLOSED` as "the code the runner actually emits."
The rule's declared block code is therefore stale content that no execution
path can produce — a small finding in its own right, and the reason the cases
below name the runner's codes rather than the artifact's.

Supporting evidence: category identifiers `C1`–`C18` refer to the coverage map
in
[taxable-interest-coverage-profile.md](taxable-interest-coverage-profile.md);
findings `E1`–`E5` and decisions `D1`–`D7` refer to
[current-engine-assessment.md](current-engine-assessment.md);
claim levels 1–6 are defined in
[concept-coverage-and-claims.md](concept-coverage-and-claims.md) and
instantiated in [taxable-interest-concept.md](taxable-interest-concept.md);
failure classes F1–F9 are defined below.

## The failure classes

Nine classes. Each is a distinct way the eight layers collapse into one
another, and each requires something different of the architecture.

| Class | The failure | What the architecture must therefore provide |
| --- | --- | --- |
| **F1** | The reported amount is not the includible amount | Layers 2 and 4 separately representable |
| **F2** | A substantive exclusion changes the result | Exclusions belong to the substantive model, not to the form that discloses them |
| **F3** | Timing moves an amount between periods | The includible event is declared, not assumed to be the reported one |
| **F4** | Ownership changes whose income it is | The subject of an amount is modelled, not inherited from the payee line |
| **F5** | An election changes the treatment | Elections are representable circumstantial facts with a declared default |
| **F6** | A legally material circumstance is absent from every source document | The economic-fact layer can hold facts no document supplies, and can be asked for them |
| **F7** | An item affects reporting without defining substantive meaning | Reporting mechanics can operate without becoming the concept |
| **F8** | An unsupported case is undetectable from the represented facts | The boundary is detectable from inside the model, or the claim is bounded |
| **F9** | A coherent concept has only partial executable coverage | The intensional model and the coverage profile are separately declared |

**F5 has no case below.** The market-discount election (C6) is the obvious
candidate, and no case was constructed for it. That is recorded as a gap in
the adversarial set, not as evidence that the class is handled. It is exactly
the kind of thing consideration 11 of the good-enough framework measures.

## Index by failure class

| # | Case | Classes | Specimen references |
| --- | --- | --- | --- |
| A1 | Acquisition-premium OID | F1, F6, F8 | C3, E4 |
| A2 | Cash interest with no information return | F6, F9 | C4 |
| A3 | Nominee distribution below the Schedule B threshold | F4, F7 | C7, gap 5 |
| A4 | Series EE education exclusion | F2, F6 | C13, E1 |
| A5 | Seller-financed mortgage | F9 | C11, E3 |
| A6 | Box 1 closed, nothing else | F9 | C1 |
| A7 | All ten slots closed, model still insufficient | F9 | E1–E5 |
| A8 | Full workspace authorization, unmodelled category present | F9 | D1 — conceptual |
| A9 | Sufficient model, workspace support absent | F9 | the converse quadrant |
| A10 | The overstated line 2b | F9 + claim scope | D1, D2 |
| A11 | Upward OID adjustment | F1, F9 | C10, E2 |
| A12 | K-1 interest and the residual family | F8 | C4, C5 |
| A13 | Payer-netted bond premium | F1, F8 | C9 |
| A14 | Two non-form amounts from one payer | F8 | C4 |
| A15 | Two Form 1099-OID statements, one wholly unrepresentable | F8, F9 | C16, C17 |
| A16 | Savings bonds previously reported under § 454 | F2, F3 | C18, D5 |

The distribution is itself a finding. F8 and F9 dominate, F1 and F2 are well
covered, F3 and F4 have one case each, F7 has one, and F5 has none. A set
weighted this way tells you where the architecture has been tested and where
it has merely been asserted.

---

## A1 — The acquisition-premium OID

**Setup.** The taxpayer holds one corporate bond bought on the secondary
market at a cost exceeding its issue price plus previously includible OID, so
§ 1272(a)(7) requires a reduction. Payer B furnishes a 2025 Form 1099-OID
reporting $1,000 in box 1. The taxpayer's includible OID is $700.

*Preconditions for publication.* All ten source families are closed: the
1099-OID box 1 family holds the single statement above, and the other nine —
1099-INT boxes 1, 3, and 10, 1099-OID box 5, non-form interest, Form 1065 K-1
box 5, and the three Schedule B adjustment classes — are closed empty.

**Expected honest result.** The engine can support "Payer B's 2025 Form
1099-OID reports $1,000 in box 1" (level 1). It cannot support any statement
about the taxpayer's includible OID.

**Current model result — executable.**
`tax.us.2025.f1099oid.box1-interest-oid` records $1,000. The `oid-subtotal` is
$1,000. With the preconditions above, all ten `require_closed` branches pass
and the `gte` guard holds, so `taxable-total` publishes $1,000 with
disposition `published_value`.

**Defect exposed.** A reported fact is consumed as an economic fact. The
acquisition date and cost — the circumstances that determine both whether
§ 1272(a)(7) applies at all and by how much — have no representation, so the
discrepancy is not merely uncomputed, it is unrepresentable and therefore
unaskable. The result is overstated by $300 with no signal of any kind.

**Operationalization.** A test asserting that the model can distinguish "box
1 reports $X" from "includible OID is $X" would fail at the vocabulary layer:
`packages/content/tax/2025/interest_composition.bundle.json` has one fact
type for both. The case is a specification for that distinction, not for a
computation.

---

## A2 — Cash interest with no information return

**Setup.** The taxpayer received $40 of interest on a personal loan to an
unrelated party. No Form 1099 was furnished. Under the Instructions for Form
1040 line 2b, the amount is includible.

**Expected honest result.** Includible; representable.

**Current model result — executable.** Correct.
`tax.us.2025.non-form-interest.amount`
carries it; family `tax.us.2025.non-form-interest` authorizes
`interest.non-form-subtotal`; it enters the composition as a declared slot.

**Defect exposed.** None on this path. The case is included as the control:
it establishes that the residual family works for the case it was designed
for, which is what makes A5 and A12 findings rather than general complaints.

**Operationalization.** Already covered by existing content. Its value is as
the baseline against which A5 and A12 are contrasted.

---

## A3 — Nominee distribution below the Schedule B threshold

**Setup.** The taxpayer has $600 of box 1 interest from Bank Alpha, of which
$100 belonged to a sibling and was distributed to them as a nominee. Under
the Instructions for Schedule B, condition 7, receiving interest as a nominee
requires Schedule B **regardless of amount**.

**Expected honest result.** Line 2b is $500, and Schedule B is required and
must show the $600 listing with a "Nominee Distribution" row of $100.

*Preconditions for publication.* All ten source families are closed: the
1099-INT box 1 family holds Bank Alpha's statement, the nominee-adjustment
family holds the $100, and the other eight are closed empty.

**Current model result — executable given those preconditions.**
`rule.form1040-line2b.v4.json` subtracts the nominee subtotal: line 2b is $500.
But `rule.attachment.schedule-b.v4.json`'s `requirement` compares each of
`tax.us.2025.interest.positive-total` ($600) and the ordinary-dividends
subtotal ($0) separately against `tax.us.2025.parameter.schedule-b-threshold`
($1,500), recording one trigger per subtotal and requiring the attachment if
*any* trigger is over — see `packages/derivation/runner.py:905-913`. Neither
$600 nor $0 is greater than $1,500, so **Schedule B is not required**.

The $100 reduction therefore happens invisibly. There is no attachment, no
Part I listing, and no row labelled "Nominee Distribution" — because those
rows exist only inside
`rule.attachment.schedule-b.v4.json`'s `itemizations`, which is not produced.

**Defect exposed.** The attachment rule tests one of the eight filing
conditions. Three of the seven untested conditions correspond to adjustment
classes the model already carries, so the engine holds the facts that would
prove Schedule B is required and does not consult them. This is the sharpest
case in this document because the model is not missing information — it is
declining to use information it has.

**Operationalization.** A test asserting `scheduleb.disposition` is "required"
whenever any adjustment subtotal is nonzero. It would fail against
`rule.attachment.schedule-b.v4.json` today. The fix is a `requirement` shape
that admits non-threshold branches; the schema is `attachment-rule.v6`.

---

## A4 — The Series EE education exclusion

**Setup.** Every condition § 135 imposes is stated, because the exclusion is
not a function of expenses alone:

- **The bonds.** Series EE bonds issued in June 1995 — after 1989, as
  § 135(c)(1) requires.
- **Ownership and age.** The bonds were issued in the taxpayer's own name as
  sole owner. The taxpayer was born in 1968 and so had reached age 24 before
  the first day of June 1995, satisfying § 135(c)(1)(B).
- **Filing status.** Single. Married filing separately is ineligible under
  § 135(d)(3); single is not.
- **Redemption.** The taxpayer cashed the bonds during 2025 for **$5,000 of
  total proceeds — $2,000 principal and $3,000 interest.** Bank Alpha reports
  the $3,000 in box 3 of a 2025 Form 1099-INT.
- **Expenses.** The taxpayer paid **$5,000** of qualified higher education
  expenses in 2025 for a dependent child enrolled at an eligible educational
  institution, and received **no** nontaxable educational benefits — no
  scholarship, no fellowship grant, nothing to net out.
- **No competing use of those expenses.** None of the $5,000 was taken into
  account in figuring an education credit, and none was used to figure the
  nontaxable part of a Coverdell education savings account distribution or of
  a qualified tuition program distribution. § 135(d)(2) reduces the qualified
  expenses by any amount so used, *before* the § 135(b) limitation is applied,
  and Form 8815 line 2 takes only the expenses that survive that reduction.
  Without this premise the $5,000 on line 2 would not be established, because
  the same tuition dollars can be claimed only once across these benefits.
- **Income.** Modified AGI of $60,000, well below the § 135(b)(2) phaseout,
  which for a single filer in 2025 begins at $99,500 and closes out at
  $114,500.

*Preconditions for publication.* All ten source families are closed: the
1099-INT box 3 family holds the single statement above, and the other nine are
closed empty.

**Expected honest result.** Form 8815 works as follows. Line 2 is $5,000 —
the qualified expenses that survive the § 135(d)(2) coordination reduction,
which here is the full amount because none of them was used for a credit or
for a tax-free ESA or QTP distribution. Line 3 is $0 of nontaxable benefits;
line 4 is $5,000.
Line 5 is the $5,000 of total proceeds, principal *and* interest — this is the
§ 135(b)(1) limitation, and it is the step that makes expenses and excluded
interest different quantities. Line 6 is the $3,000 of interest included in
those proceeds. Line 7 divides line 4 by line 5, but because line 4 equals line
5 the form directs entering **1.000** rather than a computed ratio. Line 8 is
line 6 × line 7 = $3,000. MAGI of $60,000 is below the line 10 threshold of
$99,500, so line 11 is zero or less, line 13 is **-0-**, and line 14 —
excludable savings bond interest — is $3,000 − $0 = **$3,000**.

Form 8815 line 14 carries to **Schedule B line 3**. So Schedule B line 2 is
$3,000, line 3 is $3,000, line 4 is **$0**, and Form 1040 line 2b is **$0**.
Schedule B is required regardless of amount under condition 6, because the
taxpayer is claiming the exclusion.

The ratio at lines 5 through 7 is the whole point of choosing these numbers.
Expenses do not reduce interest dollar for dollar; they enter as a fraction of
redemption proceeds and are then applied to the interest. Full exclusion
follows here only because net qualified expenses equal or exceed total
proceeds, which caps the fraction at 1.000. Had the taxpayer paid $2,000 of
expenses against the same $5,000 of proceeds, line 7 would be 0.400 and the
exclusion $1,200 — not $2,000.

**Current model result — executable.** `f1099int.box3-interest` records
$3,000. There is no line-3 constituent, no § 135 representation on the
interest route, and no fact type for qualified higher education expenses,
redemption proceeds, nontaxable educational benefits, modified AGI, the
taxpayer's age at issue, or the § 135(d)(2) coordination — that is, whether
those same expenses were also used for an education credit or a tax-free
ESA or QTP distribution. With the preconditions above, all ten closures pass
and `taxable-total` publishes $3,000 with disposition `published_value`.

Schedule B *is* produced here, but for the wrong reason: the attachment rule
fires because `positive-total` of $3,000 exceeds $1,500, not because the
taxpayer is claiming the exclusion under condition 6. Its Part I tie-out shows
the seven positive subtotals less three adjustments tying to `taxable-total`.
It shows no line 3, because `rule.attachment.schedule-b.v4.json`'s `tie_out`
has no place for one. Had the same taxpayer redeemed bonds yielding $900 of
interest, Schedule B would be required under condition 6 and the engine would
not produce it at all.

**Defect exposed.** E1. In this fact pattern the modeled inputs do reproduce
the correct pre-line-3 amount, and the engine publishes that amount as
`taxable-total` while the official route requires line 4 — the same amount
less the § 135 exclusion. Here the exclusion consumes the entire amount, so
the correct line 2b is $0 and the engine publishes $3,000: **the overstatement
is $3,000, the whole of it.** The disposition is indistinguishable from a
correct result, and the attachment that would normally let a reader check the
arithmetic is itself missing the line.

Note that the coincidence is what makes this case sharp: because the setup
holds one box 3 statement and nothing else, the model's pre-line-3 figure
happens to be right, isolating the missing subtraction as the sole error. That
does not generalise — in a workspace also holding Form 1099-OID box 2 or box 8
amounts, or a § 454 previously-reported adjustment, the pre-line-3 figure
would be wrong as well.

Note the artifact-level asymmetry. `tax.us.2025.ss-benefits-scope.no-form-8815`
in `packages/content/tax/2025/ss-benefits-scope.bundle.json` is a
declared-absence assertion that bounds the Social Security benefits worksheet:
committed content there represents the proposition *that no Form 8815 is in
play*, so the worksheet's scope condition can be discharged explicitly. The
interest route has no artifact standing in any relation to Form 8815 —
neither an exclusion constituent nor a declared absence. So one route
represents a bounded Form 8815 proposition and the other represents none.

That asymmetry is evidence about the artifacts, not about anyone's
intentions. It does not establish that the exclusion was considered and set
aside on the interest route, and no inference about authorial choice is drawn
here. What it does establish is that a declared-absence assertion is an
available and already-used device in this corpus, so the interest route's
silence is not a limitation of the vocabulary.

**Operationalization.** A test asserting that no `published_value` disposition
is reachable for `taxable-total` while the model has no line-3 constituent.
That test would fail today for every taxpayer, which is the point: the gate
is not per-case, it is per-model.

---

## A5 — Seller-financed mortgage interest

**Setup.** The taxpayer sold a house with seller financing. The buyer used it
as a personal residence and paid $8,000 of interest in 2025. No Form 1099 was
furnished. Schedule B Part I line 1 directs: list this interest first, and
show the buyer's name, address, and SSN. Condition 2 requires Schedule B
regardless of amount.

**Expected honest result.** $8,000 is includible; Schedule B is required; the
buyer's identifying details must appear in Part I.

**Current model result — executable.** No representation exists —
"seller-financed" occurs
nowhere in `packages/content/` or `docs/adr/`. The amount would be entered as
`non-form-interest.amount`, which is keyed `payer` + `tax-year` and has no
field for an address or SSN. The $8,000 would enter `taxable-total` at the
right value, Schedule B would be required (by amount, coincidentally), and
its Part I would list the amount without the mandatory buyer disclosure and
not first.

**Defect exposed.** A materially relevant category absent from the fact
vocabulary, where the absence degrades a *disclosure* obligation rather than
an amount. It also raises a boundary the product must decide before modelling
it: the required disclosure is personal data about a third party.

**Operationalization.** Not a computation test. This is a specification input
for whether the model represents circumstances at all (Shape A/B in
[representation-reconnaissance.md](representation-reconnaissance.md)) and
a data-boundary question for the owner.

---

## A6 — Box 1 closed, nothing else

**Setup.** The taxpayer confirms the Form 1099-INT box 1 family is complete.
No other family is confirmed.

**Expected honest result.** "Every box 1 statement item is recorded, and they
sum to $X" (level 3, family-scoped). Nothing about taxable interest.

**Current model result — executable.** Correct, and this is the model working
as designed. `rule.form1040-line2b.v4.json`'s `when` is an `all` of ten
`require_closed` branches, so the first unclosed source set raises
`BLOCK_CLOSURE` and `taxable-total` blocks with **`SOURCE_SET_UNCLOSED`**,
naming the source set. The form field renders empty under its `blocked`
disposition, whose declared codes include `SOURCE_SET_UNCLOSED`.

Which code appears depends on the execution path, and the distinction matters:
`SOURCE_SET_UNCLOSED` means a family exists but is unconfirmed, while
`DEPENDENCY_ABSENT` means a required symbol was never published at all — the
path taken when a constituent subtotal's own rule did not run. Both render
empty; they are different diagnoses.

**Defect exposed.** None. Included because it demonstrates the property that
makes the bottom-left quadrant of the support matrix non-empty: blocking is
constituent-scoped, so the box 1 subtotal remains available while the total
does not. Any future shape must preserve this.

**Operationalization.** Existing behaviour; the case documents what must not
regress.

---

## A7 — All ten slots closed, model still insufficient

**Setup.** The taxpayer confirms every one of the ten source families is
complete: the seven positive families and the three Schedule B adjustment
classes. The workspace holds $3,000 of box 3 Series EE interest, and the
taxpayer meets every § 135 condition set out in A4 in full — including net
qualified expenses of $5,000, at least equal to the $5,000 of redemption
proceeds, and including the premise that none of those expenses was also used
for an education credit or for a tax-free Coverdell ESA or QTP distribution,
so the § 135(d)(2) coordination reduces nothing. The whole $3,000 is therefore
excludable. They were never asked about any of it.

**Expected honest result.** Line 2b is $0.

**Current model result — executable.** The setup closes all ten families by
construction, so every `require_closed` passes and the `gte` guard holds. The
slot bijection validates: `requires`, `value` refs, closure reads, and input
pins all form the exact declared ten-slot surface. `taxable-total` publishes
$3,000, `published_value`.

**Defect exposed.** This is the milestone's central case. Internal
coextensiveness is fully satisfied — the mechanism at
`packages/derivation/package_validation.py:1154-1272` does exactly what it
promises — and the answer is wrong by $3,000. Slot bijection proves the rule
consumes what its composition declares. It says nothing about whether the
declared slots are the legally relevant ones.

A reviewer who verifies the bijection, verifies each closure, verifies each
subtotal, and verifies the arithmetic will find every check passing and will
have verified nothing about tax-model sufficiency.

**Operationalization.** No test over the current artifact set can catch this,
because no artifact records that the education exclusion is a relevant
category. The case is the argument for a declared known-unsupported-category
surface — and simultaneously the argument that such a surface must not be
readable as a completeness claim about everything omitted from it.

---

## A8 — Full workspace authorization, unmodelled category present

**Setup.** The taxpayer adopts the standing workspace-calculation
authorization: they permit the application to treat the facts currently in
the workspace as the exhaustive input universe. They have entered everything
they possess. They also hold a bond bought at acquisition premium (A1).

**Expected honest result.** The user's authorization is fully effective as to
what it covers. Tax-model sufficiency is still absent, so no level-4 claim is
available.

**Current model result — conceptual, and the reason matters.** The standing
workspace authorization is a **selected product direction, not committed
machinery**. Nothing in committed state implements it: it is not an act the
user can perform, not a marshaller input, not a closure producer, and not an
evaluator input. There is therefore no execution in which "the user adopts the
standing authorization" causes ten families to close. Closure today is
produced only per family, on a family membership horizon.

Restated as what committed state can support: if the user separately confirms
each of the ten families — the operation that exists — then all ten
`require_closed` branches pass, `taxable-total` publishes, and the user is
shown a complete-looking taxable-interest figure while the acquisition-premium
error stands uncorrected and unsignalled. That much is executable, and it is
enough to make the point.

What is *conceptual* is the framing: whether a single global authorization
should ever be treated as licensing an exhaustive claim. That question is
live precisely because the machinery does not exist yet, which is the useful
time to answer it.

**Defect exposed.** The user has made the only statement they are competent
to make — about what they possess — and the product would treat it as licence
for a claim only the product could underwrite, about what the model covers.
Nothing in the user's experience distinguishes this from a fully supported
result. This is the top-right cell of the support matrix, and the reason the
two supports must remain independent.

**Operationalization.** A presentation-level test: assert that closure — by
whatever means it is obtained — never changes the *claim level* of a published
result, only its workspace support. No current artifact carries claim level,
so the test presupposes D2 or D3, and the global-authorization form of it
additionally presupposes machinery that does not exist.

---

## A9 — Sufficient model, workspace support absent

**Setup.** Assume, counterfactually, a model with external sufficiency. The
taxpayer has entered two Form 1099-INT statements and confirmed the box 1
family, but has not confirmed the box 3 family and has adopted no standing
authorization.

**Expected honest result.** The exhaustive total blocks, naming the box 3
family. The box 1 subtotal remains available. Every source-report claim
remains available. Unrelated calculations — wages, dividends — remain
available.

**Current model result — the blocking behaviour is executable; the sufficient
model is counterfactual.** Structurally correct: the unclosed box 3 family
raises `SOURCE_SET_UNCLOSED` naming that source set, the `blocked` disposition
renders empty, and blocking is scoped to the dependent result. The box 1
subtotal, whose own family is confirmed, remains available.

**Defect exposed.** None. The case is the converse control for A8, and
establishes that the two supports fail in genuinely different ways: missing
workspace support produces a *block with a name*, while missing model support
produces a *published value*. That asymmetry is the whole problem — the
failure the product can detect is loud, and the failure it cannot detect is
silent.

**Operationalization.** Existing behaviour; documents the contrast.

---

## A10 — The overstated line 2b

**Setup.** A4's taxpayer, with A4's preconditions in full — including the
§ 135(d)(2) premise that none of the $5,000 of qualified expenses was also
used for an education credit or for a tax-free ESA or QTP distribution, which
is what establishes the $5,000 on Form 8815 line 2 and hence the $3,000
exclusion — views the generated Form 1040.

**What they see — executable given A4's preconditions.** A field labelled
"Taxable interest", line "2b", form "1040", authority "IRS", rendering `3,000`
under the `published_value` disposition, whose `render` is `{value}`. The
honest figure for that line is $0. Behind it,
`form1040.line-2b.form-field.v5.json` carries a `description` reading "exact
seven-family positive taxable interest less the three separately closed
Schedule B adjustment classes."

**Defect exposed.** A level-3 result rendered in a level-5 position. Two
distinct hazards:

*The reader hazard.* "Form 1040, line 2b, Taxable interest" has a fixed
public meaning supplied by the IRS. The narrowing is supplied by the product,
in a caption, one layer away.

*The consumer hazard, which is worse.* `tax.us.2025.interest.taxable-total`
is a published symbol available to any rule. `form-field.v3` is declared
presentation-only in
`packages/schemas/tax/form-field.v3.schema.json`; its `description` has no
semantic consumer, no validator, and no derivation edge. It is transported
into the presentation projection object, but nothing consumes it as a
contract and the committed citation-walk template does not render it — so
even the reader hazard above assumes a surface that would have to be built.
The first downstream rule to
consume `taxable-total` inherits the value without the caption, and every
result derived from it carries an unqualified error.

**Operationalization.** A validator asserting that no symbol may be consumed
by a rule outside its declared claim level, or bound to an official form
field whose authority exceeds it. Both presuppose a declaration that does not
yet exist. This case is the primary evidence for decisions D1 and D2.

---

## A11 — The upward OID adjustment

**Setup.** Payer B's Form 1099-OID box 1 reports $500. The taxpayer's
correctly figured OID is $650. Publication 1212, under "Showing an OID
adjustment," directs listing the full amount and then "subtract or add
accordingly" to reach line 2.

**Expected honest result.** Line 2b includes $650.

**Current model result — executable.** There is no OID-adjustment family, fact
type, or
subtotal, so no adjustment can be recorded at all. Even if one were added,
`rule.form1040-line2b.v4.json`'s `value` is a single `subtract` node with
three fixed operands, and all three adjustment fact types are constrained
nonnegative — so an upward adjustment remains inexpressible without changing
the rule's shape.

**Defect exposed.** The subtractive-adjustment mechanism was designed around
three classes that happen to reduce, and generalised as "subtraction." The
authority describes four classes, one of which is bidirectional. The
architecture, not merely the content, forecloses the correct answer.

This also shows why the quantity vocabulary matters: because
`quantity.taxable-interest` carries no direction, direction lives only in an
operand's position in the rule, where it cannot vary per instance.

**Operationalization.** A specification input for contract question 2 in
[representation-reconnaissance.md](representation-reconnaissance.md) —
whether a composition can express a signed constituent — and for decision D5.

---

## A12 — K-1 interest and the residual family

**Setup.** The taxpayer receives a 2025 Schedule K-1 (Form 1065) from
Partnership P reporting $200 of interest in box 5. No Form 1099-INT or
1099-OID relates to it.

**The ambiguity.** `tax.us.2025.form1065-k1.box5-interest` covers it. But
the residual fact type
`tax.us.2025.non-form-interest.amount` is titled "Interest income received
without a Form 1099-INT/OID statement instance for 2025", which the K-1
amount also satisfies on its face. Nothing in either predicate excludes the
other. A user entering the amount under the residual family would produce a
$200 subtotal there *and*, if they also entered the K-1, a $200 subtotal
there — summing to $400.

**Compounding defect.** The family artifact and its own fact type disagree.
`packages/content/tax/2025/family.non-form-interest.json` reads "without a
Form 1099-INT statement instance"; the fact type in
`packages/content/tax/2025/interest_composition.bundle.json` reads "without a
Form 1099-INT/OID statement instance". Under the family's narrower wording,
every 1099-OID amount is also a residual member.

**Defect exposed.** A residual family named for what it lacks is not a safety
net. Its predicate is fact-type membership; the prose cannot enlarge or
narrow it, and here the prose contradicts itself across two artifacts that
must agree.

**Operationalization.** A content test asserting that a family's
`closure_claim` and its member fact type's title describe the same predicate.
It would fail today on `non-form-interest`. What such a check costs, and
whether the predicate agreement it asserts can be expressed mechanically
rather than by review, were not established here.

---

## A13 — Payer-netted bond premium

**Setup.** The taxpayer holds a bond bought at a premium. Bank Alpha's Form
1099-INT reports box 1 net of amortizable bond premium — that is, the payer
already applied the reduction. The taxpayer, or the interface, also records
an ABP adjustment for the same premium.

*Preconditions for publication.* All ten source families are closed: the
1099-INT box 1 family holds Bank Alpha's statement, the ABP-adjustment family
holds the duplicate adjustment, and the other eight are closed empty. The
subtraction must leave the total at or above zero, or the `gte` guard blocks
instead of publishing.

**Expected honest result.** No ABP adjustment is appropriate; the premium has
already been applied once.

**Current model result — executable given those preconditions.**
`scheduleb.adjustment.abp-adjustment.amount` accepts the entry. `taxable-total`
subtracts it a second time. The result is understated with a `published_value`
disposition. Nothing in the closure or bijection checks distinguishes this from
a correct adjustment.

The family's `closure_claim` in
`packages/content/tax/2025/family.scheduleb-adjustment.abp-adjustment.json`
correctly scopes itself to the case "where the payer did not already net the
amount" — so the model *states* the precondition and has no way to test it.
Form 1099-INT boxes 11, 12, and 13 (bond premium) have no representation.

**Defect exposed.** A precondition declared in prose and enforced nowhere.
The adjustment instance is keyed `tax-year` + `adjustment-instance`, with no
link to the statement it adjusts, so even a human reviewer reading the
findings cannot tell which box 1 amount the adjustment relates to.

**Operationalization.** A test asserting that an ABP adjustment cannot be
recorded without a linked statement fact. It presupposes an identity change
to the adjustment fact types, which is contract question territory.

---

## A14 — Two non-form amounts from one payer

**Setup.** The taxpayer has two separate interest-bearing arrangements with
the same counterparty, neither producing a Form 1099: $300 on one and $150 on
the other.

*Preconditions.* The claim below is about the `non-form-subtotal` symbol, which
requires only that the `non-form-interest` family be closed. Carrying the error
through to a published `taxable-total` requires the other nine families to be
closed as well; the setup assumes them closed empty.

**Expected honest result.** Two distinct facts, $450 total.

**Current model result — executable.** `tax.us.2025.non-form-interest.amount`
has identity keys `payer` and `tax-year` only. The two amounts answer the *same*
fact identity, so under `supersession: {policy: "free"}` the second entry
supersedes the first rather than joining it. The subtotal is $150.

Every other interest fact type in the model is keyed on payer **and**
statement. The residual family is the one that is not, because a non-form
amount has no statement — but nothing was substituted for it.

**Defect exposed.** Identity collapse producing a silently understated
subtotal, in the one family that exists to catch everything the others miss.
The family can close successfully — the user attests that everything is
recorded, and it is; it is just recorded as one fact instead of two.

**Operationalization.** A test entering two non-form amounts with distinct
arrangements under one payer and asserting a $450 subtotal. It would fail
today, and demonstrating it needs no contract change.

The property-level repair is that the fact type must admit a discriminator
distinguishing two arrangements with one payer, since `payer`/`tax-year`
cannot. Adding one changes the fact type's identity, which is a successor
question: what it would take to migrate existing facts, and which consumers
depend on the present keying, were not examined here.

---

## A15 — Two Form 1099-OID statements, two unrepresented boxes

**Setup.** The taxpayer holds two discount obligations, and the brokerage
issues a **separate Form 1099-OID for each**, as the Instructions for Forms
1099-INT and 1099-OID require: "If a person holds more than one discount
obligation, issue a separate Form 1099-OID for each obligation." The single
exception — one form for multiple certificates — applies only where the
certificates are the same issue, held the same amount of time, acquired at the
same time and for the same price, with the same debt elections. Two different
obligations of two different issuers do not qualify, so this taxpayer receives
two statements:

- **Statement 1 — a corporate obligation.** Form 1099-OID reporting **box 1 of
  $400**, the taxable OID accrued for the part of the year the taxpayer held
  it. Box 8 is empty, and the instructions direct that box 1 not include any
  amount reported in box 8.
- **Statement 2 — a U.S. Treasury obligation** acquired at a discount and
  paying semiannual coupons. Form 1099-OID reporting **box 2 of $250**, the
  qualified stated interest paid or credited during the year, and **box 8 of
  $180**, the OID on a U.S. Treasury obligation for the part of the year the
  taxpayer held it. Reporting both on one form for one obligation is what the
  instructions contemplate: "On Form 1099-OID, report the qualified stated
  interest in box 2 and the OID in box 1, 8, or 11, as applicable."

The two boxes the model cannot represent are therefore carried by one
statement about one obligation, not smuggled onto a statement about another.

*Preconditions for publication.* All ten source families are closed: the
1099-OID box 1 family holds the $400 from statement 1, and the other nine are
recorded as closed empty — including the residual `non-form-interest` family.

*A note on that residual closure.* The committed machinery **will accept** it
and publish; that is an operational fact about the engine and is all this case
needs. Whether the closure is also *semantically true* cannot be determined,
because the committed artifacts disagree about the family's predicate. The
`closure_claim` in `packages/content/tax/2025/family.non-form-interest.json`
covers "every interest amount received without a **Form 1099-INT** statement
instance" — a predicate the $250 and $180 satisfy, since they arrive on a Form
1099-OID — while the member fact type
`tax.us.2025.non-form-interest.amount` is titled "Interest income received
without a **Form 1099-INT/OID** statement instance," which excludes them. The
same `closure_claim` then adds that it "says nothing about Form 1099-INT/OID
boxes," which pulls against its own opening predicate.

This case does not resolve that conflict, and no wording chosen here should be
read as resolving it. Under the fact-type reading the closure is true and the
amounts are simply unrepresentable; under the `closure_claim` reading the
closure is false and the user has attested something the model gave them no
way to record. Both readings are available from committed content, which is
itself a finding: a family proposition that two artifacts state differently
cannot be relied on as an attestation of anything precise.

**Expected honest result.** $830 of includible interest — $400 from statement
1, plus $250 and $180 from statement 2. Pub 1212 directs the recipient to
include the OID and qualified stated interest shown in boxes 1, 2, and 8;
§ 61(a)(4) makes the stated interest includible and § 1272(a)(1) makes the
Treasury OID currently includible.

**Current model result — executable given those preconditions.** The only OID
fact types in `packages/content/tax/2025/interest_composition.bundle.json` are
`box1-interest-oid` and `box5-market-discount`. The $250 and the $180 have no
fact type, no family, and no subtotal. They are not blocked, because nothing
requires them; the `oid-subtotal` is $400, all ten closures pass, and
`taxable-total` publishes $400 with disposition `published_value`. The
understatement is $430.

**Defect exposed.** C16 and C17. The failure is not a wrong classification but
an absent one, and the closure machinery conceals it: every family accepts
closure, the model's own consistency checks all pass, and the total is missing
more than half of what the taxpayer's two information returns report between
them.

This is the sharpest available demonstration that closure attests to the
*declared* categories only. The taxpayer holds two statements, has recorded
everything on them that the model can express, has answered every closure
question the engine asked, and is still understated — because each question is
scoped to a family the model defines, and the whole of statement 2 falls
outside every one of them. That second statement is the sharper half of the
case: it is a valid, ordinary Form 1099-OID reporting two boxes, and the model
can record **none** of it.

The residual family is where a reader would expect the shortfall to be caught,
and the predicate conflict noted above is why it is not caught reliably. A
residual category exists to absorb what the enumerated categories miss; this
one cannot do that job while two committed artifacts disagree about what it
covers. Whichever reading is adopted, the $430 has no home — under one it is
excluded by the fact type, under the other it is covered by a claim with no
fact type able to carry it.

**Operationalization.** A test recording statement 2 — a Form 1099-OID
carrying a box 2 and a box 8 amount and no box 1 amount — and asserting that
the workspace can represent it at all. Today there is nothing to record it
into, so the statement is simply unenterable while every closure still passes.
The test presumes box 2 and box 8 fact types exist, so it is a content
addition rather than a contract change.

---

## A16 — Savings bonds previously reported under a § 454 election

**Setup.** The taxpayer bought Series EE bonds in 2005 and elected under
§ 454(a) to report the annual increase in redemption value as it accrued,
reporting it every year since. They redeem in 2025. The Form 1099-INT reports
$9,000 in box 3 — the cumulative interest. $8,100 of it was included in prior
years' returns.

*Preconditions for publication.* All ten source families are closed: the
1099-INT box 3 family holds the single statement above, and the other nine are
closed empty.

**Expected honest result.** $900 is includible in 2025. Pub 550 states the
consequence directly: report the difference between the total interest shown on
Form 1099-INT and the interest previously reported.

**Current model result — executable given those preconditions.** No fact type,
family, subtotal, or adjustment represents a previously reported amount. The
$9,000 enters the total at face value. All ten closures pass and `taxable-total`
publishes $9,000 with disposition `published_value`. The overstatement is
$8,100 — the taxpayer is taxed a second time on twenty years of accrual they
already paid tax on.

**Defect exposed.** C18, and a structural point beyond it. The correction is
*subtractive*, and the line-2b rule's `value` is a single `subtract` node with
three fixed operands — nominee, accrued interest, ABP. There is no slot for
this,
so this is not a missing family that content could supply; it requires changing
the rule's shape. That places it in the same territory as A11, and it is the
second independent case forcing decision D5.

Note also the evidence problem, which is a **routing** problem and not an
epistemic one. The amount is perfectly supportable: it is evidenced by the
taxpayer's filed prior-year returns and by their savings-bond records, and a
preparer would substantiate it exactly that way. What the engine lacks is any
route for that evidence. No fact type represents a prior-year inclusion, no
family would hold it, and no consumer would read it — so the difficulty is
that the model has nowhere to put well-founded evidence, not that the
underlying assertion cannot be checked. That distinction matters for the
repair: the work is representation and consumption, not a policy decision
about trusting unsupported user claims.

**Operationalization.** A test asserting a $900 `taxable-total` from a $9,000
box 3 statement plus an $8,100 previously-reported adjustment. It cannot be
written today at any level: the fact type, the family, and the additional
operand
all do not exist.

---

## What the set is designed to show

The cases are chosen so that the model's checks pass in most of them. A1, A4,
A7, A10, A13, A14, A15, and A16 each state the closure preconditions under
which the engine reaches a `published_value` disposition — every closure
satisfied, every pin resolved, every slot bijection validated — on a wrong or
unsupportable number. Those preconditions are part of each case, not an
assumption behind it: publication requires all ten `require_closed` branches to
pass, so a case that closes one family and says nothing about the other nine has
not demonstrated publication.

A8 is the exception in this group. It reaches its conclusion from a product
direction the committed state does not implement, so it is labelled conceptual
and its consequence is a design consequence rather than an observed one.

That is the shape of the problem. The engine's validation is genuinely good
at the question it asks — does the rule consume exactly what its composition
declares — and that question is orthogonal to whether the declared model
supports the claim being made. A2, A6, and A9 are included precisely because
the model handles them correctly; without them the set would read as a
complaint about the machinery rather than a finding about its scope.

## What the set tests about the architecture

Read as a test of the modeling requirements rather than as a defect list, the
set establishes four things.

**The layer separation is necessary, not decorative.** Every case above is a
specific collapse. A1 collapses layer 2 into layer 4. A4 collapses layer 4 into
layer 5. A7 collapses layer 6 into layer 4. If the layers were an academic
distinction, these cases would not produce different numbers. They do.

**The intensional/extensional split is what makes the failures nameable.** F9
is the largest class, and every case in it is the same shape: a concept that
is perfectly coherent, and a build that covers part of it, with nothing in the
system that records the difference. Without both declarations the failure has
no place to be written down, which is why it is invisible in the output.

**Detectability is the axis that decides severity, not size.** A13 and A1
differ by a few hundred dollars and are both undetectable from the represented
facts; A6 and A9 are handled correctly and would be safe at any magnitude. The
cases that matter are the ones the model cannot see itself failing — which is
consideration 9 of the good-enough framework, arrived at from the other
direction.

**The gap list is a lower bound, and the set proves it on itself.** F5 has no
case. That absence is not evidence that elections are handled; it is evidence
about how much adversarial effort was spent. A set that could certify its own
completeness would be making exactly the mistake the framework forbids.
