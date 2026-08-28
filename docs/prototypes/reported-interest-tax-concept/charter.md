# Prototype Charter — Reported Interest to Tax Concept

**Topic:** `reported-interest-tax-concept`
**Current exhibit:** `exhibits/reported-interest-tax-concept/it5`
**Historical exhibits:** `it1`, `it2`, `it3`, `it4` (unchanged)
**Milestone:** Reported Interest to Tax Concept Vertical Slice

## Question

Does the engine need a separately recoverable item-level tax determination
between what a source document reports and what reaches the return, or can a
distributed representation satisfy the same requirements under stated
later-year access capabilities?

## Fixtures

**Box-1 fixture.** One synthetic taxpayer, one 2025 Form 1099-INT, box 1 =
$1,200, one obligation bought between interest dates, $300 paid to the seller
for already-accrued interest. All identities `demo.*`.

**Box-3 fixture, TI-A1.** A second statement, second payer, second obligation,
$840 of Series EE interest in box 3, education-expense answer `yes`. Sufficient
to refuse coverage. Not a complete § 135 fact pattern: no issuance year, owner
age, filing status, modified AGI, qualified expenses after reductions, or
redemption proceeds.

## Packagings

All derive through `packages.derivation.evaluator` over a real `Environment`.

Distributed packagings evaluate **separate** includible and basis rule
expressions, each with its own access log. The basis rule does not read the
reported amount or the payer. Provenance is never relabelled after execution.

| Id | Packaging | Carried basis payload |
| --- | --- | --- |
| A | artifact-alone | `{amount}` |
| C | embedded-composite | `{amount, reported, includible}` with per-field component provenance |
| E | relationship-edge | `{amount, sibling, reported_key}` |
| B | explicit determination | reported, includible, non-includible, basis on one object |

A source-report producer identifies and reads the statement value only. It
does not apply tax-slice coverage. Its support is the identified source fact,
not a blank form and not substantive tax authority. Tax-treatment artifacts
carry IRC § 61 / Publication 550. Treatment refusal must leave the source
report recoverable and unmodified.

E's pointers are followed only through explicitly granted object-store access.
A followed target must match requested key to self-key, item, kind, and exact
producing rule id and version, and (when granted) dependency currentness.
Copied payload fields on C keep the producing evaluation's exact rule identity.
A copied or referenced partition cannot support a current explanation after a
producing evaluation is displaced.

## Later-year access

In-memory Python object grants. Serialization, persistence, and cross-process
recovery are not executed.

1. artifact-object-only
2. artifact plus a currentness / version-resolution service
3. object-store access
4. full-workspace access

Artifact-object-only receives none of: source workspace, source facts, sibling
artifacts, undeclared version oracle. Without a currentness service the
consumer must not claim it detected an amendment.

## Required cases

| Case | Required outcome |
| --- | --- |
| TI-B1 | $1,200 includible |
| TI-B2 | $900 includible and $300 basis reduction; user never supplies the legal classification |
| TI-N1 | no result; outstanding question named |
| TI-L1 | prior result displaced where its provenance reads the corrected fact; $700 includible on recompute |
| TI-L2 | $950 includible on recompute |
| TI-A1 | tax treatment refuses coverage; the source report remains recoverable and unmodified. Do not treat the fixture as proof that full inclusion is the wrong number |

## Rubric

1. statement report unmodified
2. ordinary purchase facts recoverable
3. rule supplies the classification
4. result identifies the item
5. declared relation is read, verified against the statement item, and refuses on mismatch
6. each artifact's provenance matches the expression that ran and accounts for the facts that expression read
7. substantive authority attached to tax-treatment artifacts, not the source report
8. basis consequence published
9. reporting projection separate
10. missing facts and unsupported coverage fail explicitly

Task 6 of the later-year consumer is fact-version currentness of the
dependencies actually used, under fixed rule, authority, coverage, and
reporting assumptions. It is not general later-year usability.

Every declared fixture fact is corrected or removed after publication. Observe
currentness, refusal or recomputation, item attribution, and exact provenance
dependency. Relationship fields used by E are mutated the same way.

Do not record rule, authority, coverage-declaration, or reporting-artifact
succession as passing if they were not executed.

## Decision rule

- If a fair distributed packaging and the determination satisfy the actual
  requirements under the same access grant, say so. Do not manufacture a
  discriminator.
- Prefer the determination only if a concrete executed consumer fails under a
  fair distributed packaging and succeeds because the determination holds a
  relationship distributed provenance cannot recover.
- Distinguish a new citizen kind from a recoverable relationship or copied
  amounts. Do not infer citizen-kind, schema compatibility, or production cost
  from prototype dataclasses.
- Dependency currentness of a current partition explanation is settled: a
  displaced producing evaluation cannot support a current explanation. Remaining
  owner questions concern the product consequence of that split state.

## Boundary

Prototype evidence. No production schema, citizen, ADR, or content migration.
§ 135 is not implemented.
