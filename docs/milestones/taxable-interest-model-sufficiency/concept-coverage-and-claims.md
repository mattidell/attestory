# Concept, Coverage, and Claim: The Three Things That Must Not Be One Thing

## Why this document exists

[tax-modeling-foundation.md](tax-modeling-foundation.md) separates eight
models. This document develops the distinction that does the most work among
them, and then gives the framework for judging whether partial coverage is good
enough.

The distinction is between three things that an application is constantly
tempted to treat as one:

| | What it is | What kind of thing | Who is responsible |
| --- | --- | --- | --- |
| **Intensional concept model** | What the tax concept *means* and what it ranges over | A statement about the law | The product |
| **Executable coverage profile** | What *this build* can actually decide, and where it stops | A statement about the artifacts | The product |
| **Claim scope** | What a statement actually covers, and in what position it is read | A statement about reach | The product |

A single money amount can be simultaneously produced by a coverage profile,
correct within it, and still not a statement of the concept. Nothing
about the number reveals which of the three is in play. Only the surrounding
declarations do.

## 1. The intensional concept model

The intensional model answers *"what would have to be true for this figure to
be the thing we are naming?"*

It is written in the vocabulary of tax law, not of the application. It exists
before any rule is authored and survives every refactor. It states:

- the **subject** the concept is about, and the **period** and **regime**
- the **proposition** the concept asserts, in the law's own terms
- the **universe** the concept ranges over — everything the law would count,
  including things the application cannot currently handle
- the **operations** the law directs on that universe: inclusion, exclusion,
  allocation, timing, election-contingency
- the **authority** that establishes each of the above, at proposition level

The universe is the crucial part, and the easiest to get wrong. It is *the
law's* universe, not the application's. A model whose declared universe is
"the categories we implemented" has quietly redefined the concept to be
whatever it computes, which makes it trivially sufficient and completely
uninformative.

Writing the intensional model down is what makes a gap *visible as a gap*
rather than as an absence nobody can see.

## 2. The executable coverage profile

The coverage profile answers *"which parts of that universe can this build
actually decide, and what does it do at the edges?"*

It is extensional, mechanical, and versioned. It changes with content
releases. Unlike the intensional model, it can be checked against the
artifacts.

For each region of the concept's universe the profile records a status. This
milestone uses a **closed** status vocabulary; a case that does not fit an
existing term is a finding about the vocabulary, not a licence to invent a
term:

- **represented and supported** — the circumstance is modeled and the model
  produces the legally correct result
- **represented but semantically collapsed** — something is recorded, but a
  distinction the law makes is not preserved
- **represented but requiring judgment** — the inputs exist; the law leaves a
  determination the application does not make
- **bounded exclusion** — deliberately outside the model, declared as such
- **unsupported and blocking** — not modeled, and the application refuses to
  produce a result rather than guessing
- **unsupported but currently silently omitted** — not modeled, and the
  application produces a result anyway
- **outside the declared authority boundary** — beyond the jurisdiction,
  period, or regime the model claims

The vocabulary's whole point is the difference between the fifth and sixth
entries. *Unsupported and blocking* is a bounded product. *Unsupported but
silently omitted* is an undetected wrong answer. They are indistinguishable
from the output and opposite in consequence.

Two properties of the profile must be kept apart, because conflating them is
how internal rigour gets mistaken for legal adequacy:

**Internal coextensiveness** — the rule consumes exactly the slots its
composition declares. Mechanically checkable. Necessary.

**External sufficiency** — the declared slots support the concept the output
names. Not mechanically checkable by any amount of slot bookkeeping. Not
implied by internal coextensiveness at any level of rigour.

## 3. Claim scope

Claim scope answers *"given this concept and this coverage, what does a
statement of ours actually cover?"*

Statements form a ladder. Each rung requires something different of the
modeling, and — this is the useful part — **a lower rung frequently holds when
a higher one does not**. The labels below are an analytical prototype for
exposing where the modeling requirement changes, not a proposed product
vocabulary.

### Level 1 — Source-report claim

*"This statement, furnished by this payer for this year, reports $X in this
box."*

Supported by the statement itself. Needs no model coverage beyond the ability
to represent that box, and no completeness authorisation at all.

Unsupported neighbour: that $X is includible; that this is the only statement
from this payer.

### Level 2 — Recorded-items aggregate

*"The amounts of this kind currently recorded here sum to $X."*

Supported by the record. Needs no completeness authorisation, because the claim
is explicitly about what is recorded rather than what exists.

Unsupported neighbour: that nothing is missing; that the sum is a tax result.

### Level 3 — Result over the model's declared categories

*"Over the categories this model declares, the total is $X."*

Requires internal coextensiveness and record support for each declared
category. Does **not** require external sufficiency, because the claim is
explicitly bounded by the model's own universe.

Unsupported neighbour: that the declared categories are the legally relevant
ones.

This rung is honest only if the declared universe is legible to the reader. A
bounded claim whose bound is not stated is not a bounded claim.

### Level 4 — Derived tax-concept result

*"The taxpayer's [concept] for this year is $X."*

Requires external sufficiency **and** record sufficiency. This is the first rung
that asserts something about the taxpayer's tax position rather than about the
model or the record.

**This rung carries the whole tax substance.** Anything controlling law makes
determinative of the concept belongs here, regardless of which form discloses
it.

Unsupported neighbour: that this is what belongs on a particular official line.

### Level 5 — Official form-line binding

*"[Official line] is $X."*

Requires level 4, plus that the concept computed is the concept the line names,
plus the form-specific ordering and disclosure the authority imposes. Level 5
**verifies a correspondence**; it cannot supply substance level 4 is missing.

### Level 6 — Filed representation

*"This is what the taxpayer reported to the tax authority."*

Requires level 5 plus a filing act. Filing authorisation is a separate question
from calculation authorisation.

### What the ladder buys

Failure at a higher rung leaves lower rungs intact. So the immediate fallback
for a model that does not yet reach a rung is never "show nothing" — it is
*"show the rung the modeling reaches, and name the rung."*

**The costly mistake is not stopping at level 3. It is rendering a level-3
result in a level-5 position.**

**Read forwards, the ladder is more useful still.** Each gap between rungs is a
bill of materials: a specific set of modeling capabilities that, once built,
moves the product up one rung. That reading is developed in
[claim-boundaries-and-modeling.md](claim-boundaries-and-modeling.md), and it is
the reading this milestone uses. A rung the modeling does not reach is a
specification, not a verdict.

## Judging whether partial coverage is good enough

Partial coverage is the permanent condition. So "good enough" needs a
structure, and it needs one that cannot be satisfied by silence.

Two prohibitions govern the whole framework:

> **"Good enough" must never mean merely that no reviewer has yet discovered
> another omission.** Absence of discovered defects is a fact about the review
> effort, not about the model.

> **A list of known gaps must never imply that all unlisted cases are
> covered.** The list is a lower bound on what is missing, never an upper one.

### The considerations

These are the things that must be *identified* for a coverage decision to be
made responsibly. This milestone does not decide them; deciding them is a
product-policy act, and the point of enumerating them is that the decision
should be made against a known list rather than an implicit one.

They have a second and more useful reading. Run forwards, the same list
prioritises **where to spend modeling attention** — what can be silently
wrong, what is observable, what a question could detect, what it is worth.
That reading is in
[claim-boundaries-and-modeling.md](claim-boundaries-and-modeling.md).

1. **The exact claim being supported.** Which rung of the ladder, stated in
   words, for which subject and period.

2. **The intended use.** Explanation, calculation, binding to an official
   return line, and filing are four different uses with four different
   thresholds. A model adequate for explanation may be inadequate for binding.

3. **The supported taxpayer and transaction profile.** Which taxpayers and
   which transactions the coverage actually contemplates — stated positively,
   not as the complement of a gap list.

4. **The authority examined, and its effective period.** Which sources were
   read, of what class, governing which period. Authority that was not examined
   is not coverage, however likely it is to agree.

5. **Materiality and consequence of the unsupported cases.** What the error is
   worth, and what follows from it — a small arithmetic difference, a
   substantially wrong return, a missed benefit, an exposure.

6. **Practical incidence among taxpayers whose evidence the product actually
   sees.** Not general population frequency: incidence conditional on the
   evidence the product handles. Any incidence claim must rest on measurement
   or be labelled explicitly as an unmeasured hypothesis.

7. **Observability from ordinary evidence.** Whether the unsupported
   circumstance is visible in the documents the taxpayer normally has. A
   circumstance that never appears in any document is a permanently invisible
   gap and must be treated as such.

8. **Detectability by targeted questions.** Whether a question the product
   could reasonably ask would reveal the circumstance. This converts an
   invisible gap into a blocking one, which is a large improvement even when it
   does not produce an answer.

9. **Whether the gap can produce an undetected materially wrong result.** The
   single most important consideration. A gap that blocks is bounded. A gap
   that silently changes the answer is not.

10. **Behaviour at the support boundary.** What happens exactly at the edge:
    block, degrade the claim, warn, or proceed silently. The boundary behaviour
    is a design decision that is usually made by default and rarely declared.

11. **Independent review and adversarial evidence.** What was tested against
    the model by someone trying to break it, and what that testing found. This
    consideration is what stops the framework from collapsing into
    self-assessment.

12. **Versioning and later change.** How the coverage profile is versioned, what
    happens when the law changes, what happens when the model changes, and what
    a claim made under an earlier version means afterwards.

### Known gaps versus unknown residual risk

These are different quantities and must be reported separately.

**Known gaps** are enumerated regions of the concept's universe that the
coverage profile marks as unsupported. They are bounded and can be prioritised.

**Unknown residual risk** is everything the intensional model failed to
enumerate. It is not visible in the gap list, by construction. It is bounded
only by the depth of authority examined and the adversarial effort spent — the
two things consideration 4 and consideration 11 measure.

An application that reports only known gaps is telling the truth and creating a
false impression. The honest statement pairs them: *"these specific regions are
unsupported, and the enumeration itself rests on this much authority and this
much adversarial testing."*

Cataloguing known gaps is therefore useful and self-limiting. It must not
become an unbounded census, because a census of a universe you have not fully
enumerated cannot terminate and cannot tell you what it is missing.

## What this leaves open

Three classes of decision fall out of this document and are recorded, not
resolved:

- **Conceptual architecture.** Whether the intensional model, the coverage
  profile, and the claim are separate declared artifacts, or facets of one.
- **Authority policy.** What depth of authority examination is required before
  a region may be marked supported. Developed in
  [authority-model.md](authority-model.md).
- **Product sufficiency policy.** Where the thresholds sit on considerations
  1–12, and who is entitled to move them.

None of these is settled here, and none of them is a representation or schema
question. Representation comes last.
