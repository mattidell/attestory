# US-Federal Taxable Interest for 2025: The Derived Concept

## What this document is

This document establishes what the symbol `tax.us.2025.interest.taxable-total`
would have to *mean* for the product to publish it honestly, independently of
whatever the engine currently computes. It is the semantic reference for the
worked concept. Coverage evidence is in
[taxable-interest-authority-and-coverage.md](taxable-interest-authority-and-coverage.md);
the verdict on the current engine is in
[taxable-interest-sufficiency-assessment.md](taxable-interest-sufficiency-assessment.md).

The scope is deliberately narrow: US federal individual income tax, tax year
2025, taxable interest, Form 1040 line 2b. Nothing here generalises to other
income types, other forms, other years, other taxpayers, or other
jurisdictions. Where this document describes a structure that *looks* general
— the layer separation, the claim ladder — that structure is offered as a
prototype tested against one concept, not as a ratified product vocabulary.

## The concept has an identity independent of the form line

"US-federal taxable interest for this taxpayer for 2025 is $X" is a
proposition about a taxpayer and a tax year. It is true or false before any
form is filled in, and it remains the same proposition whether or not
Schedule B is required, whether or not Schedule B is attached, and whether or
not a return is ever filed.

This matters because the engine currently has no artifact whose subject is
that proposition. It has a rule that publishes a symbol, and a form field
that binds the symbol to line 2b. The concept's identity is therefore
recoverable only by reading the rule and the form field together and
inferring what they jointly intend. That inference is exactly what this
milestone exists to stop relying on.

To be a *declared* concept rather than an inferred one, the following must be
recoverable without private convention:

| Attribute | For this concept |
| --- | --- |
| Subject | The return subject (taxpayer) of the workspace |
| Jurisdiction | US-federal |
| Tax year | 2025 |
| Tax regime | Individual income tax |
| Quantity | A money amount in US dollars |
| Meaning | Interest includible in gross income for 2025 under the federal individual income tax, after the reductions the authority directs |
| Authority basis | Which sources establish that meaning, and of what class |
| Modeled universe | Which categories the adopted model actually represents |
| Known exclusions | Which categories are deliberately outside the model |
| Known unsupported categories | Which categories are materially relevant but not represented |
| Derivation | The rule that produces the value |
| Presentation bindings | Form 1040 line 2b; Schedule B Part I |
| Official-line eligibility | Whether the result may occupy line 2b |

The "Meaning" row rests on § 61(a), which defines gross income as "all income
from whatever source derived, including (but not limited to) the following
items", enumerating "Interest" at § 61(a)(4). The reductions the concept must
honour are likewise statutory where they exist — § 135(a) for qualifying
redeemed savings bonds, § 1272(a)(7) for acquisition premium — rather than
artifacts of the form on which they happen to be reported.

Of these thirteen, the current artifacts carry subject (implicitly, via the
workspace), jurisdiction, tax year, regime, derivation, and presentation
bindings. Quantity is carried but semantically empty. Meaning, authority
basis, modeled universe, known exclusions, known unsupported categories, and
official-line eligibility are not carried by any artifact. That analysis is
developed in
[derived-tax-concept-declaration.md](derived-tax-concept-declaration.md).

## Seven layers that must not collapse

The recurring failure this milestone addresses is a layer collapse: a fact
about a document is treated as a fact about the taxpayer's tax position, or a
form line is treated as the definition of the concept it presents.

### 1. Evidence

A Form 1099-INT, a Form 1099-OID, a Schedule K-1, a brokerage substitute
statement, a bank statement, or a PDF the user uploaded. Evidence is the
material submitted.

### 2. Reported facts

"This logical 1099-INT statement, furnished by this payer for 2025, reports
$X in box 1." This is a fact about a *statement*, not about the taxpayer's
taxable income. A logical statement is peer to evidence: one statement may be
supported by an original PDF, a corrected copy, and a re-scan, and its
identity must not derive from any of them. The engine models this correctly
— `tax.us.2025.f1099int.box1-interest` in
`packages/content/tax/2025/f1099int.bundle.json` is keyed on `payer`,
`statement`, and `tax-year`, with no file, upload, scan, document, or
evidence key.

A reported fact is not a tax conclusion. A payer's box 1 figure is the
payer's report. It is very often equal to the taxpayer's includible amount,
and that frequent coincidence is precisely why the two are so easily
conflated.

### 3. Economic and circumstantial facts

"Interest was received or accrued." "The taxpayer bought this bond between
interest dates and paid the seller accrued interest." "This amount belonged
to another person and the taxpayer received it as a nominee." "The taxpayer
made a section 1278(b) election to include market discount currently." "The
taxpayer cashed Series I bonds and paid qualified higher education expenses."
"The bond was bought at a premium and the payer did not net the
amortisation."

These are facts about the world, not about a document. Several of them
determine the tax answer and *cannot be recovered from a form-box amount
alone*. A box 1 figure does not disclose whether part of it belonged to a
nominee. A box 3 figure does not disclose whether the taxpayer qualifies for
the Series EE/I education exclusion. This is the layer where the current
model is thinnest.

### 4. Tax classification

Adopted rules decide whether and how an underlying circumstance enters the
US-federal taxable-interest concept for 2025: included, excluded, adjusted,
deferred, or blocked pending an open fact.

Where the authority leaves a judgment, or requires information the workspace
does not represent, the open fact or judgment must be *identified*.
Computation must not silently pick one branch. A model that simply sums what
it happens to have recorded has made a classification choice — "everything
recorded is includible, nothing unrecorded exists" — without declaring it.

### 5. Composition, and the two coextensiveness questions

The model combines included categories, exclusions, and adjustments. Two
distinct questions arise, and conflating them is the central defect this
milestone names.

**Internal coextensiveness.** Does the rule consume exactly the slots its
composition declares — no omission, no duplication, no substitution, no
extra? This is a mechanical property of artifacts and can be validated.

**External tax-model sufficiency.** Do the declared slots, taken together,
support the complete tax concept the output claims? This is a question about
the relationship between the declared model and the law. No amount of slot
bookkeeping answers it.

A composition can be perfectly closed over three slots and still be a wholly
inadequate model of taxable interest. Internal closure is necessary and not
remotely sufficient.

### 6. Derived tax concept

The proposition itself. It need not be asserted by the user; it may be
derived from current findings through adopted rules. Its identity does not
come from line 2b.

### 7. Presentation

Form 1040 line 2b and Schedule B Part I present, itemise, and carry the
derived result. Schedule B is reporting and attachment machinery: it exists
to disclose and to itemise, and its own existence is conditional. Taxable
interest exists as a tax concept whether or not Schedule B is required and
whether or not it is attached.

Schedule B is not the owner of taxable interest, and there is no "Schedule B
document family." Schedule B is generated return material, not submitted
source evidence. Its interest rows, its dividend rows, its foreign-account
question, its foreign-trust question, its attachment trigger, and its
completeness requirements are separate concepts that happen to share a form.

## Two independent support requirements

An exhaustive-total claim needs two supports, and neither substitutes for the
other. This distinction is carried forward from the workspace-completeness
work and is assumed here, not re-derived.

**Workspace-record sufficiency.** The user authorises the application to
treat the facts currently represented in the workspace as the exhaustive
input universe for the calculation, or supplies narrower family-level
confirmations. This is the user's authority: only the user knows what they
have.

**Tax-model sufficiency.** The application's adopted vocabulary,
classifications, rules, exclusions, adjustments, and compositions support the
exact tax concept the product claims to calculate. This is the product's
responsibility: the user is in no position to certify it and must never be
asked to.

These two are supported by different machinery, and only one of them is built.

**What family closure actually says.** The engine's committed mechanism is
family-scoped: closing a source family affirms *that family's declared
proposition* and nothing wider. Closing the Form 1099-INT box 1 family says
"every box 1 amount I hold is recorded." It does not say "every interest
amount I hold is recorded," and it cannot, because the proposition it affirms
is written in the vocabulary of the model being assessed. Amounts arising on
forms, boxes, or circumstances the model does not represent fall outside every
declared proposition, so no combination of family closures reaches them.

It follows that a user who closes all ten families has **not** said "I have
given you everything I have." They have said ten narrower things. The gap
between the conjunction of those ten statements and the broader one is exactly
the set of unrepresented categories, which is why closure completeness cannot
be evidence of model completeness — and why a user who closes every family can
still be understated, as the OID case demonstrates.

**Standing workspace authorization** — a single global act by which the user
authorises the whole workspace as the exhaustive input universe — would be the
mechanism that supports the broader statement. It is a selected product
direction. It is **not committed machinery**: no act performs it, no
marshaller accepts it, no closure producer emits it, and no evaluator consumes
it. Statements below about what such an authorization would license are
statements about a prospective design, and are marked as such.

Even with that authorization built, it would license only the
workspace-record half. Tax-model sufficiency would remain the product's
burden, unaffected by anything the user attests.

## The claim ladder

Six levels, developed as an analytical prototype to expose where standing
changes. These labels are not proposed as final product vocabulary. Their
value is that each rung fails for a different reason, and a lower rung
frequently survives when a higher one does not.

### Level 1 — Source-report claim

*"This 2025 Form 1099-INT from this payer reports $X in box 1."*

Supported by the statement itself. Requires no model coverage beyond the
ability to represent that box, and no workspace completeness authorisation
whatsoever. Unsupported neighbouring inference: that $X is includible in the
taxpayer's income; that this is the only statement from this payer.

### Level 2 — Recorded-items aggregate

*"The interest amounts currently recorded in this workspace sum to $X."*

Supported by the workspace record. Requires no completeness authorisation,
because the claim is explicitly about what is recorded, not about what
exists. Unsupported neighbouring inference: that nothing is missing; that the
sum is a tax result.

### Level 3 — Result over the model's declared categories

*"Over the categories this model declares, the 2025 total is $X."*

Requires internal coextensiveness (the rule consumes exactly the declared
slots) and workspace support for each declared family. Does **not** require
external tax-model sufficiency, because the claim is explicitly bounded by
the model's own declared universe. Unsupported neighbouring inference: that
the declared categories are the legally relevant ones.

This rung is only honest if the declared universe is legible to the reader.
A bounded claim whose bound is not stated is not a bounded claim.

### Level 4 — Derived tax-concept result

*"US-federal taxable interest for this taxpayer for 2025 is $X."*

Requires external tax-model sufficiency **and** workspace-record sufficiency.
This is the first rung that asserts something about the taxpayer's tax
position rather than about the model or the record. Unsupported neighbouring
inference: that this amount is what belongs on a specific form line.

**This rung already carries the whole tax substance.** Anything controlling
law makes determinative of *whether an amount is includible in gross income*
belongs here, not above. § 135(a) provides that "no amount shall be includible
in gross income" for qualifying redeemed savings bonds; it operates on gross
income, not on a form. A level-4 result that has not applied the § 135
exclusion is therefore not a correct level-4 result. The same holds for the
§ 454 previously-reported amount, which was included in an earlier year and is
not includible in this one.

### Level 5 — Official form-line binding

*"Form 1040 line 2b is $X."*

Requires level 4, plus that the concept the engine computed is the concept the
form line names, plus any form-specific ordering and presentation the
authority imposes. Level 5 *verifies a correspondence*; it does not supply tax
substance that level 4 is missing. Schedule B's line 2 / line 3 / line 4
sequence is the reporting arrangement of the § 135 exclusion — the place the
subtraction is disclosed and evidenced on Form 8815 — but the exclusion itself
already belongs to level 4.

**The engine fails at level 4, before the official-line binding is reached.**
A model with no representation of the § 135 exclusion cannot state US-federal
taxable interest correctly for a taxpayer who qualifies, whatever form line
the result is later bound to. The level-5 failure is real but consequent: the
value bound to line 2b is wrong because the level-4 concept beneath it is
wrong. Reading the defect as purely a form-ordering problem understates it,
because it suggests a presentation fix would suffice.

### Level 6 — Filed representation

*"This is what the taxpayer reported to the IRS."*

Requires level 5 plus a filing act. Filing is separate from calculation
authorisation and is out of scope here.

### What the ladder buys

Failure at a higher rung does not invalidate lower rungs. When external
tax-model sufficiency is absent, levels 1, 2, and 3 remain fully available
and fully honest. The product's fallback is therefore not "show nothing" — it
is "show the strongest rung that is actually supported, and name the rung."

The costly mistake is not stopping at level 3. It is rendering a level-3
result in a level-5 position.

## Explicitly unresolved semantic questions

These are open. This document does not decide them.

1. **Should the model name a pre-exclusion intermediate?** Schedule B
   distinguishes line 2 (the sum of listed interest, after nominee,
   accrued-interest, ABP, OID, and previously-reported adjustments) from line 4
   (line 2 minus the § 135 exclusion). Only line 4 goes to Form 1040 line 2b.
   The product may decide whether to model a distinct pre-exclusion quantity
   corresponding to line 2 — useful for tie-outs and for explaining the
   arithmetic to a reader — or to model only the final concept and derive the
   display rows from it.

   What is **not** open is whether the final taxable-interest concept includes
   the § 135 exclusion. It does. § 135(a) governs includibility in gross
   income, so controlling law settles it, and the question here is one of
   intermediate representation only.

2. **What is the subject when a return is joint?** The concept is stated
   above as being about "the return subject." Whether taxable interest is a
   property of a person, of a married couple, or of a return is not settled
   by anything examined here.

3. **What does "received or accrued during 2025" pin to?** The line-2b
   instruction phrase covers both cash receipt and accrual. Which economic
   fact the model treats as the includible event — and whether that differs
   by category — is not declared anywhere.

4. **Where is a substantive subtraction implemented?** Nominee distributions
   reduce the taxpayer's includible interest as a matter of substance: the
   money was someone else's. The § 135 exclusion is more clearly substantive
   still — § 135(a) provides that "no amount shall be includible in gross
   income" — and the § 454 previously-reported amount is substantive for the
   same reason, since it was already included in an earlier year. Yet all of
   them are currently expressed, where expressed at all, as Schedule B row
   mechanics.

   The open question is one of **implementation locality**: whether such a
   subtraction is a signed constituent of the composition, a separate rule
   feeding the concept, or a derived value the concept consumes — and which
   artifact kind carries it. That is a real architectural choice with real
   consequences, and it is the most consequential one found.

   The open question is **not** whether these amounts affect current-year
   taxable interest. They do, by operation of statute. The engine's current
   shape — Schedule B rows that happen to change line 2b — is a defensible
   place to *implement* the subtraction and an indefensible place to *decide*
   whether it happens.

5. **Can a form-field description honestly narrow an official-line claim?**
   That is, if a field bound to line 2b carries prose saying "this covers
   only these seven families," does the narrowing bind the claim, or does
   occupying the line adopt the line's official meaning regardless? This is
   put to the owner as a decision in
   [taxable-interest-sufficiency-assessment.md](taxable-interest-sufficiency-assessment.md).

6. **What is a "quantity"?** The engine's quantity vocabulary is a list of
   bare strings. Whether a quantity is a unit, a dimension, a tax concept, or
   a de-duplication key is not declared, and the artifact for this concept
   groups `taxable-interest` and `wages` into one vocabulary citizen.
