# Prototype Examination — Reported Interest to Tax Concept

**Exhibit:** `exhibits/reported-interest-tax-concept/it1`
(branch `prototype/reported-interest-tax-concept-it1`, commit `0d078436`)
**Charter:** [charter.md](charter.md)

Prototype code does not enter the milestone merge. It is reachable at the tag
above. This file and the charter are the durable record.

## What was built

Three modules and a test suite, on the prototype branch:

- an ordinary-fact layer and the six cases, each fact carrying a version and an
  ordinarily-phrased question ("How much did you pay the seller for interest
  already built up?");
- the two shapes, both deriving through the real
  `packages/derivation/evaluator.py` over a real `Environment`, with provenance
  taken from the evaluator's own `AccessLog` rather than asserted by the
  prototype;
- the ten-requirement rubric as executable checks, plus three probes;
- `tests/test_reported_interest_prototype.py`.

**Test result:** `15 passed, 138 subtests passed in 1.15s`.

The tax rule is a single expression tree over the ordinary facts. The user is
asked whether they bought the obligation between interest payment dates and how
much they paid the seller. The rule — not the user — decides that such interest
is not the purchaser's income. The rubric check that enforces this scans every
question put to the user for the words *taxable*, *includible*, *excludable*,
*adjustment*, and *schedule b*, and fails if any appears.

## A paper claim overturned by execution

Earlier rounds recorded that `conditional_dependency_set` could not express the
TI-N1 requirement, because its `members` must be `ref_expr` rather than family
collects. That restriction is real but **does not bite here**: the ordinary
circumstance is a keyed per-item symbol, not a family collect. With
`condition = (bought between dates == yes)` and
`members = [ref(accrued amount)]`, the evaluator distinguishes "yes, amount
supplied" from "yes, amount missing", blocking with `DEPENDENCY_ABSENT` and
naming the missing fact.

This is the reverse of the milestone's earlier failure mode: a paper claim was
falsified by execution in the direction of *more* expressiveness, not less.

## Case outcomes

Identical across all three shapes. Every number below was produced by an
executed run.

| Case | Shape A | Shape A-repaired | Shape B |
| --- | --- | --- | --- |
| TI-B1 | line 2b = 1200 | line 2b = 1200 | line 2b = 1200 |
| TI-B2 | line 2b = 900 | line 2b = 900 | line 2b = 900 |
| TI-N1 | blocked: `DEPENDENCY_ABSENT` (accrued-interest-paid-to-seller) | same | same |
| TI-L1 | line 2b = 700 | line 2b = 700 | line 2b = 700 |
| TI-L2 | line 2b = 950 | line 2b = 950 | line 2b = 950 |
| TI-A1 | blocked: `SLICE_COVERAGE_UNSUPPORTED` | same | same |

**Arithmetic does not discriminate.** Both shapes produce every required number,
including the two cases designed to break the weaker one. Any recommendation
that rests on the displayed number is unsupported.

## Rubric results

Shape A fails exactly one requirement, on four cases:

- **TI-B1, TI-B2, TI-L1, TI-L2 / authority attached** — the published symbols
  are bare amounts; no authority is recoverable from the result for why the
  reduction was taken.

Shape A-repaired and shape B fail nothing. All ten requirements pass on all six
cases for both.

So the static rubric alone does **not** decide the question. A-repaired —
distributed symbols with authority attached per symbol — clears it. That is why
two dynamic probes were added.

## Lifecycle independence

All six observations pass. Two are worth naming because they are the strongest
points in shape A's favour and shape B's disfavour:

- **A: source correction leaves basis standing.** The basis symbol never read
  box 1, so reissuing the statement does not disturb it. Displacement is precise.
- **B: displacement is whole-object.** A source correction displaces the basis
  field too, though recomputation restores it. Displacement is coarse.

On lifecycle precision, the distributed shape is the better one.

## Probe 1 — partial refresh

Question: can the distributed shape's symbols drift out of agreement with each
other?

| Observation | Result |
| --- | --- |
| A coherent before correction | `True` |
| A coherent after partial refresh | `False` |
| A includible after refresh | `950` |
| A basis after refresh | `300` |
| A implied non-includible | `250` |
| **A detected the disagreement** | **`False`** |
| B coherent after correction | `True` |
| B includible | `950` |
| B basis | `250` |

After the circumstance correction $300 → $250, refreshing only the includible
symbol leaves shape A asserting $950 includible — which implies $250 of
non-includible interest — while its basis symbol still reads $300. The two
symbols disagree, and **nothing in the shape can tell**. The coherence check is
an external observer's arithmetic, not something the result carries.

Shape B cannot reach this state. Its fields are one object with one account of
one set of source facts.

## Probe 2 — cross-year carry

The obvious objection to probe 1 is that it models stale persistence, and a full
re-run from current facts would recompute both symbols. Probe 2 is the answer,
because the basis consequence must **outlive the year in which it is computed**.

| Observation | Shape A | Shape B |
| --- | --- | --- |
| what is carried | `one amount 300 for item demo.obligation-1` | `reported 1200, includible 900, non-includible 300, basis 300` |
| can state the reported amount it came from | `False` | `True` |
| can state the includible amount it is consistent with | `False` | `True` |
| carried value displaced by the amendment | `True` | `True` |
| **self-check available in a later year** | **`False`** | **`True`** |

Both shapes correctly displace the carried value when the source year is
amended. The difference is what a later year can *verify*. Shape A carries a
bare $300 against an item. In the year of disposition there is no re-run to
perform, because the facts that produced it belong to a prior year's workspace;
the amount either matches or it does not, and nothing can say which.

## Incumbent baseline — exactly what was executed

`tests/test_schedule_b_interest_adjustments.py` and
`tests/tax/test_track2_line2b.py` → **14 passed, 9 subtests passed in 3.19s**.

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

Verified independently by search: the 2025 package contains no § 135 or Form
8815 content. Every `8815` match in the tree is a hex-checksum substring, and
`rg -o 'IRC[^,"]{0,10}135|section 135|§ *135'` returns nothing.

Therefore, for a taxpayer with qualifying savings-bond education expenses, the
incumbent flows box 1 to line 2b unreduced. **The incumbent's ordinary line-2b
result is not correct for this taxpayer**, and it is wrong silently. Both
prototype shapes block on `SLICE_COVERAGE_UNSUPPORTED` instead.

## Recommendation

**Recommend the explicit determination representation (shape B).**

Not because it computes anything the distributed shape cannot — it does not, on
any of the six cases — but because of what the two probes show. The distributed
shape can enter a silently incoherent state and cannot detect it, and its
carried basis consequence cannot state the reported or includible amount it is
consistent with once the producing year is gone. The determination shape cannot
reach either state.

Note carefully what "distributed" had to become before it got this far. Shape A
as first built failed authority attachment; repairing it meant attaching the
item, the rule, the authority, and provenance to each symbol. A-repaired is
already most of a determination, distributed across symbols that no longer have
a reason to be separate — and it still fails both probes precisely *because*
they are separate.

### The strongest case against this recommendation

Two, honestly stated.

1. **Lifecycle precision is genuinely worse.** Shape B's displacement is
   whole-object: correcting the statement displaces the basis field even though
   the basis never depended on box 1. Shape A displaces exactly what changed.
   That is a real cost and it is the one place the distributed shape wins.
2. **Probe 1 models stale persistence.** If the system always re-runs every
   symbol from current facts, the incoherent state is unreachable and probe 1
   proves nothing. This objection is answered by probe 2 and only by probe 2 —
   which is why the recommendation should not be taken to rest on probe 1 alone.
   If probe 2 were removed, the honest verdict would be "both work; prefer the
   cheaper."

### Smallest remaining owner decision

**Does a consequence that outlives the tax year have to be self-checkable?**

Everything above reduces to this. If a carried basis reduction must be able to
state, in the year of disposition, the reported and includible amounts it is
consistent with, then a determination object is warranted and the distributed
shape is out. If a bare amount keyed to an item is sufficient — because the
broker reports the reduced basis, or because the user is expected to reconcile —
then the distributed shape is cheaper and probe 2 loses its force.

That question is not a representation question and this prototype cannot answer
it. It is a product question about what the year-of-disposition experience owes
the user.

## Status of the necessity hypothesis

The milestone's original proposition — that a separately recoverable item-level
determination is necessary — is **supported by this round's evidence, on the
narrow ground of the two probes, and on no other ground**.

It was previously recorded as defeated. That record was wrong twice over: the
counterexample was never executed, and "the existing engine can subtract an
already-classified adjustment" establishes working arithmetic, not derivation
from ordinary facts. Both statements are withdrawn in the milestone documents.

This round is not a production selection. It is one executed comparison on one
fixture, and the recommendation stands or falls on a single unresolved product
question.
