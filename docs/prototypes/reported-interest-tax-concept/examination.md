# Prototype Examination — Reported Interest to Tax Concept

**Current exhibit:** `exhibits/reported-interest-tax-concept/it4`
**Historical exhibits, unchanged:** `it1`, `it2`, `it3`
**Charter:** [charter.md](charter.md)

Prototype code is not on the milestone branch.

## The question

Does the accrued-interest-at-purchase case require a separately recoverable
item-level tax determination, or can a distributed representation satisfy the
same requirements under stated later-year access capabilities?

## What was executed

Four packagings, the real `packages.derivation.evaluator`, one shared
source-year currentness policy (`Store.serve` refuses a displaced artifact),
and a later-year consumer that receives only the capabilities named for that
run.

Distributed packagings **A**, **C**, and **E** each evaluate an includible rule
and a basis rule through the evaluator, each with its own `AccessLog`. The
basis rule does not read the reported amount or the payer. **B** evaluates one
determination rule. A rule id in provenance is the expression that ran.

| Packaging | What the carried basis artifact holds |
| --- | --- |
| **A** artifact-alone | `{amount}` |
| **C** embedded-composite | `{amount, reported, includible}` plus per-field component provenance |
| **E** relationship-edge | `{amount, sibling, reported_key}` — pointers, no partition amounts |
| **B** explicit determination | reported, includible, non-includible, and basis amounts on one object |

Later-year access is one of:

1. **bytes-only** — the carried artifact and nothing else
2. **currentness** — the artifact plus a version-resolution service
3. **object-store** — the artifact plus an identity-addressable store of retained artifacts
4. **full-workspace** — artifact, currentness, object store, and the source-year workspace

A bytes-only consumer is not given the source workspace, source facts, sibling
artifacts, or a version oracle. Without a currentness service it does not claim
to have detected an amendment.

**Test result, from the exhibit tree:**
`pytest tests/test_reported_interest_prototype.py -n0` → **32 passed, 455
subtests passed in 0.08s**.

## Case outcomes

Identical across A / C / E / B.

| Case | Outcome |
| --- | --- |
| TI-B1 | line 2b = 1200 |
| TI-B2 | line 2b = 900; basis reduction 300 |
| TI-N1 | blocked `DEPENDENCY_ABSENT` (accrued-interest-paid-to-seller) |
| TI-L1 | line 2b = 700 |
| TI-L2 | line 2b = 950 |
| TI-A1 | blocked `SLICE_COVERAGE_UNSUPPORTED` |

Arithmetic does not discriminate.

TI-A1 is a distinct box-3 Series EE fixture ($840, second statement, second
obligation, education answer `yes`). The fixture does not record issuance year,
owner age, filing status, modified AGI, qualified expenses after reductions, or
redemption proceeds. Coverage refusal is the required prototype behaviour. The
fixture does **not** establish a positive § 135 exclusion, so it does not prove
that full inclusion is the wrong number for this taxpayer.

## Separate rules

On TI-B2, shape A:

- includible rule `demo.rule.includible-interest.v3` reads the reported amount,
  payer, obligation, purchase question, accrued amount, relation, obligation
  kind, and education answer;
- basis rule `demo.rule.basis-reduction.v3` reads the obligation, purchase
  question, accrued amount, relation, obligation kind, and education answer —
  **not** the reported amount, **not** the payer.

Correcting the reported amount or the payer displaces the includible artifact
and leaves the basis artifact current. Correcting the accrued amount, relation,
obligation kind, or education answer displaces both. That is observed, not
stamped.

Rule succession, authority succession, coverage-declaration succession, and
reporting-artifact succession were **not** executed. They remain open.

## Later-year consumer (six tasks)

Tasks: (1) identify the obligation; (2) recover the basis reduction with its
rule and authority; (3) identify the ordinary fact that supplied the amount;
(4) detect a source-year amendment of the *carried* artifact's own provenance;
(5) explain why the basis reduction exists as a *current* partition of reported
interest; (6) decide fact-version currentness of the dependencies actually
used, under the assumption that rule, authority, coverage declaration, and
reporting contract are unchanged. Task 6 does not decide general later-year
usability.

Unamended TI-B2, tasks passed:

| Packaging | bytes-only | currentness | object-store | full-workspace |
| --- | --- | --- | --- | --- |
| A | 3/6 | 5/6 | 3/6 | 6/6 |
| C | 4/6 | 6/6 | 4/6 | 6/6 |
| E | 3/6 | 5/6 | 4/6 | 6/6 |
| B | 4/6 | 6/6 | 4/6 | 6/6 |

Bytes-only never answers tasks 4 or 6. Task 5 when the source year is unamended:

- **A** recovers the partition only with the full source-year workspace.
- **C** recovers it from copied amounts, including bytes-only. Each copied
  field keeps the provenance of the evaluation that produced it.
- **E** recovers it only by following `sibling` and `reported_key` through an
  object store, and only when each target matches the carried item and expected
  kind.
- **B** recovers it from the carried object, including bytes-only.

After an accrued-amount amendment, every packaging with a currentness service
reports the carried artifact displaced and `fact_versions_current=False`.

After a reported-amount correction (1200 → 1000):

- **C** with currentness: the basis amount remains current
  (`carried_displaced=False`); the copied reported and includible fields are
  identified as historical snapshots; task 5 fails as a current explanation;
  used-dependency currentness is false.
- **B** with currentness: the whole object is displaced
  (`carried_displaced=True`).
- **E** with full-workspace: followed targets are displaced; task 5 fails;
  used-dependency currentness is false. Same-valued targets belonging to
  another item are rejected (`foreign-item`). Wrong-kind targets are rejected.

C's copied fields are not current merely because the basis amount is current.
E's pointers are not current merely because the carried basis artifact is
current.

## Relationship fields

On E, with an object store:

- intact same-item, correct-kind pointers → task 5 passes;
- `sibling` or `reported_key` removed, missing, foreign-item, or wrong-kind →
  task 5 fails;
- empty store → task 5 fails;
- displaced target, when currentness is also granted → task 5 fails.

On C, pointer corruption is ignored; removing copied amounts fails task 5;
stale copied amounts fail task 5 once a currentness service is granted.

E's reported-interest artifact cites Form 1099-INT as statement support, not
IRC § 61 / Publication 550.

## What the evidence supports

**A separately recoverable item-level determination is not established as
necessary. No representation is recommended on necessity grounds.**

C and B are not interchangeable under a source correction: B is wholly
displaced; C's basis amount can remain current while its copied partition is a
stale snapshot. E is not a self-sufficient edge: it needs an object store, item
and kind validation, and target currentness. Those are executed differences in
retained capability and dependency currentness, not a proof that a new citizen
kind is required.

Whether a production schema for any packaging would be a new citizen kind
depends on a declared schema and consumer contract. This milestone does not
select one. Production cost, schema compatibility, and migration size were not
measured.

## TI-A1 and the incumbent

`package.core-calculations.v33` selects `tax.us.2025.rule.form1040-line2b` v4.
`rule.f1099int-b3-subtotal.json` publishes the box-3 subtotal as an addend.
The rule's `when` requires family closure and a non-negative result. It does
not pin a Form 8815 or § 135 fact. No committed rule computes the § 135
exclusion.

`tax.us.2025.ss-benefits-scope.no-form-8815` exists and is consumed by the
Social Security Benefits Worksheet rules. It does not scope line 2b.

The incumbent therefore **cannot determine whether a § 135 exclusion applies**
and **may publish full inclusion of box 3** without representing the statutory
conditions (issuance after 1989, owner age, qualifying ownership, filing
status, modified AGI, qualified expenses after reductions, redemption proceeds
and the Form 8815 proportion). That is the coverage omission. It is not a
proof that $840 is the wrong number for the TI-A1 fixture, because that
fixture does not establish a positive exclusion.

All four prototype packagings refuse coverage on TI-A1.

## Incumbent baseline

`tests/test_schedule_b_interest_adjustments.py` and
`tests/tax/test_track2_line2b.py` — exact execution of committed incumbent
tests; a structural analogue at different amounts ($2,000 box 1 less $100
already-classified accrued-interest adjustment → $1,900); not an execution of
the six semantic cases. The incumbent has no representation of the ordinary
purchase question.

## Remaining owner decision

When a later year needs the basis consequence:

1. which retained capabilities are granted (artifact bytes; fact-version
   currentness of used dependencies; an object store of validated targets; the
   source-year workspace);
2. whether a copied or pointed-to partition may be treated as current only
   while its producing evaluations remain current — the prototype now
   distinguishes those cases, and the product still has to choose the rule.

Rule, authority, coverage, and reporting succession remain outside the executed
currentness service. Selecting a packaging before selecting those grants would
reverse the dependency.

## Open

- Rule, authority, coverage-declaration, and reporting-artifact succession.
- Any § 135 computation; this remains an outside-slice coverage probe.
- Production representation, schema, and citizen kind.
