# Worked Semantic Example: US-Federal Taxable Interest for 2025

## What this document is

This is the **worked specimen** for the modeling architecture set out in
[tax-modeling-foundation.md](tax-modeling-foundation.md) and
[concept-coverage-and-claims.md](concept-coverage-and-claims.md). Its purpose
is to show that the architecture survives contact with a real tax concept, and
to expose the places where it strains.

Taxable interest is a good specimen precisely because it looks easy. It is a
single money amount, reported on familiar forms, that most taxpayers can read
off a statement. If the layer separation is unnecessary anywhere, it is
unnecessary here — and it turns out not to be.

The scope is narrow on purpose: US federal individual income tax, tax year
2025, taxable interest, Form 1040 line 2b. Nothing here generalises to other
income types, forms, years, or jurisdictions. What generalises is the
*structure*, and it does so as a prototype tested against one concept, not as
a ratified product vocabulary.

## The intensional model for this concept

*"US-federal taxable interest for this taxpayer for 2025 is $X"* is a
proposition about a taxpayer and a tax year. It is true or false before any
form is filled in, and it remains the same proposition whether or not
Schedule B is required, whether or not Schedule B is attached, and whether or
not a return is ever filed.

For that proposition to be **declared** rather than inferred from whatever the
code happens to do, the following must be recoverable without private
convention:

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
honour are statutory where they exist — § 135(a) for qualifying redeemed
savings bonds, § 1272(a)(7) for acquisition premium — rather than artifacts of
the form on which they happen to be reported.

Note what the table does **not** contain: any reference to what the current
engine can compute. That is deliberate, and it is the ordering discipline the
whole milestone rests on. The intensional model is written from authority; the
coverage profile is measured against it afterwards. Written the other way
round, the model becomes "whatever we implemented" and is sufficient by
construction.

## The eight layers, instantiated

The generic layers are defined upstream. Here is what each one contains for
this concept, and what collapses into what when it is not kept separate.

**1. Evidence.** A Form 1099-INT PDF, a Form 1099-OID, a Schedule K-1, a
brokerage substitute statement, a bank statement, a re-scan, a corrected copy.

*Collapse risk:* if a reported fact's identity derives from the file, a
corrected 1099-INT becomes a second income item. The engine models this
correctly — `tax.us.2025.f1099int.box1-interest` is keyed on `payer`,
`statement`, and `tax-year`, with no file, upload, scan, document, or evidence
key.

**2. Reported facts.** *"This logical 1099-INT statement, furnished by this
payer for 2025, reports $X in box 1."* A fact about a statement.

*Collapse risk:* the box 1 figure is very often equal to the includible amount,
and that frequent coincidence is exactly why the two get conflated. The cases
where they differ are the interesting ones, and they are invisible from the box.

**3. Economic and circumstantial facts.** Interest was received or accrued. The
taxpayer bought a bond between interest dates and paid the seller accrued
interest. An amount was received as a nominee and belongs to another person.
The taxpayer made a § 1278(b) election. Series EE/I bonds were redeemed and
qualified higher education expenses were paid, with no education credit and no
tax-favoured distribution claiming the same expenses. A bond was bought at a
premium and the payer did not net the amortisation.

*Collapse risk:* several of these **cannot be recovered from a form-box amount
at all**. A box 1 figure does not disclose a nominee portion. A box 3 figure
does not disclose education-exclusion eligibility. This is the thinnest layer
in the current model, and its thinness is not visible from any output.

**4. Substantive tax model.** Whether an amount is includible, excluded,
adjusted, reallocated, moved between periods, or made contingent on an election
or an unrepresented fact.

*Collapse risk:* a model that sums what it happens to have recorded has decided
*"everything recorded is includible and nothing unrecorded exists"* without
declaring it.

**5. Reporting model.** Form 1040 line 2b and Schedule B Part I present,
itemise, and carry the result. Schedule B's line 2 / line 3 / line 4 sequence
is the *reporting arrangement* of the § 135 exclusion — the place the
subtraction is disclosed and evidenced on Form 8815.

*Collapse risk:* Schedule B is not the owner of taxable interest, and there is
no "Schedule B document family." It is generated return material, not
submitted source evidence. Its interest rows, dividend rows, foreign-account
question, foreign-trust question, attachment trigger, and completeness
requirements are separate concepts that happen to share a form. Taxable
interest exists whether or not Schedule B is required.

**6. Execution model.** The committed rule, its composition slots, its guards,
and the validator behaviour around them.

*Collapse risk:* the whole finding of this milestone. Internal coextensiveness
— the rule consumes exactly its declared slots — is real, checkable, and
completely silent on legal relevance. A composition perfectly closed over its
declared slots can be a wholly inadequate model of taxable interest.

**7. Claim and standing.** Which rung of the ladder this build is entitled to.

**8. Explanation and presentation.** How the figure, its derivation, its
bounds, and its residual uncertainty reach a reader.

## The claim ladder for this concept

The generic ladder is in
[concept-coverage-and-claims.md](concept-coverage-and-claims.md). Instantiated:

| Rung | For taxable interest | Currently supported? |
| --- | --- | --- |
| 1 — source report | "This 2025 Form 1099-INT from this payer reports $X in box 1" | Yes |
| 2 — recorded aggregate | "The interest amounts recorded in this workspace sum to $X" | Yes |
| 3 — declared categories | "Over the categories this model declares, the 2025 total is $X" | Yes, if the declared universe is stated to the reader |
| 4 — derived tax concept | "US-federal taxable interest for this taxpayer for 2025 is $X" | **No** |
| 5 — official line | "Form 1040 line 2b is $X" | No, consequent on 4 |
| 6 — filed | "This is what the taxpayer reported" | Out of scope |

**The engine fails at level 4, before the official-line binding is reached.**
This is the single most important structural fact in the specimen, and it is
easy to state wrongly.

§ 135(a) provides that "no amount shall be includible in gross income" for
qualifying redeemed savings bonds. It operates on gross income, not on a form.
A model with no representation of that exclusion therefore cannot state
US-federal taxable interest correctly for a taxpayer who qualifies, **whatever
form line the result is later bound to**. The § 454 previously-reported amount
is substantive for the same reason: it was included in an earlier year and is
not includible in this one.

The level-5 failure is real but consequent — the value bound to line 2b is
wrong because the level-4 concept beneath it is wrong. Reading the defect as a
form-ordering problem understates it, because it implies a presentation fix
would suffice.

The corresponding good news is that levels 1 through 3 remain fully available
and fully honest. The product's fallback is not "show nothing."

## Two supports, one of which is not the user's to give

An exhaustive-total claim needs two independent supports.

**Workspace-record sufficiency** is the user's authority: only the user knows
what records they hold. The mechanism for this, its scope, and its limits were
settled in earlier work and are assumed here, not re-derived or reopened.

**Tax-model sufficiency** is the product's responsibility: whether the adopted
vocabulary, classifications, rules, exclusions, adjustments, and compositions
support the exact tax concept the product claims to calculate.

The only point this milestone needs from the pairing is the asymmetry:

> **The user is in no position to certify tax-model sufficiency and must never
> be asked to.** No user attestation, however broad, converts an insufficient
> model into a sufficient one. Whatever the user authorises about their own
> records leaves the product's burden exactly where it was.

That is the whole of what the specimen needs from this topic. The mechanics of
record authorisation are outside this milestone.

## Where the architecture strains

Six semantic questions arose that the layer separation surfaces but does not
answer. They are recorded as open. This document does not decide them, and none
of them is a schema question.

1. **Should the model name a pre-exclusion intermediate?** Schedule B
   distinguishes line 2 (listed interest after nominee, accrued-interest, ABP,
   OID, and previously-reported adjustments) from line 4 (line 2 minus the
   § 135 exclusion). Only line 4 reaches Form 1040 line 2b. The product may
   model a distinct pre-exclusion quantity — useful for tie-outs and for
   explaining the arithmetic — or model only the final concept and derive the
   display rows from it.

   What is **not** open is whether the final concept includes the § 135
   exclusion. It does; § 135(a) governs includibility in gross income, so
   controlling law settles it. The question is intermediate representation only.

2. **What is the subject when a return is joint?** Whether taxable interest is
   a property of a person, of a married couple, or of a return is not settled
   by anything examined here.

3. **What does "received or accrued during 2025" pin to?** The line-2b
   instruction phrase covers both cash receipt and accrual. Which economic
   event the model treats as includible — and whether it differs by category —
   is not declared anywhere.

4. **Where is a substantive subtraction implemented?** Nominee distributions
   reduce includible interest as a matter of substance: the money was someone
   else's. The § 135 exclusion is more clearly substantive still. The § 454
   previously-reported amount likewise. Yet all of them are currently
   expressed, where expressed at all, as Schedule B row mechanics.

   The open question is **implementation locality**: whether such a subtraction
   is a signed constituent of the composition, a separate rule feeding the
   concept, or a derived value the concept consumes. That is a real
   architectural choice and the most consequential one found.

   The open question is **not** whether these amounts affect current-year
   taxable interest. They do, by operation of statute. The engine's current
   shape is a defensible place to *implement* the subtraction and an
   indefensible place to *decide* whether it happens.

5. **Can a form-field description honestly narrow an official-line claim?** If
   a field bound to line 2b carries prose saying "this covers only these seven
   families," does the narrowing bind the claim, or does occupying the line
   adopt the line's official meaning regardless? This is a claim-standing
   question, not a presentation one, which is why it is hard.

6. **What is a "quantity"?** The engine's quantity vocabulary is a list of bare
   strings. Whether a quantity is a unit, a dimension, a tax concept, or a
   de-duplication key is not declared, and the artifact for this concept groups
   `taxable-interest` and `wages` into one vocabulary citizen.

Questions 1, 3, 4, and 6 are all instances of the same underlying gap: the
application has no artifact whose subject is the *concept*. It has a rule that
publishes a symbol and a form field that binds the symbol to a line, and the
concept's identity is recoverable only by reading the two together and
inferring what they jointly intend. Ending that reliance on inference is what
the architecture above is for.
