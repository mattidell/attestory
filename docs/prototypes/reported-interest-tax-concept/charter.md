# Prototype Charter — Reported Interest to Tax Concept

**Topic:** `reported-interest-tax-concept`
**Exhibit tag:** `exhibits/reported-interest-tax-concept/it1`
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

## Fixture

One synthetic taxpayer. One 2025 Form 1099-INT, one logical statement, one
identified obligation, box 1 = $1,200. The taxpayer bought the obligation
between interest payment dates and paid the seller $300 of interest that had
already accrued.

All identities are `demo.*`. No real tax document, personal fact, or workspace
path enters the repository or an agent account.

## The two shapes under comparison

Both derive through the **real engine expression evaluator**
(`packages/derivation/evaluator.py`) over a real `Environment`, so the
comparison measures the two shapes rather than two hand-rolled calculators.

- **Shape A — distributed representation.** Ordinary facts plus a tax rule
  derive an item-linked result. No durable determination object exists; the
  outputs are independent symbols.
- **Shape B — explicit determination representation.** A recoverable
  item-level result holding the reported amount, the includible amount, the
  non-includible amount, the basis consequence, the item identity, the rule,
  the authority, and the source facts.

The candidate path must begin with **ordinary facts**. Neither shape may take
"$300 accrued-interest Schedule B adjustment" as its representation of the
circumstance — that is a legal classification, and supplying it to the engine
assumes away the question.

A third variant, **A-repaired**, was added mid-round: shape A with authority
attached per symbol. Its purpose is to test whether A's one static failure can
be repaired without A becoming B.

## Required cases

| Case | Circumstance | Required outcome |
| --- | --- | --- |
| TI-B1 | No accrued interest | $1,200 includible; the result records why no adjustment applies |
| TI-B2 | $300 accrued interest paid to seller | $900 includible and a $300 basis reduction, with the user never supplying the legal classification |
| TI-N1 | Purchase between dates answered *yes*, amount not supplied | No result; the outstanding question identifiable; no silent $1,200 and no silent zero |
| TI-L1 | Source correction, box 1 $1,200 → $1,000 | Prior result displaced; $700 includible |
| TI-L2 | Circumstance correction, $300 → $250 | $950 includible |
| TI-A1 | Savings bond, qualified education expenses claimed (§ 135) — outside the slice | Coverage failure stated explicitly, not a wrong number |

## Evidence rubric

Success is **not** judged by the displayed number alone. Each shape is scored on
ten requirements:

1. the statement report is recoverable and unmodified;
2. the ordinary purchase facts are recoverable;
3. the tax rule supplies the classification — the user is never asked for one;
4. the result identifies the item it concerns;
5. every input whose correction should displace the result appears in provenance;
6. substantive authority is attached to the result;
7. the $300 basis consequence is preserved;
8. source correction and circumstance correction have independent lifecycle
   effects;
9. the reporting projection is separate from the derived result;
10. missing facts and unsupported coverage fail explicitly.

## Incumbent baseline

The incumbent is exercised through its **existing committed tests only**. Those
tests are a structural analogue at different amounts, not an execution of the
six semantic cases, and the examination must say which is which.

## Decision rule

- If the distributed shape satisfies the rubric, no new citizen is needed.
- If it cannot preserve item linkage, authority, basis, lifecycle, and
  explanation without effectively recreating the determination across unrelated
  artifacts, recommend the explicit determination.
- If both work, compare actual complexity and failure modes drawn from the
  prototype, not from anticipation.
- If neither works, report the failed requirements and the smallest additional
  probe. Do not substitute another hypothetical design.

## Boundary

These are prototype evidence shapes, not production contracts. This round does
not publish a schema, add a production citizen, change an accepted ADR, migrate
production content, or select a final storage mechanism.

## Stop condition

The round stops when every required case has executed under both shapes and the
rubric has been scored, or when a shape fails a requirement in a way no
in-charter repair can address.
