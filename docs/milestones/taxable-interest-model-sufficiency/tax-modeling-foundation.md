# Modeling Substantive Tax Concepts: Foundation and Separation of Models

## The question this milestone answers

**How ought this application model substantive tax concepts partially but
defensibly, while keeping evidence, economic facts, tax classification, return
reporting, computation, claims, and presentation distinct?**

Every word of that question is load-bearing.

*Substantive* — the meaning tax law assigns, not the arrangement a form
imposes on it.

*Partially* — no application will model the whole of any tax domain. Partial
coverage is the permanent condition, not a temporary defect to be worked off.

*Defensibly* — partial coverage is acceptable only if the boundary of the
coverage is declared, the claim made is bounded by that declaration, and the
residual risk outside it is characterised rather than assumed away.

*Distinct* — the same money amount travels through every layer below. That
travel is exactly why the layers collapse into one another, and the collapse
is what produces confidently wrong answers.

US-federal taxable interest for 2025 is used throughout this milestone as a
**worked specimen**. It is not the subject. Whether that particular concept is
complete, which categories it omits, and whether it may occupy Form 1040
line 2b are real questions with real answers recorded elsewhere in this
milestone — but they are downstream of, and instances of, the question above.

## Non-goals

This document does not attempt a universal tax ontology, and nothing here
should be read as one. It proposes a separation of concerns tested against a
single concept. It does not select a schema, a citizen kind, a field shape, or
a contract. It does not implement tax rules or add missing categories. Those
are later decisions, and this milestone deliberately declines to prejudge them.

## Eight models, and why they must not collapse

The recurring failure is a **layer collapse**: a fact about a document is
treated as a fact about the taxpayer's tax position; a form line is treated as
the definition of the concept it presents; the fact that a computation ran is
treated as evidence that the concept is correctly modeled.

These eight models must connect. They must not become one model merely because
the same amount passes through them.

### 1. Evidence model

What the taxpayer actually submitted or the application actually holds: a PDF,
a scan, a photograph, a manual entry, a broker download, a corrected copy of a
document already held.

Evidence is *material*. It has custody, provenance, a receipt time, and a
relationship to other material — but it asserts nothing by itself. Two scans of
one statement are two pieces of evidence about one reported fact. A corrected
Form 1099-INT is evidence that supersedes, not a second income item.

The evidence model's job is to know what is held, where it came from, and what
it is evidence *of*. It must not be the identity of anything downstream. If a
reported fact's identity derives from the file it arrived in, re-scanning
creates phantom income.

### 2. Reported-fact model

What a document says: *"the logical 2025 Form 1099-INT furnished by this payer
reports $X in box 1."*

This is a fact about a **statement**, not about the taxpayer. The logical
statement is peer to evidence rather than derived from it: one statement may be
supported by an original, a correction, and a re-scan, and its identity must
come from the payer, the statement, and the tax year — never from a file.

A reported figure is a third party's report of what it believes it paid. It is
very often equal to the taxpayer's includible amount, and that frequent
coincidence is exactly why the two are so easily conflated. The reported-fact
model must be able to represent a reported amount that is *not* the includible
amount without being incoherent.

### 3. Economic and circumstantial fact model

What actually happened in the world, independent of any document:

- Interest was received; interest accrued.
- The taxpayer bought a bond between interest dates and paid the seller
  accrued interest belonging to the seller.
- An amount was received as a nominee and belongs to another person.
- A bond was bought at a premium and the payer did not net the amortisation.
- Series EE/I bonds were redeemed and qualified higher education expenses were
  paid in the same year, with no competing education credit or tax-favoured
  distribution claiming those same expenses.
- An election was made — for example, to include market discount currently.

These facts determine the tax answer and, critically, **several of them cannot
be recovered from a form-box amount at all**. A box 1 figure does not disclose
whether part of it belonged to a nominee. A box 3 figure does not disclose
whether the redemption qualified for an education exclusion.

This is the layer that separates a document-transcription product from a tax
product. An application that has only layers 1, 2, and 5 can transcribe forms
accurately and still be systematically wrong about tax.

### 4. Substantive tax model

What the law makes of those facts: whether an amount is includible in gross
income, excluded, adjusted, allocated to a different person, assigned to a
different period, or made contingent on an election or an open fact.

This is the layer where the meaning lives. Statutory includibility questions
belong here regardless of which form happens to disclose them. Where the
authority leaves a judgment, or requires a fact the application does not
represent, the judgment or the open fact must be **identified** — computation
must never silently pick a branch.

A model that simply sums whatever it happens to have recorded has made a
substantive classification decision — *"everything recorded is includible and
nothing unrecorded exists"* — without declaring it, and usually without
noticing it.

The substantive tax model is **intensional**: it says what the concept *means*
and what it ranges over. It is not the same thing as what the engine can
compute, which is layer 6.

### 5. Reporting model

How the tax system requires the substantive result to be arranged, disclosed,
itemised, sequenced, and carried: which line, on which form, in which order,
subject to which attachment and disclosure thresholds.

Reporting mechanics are genuine requirements with genuine authority. They are
not the definition of the underlying concept. A subtraction that appears as a
row on a schedule may be either (a) a substantive reduction that the schedule
merely *discloses*, or (b) a purely presentational arrangement. Those are
different, and the reporting model must not be where that difference is
decided.

The reporting model verifies a **correspondence**: that the concept the
application computed is the concept the official line names. It cannot supply
substance the substantive model is missing.

### 6. Execution model

What this application can actually run: the rules that exist, the inputs they
consume, the categories they range over, the guards that block, the values they
publish, and the conditions under which they refuse.

The execution model is **extensional**. It is a coverage profile over the
intensional concept in layer 4 — the subset of the concept's universe that this
build can actually decide. It is versioned, it changes with every content
release, and it is the only layer that can be mechanically verified.

Two properties are routinely confused here and must be kept apart:

**Internal coextensiveness.** Does the rule consume exactly the slots its
composition declares — no omission, duplication, substitution, or extra? This
is a mechanical property of artifacts, and it can be validated automatically.

**External sufficiency.** Do the declared slots, taken together, support the
concept the output claims? This is a question about the relationship between
the declared model and the law. No amount of slot bookkeeping answers it.

A composition can be perfectly closed over three slots and be a wholly
inadequate model of the concept it names. Internal closure is necessary and
nowhere near sufficient. **This is the central finding of the milestone.**

### 7. Claim and standing model

What a statement of the application's actually covers, and how far it reaches.

A number computed is not a statement made. The same computed figure honestly
supports *"the interest amounts recorded here sum to $X"* and does not support
*"your 2025 taxable interest is $X"*, and the difference is not in the
arithmetic. How far a statement reaches depends on the coverage profile in
layer 6, on the authority examined in the coverage method, and on what the user
has said about their own records — three independent inputs, none of which
substitutes for another.

This layer's job is to know the scope of what is being said and to say it. Its
failure mode is not modesty. It is a statement whose apparent reach exceeds
what the modeling underneath it covers.

This layer is also where the milestone's forward question lands: the distance
between what a statement reaches and what the product would like it to reach is
a modeling specification, developed in
[claim-boundaries-and-modeling.md](claim-boundaries-and-modeling.md).

### 8. Explanation and presentation model

How the result, its derivation, its authority, its bounds, and its residual
uncertainty are shown to a human.

Explanation is downstream of scope, not a substitute for it. A prose
disclaimer beneath a number does not change what asserting the number means. A
citation displayed next to a figure does not establish that the cited authority
governs the proposition the figure asserts.

Presentation is also where the layer collapse becomes visible to the user, and
therefore where its cost is paid.

## The chain

The layers connect in one direction:

> evidence → reported and economic facts → substantive tax classifications and
> derived tax concepts → reporting calculations and form bindings → return
> representation → explanation and claim scope

Three things about this chain matter more than the sequence.

**Information is added, not just transformed.** Between layers 2 and 4 the
application must acquire circumstantial facts that no document supplies. A
chain that only transforms document contents cannot reach a correct
substantive result except by luck — specifically, by the luck of the taxpayer
having no circumstance the documents fail to disclose.

**The chain narrows the claim, it does not strengthen it.** Each layer can
only lose support. Arriving at layer 8 with a well-formatted number does not
recover substance that was never established at layer 4.

**Failure at a high layer does not invalidate the low ones.** When the
substantive model is insufficient, the reported-fact claims and the
recorded-aggregate claims remain fully available and fully honest. The
product's fallback is not "show nothing." It is *"make the strongest claim
that is actually supported, and say which claim it is."*

## The collapse catalogue

Each of these is a specific way two layers merge. Each has been observed in the
worked specimen.

| Collapse | What it looks like | What goes wrong |
| --- | --- | --- |
| Evidence into reported fact | A statement's identity derives from the file it arrived in | Re-scans and corrections become duplicate income |
| Reported fact into economic fact | A box amount is treated as what happened | Nominee, premium, and accrual circumstances vanish |
| Reported fact into substantive result | A box amount is treated as includible income | Reported ≠ includible cases are silently wrong |
| Economic fact into substantive result | Recording an item is treated as classifying it | Undeclared classification: "recorded means includible" |
| Substantive model into reporting model | A statutory exclusion is modeled as a schedule row | The law's operation is decided by form layout |
| Reporting model into substantive model | The form line's meaning defines the concept | The concept cannot exist when no form is required |
| Execution model into substantive model | "The rule ran and validated" is read as "the concept is right" | Internal closure mistaken for legal sufficiency |
| Execution model into claim model | Publishing a value is treated as the value meaning what its name says | Bounded results rendered in unbounded positions |
| Claim model into presentation | A disclaimer is treated as bounding the claim | The assertion is made anyway, then hedged |

The single most expensive item in that table is the last row of the execution
group. **The costly mistake is not producing a bounded result. It is rendering
a bounded result in a position that means something unbounded.**

## What follows from this foundation

Three consequences shape the rest of this milestone.

1. Because layers 4 and 6 are different, an application needs *two* artifacts
   about its own model: what the concept means, and what this build covers.
   That distinction is developed in
   [concept-coverage-and-claims.md](concept-coverage-and-claims.md).

2. Because substance and reporting are different, authority must be recorded
   at the level of the **proposition** it supports, with its class, and not as
   a decorative citation on a rule. That is developed in
   [authority-model.md](authority-model.md).

3. Because these are modeling requirements rather than a list of missing
   features, they must be tested by cases designed to break the *architecture*,
   not by an inventory of uncovered categories. That is
   [taxable-interest-adversarial-cases.md](taxable-interest-adversarial-cases.md).

Assessment of what the current engine does, and of the shapes a future
representation might take, is deliberately last. It is downstream of this
foundation, and it must not be allowed to run backwards — the question is not
what the existing schemas can express.
