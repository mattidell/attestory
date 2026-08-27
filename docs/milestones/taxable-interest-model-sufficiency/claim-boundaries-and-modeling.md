# What the Product Could Say: Claim Boundaries as a Map of Modeling Work

## The question, and its direction

**What could this product say about a tax concept if the domain were modeled
properly — and what modeling would each thing it might say require?**

The direction matters more than the words. There are two ways to run into the
edge of a model, and they lead to opposite places.

> *"We found a gap. What may we still say?"* — leads down the claim ladder,
> toward a narrower statement, and terminates in a permission list.

> *"We found a gap. What modeling would let us say it?"* — leads into the
> domain, toward a specification, and terminates in work worth doing.

This milestone takes the second. The evidence is the same evidence either way;
the adversarial cases, the coverage map, and the engine findings were all
gathered before the direction was settled and none of them changes. What
changes is what a finding *is*. A gap stops being a verdict and becomes a
requirement.

**The benchmark.** When a probe finds a deficiency, the question to ask is
whether the **domain modeling must expand or change** — not whether the claim
must weaken, and not whether more evidence is needed.

## What this milestone is not doing

It is not modeling claim defensibility. Claim integrity is a constraint on the
exploration in the way correctness is a constraint: violating it invalidates a
result, but pursuing it is not the point. The product is not trying to become
an authority or to win a defense of its conclusions.

Nor is it asking what the product may say *right now*, given the engine as
built. That framing quietly caps the exploration at current capability, which
is exactly backwards for a stage whose purpose is to find out what good
modeling makes possible. The tax and law domains are large. The interesting
question is how much of that space becomes reachable with attention, not how
little is reachable without it.

## The claim ladder, read as a modeling-investment map

The six rungs are unchanged and are defined in
[concept-coverage-and-claims.md](concept-coverage-and-claims.md). Read
forwards, each gap between rungs is a bill of materials.

### Level 3 → Level 4: from "over our categories" to "your taxable interest"

This is the expensive step, and it is entirely modeling. For the specimen it
requires:

| Requirement | Why the current model cannot do it |
| --- | --- |
| Facts no document discloses can be held | Acquisition date and cost, nominee ownership, education-expense coordination, premium netting, election status, and frozen-deposit status have no representation |
| Substantive exclusions are operands, not schedule rows | The § 135 exclusion exists in the model only as Schedule B presentation machinery, so a statutory reduction is decided by form layout |
| Amounts carry a period assignment | "Received or accrued" is never pinned to a modelled event |
| Amounts carry a subject | Nominee amounts belong to another person, and the model has no way to say so substantively |
| Elections are representable, with a declared default | No election has any representation; the default is implicit and undeclared |
| Reported and includible are separable | One fact type serves both, so the distinction is not merely uncomputed but unrepresentable — and therefore unaskable |
| The boundary is detectable from inside | The model cannot tell when an unmodelled circumstance may be present, which is what makes silent omission possible |

The last row is the one to fund first. It is the difference between a model
that is bounded and a model that is wrong without knowing it.

### Level 4 → Level 5: from the concept to the official line

A different and much smaller bill: fidelity of the form arrangement and its
ordering, the disclosure and attachment conditions, and a check that the
concept computed is the concept the line names. This step verifies a
correspondence. It cannot supply substance the level-4 modeling is missing,
which is why treating the current defect as a form-ordering problem
understates it.

### Level 5 → Level 6

A filing act, plus the machinery that keeps a simulation distinct from a
determination and a determination distinct from a filing. Out of scope here.

### Why the map is worth having

It converts an open-ended "is the model good enough" into a finite, orderable
list of capabilities with known consequences. Occupying an official form line
remains the demanding target at the top, and it earns that position: it is the
most exacting claim available in the domain, so aiming at it forces the
modeling question to its limit rather than letting it settle wherever the
engine happens to be.

## The coverage map, read as a backlog

Each status in
[taxable-interest-coverage-profile.md](taxable-interest-coverage-profile.md)
implies a specific kind of modeling work.

| Status | What modeling moves it |
| --- | --- |
| represented and supported | Nothing |
| represented but semantically collapsed | Split the representation so the distinction the law makes survives |
| represented but requiring judgment | Represent the determination, or represent the open fact and surface it |
| bounded exclusion | Nothing — but the bound must be declared where a reader sees it |
| unsupported and blocking | Add the category; the failure mode is already safe |
| unsupported but silently omitted | Make it detectable first, then add the category |
| outside the declared authority boundary | Widen the boundary, or leave and say so |

The ordering rule falls straight out of the table: **a category that can be
silently wrong outranks a category that blocks**, whatever their relative
sizes. Blocking is a bounded failure the user can see. Silent omission is not.

## The adversarial cases, read as specifications

The nine failure classes in
[taxable-interest-adversarial-cases.md](taxable-interest-adversarial-cases.md)
each name a modeling capability by describing its absence.

| Class | The capability it specifies |
| --- | --- |
| F1 reported ≠ includible | Reported facts and includible amounts separately representable |
| F2 substantive exclusion | Exclusions as substantive operands, independent of the form that discloses them |
| F3 timing | A declared includible event and an explicit period assignment |
| F4 ownership | Subject assignment per amount, not inherited from the payee line |
| F5 election | Elections as representable circumstances with a declared default |
| F6 absent from every document | Circumstance intake that does not depend on a document supplying the fact |
| F7 reporting without substance | Reporting operations that can run without becoming the concept |
| F8 undetectable | Boundary detection from inside the model |
| F9 partial coverage | A declared concept universe, separate from what the build covers |

F5 has no case. Under the old direction that was an admission. Under this one
it is an unexplored region of the specification, and the cheapest kind of work
to schedule.

## Which layer does an expansion belong to?

The eight layers in
[tax-modeling-foundation.md](tax-modeling-foundation.md) are the instrument for
placing a requirement once it is identified. Expanding the wrong layer is the
characteristic way modeling work goes wrong — it produces something that
computes but does not mean.

The specimen's largest deficit sits at layer 3, economic and circumstantial
facts. That is not where an engine built by translating form instructions
naturally grows, because form instructions describe layers 2 and 5 and are
silent about layer 3 by construction. **This is the clearest evidence the
milestone has produced that translating form instructions is structurally
insufficient**, and it is a wrong number rather than a philosophical objection:
a statutory exclusion that operates on gross income is visible to the current
model only as a row on a schedule, so the model gets it wrong for every
taxpayer who qualifies.

## Where to spend attention first

The considerations in
[concept-coverage-and-claims.md](concept-coverage-and-claims.md) were written
as tests of whether coverage is adequate. Read forwards, they are
prioritisation inputs for modeling work:

- **Can it be silently wrong?** The dominant input. Fund detectability before
  coverage.
- **Is the circumstance observable from ordinary evidence?** If yes, intake is
  tractable. If no, it needs a question, and if no question can find it the
  gap is permanent and must be declared as such.
- **Can a targeted question detect it?** Converting an invisible gap into a
  blocking one is a large improvement even when it produces no answer.
- **What is it worth, and how often does it arise?** Real inputs, but any
  incidence claim must rest on measurement or be labelled an unmeasured
  hypothesis.
- **What happens exactly at the boundary?** Usually decided by default and
  rarely declared.

Known gaps are the backlog. Unknown residual risk is the argument for
continuing to probe adversarially, and it does not shrink because the backlog
does.

## A note on the meta level

Not everything the product might say is a substantive tax statement. It can
also say where a treatment comes from, what class of source establishes it,
that a determination turns on a fact not held and what that fact would change,
that a situation sits near a modelled boundary, or that guidance is
explanatory rather than controlling.

These are recorded here mainly because they help keep the focus honest: they
are things the modeling makes possible, and their requirements — provenance at
proposition level, uncertainty representation, boundary detection — mostly
overlap with what the substantive claims already need. They are a byproduct of
modeling the domain well, not a separate goal, and this milestone does not
develop them further.

## What this leaves open

The map is an instrument, not a plan. It says what each capability costs and
what it unlocks; it does not say which to build, in what order, or in what
representation. Those remain open, and the representation question remains
deliberately last — see
[current-engine-assessment.md](current-engine-assessment.md) for what the
existing structure does today and
[representation-reconnaissance.md](representation-reconnaissance.md) for why no
shape is chosen here.
