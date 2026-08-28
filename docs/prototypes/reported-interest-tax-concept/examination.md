# Prototype Examination — Reported Interest to Tax Concept

**Exhibit:** `exhibits/reported-interest-tax-concept/it2` (commit `14e50d3e`)
**Superseded exhibit:** `exhibits/reported-interest-tax-concept/it1` (commit `0d078436`),
retained unchanged as historical evidence of the defective round.
**Charter:** [charter.md](charter.md)

Prototype code does not enter the milestone merge. Both iterations are reachable
at the tags above; no prototype branch remains. This file and the charter are
the durable record.

## Why there are two iterations

Iteration 1 executed, produced every required number, and recommended the
explicit determination shape. Review found the recommendation rested on two
defective probes and a provenance rubric too narrow to detect them. The
recommendation is **withdrawn**. What follows is iteration 2's evidence, and
every claim iteration 1 made that did not survive is named here rather than
quietly dropped.

| Iteration 1 claim | Status after iteration 2 |
| --- | --- |
| Distributed symbols can silently disagree after a partial refresh | **Withdrawn.** The probe refreshed one affected artifact and retained another whose own provenance said the correction displaced it. It measured a decision to retain displaced state, not a property of distributed representation. |
| Shape A cannot state the reported or includible amount in a later year, and has no self-check | **Withdrawn as stated.** Those were hard-coded booleans, not observations. What an actual later-year consumer can recover is now executed, and the answer depends on a product assumption. |
| All ten requirements pass for A-repaired and B | **Withdrawn.** The rubric's expected-input set named three facts. The obligation kind, the education answer, the payer, the statement's own item, the declared relation, the rule identity, the authority, and the coverage declaration were absent from every provenance account, so nothing could fail. |
| A source correction leaves shape A's basis symbol standing; distributed displacement is more precise | **Withdrawn.** It was an artefact of a discarded guard access log. The basis artifact is taken under a coverage guard that reads the statement, so reissuing the statement displaces it. Displacement is whole-object in every shape. |
| TI-A1 was executed | **Withdrawn.** Iteration 1 reused the box-1 fixture and flipped two categorical answers. TI-A1 now has its own box-3 fixture. |
| The 2025 package contains no § 135 or Form 8815 content | **Withdrawn as stated.** It contains Form 8815 content. See [TI-A1 and the incumbent](#ti-a1-and-the-incumbent). |

## What was built

Four modules and a test suite:

- an ordinary-fact layer and the six cases, each fact carrying a version and an
  ordinarily-phrased question ("How much did you pay the seller for interest
  already built up?"), with **two distinct fixtures** — a box-1 statement for the
  accrued-interest slice and a separate box-3 statement for TI-A1;
- three shapes, all deriving through the real
  `packages/derivation/evaluator.py` over a real `Environment`, with provenance
  taken from the evaluator's own `AccessLog` rather than asserted by the
  prototype;
- an eleven-requirement rubric as executable checks, a currentness probe, and a
  later-year consumer;
- `tests/test_reported_interest_prototype.py`, including six adversarial tests.

**Test result, run from the exhibit tree at the tag**
`exhibits/reported-interest-tax-concept/it2` (commit `14e50d3e`):
`pytest tests/test_reported_interest_prototype.py -n0` → **26 passed, 298
subtests passed in 0.05s**. The six required-case tests, the rubric, the six
adversarial corrections, the currentness probe, and the later-year consumer
are all in that file.

The tax rule is a single expression tree over the ordinary facts. The user is
asked whether they bought the obligation between interest payment dates and how
much they paid the seller. The rule — not the user — decides that such interest
is not the purchaser's income. The rubric check that enforces this scans every
question put to the user for the words *taxable*, *includible*, *excludable*,
*adjustment*, and *schedule b*, and fails if any appears.

### The three shapes

Iteration 1 scored an unrepaired shape A whose published symbols carried no
item, rule, or authority. Nobody would build that, and scoring it inflated the
apparent gap. It is dropped. The shapes compared here are:

- **A — distributed.** Two artifacts, published by two rules, each carrying its
  own item, rule identity, substantive authority, and provenance. Nothing
  durable states how the two amounts relate.
- **A+ — distributed, with the partition edge.** Identical to A except that the
  artifact a later year carries also names what it is a part of. Still two
  artifacts, still two rules, **no determination object**. It exists to separate
  "a durable relationship is necessary" from "a new kind of citizen is
  necessary".
- **B — explicit determination.** One item-level result holding the reported,
  includible, non-includible, and basis amounts together with the item, rule,
  authority, and source facts.

All three share one evaluation path, one guard, and one currentness policy.

## A paper claim overturned by execution

Earlier rounds recorded that `conditional_dependency_set` could not express the
TI-N1 requirement, because its `members` must be `ref_expr` rather than family
collects. That restriction is real but **does not bite here**: the ordinary
circumstance is a keyed per-item symbol, not a family collect. With
`condition = (bought between dates == yes)` and members naming the accrued
amount and the relation, the evaluator distinguishes "yes, amount supplied" from
"yes, amount missing", blocking with `DEPENDENCY_ABSENT` and naming what is
missing.

Iteration 2 leans on the same op a second way. Because
`conditional_dependency_set` does **not** short-circuit — it evaluates every
member and accumulates absences — a dependency set with a literal-true condition
is the way to make provenance independent of evaluation order. The `all` op does
short-circuit, so a guard expressed only with `all` silently truncates the read
set. That is one of the two mechanisms behind iteration 1's incomplete
provenance.

## Case outcomes

Identical across all three shapes. Every number below was produced by an
executed run.

| Case | Shape A | Shape A+ | Shape B |
| --- | --- | --- | --- |
| TI-B1 | line 2b = 1200 | 1200 | 1200 |
| TI-B2 | line 2b = 900 | 900 | 900 |
| TI-N1 | blocked: `DEPENDENCY_ABSENT` (accrued-interest-paid-to-seller) | same | same |
| TI-L1 | line 2b = 700 | 700 | 700 |
| TI-L2 | line 2b = 950 | 950 | 950 |
| TI-A1 | blocked: `SLICE_COVERAGE_UNSUPPORTED` | same | same |

**Arithmetic does not discriminate.** All three shapes produce every required
number, including the two cases designed to break the weaker one. Any
recommendation that rests on the displayed number is unsupported.

## Rubric results

Eleven requirements, six cases, three shapes. **One requirement fails, for one
shape, on the four cases that publish a result:**

- **TI-B1, TI-B2, TI-L1, TI-L2 / shape A / relationship durable on the carried
  artifact** — the carried artifact holds only `['amount']`; the reported and
  includible amounts it partitions are recoverable only from the source year's
  sibling artifacts.

Shapes A+ and B fail nothing. Every other requirement — including provenance
completeness against the fixture's full declared fact set plus rule, authority,
and coverage; item attribution; operational verification of the declared
relation; and explicit failure — passes for all three shapes on all six cases.

This is the significant change from iteration 1. The repaired rubric is
strictly harder, and the distributed shape still clears all of it but one row.

## Provenance, repaired

Every artifact's provenance now accounts for every declared fact the fixture
holds — eight on TI-B2 (reported amount, payer, statement obligation, purchase
question, accrued amount, declared relation, obligation kind, education
answer); six on TI-B1 and TI-A1, which do not hold the accrued amount or the
relation — plus three non-fact inputs: the rule identity and version, the
substantive authority, and the coverage declaration. Two mechanisms were
needed:

1. **One access log.** Guard and value are evaluated against a single
   `AccessLog`. Iteration 1 ran the guard in a throwaway log, so the obligation
   kind and education answer — the facts that decide coverage — displaced
   nothing.
2. **The relation is operational.** `accrued-relates-to` and the statement's
   `obligation` are declared to be the same fact type, which is what permits
   `categorical_compare` to compare them at all: the evaluator refuses to
   compare operands of different declared domains. Item identity is established
   by the relation the taxpayer supplied and refuses on disagreement, rather
   than being recovered from the statement or from a naming convention.

### Adversarial tests

Six corrections applied **after** a result exists. Each observes currentness,
refusal, item attribution, and provenance — not a number. All pass for all three
shapes.

| Correction | Persisted artifacts | Recomputation |
| --- | --- | --- |
| obligation kind → series EE savings bond | all displaced, `serve` refuses | blocks `SLICE_COVERAGE_UNSUPPORTED` |
| education answer → yes | all displaced, `serve` refuses | blocks `SLICE_COVERAGE_UNSUPPORTED` |
| relation repointed to a third obligation | all displaced, `serve` refuses | blocks `ITEM_RELATION_MISMATCH` |
| statement item changed, relation left standing | all displaced, `serve` refuses | blocks `ITEM_RELATION_MISMATCH`; prior artifacts stay attributed to the item they were taken for |
| relation removed | all displaced, `serve` refuses | blocks `DEPENDENCY_ABSENT`, naming the relation |
| payer corrected | all displaced, `serve` refuses | recomputes to 900, same item |

Under iteration 1's rubric, the first two, the third, the fourth, the fifth, and
the sixth would all have left the persisted result standing as current.

## Probe 1 — currentness

Iteration 1's partial-refresh probe is deleted. Its replacement asks what a
correction does under a policy no shape may opt out of: a changed dependency
displaces every artifact whose provenance reads it, and a displaced artifact is
not servable as current. `Store.serve` raises rather than returning one.

Under a circumstance correction, a source correction, and an obligation-kind
correction, for every shape:

- artifacts left current: **`()`** in all nine combinations;
- artifacts refused on `serve`: **the complete published set** in all nine.

There is no state in which one artifact is refreshed and a displaced sibling is
still served. **The discriminator iteration 1 reported does not exist once both
shapes are held to the same currentness policy.** Constructing it required an
API that returns displaced state as current, which the engine's actual execution
model — saturating all adopted rules into one `RunResult` — does not have, and
which iteration 1 never identified in any candidate architecture.

## Probe 2 — the later-year consumer

The basis consequence must outlive the year in which it is computed. A consumer
now performs six concrete recovery tasks against whatever each shape actually
persisted. It does not inspect capability flags and does not know which shape it
is reading. It is run under two product assumptions:

- **carried-only** — the later year holds the basis artifact it carried forward
  and nothing else. This is the assumption if basis is tracked on the holding.
- **full-source-year** — the later year can reach every artifact the source year
  published, and the source-year facts, on demand.

| Shape / access | Tasks passed |
| --- | --- |
| A / carried-only | **5 / 6** |
| A / full-source-year | 6 / 6 |
| A+ / carried-only | 6 / 6 |
| A+ / full-source-year | 6 / 6 |
| B / carried-only | 6 / 6 |
| B / full-source-year | 6 / 6 |

Tasks 1, 2, 3, 4 and 6 pass for every shape under both assumptions. All three
shapes identify the obligation, recover the basis amount with its source-year
rule and both authorities, name the ordinary fact that supplied the amount,
detect that the source year was amended (`displaced=True`, naming the changed
input), and decide correctly that the carried value is no longer usable.

The single failure is **shape A, carried-only, task 5 — explain why the basis
reduction exists**:

> the amount 300, its rule, and its authority are recoverable, but `['reported',
> 'includible']` are not: nothing carried forward states what this amount is a
> part of, so the reduction cannot be explained as a partition of the reported
> interest without re-opening the source year.

Given full-source-year access, shape A assembles the same explanation from the
carried artifact, a sibling artifact, and the source-year statement fact that
its own provenance names.

## The conclusion the evidence supports

**No representation is recommended on necessity grounds, because the executed
evidence does not establish necessity.**

Stated precisely:

1. All three shapes satisfy every semantic, lifecycle, provenance, refusal, item
   attribution, and explanation requirement on all six cases, under one shared
   execution and currentness policy — with one exception.
2. The exception is one task, under one product assumption: shape A cannot
   explain a carried basis reduction as a partition of the reported interest
   when the later year holds only what it carried.
3. **Shape A+ closes that gap and is not a determination.** It is two artifacts
   from two rules with no item-level result object; it differs from shape A only
   in that the carried artifact names what it partitions. It scores 6/6
   carried-only, exactly as shape B does.

So the necessary thing, if the product requires task 5 under carried-only
access, is **a recoverable relationship — one durable edge on the artifact that
travels** — and not a new kind of citizen. The milestone's original proposition,
that a *separately recoverable item-level determination* is necessary, is **not
supported**. The weaker proposition, that *some durable relationship beyond
independent amounts* is necessary, is supported **conditionally**, on a product
requirement the owner has not selected.

### The owner-held product requirement

**When a later year needs the basis consequence, what does it hold?**

- **If the later year carries only the basis artifact** — because basis is
  tracked on the holding, or the source year's workspace is not retained — then
  the carried artifact must name what it is a part of. Shape A is out. Shape A+
  and shape B both satisfy this, and the choice between them is an ordinary
  design question about cohesion and cost, not a question this prototype
  decides.
- **If the later year may re-open the source year** — reaching sibling artifacts
  and the source-year facts that provenance names — then shape A satisfies every
  requirement and is the cheapest of the three. Choosing A+ or B would be a
  preference, not a necessity.

The two consequences are stated plainly and neither is recommended here, because
selecting between them is the owner's call and the prototype has no evidence
bearing on it.

### The strongest case against treating this as settled

1. **One fixture, one slice.** Everything above is a single accrued-interest
   pattern on a single obligation. A shape that holds up here may not hold up
   where one ordinary fact bears on several items, or several statements bear on
   one item. Nothing here tests that.
2. **A+ was built by the same author, after the gap was known.** It is a fair
   rival in that it is genuinely distributed and passes the same suite, but it
   was designed to close a specific failing task. A reviewer should ask whether
   a seventh task, or a different consumer, separates A+ from B — and this round
   did not look for one.
3. **Cost is not measured.** Nothing here establishes production cost, schema
   compatibility, or migration size, and none may be inferred from prototype
   dataclasses. The cohesion argument for B and the cheapness argument for A are
   both unquantified.
4. **Task 5's framing is a choice.** Requiring an explanation to state the
   partition, rather than to cite the rule and the supplying fact, is what
   creates the gap. That framing is defensible — an explanation that cannot say
   what an amount was separated from is thin — but it is a framing, not a
   measurement.

## Incumbent baseline — exactly what was executed

`tests/test_schedule_b_interest_adjustments.py` and
`tests/tax/test_track2_line2b.py` → **14 passed, 9 subtests passed in 6.36s**.

What these establish, precisely:

- subtraction of an **already-classified** adjustment: $2,000 box 1 less a $100
  accrued-interest adjustment resolves line 2b to $1,900. This is a *structural
  analogue at different amounts*, not an execution of TI-B2;
- closed-empty family behaviour and its correction;
- unclosed-family blocking;
- the negative-line-2b guard;
- a presentation golden.

What they do **not** establish: none of the six semantic cases was executed
against the incumbent. The incumbent has no representation of the ordinary
purchase question at all, so TI-B2 and TI-N1 cannot be posed to it without first
supplying the classification the cases exist to withhold.

Distinguish three grades of evidence in anything that cites this section: exact
execution of a case (none, for the incumbent); a structural analogue (the $2,000
/ $100 test); and artifact inspection (the readings in
`incumbent-representation.md`).

## TI-A1 and the incumbent

TI-A1 is Series EE savings-bond interest reported in **box 3** with qualified
education expenses. The prototype now executes it as its own fixture: a second
statement, a second payer, a second obligation, and $840 in box 3 — deliberately
not the box-1 amount, so a leaked result would be visible rather than plausible.
All three shapes block on `SLICE_COVERAGE_UNSUPPORTED`.

Iteration 1 recorded that "the 2025 package contains no § 135 or Form 8815
content" and that every `8815` match was a hex-checksum substring. **That was
wrong.** The corrected, artifact-grounded account:

1. **Form 8815 content exists.** `ss-benefits-scope.bundle.json` defines the
   fact type `tax.us.2025.ss-benefits-scope.no-form-8815`, a tax-year-keyed
   contributed categorical over `{yes, no}` with no default, titled as a
   completeness component: "`yes` asserts the named excluded class is absent;
   `no` asserts it is present and blocks." It is consumed by
   `rule.ss-benefits-worksheet.json` and its `.v2` and `.v3` successors.
2. **Its reach is one worksheet.** It scopes the bounded Social Security
   Benefits Worksheet claim. It says nothing about line 2b.
3. **No committed rule computes the § 135 exclusion.** A search of the committed
   content for section 135 and for qualified-education language returns nothing
   outside student-loan interest, which is a different provision.
4. **Box 3 reaches line 2b unreduced.** `package.core-calculations.v33`
   selects `tax.us.2025.rule.form1040-line2b` version `v4`.
   `rule.f1099int-b3-subtotal.json` publishes `tax.us.2025.interest.b3-subtotal`,
   which is an addend in that rule. The rule's `scope` is tax-year /
   jurisdiction / family, and its `when` clause requires family closure plus a
   non-negative result. It does **not** pin a Form 8815 or § 135 coverage fact,
   and its only subtractions are the nominee, accrued-interest, and
   amortizable-bond-premium subtotals. Nothing in the selected rule computes
   the § 135 exclusion or subtracts it from line 2b.

Therefore, for a taxpayer with qualifying savings-bond education expenses, the
incumbent flows box 3 to line 2b unreduced. **The incumbent's ordinary line-2b
result is not correct for this taxpayer, and it is wrong silently.**

The useful finding is sharper than iteration 1's wrong one. The package already
**owns the pattern** for declaring a class out of scope: a tax-year-keyed
`{yes, no}` completeness component that blocks when the excluded class is
present. It applies that pattern to the Social Security Benefits Worksheet and
not to line 2b. The gap is not a missing idea; it is a pattern applied in one
place and not another. That is a repair the incumbent can absorb, and it does
not depend on which representation this milestone selects.

## Status of the necessity hypothesis

**Not established.** The milestone's proposition — that a separately recoverable
item-level determination is necessary — was recorded as defeated, then as
supported by iteration 1's two probes, and is now neither. Both earlier records
are withdrawn:

- the original defeat rested on a counterexample that was never executed, and on
  reading "the existing engine can subtract an already-classified adjustment" as
  derivation from ordinary facts, which it is not;
- iteration 1's support rested on a manufactured discriminator and a hard-coded
  verdict.

What is established is narrower and firmer: on this fixture, under a fair shared
policy, a distributed representation meets every requirement except one
explanation task under one product assumption, and a distributed representation
carrying one additional edge meets that too. This round is not a production
selection.
