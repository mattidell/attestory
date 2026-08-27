# What Good Tax Modeling Would Make Possible

## The question

**What could this product say about a tax concept if the domain were modeled
properly — and what modeling would each thing it might say require?**

US-federal taxable interest for 2025 is the **worked specimen** throughout, not
the subject. The supporting question is the one the layer architecture answers:
how to keep evidence, economic facts, tax classification, return reporting,
computation, claim scope, and presentation distinct, so that a shortfall can be
located precisely enough to act on.

**The direction is the whole point.** On finding a deficiency, the question is
whether the domain modeling must expand or change — not whether the claim must
weaken, and not whether more evidence is needed. A gap is a specification, not
a verdict.

Two things this milestone is not doing. It is not modeling claim
defensibility: claim integrity constrains the exploration the way correctness
does, but pursuing it is not the goal. And it is not asking what the product
may say given the engine as built, because that caps the exploration at
current capability.

## Reading order

The documents build on one another. Read them in this order.

**1 — Foundation and separation of models**

- [tax-modeling-foundation.md](tax-modeling-foundation.md) — the eight models
  that must connect without collapsing, the chain between them, and the
  catalogue of specific collapses.
- [concept-coverage-and-claims.md](concept-coverage-and-claims.md) — the
  distinction between the intensional concept model, the executable coverage
  profile, and claim scope; the claim ladder; and the considerations that
  decide where partial coverage is fit for a stated use.

**2 — The worked semantic example**

- [taxable-interest-concept.md](taxable-interest-concept.md) — the architecture
  instantiated against one real concept, and the six places it strains.

**3 — Authority and coverage-profile method**

- [authority-model.md](authority-model.md) — what must be recorded for a
  proposition to count as supported, what each class of source can and cannot
  establish, and how a coverage profile is constructed.
- [taxable-interest-coverage-profile.md](taxable-interest-coverage-profile.md)
  — that method applied: declared authority boundary, category-by-category
  coverage, and the actionable gaps it exposes.

**4 — Adversarial tests of the modeling requirements**

- [taxable-interest-adversarial-cases.md](taxable-interest-adversarial-cases.md)
  — sixteen bounded synthetic cases organised by failure class, testing the
  architecture rather than inventorying missing features.

**5 — Synthesis**

- [claim-boundaries-and-modeling.md](claim-boundaries-and-modeling.md) — reads
  the ladder, the coverage map, and the failure classes forwards as one
  instrument: what each capability costs and what it unlocks. **If you read one
  document, read this one.**

**6 — Downstream: the current engine**

- [current-engine-assessment.md](current-engine-assessment.md) — what one
  build's modeling reaches today, and the decisions its shortfalls raise.
- [representation-reconnaissance.md](representation-reconnaissance.md) —
  premature implementation reconnaissance, retained as evidence. No
  representation is selected in this milestone.

## Two rules that govern everything here

> **Coverage is never adequate merely because no reviewer has yet discovered
> another omission.**

> **A list of known gaps must never imply that all unlisted cases are
> covered.**

## What is deliberately not here

No tax rules are implemented and no missing categories are added. No schema,
validator, runner, content package, or ADR is changed. No citizen kind, field
shape, or contract is selected. No filing policy or legal-liability question is
decided. No claim to exhaustive knowledge of taxable-interest law is made, and
none of this generalises to other tax domains without being retested there.
