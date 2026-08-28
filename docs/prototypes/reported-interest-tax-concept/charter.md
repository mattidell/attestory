# Prototype Charter — Reported Interest to Tax Concept

**Topic:** `reported-interest-tax-concept`
**Exhibit tags:** `exhibits/reported-interest-tax-concept/it1` (superseded), `.../it2` (current)
**Milestone:** Reported Interest to Tax Concept Vertical Slice

## The question this prototype exists to decide

Does the engine need a **separately recoverable item-level tax determination**
between what a source document reports and what reaches the return, or can the
same requirements be met by ordinary facts and a tax rule that derive a result
without any durable determination object?

The milestone's earlier rounds tried to settle this on paper. They could not.
Each paper round produced a claim about a mechanism that the next round
falsified, and the milestone reached a conclusion — "not established" — that
rested on an unexecuted design. This prototype replaces that argument with an
executed comparison.

## Fixtures

**Box-1 fixture, for the slice.** One synthetic taxpayer. One 2025 Form
1099-INT, one logical statement, one identified obligation, box 1 = $1,200. The
taxpayer bought the obligation between interest payment dates and paid the
seller $300 of interest that had already accrued.

**Box-3 fixture, for TI-A1.** A second statement from a second payer covering a
second obligation, reporting $840 of Series EE savings-bond interest in box 3,
with qualified education expenses claimed. The amount is deliberately not the
box-1 amount so that a result leaking in from the other fixture is visible
rather than plausible.

Iteration 1 had one fixture and produced TI-A1 by flipping two categorical
answers on the box-1 statement, so the case it claimed to execute was not the
case the scenario document specifies. Iteration 2 separates them.

All identities are `demo.*`. No real tax document, personal fact, or workspace
path enters the repository or an agent account.

## The shapes under comparison

Both derive through the **real engine expression evaluator**
(`packages/derivation/evaluator.py`) over a real `Environment`, so the
comparison measures the shapes rather than two hand-rolled calculators.

- **Shape A — distributed representation.** Ordinary facts plus tax rules
  publish independent artifacts, each carrying its own item, rule identity,
  substantive authority, and provenance. No durable statement relates them.
- **Shape A+ — distributed, with the partition edge.** Identical to A except
  that the artifact a later year carries also names what it is a part of. Still
  two artifacts from two rules; no item-level result object.
- **Shape B — explicit determination representation.** A recoverable
  item-level result holding the reported amount, the includible amount, the
  non-includible amount, the basis consequence, the item identity, the rule,
  the authority, and the source facts.

The candidate path must begin with **ordinary facts**. Neither shape may take
"$300 accrued-interest Schedule B adjustment" as its representation of the
circumstance — that is a legal classification, and supplying it to the engine
assumes away the question.

All shapes are held to **one execution and currentness policy**. A changed
dependency displaces every artifact whose provenance reads it, and a displaced
artifact is not servable as current merely because it has not been recomputed.
No shape may be given a selective-persistence behaviour the others do not have.

Iteration 1 also scored an unrepaired variant of shape A whose symbols carried
no item, rule, or authority. That is not a candidate anyone would build, and
scoring it inflated the apparent gap; it is dropped. **A+ replaces it** and
serves the opposite purpose: it exists to test whether A's remaining failure can
be repaired *without* A becoming B, so that "a durable relationship is
necessary" is not mistaken for "a new citizen kind is necessary".

## Required cases

| Case | Circumstance | Required outcome |
| --- | --- | --- |
| TI-B1 | No accrued interest | $1,200 includible; the result records why no adjustment applies |
| TI-B2 | $300 accrued interest paid to seller | $900 includible and a $300 basis reduction, with the user never supplying the legal classification |
| TI-N1 | Purchase between dates answered *yes*, amount not supplied | No result; the outstanding question identifiable; no silent $1,200 and no silent zero |
| TI-L1 | Source correction, box 1 $1,200 → $1,000 | Prior result displaced; $700 includible |
| TI-L2 | Circumstance correction, $300 → $250 | $950 includible |
| TI-A1 | Box-3 Series EE savings-bond interest, qualified education expenses claimed (§ 135) — outside the slice, and run on its own fixture | Coverage failure stated explicitly, not a wrong number |

## Evidence rubric

Success is **not** judged by the displayed number alone. Each shape is scored on
eleven requirements:

1. the statement report is recoverable and unmodified;
2. the ordinary purchase facts are recoverable;
3. the tax rule supplies the classification — the user is never asked for one;
4. the result identifies the item it concerns;
5. the declared relation naming which holding was bought is **read and verified
   against the item the statement covers**, and refuses on disagreement;
6. every input whose correction should displace the result appears in
   provenance;
7. substantive authority is attached to the result;
8. the $300 basis consequence is preserved;
9. the relationship among the amounts is recoverable from the artifact a later
   year carries;
10. the reporting projection is separate from the derived result;
11. missing facts and unsupported coverage fail explicitly.

Requirement 6 is scored against the fixture's **full declared fact set** — the
reported amount, the payer, the statement's obligation, the purchase question,
the accrued amount, the declared relation, the obligation kind, and the
education answer — plus the rule identity and version, the substantive
authority, and the coverage declaration. Iteration 1 named three facts, so
nothing could fail it. A rubric whose expected-input set omits a relevant fact
does not license the claim that all requirements pass.

Requirements 5, 6 and 9 are additionally exercised **adversarially**: each of
the eight facts is corrected after a result exists, and the observation is
currentness, refusal, item attribution, and provenance — not a number.

## Incumbent baseline

The incumbent is exercised through its **existing committed tests only**. Those
tests are a structural analogue at different amounts, not an execution of the
six semantic cases, and the examination must say which is which.

## Decision rule

- If the distributed shape satisfies the rubric and the later-year consumer, no
  new citizen is needed. Say so; do not manufacture a discriminator to force a
  recommendation.
- Prefer the explicit determination **only** if a concrete executed consumer
  fails under a fair distributed representation and succeeds because the
  determination holds a relationship distributed provenance cannot recover.
- Distinguish "a new citizen kind is necessary" from "some recoverable
  relationship or provenance edge is necessary". Shape A+ is the instrument for
  telling those apart.
- If the difference reduces to an owner-held product requirement, state the two
  product consequences plainly and do not claim necessity before that
  requirement is selected.
- If both work, compare actual complexity and failure modes drawn from the
  prototype, not from anticipation. Do not infer production cost, schema
  compatibility, or migration size from prototype dataclasses.
- If neither works, report the failed requirements and the smallest additional
  probe. Do not substitute another hypothetical design.

### Deciding evidence must be executed

A probe may not report a conclusion it did not compute. Two specific
prohibitions, both drawn from iteration 1's defects:

- **No hard-coded capability verdicts.** A claim that a shape cannot state
  something must come from asking the persisted artifacts, through a consumer
  performing a concrete task.
- **No manufactured currentness gaps.** A comparison may not selectively
  refresh one affected output while treating another affected output as
  standing. If partial refresh is claimed to be possible in a candidate
  architecture, the exact persistence mechanism that permits it must be
  identified and executed; otherwise it is not evidence.

## Boundary

These are prototype evidence shapes, not production contracts. This round does
not publish a schema, add a production citizen, change an accepted ADR, migrate
production content, or select a final storage mechanism.

## Stop condition

The round stops when every required case has executed under every shape, on its
own fixture, and the rubric and both probes have been scored — or when a shape
fails a requirement in a way no in-charter repair can address.

A round does not stop on a scored rubric alone if the rubric's expected-input
set is later found to omit a relevant fact. That is what happened at the end of
iteration 1, and it is why iteration 2 exists.
