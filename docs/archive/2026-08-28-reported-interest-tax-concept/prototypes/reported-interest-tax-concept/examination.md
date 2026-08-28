# Prototype Examination — Reported Interest to Tax Concept

**Current exhibit:** `exhibits/reported-interest-tax-concept/it6`
**Historical exhibits, unchanged:** `it1`, `it2`, `it3`, `it4`, `it5`
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

Later-year access is one of these **in-memory Python object grants**. The
exhibit does not execute serialization, deserialization, persistence,
cross-process recovery, or a durable storage schema.

1. **artifact-object-only** — the carried artifact object and nothing else
2. **currentness** — the artifact plus a version-resolution service
3. **object-store access** — the artifact plus an in-memory identity-addressable
   mapping of retained artifact objects
4. **full-workspace** — artifact, currentness, object-store access, and the
   source-year workspace

An artifact-object-only consumer is not given the source workspace, source
facts, sibling artifacts, or a version oracle. Without a currentness service it
does not claim to have detected an amendment.

**Test result, from the exhibit tree:**
`pytest tests/test_reported_interest_prototype.py -n0` → **40 passed, 493
subtests passed in 0.09s**.

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
(5) recover the recorded partition explanation — reconstruct the source-year
partition of reported / includible / basis amounts from the carried object or
followed objects; (6) decide fact-version currentness of the dependencies
actually used, under the assumption that rule, authority, coverage declaration,
and reporting contract are unchanged. Task 6 does not decide general later-year
usability.

Task 5 true and task 6 unknown means a recorded explanation is recoverable but
currentness is unknown. Task 5 true and task 6 false
(`fact_version_current=False`) means the recoverable explanation is historical.
Task 5 true and task 6 true (`fact_version_current=True`) is required before
this publication may call the result a current explanation under the
prototype's bounded assumptions. An unamended fixture is harness knowledge, not
a capability granted to the later-year consumer.

Unamended TI-B2, tasks passed (counts unchanged; meaning restated):

| Packaging | artifact-object-only | currentness | object-store access | full-workspace |
| --- | --- | --- | --- | --- |
| A | 3/6 | 5/6 | 3/6 | 6/6 |
| C | 4/6 | 6/6 | 4/6 | 6/6 |
| E | 3/6 | 5/6 | 4/6 | 6/6 |
| B | 4/6 | 6/6 | 4/6 | 6/6 |

Artifact-object-only never answers tasks 4 or 6. **C** and **B** with
artifact-object-only recover the recorded partition but cannot establish
currentness. **E** with object-store access recovers the recorded partition but
cannot establish currentness. Object-store access is not a currentness grant. A
current explanation requires both reconstruction (task 5) and a currentness
grant whose used dependencies match (task 6).

Task 5 when the source year is unamended:

- **A** recovers the recorded partition only with the full source-year
  workspace.
- **C** recovers it from copied amounts, including artifact-object-only. Each
  copied field keeps the provenance of the evaluation that produced it,
  including exact producing rule id and version.
- **E** recovers it only by following `sibling` and `reported_key` through
  object-store access, and only when each target's self-key, item, kind, and
  producing rule id/version match. Following a retained object reconstructs the
  recorded partition; it does not establish currentness.
- **B** recovers it from the carried object, including artifact-object-only.

After an accrued-amount amendment, every packaging with a currentness service
reports the carried artifact displaced and `fact_version_current=False`.

After a reported-amount correction (1200 → 1000):

- **C** with currentness: the recorded partition remains recoverable from the
  copies (task 5); the basis amount remains independently current
  (`carried_displaced=False`); used-dependency currentness is false, so the
  recoverable explanation is historical.
- **B** with currentness: the whole object is displaced
  (`carried_displaced=True`); the recorded amounts remain on the object
  (task 5) and used-dependency currentness is false.
- **E** with full-workspace: retained targets still reconstruct the recorded
  partition (task 5); used-dependency currentness is false. Same-valued targets
  are still rejected for foreign item, wrong kind, wrong producing rule, wrong
  rule version, or store lookup key differing from the artifact's self-key.

**Settled invariant.** A copied or referenced partition cannot support a
*current* explanation after an evaluation that produced one of its components
has been displaced. That is provenance correctness, not an owner-selectable
policy. Reconstruction of the recorded partition (task 5) is not that grant.

## Relationship fields

On E, with object-store access:

- intact same-item, correct-kind, correct-producer, matching self-key pointers
  → task 5 recovers the recorded partition;
- `sibling` or `reported_key` removed, missing, foreign-item, wrong-kind,
  wrong producing rule, wrong rule version, or self-key mismatch → task 5
  fails;
- empty store → task 5 fails;
- a displaced retained target, when currentness is also granted → task 5 still
  recovers the recorded partition; task 6 reports `fact_version_current=False`.

On C, pointer corruption is ignored; removing copied amounts fails task 5; a
mutated component producer fails task 5; stale copied amounts still reconstruct
the recorded partition (task 5) and are historical under task 6 once a
currentness service is granted.

The source-report artifact is published independently of tax-slice coverage
and of tax authority. Its support is the exact statement reads (reported
amount, payer, obligation). Its substantive tax-authority collection is empty
and accrued-interest coverage id/version are absent; `accounted()` marks
`authority:omitted` and `coverage:omitted`. Treatment artifacts retain
IRC § 61 / Publication 550 and the accrued-interest coverage declaration. On
TI-A1 the tax treatment returns `SLICE_COVERAGE_UNSUPPORTED` and the source
report of $840 remains recoverable and unmodified.

## What the evidence supports

**A separately recoverable item-level determination is not established as
necessary. No representation is recommended on necessity grounds.**

C and B are not interchangeable under a source correction: B is wholly
displaced; C's basis amount can remain current while its copied partition is a
historical recorded explanation. E is not a self-sufficient edge: it needs an
object store and validation of self-key, item, kind, and exact producing rule
id/version. Object-store access recovers the recorded partition; it does not
establish currentness. Those are executed differences in retained capability
and dependency currentness, not a proof that a new citizen kind is required.

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

A copied or referenced partition cannot be treated as a *current* explanation
once a producing evaluation is displaced. What remains open is the product
consequence of that split state, for example:

- recompute a current explanation;
- retain the old explanation explicitly as historical;
- withhold a current explanation;
- decide whether an independently current basis amount supports some
  specifically named later-year task.

The exhibit measured in-memory object grants (artifact-object-only,
currentness, object-store access, full-workspace), not serialization or
durable storage. Rule, authority, coverage, and reporting succession remain
outside the executed currentness service.

## Open

- Rule, authority, coverage-declaration, and reporting-artifact succession.
- Any § 135 computation; this remains an outside-slice coverage probe.
- Production representation, schema, and citizen kind.
